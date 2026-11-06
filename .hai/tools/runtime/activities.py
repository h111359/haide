"""Activity lifecycle operations. All caller-supplied narrative remains attributed."""
from pathlib import Path
from datetime import datetime, timezone
import re
import sys
import uuid
from .storage import SafetyError, checked_path, fingerprint, read_json, write_bytes, write_json, lock

_TOOLS = Path(__file__).resolve().parents[1]
for _part in ('agents', 'startup', 'activities'):
    sys.path.insert(0, str(_TOOLS / _part))
from discovery import discover, _validate_state, STEPS, STEP_VALUES

CURRENT = '00000000_000000_active'
ARTIFACTS = {'definition.md', 'analysis.md', 'decisions.md', 'plan.md', 'requirements.md'}
MUTATIONS = ('create', 'record', 'close', 'supplement', 'chat-post')

def now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def envelope(op, status='ok', result=None, changed=None, issues=None):
    return {'ok': status in ('ok', 'planned'), 'status': status, 'operation': op,
            'result': result or {}, 'changed_files': changed or [], 'issues': issues or []}

def required_text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + ' must be nonempty text')
    return value

def provenance(request):
    p = request.get('provenance')
    if not isinstance(p, dict): raise ValueError('provenance is required')
    return 'source: ' + required_text(p.get('source'), 'provenance.source') + '; reason: ' + required_text(p.get('reason'), 'provenance.reason')

def store_path(root):
    state = read_json(checked_path(root, '.hai_env/state.json', allow_missing=False))
    location = state.get('activities', {}).get('location')
    path = checked_path(root, location)
    if path.exists() and not path.is_dir(): raise SafetyError('Activity store is not a directory')
    for reserved in ('.hai', '.git', '.hai_env/agents', '.hai_env/config', '.hai_env/state.json', '.hai_env/agent_instructions.md', '.hai_env/model_profiles.json'):
        if location == reserved or location.startswith(reserved + '/') or reserved.startswith(location + '/'):
            raise SafetyError('Activity store overlaps a protected path')
    return location

def rename_preflight():
    import ctypes, os, sys
    if os.name == 'nt': return 'windows'
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform.startswith('linux') and hasattr(libc, 'renameat2'):
        import errno
        probe = libc.renameat2
        probe.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        probe.restype = ctypes.c_int
        probe(-100, b'', -100, b'', 1)
        if ctypes.get_errno() in (errno.ENOSYS, errno.EINVAL): raise SafetyError('Atomic no-replace rename is unsupported by this system')
        return 'linux'
    if sys.platform == 'darwin' and hasattr(libc, 'renamex_np'): return 'darwin'
    raise SafetyError('Atomic no-replace rename is unavailable on this platform')

def rename_exclusive(source, destination):
    import ctypes, os
    platform = rename_preflight()
    if platform == 'windows':
        os.rename(source, destination)  # Windows rename fails when destination exists.
        return
    libc = ctypes.CDLL(None, use_errno=True)
    if platform == 'linux':
        func = libc.renameat2
        func.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        args = (-100, os.fsencode(source), -100, os.fsencode(destination), 1)
    else:
        func = libc.renamex_np
        func.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        args = (os.fsencode(source), os.fsencode(destination), 4)  # RENAME_EXCL
    func.restype = ctypes.c_int
    if func(*args):
        code = ctypes.get_errno()
        raise OSError(code, os.strerror(code), str(destination))

def check_recording_files(root, base, proof, paths):
    """Compare fresh, safe workspace file hashes against supplied proof snapshots."""
    if not isinstance(paths, dict): raise SafetyError('Recording source and artifact paths required')
    evidence = proof['evidence']
    for kind, snapshot_key in (('sources','source_snapshots'), ('artifacts','artifact_snapshots')):
        mapping = paths.get(kind); expected = evidence.get(snapshot_key)
        if not isinstance(mapping,dict) or not isinstance(expected,dict) or set(mapping) != set(expected):
            raise SafetyError('Recording path mapping does not match evidence')
        for key, relative in mapping.items():
            if kind == 'artifacts':
                if not isinstance(relative,str) or not relative.startswith(base + '/'): raise SafetyError('Recording artifact must be inside the selected Activity')
            path = checked_path(root,relative,allow_missing=False)
            current = fingerprint(path)
            if current is None or current[-1] != expected[key]: raise SafetyError('Recording file changed or does not match proof: ' + relative)

