"""Independent QA scenarios: invoke public CLI against isolated native fixtures."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid

REPO = Path(__file__).resolve().parents[6]
HOME = Path(__file__).resolve().parent
TEMP = HOME / 'tmp'
TEMP.mkdir(exist_ok=True)
tempfile.tempdir = str(TEMP)
for key in ('TMP', 'TEMP', 'TMPDIR'):
    os.environ[key] = str(TEMP)
PROV = {'source': 'Independent QA controlled fixture', 'reason': 'Verify approved Windows/Linux portability behavior'}
results = []


def scenario(rep):
    root = HOME / ('café ' + rep + ' ' + uuid.uuid4().hex[:8])
    root.mkdir()
    shutil.copytree(REPO / '.hai', root / '.hai')
    requests = root / 'requests'
    requests.mkdir()
    sid = str(uuid.uuid4())
    env = {**os.environ, 'CODEX_THREAD_ID': sid, 'CODEX_SESSION_ID': sid, 'PYTHONDONTWRITEBYTECODE': '1'}
    count = 0

    def cli(group, action='', request=None, apply=False, expect=True):
        nonlocal count
        count += 1
        args = [sys.executable, '-B', str(root / '.hai/tools/hai.py'), group]
        if action:
            args.append(action)
        args.extend(['--workspace', str(root)])
        if request is not None:
            p = requests / f'{count:03}.json'
            p.write_text(json.dumps(request, ensure_ascii=False), encoding='utf-8')
            args.extend(['--request', str(p)])
        if apply:
            args.append('--apply')
        process = subprocess.run(args, cwd=root, env=env, capture_output=True, text=True, encoding='utf-8')
        try:
            value = json.loads(process.stdout)
        except Exception:
            raise AssertionError((args, process.returncode, process.stdout, process.stderr))
        results.append({'representation': rep, 'step': count, 'operation': group + ' ' + action,
                        'exit': process.returncode, 'response': value})
        assert bool(value['ok']) == expect, (group, action, value)
        assert (process.returncode == 0) == expect, (group, action, process.returncode)
        for path in value.get('changed_files', []):
            assert '\\' not in path, ('noncanonical changed_files', path)
        return value

    cli('environment', 'initialize', {'provenance': PROV}, True)
    cli('environment', 'configure', {'changes': {'features.chronicles.enabled': True}, 'provenance': PROV}, True)
    startup = cli('startup')['result']['execution_context']
    assert startup['os_name'] == os.name and startup['sys_platform'] == sys.platform
    assert startup['workspace_path_format'] == 'posix-relative'
    created = cli('activity', 'create', {'initial_input': 'Independent Windows QA: café', 'provenance': PROV}, True)
    aid = created['result']['state']['activity_id']
    base = created['result']['path']
    assert '\\' not in base
    discovered = cli('activity', 'discover')['result']
    assert discovered['path'] == base
    for excerpt in discovered['continuity'].values():
        assert '\\' not in excerpt['path']
    assert cli('activity', 'show', {'activity_id': aid})['result']['path'] == base
    for n in (1, 2):
        cli('activity', 'record', {'activity_id': aid, 'steps': {'analysis': 'completed'},
            'artifacts': [{'name': 'decisions.md', 'text': f'Clarification café {n}\n', 'reason': 'Independent persisted revision'}],
            'log': f'Applied clarification {n}', 'provenance': PROV}, True)
        if n == 1:
            previous_artifact = (root / base / 'decisions.md').read_bytes()
    revisions = list((root / base / 'files/revisions/decisions').glob('*.md'))
    assert len(revisions) == 1 and revisions[0].read_bytes() == previous_artifact
    cli('activity', 'chat-post', {'activity_id': aid, 'author': 'quality-assurance', 'text': 'QA café', 'provenance': PROV}, True)
    assert cli('activity', 'chat-read', {'activity_id': aid})['result']['messages'][0]['text'] == 'QA café'
    cli('activity', 'usage-update', {'activity_id': aid, 'provenance': PROV}, True)
    cli('activity', 'usage-read', {'activity_id': aid})
    allocation = cli('activity', 'invocation-allocate', {'activity_id': aid, 'agent': 'quality-assurance', 'provenance': PROV}, True)
    assert allocation['result']['allocated']
    sources = root / 'codex/sessions/2026/11/12'
    sources.mkdir(parents=True)
    source = sources / ('rollout-fixture-' + sid + '.jsonl')
    env['CODEX_HOME'] = str(root / 'codex')
    def rec(kind, payload):
        return {'timestamp': '2026-11-12T08:00:00Z', 'type': kind, 'payload': payload}
    records = [rec('session_meta', {'id': sid, 'timestamp': '2026-11-12T08:00:00Z', 'cwd': str(root)})]
    if rep == 'event_msg':
        records += [rec(rep, {'type': 'user_message', 'message': 'Actual QA work prompt'}),
                    rec(rep, {'type': 'agent_message', 'message': 'Actual completed QA outcome', 'phase': 'final_answer'})]
    else:
        records += [rec(rep, {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'Actual QA work prompt'}]}),
                    rec(rep, {'type': 'message', 'role': 'assistant', 'phase': 'final_answer', 'content': [{'type': 'output_text', 'text': 'Actual completed QA outcome'}]})]
    source.write_text(''.join(json.dumps(x) + '\n' for x in records), encoding='utf-8')
    if rep == 'response_item':
        cli('recording', 'discover', {}, expect=False)
    discovery = cli('recording', 'discover', {'representation': rep})
    assert discovery['result']['latest_user_occurrence']['source_position'] == 1
    cli('recording', 'bind', {'activity_id': aid, 'representation': rep, 'start_position': 1,
        'enabled_intervals': [{'start': {'source_session_id': sid, 'source_position': 1}, 'end': None, 'provenance': 'Enabled before controlled QA prompt'}], 'provenance': PROV}, True)
    cli('recording', 'synchronize', {'activity_id': aid, 'provenance': PROV}, True)
    cli('recording', 'verify', {'activity_id': aid})
    package = root / 'sources/quality-assurance'
    shutil.copytree(REPO / '.hai_env/agents/quality-assurance', package)
    installed = cli('packages', 'install', {'source': 'sources/quality-assurance', 'name': 'quality-assurance', 'provenance': PROV}, True)
    assert installed['result']['destination'] == '.hai_env/agents/quality-assurance'
    for diff in installed['result']['differences']:
        assert '\\' not in diff
    cli('packages', 'install', {'source': 'sources/quality-assurance', 'name': 'quality-assurance', 'provenance': PROV}, True, expect=False)
    for bad in ('../outside', 'C:/outside', 'sources\\quality-assurance', '.git/../sources/quality-assurance'):
        cli('packages', 'install', {'source': bad, 'name': 'quality-assurance', 'provenance': PROV}, expect=False)
    closed = cli('activity', 'close', {'activity_id': aid, 'outcome': 'completed', 'archive_label': 'qa-native',
        'outcome_text': 'Controlled QA fixture complete', 'recording': {'status': 'pending', 'details': 'Core must freshly verify'}, 'provenance': PROV}, True)
    archive = closed['result']['archive_path']
    assert '\\' not in archive and not (root / base).exists()
    cli('activity', 'supplement', {'activity_id': aid, 'text': 'Archived supplement café', 'provenance': PROV}, True)
    cli('activity', 'chat-read', {'activity_id': aid})
    cli('activity', 'usage-read', {'activity_id': aid})
    cli('recording', 'verify', {'activity_id': aid})
    assert 'Archived supplement café' in (root / archive / 'log.md').read_text(encoding='utf-8')
    fresh = cli('activity', 'create', {'initial_input': '', 'provenance': PROV}, True)
    assert fresh['result']['state']['activity_id'] != aid
    assert cli('activity', 'chat-read', {'activity_id': fresh['result']['state']['activity_id']})['result']['messages'] == []
    return {'representation': rep, 'root': str(root), 'steps': count, 'status': 'passed'}


if __name__ == '__main__':
    summary = []
    try:
        for representation in ('event_msg', 'response_item'):
            summary.append(scenario(representation))
    except Exception as error:
        summary.append({'status': 'failed', 'error': repr(error)})
        raise
    finally:
        hashes = {p.relative_to(REPO).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in (REPO / '.hai/tools').rglob('*.py')}
        (HOME / 'cli-results.json').write_text(json.dumps({'platform': sys.platform, 'python': sys.version, 'summary': summary, 'reviewed_hashes': hashes, 'results': results}, indent=2), encoding='utf-8')
        print(json.dumps(summary, indent=2))
