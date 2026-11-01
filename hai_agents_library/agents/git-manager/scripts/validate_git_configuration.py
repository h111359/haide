"""Read-only Git extension settings validation; never probes Git or changes state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
# Reuse only generic containment and duplicate-free JSON utilities from the
# framework installed beside this extension, never core integration policy.
_INSTALLED_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_INSTALLED_ROOT / '.hai/tools/startup'))
from startup_check import safe_path, readable_file, overlaps
from agent_tools import Invalid, load_json

NAMES = ('git', 'github')


def validate_settings(state: dict) -> dict:
    if not isinstance(state, dict):
        raise Invalid('State envelope must be a JSON object')
    statuses = {name: {'enabled': False, 'status': 'unconfigured'} for name in NAMES}
    statuses['git']['auto_push'] = {'enabled': False, 'status': 'unconfigured', 'readiness': 'not_checked'}
    issues = []
    if 'integrations' not in state:
        return {'ok': True, 'integrations': statuses, 'issues': issues}
    container = state['integrations']
    if not isinstance(container, dict):
        for name in NAMES:
            statuses[name].update(enabled=False, status='invalid')
        statuses['git']['auto_push'].update(status='unverified')
        issues.append({'path': 'integrations', 'message': 'Expected object; Git and GitHub unavailable'})
        return {'ok': False, 'integrations': statuses, 'issues': issues}
    for name in NAMES:
        if name not in container:
            continue
        entry = container[name]
        valid = isinstance(entry, dict) and type(entry.get('enabled')) is bool
        if valid:
            statuses[name].update(enabled=entry['enabled'], status='enabled' if entry['enabled'] else 'disabled')
        else:
            statuses[name].update(enabled=False, status='invalid')
            issues.append({'path': f'integrations.{name}', 'message': 'Expected object with Boolean enabled; integration unavailable'})
        if name != 'git':
            continue
        policy = statuses['git']['auto_push']
        if isinstance(entry, dict) and 'auto_push' not in entry:
            continue
        push = entry.get('auto_push') if isinstance(entry, dict) else None
        if not isinstance(push, dict) or type(push.get('enabled')) is not bool:
            policy.update(enabled=False, status='invalid')
            issues.append({'path': 'integrations.git.auto_push', 'message': 'Expected object with Boolean enabled; push unavailable'})
        elif push['enabled'] and not (valid and entry['enabled']):
            policy.update(enabled=False, status='invalid')
            issues.append({'path': 'integrations.git.auto_push', 'message': 'Enabled Git required for automatic push'})
        else:
            policy.update(enabled=push['enabled'], status='enabled' if push['enabled'] else 'disabled')
    return {'ok': not issues, 'integrations': statuses, 'issues': issues}


def check(workspace: Path) -> dict:
    workspace = workspace.resolve(strict=True)
    if not workspace.is_dir():
        raise Invalid('Workspace must be an existing directory')
    path = safe_path(workspace, '.hai_env/state.json')
    for reserved in ('.hai', '.git', '.hai_env/agents', '.hai_env/model_profiles.json', '.hai_env/agent_instructions.md'):
        if overlaps(path, workspace / reserved):
            raise Invalid('State path aliases a reserved resource')
    readable_file(path)
    result = validate_settings(load_json(path))
    result['scope'] = 'saved_git_extension_configuration_only'
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = check(args.workspace)
    except (Invalid, OSError, UnicodeError, RuntimeError, ValueError) as exc:
        result = {'ok': False, 'scope': 'saved_git_extension_configuration_only',
                  'integrations': {name: {'enabled': False, 'status': 'unverified'} for name in NAMES},
                  'issues': [{'path': '.hai_env/state.json', 'message': str(exc)}]}
        result['integrations']['git']['auto_push'] = {'enabled': False, 'status': 'unverified', 'readiness': 'not_checked'}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
