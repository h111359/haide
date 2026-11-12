"""Source-bounded usage snapshots; token counters are not subscription charges."""
from datetime import datetime
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import json
from pathlib import Path
import re
import stat
from path_contract import source_path_string, native_source_path, is_link_or_reparse

from .storage import SafetyError, _pairs, checked_path, fingerprint, read_json, write_bytes, write_json

METRICS = ('input_tokens', 'cached_input_tokens', 'output_tokens',
           'reasoning_output_tokens', 'total_tokens')
RATE_KEYS = {'input_credits_per_million', 'cached_input_credits_per_million', 'output_credits_per_million'}
ROOT_KEYS = {'usage_format_version', 'activity_id', 'updated_at', 'provenance',
             'sources', 'pricing', 'reported_spend', 'summary', 'markdown_sha256'}


def nonblank(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + ' must be nonblank text')
    return value


def stamp(value):
    if not isinstance(value, str) or datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%dT%H:%M:%SZ') != value:
        raise ValueError('Expected a UTC timestamp')
    return value


def provenance(value):
    if not isinstance(value, dict):
        raise ValueError('Usage provenance required')
    return {k: nonblank(value.get(k), 'provenance.' + k) for k in ('source', 'reason')}


def number(value):
    if not isinstance(value, str) or len(value) > 100 or not re.fullmatch(r'[0-9]+(?:\.[0-9]+)?', value):
        raise ValueError('Rates and spend must be nonnegative decimal strings')
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError('Invalid decimal') from exc
    if not result.is_finite() or result < 0:
        raise ValueError('Rates and spend must be finite and nonnegative')
    return format(result, 'f')


def pricing(value):
    if value is None:
        return None
    if not isinstance(value, dict) or not {'rates', 'source', 'captured_at'} <= value.keys() or set(value) - {'rates', 'source', 'captured_at'}:
        raise ValueError('Invalid pricing snapshot fields')
    rates = value['rates']
    if not isinstance(rates, dict) or not rates:
        raise ValueError('pricing.rates must be a nonempty model map')
    normalized = {}
    for model, rate in rates.items():
        nonblank(model, 'rate model')
        if not isinstance(rate, dict) or set(rate) != RATE_KEYS:
            raise ValueError('Each model rate needs input, cached input and output credit rates')
        normalized[model] = {k: number(rate[k]) for k in sorted(RATE_KEYS)}
    return {'rates': normalized, 'source': nonblank(value['source'], 'pricing.source'),
            'captured_at': stamp(value['captured_at'])}


def reported(value):
    if value is None:
        return None
    if not isinstance(value, dict) or set(value) != {'credits', 'source', 'through'}:
        raise ValueError('Reported spend needs credits, source and through')
    through = value['through']
    if not isinstance(through, dict) or any(not isinstance(k, str) or not k.strip() or type(v) is not int or v < 0 for k, v in through.items()):
        raise ValueError('Reported spend through must map source IDs to observed positions')
    return {'credits': number(value['credits']) if value['credits'] is not None else None,
            'source': nonblank(value['source'], 'reported spend source'),
            'through': dict(through)}


def tokens(value):
    if not isinstance(value, dict) or not set(METRICS) <= value.keys() or any(type(value[k]) is not int or value[k] < 0 for k in METRICS):
        raise ValueError('Token counters must be nonnegative integers, not Booleans')
    result = {k: value[k] for k in METRICS}
    if (result['cached_input_tokens'] > result['input_tokens']
            or result['reasoning_output_tokens'] > result['output_tokens']
            or result['total_tokens'] != result['input_tokens'] + result['output_tokens']):
        raise ValueError('Inconsistent token counter subsets or total')
    return result


def binding(root, value):
    if not isinstance(value, dict) or not {'path', 'session_id', 'start_position'} <= value.keys() or set(value) - {'path', 'session_id', 'start_position', 'end_position'}:
        raise ValueError('A source needs path, session_id and start_position')
    path = source_path_string(root, nonblank(value['path'], 'source path'))
    start, end = value['start_position'], value.get('end_position')
    if type(start) is not int or start < 0 or (end is not None and (type(end) is not int or end < start)):
        raise ValueError('Invalid inclusive source positions')
    return {'path': str(path), 'session_id': nonblank(value['session_id'], 'source session_id'),
            'start_position': start, 'end_position': end}


