"""Core exact-source Activity chronicles. Never discovers session sources."""
from datetime import datetime, timezone
import hashlib
import json
import re
from pathlib import Path
import uuid
from zoneinfo import ZoneInfo

from .storage import SafetyError, checked_path, fingerprint, read_json, write_bytes, write_json
from .usage import binding, provenance, stamp


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def occurrence(session, position):
    return {'source_session_id': session, 'source_position': position}


def assignment(root, value):
    if not isinstance(value, dict) or set(value) - {'path', 'session_id', 'start_position', 'end_position', 'representation', 'enabled_intervals'}:
        raise ValueError('Invalid chronicle source assignment')
    b = binding(root, {k: v for k, v in value.items() if k in {'path', 'session_id', 'start_position', 'end_position'}})
    b['representation'] = value.get('representation')
    if b['representation'] not in ('event_msg', 'response_item'):
        raise ValueError('Explicit chronicle representation required')
    intervals = value.get('enabled_intervals')
    if not isinstance(intervals, list) or not intervals:
        raise ValueError('Attributable enabled intervals required')
    previous = -1
    for interval in intervals:
        if not isinstance(interval, dict) or set(interval) != {'start', 'end', 'provenance'} or not isinstance(interval['provenance'], str) or not interval['provenance'].strip():
            raise ValueError('Invalid chronicle enabled interval')
        positions = []
        for key in ('start', 'end'):
            point = interval[key]
            if point is None and key == 'end':
                positions.append(None); continue
            if not isinstance(point, dict) or set(point) != {'source_session_id', 'source_position'} or point['source_session_id'] != b['session_id'] or type(point['source_position']) is not int or point['source_position'] < b['start_position']:
                raise ValueError('Interval must use assigned source positions')
            positions.append(point['source_position'])
        start, end = positions
        if start <= previous or (end is not None and end < start) or (b['end_position'] is not None and (end is None or end > b['end_position'])):
            raise ValueError('Overlapping or out-of-assignment enabled intervals')
        previous = end if end is not None else float('inf')
    b['enabled_intervals'] = intervals
    return b


