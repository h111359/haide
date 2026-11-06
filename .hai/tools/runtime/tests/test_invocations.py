"""Invocation allocation fixtures; real-host handoff needs separate evidence."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
import uuid
from unittest import mock

TOOLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(TOOLS))
from runtime import activities, invocations
from runtime.storage import SafetyError


class InvocationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='hai-invocation-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / '.hai_env/activities').mkdir(parents=True)
        (self.root / '.hai/templates').mkdir(parents=True)
        shutil.copy(TOOLS.parent / 'templates/state.json', self.root / '.hai/templates/state.json')
        (self.root / '.hai_env/agent_instructions.md').write_text('')
        (self.root / '.hai_env/state.json').write_text(json.dumps({
            'state_format_version': 3, 'activities': {'location': '.hai_env/activities'},
            'features': {'chronicles': {'enabled': False, 'record_every_prompts': 5}}}))
        self.prov = {'source': 'fixture host', 'reason': 'allocate before dispatch'}
        created = activities.handle('create', self.root, {'initial_input': 'fixture', 'provenance': self.prov}, True)
        self.assertTrue(created['ok'], created)
        self.ident = created['result']['state']['activity_id']
        self.base = self.root / created['result']['path']

    def allocate(self, apply=True, **extra):
        return activities.handle('invocation-allocate', self.root, {
            'activity_id': self.ident, 'agent': 'quality-assurance',
            'provenance': self.prov, **extra}, apply)

    def close(self):
        return activities.handle('close', self.root, {
            'activity_id': self.ident, 'outcome': 'completed', 'archive_label': 'invocation-test',
            'outcome_text': 'Fixture has no live workers',
            'recording': {'status': 'disabled', 'details': 'Fixture recording off'},
            'provenance': self.prov}, True)

    def test_preview_creates_nothing_and_is_not_allocation(self):
        r = self.allocate(apply=False)
        self.assertEqual(r['status'], 'planned')
        self.assertFalse(r['result']['allocated'])
        self.assertEqual(r['changed_files'], [])
        self.assertFalse((self.base / 'files').exists())

    def test_repeated_same_agent_has_distinct_attributed_directories(self):
        state = (self.root / '.hai_env/state.json').read_bytes()
        first = self.allocate(); second = self.allocate()
        self.assertTrue(first['ok'] and second['ok'])
        a, b = first['result'], second['result']
        self.assertNotEqual(a['path'], b['path'])
        self.assertNotEqual(a['invocation_id'], b['invocation_id'])
        for allocation in (a, b):
            self.assertTrue(allocation['allocated'])
            path = self.root / allocation['path']
            self.assertTrue(path.is_dir())
            self.assertEqual(json.loads((self.root / allocation['metadata_path']).read_text()), allocation['metadata'])
            self.assertEqual(path, self.base / allocation['activity_relative_path'])
            self.assertEqual(allocation['metadata']['activity_id'], self.ident)
            self.assertEqual(allocation['metadata']['agent'], 'quality-assurance')
            self.assertEqual(allocation['metadata']['provenance'], self.prov)
            (path / 'sentinel.txt').write_text(allocation['invocation_id'])
        self.assertEqual((self.root / a['path'] / 'sentinel.txt').read_text(), a['invocation_id'])
        self.assertEqual((self.root / '.hai_env/state.json').read_bytes(), state)

    def test_no_destination_or_caller_identity_override(self):
        for kw in [{'agent': '../agent'}, {'agent': ''}, {'agent': 'A' * 65},
                   {'path': 'elsewhere'}, {'invocation_id': str(uuid.uuid4())},
                   {'provenance': {'source': 'fixture'}}]:
            self.assertFalse(self.allocate(**kw)['ok'])
            self.assertFalse((self.base / 'files').exists())

    def test_collision_preserves_existing_folder_without_retry(self):
        first = self.allocate()['result']
        marker = self.root / first['path'] / 'keep.txt'
        marker.write_text('earlier work')
        with mock.patch.object(invocations.uuid, 'uuid4', return_value=uuid.UUID(first['invocation_id'])):
            collision = self.allocate()
        self.assertEqual(collision['status'], 'blocked', collision)
        self.assertEqual(collision['changed_files'], [])
        self.assertEqual(len(list(marker.parent.parent.iterdir())), 1)
        self.assertEqual(marker.read_text(), 'earlier work')

    def test_files_parent_must_be_a_directory(self):
        (self.base / 'files').write_text('unrelated material')
        r = self.allocate()
        self.assertFalse(r['ok'])
        self.assertEqual(r['changed_files'], [])
        self.assertEqual((self.base / 'files').read_text(), 'unrelated material')

    def test_linked_parent_is_rejected(self):
        outside = self.root / 'outside'
        outside.mkdir()
        try:
            (self.base / 'files').symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable')
        self.assertFalse(self.allocate()['ok'])
        self.assertEqual(list(outside.iterdir()), [])

    def test_partial_metadata_failure_reports_and_preserves_directory(self):
        with mock.patch.object(invocations, 'write_json', side_effect=OSError('injected metadata failure')):
            r = self.allocate()
        self.assertEqual(r['status'], 'partial', r)
        created = self.base / 'files/agent-invocations'
        folders = list(created.iterdir())
        self.assertEqual(len(folders), 1)
        self.assertIn(str(folders[0].relative_to(self.root)), r['changed_files'])
        self.assertTrue(folders[0].is_dir())
        self.assertFalse((folders[0] / 'invocation.json').exists())
        self.assertNotIn('allocated', r['result'])

    def test_partial_file_creation_is_included_in_report(self):
        def fail(root, relative, value):
            (root / relative).write_text('{partial')
            raise SafetyError('injected partial file', [relative])
        with mock.patch.object(invocations, 'write_json', side_effect=fail):
            r = self.allocate()
        self.assertEqual(r['status'], 'partial', r)
        manifests = list((self.base / 'files/agent-invocations').glob('*/invocation.json'))
        self.assertEqual(len(manifests), 1)
        self.assertIn(str(manifests[0].relative_to(self.root)), r['changed_files'])
        self.assertEqual(manifests[0].read_text(), '{partial')

    def test_readback_failure_is_not_reported_as_success(self):
        with mock.patch.object(invocations, 'read_json', return_value={}):
            r = self.allocate()
        self.assertEqual(r['status'], 'partial')
        self.assertTrue(list((self.base / 'files/agent-invocations').glob('*/invocation.json')))

    def test_changed_activity_is_detected_and_created_material_retained(self):
        real_write = invocations.write_json
        def change(root, relative, value):
            real_write(root, relative, value)
            state_path = self.base / 'state.json'
            state = json.loads(state_path.read_text())
            state['external_change'] = True
            state_path.write_text(json.dumps(state))
        with mock.patch.object(invocations, 'write_json', side_effect=change):
            r = self.allocate()
        self.assertEqual(r['status'], 'partial', r)
        self.assertIn('Activity changed', r['issues'][0])
        self.assertTrue(list((self.base / 'files/agent-invocations').glob('*/invocation.json')))

    def test_allocation_serializes_competitors_and_closure(self):
        started, release = threading.Event(), threading.Event()
        real_allocate = invocations.allocate
        def held(*args):
            started.set()
            if not release.wait(5):
                raise RuntimeError('Fixture timed out')
            return real_allocate(*args)
        with ThreadPoolExecutor(max_workers=1) as pool:
            with mock.patch.object(invocations, 'allocate', side_effect=held):
                future = pool.submit(self.allocate)
                try:
                    self.assertTrue(started.wait(5))
                    self.assertEqual(self.allocate()['status'], 'blocked')
                    self.assertEqual(self.close()['status'], 'blocked')
                    self.assertEqual(json.loads((self.base / 'state.json').read_text())['lifecycle'], 'active')
                finally:
                    release.set()
                first = future.result()
                self.assertTrue(first['ok'], first)
        second = self.allocate()
        self.assertTrue(second['ok'])
        self.assertNotEqual(first['result']['path'], second['result']['path'])

    def test_archive_preserves_files_and_new_activity_has_new_identity(self):
        a = self.allocate()['result']
        folder = self.root / a['path']
        (folder / 'notes.md').write_text('retained work')
        manifest = (folder / 'invocation.json').read_bytes()
        closed = self.close()
        self.assertTrue(closed['ok'], closed)
        archived = self.root / closed['result']['archive_path'] / a['activity_relative_path']
        self.assertEqual((archived / 'invocation.json').read_bytes(), manifest)
        self.assertEqual((archived / 'notes.md').read_text(), 'retained work')
        self.assertFalse(self.allocate()['ok'])
        new = activities.handle('create', self.root, {'initial_input': '', 'provenance': self.prov}, True)
        old_id = self.ident
        self.ident = new['result']['state']['activity_id']
        b = self.allocate()['result']
        self.assertNotEqual(a['invocation_id'], b['invocation_id'])
        self.assertEqual(b['metadata']['activity_id'], self.ident)
        self.assertFalse(activities.handle('invocation-allocate', self.root, {
            'activity_id': old_id, 'agent': 'quality-assurance', 'provenance': self.prov}, True)['ok'])
        self.assertEqual((archived / 'notes.md').read_text(), 'retained work')

    def test_custom_store_and_missing_mandatory_instructions(self):
        target = self.root / 'project/activities'
        target.parent.mkdir()
        (self.root / '.hai_env/activities').rename(target)
        state_path = self.root / '.hai_env/state.json'
        state = json.loads(state_path.read_text()); state['activities']['location'] = 'project/activities'
        state_path.write_text(json.dumps(state))
        r = self.allocate()
        self.assertTrue(r['ok'], r)
        self.assertTrue(r['result']['path'].startswith('project/activities/'))
        (self.root / '.hai_env/agent_instructions.md').unlink()
        self.assertFalse(self.allocate()['ok'])

    def test_cli_preview_and_applied_result(self):
        request = self.root / 'request.json'
        request.write_text(json.dumps({'activity_id': self.ident, 'agent': 'quality-assurance', 'provenance': self.prov}))
        args = [sys.executable, '-B', str(TOOLS / 'hai.py'), 'activity', 'invocation-allocate',
                '--workspace', str(self.root), '--request', str(request)]
        preview = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(preview.returncode, 0, preview.stdout)
        self.assertFalse(json.loads(preview.stdout)['result']['allocated'])
        self.assertFalse((self.base / 'files').exists())
        applied = subprocess.run(args + ['--apply'], capture_output=True, text=True)
        self.assertEqual(applied.returncode, 0, applied.stdout)
        result = json.loads(applied.stdout)['result']
        self.assertTrue(result['allocated'])
        self.assertTrue((self.root / result['path']).is_dir())


if __name__ == '__main__':
    unittest.main()