def observe(b, previous):
    """Read only one explicitly assigned saved source; never discover sessions."""
    path = native_source_path(b['path'])
    if path.resolve(strict=True) != path or any(is_link_or_reparse(p.lstat()) for p in (path, *path.parents)):
        raise SafetyError('Usage source must be canonical and nonlinked')
    before = path.stat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise SafetyError('Usage source must be an unaliased regular file')
    raw = path.read_bytes()
    after = path.stat()
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
        raise SafetyError('Usage source changed during reading')
    if previous and hashlib.sha256(raw[:previous['prefix_bytes']]).hexdigest() != previous['prefix_sha256']:
        raise SafetyError('Previously observed usage source prefix changed or was truncated')
    lines = raw.splitlines(keepends=True)
    end = b['end_position'] if b['end_position'] is not None else len(lines) - 1
    if b['start_position'] > end or end >= len(lines):
        raise SafetyError('Assigned usage range is not retained yet')
    prefix = b''.join(lines[:end + 1])
    if not prefix.endswith(b'\n'):
        raise SafetyError('Usage source has an incomplete record at the assigned cutoff')
    last = {k: 0 for k in METRICS}
    sums = {k: 0 for k in METRICS}
    models = {}
    current_model = '(unknown)'
    session = None
    original_start = None
    baseline = None
    through = None
    through_time = None
    for position, line in enumerate(lines[:end + 1]):
        record = json.loads(line.decode('utf-8'), object_pairs_hook=_pairs,
                            parse_constant=lambda _: (_ for _ in ()).throw(ValueError('Non-JSON source constant')))
        if not isinstance(record, dict) or not isinstance(record.get('payload'), dict):
            raise ValueError('Unsupported saved source record')
        payload = record['payload']
        if position == 0 and record.get('type') != 'session_meta':
            raise ValueError('Usage requires source retained from its session metadata')
        if record.get('type') == 'session_meta':
            identity = nonblank(payload.get('id'), 'saved session ID')
            started = nonblank(payload.get('timestamp', record.get('timestamp')), 'original session timestamp')
            if session is not None and (identity != session or started != original_start):
                raise ValueError('Conflicting resumed source identity')
            session, original_start = identity, started
            if session != b['session_id']:
                raise ValueError('Saved source identity differs from assigned session')
        elif record.get('type') == 'turn_context':
            model = payload.get('model')
            current_model = model if isinstance(model, str) and model.strip() else '(unknown)'
        elif record.get('type') == 'event_msg' and payload.get('type') == 'token_count':
            info = payload.get('info')
            if info is None:
                continue  # A limit-only event supplies no token measurement.
            if not isinstance(info, dict):
                raise ValueError('Unsupported token_count info')
            total = tokens(info.get('total_token_usage'))
            delta = {k: total[k] - last[k] for k in METRICS}
            if any(v < 0 for v in delta.values()):
                raise ValueError('Cumulative token counters decreased; do not infer a reset')
            tokens(delta)
            if position < b['start_position']:
                baseline = position
            else:
                model_totals = models.setdefault(current_model, {k: 0 for k in METRICS})
                for k in METRICS:
                    sums[k] += delta[k]
                    model_totals[k] += delta[k]
                through = position
                through_time = nonblank(record.get('timestamp'), 'token observation timestamp')
            last = total
    if session != b['session_id'] or through is None:
        raise SafetyError('No usable token snapshots in the assigned source range')
    return {'tokens': sums, 'by_model': models, 'through_position': through,
            'through_timestamp': through_time, 'observed_end_position': end,
            'baseline_position': baseline, 'prefix_bytes': len(prefix),
            'prefix_sha256': hashlib.sha256(prefix).hexdigest()}