def load(root, base, ident):
    ledger = checked_path(root, base + '/chronicles/core.json')
    fp = fingerprint(ledger)
    directory = checked_path(root, base + '/chronicles')
    if fp is None:
        if directory.exists() and any(directory.iterdir()):
            raise SafetyError('Existing chronicles lack a core binding ledger; explicit adoption required')
        return None, fp
    data = read_json(ledger)
    if not isinstance(data, dict) or set(data) != {'core_format_version', 'activity_id', 'updated_at', 'sources', 'artifact_hashes', 'provenance', 'enablement_revision'} or type(data['core_format_version']) is not int or data['core_format_version'] != 1 or data['activity_id'] != ident:
        raise SafetyError('Invalid chronicle core ledger')
    stamp(data['updated_at']); provenance(data['provenance'])
    if type(data['enablement_revision']) is not int or data['enablement_revision'] < 0:
        raise SafetyError('Invalid chronicle enablement revision')
    if not isinstance(data['sources'], list) or not data['sources'] or not isinstance(data['artifact_hashes'], dict):
        raise SafetyError('Invalid chronicle core sources/artifacts')
    seen = set()
    for entry in data['sources']:
        if not isinstance(entry, dict) or set(entry) != {'binding', 'prefix_bytes', 'prefix_sha256', 'segment_path', 'original_started_at', 'closure_binding'}:
            raise SafetyError('Invalid chronicle core source')
        b = assignment(root, entry['binding'])
        if b != entry['binding'] or b['session_id'] in seen or type(entry['prefix_bytes']) is not int or entry['prefix_bytes'] < 0:
            raise SafetyError('Invalid/duplicate chronicle binding')
        if not isinstance(entry['prefix_sha256'], str) or not re.fullmatch('[a-f0-9]{64}', entry['prefix_sha256']):
            raise SafetyError('Invalid source prefix fingerprint')
        seen.add(b['session_id'])
        if entry['closure_binding'] is not None:
            assignment(root, entry['closure_binding'])
        if not isinstance(entry['segment_path'], str) or not entry['segment_path'].startswith('chronicles/') or entry['segment_path'] not in data['artifact_hashes']:
            raise SafetyError('Missing chronicle segment hash')
    if 'chronicles/checkpoint.json' not in data['artifact_hashes']:
        raise SafetyError('Missing chronicle checkpoint hash')
    for relative, expected in data['artifact_hashes'].items():
        if not isinstance(relative, str) or not relative.startswith('chronicles/') or relative == 'chronicles/core.json':
            raise SafetyError('Invalid chronicle artifact path')
        target = checked_path(root, base + '/' + relative, allow_missing=False)
        if fingerprint(target)[-1] != expected:
            raise SafetyError('Chronicle artifact changed: ' + relative)
    checkpoint = read_json(checked_path(root, base + '/chronicles/checkpoint.json', allow_missing=False))
    if not isinstance(checkpoint, dict) or type(checkpoint.get('checkpoint_format_version')) is not int or checkpoint['checkpoint_format_version'] != 1 or checkpoint.get('activity_id') != ident:
        raise SafetyError('Invalid chronicle checkpoint identity/format')
    if checkpoint.get('pending_ranges') != [] or checkpoint.get('in_flight') is not None:
        raise SafetyError('Pending/prepared/interrupted chronicle work requires explicit reconciliation')
    recorded = checkpoint.get('sources')
    if not isinstance(recorded, list) or len(recorded) != len(data['sources']):
        raise SafetyError('Checkpoint sources differ from binding ledger')
    for source, entry in zip(recorded, data['sources']):
        b = entry['binding']
        if not isinstance(source, dict) or source.get('source_session_id') != b['session_id'] or source.get('durable_path') != b['path'] or source.get('enabled_intervals') != b['enabled_intervals']:
            raise SafetyError('Checkpoint source assignment differs from ledger')
        ranges = source.get('assigned_ranges')
        if not isinstance(ranges, list) or len(ranges) != 1:
            raise SafetyError('Invalid checkpoint source range')
        r = ranges[0]
        if not isinstance(r, dict) or set(r) != {'start', 'end'}:
            raise SafetyError('Invalid checkpoint range')
        positions = []
        for key in ('start', 'end'):
            point = r[key]
            if not isinstance(point, dict) or set(point) != {'source_session_id', 'source_position'} or point['source_session_id'] != b['session_id'] or type(point['source_position']) is not int:
                raise SafetyError('Invalid checkpoint occurrence')
            positions.append(point['source_position'])
        if not b['start_position'] <= positions[0] <= positions[1] or (b['end_position'] is not None and positions[1] > b['end_position']):
            raise SafetyError('Checkpoint range escapes assignment')
    expected_verified = [{'range': s['assigned_ranges'][0], 'segment_path': e['segment_path'], 'verified_at': data['updated_at']} for s, e in zip(recorded, data['sources'])]
    if checkpoint.get('verified_ranges') != expected_verified:
        raise SafetyError('Checkpoint coverage differs from ledger')
    return data, fp


def read_assigned(b, previous=None):
    from chronicles.read_codex_source import read_source
    path = Path(b['path'])
    if path.resolve(strict=True) != path or any(p.is_symlink() for p in (path, *path.parents)) or path.stat().st_nlink != 1:
        raise SafetyError('Chronicle source must be canonical, regular and nonlinked')
    before = fingerprint(path)
    raw = path.read_bytes()
    if previous and (len(raw) < previous['prefix_bytes'] or digest(raw[:previous['prefix_bytes']]) != previous['prefix_sha256']):
        raise SafetyError('Previously observed chronicle source changed or was truncated')
    extracted = read_source(path, b['representation'], b['session_id'])
    if not extracted['ok'] or fingerprint(path) != before or extracted['source_sha256'] != digest(raw):
        raise SafetyError('Chronicle source unavailable/incomplete/changed: ' + str(extracted['issues']))
    messages = [m for m in extracted['messages'] if m['source_position'] >= b['start_position'] and (b['end_position'] is None or m['source_position'] <= b['end_position']) and any(m['source_position'] >= interval['start']['source_position'] and (interval['end'] is None or m['source_position'] <= interval['end']['source_position']) for interval in b['enabled_intervals'])]
    if not messages:
        raise SafetyError('No completed eligible source in assigned chronicle range')
    if previous and previous['original_started_at'] != extracted['original_started_at']:
        raise SafetyError('Chronicle original source identity changed')
    return raw, extracted, messages


def assert_fresh(b, raw, messages):
    # Appended tool/progress records are harmless; new eligible exchanges are not.
    newer, _, current = read_assigned(b)
    if len(newer) < len(raw) or newer[:len(raw)] != raw or current != messages:
        raise SafetyError('Chronicle source gained eligible text or changed; refresh required')


