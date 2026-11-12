"""Independent, read-only runner and source path boundary checks."""
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(root / '.hai/tools'))
from path_contract import source_path_string, native_source_path, relative_parts

cases = 0
def check(label, condition):
    global cases
    cases += 1
    print(('PASS' if condition else 'FAIL') + ' ' + label, flush=True)
    if not condition:
        raise AssertionError(label)

foreign = '/home/person/archive/source.jsonl' if os.name == 'nt' else r'C:\Users\person\archive\source.jsonl'
check('foreign path retained exactly', source_path_string(root, foreign) == foreign)
try:
    native_source_path(foreign)
except ValueError as exc:
    check('foreign read fails with platform diagnostic', 'another operating system' in str(exc))
else:
    check('foreign read rejected', False)
for value in ('a/COM0.txt', 'a/LPT0.txt', 'a/COM10.txt', 'a/ordinary.txt'):
    check('valid name ' + value, relative_parts(value) == value.split('/'))
for value in ('a/COM9.txt', 'a/LPT3.txt', 'a/AUX .txt', 'a/CONIN$.txt', 'a/C:stream'):
    try:
        relative_parts(value)
    except ValueError:
        check('invalid name ' + value, True)
    else:
        check('invalid name ' + value, False)

work = '.hai_env/activities/00000000_000000_active/files/agent-invocations/6d92e143-85a3-4be1-9d8f-4da38524f474/test-work'
run = subprocess.run([sys.executable, '-B', str(root / '.hai/tools/run_tests.py'), '--workspace', str(root), '--work-dir', work, '--suite', 'chronicles'], capture_output=True, text=True)
check('runner rejects invocation test folder (observed bug)', run.returncode == 2 and 'work-dir must be inside an Activity files/test-work directory' in run.stderr)
check('rejected runner did not create fixture folder', not (root / work).exists())
print('TOTAL', cases)
