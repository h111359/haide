"""Pure clarification preparation/validation. Persistence belongs to the host/runtime."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import uuid

START = '<!-- hai-clarification-event:v1 -->\n```json\n'
END = '<!-- /hai-clarification-event -->\n'
BASE_ITEMS = tuple(f'R{category}.{item}' for category, count in enumerate((4, 3, 3, 4, 2, 4, 5, 3), 1)
                   for item in range(1, count + 1))


def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + ' must be nonempty text')
    return value


def question_block(question):
    lines = [f"### {question['id']} — Unanswered", '', question['question'], '',
             'Implementation impact: ' + question['impact'], '']
    for option in question['options']:
        label = option['label']
        recommendation = ' (Recommended)' if label == question['recommended'] else ''
        lines.append(f"- [ ] {label}: {option['text']}{recommendation}")
    lines += ['- Other: ___', '', 'Status: unanswered']
    return '\n'.join(lines)


def display(event):
    if event['kind'] == 'questions':
        blocks = '\n\n'.join(question_block(q) for q in event['questions'])
        form = '\n'.join(q['id'] + ': ' + ', '.join(o['label'] + ' [ ]' for o in q['options'])
                         + ', Other: ___' for q in event['questions'])
        return f"### Batch {event['batch_id']}\n\n{blocks}\n\nAnswer form:\n\n{form}"
    # JSON encoding preserves raw Unicode and exact newlines in a readable code block.
    return '### ' + event['kind'].capitalize() + '\n\n' + json.dumps(
        {k: v for k, v in event.items() if k not in ('sequence', 'activity_id')},
        ensure_ascii=False, indent=2)


def render(event):
    return START + json.dumps(event, ensure_ascii=False, indent=2) + '\n```\n\n' + display(event) + '\n' + END


def validate(events, activity_id):
    uuid.UUID(activity_id)
    questions, responses, unresolved, identities = {}, {}, {}, set()
    mapping_targets, mapped = {}, {}
    batches = 0
    for sequence, event in enumerate(events, 1):
        if (event.get('activity_id') != activity_id or type(event.get('sequence')) is not int
                or event['sequence'] != sequence):
            raise ValueError('Activity identity or event sequence mismatch')
        identity = text(event.get('event_id'), 'event_id')
        if identity in identities:
            raise ValueError('duplicate event_id')
        identities.add(identity)
        for name in ('author', 'source', 'at'):
            text(event.get(name), name)
        if not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', event['at']):
            raise ValueError('at must be a supplied UTC timestamp')
        if event['kind'] == 'questions':
            batches += 1
            if event.get('batch_id') != f'B{batches:03}' or not event.get('questions'):
                raise ValueError('invalid batch identity or empty questions')
            for q in event['questions']:
                expected = f'Q{len(questions) + 1:03}'
                if q.get('id') != expected or q.get('status') != 'unanswered' or q.get('other') != '___':
                    raise ValueError('question IDs/status/free-text placeholder are not canonical')
                text(q.get('question'), 'question'); text(q.get('impact'), 'impact')
                options = q.get('options')
                if not isinstance(options, list):
                    raise ValueError('options must be a list (empty for free-text questions)')
                labels = []
                for index, option in enumerate(options):
                    label = chr(ord('A') + index)
                    if index >= 26 or option.get('label') != label or option.get('checked') is not False:
                        raise ValueError('options require consecutive A–Z labels and unchecked choices')
                    text(option.get('text'), 'option text'); labels.append(label)
                if q.get('recommended') is not None and q['recommended'] not in labels:
                    raise ValueError('recommendation must identify an offered option')
                questions[q['id']] = q
        elif event['kind'] == 'unresolved':
            text(event.get('raw'), 'raw response'); text(event.get('reason'), 'mapping reason')
            candidates = event.get('candidate_question_ids')
            if not isinstance(candidates, list) or not candidates or any(q not in questions for q in candidates):
                raise ValueError('unresolved response needs known candidate question IDs')
            unresolved[identity] = event
        elif event['kind'] in ('response', 'revision'):
            qid = event.get('question_id')
            if qid not in questions:
                raise ValueError('unknown question ID')
            history = responses.setdefault(qid, [])
            if type(event.get('response_number')) is not int or event['response_number'] != len(history) + 1:
                raise ValueError('invalid per-question response number')
            if event['kind'] == 'revision':
                if not history or event.get('supersedes') != history[-1]['event_id']:
                    raise ValueError('revision must supersede the latest effective response')
            elif history or event.get('supersedes') is not None:
                raise ValueError('changed answers require an explicit revision')
            text(event.get('raw'), 'raw response')
            parts = event.get('parts')
            if not isinstance(parts, dict) or not parts or any(not isinstance(k, str) or not k.strip()
                    or not isinstance(v, str) or not v.strip() for k, v in parts.items()):
                raise ValueError('parts must map exact question-part names to nonblank verbatim answers')
            mapping = event.get('resolves_event_id')
            if mapping is not None:
                original = unresolved.get(mapping)
                if (not original or qid not in original['candidate_question_ids']
                        or event['raw'] != original['raw']):
                    raise ValueError('mapping must retain the unresolved raw response and candidate ID')
                text(event.get('mapping_text'), 'actual human mapping clarification')
                targets = event.get('mapped_question_ids')
                if (not isinstance(targets, list) or not targets or len(set(targets)) != len(targets)
                        or qid not in targets or any(q not in original['candidate_question_ids'] for q in targets)):
                    raise ValueError('mapping needs the complete human-confirmed target question IDs')
                target_set = set(targets)
                if mapping in mapping_targets and mapping_targets[mapping] != target_set:
                    raise ValueError('mapped target scope changed within the same unresolved event')
                mapping_targets[mapping] = target_set
                mapped.setdefault(mapping, set()).add(qid)
            history.append(event)
        else:
            raise ValueError('unknown event kind')
    return {'questions': questions, 'responses': responses,
            'unresolved': [key for key in unresolved if key not in mapping_targets
                           or mapped.get(key, set()) != mapping_targets[key]],
            'unanswered': [key for key in questions if key not in responses],
            'effective': {key: history[-1] for key, history in responses.items()}}


def parse(ledger, activity_id):
    if not isinstance(ledger, str):
        raise ValueError('ledger must be text')
    events, cursor = [], 0
    while True:
        start = ledger.find(START, cursor)
        if start < 0:
            break
        event, length = json.JSONDecoder().raw_decode(ledger[start + len(START):])
        if not isinstance(event, dict):
            raise ValueError('event must be an object')
        # Match the entire canonical visible block, not a regex vulnerable to raw user text.
        encoded = render(event)
        if ledger[start:start + len(encoded)] != encoded:
            raise ValueError('ledger event/readback content differs from canonical saved block')
        events.append(event)
        cursor = start + len(encoded)
    # Never interpret a damaged event marker as absence of prior dialogue.
    outside = ledger
    for event in events:
        outside = outside.replace(render(event), '', 1)
    if 'hai-clarification-event' in outside:
        raise ValueError('incomplete or unsupported clarification event')
    validate(events, activity_id)
    return events


def read_ledger(path, activity_id):
    path = Path(path)
    # A dangling symlink is invalid, not an absent ledger.
    if path.is_symlink():
        raise ValueError(str(path) + ': linked ledger is forbidden')
    if not path.exists():
        return '', []
    with path.open('r', encoding='utf-8', newline='') as stream:
        raw = stream.read()
    return raw, parse(raw, activity_id)


def prepare(ledger, activity_id, event):
    """Return append-only candidate bytes; a duplicate source event is a no-op."""
    events = parse(ledger, activity_id)
    proposed = deepcopy(event)
    proposed.update(activity_id=activity_id, sequence=len(events) + 1)
    for prior in events:
        if prior['event_id'] == proposed.get('event_id'):
            proposed['sequence'] = prior['sequence']
            if proposed != prior:
                raise ValueError('event_id reused with different content')
            return ledger
    validate(events + [proposed], activity_id)
    return ledger + ('\n' if ledger and not ledger.endswith('\n') else '') + render(proposed)


def next_ids(ledger, activity_id):
    events = parse(ledger, activity_id)
    state = validate(events, activity_id)
    return f"B{1 + sum(e['kind'] == 'questions' for e in events):03}", f"Q{1 + len(state['questions']):03}"


def verify_readback(before, candidate, actual, activity_id, event_id):
    if not candidate.startswith(before) or not actual.startswith(candidate):
        raise ValueError('ledger predecessor or exact append readback mismatch')
    events = parse(actual, activity_id)
    matches = [e for e in events if e['event_id'] == event_id]
    if len(matches) != 1:
        raise ValueError('saved event not uniquely verified')
    return matches[0]


def readiness_items(convention):
    items = re.findall(r'^- \[ \] \*\*(R\d+\.\d+) ', convention, re.M)
    if len(items) != len(set(items)) or [i for i in items if i in BASE_ITEMS] != list(BASE_ITEMS):
        raise ValueError('readiness convention changed or omitted stable initial identifiers/order')
    # Each category stays contiguous; additions follow existing items in that category.
    positions = [tuple(map(int, i[1:].split('.'))) for i in items]
    if positions != sorted(positions):
        raise ValueError('readiness extensions must append within their category')
    categories = sorted({category for category, _ in positions})
    if categories != list(range(1, max(categories) + 1)):
        raise ValueError('new categories require the next category number')
    for category in categories:
        numbers = [number for cat, number in positions if cat == category]
        if numbers != list(range(1, len(numbers) + 1)):
            raise ValueError('new items require the next unused item number')
    return tuple(items)


def assess_readiness(items, checks, *, blockers=(), exemption=None):
    if exemption:
        text(exemption.get('reason'), 'exemption reason')
        valid = ((exemption.get('kind') == 'internal_framework_upkeep'
                  and exemption.get('user_visible_change') is False)
                 or (exemption.get('kind') == 'urgent_clear_defect'
                     and all(exemption.get(k) is True for k in ('urgent', 'clear', 'single_reversible_change'))))
        if not valid:
            raise ValueError('request does not meet a narrow readiness exemption')
        return {'status': 'exempt' if not blockers else 'fail', 'exemption': exemption,
                'failed': [], 'blockers': list(blockers)}
    if set(checks) - set(items):
        raise ValueError('unknown readiness check')
    failed = []
    for item in items:
        check = checks.get(item, {})
        valid = check.get('satisfied') is True and isinstance(check.get('evidence'), str) and bool(check['evidence'].strip())
        basis = check.get('basis', 'evidence')
        if basis not in ('evidence', 'assumption', 'deferral'):
            valid = False
        if basis in ('assumption', 'deferral'):
            valid = (valid and check.get('resolves_uncertainty') is True
                     and check.get('requires_human_decision') is False
                     and isinstance(check.get('consequences_if_false'), str)
                     and bool(check['consequences_if_false'].strip()))
        if not valid:
            failed.append(item)
    return {'status': 'pass' if not failed and not blockers else 'fail', 'failed': failed,
            'blockers': list(blockers), 'checks': deepcopy(checks)}


def validate_proposal(proposal, assessment, ledger, activity_id, *, blockers=()):
    state = validate(parse(ledger, activity_id), activity_id)
    if assessment.get('status') not in ('pass', 'exempt') or blockers or assessment.get('blockers'):
        raise ValueError('readiness or consequential blockers prevent proposal')
    if state['unanswered'] or state['unresolved']:
        raise ValueError('unverified/unresolved dialogue prevents proposal')
    if re.search(r'^#{1,2}(?:\s|$)', proposal, re.M):
        raise ValueError('proposal headings must be level three or deeper')
    for heading in ('Intent', 'Effective decisions', 'Context', 'Outcomes', 'Scope',
                    'Exclusions', 'Constraints and assumptions', 'Acceptance criteria'):
        if not re.search(r'^### ' + re.escape(heading) + r'[ \t]*\n(?:[ \t]*\n)*[^\s#]', proposal, re.M):
            raise ValueError('proposal needs nonempty section: ' + heading)
    return {'status': 'ready_for_human_review', 'activity_id': activity_id,
            'target': 'proposed current Activity input', 'sha256': hashlib.sha256(proposal.encode()).hexdigest()}


def protection_check(before, after, authorized_prefixes=()):
    """Snapshots are path->digest, including absent/deleted paths by set difference."""
    protected = ('.hai', 'hai_agents_library/agents', '.hai_env/agents')
    def under(path, prefix):
        return path == prefix or path.startswith(prefix + '/')
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p)
                     and any(under(p, prefix) for prefix in protected))
    unauthorized = [p for p in changed if not any(under(p, prefix) for prefix in authorized_prefixes)]
    return {'ok': not unauthorized, 'changed_protected_paths': changed, 'unauthorized': unauthorized,
            'error': 'ERROR: Protected framework modified without authorization; workflow stopped.' if unauthorized else None}