def summarize(sources, rates, spend):
    known = [s['observation'] for s in sources if s['observation'] is not None]
    coverage = 'observed' if sources and all(s['status'] == 'current' for s in sources) else 'partial' if known else 'unavailable'
    total = {k: sum(o['tokens'][k] for o in known) for k in METRICS} if known else None
    models = {}
    for o in known:
        for model, value in o['by_model'].items():
            merged = models.setdefault(model, {k: 0 for k in METRICS})
            for k in METRICS:
                merged[k] += value[k]
    estimate = None
    if rates and coverage == 'observed' and set(models) <= rates['rates'].keys():
        with localcontext() as context:
            context.prec = 10000  # Exact for bounded decimal rates and JSON integer counters.
            estimate = Decimal(0)
            for model, t in models.items():
                rate = rates['rates'][model]
                estimate += ((t['input_tokens'] - t['cached_input_tokens']) * Decimal(rate['input_credits_per_million'])
                             + t['cached_input_tokens'] * Decimal(rate['cached_input_credits_per_million'])
                             + t['output_tokens'] * Decimal(rate['output_credits_per_million'])) / Decimal(1000000)
            estimate = format(estimate, 'f')
    expected = {s['binding']['session_id']: s['observation']['through_position'] for s in sources if s['observation']}
    report_current = spend is not None and spend['through'] == expected and all(s['status'] == 'current' for s in sources)
    return {'coverage': coverage, 'tokens': total, 'by_model': models,
            'estimated_credits': estimate,
            'reported_credits': spend['credits'] if report_current else None,
            'reported_spend_current': report_current,
            'missing_rate_models': sorted(set(models) - rates['rates'].keys()) if rates else sorted(models)}


def cell(value):
    return str(value).replace('&', '&amp;').replace('|', '&#124;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', ' ')


def render(data):
    s = data['summary']
    lines = ['# Activity usage', '', 'Activity: `' + data['activity_id'] + '`', '',
             'Updated: ' + data['updated_at'], '', 'Coverage: **' + s['coverage'] + '** for explicitly assigned source ranges only.', '',
             'This is the latest observed snapshot, not an invoice. Unregistered sessions and future or unsaved usage are not included.', '',
             '## Tokens', '', '| Metric | Observed value |', '| --- | --- |']
    for key in METRICS:
        lines.append('| ' + key + ' | ' + (str(s['tokens'][key]) if s['tokens'] is not None else 'Unavailable') + ' |')
    lines += ['', 'Cached input is included in input; reasoning is included in output. Total is input plus output, without adding those subsets again.', '',
              'Partial/stale coverage shows last-known token values; it does not establish complete current usage.', '',
              '## Credits', '', '| Kind | Value |', '| --- | --- |']
    for label, value in [('Caller-reported credits', s['reported_credits']),
                         ('Estimated credit equivalent', s['estimated_credits'])]:
        lines.append('| ' + label + ' | ' + (cell(value) if value is not None else 'Unavailable') + ' |')
    lines += ['', 'Estimates use the supplied rate snapshot; they are not actual debited credits or subscription charges. Quota percentages and remaining credit balances are never spend.', '']
    if data['pricing']:
        rate = data['pricing']
        lines += ['Rate source: ' + cell(rate['source']), '', 'Rate captured: ' + rate['captured_at'], '',
                  '| Model | Input credits / 1M | Cached input credits / 1M | Output credits / 1M |', '| --- | --- | --- | --- |']
        for model, values in sorted(rate['rates'].items()):
            lines.append('| ' + ' | '.join(cell(v) for v in [model, values['input_credits_per_million'], values['cached_input_credits_per_million'], values['output_credits_per_million']]) + ' |')
        lines += ['']
    if data['reported_spend']:
        lines += ['Reported-spend evidence: ' + cell(data['reported_spend']['source']), '',
                  'Reported evidence matches current source cutoffs: ' + str(s['reported_spend_current']), '']
    lines += ['## Sources', '', '| Session | Assigned positions | Latest token position | Status |', '| --- | --- | --- | --- |']
    errors = []
    for source in data['sources']:
        b, o = source['binding'], source['observation']
        lines.append('| ' + ' | '.join(cell(v) for v in [b['session_id'], str(b['start_position']) + '..' + (str(b['end_position']) if b['end_position'] is not None else 'live'), o['through_position'] if o else 'Unavailable', source['status']]) + ' |')
        if source['error']:
            errors.append('- ' + cell(b['session_id']) + ': ' + cell(source['error']))
    if errors:
        lines += ['', *errors]
    if not data['sources']:
        lines += ['', 'No usage sources have been assigned. Values are unavailable, not zero.']
    lines += ['', 'Source cutoffs, last-good observations and provenance are retained in `usage.json`. Updates before closure include only usage already available at that time.', '']
    return '\n'.join(lines).encode('utf-8')


