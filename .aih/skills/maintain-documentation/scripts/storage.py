"""File-authoritative state, optimistic revisions, OS locks and recoverable journals.

Files ending .yaml are deliberately written in the JSON subset of YAML 1.2.
The implementation assumes a local filesystem with working advisory locks,
atomic same-directory rename and fsync. Network/synchronized storage is untested.
"""
from __future__ import annotations
import base64
import contextlib
import datetime as dt
import json
import os
from pathlib import Path
import re
import threading
import time
import uuid
from security import Workspace, BoundaryError, digest, canonical_directory


class StorageError(ValueError):
    def __init__(self, message, code="storage_error", details=None):
        super().__init__(message)
        self.code, self.details = code, details or {}


class ConflictError(StorageError):
    def __init__(self, message="Files changed since the reviewed revision", details=None):
        super().__init__(message, "revision_conflict", details)


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _no_duplicates(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise StorageError(f"Duplicate key: {k}", "invalid_document")
        result[k] = v
    return result


def loads(text):
    try:
        return json.loads(text, object_pairs_hook=_no_duplicates,
                          parse_constant=lambda value: (_ for _ in ()).throw(StorageError("Non-finite JSON numbers are prohibited")))
    except json.JSONDecodeError as exc:
        raise StorageError(f"Invalid JSON-compatible YAML at line {exc.lineno}; use the installed JSON/YAML templates", "invalid_document") from exc


def dumps(value):
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n"


_SECRET_PATTERNS = [
    re.compile(r"\b(?:sk-(?:proj-)?|gh[pousr]_|github_pat_|xox[baprs]-)[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(r"(?i)[a-z][a-z0-9+.-]*://[^\s/@:]+:[^\s/@]+@"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\b(?:api[_-]?key|password|client[_-]?secret|access[_-]?token|refresh[_-]?token|authorization)\s*[:=]\s*[\"']?(?:bearer\s+)?(?!\$\{|env:|<|REDACTED|\[redacted\])[^\s\"',}]{8,}"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
]


def sensitive_categories(value):
    text = value if isinstance(value, str) else dumps(value)
    return [f"credential_pattern_{i + 1}" for i, pattern in enumerate(_SECRET_PATTERNS) if pattern.search(text)]


def screen_sensitive(value):
    categories = sensitive_categories(value)
    if categories:
        raise StorageError("Sensitive input rejected before persistence. Remove the credential and resubmit; use environment-variable references.", "sensitive_input", {"categories": categories})
    return value


def sanitize(value):
    if isinstance(value, dict):
        if value.get("type", "") in ("reasoning", "reasoning.summary", "reasoning.delta"):
            return {"type": "private_reasoning_omitted"}
        return {k: sanitize(v) for k, v in value.items() if k not in ("reasoning", "private_reasoning", "chain_of_thought", "auth", "credentials")}
    if isinstance(value, list):
        return [sanitize(v) for v in value]
    if isinstance(value, str):
        for pattern in _SECRET_PATTERNS:
            value = pattern.sub("[redacted sensitive value]", value)
    return value


_LOCKS = {}
_LOCKS_GUARD = threading.Lock()
_LOCAL = threading.local()


@contextlib.contextmanager
def home_lock(home, *, shared=False):
    """Read-only directory lock; reserves an uninitialized home without files."""
    home = canonical_directory(home)
    if os.name != "posix":
        raise StorageError("Maintenance directory locking requires Linux/WSL", "platform_unsupported")
    import fcntl
    fd = os.open(home, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        try:
            fcntl.flock(fd, (fcntl.LOCK_SH if shared else fcntl.LOCK_EX) | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise StorageError("Another explicit maintenance or initialization action holds this framework home; no work was queued", "maintenance-busy") from exc
        yield
    finally:
        os.close(fd)


class Store:
    def __init__(self, home):
        self.home = Path(home).resolve()
        self.workspace = Workspace(home)
        self.root = self.home / ".aih_product"

    def _ref(self, path):
        path = str(path)
        if ":" in path:
            rid, parts = self.workspace.parse(path)
            if rid != "home" or not parts or parts[0] != ".aih_product":
                raise StorageError("Store paths must address central product state")
            return path
        if path.startswith(".aih_product/"):
            path = path[len(".aih_product/"):]
        return "home:.aih_product/" + path

    def path(self, path):
        return self.workspace.resolve(self._ref(path))

    def read_text(self, path, default=None):
        try:
            return self.workspace.read_text(self._ref(path))
        except FileNotFoundError:
            return default

    def read(self, path, default=None, raw=False):
        value = self.read_text(path)
        return default if value is None else (value if raw else loads(value))

    def hash(self, path):
        value = self.read_text(path)
        return None if value is None else digest(value)

    def write(self, path, value, *, expected_hash="unchecked"):
        text = value if isinstance(value, (str, bytes)) else dumps(value)
        return self.workspace.atomic_write(self._ref(path), text, internal=True, expected_hash=expected_hash)

    @contextlib.contextmanager
    def lock(self, timeout=10):
        lock_ref = "home:.aih_product/ledger/.lock"
        key = str(self.home)
        with _LOCKS_GUARD:
            mutex = _LOCKS.setdefault(key, threading.RLock())
        if not mutex.acquire(timeout=timeout):
            raise StorageError("Another transaction holds the state lock", "locked")
        held = getattr(_LOCAL, "held", None)
        if held is None:
            held = _LOCAL.held = {}
        if key in held:
            if len(held[key]) > 2 and held[key][2] == "read":
                mutex.release()
                raise StorageError("A shared read lock cannot be upgraded to a mutating transaction", "lock_upgrade")
            held[key][1] += 1
            try:
                yield self
            finally:
                held[key][1] -= 1
                mutex.release()
            return
        fd = None
        try:
            self.workspace.mkdir("home:.aih_product/ledger", internal=True)
            with self.workspace._parent(lock_ref, write=True, internal=True) as (parent, name):
                self.workspace._check_leaf(parent, name)
                fd = os.open(name, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600, dir_fd=parent)
            if os.fstat(fd).st_nlink != 1:
                raise StorageError("The state lock is aliased", "unsafe_lock")
            if os.name != "posix":
                raise StorageError("Native Windows locking/mutation support is unavailable; use Linux/WSL", "platform_unsupported")
            import fcntl
            deadline = time.monotonic() + timeout
            while True:
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() > deadline:
                        raise StorageError("Another process holds the state lock; deleting the file does not stop its owner", "locked")
                    time.sleep(0.03)
            held[key] = [fd, 1, "write"]
            yield self
        finally:
            held.pop(key, None)
            if fd is not None:
                os.close(fd)
            mutex.release()

    @contextlib.contextmanager
    def read_lock(self, timeout=10):
        """Lock an initialized store for a confined, strictly read-only helper.

        The existing lock is opened read-only and never created. A caller already
        holding the exclusive lock can perform nested deterministic reads.
        """
        key = str(self.home)
        with _LOCKS_GUARD:
            mutex = _LOCKS.setdefault(key, threading.RLock())
        if not mutex.acquire(timeout=timeout):
            raise StorageError("Another transaction holds the state lock", "locked")
        held = getattr(_LOCAL, "held", None)
        if held is None:
            held = _LOCAL.held = {}
        if key in held:
            held[key][1] += 1
            try:
                yield self
            finally:
                held[key][1] -= 1
                mutex.release()
            return
        fd = None
        try:
            if os.name != "posix":
                raise StorageError("Native Windows locking support is unavailable; use Linux/WSL", "platform_unsupported")
            with self.workspace._parent("home:.aih_product/ledger/.lock") as (parent, name):
                before = self.workspace._check_leaf(parent, name, absent_ok=False)
                fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent)
                after = os.fstat(fd)
                if after.st_nlink != 1 or (after.st_dev, after.st_ino) != (before.st_dev, before.st_ino):
                    raise StorageError("The state lock changed identity or is aliased", "unsafe_lock")
            import fcntl
            deadline = time.monotonic() + timeout
            while True:
                try:
                    fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() > deadline:
                        raise StorageError("A mutating transaction holds the state lock", "locked")
                    time.sleep(0.03)
            held[key] = [fd, 1, "read"]
            yield self
        finally:
            held.pop(key, None)
            if fd is not None:
                os.close(fd)
            mutex.release()

    def transaction(self, writes, expected=None, *, operation_id=None):
        """Journal a set of information writes. Recovery only completes unchanged steps."""
        if not isinstance(writes, dict) or not writes:
            raise StorageError("A transaction needs a non-empty path/value mapping")
        with self.lock():
            txid = "tx-" + uuid.uuid4().hex
            steps = []
            for path, value in writes.items():
                self.workspace.resolve(self._ref(path), write=True, internal=True)
                raw = value if isinstance(value, bytes) else (value if isinstance(value, str) else dumps(value)).encode("utf-8")
                before = self.hash(path)
                if expected and path in expected and before != expected[path]:
                    raise ConflictError(details={"path": path, "expected": expected[path], "actual": before})
                steps.append({"path": str(path), "before": before, "after": digest(raw), "data_base64": base64.b64encode(raw).decode("ascii"), "done": False})
            journal = {"schema_version": "1.0", "id": txid, "operation_id": operation_id, "created": now(), "status": "prepared",
                       "storage_assumption": "local-filesystem-fsync-advisory-locks", "steps": steps}
            jp = f"ledger/transactions/{txid}.json"
            self.write(jp, journal)
            try:
                for step in steps:
                    self.write(step["path"], base64.b64decode(step["data_base64"]), expected_hash=step["before"])
                    step["done"] = True
                    journal["status"] = "applying"
                    self.write(jp, journal)
                journal["status"] = "committed"
                journal["completed"] = now()
                # Completed journals retain versions, not another copy of all content.
                for step in steps:
                    step.pop("data_base64", None)
                self.write(jp, journal)
            except Exception:
                journal["status"] = "interrupted"
                self.write(jp, journal)
                raise
            return {"id": txid, "status": "committed", "changed": list(writes), "journal": jp}

    def recover(self, *, apply=False):
        results = []
        directory = self.path("ledger/transactions")
        if not directory.exists():
            return results
        with self.lock():
            for path in sorted(directory.glob("*.json")):
                jp = "ledger/transactions/" + path.name
                journal = self.read(jp)
                if journal.get("status") == "committed":
                    continue
                conflicts, outstanding = [], []
                for step in journal["steps"]:
                    actual = self.hash(step["path"])
                    if actual == step["after"]:
                        step["done"] = True
                    elif actual == step["before"] and not step["done"]:
                        outstanding.append(step)
                    else:
                        conflicts.append({"path": step["path"], "expected_before": step["before"], "expected_after": step["after"], "actual": actual})
                status = "conflict" if conflicts else "recoverable"
                if apply and not conflicts:
                    for step in outstanding:
                        self.write(step["path"], base64.b64decode(step["data_base64"]), expected_hash=step["before"])
                        step["done"] = True
                        self.write(jp, journal)
                    journal.update(status="committed", recovered=now())
                    for step in journal["steps"]:
                        step.pop("data_base64", None)
                    self.write(jp, journal)
                    status = "committed"
                results.append({"id": journal["id"], "status": status, "conflicts": conflicts, "outstanding": [s["path"] for s in outstanding]})
        return results

    def append_event(self, event):
        with self.lock():
            entry = {"schema_version": "1.0", "id": "event-" + uuid.uuid4().hex, "at": now(), "created": now(), "type": "framework-event", "owner": event.get("operation_id", "framework"), **sanitize(event)}
            path = f"ledger/events/{entry['id']}.json"
            self.write(path, entry, expected_hash=None)
            # The immutable event file remains authoritative; this append-only
            # chronological stream is a convenient portal observation index.
            stream_ref = self._ref("ledger/events.jsonl")
            with self.workspace._parent(stream_ref, write=True, internal=True, create=True) as (parent, name):
                checked = self.workspace._check_leaf(parent, name)
                fd = os.open(name, os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW, 0o600, dir_fd=parent)
                try:
                    actual = os.fstat(fd)
                    if actual.st_nlink != 1 or checked and (actual.st_dev, actual.st_ino) != (checked.st_dev, checked.st_ino):
                        raise StorageError("Event stream changed identity", "path_race")
                    data = (json.dumps(entry, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
                    offset = 0
                    while offset < len(data):
                        offset += os.write(fd, data[offset:])
                    os.fsync(fd)
                    os.fsync(parent)
                finally:
                    os.close(fd)
            return {**entry, "ref": path}

    def temp_create(self, operation_id):
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,100}", operation_id):
            raise StorageError("Invalid operation identity")
        ident = operation_id + "-" + uuid.uuid4().hex
        path = "tmp/" + ident
        self.write(path + "/owner.json", {"schema_version": "1.0", "operation_id": operation_id, "path": path, "created": now(), "inert": True, "status": "active"})
        return path

    def temp_cleanup(self, path=None, *, operation_id=None, reconciled=False, active_operations=None):
        if path is None:
            results = []
            base = self.path("tmp")
            if not base.exists():
                return results
            for directory in sorted(base.iterdir()):
                candidate = "tmp/" + directory.name
                try:
                    self.workspace.resolve(self._ref(candidate), must_exist=True)
                    owner = self.read(candidate + "/owner.json", {})
                    ident = owner.get("operation_id")
                    record = self.read(f"ledger/operations/{ident}/operation.yaml", {}) if ident else {}
                    if ident in (active_operations or []) or record.get("status") not in ("completed", "failed", "stopped", "blocked"):
                        results.append({"path": candidate, "status": "retained", "reason": "Active or uncertain operation ownership"})
                        continue
                    process = self.read(f"ledger/operations/{ident}/process.json", {})
                    if process and not process.get("termination_confirmed"):
                        results.append({"path": candidate, "status": "retained", "reason": "Process termination has not been confirmed"})
                        continue
                    self.temp_cleanup(candidate, operation_id=ident, reconciled=True)
                    results.append({"path": candidate, "status": "removed"})
                except (BoundaryError, StorageError, OSError) as exc:
                    results.append({"path": candidate, "status": "retained", "reason": str(exc)})
            return results
        if not reconciled:
            raise StorageError("Temporary cleanup requires reconciled ownership")
        if not re.fullmatch(r"tmp/[A-Za-z0-9_-]+", path):
            raise StorageError("Invalid operation-owned temporary directory")
        with self.lock():
            owner = self.read(path + "/owner.json")
            state = self.read("state.yaml", {})
            active = state.get("owner") or {}
            if owner.get("operation_id") != operation_id or active.get("id", active.get("operation_id")) == operation_id:
                raise StorageError("Active or mismatched temporary ownership")
            self.append_event({"type": "temporary_cleanup_started", "path": path, "operation_id": operation_id})
            base = self.path(path)
            for directory, dirs, files in os.walk(base, topdown=False, followlinks=False):
                for name in files + dirs:
                    ref = self.workspace.reference(Path(directory) / name)
                    self.workspace.resolve(ref, write=True, internal=True)
                    self.workspace.unlink(ref, internal=True)
            self.workspace.unlink(self._ref(path), internal=True)
            self.append_event({"type": "temporary_cleanup_completed", "path": path, "operation_id": operation_id})
