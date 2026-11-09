"""Read-only structural checks. Authority and semantic truth remain host duties."""
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import stat
import uuid

PHASE_SECTIONS = ['Purpose', 'Why now', 'Visible result', 'Scope', 'Actions', 'Affected files', 'Complete when']
ASSESSMENT_SECTIONS = ['Identity and input', 'Interpretation', 'Scope and exclusions', 'Evidence and findings',
                       'Edge conditions', 'Options', 'Knowledge effects', 'Decisions', 'Readiness']
PLAN_FIELDS = ['Format', 'Activity', 'Input revision', 'Decision revision', 'Mode', 'Readiness', 'Authority',
               'Business readiness', 'Readiness evidence', 'Business limits', 'Technical limits', 'Timing limits',
               'Authorization limits', 'Assumptions', 'Knowledge updates', 'Required owners']
TECHNICAL_CHECKS = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']


def meaningful(value):
    if not isinstance(value, str): return False
    for line in value.splitlines():
        line = re.sub(r'^\s*(?:[-*+] |\d+[.)] )', '', line)
        line = re.sub(r'^\s*\[[ xX]\]\s*', '', line).strip(' `*_\t')
        if line and line.lower() not in {'todo', 'tbd', '...', '___', '<fill>', 'placeholder', 'template'} and not re.fullmatch(r'<(?:fill|todo|tbd)[^>]*>', line, re.I):
            return True
    return False


def safe_file(workspace, value):
    """Only regular, singly linked, nonaliased files within the supplied root."""
    root = Path(workspace).resolve(strict=True)
    raw = Path(value)
    candidate = raw if raw.is_absolute() else root / raw
    if '..' in candidate.parts or not candidate.is_relative_to(root):
        raise ValueError('file must be inside workspace without traversal')
    cursor = root
    for part in candidate.relative_to(root).parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError('linked file or ancestor: ' + str(cursor))
    info = candidate.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise ValueError('expected regular singly linked file: ' + str(candidate))
    if '.git' in candidate.relative_to(root).parts:
        raise ValueError('version-control metadata is not a document input')
    return candidate


def clean_markdown(text):
    lines, fence = [], None
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
        if match:
            token, rest = match.groups()
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not rest.strip():
                fence = None
            lines.append('')
        elif fence is None:
            if re.search(r'<!--|</?[A-Za-z][\w:-]*(?:\s[^<>]*)?/?>', line):
                raise ValueError('HTML structure is unsupported')
            lines.append(line)
        else:
            lines.append('')
    if fence:
        raise ValueError('unclosed Markdown fence')
    return '\n'.join(lines)


def sections(text, level):
    pattern = re.compile(r'^' + '#' * level + r' (.+)$', re.M)
    matches = list(pattern.finditer(text))
    return [(m.group(1), text[m.end():matches[i+1].start() if i+1 < len(matches) else len(text)].strip())
            for i, m in enumerate(matches)]


def fields(text):
    result = {}
    for key, value in re.findall(r'^- ([A-Za-z][A-Za-z ]*): (.*)$', text, re.M):
        if key in result:
            raise ValueError('duplicate field: ' + key)
        result[key] = value.strip()
    return result


def table(text, header):
    """Read one exact pipe table; no escaped pipes or multiline cells."""
    lines = text.splitlines()
    wanted = '| ' + ' | '.join(header) + ' |'
    indices = [i for i, line in enumerate(lines) if line.strip() == wanted]
    if len(indices) != 1:
        raise ValueError('expected one table: ' + ', '.join(header))
    i = indices[0]
    if i + 1 >= len(lines) or not re.fullmatch(r'\|(?:\s*:?-+:?\s*\|){' + str(len(header)) + '}', lines[i+1].strip()):
        raise ValueError('invalid table separator')
    rows = []
    for line in lines[i+2:]:
        if not line.strip().startswith('|'):
            break
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) != len(header) or not all(meaningful(c) for c in cells):
            raise ValueError('invalid or empty table cells')
        rows.append(cells)
    if not rows:
        raise ValueError('empty table: ' + ', '.join(header))
    return rows