def append_bytes(existing, text):
    return existing + (b'\n' if existing and not existing.endswith(b'\n') else b'') + text.encode('utf-8') + b'\n'

def handle(operation, workspace, request, apply):
    op = operation.split('.')[-1].split('/')[-1]
    root = Path(workspace).resolve(strict=True)
    changed = []
    try:
        fields = {'discover':set(), 'show':{'activity_id'}, 'create':{'initial_input','provenance'}, 'record':{'activity_id','steps','implementation_start','artifacts','input_append','log','provenance'}, 'close':{'activity_id','outcome','archive_label','outcome_text','recording','recording_requirement','recording_proof','recording_paths','provenance'}, 'supplement':{'activity_id','text','provenance'}}
        fields['chat-read'] = {'activity_id', 'after_sequence', 'limit'}
        fields['chat-post'] = {'activity_id', 'author', 'text', 'provenance'}
        if not isinstance(request,dict) or (op in fields and set(request) - fields[op]): raise ValueError('Unknown or invalid request fields')
        location = store_path(root)
        def run():
            if apply and op in MUTATIONS:
                from .startup import require_mutation_context
                require_mutation_context(root)
            d = discover(root, location)
            if d['status'] == 'invalid': raise SafetyError('Activity store invalid: ' + str(d['issues']))
            if op == 'discover': return envelope(operation, result=d)
            if op in ('show', 'chat-read'):
                if op == 'chat-read' and apply:
                    raise ValueError('chat-read is read-only; omit --apply')
                ident = required_text(request.get('activity_id'), 'activity_id')
                matches = []
                for child in checked_path(root, location).iterdir():
                    state = read_json(checked_path(root, f'{location}/{child.name}/state.json', allow_missing=False))
                    if state.get('activity_id') == ident: matches.append((child, state))
                if len(matches) != 1: raise SafetyError('Activity ID not uniquely found')
                child, state = matches[0]
                if op == 'chat-read':
                    from . import chat
                    return envelope(operation, result=chat.read(root, str(child.relative_to(root)), ident, request))
                return envelope(operation, result={'path': str(child.relative_to(root)), 'state': state})
            prov = provenance(request)
            stamp = now()
            if op == 'create':
                initial = request.get('initial_input')
                if not isinstance(initial, str): raise ValueError('initial_input must be text')
                if d['status'] != 'absent': raise SafetyError('A current Activity already exists')
                base = f'{location}/{CURRENT}'
                state = {'activity_id': str(uuid.uuid4()), 'lifecycle': 'active', 'created_at': stamp,
                         'closed_at': None, 'outcome': None, 'implementation_started_at': None,
                         'steps': {k: 'not_started' for k in sorted(STEPS)}}
                paths = [base + '/' + n for n in ('state.json', 'input.md', 'log.md')]
                if not apply: return envelope(operation, 'planned', {'state': state, 'paths': paths})
                store = checked_path(root, location)
                if not store.exists():
                    store.mkdir(parents=True); changed.append(location)
                checked_path(root, base).mkdir(); changed.append(base)
                for path, data in [(paths[0], None), (paths[1], initial.encode()), (paths[2], f'# Activity log\n\n- {stamp} — Created Activity ({prov}).\n'.encode())]:
                    if data is None: write_json(root, path, state)
                    else: write_bytes(root, path, data)
                    changed.append(path)
                if discover(root,location)['activity_id'] != state['activity_id']: raise SafetyError('Created Activity readback failed')
                return envelope(operation, result={'state': state, 'path': base}, changed=changed)
            ident = required_text(request.get('activity_id'), 'activity_id')
            if op == 'supplement':
                found = []
                for child in checked_path(root, location).iterdir():
                    s = read_json(checked_path(root, f'{location}/{child.name}/state.json', allow_missing=False))
                    if s.get('activity_id') == ident and s.get('lifecycle') == 'closed': found.append(child)
                if len(found) != 1: raise SafetyError('Closed Activity ID not uniquely found')
                text = required_text(request.get('text'), 'text')
                path = str((found[0] / 'log.md').relative_to(root)); target = checked_path(root, path, allow_missing=False); old = fingerprint(target)
                data = append_bytes(target.read_bytes(), f'\n- {stamp} — Supplement ({prov}): {text}')
                if apply: write_bytes(root, path, data, old); changed.append(path)
                return envelope(operation, 'ok' if apply else 'planned', {'path': path}, changed)
            if d['status'] != 'current' or d['activity_id'] != ident: raise SafetyError('Selected ID is not the sole current Activity')
            base = d['path']; state_path = base + '/state.json'; state_target = checked_path(root, state_path, allow_missing=False)
            state_fp = fingerprint(state_target); state = read_json(state_target); _validate_state(state)
            if op == 'chat-post':
                from . import chat
                relative, message, raw, expected = chat.prepare(root, base, ident, request, stamp)
                if not apply:
                    return envelope(operation, 'planned', {'path': relative, 'message': message})
                chat.append(root, relative, ident, message, raw, expected)
                return envelope(operation, result={'path': relative, 'message': message}, changed=[relative])
            if op == 'record':
                steps = request.get('steps', {})
                if not isinstance(steps, dict) or any(k not in STEPS or v not in STEP_VALUES for k,v in steps.items()): raise ValueError('invalid steps')
                start = request.get('implementation_start', False)
                if type(start) is not bool: raise ValueError('implementation_start must be boolean')
                if start and state['implementation_started_at'] is None: state['implementation_started_at'] = stamp
                state['steps'].update(steps); _validate_state(state)
                artifacts = request.get('artifacts', [])
                if not isinstance(artifacts, list): raise ValueError('artifacts must be a list')
                staged = []
                seen = set()
                for item in artifacts:
                    if not isinstance(item, dict) or item.get('name') not in ARTIFACTS or item['name'] in seen: raise ValueError('invalid or duplicate artifact')
                    name = item['name']; seen.add(name); text = required_text(item.get('text'), 'artifact.text'); reason = required_text(item.get('reason'), 'artifact.reason')
                    path = base + '/' + name; target = checked_path(root, path); fp = fingerprint(target)
                    if fp:
                        revdir = base + '/files/revisions/' + name[:-3]; checked_path(root, revdir)
                        seq = 1
                        while checked_path(root, f'{revdir}/{stamp.replace("-", "").replace(":", "").replace("T", "_").removesuffix("Z")}_{seq:02}.md').exists(): seq += 1
                        rev = f'{revdir}/{stamp.replace("-", "").replace(":", "").replace("T", "_").removesuffix("Z")}_{seq:02}.md'
                        staged.append((rev, target.read_bytes(), None, True))
                    staged.append((path, (text + f'\n\nRevision provenance: {prov}; reason: {reason}; recorded {stamp}.\n').encode(), fp, False))
                input_append = request.get('input_append')
                if input_append is not None:
                    if not isinstance(input_append, str): raise ValueError('input_append must be text')
                    ipath = base + '/input.md'; it = checked_path(root, ipath, allow_missing=False); ifp = fingerprint(it)
                    staged.append((ipath, it.read_bytes() + input_append.encode('utf-8'), ifp, False))
                log = required_text(request.get('log'), 'log'); logpath = base + '/log.md'; lt = checked_path(root, logpath, allow_missing=False); lfp = fingerprint(lt)
                staged.append((logpath, append_bytes(lt.read_bytes(), f'\n- {stamp} — {log} ({prov}).'), lfp, False))
                if not apply: return envelope(operation, 'planned', {'state': state, 'paths': [x[0] for x in staged] + [state_path]})
                for path,data,fp,revision in staged:
                    if revision:
                        parent = checked_path(root, str(Path(path).parent)); parent.mkdir(parents=True, exist_ok=True)
                    write_bytes(root, path, data, fp); changed.append(path)
                write_json(root, state_path, state, state_fp); changed.append(state_path)
                if read_json(checked_path(root,state_path,allow_missing=False)) != state: raise SafetyError('State readback mismatch')
                return envelope(operation, result={'state': state}, changed=changed)
            if op == 'close':
                outcome = request.get('outcome'); label = request.get('archive_label'); text = required_text(request.get('outcome_text'), 'outcome_text'); rec = request.get('recording')
                if outcome not in ('completed','cancelled','stopped') or not isinstance(label,str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+){0,4}',label): raise ValueError('invalid outcome or archive_label')
                if not isinstance(rec,dict) or rec.get('status') not in ('disabled','verified','pending','unavailable') or not isinstance(rec.get('details'),str): raise ValueError('explicit recording status and details required')
                enabled = read_json(checked_path(root, '.hai_env/state.json', allow_missing=False)).get('features', {}).get('chronicles', {}).get('enabled')
                if type(enabled) is not bool: raise SafetyError('Recording enablement is unverified')
                requirement = request.get('recording_requirement', {'enabled': enabled, 'mandatory': False})
                if not isinstance(requirement,dict) or type(requirement.get('mandatory')) is not bool or type(requirement.get('enabled')) is not bool or requirement['enabled'] != enabled: raise ValueError('invalid or inconsistent recording_requirement')
                if rec.get('mandatory') is True: requirement = {**requirement, 'mandatory': True}
                if rec['status'] == 'verified':
                    from .recording import assess_closure
                    proof = request.get('recording_proof')
                    if not isinstance(proof,dict) or proof.get('recording_requirement') != requirement or not isinstance(proof.get('operation'),dict) or proof['operation'].get('activity_id') != ident or not assess_closure(proof)['ok'] or not (requirement['enabled'] or requirement['mandatory']):
                        raise SafetyError('Recording verification evidence is missing or insufficient')
                    check_recording_files(root, base, proof, request.get('recording_paths'))
                elif requirement['mandatory']: raise SafetyError('Mandatory recording obligation is not verified')
                elif requirement['enabled'] and rec['status'] == 'disabled': raise SafetyError('Enabled recording must be reported accurately')
                name = stamp.replace('-','').replace(':','').replace('T','_').removesuffix('Z') + '_' + label; dest = location + '/' + name; n = 2
                while checked_path(root,dest).exists(): dest = location + '/' + name + f'_{n:02}'; n += 1
                outcome_path = base + '/outcome.md'; checked_path(root,outcome_path)
                if fingerprint(root / outcome_path) is not None: raise SafetyError('outcome already exists')
                state.update(lifecycle='closed',closed_at=stamp,outcome=outcome); _validate_state(state)
                if not apply: return envelope(operation,'planned',{'archive_path':dest,'state':state,'recording':rec})
                rename_preflight()
                logpath = base + '/log.md'; logtarget = checked_path(root,logpath,allow_missing=False); logfp = fingerprint(logtarget)
                write_bytes(root,logpath,append_bytes(logtarget.read_bytes(), f'\n- {stamp} — Closed as {outcome}; Activity path moved from {base} to {dest} ({prov}).'),logfp); changed.append(logpath)
                write_bytes(root,outcome_path,(f'# Outcome\n\n{text}\n\nRecording: {rec["status"]} — {rec["details"]}\n\nProvenance: {prov}\n').encode()); changed.append(outcome_path)
                if rec['status'] == 'verified': check_recording_files(root, base, proof, request.get('recording_paths'))
                write_json(root,state_path,state,state_fp); changed.append(state_path)
                final_fingerprints = {p: fingerprint(checked_path(root,p,allow_missing=False)) for p in (state_path, outcome_path, logpath)}
                # Rename only to a newly reserved name, with no overwrite.
                import os
                if checked_path(root,dest).exists(): raise SafetyError('Archive destination appeared')
                if rec['status'] == 'verified': check_recording_files(root, base, proof, request.get('recording_paths'))
                if any(fingerprint(checked_path(root,p,allow_missing=False)) != fp for p,fp in final_fingerprints.items()): raise SafetyError('Closure files changed before archival')
                rename_exclusive(checked_path(root,base,allow_missing=False), checked_path(root,dest)); changed.append(dest)
                if read_json(checked_path(root,dest + '/state.json',allow_missing=False)) != state or discover(root,location)['status'] != 'absent': raise SafetyError('Closure readback mismatch')
                return envelope(operation,result={'archive_path':dest,'state':state,'recording':rec},changed=changed)
            raise ValueError('unsupported Activity operation')
        if apply and op in MUTATIONS:
            with lock(root): return run()
        return run()
    except (ValueError, TypeError, KeyError) as exc:
        return envelope(operation,'partial' if changed else 'input_error',changed=changed,issues=[str(exc)])
    except (SafetyError, OSError, UnicodeError) as exc:
        changed.extend(x for x in getattr(exc, 'changed_files', []) if x not in changed)
        return envelope(operation,'partial' if changed else 'blocked',changed=changed,issues=[str(exc)])
