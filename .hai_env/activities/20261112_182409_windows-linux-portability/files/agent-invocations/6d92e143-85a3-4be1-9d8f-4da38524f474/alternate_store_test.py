"""Use an isolated valid alternate-store workspace and test the runner."""
import json
from pathlib import Path
import shutil
import subprocess
import sys

here = Path(__file__).resolve().parent
root = here.parents[5]
fixture = here / 'alternate-store-fixture'
(fixture / '.hai/templates').mkdir(parents=True)
(fixture / '.hai_env/config').mkdir(parents=True)
shutil.copyfile(root / '.hai/templates/state.json', fixture / '.hai/templates/state.json')
(fixture / '.hai_env/config/agent_instructions.md').write_bytes(b'')
(fixture / '.hai_env/config/state.json').write_text(json.dumps({'state_format_version': 3, 'activities': {'location': 'records/activities'}, 'features': {'chronicles': {'enabled': False, 'record_every_prompts': 5}}}), encoding='utf-8')
request = fixture / 'request.json'
request.write_text(json.dumps({'initial_input': 'Fixture', 'provenance': {'source': 'independent QA', 'reason': 'alternate store test'}}), encoding='utf-8')
def cli(*args):
    process = subprocess.run([sys.executable, '-B', str(root / '.hai/tools/hai.py'), *args, '--workspace', str(fixture)], capture_output=True, text=True)
    print('CLI', args, 'exit', process.returncode, process.stdout, process.stderr)
    return json.loads(process.stdout)

startup = cli('startup')
assert startup['ok'], startup
created = cli('activity', 'create', '--request', str(request), '--apply')
assert created['ok'], created
assert created['result']['path'] == 'records/activities/00000000_000000_active'
work = 'records/activities/00000000_000000_active/files/test-work'
p = subprocess.run([sys.executable, '-B', str(root / '.hai/tools/run_tests.py'), '--workspace', str(fixture), '--work-dir', work, '--suite', 'chronicles'], capture_output=True, text=True)
print('RUNNER exit', p.returncode, p.stderr)
assert p.returncode == 2 and 'work-dir must be inside an Activity files/test-work directory' in p.stderr
assert not (fixture / work).exists()
print('PASS alternate store valid, Activity created, runner rejected expected test area without writes')