def check_overlaps(root, base, entries):
    """Inspect only other Activities' binding metadata, never transcript text."""
    store = checked_path(root, str(Path(base).parent), allow_missing=False)
    for child in store.iterdir():
        if not child.is_dir() or child == root / base:
            continue
        checked_path(root, str(child.relative_to(root)), allow_missing=False)
        otherpath = checked_path(root, str(child.relative_to(root)) + '/chronicles/core.json')
        if not otherpath.exists():
            # Legacy checkpoint metadata may claim ranges we cannot infer safely.
            legacy = checked_path(root, str(child.relative_to(root)) + '/chronicles/checkpoint.json')
            if legacy.exists():
                old = read_json(legacy)
                if not isinstance(old, dict) or not isinstance(old.get('sources'), list) or not old['sources']:
                    raise SafetyError('Invalid legacy recording assignment metadata')
                for source in old['sources']:
                    if not isinstance(source, dict) or not isinstance(source.get('source_session_id'), str) or not source['source_session_id'].strip():
                        raise SafetyError('Invalid legacy source identity')
                    for new in entries:
                        if source.get('source_session_id') != new['session_id']:
                            continue
                        ranges = source.get('assigned_ranges')
                        if not isinstance(ranges, list) or not ranges:
                            raise SafetyError('Related legacy source assignment needs explicit overlap review')
                        for r in ranges:
                            bounds = [r.get(k, {}).get('source_position') for k in ('start', 'end')] if isinstance(r, dict) else []
                            if len(bounds) != 2 or any(type(p) is not int or p < 0 for p in bounds) or bounds[1] < bounds[0]:
                                raise SafetyError('Related legacy boundaries need explicit overlap review')
                            if max(bounds[0], new['start_position']) <= min(bounds[1], new['end_position'] if new['end_position'] is not None else float('inf')):
                                raise SafetyError('Chronicle assignment overlaps retained legacy coverage')
            continue
        childbase = str(child.relative_to(root))
        state = read_json(checked_path(root, childbase + '/state.json', allow_missing=False))
        other, _ = load(root, childbase, state['activity_id'])
        for existing in other['sources']:
            b = existing['binding']
            for new in entries:
                if b['session_id'] == new['session_id'] and max(b['start_position'], new['start_position']) <= min(b['end_position'] if b['end_position'] is not None else float('inf'), new['end_position'] if new['end_position'] is not None else float('inf')):
                    raise SafetyError('Chronicle assignment overlaps another Activity; finalize prior boundary explicitly')


def render(ident, b, started, messages):
    metadata = {'source_session_id': b['session_id'], 'durable_path': b['path'], 'original_started_at': started, 'activity_id': ident,
                'representation': b['representation'], 'assigned_start': b['start_position'], 'assigned_end': b['end_position'],
                'last_verified_source_position': messages[-1]['source_position'], 'enabled_intervals': b['enabled_intervals']}
    text = '# Activity transcript\n\n## Source:\n\n' + json.dumps(metadata, ensure_ascii=True, indent=2) + '\n\n'
    for message in messages:
        text += ('## Prompt:\n\n' if message['role'] == 'user' else '## Outcome:\n\n') + message['text'] + '\n\n'
    return text.encode('utf-8')


