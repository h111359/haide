"""Run core regression suites with all test working directories inside a workspace."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from runtime.storage import SafetyError, checked_path, read_json

SUITES = ('runtime/tests', 'startup', 'activities', 'chronicles', 'configuration', 'agents')


def test_work_path(root, relative):
    """Accept owned test areas under the configured store, including CI scaffolds."""
    work = checked_path(root, relative)
    state = read_json(checked_path(root, '.hai_env/config/state.json', allow_missing=False))
    try:
        location = state['activities']['location']
    except (KeyError, TypeError) as exc:
        raise SafetyError('Missing configured Activity location') from exc
    checked_path(root, location)
    store = location.split('/')
    parts = relative.split('/')
    tail = parts[len(store):]
    owned = (len(tail) >= 3 and tail[1:3] == ['files', 'test-work'])
    invocation = (len(tail) >= 5 and tail[1:3] == ['files', 'agent-invocations']
                  and tail[4] == 'test-work')
    if parts[:len(store)] != store or not (owned or invocation):
        raise SafetyError('work-dir must be inside an Activity files/test-work or files/agent-invocations/<id>/test-work directory under the configured store')
    return work


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', default='.')
    parser.add_argument('--work-dir', required=True, help='Canonical workspace-relative disposable fixture directory')
    parser.add_argument('--suite', action='append', choices=SUITES)
    args = parser.parse_args()
    root = Path(args.workspace).resolve(strict=True)
    try:
        work = test_work_path(root, args.work_dir)
    except SafetyError as exc:
        parser.error(str(exc))
    work.mkdir(parents=True, exist_ok=True)
    temporary = checked_path(root, args.work_dir + '/tmp')
    temporary.mkdir(exist_ok=True)
    env = dict(os.environ, TMP=str(temporary), TEMP=str(temporary), TMPDIR=str(temporary), PYTHONDONTWRITEBYTECODE='1')
    tools = Path(__file__).resolve().parent
    failed = False
    for suite in args.suite or SUITES:
        result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
                                 '-s', str(tools / suite), '-p', 'test_*.py'], cwd=work, env=env)
        print(json.dumps({'suite': suite, 'exit_code': result.returncode}), flush=True)
        failed |= result.returncode != 0
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
