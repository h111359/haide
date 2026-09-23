"""Root-qualified, permission-aware filesystem operations.

Only the explicitly registered union is addressable. POSIX operations traverse with
O_NOFOLLOW directory handles; Windows mutations fail closed until a native
reparse-safe implementation is installed. External administrators remain outside
AIH's control; identity checks detect replaced roots and parents.
"""
from __future__ import annotations
import contextlib
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import stat
import uuid

INERT_FORBIDDEN_SUFFIXES = frozenset({".py", ".pyw", ".pyc", ".pyo", ".pyd", ".sh", ".bash", ".zsh", ".fish", ".cmd", ".bat", ".ps1", ".psm1", ".exe", ".com", ".dll", ".so", ".dylib", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".wasm", ".jar", ".class", ".whl", ".egg", ".php", ".rb", ".pl", ".lua", ".c", ".cpp", ".h", ".hpp", ".go", ".rs", ".db", ".sqlite", ".sqlite3"})
INERT_FORBIDDEN_DIRS = frozenset({"__pycache__", ".venv", "venv", "node_modules", "site-packages", "__pypackages__", ".pytest_cache", ".git"})
EXECUTABLE_MAGIC = (b"\x7fELF", b"MZ", b"SQLite format 3\x00", b"\x00asm", b"\xca\xfe\xba\xbe")


def forbidden_state_directory(name):
    return name in INERT_FORBIDDEN_DIRS or name.endswith((".dist-info", ".egg-info"))


class BoundaryError(ValueError):
    def __init__(self, message, code="workspace_boundary", details=None):
        super().__init__(message)
        self.code, self.details = code, details or {}


def digest(data):
    return hashlib.sha256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()


def _identity(st):
    return st.st_dev, st.st_ino


def _is_link(st):
    return stat.S_ISLNK(st.st_mode) or bool(getattr(st, "st_file_attributes", 0) & 0x400)


def canonical_directory(path, *, missing=False):
    """Validate only this explicitly selected path, never enumerate neighbors."""
    path = Path(os.path.abspath(os.fspath(path)))
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current /= part
        try:
            st = current.lstat()
        except FileNotFoundError:
            if missing:
                return path
            raise BoundaryError(f"Workspace folder is missing: {path}", "root_missing")
        if _is_link(st):
            raise BoundaryError(f"Symlink/reparse path is not permitted: {current}", "path_alias")
        if not stat.S_ISDIR(st.st_mode):
            raise BoundaryError(f"Workspace parent is not a directory: {current}")
    if path.resolve() != path:
        raise BoundaryError("Workspace path has an unresolved alias")
    return path


def validate_registry(home, registry, *, allow_missing=False):
    home = canonical_directory(home)
    if isinstance(registry, list):
        registry = {"revision": 1, "roots": registry}
    if not isinstance(registry, dict) or not isinstance(registry.get("roots"), list):
        raise BoundaryError("Workspace requires a roots list")
    revision = registry.get("revision", 1)
    if type(revision) is not int or revision < 1:
        raise BoundaryError("Workspace revision must be a positive integer")
    roots, ids, identities = [], set(), set()
    for item in registry["roots"]:
        if not isinstance(item, dict):
            raise BoundaryError("Each workspace root must be an object")
        root = dict(item)
        rid = root.get("id", "")
        if not re.fullmatch(r"[a-z][a-z0-9_-]{0,47}", rid) or rid in ids:
            raise BoundaryError("Root IDs must be unique stable lowercase names")
        if root.get("access") not in ("read-write", "read-only"):
            raise BoundaryError(f"Invalid access mode for {rid}")
        if not isinstance(root.get("path"), str) or not Path(root["path"]).is_absolute():
            raise BoundaryError(f"Root {rid} requires an absolute canonical path")
        path = canonical_directory(root["path"], missing=allow_missing)
        for other in roots:
            old = Path(other["path"])
            if path == old or path in old.parents or old in path.parents:
                raise BoundaryError(f"Overlapping workspace roots: {rid} and {other['id']}", "root_overlap")
        try:
            st = path.stat()
            ident = _identity(st)
            if ident in identities:
                raise BoundaryError("Workspace roots alias the same directory", "root_alias")
            identities.add(ident)
            available = os.access(path, os.R_OK | os.X_OK)
        except OSError:
            available = False
        root.update(path=str(path), name=root.get("name") or rid,
                    purpose=root.get("purpose") or "Product component", available=available)
        roots.append(root)
        ids.add(rid)
    fixed = next((r for r in roots if r["id"] == "home"), None)
    if not fixed or Path(fixed["path"]) != home or fixed["access"] != "read-write":
        raise BoundaryError("The canonical framework home must remain the writable 'home' root", "home_required")
    return {**registry, "revision": revision, "roots": roots}


