"""Read-only developer preflight and delivery evidence checks; not authorization."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import stat
import uuid


def nonempty(value):
    if not isinstance(value, str): return False
    placeholders = {'todo', 'tbd', '...', '___', '<fill>', 'placeholder', 'template'}
    for line in value.splitlines():
        line = re.sub(r'^\s*(?:[-*+] |\d+[.)] )', '', line)
        line = re.sub(r'^\s*\[[ xX]\]\s*', '', line).strip(' `*_\t')
        if line and line.lower() not in placeholders and not re.fullmatch(r'<(?:fill|todo|tbd)[^>]*>', line, re.I):
            return True
    return False


def safe_file(root, value):
    root = Path(root).resolve(strict=True)
    path = Path(value)
    path = path if path.is_absolute() else root / path
    if '..' in path.parts or not path.is_relative_to(root): raise ValueError('input outside workspace or traversal')
    cursor = root
    for part in path.relative_to(root).parts:
        cursor /= part
        if cursor.is_symlink(): raise ValueError('linked input or ancestor: ' + str(cursor))
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1: raise ValueError('input must be regular and singly linked')
    if '.git' in path.relative_to(root).parts: raise ValueError('metadata is not an input')
    return path


def visible_markdown(text):
    """Ignore fenced examples; never treat their headings as current instructions."""
    lines, fence = [], None
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
        if match:
            token, rest = match.groups()
            if fence is None: fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not rest.strip(): fence = None
            lines.append('')
        elif fence is None:
            if re.search(r'<!--|</?[A-Za-z][\w:-]*(?:\s[^<>]*)?/?>', line):
                raise ValueError('HTML structure is unsupported in direct instructions')
            lines.append(line)
        else:
            lines.append('')
    if fence: raise ValueError('unclosed direct instruction fence')
    return '\n'.join(lines)


def read_json(path):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out: raise ValueError('duplicate JSON key: '+key)
            out[key] = value
        return out
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda s: (_ for _ in ()).throw(ValueError('invalid constant: '+s)))


def plan_peer(root):
    peer = safe_file(root, '.hai_env/agents/solution-architect/scripts/plan_contract.py')
    spec = importlib.util.spec_from_file_location('hai_installed_plan_contract', peer)
    module = importlib.util.module_from_spec(spec)
    # Read/compile avoids bytecode writes even if the embedding caller omitted -B.
    exec(compile(peer.read_bytes(), str(peer), 'exec'), module.__dict__)
    return module


def permitted_write(root, write, permissions):
    if not isinstance(write, dict) or write.get('operation') not in {'create', 'modify', 'delete', 'move'}:
        return False
    value = write.get('path')
    if not nonempty(value): return False
    path = Path(value)
    if '..' in path.parts: return False
    if not path.is_absolute(): path = root / path
    resolved = path.resolve()
    if resolved.is_file() and resolved.stat().st_nlink != 1:
        # Other hard-link names cannot be discovered safely; containment is unknown.
        return False
    if resolved.is_relative_to(root): return '.git' not in resolved.relative_to(root).parts
    for permission in permissions:
        if not isinstance(permission, dict): continue
        location = permission.get('location')
        if not nonempty(location) or not Path(location).is_absolute(): continue
        scope = Path(location).resolve()
        operations = permission.get('operations')
        if (isinstance(operations, list) and resolved.is_relative_to(scope) and write['operation'] in operations
                and permission.get('origin') == 'human'
                and all(nonempty(permission.get(k)) for k in ['text', 'source', 'purpose'])
                and permission.get('purpose') == write.get('purpose')):
            return True
    return False


def preflight(root, directive, context, peer=None):
    issues = []
    root = Path(root).resolve()
    try:
        if not isinstance(context, dict): raise ValueError('context must be an object')
        for key in ['activity_id', 'input_revision', 'decision_revision', 'directive_sha256']:
            if not nonempty(context.get(key)): issues.append('missing current context: '+key)
        uuid.UUID(context.get('activity_id', ''))
        if context.get('directive_sha256') != hashlib.sha256(directive.encode('utf-8')).hexdigest():
            issues.append('directive hash differs from current host assignment')
        authority = context.get('authority', {})
        if not isinstance(authority, dict) or authority.get('origin') != 'human' or not all(
                nonempty(authority.get(k)) for k in ['text', 'source']):
            issues.append('missing covering human authority evidence')
        readiness = context.get('business_readiness', {})
        if not isinstance(readiness, dict) or readiness.get('status') not in {'passed', 'exempt'} or not nonempty(readiness.get('evidence')):
            issues.append('business readiness not established')
        if context.get('unresolved_decisions') != []: issues.append('unresolved or missing decision state')
        if context.get('implementation_start_verified') is not True: issues.append('runtime implementation-start evidence missing')
        for field in ['conventions', 'owners']:
            values = context.get(field)
            if not isinstance(values, list):
                issues.append('missing dependency inventory: '+field);continue
            for dep in values:
                if not isinstance(dep, dict) or type(dep.get('required')) is not bool or not nonempty(dep.get('name')):
                    issues.append('invalid dependency: '+field);continue
                if dep['required'] and dep.get('status') != 'ready': issues.append('required dependency unavailable: '+dep['name'])
        for key in ['expected_tasks', 'acceptance_ids']:
            values = context.get(key)
            if not isinstance(values, list) or not values or not all(nonempty(v) for v in values) or len(values) != len(set(values)):
                issues.append('invalid completeness inventory: '+key)
        expected_checks = context.get('expected_checks')
        if not isinstance(expected_checks, list) or not expected_checks:
            issues.append('expected checks missing')
        else:
            covered, required_coverage = set(), set()
            check_ids = []
            for check in expected_checks:
                if (not isinstance(check, dict) or not nonempty(check.get('id')) or type(check.get('required')) is not bool
                        or not isinstance(check.get('acceptance'), list) or not all(nonempty(x) for x in check['acceptance'])):
                    issues.append('invalid expected check');continue
                check_ids.append(check['id']); covered.update(check['acceptance'])
                if check['required']: required_coverage.update(check['acceptance'])
            if len(check_ids) != len(set(check_ids)): issues.append('duplicate expected check IDs')
            if covered != set(context.get('acceptance_ids', [])): issues.append('acceptance coverage differs from current directive')
            if required_coverage != set(context.get('acceptance_ids', [])): issues.append('acceptance needs mandatory verification coverage')
        writes = context.get('writes')
        permissions = context.get('outside_permissions', [])
        if not isinstance(writes, list) or not isinstance(permissions, list):
            issues.append('invalid write/permission inventory')
        else:
            for write in writes:
                if not permitted_write(root, write, permissions): issues.append('write lacks workspace containment or covering permission: '+str(write))
        protected = context.get('protected_changes')
        if not isinstance(protected, list): issues.append('missing protected-change inspection')
        else:
            inferred = []
            for write in writes if isinstance(writes, list) else []:
                if not isinstance(write, dict) or not isinstance(write.get('path'), str): continue
                path = Path(write['path'])
                path = path if path.is_absolute() else root/path
                resolved = path.resolve()
                if resolved.is_relative_to(root):
                    relative = resolved.relative_to(root)
                    if relative.parts[:1] == ('.hai',) or relative.parts[:2] in {('hai_agents_library','agents'),('.hai_env','agents')}:
                        inferred.append(write['path'])
            if any(p not in protected for p in inferred): issues.append('protected write omitted from inspection inventory')
        if isinstance(protected, list) and protected:
            permission = context.get('maintenance_authority', {})
            if (not isinstance(permission, dict) or permission.get('origin') != 'human'
                    or not all(nonempty(permission.get(k)) for k in ['text', 'source'])
                    or not isinstance(permission.get('paths'), list)
                    or any(p not in permission['paths'] for p in protected)):
                issues.append('protected changes require covering human maintenance authority')
        mode = context.get('mode')
        if mode == 'plan':
            peer = peer or plan_peer(root)
            result = peer.validate(directive, 'plan', {
                'Activity': context.get('activity_id'), 'Input revision': context.get('input_revision'),
                'Decision revision': context.get('decision_revision')})
            issues.extend('plan: '+issue for issue in result['issues'])
            if result.get('ok') and (result['tasks'] != context.get('expected_tasks') or result['acceptance'] != context.get('acceptance_ids')):
                issues.append('host completeness inventory differs from plan')
        elif mode == 'direct':
            if context.get('direct_selected') is not True: issues.append('direct execution not explicitly selected')
            markdown = visible_markdown(directive)
            if not markdown.startswith('# ') or len(re.findall(r'^# [^#].*$', markdown, re.M)) != 1:
                issues.append('direct directive needs one initial H1 title')
            names = re.findall(r'^## (.+)$', markdown, re.M)
            required = ['Outcome', 'Scope', 'Constraints', 'Acceptance', 'Tasks', 'Verification', 'Documentation']
            if names != required: issues.append('direct directive needs ordered sections: '+', '.join(required))
            parts = re.split(r'^## .+$', markdown, flags=re.M)[1:]
            if not parts or not all(nonempty(p.strip()) for p in parts): issues.append('empty or template-only direct directive')
        else:
            issues.append('mode must be plan or direct')
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        issues.append(str(exc))
    return {'ok': not issues, 'issues': issues, 'semantic_verification': 'not_performed'}


def validate_evidence(evidence, context):
    issues = []
    try:
        if not isinstance(evidence, dict): raise ValueError('evidence must be an object')
        for key in ['activity_id', 'directive_sha256', 'input_revision', 'decision_revision']:
            if not nonempty(context.get(key)) or evidence.get(key) != context[key]: issues.append('stale evidence: '+key)
        if evidence.get('status') not in {'verified', 'blocked', 'partial'}: issues.append('invalid outcome status')
        if not isinstance(evidence.get('changes'), list): issues.append('changed-path evidence missing')
        for item in evidence.get('changes', []):
            if not isinstance(item, dict) or not all(nonempty(item.get(k)) for k in ['path', 'operation', 'baseline', 'result']):
                issues.append('incomplete changed-path evidence')
            elif not any(isinstance(w, dict) and w.get('path') == item['path'] and w.get('operation') == item['operation']
                         for w in context.get('writes', [])):
                issues.append('actual change outside validated write inventory: '+item['path'])
        for field in ['tasks', 'checks', 'owners']:
            if not isinstance(evidence.get(field), list): issues.append('missing evidence list: '+field)
        tasks = evidence.get('tasks', [])
        checks = evidence.get('checks', [])
        if not tasks or any(not isinstance(t, dict) or not all(nonempty(t.get(k)) for k in ['id', 'status', 'result']) for t in tasks):
            issues.append('task evidence missing/incomplete')
        task_ids = [t.get('id') for t in tasks if isinstance(t, dict)]
        if task_ids != context.get('expected_tasks'): issues.append('task evidence differs from assigned tasks')
        if not checks or any(not isinstance(c, dict) or type(c.get('required')) is not bool or not all(nonempty(c.get(k)) for k in ['id', 'status', 'result']) for c in checks):
            issues.append('check evidence missing/incomplete')
        expected = {c['id']: c for c in context.get('expected_checks', []) if isinstance(c, dict) and 'id' in c}
        actual = {c['id']: c for c in checks if isinstance(c, dict) and 'id' in c}
        if len(actual) != len(checks) or set(actual) != set(expected): issues.append('check evidence missing/duplicate/unexpected IDs')
        for cid, check in actual.items():
            if cid in expected and check.get('required') != expected[cid].get('required'): issues.append('required check downgraded: '+str(cid))
        owner_names = [o.get('name') for o in evidence.get('owners', []) if isinstance(o, dict)]
        expected_owners = [o['name'] for o in context.get('owners', []) if isinstance(o, dict) and o.get('required')]
        if len(owner_names) != len(set(owner_names)) or not set(expected_owners) <= set(owner_names): issues.append('required owner evidence omitted/duplicate')
        for owner in evidence.get('owners', []):
            if isinstance(owner, dict) and owner.get('name') in expected_owners and owner.get('required') is not True:
                issues.append('required owner downgraded')
        if any(c.get('status') not in {'passed', 'failed', 'skipped', 'unavailable'} for c in checks if isinstance(c, dict)):
            issues.append('unknown check status')
        if not all(nonempty(evidence.get(k)) for k in ['documentation', 'protection', 'history']):
            issues.append('documentation/protection/history evidence missing')
        if not isinstance(evidence.get('blockers'), list): issues.append('blocker state missing')
        if evidence.get('status') == 'verified':
            if evidence.get('blockers') != []: issues.append('verified outcome has blockers')
            if any(t.get('status') != 'completed' for t in tasks if isinstance(t, dict)): issues.append('unfinished required task')
            if any(c.get('required') and c.get('status') != 'passed' for c in checks if isinstance(c, dict)):
                issues.append('required verification not passed')
            passed_coverage = {a for cid, check in actual.items() if check.get('status') == 'passed' and check.get('required') is True
                               for a in expected.get(cid, {}).get('acceptance', [])}
            if passed_coverage != set(context.get('acceptance_ids', [])): issues.append('acceptance lacks passed mandatory evidence')
            for owner in evidence.get('owners', []):
                if not isinstance(owner, dict) or type(owner.get('required')) is not bool or not nonempty(owner.get('name')):
                    issues.append('invalid owner evidence')
                elif owner['required'] and (owner.get('status') != 'completed' or not nonempty(owner.get('evidence'))):
                    issues.append('required owner work not completed')
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        issues.append(str(exc))
    return {'ok': not issues, 'issues': issues, 'semantic_verification': 'not_performed'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--directive', required=True)
    parser.add_argument('--context', required=True)
    parser.add_argument('--evidence')
    args = parser.parse_args()
    try:
        directive = safe_file(args.workspace, args.directive).read_bytes().decode('utf-8')
        context = read_json(safe_file(args.workspace, args.context))
        result = preflight(args.workspace, directive, context)
        if args.evidence:
            other = validate_evidence(read_json(safe_file(args.workspace, args.evidence)), context)
            result['issues'].extend(other['issues']); result['ok'] = not result['issues']
        code = 0 if result['ok'] else 1
    except (OSError, UnicodeError, ValueError) as exc:
        result, code = {'ok': False, 'issues': [str(exc)]}, 2
    print(json.dumps(result, ensure_ascii=False))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