def target_path(value):
    path = value.strip('`')
    p = PurePosixPath(path)
    return bool(path) and not p.is_absolute() and not any(x in path for x in ['\\', ':']) and all(
        part not in {'..', '.', ''} for part in path.split('/')) and '.git' not in p.parts


def validate(text, kind='plan', expected=None):
    issues = []
    result = {'ok': False, 'issues': issues, 'kind': kind, 'semantic_verification': 'not_performed'}
    try:
        text = clean_markdown(text)
        if len(re.findall(r'^# [^#].+$', text, re.M)) != 1 or not text.startswith('# '):
            raise ValueError('expected one initial H1 title')
        blocks = sections(text, 2)
        names = [name for name, _ in blocks]
        if len(names) != len(set(names)):
            raise ValueError('duplicate level-two heading')
        content = dict(blocks)
        if kind == 'assessment':
            if names != ASSESSMENT_SECTIONS or not all(meaningful(v) for _, v in blocks):
                raise ValueError('assessment needs ordered nonempty sections: ' + ', '.join(ASSESSMENT_SECTIONS))
            info = fields(content['Identity and input'])
            for key in ['Activity', 'Input revision', 'Decision revision']:
                if not meaningful(info.get(key)):
                    issues.append('missing assessment field: ' + key)
            uuid.UUID(info.get('Activity', ''))
            checks = table(content['Readiness'], ['Check', 'Status', 'Evidence'])
            if [r[0] for r in checks] != TECHNICAL_CHECKS:
                issues.append('readiness must contain T1–T6 exactly in order')
            for _, status, evidence in checks:
                if status != 'passed':
                    issues.append('technical readiness not passed: ' + status)
            result['identity'] = info
        elif kind == 'plan':
            if names[:3] != ['Execution contract', 'Acceptance criteria', 'Plan overview']:
                raise ValueError('plan needs Execution contract, Acceptance criteria and Plan overview first')
            info = fields(content['Execution contract'])
            for key in PLAN_FIELDS:
                if not meaningful(info.get(key)):
                    issues.append('missing execution field: ' + key)
            uuid.UUID(info.get('Activity', ''))
            if info.get('Format') != 'hai-plan-v1': issues.append('unsupported plan format')
            if info.get('Mode') not in {'normal', 'accelerated'}: issues.append('invalid planning mode')
            if info.get('Readiness') != 'ready': issues.append('plan is not execution ready')
            if info.get('Business readiness') not in {'passed', 'exempt'}: issues.append('business readiness unavailable')
            criteria = table(content['Acceptance criteria'], ['ID', 'Criterion', 'Verification'])
            ids = [row[0] for row in criteria]
            if len(ids) != len(set(ids)) or not all(re.fullmatch(r'A[1-9]\d*', x) for x in ids):
                issues.append('invalid/duplicate acceptance IDs')
            overview = table(content['Plan overview'], ['Phase', 'Goal', 'Depends on', 'Expected result'])
            phase_blocks = [(n, body) for n, body in blocks if re.fullmatch(r'Phase [1-9]\d* — .+', n)]
            if not phase_blocks: issues.append('no phases')
            phase_names = [n for n, _ in phase_blocks]
            expected_names = ['Execution contract', 'Acceptance criteria', 'Plan overview'] + phase_names + ['File inventory']
            remaining = names[len(expected_names):]
            if names[:len(expected_names)] != expected_names or remaining not in [[], ['Risks'], ['References'], ['Risks', 'References']]:
                issues.append('unsupported or out-of-order plan sections')
            numbers = [n.split()[1] for n, _ in phase_blocks]
            if len(numbers) != len(set(numbers)): issues.append('duplicate phase numbers')
            if [re.match(r'\d+', r[0]).group() if re.match(r'\d+', r[0]) else '' for r in overview] != numbers:
                issues.append('overview does not match phase order')
            prior_phases = []
            for phase, _, dependencies, _ in overview:
                number = re.match(r'\d+', phase)
                if dependencies != 'None':
                    dependency_numbers = []
                    for dependency in dependencies.split(','):
                        match = re.fullmatch(r'\s*([1-9]\d*):\s*(\S.*)', dependency)
                        if not match or match.group(1) not in prior_phases:
                            issues.append('phase dependency must name an earlier phase and reason: '+phase)
                        elif match.group(1) in dependency_numbers:
                            issues.append('duplicate phase dependency: '+phase)
                        else:
                            dependency_numbers.append(match.group(1))
                if number: prior_phases.append(number.group())
            tasks, covered = [], set()
            for name, body in phase_blocks:
                local = sections(body, 3)
                if [n for n, _ in local] != PHASE_SECTIONS or not all(meaningful(v) for _, v in local):
                    raise ValueError('invalid phase sections: ' + name)
                actions = dict(local)['Actions']
                rows = table(actions, ['Step', 'Action', 'Purpose or expected result'])
                details = table(actions, ['Task', 'Target', 'Operation', 'Depends on', 'Acceptance', 'Check'])
                if [r[0] for r in rows] != [r[0] for r in details]: issues.append('task details differ from actions: ' + name)
                for task, target, operation, deps, accepts, check in details:
                    if not re.fullmatch(name.split()[1] + r'\.[1-9]\d*', task): issues.append('invalid task ID: ' + task)
                    if task in tasks: issues.append('duplicate task: ' + task)
                    if not target_path(target): issues.append('invalid workspace target: ' + target)
                    if deps != 'None' and any(d.strip() not in tasks for d in deps.split(',')):
                        issues.append('dependency must name earlier task: ' + task)
                    tasks.append(task)
                    refs = {a.strip() for a in accepts.split(',')}
                    if not refs <= set(ids): issues.append('unknown acceptance reference: ' + task)
                    covered |= refs
            if set(ids) - covered: issues.append('uncovered acceptance: ' + ', '.join(sorted(set(ids)-covered)))
            inventory = table(content.get('File inventory', ''), ['Path', 'Change', 'Purpose'])
            inventory_paths = [r[0].strip('`') for r in inventory]
            if len(inventory_paths) != len(set(inventory_paths)) or not all(target_path(p) for p in inventory_paths):
                issues.append('invalid/duplicate inventory paths')
            if any(r[1] not in {'Add', 'Edit', 'Move', 'Delete', 'Inspect'} for r in inventory):
                issues.append('invalid inventory operation')
            for _, body in phase_blocks:
                for row in table(dict(sections(body, 3))['Actions'], ['Task', 'Target', 'Operation', 'Depends on', 'Acceptance', 'Check']):
                    if row[1].strip('`') not in inventory_paths: issues.append('target missing from inventory: ' + row[1])
            result.update(identity=info, tasks=tasks, acceptance=ids)
        else:
            raise ValueError('unsupported document kind')
        if expected is not None:
            for key in ['Activity', 'Input revision', 'Decision revision']:
                if key not in expected or expected[key] != info.get(key): issues.append('stale/missing expected identity: ' + key)
    except (ValueError, KeyError, TypeError) as exc:
        issues.append(str(exc))
    result['ok'] = not issues
    return result


def load_json(path):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out: raise ValueError('duplicate JSON key: ' + key)
            out[key] = value
        return out
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda s: (_ for _ in ()).throw(ValueError('invalid JSON constant: '+s)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--document', required=True)
    parser.add_argument('--kind', choices=['assessment', 'plan'], default='plan')
    parser.add_argument('--expected', help='Optional current identity JSON; required by host execution preflight')
    args = parser.parse_args()
    try:
        document = safe_file(args.workspace, args.document)
        expected = load_json(safe_file(args.workspace, args.expected)) if args.expected else None
        if expected is not None and not isinstance(expected, dict): raise ValueError('expected identity must be an object')
        result = validate(document.read_bytes().decode('utf-8'), args.kind, expected)
        code = 0 if result['ok'] else 1
    except (OSError, ValueError, UnicodeError) as exc:
        result, code = {'ok': False, 'issues': [str(exc)]}, 2
    print(json.dumps(result, ensure_ascii=False))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
