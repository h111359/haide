"""Read-only recording evidence and scheduling; no background hooks are assumed."""
from pathlib import Path
import sys
from .storage import checked_path, read_json, SafetyError
from .activities import envelope
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'activities'))
from recording_gate import assess_closure

def handle(operation, workspace, request, apply):
    op = operation.split('.')[-1].split('/')[-1]
    try:
        fields = {'status':set(), 'schedule':{'occurrence_ids','covered_ids','threshold','last_dispatched_count'}}
        if not isinstance(request,dict) or (op in fields and set(request) - fields[op]): raise ValueError('Unknown or invalid request fields')
        if apply: return envelope(operation, 'input_error', issues=['Recording operations are read-only'])
        if op == 'assess-closure':
            result = assess_closure(request)
            return envelope(operation, 'ok' if result['ok'] else 'blocked', result, issues=result['issues'])
        if op == 'status':
            state = read_json(checked_path(workspace, '.hai_env/state.json', allow_missing=False))
            config = state.get('features', {}).get('chronicles', {})
            if type(config.get('enabled')) is not bool: raise ValueError('recording enablement is unverified')
            return envelope(operation, result={'enabled': config['enabled'], 'record_every_prompts': config.get('record_every_prompts', 5), 'source': 'unavailable', 'coverage': 'unverified', 'synchronization': 'unsupported'})
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
    except (SafetyError, OSError, ValueError, TypeError) as exc:
        return envelope(operation, 'input_error' if isinstance(exc,(ValueError, TypeError)) else 'blocked', issues=[str(exc)])
