"""Collect independent, read-only startup and current Activity context."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'activities'))
from startup_check import (Invalid, check, safe_path, load_agent_contract,
                           read_configuration, ConfigurationError)
from discovery import discover


def leader_configuration(workspace, agents, catalogue_status):
    result = {'status': 'unavailable', 'path': '.hai_env/config/agents/leader.json',
              'settings': {}, 'configured_fields': [], 'issues': []}
    entry = next((a for a in agents if a.get('name') == 'leader' and a.get('origin') == '.hai'), None)
    if entry is None:
        if catalogue_status not in ('valid', 'partial'):
            result['status'] = 'unverified'
        return result
    relative = '.hai/agents/leader/configuration/contract.json'
    try:
        definition = safe_path(workspace, entry['definition'])
        contract_path = safe_path(workspace, relative)
        if not contract_path.is_relative_to(definition.parent):
            raise Invalid('Leader contract resolves outside its registered package')
        contract = load_agent_contract(contract_path, 'leader')
        return read_configuration(workspace, 'leader', contract)
    except (Invalid, ConfigurationError, OSError, UnicodeError, RuntimeError) as exc:
        result['status'] = 'invalid'
        result['issues'].append({'code': 'agent_configuration', 'path': relative,
                                 'agent': 'leader', 'message': str(exc)})
        return result


def context(workspace):
    workspace = Path(workspace).resolve(strict=True)
    result = check(workspace)
    leader = leader_configuration(workspace, result['agents'], result['catalogues']['framework'])
    result['leader_configuration'] = leader
    result['issues'].extend(leader['issues'])
    if result['state_status'] == 'valid':
        activity = discover(workspace, result['activities']['location'])
    else:
        activity = {'status': 'unverified', 'store': None, 'activity_id': None,
                    'path': None, 'state': None, 'continuity': {}, 'issues': []}
    result['activity_context'] = activity
    result['issues'].extend(activity['issues'])
    result['ok'] = result['ok'] and leader['status'] in ('configured', 'defaulted') and activity['status'] in ('current', 'absent') and not activity['issues']
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        result = context(args.workspace)
        code = 0 if result['ok'] else 1
    except (Invalid, OSError, RuntimeError) as exc:
        result = {'ok': False, 'issues': [{'code': 'input', 'message': str(exc)}]}
        code = 2
    print(json.dumps(result, ensure_ascii=True, separators=(',', ':')))
    return code


if __name__ == '__main__':
    sys.exit(main())