def synchronize(root, base, ident, request, time, apply, expected_state, required=True, finalize=False):
    """Prepare/refresh exact assigned transcripts, then checkpoint and ledger last."""
    if not required:
        return {'activity_id': ident, 'status': 'disabled', 'details': 'Recording disabled; no independent obligation'}, []
    old, ledger_fp = load(root, base, ident)
    environment_path = checked_path(root, '.hai_env/state.json', allow_missing=False)
    environment_fp = fingerprint(environment_path)
    revision = read_json(environment_path)['features']['chronicles'].get('enablement_revision', 0)
    if type(revision) is not int or revision < 0:
        raise SafetyError('Invalid chronicle enablement revision')
    boundary_changed = old is not None and old['enablement_revision'] != revision
    if boundary_changed and 'sources' not in request:
        raise SafetyError('Recording enablement changed; explicit updated enabled intervals required')
    entries = {e['binding']['session_id']: e for e in old['sources']} if old else {}
    # A fresh explicit operation on the still-active Activity resumes its retained
    # live assignment after an interrupted closure. Historical closed ranges stay fixed.
    state = read_json(checked_path(root, base + '/state.json', allow_missing=False))
    if state['lifecycle'] != 'active':
        raise SafetyError('Synchronization requires an active Activity')
    for sid, entry in list(entries.items()):
        if entry.get('closure_binding') is not None:
            entries[sid] = dict(entry, binding=entry['closure_binding'], closure_binding=None)
    supplied = request.get('sources', [])
    if not isinstance(supplied, list):
        raise ValueError('Chronicle sources must be an array')
    seen = set()
    for value in supplied:
        b = assignment(root, value)
        if b['session_id'] in seen:
            raise ValueError('Duplicate chronicle source identity')
        seen.add(b['session_id'])
        if b['session_id'] in entries and entries[b['session_id']]['binding'] != b:
            previous_binding = entries[b['session_id']]['binding']
            if not boundary_changed or {k: v for k, v in b.items() if k != 'enabled_intervals'} != {k: v for k, v in previous_binding.items() if k != 'enabled_intervals'}:
                raise SafetyError('Chronicle assignment changes require explicit resolution')
            entries[b['session_id']] = dict(entries[b['session_id']], binding=b)
        if b['session_id'] not in entries:
            entries[b['session_id']] = {'binding': b}
    if boundary_changed and not {e['binding']['session_id'] for e in old['sources']} <= seen:
        raise SafetyError('Updated enabled intervals required for every recorded source')
    if not entries:
        raise SafetyError('Enabled chronicles require explicit source assignments before closure/synchronization')
    check_overlaps(root, base, [e['binding'] for e in entries.values()])
    outputs, new_entries, observations, sources, verified, cursors = {}, [], [], [], [], {}
    taken = set(old['artifact_hashes']) if old else set()
    for entry in entries.values():
        b = json.loads(json.dumps(entry['binding'])); previous = entry if 'prefix_bytes' in entry else None
        raw, extracted, messages = read_assigned(b, previous)
        if boundary_changed and previous:
            prior = next(e for e in old['sources'] if e['binding']['session_id'] == b['session_id'])
            _, _, prior_messages = read_assigned(prior['binding'], prior)
            observed_lines = len(raw[:prior['prefix_bytes']].splitlines())
            old_positions = {m['source_position'] for m in prior_messages if m['source_position'] < observed_lines}
            if not old_positions <= {m['source_position'] for m in messages}:
                raise SafetyError('Updated intervals would remove previously recorded exchanges')
        closure_binding = entry.get('closure_binding')
        if finalize and b['end_position'] is None:
            closure_binding = json.loads(json.dumps(b))
            b['end_position'] = messages[-1]['source_position']
            b['enabled_intervals'] = [dict(i, end=occurrence(b['session_id'], min(i['end']['source_position'], b['end_position']) if i['end'] else b['end_position'])) for i in b['enabled_intervals'] if i['start']['source_position'] <= b['end_position']]
        segment = entry.get('segment_path')
        if segment is None:
            start = datetime.fromisoformat(extracted['original_started_at'].replace('Z', '+00:00')).astimezone(ZoneInfo('Europe/Sofia')).strftime('%Y%m%d_%H%M%S')
            n = 1
            while True:
                segment = f'chronicles/{start}_segment-{n:02d}.md'
                if segment not in taken and not checked_path(root, base + '/' + segment).exists():
                    break
                n += 1
            taken.add(segment)
        outputs[segment] = render(ident, b, extracted['original_started_at'], messages)
        new_entries.append({'binding': b, 'prefix_bytes': len(raw), 'prefix_sha256': digest(raw), 'segment_path': segment, 'original_started_at': extracted['original_started_at'], 'closure_binding': closure_binding})
        observations.append((b, raw, messages))
        r = {'start': occurrence(b['session_id'], messages[0]['source_position']), 'end': occurrence(b['session_id'], messages[-1]['source_position'])}
        sources.append({'source_session_id': b['session_id'], 'durable_path': b['path'], 'original_started_at': extracted['original_started_at'], 'assigned_ranges': [r], 'enabled_intervals': b['enabled_intervals'], 'retained_source_complete': True})
        verified.append({'range': r, 'segment_path': segment, 'verified_at': time})
        users = [m for m in messages if m['role'] == 'user']
        if users: cursors[b['session_id']] = occurrence(b['session_id'], users[-1]['source_position'])
    attempt = str(uuid.uuid4())
    checkpoint = {'checkpoint_format_version': 1, 'activity_id': ident, 'sources': sources, 'verified_ranges': verified, 'pending_ranges': [], 'cadence_cursors': cursors,
                  'last_attempt': {'attempt_id': attempt, 'dispatch_cursors': cursors, 'started_at': time, 'finished_at': time, 'status': 'verified', 'error': None}, 'last_successful_at': time, 'in_flight': None}
    outputs['chronicles/checkpoint.json'] = (json.dumps(checkpoint, ensure_ascii=True, indent=2) + '\n').encode()
    ledger = {'core_format_version': 1, 'activity_id': ident, 'updated_at': time, 'sources': new_entries, 'artifact_hashes': {p: digest(raw) for p, raw in outputs.items()}, 'provenance': provenance(request['provenance']), 'enablement_revision': revision}
    expected_artifacts = {}
    for relative in outputs:
        current = fingerprint(checked_path(root, base + '/' + relative))
        expected_hash = old['artifact_hashes'].get(relative) if old else None
        if (expected_hash is None and current is not None) or (expected_hash is not None and (current is None or current[-1] != expected_hash)):
            raise SafetyError('Chronicle target changed during preparation: ' + relative)
        expected_artifacts[relative] = current
    result = {'activity_id': ident, 'status': 'verified' if apply else 'planned', 'segments': [e['segment_path'] for e in new_entries], 'checkpoint_path': base + '/chronicles/checkpoint.json', 'cutoff': [v['range']['end'] for v in verified], 'source_count': len(new_entries), 'message_count': sum(len(o[2]) for o in observations)}
    if not apply:
        return result, []
    changed = []
    try:
        if fingerprint(checked_path(root, base + '/state.json', allow_missing=False)) != expected_state:
            raise SafetyError('Activity changed before recording')
        if fingerprint(environment_path) != environment_fp:
            raise SafetyError('Recording settings changed before synchronization')
        if fingerprint(checked_path(root, base + '/chronicles/core.json')) != ledger_fp:
            raise SafetyError('Chronicle ledger changed before recording')
        for b, raw, messages in observations: assert_fresh(b, raw, messages)
        directory = checked_path(root, base + '/chronicles')
        if not directory.exists(): directory.mkdir(); changed.append(base + '/chronicles')
        for relative, content in outputs.items():
            write_bytes(root, base + '/' + relative, content, expected_artifacts[relative])
            changed.append(base + '/' + relative)
        write_json(root, base + '/chronicles/core.json', ledger, ledger_fp); changed.append(base + '/chronicles/core.json')
        load(root, base, ident)
        for b, raw, messages in observations: assert_fresh(b, raw, messages)
        if fingerprint(checked_path(root, base + '/state.json', allow_missing=False)) != expected_state:
            raise SafetyError('Activity changed during recording')
        if fingerprint(environment_path) != environment_fp:
            raise SafetyError('Recording settings changed during synchronization')
        return result, changed
    except Exception as exc:
        raise SafetyError(str(exc), list(dict.fromkeys(changed + getattr(exc, 'changed_files', [])))) from exc


