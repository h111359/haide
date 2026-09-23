"""Typed test execution and kernel-enforced child-process confinement.

Linux Landlock ABI >=3 controls readable/ writable paths for the entire process
lineage. seccomp denies metadata/namespace/ptrace escapes and session detachment.
No unsupported-platform or missing-kernel fallback launches a process.
"""
from __future__ import annotations
import ctypes
import ctypes.util
import errno
import json
import os
from pathlib import Path
import platform
import queue
import re
import signal
import subprocess
import sys
import threading
import time
import uuid

sys.dont_write_bytecode = True
from security import Workspace, BoundaryError, digest
from storage import Store, now, sanitize


class ExecutionError(ValueError):
    def __init__(self, message, code="execution_blocked", details=None):
        super().__init__(message)
        self.code, self.details = code, details or {}


# Landlock ABI filesystem rights. Rights absent in the host ABI are not requested.
EXECUTE = 1 << 0
WRITE_FILE = 1 << 1
READ_FILE = 1 << 2
READ_DIR = 1 << 3
REMOVE_DIR = 1 << 4
REMOVE_FILE = 1 << 5
MAKE_CHAR = 1 << 6
MAKE_DIR = 1 << 7
MAKE_REG = 1 << 8
MAKE_SOCK = 1 << 9
MAKE_FIFO = 1 << 10
MAKE_BLOCK = 1 << 11
MAKE_SYM = 1 << 12
REFER = 1 << 13
TRUNCATE = 1 << 14
READ = READ_FILE | READ_DIR
WRITE = WRITE_FILE | REMOVE_DIR | REMOVE_FILE | MAKE_DIR | MAKE_REG | MAKE_SYM | REFER | TRUNCATE


def confinement_diagnostics():
    result = {"platform": platform.system(), "backend": "linux-landlock-seccomp", "available": False,
              "storage": "local filesystem, advisory flock, same-directory rename and fsync; shared/synchronized filesystems untested"}
    if sys.platform != "linux" or platform.machine() not in ("x86_64", "aarch64"):
        return {**result, "reason": "Managed subprocesses require Linux x86_64/aarch64 with Landlock ABI >=3 and libseccomp; Windows users can run AIH inside a compatible WSL2 distribution."}
    libc = ctypes.CDLL(None, use_errno=True)
    abi = libc.syscall(444, 0, 0, 1)
    try:
        ctypes.CDLL("libseccomp.so.2")
        lib = "libseccomp.so.2"
    except OSError:
        lib = None
    if abi < 3 or not lib:
        return {**result, "landlock_abi": abi, "reason": "Landlock ABI >=3 and libseccomp are required; launch is blocked without enforceable write/read confinement."}
    return {**result, "available": True, "landlock_abi": abi, "seccomp": lib}


