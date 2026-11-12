"""Read-only resolution of one host-identified Codex session, never reconstruction."""
from environment_paths import STATE, PROFILES, INSTRUCTIONS
import hashlib
import json
import os
from pathlib import Path
import stat
import uuid
from path_contract import native_source_path, is_link_or_reparse

from .storage import SafetyError, fingerprint, read_json, checked_path


def canonical(path, *, directory=False):
    path = native_source_path(str(path)).expanduser()
    if not path.is_absolute() or '..' in path.parts:
        raise SafetyError('Source locations must be absolute and contain no traversal')
    for part in (path, *path.parents):
        if is_link_or_reparse(part.lstat()):
            raise SafetyError('Linked source locations are forbidden: ' + str(part))
    if path.resolve(strict=True) != path:
        raise SafetyError('Source location must be canonical: ' + str(path))
    info = path.stat()
    if directory:
        if not stat.S_ISDIR(info.st_mode):
            raise SafetyError('Expected source storage directory: ' + str(path))
    elif not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise SafetyError('Source must be a singly linked regular file: ' + str(path))
    return path


def session_identity(request, environ):
    # Subagents can inherit a parent SESSION_ID while THREAD_ID identifies their
    # own rollout. Prefer the current execution thread, not the inherited parent.
    host = environ.get('CODEX_THREAD_ID') or environ.get('CODEX_SESSION_ID')
    values = [host] if host else []
    supplied = request.get('session_id')
    if supplied is not None:
        values.append(supplied)
    if not values:
        raise SafetyError('Current session identity unavailable; supply the authoritative host session_id')
    if any(not isinstance(v, str) or not v for v in values) or len(set(values)) != 1:
        raise SafetyError('Host and supplied session identities conflict')
    try:
        if str(uuid.UUID(values[0])) != values[0]:
            raise ValueError()
    except ValueError as exc:
        raise SafetyError('Current session identity must be a canonical UUID') from exc
    return values[0]


def inspect_source(workspace, path, identity, representation):
    from chronicles.read_codex_source import read_source
    path = canonical(path)
    before = fingerprint(path)
    raw = path.read_bytes()
    extracted = read_source(path, representation, identity)
    if not extracted['ok']:
        raise SafetyError('Saved source is unsupported or incomplete: ' + str(extracted['issues']))
    if fingerprint(path) != before or extracted['source_sha256'] != hashlib.sha256(raw).hexdigest():
        raise SafetyError('Source changed during discovery; no binding was made')
    metadata = [json.loads(line)['payload'] for line in raw.splitlines()
                if json.loads(line).get('type') == 'session_meta']
    if not metadata or any(not isinstance(m.get('cwd'), str)
                           or Path(m['cwd']).resolve() != workspace for m in metadata):
        raise SafetyError('Source workspace metadata does not match the selected workspace')
    users = [m for m in extracted['messages'] if m['role'] == 'user']
    result = {'path': str(path), 'session_id': identity, 'representation': representation,
              'original_started_at': extracted['original_started_at'],
              'source_sha256': extracted['source_sha256'],
              'latest_user_occurrence': ({'source_position': users[-1]['source_position'],
                                          'timestamp': users[-1]['timestamp']} if users else None)}
    return result, extracted


def resolve(workspace, request, environ=None):
    """Search filenames only; read content only after a unique exact-ID match."""
    root = Path(workspace).resolve(strict=True)
    environ = os.environ if environ is None else environ
    identity = session_identity(request, environ)
    representation = request.get('representation', 'event_msg')
    if representation not in ('event_msg', 'response_item'):
        raise ValueError('Unsupported source representation')
    if request.get('source_path') is not None:
        path = canonical(request['source_path'])
        method = 'host_supplied_path'
    else:
        home = request.get('codex_home', environ.get('CODEX_HOME') or str(Path.home() / '.codex'))
        sessions = canonical(canonical(home, directory=True) / 'sessions', directory=True)
        candidates = []
        def failed(error):
            raise SafetyError('Cannot establish unique current-session source: ' + str(error))
        for directory, dirs, files in os.walk(sessions, followlinks=False, onerror=failed):
            dirs[:] = [name for name in dirs
                       if not is_link_or_reparse((Path(directory) / name).lstat())]
            candidates.extend(Path(directory) / name for name in files
                              if name.startswith('rollout-') and name.endswith('-' + identity + '.jsonl'))
        if len(candidates) != 1:
            raise SafetyError(f'Expected one source for current session {identity}; found {len(candidates)}')
        path = canonical(candidates[0])
        method = 'current_session_filename'
    result, _ = inspect_source(root, path, identity, representation)
    if result['latest_user_occurrence'] is None:
        raise SafetyError('No saved user occurrence in selected representation ' + representation
                          + '; supply an explicit supported representation or wait for a saved work prompt')
    return {**result, 'discovery_method': method}


def enabled(workspace, request):
    flag = read_json(checked_path(workspace, STATE, allow_missing=False))['features']['chronicles']['enabled']
    mandatory = request.get('mandatory', False)
    if type(flag) is not bool or type(mandatory) is not bool:
        raise ValueError('Recording flags must be Boolean')
    if mandatory:
        from .activities import provenance
        provenance(request)  # The host identifies the independently applicable instruction.
    return flag or mandatory


def readiness(workspace, activity):
    """Separate recording readiness from environment validity; never write."""
    root = Path(workspace).resolve(strict=True)
    try:
        if not enabled(root, {}):
            return {'status': 'disabled', 'details': 'Optional recording is off; independent obligations remain host-owned'}
        if activity['status'] != 'current':
            return {'status': 'needs_activity' if activity['status'] == 'absent' else 'unverified'}
        from . import chronicles
        data, _ = chronicles.load(root, activity['path'], activity['activity_id'])
        host_ids = [os.environ[k] for k in ('CODEX_SESSION_ID', 'CODEX_THREAD_ID') if os.environ.get(k)]
        if not host_ids:
            return {'status': 'unverified', 'registered_source_count': len(data['sources']) if data else 0,
                    'details': 'Current host session identity unavailable; registered-source coverage alone does not establish current-session readiness'}
        identity = session_identity({}, os.environ)
        if data and any(e['binding']['session_id'] == identity for e in data['sources']):
            try:
                evidence = chronicles.verify(root, activity['path'], activity['activity_id'])
                return {'status': 'verified', 'details': 'Registered sources only; no claim about unknown sessions', **evidence}
            except SafetyError as exc:
                if str(exc) == 'Chronicles do not cover current eligible source; synchronize required':
                    return {'status': 'needs_synchronization', 'details': str(exc), 'next_operation': 'recording synchronize'}
                raise
        source = resolve(root, {})
        return {'status': 'needs_binding', 'source': source, 'next_operation': 'recording bind',
                'details': 'Supply the observed first work-prompt position and attributable enabled interval; no range inferred'}
    except (SafetyError, OSError, ValueError, TypeError, KeyError) as exc:
        return {'status': 'blocked', 'details': str(exc)}