class Workspace:
    def __init__(self, home, registry=None):
        self.home = canonical_directory(home)
        if registry is None:
            registry = {"revision": 1, "roots": [{"id": "home", "name": "Home", "path": str(self.home),
                          "purpose": "Framework home and product", "access": "read-write"}]}
        self.registry = validate_registry(self.home, registry, allow_missing=True)
        self.revision = self.registry["revision"]
        self.roots = {r["id"]: r for r in self.registry["roots"]}
        self._identities = {}
        for rid, root in self.roots.items():
            try:
                self._identities[rid] = _identity(Path(root["path"]).stat())
            except OSError:
                pass

    def parse(self, ref):
        if isinstance(ref, dict):
            if ref.get("workspace_revision", self.revision) != self.revision:
                raise BoundaryError("Historical file reference requires its recorded root mapping", "stale_workspace")
            ref = f"{ref.get('root', ref.get('root_id', ''))}:{ref.get('path', '')}"
        if not isinstance(ref, str) or ":" not in ref:
            raise BoundaryError("Use a root-qualified path such as home:src/main.py")
        rid, rel = ref.split(":", 1)
        if rid not in self.roots:
            raise BoundaryError(f"Root {rid!r} is not registered", "unknown_root")
        if "\\" in rel or "\x00" in rel or ":" in rel or rel.startswith("/"):
            raise BoundaryError("Absolute, alternate-stream, and ambiguous paths are prohibited")
        parts = rel.split("/") if rel else []
        if any(p in ("..", "") for p in parts) or any(p.endswith((" ", ".")) and p != "." for p in parts):
            raise BoundaryError("Traversal or ambiguous path component")
        parts = [p for p in parts if p != "."]
        if any(re.fullmatch(r"(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])(\..*)?", p) for p in parts):
            raise BoundaryError("Reserved device path")
        return rid, parts

    def reference(self, path):
        path = Path(os.path.abspath(path))
        for rid, root in self.roots.items():
            try:
                rel = path.relative_to(root["path"])
                return f"{rid}:{rel.as_posix()}"
            except ValueError:
                continue
        raise BoundaryError("Path is outside the registered workspace")

    def _root(self, rid):
        root = Path(self.roots[rid]["path"])
        try:
            st = root.lstat()
        except OSError as exc:
            raise BoundaryError(f"Registered root {rid} is unavailable: {exc}", "root_missing") from exc
        if _is_link(st) or not stat.S_ISDIR(st.st_mode) or _identity(st) != self._identities.get(rid):
            raise BoundaryError(f"Registered root {rid} changed identity; explicit reconciliation is required", "root_changed")
        canonical_directory(root)
        return root

    def _authorize(self, rid, parts, *, write=False, scope=None, internal=False):
        if write:
            if self.roots[rid]["access"] != "read-write":
                raise BoundaryError(f"Root {rid} is read-only", "read_only")
            if not parts:
                raise BoundaryError("Changing the registered root itself is prohibited")
            if rid == "home" and parts[0] == ".aih":
                raise BoundaryError("Installed framework core is immutable", "immutable_core")
            if rid == "home" and parts[0] == ".aih_product" and not internal:
                raise BoundaryError("Product state changes require the typed engine operation", "state_protected")
            if internal and not (rid == "home" and parts[0] == ".aih_product"):
                raise BoundaryError("Internal state authority does not permit product writes")
            if scope is None and not internal:
                raise BoundaryError("Product writes require an explicit action scope", "scope_required")
            if scope is not None:
                allowed = False
                for entry in scope:
                    srid, sparts = self.parse(entry.removesuffix("/**"))
                    if srid == rid and parts[:len(sparts)] == sparts:
                        allowed = True
                        break
                if not allowed:
                    raise BoundaryError("The file is outside the current action's permitted scope", "out_of_scope")

    def resolve(self, ref, write=False, scope=None, internal=False, must_exist=False):
        rid, parts = self.parse(ref)
        self._authorize(rid, parts, write=write, scope=scope, internal=internal)
        root = self._root(rid)
        path = root
        for idx, part in enumerate(parts):
            path /= part
            try:
                st = path.lstat()
            except FileNotFoundError:
                if must_exist:
                    raise BoundaryError(f"Path is missing: {ref}", "path_missing")
                continue
            if _is_link(st):
                raise BoundaryError(f"Symlinks/reparse points are not followed: {ref}", "path_alias")
            if stat.S_ISREG(st.st_mode) and st.st_nlink != 1:
                raise BoundaryError(f"Hard-linked files are not accepted: {ref}", "hardlink")
            if not stat.S_ISREG(st.st_mode) and not stat.S_ISDIR(st.st_mode):
                raise BoundaryError(f"Special files are not accepted: {ref}", "special_file")
            if idx < len(parts) - 1 and not stat.S_ISDIR(st.st_mode):
                raise BoundaryError("Non-directory path parent")
        return path

    @contextlib.contextmanager
    def _parent(self, ref, *, write=False, scope=None, internal=False, create=False):
        rid, parts = self.parse(ref)
        self._authorize(rid, parts, write=write, scope=scope, internal=internal)
        if not parts:
            raise BoundaryError("A file/directory path is required")
        if os.name != "posix" or not hasattr(os, "O_NOFOLLOW"):
            raise BoundaryError("Safe managed mutation/read handles are unavailable on this platform; use Linux/WSL", "platform_unsupported")
        root = self._root(rid)
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        fd = os.open(root, flags)
        walked = root
        try:
            if _identity(os.fstat(fd)) != self._identities[rid]:
                raise BoundaryError("Root changed between validation and use", "path_race")
            for part in parts[:-1]:
                walked /= part
                try:
                    child = os.open(part, flags, dir_fd=fd)
                except FileNotFoundError:
                    if not create:
                        raise
                    os.mkdir(part, mode=0o700, dir_fd=fd)
                    os.fsync(fd)
                    child = os.open(part, flags, dir_fd=fd)
                os.close(fd)
                fd = child
            # Detect a renamed parent or replaced ancestor immediately before use.
            current = self.resolve(ref, write=write, scope=scope, internal=internal).parent
            if _identity(current.stat()) != _identity(os.fstat(fd)):
                raise BoundaryError("Parent changed between validation and use", "path_race")
            yield fd, parts[-1]
        except OSError as exc:
            if exc.errno in (20, 40):
                raise BoundaryError("Path changed or contains a link", "path_race") from exc
            raise
        finally:
            os.close(fd)

    @staticmethod
    def _check_leaf(fd, name, *, absent_ok=True):
        try:
            st = os.stat(name, dir_fd=fd, follow_symlinks=False)
        except FileNotFoundError:
            if absent_ok:
                return None
            raise
        if _is_link(st) or (stat.S_ISREG(st.st_mode) and st.st_nlink != 1):
            raise BoundaryError("Linked file rejected at point of use", "path_alias")
        if not (stat.S_ISREG(st.st_mode) or stat.S_ISDIR(st.st_mode)):
            raise BoundaryError("Special filesystem object rejected")
        return st

    def read_bytes(self, ref, max_bytes=32 * 1024 * 1024):
        with self._parent(ref) as (parent, name):
            st = self._check_leaf(parent, name, absent_ok=False)
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent)
            try:
                actual = os.fstat(fd)
                if _identity(st) != _identity(actual) or actual.st_nlink != 1 or not stat.S_ISREG(actual.st_mode):
                    raise BoundaryError("Read target changed", "path_race")
                if actual.st_size > max_bytes:
                    raise BoundaryError(f"File exceeds the {max_bytes} byte read limit", "file_too_large")
                with os.fdopen(fd, "rb", closefd=False) as stream:
                    data = stream.read(max_bytes + 1)
                if len(data) > max_bytes:
                    raise BoundaryError("File grew beyond the read limit")
                final = os.fstat(fd)
                if (actual.st_size, actual.st_mtime_ns, actual.st_ctime_ns) != (final.st_size, final.st_mtime_ns, final.st_ctime_ns):
                    raise BoundaryError("File content changed while reading", "path_race")
                return data
            finally:
                os.close(fd)

    def file_info(self, ref):
        """Hash a complete regular file without imposing the text-read size cap."""
        with self._parent(ref) as (parent, name):
            checked = self._check_leaf(parent, name, absent_ok=False)
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent)
            try:
                before = os.fstat(fd)
                if _identity(before) != _identity(checked) or before.st_nlink != 1 or not stat.S_ISREG(before.st_mode):
                    raise BoundaryError("Inventory target changed", "path_race")
                hasher = hashlib.sha256()
                count = 0
                while True:
                    block = os.read(fd, 1024 * 1024)
                    if not block:
                        break
                    count += len(block)
                    hasher.update(block)
                after = os.fstat(fd)
                if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                    raise BoundaryError("Inventory content changed while hashing", "path_race")
                return {"sha256": hasher.hexdigest(), "bytes": count}
            finally:
                os.close(fd)

    def read_text(self, ref, max_bytes=32 * 1024 * 1024):
        return self.read_bytes(ref, max_bytes).decode("utf-8")

    def atomic_write(self, ref, data, *, scope=None, internal=False, expected_hash="unchecked"):
        data = data.encode("utf-8") if isinstance(data, str) else bytes(data)
        rid, parts = self.parse(ref)
        if rid == "home" and parts and parts[0] == ".aih_product":
            if Path(parts[-1]).suffix.lower() in INERT_FORBIDDEN_SUFFIXES or data.startswith(EXECUTABLE_MAGIC) or any(forbidden_state_directory(part) for part in parts[1:-1]):
                raise BoundaryError("Product state accepts inert information only", "executable_state")
        with self._parent(ref, write=True, scope=scope, internal=internal, create=True) as (parent, name):
            old = self._check_leaf(parent, name)
            if old and not stat.S_ISREG(old.st_mode):
                raise BoundaryError("File replacement target is not a regular file")
            if expected_hash != "unchecked":
                actual = digest(self.read_bytes(ref)) if old else None
                if actual != expected_hash:
                    raise BoundaryError("File changed since it was reviewed", "revision_conflict", {"ref": ref, "expected": expected_hash, "actual": actual})
            tmp = f".aih-write-{uuid.uuid4().hex}"
            fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
            try:
                with os.fdopen(fd, "wb", closefd=False) as stream:
                    stream.write(data)
                    stream.flush()
                    os.fsync(fd)
                latest = self._check_leaf(parent, name)
                if (old is None) != (latest is None) or (old and (_identity(old), old.st_size, old.st_mtime_ns, old.st_ctime_ns) != (_identity(latest), latest.st_size, latest.st_mtime_ns, latest.st_ctime_ns)):
                    raise BoundaryError("File identity changed before replacement", "path_race")
                os.replace(tmp, name, src_dir_fd=parent, dst_dir_fd=parent)
                os.fsync(parent)
            finally:
                os.close(fd)
                try:
                    os.unlink(tmp, dir_fd=parent)
                except FileNotFoundError:
                    pass
        return {"ref": ref, "sha256": digest(data), "workspace_revision": self.revision, "bytes": len(data)}

    write = atomic_write

    def mkdir(self, ref, *, scope=None, internal=False):
        rid, parts = self.parse(ref)
        if rid == "home" and parts and parts[0] == ".aih_product" and any(forbidden_state_directory(part) for part in parts[1:]):
            raise BoundaryError("Product state cannot contain installed packages, executable environments or bytecode caches", "executable_state")
        with self._parent(ref, write=True, scope=scope, internal=internal, create=True) as (parent, name):
            st = self._check_leaf(parent, name)
            if st:
                if not stat.S_ISDIR(st.st_mode):
                    raise BoundaryError("Directory target exists as a file")
            else:
                os.mkdir(name, 0o700, dir_fd=parent)
                os.fsync(parent)
        return self.resolve(ref)

    def unlink(self, ref, *, scope=None, internal=False, expected_hash="unchecked"):
        with self._parent(ref, write=True, scope=scope, internal=internal) as (parent, name):
            st = self._check_leaf(parent, name, absent_ok=False)
            if expected_hash != "unchecked" and digest(self.read_bytes(ref)) != expected_hash:
                raise BoundaryError("Delete target changed", "revision_conflict")
            if stat.S_ISDIR(st.st_mode):
                os.rmdir(name, dir_fd=parent)  # only empty, checked directories
            else:
                os.unlink(name, dir_fd=parent)
            os.fsync(parent)

    def move(self, source, destination, *, scope=None, internal=False):
        with self._parent(source, write=True, scope=scope, internal=internal) as (srcfd, src):
            old = self._check_leaf(srcfd, src, absent_ok=False)
            with self._parent(destination, write=True, scope=scope, internal=internal, create=True) as (dstfd, dst):
                if self._check_leaf(dstfd, dst):
                    raise BoundaryError("Move destination already exists")
                if _identity(old) != _identity(self._check_leaf(srcfd, src, absent_ok=False)):
                    raise BoundaryError("Move source changed", "path_race")
                if os.fstat(srcfd).st_dev != os.fstat(dstfd).st_dev:
                    raise BoundaryError("Cross-filesystem moves require journalled copy/reconciliation", "cross_filesystem")
                os.rename(src, dst, src_dir_fd=srcfd, dst_dir_fd=dstfd)
                os.fsync(srcfd)
                os.fsync(dstfd)

    def inventory(self, root_ids=None, *, include_core=False):
        entries, problems = [], []
        excluded = {".git", "__pycache__", ".aih_runtime", ".venv", "node_modules"}
        for rid in root_ids or self.roots:
            try:
                root = self._root(rid)
                for directory, dirs, files in os.walk(root, followlinks=False):
                    relbase = Path(directory).relative_to(root)
                    dirs[:] = sorted(d for d in dirs if d not in excluded and not (rid == "home" and relbase == Path(".") and d in ({".aih_product"} if include_core else {".aih", ".aih_product"})))
                    for name in list(dirs):
                        ref = f"{rid}:{(relbase / name).as_posix()}"
                        try:
                            self.resolve(ref, must_exist=True)
                        except (BoundaryError, OSError) as exc:
                            dirs.remove(name)
                            problems.append({"ref": ref, "error": str(exc)})
                    for name in sorted(files):
                        ref = f"{rid}:{(relbase / name).as_posix()}"
                        try:
                            info = self.file_info(ref)
                            entries.append({"ref": ref, "root_id": rid, "path": (relbase / name).as_posix(),
                                            **info, "workspace_revision": self.revision})
                        except (BoundaryError, OSError) as exc:
                            problems.append({"ref": ref, "error": str(exc)})
            except (BoundaryError, OSError) as exc:
                problems.append({"root_id": rid, "error": str(exc)})
        return {"workspace_revision": self.revision, "roots": self.registry["roots"], "files": entries, "problems": problems,
                "complete": not problems, "fingerprint": digest("\n".join(f"{e['ref']}\0{e['sha256']}" for e in entries))}

    def fingerprint(self, root_ids=None):
        return self.inventory(root_ids)["fingerprint"]
