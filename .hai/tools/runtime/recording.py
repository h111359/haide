"""Read-only recording evidence and scheduling; no background hooks are assumed."""
from pathlib import Path
import sys
from .storage import checked_path, read_json, SafetyError, lock, fingerprint
from .activities import envelope
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'activities'))
from recording_gate import assess_closure

def handle(operation, workspace, request, apply):
    op = operation.split('.')[-1].split('/')[-1]
    try:
        source_fields = {'session_id', 'source_path', 'codex_home', 'representation', 'mandatory', 'provenance'}
        fields = {'status':set(), 'schedule':{'occurrence_ids','covered_ids','threshold','last_dispatched_count'},
                  'discover': source_fields, 'bind': source_fields | {'activity_id', 'start_position', 'enabled_intervals'},
                  'synchronize': {'activity_id', 'sources', 'provenance', 'mandatory'}, 'verify': {'activity_id'}}
        if not isinstance(request,dict) or (op in fields and set(request) - fields[op]): raise ValueError('Unknown or invalid request fields')
        if apply and op not in ('synchronize', 'bind'): return envelope(operation, 'input_error', issues=['Only recording synchronize/bind support --apply'])
        if op in ('synchronize', 'verify', 'discover', 'bind'):
            from .startup import require_mutation_context
            from .activities import store_path, discover, now, required_text, handle as activity_handle
            from . import chronicles
            root = Path(workspace).resolve(strict=True)
            def execute():
                require_mutation_context(root)
                if op in ('discover', 'bind'):
                    from . import source_discovery
                    if not source_discovery.enabled(root, request):
                        return envelope(operation, result={'status': 'disabled', 'details': 'Recording disabled; no independent obligation'})
                    source = source_discovery.resolve(root, request)
                    if op == 'discover':
                        return envelope(operation, result=source)
                context = discover(root, store_path(root))
                ident = required_text(request.get('activity_id'), 'activity_id')
                if op == 'verify':
                    selected = activity_handle('show', root, {'activity_id': ident}, False)
                    if not selected['ok']:
                        raise SafetyError('Activity not safely/uniquely found')
                    return envelope(operation, result=chronicles.verify(root, selected['result']['path'], ident))
                if context['status'] != 'current' or context['activity_id'] != ident:
                    raise SafetyError('Chronicle recording requires the sole current Activity')
                base = context['path']
                if op == 'bind':
                    from .activities import provenance
                    provenance(request)
                    start = request.get('start_position')
                    _, extracted = source_discovery.inspect_source(root, source['path'], source['session_id'], source['representation'])
                    if type(start) is not int or not any(m['source_position'] == start and m['role'] == 'user' for m in extracted['messages']):
                        raise ValueError('start_position must identify an observed saved user occurrence, never an inferred timestamp')
                    binding = {k: source[k] for k in ('path', 'session_id', 'representation')}
                    binding.update(start_position=start, enabled_intervals=request.get('enabled_intervals'))
                    chronicles.assignment(root, binding)
                    request_for_sync = {'sources': [binding], 'provenance': request['provenance']}
                    result, changed = chronicles.synchronize(root, base, ident, request_for_sync, now(), apply,
                        fingerprint(checked_path(root, base + '/state.json', allow_missing=False)))
                    result['source'] = source
                    result['usage_source'] = {k: binding[k] for k in ('path', 'session_id', 'start_position')}
                    return envelope(operation, 'ok' if apply else 'planned', result, changed)
                enabled = read_json(checked_path(root, '.hai_env/state.json', allow_missing=False))['features']['chronicles']['enabled']
                mandatory = request.get('mandatory', False)
                if type(mandatory) is not bool:
                    raise ValueError('mandatory must be Boolean and attributable to workspace instructions')
                result, changed = chronicles.synchronize(root, base, ident, request, now(), apply,
                    fingerprint(checked_path(root, base + '/state.json', allow_missing=False)), required=enabled or mandatory)
                return envelope(operation, 'ok' if apply else 'planned', result, changed)
            if apply:
                with lock(root): return execute()
            return execute()
        if op == 'assess-closure':
            result = assess_closure(request)
            return envelope(operation, 'ok' if result['ok'] else 'blocked', result, issues=result['issues'])
        if op == 'status':
            state = read_json(checked_path(workspace, '.hai_env/state.json', allow_missing=False))
            config = state.get('features', {}).get('chronicles', {})
            if type(config.get('enabled')) is not bool: raise ValueError('recording enablement is unverified')
            return envelope(operation, result={'enabled': config['enabled'], 'record_every_prompts': config.get('record_every_prompts', 5), 'source': 'host_assigned', 'coverage': 'unverified', 'synchronization': 'core recording synchronize'})
        if op == 'schedule':
            occurrences = request.get('occurrence_ids'); covered = request.get('covered_ids', []); threshold = request.get('threshold', 5)
            if (not isinstance(occurrences,list) or not isinstance(covered,list) or type(threshold) is not int or threshold < 1
                or any(not isinstance(x,str) or not x for x in occurrences + covered) or len(set(occurrences)) != len(occurrences) or len(set(covered)) != len(covered)):
                raise ValueError('occurrence_ids and covered_ids must be unique nonempty strings and threshold positive')
            if not set(covered).issubset(occurrences): raise ValueError('coverage contains unobserved occurrences')
            cursor = request.get('last_dispatched_count', 0)
            if type(cursor) is not int or cursor < 0 or cursor > len(occurrences): raise ValueError('last_dispatched_count must index the observed occurrences')
            pending = [x for x in occurrences if x not in set(covered)]
            return envelope(operation, result={'observed_ids': occurrences, 'covered_ids': covered, 'gaps': pending, 'dispatch_due': len(occurrences) - cursor >= threshold, 'last_dispatched_count': cursor, 'new_since_dispatch': len(occurrences) - cursor, 'threshold': threshold, 'checkpoint_persisted': False})
        return envelope(operation, 'unsupported', issues=['Recording operation or host integration is unsupported'])
    except (SafetyError, OSError, ValueError, TypeError, KeyError) as exc:
        changed = getattr(exc, 'changed_files', [])
        return envelope(operation, 'partial' if changed else 'input_error' if isinstance(exc,(ValueError, TypeError)) else 'blocked', changed=changed, issues=[str(exc)])
