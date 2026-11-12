"""Independent native safety probes, no live workspace state mutations."""
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

HOME = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(REPO / '.hai/tools'))
from runtime.storage import checked_path, SafetyError
from runtime.activities import rename_exclusive

root = HOME / ('safety-' + uuid.uuid4().hex)
root.mkdir()
results = []
for bad in ('../escape', '/absolute', 'C:/drive', 'folder\\native', 'a//b', './a',
            'NUL', 'con.txt', 'COM1.log', 'trail.', 'trail ', 'a:b', 'bad?name', 'bad*name'):
    try:
        checked_path(root, bad)
    except SafetyError as exc:
        results.append({'test': 'reject noncanonical', 'path': bad, 'status': 'passed', 'error': str(exc)})
    else:
        results.append({'test': 'reject noncanonical', 'path': bad, 'status': 'failed'})
source = root / 'source'
dest = root / 'destination'
source.mkdir(); dest.mkdir()
(source / 'source.txt').write_bytes(b'source')
(dest / 'destination.txt').write_bytes(b'destination')
try:
    rename_exclusive(source, dest)
except OSError:
    assert (source / 'source.txt').read_bytes() == b'source'
    assert (dest / 'destination.txt').read_bytes() == b'destination'
    results.append({'test': 'native no-overwrite rename collision', 'status': 'passed'})
else:
    results.append({'test': 'native no-overwrite rename collision', 'status': 'failed'})
outside = HOME / ('junction-target-' + uuid.uuid4().hex)
outside.mkdir()
(outside / 'sentinel.txt').write_bytes(b'untouched')
link = root / 'junction'
if os.name == 'nt':
    made = subprocess.run(['cmd.exe', '/c', 'mklink', '/J', str(link), str(outside)], capture_output=True, text=True)
    if made.returncode:
        results.append({'test': 'Windows junction rejection', 'status': 'skipped', 'reason': made.stderr})
    else:
        for relative in ('junction', 'junction/new-file.txt', 'junction/sentinel.txt'):
            try:
                checked_path(root, relative)
            except SafetyError as exc:
                results.append({'test': 'Windows junction rejection', 'path': relative, 'status': 'passed', 'error': str(exc)})
            else:
                results.append({'test': 'Windows junction rejection', 'path': relative, 'status': 'failed'})
        assert (outside / 'sentinel.txt').read_bytes() == b'untouched'
report = {'platform': sys.platform, 'python': sys.version, 'results': results}
(HOME / 'safety-results.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
assert all(x['status'] != 'failed' for x in results)
