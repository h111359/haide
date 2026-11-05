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


def context(workspace):
    workspace = Path(workspace).resolve(strict=True)
    result = check(workspace)
    if result['state_status'] == 'valid':
        activity = discover(workspace, result['activities']['location'])
    else:
        activity = {'status': 'unverified', 'store': None, 'activity_id': None,
                    'path': None, 'state': None, 'continuity': {}, 'issues': []}
    result['activity_context'] = activity
    result['issues'].extend(activity['issues'])
    result['ok'] = result['ok'] and activity['status'] in ('current', 'absent') and not activity['issues']
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
