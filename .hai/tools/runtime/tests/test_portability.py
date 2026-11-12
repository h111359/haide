"""Native CLI and filesystem regressions for Windows/Linux runtime contracts."""
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

TOOLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(TOOLS))
from path_contract import relative_parts, is_link_or_reparse, source_path_string, native_source_path
from runtime import storage, activities, chronicles, recording, usage
from startup_check import safe_path
from configuration_tools import _safe_path
import migrate_specification_configuration as specification_migration


class PortabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='hai-portability-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / 'workspace café with spaces'
        (self.root / '.hai/templates').mkdir(parents=True)
        shutil.copy(TOOLS.parent / 'templates/state.json', self.root / '.hai/templates/state.json')
        (self.root / '.hai_env/config').mkdir(parents=True)
        (self.root / '.hai_env/config/agent_instructions.md').write_bytes(b'')
        self.config = {'state_format_version': 3, 'activities': {'location': '.hai_env/activities'},
                       'features': {'chronicles': {'enabled': True, 'record_every_prompts': 5}}}
        (self.root / '.hai_env/config/state.json').write_text(json.dumps(self.config), encoding='utf-8')
        self.prov = {'source': 'portable CLI fixture', 'reason': 'exercise native behavior'}
        self.env = dict(os.environ)
        for name in ('CODEX_THREAD_ID', 'CODEX_SESSION_ID', 'CODEX_HOME'):
            self.env.pop(name, None)

    def cli(self, group, op='', request=None, apply=False):
        args = [sys.executable, '-B', str(TOOLS / 'hai.py'), group]
        if op:
            args.append(op)
        args += ['--workspace', str(self.root)]
        if request is not None:
            path = self.root / 'request.json'
            path.write_text(json.dumps(request), encoding='utf-8')
            args += ['--request', str(path)]
        if apply:
            args.append('--apply')
        result = subprocess.run(args, env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertTrue(result.stdout, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0 if data['ok'] else 1 if data['status'] not in ('invalid', 'input_error') else 2, data)
        return data

    def good(self, *args, **kwargs):
        data = self.cli(*args, **kwargs)
        self.assertTrue(data['ok'], data)
        for path in data['changed_files']:
            relative_parts(path.rstrip('/'))
        return data['result']

    def create(self):
        result = self.good('activity', 'create', {'initial_input': '', 'provenance': self.prov}, True)
        return result['state']['activity_id'], result['path']

    def test_cli_lifecycle_recording_both_representations(self):
        for representation in ('event_msg', 'response_item'):
            with self.subTest(representation=representation):
                ident, base = self.create()
                self.assertEqual(self.good('activity', 'discover')['path'], base)
                self.assertEqual(self.good('activity', 'show', {'activity_id': ident})['path'], base)
                for text in ('First café\nexact text', 'Updated café\nexact text'):
                    self.good('activity', 'record', {'activity_id': ident, 'steps': {'analysis': 'completed'},
                              'artifacts': [{'name': 'decisions.md', 'text': text, 'reason': 'clarification'}],
                              'log': 'persisted clarification', 'provenance': self.prov}, True)
                revisions = list((self.root / base / 'files/revisions/decisions').iterdir())
                self.assertEqual(len(revisions), 1)
                self.assertIn('First café\nexact text', revisions[0].read_text(encoding='utf-8'))
                self.good('activity', 'chat-post', {'activity_id': ident, 'author': 'quality-assurance',
                          'text': 'café\nline two', 'provenance': self.prov}, True)
                chat = (self.root / base / 'chat.jsonl').read_bytes()
                self.assertNotIn(b'\r\n', chat)
                self.good('activity', 'chat-read', {'activity_id': ident})
                sid = 'ae9f1b34-0a77-4eae-bdbf-00d035c57d4b' if representation == 'event_msg' else 'ae9f1b34-0a77-4eae-bdbf-00d035c57d4c'
                source = self.root / (representation + '.jsonl')
                def record(kind, payload):
                    return {'timestamp': '2026-11-09T00:00:00Z', 'type': kind, 'payload': payload}
                records = [record('session_meta', {'id': sid, 'timestamp': '2026-11-09T00:00:00Z', 'cwd': str(self.root)})]
                if representation == 'event_msg':
                    records += [record('event_msg', {'type': 'user_message', 'message': 'Exact café prompt'}),
                                record('event_msg', {'type': 'agent_message', 'message': 'Exact outcome', 'phase': 'final_answer'})]
                else:
                    records += [record('response_item', {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'Exact café prompt'}]}),
                                record('response_item', {'type': 'message', 'role': 'assistant', 'phase': 'final_answer', 'content': [{'type': 'output_text', 'text': 'Exact outcome'}]})]
                source.write_bytes(('\r\n'.join(json.dumps(r) for r in records) + '\r\n').encode('utf-8'))
                bind = {'activity_id': ident, 'session_id': sid, 'source_path': str(source), 'representation': representation,
                        'start_position': 1, 'enabled_intervals': [{'start': {'source_session_id': sid, 'source_position': 1}, 'end': None, 'provenance': 'enabled before work'}], 'provenance': self.prov}
                self.good('recording', 'discover', {k: bind[k] for k in ('session_id', 'source_path', 'representation')})
                self.good('recording', 'bind', bind, True)
                segments = list((self.root / base / 'chronicles').glob('*segment*.md'))
                self.assertEqual(segments[0].name, '20261109_000000_segment-01.md')
                self.good('recording', 'synchronize', {'activity_id': ident, 'provenance': self.prov}, True)
                self.good('recording', 'verify', {'activity_id': ident})
                closed = self.good('activity', 'close', {'activity_id': ident, 'outcome': 'completed', 'archive_label': 'portable',
                                   'outcome_text': 'verified fixture', 'recording': {'status': 'pending', 'details': 'runtime verifies'}, 'provenance': self.prov}, True)
                self.good('recording', 'verify', {'activity_id': ident})
                self.good('activity', 'supplement', {'activity_id': ident, 'text': 'archive verified', 'provenance': self.prov}, True)
                self.assertFalse((self.root / base).exists())
                self.assertTrue((self.root / closed['archive_path'] / 'outcome.md').exists())
        context = self.good('startup')['execution_context']
        self.assertEqual(context['sys_platform'], sys.platform)
        self.assertEqual(context['workspace_path_format'], 'posix-relative')

    def test_all_workspace_validators_reject_nonportable_strings(self):
        for value in ('../escape', '/absolute', 'C:/drive', 'C:drive', 'a\\b', 'a//b', 'a/./b', 'a/../b',
                      'a/CON.txt', 'a/CON .txt', 'a/CONIN$', 'a/CONOUT$.txt', 'a/com¹.log', 'a/trailing.', 'a/space ', 'a/stream:name',
                      'a/*', 'a/?', 'a/<bad>', 'a/"bad"', 'a/pipe|', 'a/\x00bad', 'a/\nbad'):
            for validator in (relative_parts, lambda p: storage.checked_path(self.root, p),
                              lambda p: safe_path(self.root, p), lambda p: _safe_path(self.root, p)):
                with self.subTest(value=value, validator=validator), self.assertRaises((ValueError, storage.SafetyError)):
                    validator(value)

    def test_reparse_attribute_detection_does_not_require_path_is_junction(self):
        self.assertTrue(is_link_or_reparse(SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0x400)))
        self.assertFalse(is_link_or_reparse(SimpleNamespace(st_mode=stat.S_IFDIR)))

    def test_foreign_source_metadata_is_preserved_but_never_opened(self):
        foreign = '/home/example/session.jsonl' if os.name == 'nt' else 'C:\\Users\\example\\session.jsonl'
        self.assertEqual(source_path_string(self.root, foreign), foreign)
        with self.assertRaisesRegex(ValueError, 'another operating system'):
            native_source_path(foreign)

    def test_specification_migration_rejects_reparse_ancestor(self):
        directory = self.root / 'junction'
        directory.mkdir()
        original = Path.lstat
        def lstat(path, *args, **kwargs):
            if path == directory:
                return SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0x400)
            return original(path, *args, **kwargs)
        with mock.patch.object(Path, 'lstat', autospec=True, side_effect=lstat):
            with self.assertRaisesRegex(ValueError, 'reparse'):
                specification_migration._ensure_unaliased(self.root, 'junction/file', kind='file')

    def test_native_path_serialization_has_portable_contract(self):
        for cls in (PureWindowsPath, PurePosixPath):
            self.assertEqual(cls('.hai_env/activities/current').as_posix(), '.hai_env/activities/current')

    def test_rename_collision_preserves_both_directories(self):
        source, dest = self.root / 'source', self.root / 'dest'
        source.mkdir(); dest.mkdir()
        (source / 'marker').write_bytes(b'source'); (dest / 'marker').write_bytes(b'dest')
        with self.assertRaises(OSError):
            activities.rename_exclusive(source, dest)
        self.assertEqual((source / 'marker').read_bytes(), b'source')
        self.assertEqual((dest / 'marker').read_bytes(), b'dest')

    def test_write_failure_reports_canonical_candidate(self):
        target = self.root / 'file.json'; target.write_bytes(b'original')
        with mock.patch.object(storage.os, 'replace', side_effect=OSError('injected replace failure')):
            with self.assertRaises(storage.SafetyError) as caught:
                storage.write_bytes(self.root, 'file.json', b'new', storage.fingerprint(target))
        self.assertTrue(caught.exception.changed_files)
        for relative in caught.exception.changed_files:
            relative_parts(relative)
        self.assertEqual(target.read_bytes(), b'original')


if __name__ == '__main__':
    unittest.main()