def load(root, base, activity_id):
    ledger = checked_path(root, base + '/usage.json')
    report = checked_path(root, base + '/usage.md')
    ledger_fp, report_fp = fingerprint(ledger), fingerprint(report)
    if ledger_fp is None:
        if report_fp is not None:
            raise SafetyError('Existing usage.md has no checkpoint; preserve it for explicit adoption')
        return None, ledger_fp, report_fp
    try:
        data = read_json(ledger)
        if not isinstance(data, dict) or set(data) != ROOT_KEYS or type(data['usage_format_version']) is not int or data['usage_format_version'] not in (1, 2) or data['activity_id'] != activity_id:
            raise ValueError('Invalid or mismatched usage checkpoint')
        # Read the unreleased v1 checkpoint only when discarded monetary fields
        # are null. Non-null historical values require explicit preservation.
        if data['usage_format_version'] == 1:
            for container, keys in [(data['pricing'], ('currency', 'money_per_credit')),
                                    (data['reported_spend'], ('money',)),
                                    (data['summary'], ('estimated_money', 'reported_money'))]:
                if container is not None:
                    for key in keys:
                        if container.get(key) is not None:
                            raise ValueError('Non-null legacy money data requires explicit preservation')
                        container.pop(key, None)
        stamp(data['updated_at']); provenance(data['provenance'])
        pricing(data['pricing']); reported(data['reported_spend'])
        if not isinstance(data['sources'], list):
            raise ValueError('Usage sources must be an array')
        seen = set()
        for source in data['sources']:
            if not isinstance(source, dict) or set(source) != {'binding', 'observation', 'status', 'error'}:
                raise ValueError('Invalid usage source checkpoint')
            b = binding(root, source['binding'])
            if b != source['binding'] or b['session_id'] in seen:
                raise ValueError('Duplicate or noncanonical source binding')
            seen.add(b['session_id'])
            o = source['observation']
            if source['status'] not in ('current', 'stale', 'unavailable') or (source['status'] == 'unavailable') != (o is None):
                raise ValueError('Invalid observation status')
            if source['status'] == 'current' and source['error'] is not None or source['status'] != 'current' and not isinstance(source['error'], str):
                raise ValueError('Invalid observation error')
            if o is not None:
                if not isinstance(o, dict) or set(o) != {'tokens', 'by_model', 'through_position', 'through_timestamp', 'observed_end_position', 'baseline_position', 'prefix_bytes', 'prefix_sha256'}:
                    raise ValueError('Invalid observation fields')
                tokens(o['tokens'])
                if not isinstance(o['by_model'], dict) or not o['by_model']:
                    raise ValueError('Invalid model counters')
                for model, counts in o['by_model'].items():
                    nonblank(model, 'observed model'); tokens(counts)
                if any(sum(t[k] for t in o['by_model'].values()) != o['tokens'][k] for k in METRICS):
                    raise ValueError('Model counters differ from source totals')
                for key in ('through_position', 'observed_end_position', 'prefix_bytes'):
                    if type(o[key]) is not int or o[key] < 0:
                        raise ValueError('Invalid observation boundary')
                if o['through_position'] < b['start_position'] or o['through_position'] > o['observed_end_position'] or not re.fullmatch('[a-f0-9]{64}', o['prefix_sha256']):
                    raise ValueError('Invalid observation range or fingerprint')
                nonblank(o['through_timestamp'], 'observation time')
                if o['baseline_position'] is not None and (type(o['baseline_position']) is not int or not 0 <= o['baseline_position'] < b['start_position']):
                    raise ValueError('Invalid baseline boundary')
        if json.dumps(data['summary'], sort_keys=True) != json.dumps(summarize(data['sources'], data['pricing'], data['reported_spend']), sort_keys=True):
            raise ValueError('Usage summary differs from retained observations')
        if report_fp is None or data['markdown_sha256'] != hashlib.sha256(report.read_bytes()).hexdigest():
            raise ValueError('Usage report is missing or changed; inspect before replacing it')
        return data, ledger_fp, report_fp
    except (ValueError, TypeError, KeyError) as exc:
        raise SafetyError(str(exc)) from exc


