"""Read-only Git-owned configuration validation; never probes Git or changes files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
# Resolve shared helpers beside this package, never from the target workspace.
_INSTALLED_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_INSTALLED_ROOT / '.hai/tools/configuration'))
from configuration_tools import ConfigurationError, configuration_path, load_contract, load_json

Invalid = ConfigurationError
CONTRACT_PATH = Path(__file__).resolve().parents[1] / 'configuration/contract.json'

NAMES = ('git', 'github')


def validate_settings(settings: dict) -> dict:
    if not isinstance(settings, dict):
        raise Invalid('Settings must be a JSON object')
    statuses = {name: {'enabled': False, 'status': 'unconfigured'} for name in NAMES}
    statuses['git']['auto_push'] = {'enabled': False, 'status': 'unconfigured', 'readiness': 'not_checked'}
    issues = []
    container = settings
    for name in NAMES:
        if name not in container:
            continue
        entry = container[name]
        valid = isinstance(entry, dict) and ('enabled' not in entry or type(entry['enabled']) is bool)
        if valid:
            if 'enabled' in entry:
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
        if isinstance(push, dict) and 'enabled' not in push:
            continue
        if not isinstance(push, dict) or type(push.get('enabled')) is not bool:
            policy.update(enabled=False, status='invalid')
            issues.append({'path': 'integrations.git.auto_push', 'message': 'Expected object with Boolean enabled; push unavailable'})
        elif push['enabled'] and not (valid and entry.get('enabled', False)):
            policy.update(enabled=False, status='invalid')
            issues.append({'path': 'integrations.git.auto_push', 'message': 'Enabled Git required for automatic push'})
        else:
            policy.update(enabled=push['enabled'], status='enabled' if push['enabled'] else 'disabled')
    return {'ok': not issues, 'integrations': statuses, 'issues': issues}


def check(workspace: Path) -> dict:
    workspace = workspace.resolve(strict=True)
    if not workspace.is_dir():
        raise Invalid('Workspace must be an existing directory')
    contract = load_contract(CONTRACT_PATH, 'git-manager')
    expected = {'git.enabled', 'git.auto_push.enabled', 'github.enabled'}
    if set(contract['settings']) != expected or any(item['default'] is not False for item in contract['settings'].values()):
        raise Invalid('Git contract must declare the three disabled-by-default Boolean switches')
    path = configuration_path(workspace, 'git-manager')
    settings = {}
    if path.exists():
        data = load_json(path)
        if (not isinstance(data, dict) or type(data.get('config_format_version')) is not int
                or data['config_format_version'] not in contract['supported_config_format_versions']
                or not isinstance(data.get('settings'), dict)):
            raise Invalid('Configuration requires a supported config_format_version and settings object')
        settings = data['settings']
    result = validate_settings(settings)
    result['configuration_status'] = ('configured' if path.exists() else 'defaulted') if result['ok'] else 'invalid'
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
                  'configuration_status': 'invalid',
                  'issues': [{'path': '.hai_env/config/agents/git-manager.json', 'message': str(exc)}]}
        result['integrations']['git']['auto_push'] = {'enabled': False, 'status': 'unverified', 'readiness': 'not_checked'}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