def _restrict(paths, network, *, allow_session_creation=False):
    """Called only in the fresh child immediately before exec, never on the server."""
    libc = ctypes.CDLL(None, use_errno=True)
    abi = libc.syscall(444, 0, 0, 1)
    if abi < 3:
        raise ExecutionError("Landlock is unavailable")
    class Ruleset(ctypes.Structure):
        _fields_ = [("handled_access_fs", ctypes.c_uint64)]
    class Beneath(ctypes.Structure):
        _pack_ = 1
        _fields_ = [("allowed_access", ctypes.c_uint64), ("parent_fd", ctypes.c_int32)]
    handled = (1 << 15) - 1
    rules = Ruleset(handled)
    rulesfd = libc.syscall(444, ctypes.byref(rules), ctypes.sizeof(rules), 0)
    if rulesfd < 0:
        raise ExecutionError(f"Cannot create Landlock ruleset: errno {ctypes.get_errno()}")
    try:
        for path, rights, expected_identity in paths:
            if path == "/proc/self":
                path = f"/proc/{os.getpid()}"
            fd = os.open(path, os.O_PATH | os.O_CLOEXEC | os.O_NOFOLLOW)
            try:
                target_stat = os.fstat(fd)
                if expected_identity is not None and [target_stat.st_dev, target_stat.st_ino] != expected_identity:
                    raise ExecutionError("A confinement target changed between validation and launch")
                if not Path(path).is_dir():
                    rights &= READ_FILE | WRITE_FILE | EXECUTE | TRUNCATE
                entry = Beneath(rights, fd)
                if libc.syscall(445, rulesfd, 1, ctypes.byref(entry), 0) < 0:
                    raise ExecutionError(f"Cannot establish confinement for {path}: errno {ctypes.get_errno()}")
            finally:
                os.close(fd)
        if libc.prctl(38, 1, 0, 0, 0) != 0 or libc.syscall(446, rulesfd, 0) != 0:
            raise ExecutionError(f"Cannot enforce Landlock: errno {ctypes.get_errno()}")
    finally:
        os.close(rulesfd)
    library = "libseccomp.so.2"
    sec = ctypes.CDLL(library, use_errno=True)
    sec.seccomp_init.argtypes = [ctypes.c_uint32]
    sec.seccomp_init.restype = ctypes.c_void_p
    sec.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
    sec.seccomp_syscall_resolve_name.restype = ctypes.c_int
    sec.seccomp_rule_add.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint]
    sec.seccomp_load.argtypes = [ctypes.c_void_p]
    sec.seccomp_release.argtypes = [ctypes.c_void_p]
    ctx = sec.seccomp_init(0x7fff0000)  # SCMP_ACT_ALLOW
    if not ctx:
        raise ExecutionError("Cannot create seccomp filter")
    forbidden = ["chmod", "fchmod", "fchmodat", "fchmodat2", "chown", "fchown", "lchown", "fchownat",
                 "utime", "utimes", "futimesat", "utimensat", "setxattr", "lsetxattr", "fsetxattr", "removexattr", "lremovexattr", "fremovexattr",
                 "ptrace", "process_vm_writev", "process_vm_readv", "mount", "umount2", "pivot_root", "chroot",
                 "setns", "unshare", "bpf", "io_uring_setup", "open_by_handle_at", "name_to_handle_at",
                 "setsid", "setpgid", "link", "linkat", "mknod", "mknodat", "kexec_load", "reboot"]
    if allow_session_creation:
        # Explicit browser-validation supervisors own/reap detached native
        # helpers. Production _exec never enables this narrow exception.
        forbidden = [name for name in forbidden if name not in ("setsid", "setpgid")]
    if not network:
        forbidden += ["socket", "connect", "bind", "listen", "accept", "accept4"]
    try:
        for name in forbidden:
            num = sec.seccomp_syscall_resolve_name(name.encode())
            if num >= 0 and sec.seccomp_rule_add(ctx, 0x00050000 | errno.EPERM, num, 0) != 0:
                raise ExecutionError(f"Cannot install seccomp syscall rule: {name}")
        if sec.seccomp_load(ctx) != 0:
            raise ExecutionError("Cannot enforce seccomp")
    finally:
        sec.seccomp_release(ctx)


def process_identity(pid):
    try:
        content = Path(f"/proc/{pid}/stat").read_text()
        after = content[content.rfind(")") + 2:].split()
        return {"pid": pid, "start_ticks": after[19], "pgid": int(after[2])}
    except (OSError, IndexError, ValueError):
        return None


def process_alive(identity):
    if identity and "identity" in identity:
        if identity.get("termination_confirmed"):
            return False
        identity = identity["identity"]
    if not identity:
        return False
    actual = process_identity(identity["pid"])
    if actual:
        # Reuse/mismatch is uncertainty, never affirmative proof of termination.
        return True
    return bool(identity.get("pgid") and _group_alive(identity["pgid"]))


def _group_alive(pgid):
    # Zombies cannot mutate files; exclude them while waiting for a parent to reap.
    for name in os.listdir("/proc"):
        if name.isdigit():
            try:
                text = Path(f"/proc/{name}/stat").read_text()
                fields = text[text.rfind(")") + 2:].split()
                if int(fields[2]) == pgid and fields[0] != "Z":
                    return True
            except (OSError, IndexError, ValueError):
                continue
    return False