def verify(root, base, ident, closing=False):
    data, _ = load(root, base, ident)
    if data is None:
        raise SafetyError('No core chronicle checkpoint to verify')
    revision = read_json(checked_path(root, '.hai_env/state.json', allow_missing=False))['features']['chronicles'].get('enablement_revision', 0)
    active = read_json(checked_path(root, base + '/state.json', allow_missing=False))['lifecycle'] == 'active'
    if active and revision != data['enablement_revision']:
        raise SafetyError('Recording enablement changed; synchronize explicit intervals first')
    for entry in data['sources']:
        b = entry['binding']; raw, extracted, messages = read_assigned(b, entry)
        if active and not closing and entry['closure_binding'] is not None:
            raise SafetyError('Interrupted closure assignment requires fresh synchronization')
        target = checked_path(root, base + '/' + entry['segment_path'], allow_missing=False)
        if target.read_bytes() != render(ident, b, extracted['original_started_at'], messages):
            raise SafetyError('Chronicles do not cover current eligible source; synchronize required')
        if closing and entry['closure_binding'] is not None:
            _, _, live = read_assigned(entry['closure_binding'], entry)
            if live != messages:
                raise SafetyError('New eligible exchange appeared after closure cutoff')
    return {'activity_id': ident, 'status': 'verified', 'source_count': len(data['sources']), 'checkpoint_path': base + '/chronicles/checkpoint.json'}