def update(root, base, activity_id, request, time, apply, expected_state):
    old, ledger_fp, report_fp = load(root, base, activity_id)
    entries = json.loads(json.dumps(old['sources'])) if old else []
    if 'sources' in request:
        if not isinstance(request['sources'], list):
            raise ValueError('sources must be an array')
        supplied = set()
        for raw in request['sources']:
            b = binding(root, raw)
            if b['session_id'] in supplied:
                raise ValueError('Duplicate supplied session ID')
            supplied.add(b['session_id'])
            existing = next((s for s in entries if s['binding']['session_id'] == b['session_id']), None)
            if existing and existing['binding'] != b:
                raise ValueError('Existing source assignments are immutable; resolve changed attribution explicitly')
            if not existing:
                entries.append({'binding': b, 'observation': None, 'status': 'unavailable', 'error': 'Not yet observed'})
    rates = pricing(request['pricing']) if 'pricing' in request else old['pricing'] if old else None
    spend = reported(request['reported_spend']) if 'reported_spend' in request else old['reported_spend'] if old else None
    for entry in entries:
        try:
            entry['observation'] = observe(entry['binding'], entry['observation'])
            entry['status'], entry['error'] = 'current', None
        except (SafetyError, OSError, ValueError, UnicodeError, KeyError, TypeError) as exc:
            entry['status'] = 'stale' if entry['observation'] is not None else 'unavailable'
            entry['error'] = str(exc)
    data = {'usage_format_version': 2, 'activity_id': activity_id, 'updated_at': time,
            'provenance': provenance(request['provenance']), 'sources': entries,
            'pricing': rates, 'reported_spend': spend, 'summary': summarize(entries, rates, spend)}
    markdown = render(data)
    data['markdown_sha256'] = hashlib.sha256(markdown).hexdigest()
    result = {'activity_id': activity_id, 'path': base + '/usage.md',
              'checkpoint_path': base + '/usage.json', 'updated_at': time, 'summary': data['summary']}
    if not apply:
        return result, []
    changed = []
    try:
        if fingerprint(checked_path(root, base + '/state.json', allow_missing=False)) != expected_state:
            raise SafetyError('Activity changed before usage update')
        write_json(root, base + '/usage.json', data, ledger_fp)
        changed.append(base + '/usage.json')
        write_bytes(root, base + '/usage.md', markdown, report_fp)
        changed.append(base + '/usage.md')
        load(root, base, activity_id)
        if fingerprint(checked_path(root, base + '/state.json', allow_missing=False)) != expected_state:
            raise SafetyError('Activity changed during usage update')
        return result, changed
    except (SafetyError, OSError) as exc:
        changed.extend(p for p in getattr(exc, 'changed_files', []) if p not in changed)
        raise SafetyError(str(exc), changed) from exc


def read(root, base, activity_id):
    data, _, _ = load(root, base, activity_id)
    return {'activity_id': activity_id, 'path': base + '/usage.md', 'available': data is not None,
            'updated_at': data['updated_at'] if data else None,
            'summary': data['summary'] if data else {'coverage': 'unavailable', 'tokens': None}}
