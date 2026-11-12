"""Bounded workspace storage with optimistic checks and cooperative locks."""
from __future__ import annotations
import contextlib
import hashlib
import json
import os
from pathlib import Path
import stat
import uuid
from path_contract import relative_parts, is_link_or_reparse

class SafetyError(Exception):
    def __init__(self, message, changed_files=None):
        super().__init__(message)
        self.changed_files = changed_files or []

def _pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise SafetyError(f'duplicate JSON key: {k}')
        out[k] = v
    return out

def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=_pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(SafetyError(f'invalid JSON constant: {value}')))
    except (OSError, UnicodeError, ValueError) as exc:
        raise SafetyError(str(exc)) from exc

def checked_path(root, relative, *, allow_missing=True):
    root = Path(root).resolve(strict=True)
    try:
        parts = relative_parts(relative)
    except ValueError as exc:
        raise SafetyError(str(exc)) from exc
    path = root
    for part in parts:
        path = path / part
        try:
            info = path.lstat()
        except FileNotFoundError:
            if not allow_missing:
                raise SafetyError(f'Missing path: {relative}')
            continue
        if is_link_or_reparse(info):
            raise SafetyError(f'Symlink or reparse point prohibited: {relative}')
        if path != root / relative and not stat.S_ISDIR(info.st_mode):
            raise SafetyError(f'Non-directory parent: {relative}')
        if stat.S_ISREG(info.st_mode) and info.st_nlink != 1:
            raise SafetyError(f'Hard-linked file prohibited: {relative}')
    return path

def fingerprint(path):
    path = Path(path)
    try:
        s = path.lstat()
    except FileNotFoundError:
        return None
    if is_link_or_reparse(s) or not stat.S_ISREG(s.st_mode) or s.st_nlink != 1:
        raise SafetyError(f'Expected an unaliased regular file: {path}')
    return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, hashlib.sha256(path.read_bytes()).hexdigest())

def json_bytes(value):
    return (json.dumps(value, ensure_ascii=True, indent=2) + '\n').encode('utf-8')

def write_bytes(root, relative, content, expected=None):
    path = checked_path(root, relative)
    if fingerprint(path) != expected:
        raise SafetyError(f'Inspected input changed: {relative}')
    if not path.parent.is_dir():
        raise SafetyError(f'Parent directory is missing: {relative}')
    candidate = None
    created = False
    try:
        if expected is None:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
            created = True
            with os.fdopen(fd, 'wb') as stream:
                stream.write(content); stream.flush(); os.fsync(stream.fileno())
        else:
            candidate = path.parent / ('.hai-candidate-' + uuid.uuid4().hex)
            fd = os.open(candidate, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            created = True
            with os.fdopen(fd, 'wb') as stream:
                stream.write(content); stream.flush(); os.fsync(stream.fileno())
            if fingerprint(checked_path(root, relative)) != expected:
                raise SafetyError('Inspected input changed before replacement')
            os.replace(candidate, path)
        return relative
    except Exception as exc:
        changed = [(candidate or path).relative_to(root).as_posix()] if created else []
        raise SafetyError(str(exc), changed) from exc

def write_json(root, relative, value, expected=None):
    return write_bytes(root, relative, json_bytes(value), expected)

@contextlib.contextmanager
def lock(root):
    # Never remove a lock that was present on entry: it may be stale or invalid.
    directory = checked_path(root, '.hai_env')
    if not directory.is_dir():
        raise SafetyError('Environment directory required for mutation lock')
    path = checked_path(root, '.hai_env/.runtime.lock')
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    except FileExistsError as exc:
        raise SafetyError('Runtime lock exists; inspect stale or invalid lock before proceeding') from exc
    token = uuid.uuid4().hex
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        f.write(token)
    identity = fingerprint(path)
    try:
        yield
    finally:
        if fingerprint(path) == identity:
            path.unlink()
