"""Portable workspace-relative names and native filesystem alias checks.

Only internally derived Paths should be serialized with ``.as_posix()``.
Untrusted saved/request strings are validated, never repaired or normalized.
Absolute external source paths have a separate, native-path contract.
"""
import re
import stat
import os
from pathlib import Path, PurePosixPath, PureWindowsPath


def relative_parts(relative):
    if not isinstance(relative, str) or not relative:
        raise ValueError(f'Expected a canonical workspace-relative path: {relative!r}')
    if any(c in relative for c in '\\:<>"|?*#') or any(ord(c) < 32 for c in relative):
        raise ValueError(f'Expected a canonical workspace-relative path: {relative!r}')
    parts = relative.split('/')
    for part in parts:
        device = part.split('.')[0].rstrip(' ')
        if (not part or part in ('.', '..') or part.endswith((' ', '.'))
                or re.fullmatch(r'(?:CON|CONIN\$|CONOUT\$|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])', device, re.IGNORECASE)):
            raise ValueError(f'Path contains unsafe or noncanonical components: {relative!r}')
    return parts


def is_link_or_reparse(info):
    """Include Windows junctions on Python 3.11, without following their targets."""
    return (stat.S_ISLNK(info.st_mode)
            or bool(getattr(info, 'st_file_attributes', 0)
                    & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400)))


def foreign_absolute(value):
    return ((os.name == 'nt' and PurePosixPath(value).is_absolute() and not PureWindowsPath(value).is_absolute())
            or (os.name != 'nt' and PureWindowsPath(value).is_absolute()))


def source_path_string(root, value):
    """Retain foreign absolute metadata; never reinterpret it under this workspace."""
    if '\x00' in value or '..' in PurePosixPath(value).parts or '..' in PureWindowsPath(value).parts:
        raise ValueError('Source traversal or NUL is prohibited')
    if foreign_absolute(value):
        return value
    path = Path(value)
    if path.drive and not path.is_absolute():
        raise ValueError('Drive-relative source paths are prohibited')
    if os.name == 'nt' and path.root and not path.drive:
        raise ValueError('Drive-rooted source paths require an explicit drive')
    return str(path if path.is_absolute() else root / path)


def native_source_path(value):
    if foreign_absolute(value):
        raise ValueError('Recording/usage source belongs to another operating system and is unavailable here: ' + value)
    return Path(value)