def stop_process(identity, grace=2.0):
    """Stop a verified controlled group. A missing leader alone is insufficient."""
    if identity and "identity" in identity:
        identity = identity["identity"]
    if not identity or not identity.get("pgid") or identity["pgid"] == os.getpgrp():
        return {"confirmed": False, "termination_confirmed": False, "reason": "Missing or unsafe process identity"}
    actual = process_identity(identity["pid"])
    if actual and actual["start_ticks"] != identity.get("start_ticks"):
        return {"confirmed": False, "termination_confirmed": False, "reason": "PID was reused; reconciliation required"}
    pgid = identity["pgid"]
    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return {"confirmed": True, "termination_confirmed": True, "status": "already_stopped"}
    deadline = time.monotonic() + grace
    while time.monotonic() < deadline and _group_alive(pgid):
        time.sleep(0.03)
    if _group_alive(pgid):
        try:
            os.killpg(pgid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        deadline = time.monotonic() + grace
        while time.monotonic() < deadline and _group_alive(pgid):
            time.sleep(0.03)
    confirmed = not _group_alive(pgid)
    return {"confirmed": confirmed, "termination_confirmed": confirmed, "status": "stopped" if confirmed else "termination_uncertain"}


class Confinement:
    def __init__(self, workspace):
        self.workspace = workspace

    def diagnostics(self):
        return confinement_diagnostics()

    def prepare(self, command, *, cwd, write_scope, runtime_ref, env=None, credential_paths=None, network=False):
        status = self.diagnostics()
        if not status["available"]:
            raise ExecutionError(status["reason"], details=status)
        if not isinstance(command, list) or not command or not all(isinstance(s, str) and "\0" not in s for s in command):
            raise ExecutionError("Commands must be trusted typed argument arrays")
        executable = Path(command[0])
        if not executable.is_absolute() or not executable.is_file():
            raise ExecutionError("A trusted absolute installed executable is required")
        executable = executable.resolve()
        working = self.workspace.resolve(cwd, must_exist=True)
        if not working.is_dir():
            raise ExecutionError("The working directory must be a registered directory")
        scopes = list(write_scope or [])
        if runtime_ref not in scopes:
            scopes.append(runtime_ref)
        # No writable root grants that would include protected core/state. File
        # and directory grants are resolved independently; root membership alone
        # never grants a process implementation authority.
        for ref in scopes:
            rid, parts = self.workspace.parse(ref)
            if not parts or (rid == "home" and parts[0] in (".aih", ".aih_product")):
                raise ExecutionError("Process writes require narrow normal-product locations; core and product state remain protected")
            self.workspace.resolve(ref, write=True, scope=scopes)
        self.workspace.mkdir(runtime_ref, scope=scopes)
        runtime = self.workspace.resolve(runtime_ref, write=True, scope=scopes)
        paths = []
        for root in self.workspace.roots.values():
            self.workspace.resolve(root["id"] + ":", must_exist=True)
            paths.append((root["path"], READ))
        for name in ("/usr", "/bin", "/sbin", "/lib", "/lib64"):
            if Path(name).exists():
                paths.append((str(Path(name).resolve()), READ | EXECUTE))
        # Minimal documented host prerequisites; no arbitrary user-home read.
        for name in ("/etc/ld.so.cache", "/etc/ld.so.conf", "/etc/ssl", "/etc/resolv.conf", "/etc/hosts", "/etc/nsswitch.conf", "/etc/localtime", "/dev/null", "/dev/urandom", "/dev/random", "/proc/self"):
            if Path(name).exists():
                paths.append((name, READ))
        paths.append((str(executable.parent), READ | EXECUTE))
        # Python needs this immutable launcher and its local imports. These are
        # read/execute prerequisites even for an isolated copied product fixture.
        paths.append((str(Path(__file__).resolve().parents[1]), READ | EXECUTE))
        for path in credential_paths or []:
            path = Path(path)
            if not path.is_absolute() or not (path.is_file() or path.is_dir()):
                raise ExecutionError("A host prerequisite reference must name an existing file/directory")
            paths.append((str(path.resolve()), READ))
        for ref in scopes:
            target = self.workspace.resolve(ref, write=True, scope=scopes)
            if not target.exists():
                raise ExecutionError(f"Declare an existing writable output/cache directory before launch: {ref}")
            # Hardlinks within writable directories can alias unregistered files.
            if target.is_dir():
                for directory, dirs, files in os.walk(target, followlinks=False):
                    for name in dirs + files:
                        self.workspace.resolve(self.workspace.reference(Path(directory) / name), write=True, scope=scopes)
            paths.append((str(target), READ | WRITE))
        paths.append(("/dev/null", READ_FILE | WRITE_FILE))
        clean = {"PATH": os.pathsep.join([str(executable.parent), "/usr/bin", "/bin"]), "LANG": "C.UTF-8",
                 "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUNBUFFERED": "1", "TMPDIR": str(runtime),
                 "TEMP": str(runtime), "TMP": str(runtime), "XDG_CACHE_HOME": str(runtime / "cache"),
                 "XDG_CONFIG_HOME": str(runtime / "config"), "XDG_DATA_HOME": str(runtime / "data"),
                 "XDG_STATE_HOME": str(runtime / "state"), "XDG_RUNTIME_DIR": str(runtime), "AIH_MANAGED_CHILD": "1", "AIH_WORKSPACE_REVISION": str(self.workspace.revision),
                 "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull, "GIT_OPTIONAL_LOCKS": "0"}
        for key, value in (env or {}).items():
            if not re.fullmatch(r"[A-Z][A-Z0-9_]*", key) or key in ("LD_PRELOAD", "LD_LIBRARY_PATH", "PYTHONPATH", "PYTHONSTARTUP"):
                raise ExecutionError("Unsafe environment setting")
            clean[key] = value
        pinned_paths = []
        for target, rights in paths:
            if target != "/proc/self":
                target = str(Path(target).resolve())
            target_stat = os.stat(target)
            identity = None if target == "/proc/self" else [target_stat.st_dev, target_stat.st_ino]
            pinned_paths.append((target, rights, identity))
        config = {"paths": pinned_paths, "network": bool(network), "command": [str(executable), *command[1:]]}
        launcher = [sys.executable, "-B", str(Path(__file__).resolve()), "_exec", json.dumps(config, separators=(",", ":"))]
        return launcher, str(working), clean


def run_process(command, workspace, *, cwd="home:", write_scope=None, runtime_ref=None, timeout=300,
                env=None, credential_paths=None, network=False, on_event=None, stop_event=None,
                operation_id=None, output_ref=None, on_start=None, stdin_text=None):
    opid = operation_id or "run-" + uuid.uuid4().hex
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,100}", opid):
        raise ExecutionError("Invalid operation identity")
    runtime_ref = runtime_ref or f"home:.aih_runtime/{opid}"
    launcher, working, clean = Confinement(workspace).prepare(command, cwd=cwd, write_scope=write_scope or [],
                              runtime_ref=runtime_ref, env=env, credential_paths=credential_paths, network=network)
    started = now()
    store = Store(workspace.home)
    identity_ref = f"ledger/operations/{opid}/process.json"
    gate_config = json.loads(launcher[-1])
    gate_config["ownership_record"] = str(store.path(identity_ref))
    launcher[-1] = json.dumps(gate_config, separators=(",", ":"))
    proc = subprocess.Popen(launcher, cwd=working, env=clean, stdin=subprocess.PIPE if stdin_text is not None else subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True, text=True,
                            encoding="utf-8", errors="replace", bufsize=1)
    identity = process_identity(proc.pid)
    try:
        store.write(identity_ref, {"operation_id": opid, "identity": identity, "status": "running", "started": started,
                                   "workspace_revision": workspace.revision, "write_scope": write_scope or [], "runtime_ref": runtime_ref})
        if on_start:
            on_start(identity)
    except BaseException:
        stop_process(identity)
        proc.wait(timeout=5)
        raise
    if stdin_text is not None:
        try:
            proc.stdin.write(stdin_text)
            proc.stdin.close()
        except BrokenPipeError:
            pass
    events = queue.Queue()
    def reader(stream, kind):
        for line in iter(stream.readline, ""):
            events.put((kind, line))
        stream.close()
    threads = [threading.Thread(target=reader, args=(proc.stdout, "stdout"), daemon=True),
               threading.Thread(target=reader, args=(proc.stderr, "stderr"), daemon=True)]
    for thread in threads:
        thread.start()
    output, error, stopped, timed_out = [], [], False, False
    secret_values = [v for k, v in (env or {}).items() if re.search(r"(?:KEY|TOKEN|SECRET|PASSWORD|AUTH)", k) and isinstance(v, str) and len(v) >= 6]
    # Authentication remains at its permitted host reference. Exact values are
    # held only in memory to suppress accidental tool echoes, including opaque
    # refresh credentials with no recognizable provider prefix.
    def collect_credentials(value, sensitive=False):
        if isinstance(value, dict):
            for key, item in value.items():
                collect_credentials(item, sensitive or bool(re.search(r"(?i)(key|token|secret|password|credential)", key)))
        elif isinstance(value, list):
            for item in value:
                collect_credentials(item, sensitive)
        elif sensitive and isinstance(value, str) and len(value) >= 6:
            secret_values.extend([value, *[line for line in value.splitlines() if len(line) >= 6]])
    for reference in credential_paths or []:
        credential_file = Path(reference)
        try:
            if credential_file.is_file() and credential_file.stat().st_size <= 1024 * 1024:
                if credential_file.suffix == ".json":
                    collect_credentials(json.loads(credential_file.read_text("utf-8")))
                elif credential_file.suffix == ".toml":
                    import tomllib
                    collect_credentials(tomllib.loads(credential_file.read_text("utf-8")))
                elif credential_file.suffix in (".pem", ".key"):
                    collect_credentials(credential_file.read_text("utf-8"), True)
        except (OSError, UnicodeError, ValueError):
            pass
    def safe_output(line):
        for secret in secret_values:
            line = line.replace(secret, "[redacted credential]")
        try:
            return json.dumps(sanitize(json.loads(line)), ensure_ascii=False) + "\n"
        except json.JSONDecodeError:
            return sanitize(line)
    start = time.monotonic()
    termination = {"confirmed": False}
    while proc.poll() is None or any(thread.is_alive() for thread in threads) or not events.empty():
        if proc.poll() is not None and _group_alive(identity["pgid"]):
            termination = stop_process(identity)
        if proc.poll() is None and ((stop_event and stop_event.is_set()) or time.monotonic() - start > timeout):
            stopped = bool(stop_event and stop_event.is_set())
            timed_out = not stopped
            termination = stop_process(identity)
        try:
            kind, line = events.get(timeout=0.05)
        except queue.Empty:
            continue
        safe = safe_output(line)
        (output if kind == "stdout" else error).append(safe)
        if on_event:
            try:
                on_event({"type": kind, "text": safe, "operation_id": opid})
            except BaseException:
                termination = stop_process(identity)
                proc.wait(timeout=5)
                store.write(identity_ref, {"operation_id": opid, "identity": identity,
                            "status": "event_handler_failed", "termination_confirmed": termination["confirmed"], "ended": now()})
                raise
    returncode = proc.wait()
    # A well-behaved leader can exit while leaving grandchildren behind. They
    # retain the group's identity because seccomp forbids setsid/setpgid.
    if _group_alive(identity["pgid"]):
        termination = stop_process(identity)
    else:
        termination = {"confirmed": True, "status": "exited"}
    result = {"operation_id": opid, "returncode": returncode, "stdout": "".join(output), "stderr": "".join(error),
              "status": "termination_uncertain" if not termination["confirmed"] else ("stopped" if stopped else "timeout" if timed_out else "exited"),
              "termination_confirmed": termination["confirmed"], "started": started, "ended": now(),
              "workspace_revision": workspace.revision, "process_identity": identity,
              "confinement": "linux-landlock-seccomp", "usage": None}
    store.write(identity_ref, {"operation_id": opid, "identity": identity, "status": result["status"], "termination_confirmed": termination["confirmed"], "ended": now()})
    if output_ref:
        ref = output_ref.removeprefix("home:.aih_product/")
        store.write(ref, result)
    return result


def _within_ref(ref, prefix):
    root, _, path = ref.partition(":")
    allowed_root, _, allowed_path = prefix.partition(":")
    allowed_path = allowed_path.rstrip("/")
    return root == allowed_root and (not allowed_path or path == allowed_path or path.startswith(allowed_path + "/"))


def test_inputs_unchanged(before, after, contracts):
    """Ignore only explicitly declared non-source output/cache effects."""
    if not before.get("complete") or not after.get("complete"):
        return False
    previous = {item["ref"]: item["sha256"] for item in before["files"]}
    current = {item["ref"]: item["sha256"] for item in after["files"]}
    outputs = [ref for contract in contracts for ref in contract.get("write_paths", [])]
    sources = [ref for contract in contracts for ref in contract.get("source_paths", [])]
    changed = {ref for ref in set(previous) | set(current) if previous.get(ref) != current.get(ref)}
    return all(any(_within_ref(ref, output) for output in outputs) and not any(_within_ref(ref, source) for source in sources) for ref in changed)


def validate_test_contract(contract, workspace, allowed_scope, authorization=None):
    required = {"id", "workspace_revision", "runner", "environment", "working_directory", "source_paths", "write_paths", "prerequisites", "isolation", "cleanup", "authorization", "required"}
    missing = sorted(required - set(contract))
    if missing:
        raise ExecutionError("Test contract missing: " + ", ".join(missing), "invalid_test_contract")
    if contract["workspace_revision"] != workspace.revision:
        raise ExecutionError("Test contract refers to an obsolete workspace revision", "stale_test_contract")
    if contract["runner"] not in ("python-unittest", "python-script") or contract["environment"] != "python3":
        raise ExecutionError("Only registered Python unittest/script environments are supported")
    if contract["isolation"] not in ("landlock", "linux-landlock-seccomp") or contract["cleanup"] not in ("retain", "operation-runtime"):
        raise ExecutionError("Unsupported isolation/cleanup contract")
    if type(contract["required"]) is not bool or not isinstance(contract["authorization"], str) or not contract["authorization"]:
        raise ExecutionError("Required status and explicit test authorization must be recorded")
    if authorization is not None and contract["authorization"] != authorization:
        raise ExecutionError("The required test execution authority is absent")
    for field in ("source_paths", "write_paths", "prerequisites"):
        if not isinstance(contract[field], list):
            raise ExecutionError(f"Test contract {field} must be a list")
    work_rid, work_parts = workspace.parse(contract["working_directory"])
    if work_rid == "home" and work_parts and work_parts[0] == ".aih_product":
        raise ExecutionError("Test working directories must be outside inert product state")
    workspace.resolve(contract["working_directory"], must_exist=True)
    if not contract["source_paths"]:
        raise ExecutionError("A test contract must identify its runnable sources")
    for ref in contract["source_paths"]:
        source_rid, source_parts = workspace.parse(ref)
        if source_rid == "home" and source_parts and source_parts[0] == ".aih_product":
            raise ExecutionError("Test sources must be outside inert product state")
        workspace.resolve(ref, must_exist=True)
    for ref in contract["write_paths"]:
        workspace.resolve(ref, write=True, scope=allowed_scope, must_exist=True)
        if any(_within_ref(ref, source) or _within_ref(source, ref) for source in contract["source_paths"]):
            raise ExecutionError("Test output/cache effects must be disjoint from declared runnable sources; use a separate approved build directory")
    for prerequisite in contract["prerequisites"]:
        if not isinstance(prerequisite, dict) or set(prerequisite) - {"kind", "ref", "name"}:
            raise ExecutionError("Test prerequisites must be typed objects")
        if prerequisite.get("kind") == "file":
            workspace.resolve(prerequisite["ref"], must_exist=True)
        elif prerequisite.get("kind") == "environment":
            if not re.fullmatch(r"[A-Z][A-Z0-9_]*", prerequisite.get("name", "")) or not os.environ.get(prerequisite["name"]):
                raise ExecutionError("A required test environment reference is unavailable")
        else:
            raise ExecutionError("Unsupported test prerequisite; external effects require a trusted extension")
    return contract


def run_registered_test(contract, workspace, allowed_scope=None, *, operation_id=None, stop_event=None,
                        on_event=None, authorization=None):
    validate_test_contract(contract, workspace, allowed_scope or [], authorization)
    before = workspace.inventory()
    if not before["complete"]:
        raise ExecutionError("Incomplete source inventory blocks content-bound test evidence", details={"problems": before["problems"]})
    if contract["runner"] == "python-unittest":
        start = workspace.resolve(contract.get("start_directory", contract["source_paths"][0]), must_exist=True)
        pattern = contract.get("pattern", "test*.py")
        if not isinstance(pattern, str) or "/" in pattern or "\\" in pattern:
            raise ExecutionError("Invalid unittest filename pattern")
        command = [sys.executable, "-B", "-m", "unittest", "discover", "-s", str(start), "-p", pattern, "-v"]
    else:
        script = workspace.resolve(contract.get("script", ""), must_exist=True)
        if script.suffix != ".py" or ".aih_product" in script.parts:
            raise ExecutionError("Registered scripts must be Python source outside product state")
        command = [sys.executable, "-B", str(script)]
    result = run_process(command, workspace, cwd=contract["working_directory"], write_scope=contract["write_paths"],
                         timeout=contract.get("timeout", 300), operation_id=operation_id,
                         on_event=on_event, stop_event=stop_event, network=False,
                         env={p["name"]: os.environ[p["name"]] for p in contract["prerequisites"] if p.get("kind") == "environment"})
    after = workspace.inventory()
    stable = test_inputs_unchanged(before, after, [contract])
    tests_collected = None
    if contract["runner"] == "python-unittest":
        matches = re.findall(r"Ran (\d+) tests? in ", result["stdout"] + result["stderr"])
        tests_collected = int(matches[-1]) if matches else 0
    result.update(suite_id=contract["id"], required=contract["required"], contract=contract,
                  checked_content=after, input_content=before, content_unchanged=stable, tests_collected=tests_collected,
                  outcome="blocked" if tests_collected == 0 else "passed" if result["returncode"] == 0 and result["status"] == "exited" and stable else "failed" if result["returncode"] else "stale")
    return result


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "_exec":
        try:
            cfg = json.loads(sys.argv[2])
            gate_deadline = time.monotonic() + 10
            current_identity = process_identity(os.getpid())
            while True:
                try:
                    recorded = json.loads(Path(cfg["ownership_record"]).read_text("utf-8"))
                    if recorded.get("identity") == current_identity and recorded.get("status") == "running":
                        break
                except (OSError, ValueError, KeyError):
                    pass
                if time.monotonic() >= gate_deadline:
                    raise ExecutionError("No durable ownership acknowledgment; the child did not execute")
                time.sleep(0.01)
            # Resolve libseccomp before filesystem restriction; loading the
            # library after restriction remains allowed from /usr and /lib.
            ctypes.CDLL("libseccomp.so.2")
            _restrict(cfg["paths"], cfg["network"])
            os.execvpe(cfg["command"][0], cfg["command"], os.environ)
        except Exception as exc:
            print(json.dumps({"error": "confinement_start_failed", "message": str(exc)}), file=sys.stderr)
            raise SystemExit(125)
    raise SystemExit("This is an internal confined-process entry point. Use the typed AIH CLI operations.")
