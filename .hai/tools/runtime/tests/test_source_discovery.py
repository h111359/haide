"""Current-session discovery, early binding and real runtime lifecycle fixtures."""
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runtime import source_discovery as sources, recording, activities, startup

SID = 'ae9f1b34-0a77-4eae-bdbf-00d035c57d4b'
OTHER = 'ae9f1b34-0a77-4eae-bdbf-00d035c57d4c'


class SourceDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / 'codex'
        self.source = self.home / 'sessions/2026/11/09' / ('rollout-fixture-' + SID + '.jsonl')
        self.source.parent.mkdir(parents=True)
        self.env = {'CODEX_SESSION_ID': SID, 'CODEX_THREAD_ID': SID, 'CODEX_HOME': str(self.home)}
        self.records = [self.record('session_meta', {'id': SID, 'timestamp': '2026-11-09T00:00:00Z', 'cwd': str(self.root)}),
                        self.message('user_message', 'same question'),
                        self.message('agent_message', 'Exact answer\n', phase='final_answer'),
                        self.message('user_message', 'same question')]
        self.save()
        (self.root / '.hai/templates').mkdir(parents=True)
        shutil.copy(Path(__file__).resolve().parents[3] / 'templates/state.json', self.root / '.hai/templates/state.json')
        (self.root / '.hai_env/config').mkdir(parents=True)
        (self.root / '.hai_env/config/agent_instructions.md').write_text('')
        self.state = {'state_format_version': 3, 'activities': {'location': '.hai_env/activities'},
                      'features': {'chronicles': {'enabled': True, 'record_every_prompts': 5}}}
        self.save_state()
        self.prov = {'source': 'fixture explicit enabled-current-session policy', 'reason': 'test registration'}
        created = activities.handle('create', self.root, {'initial_input': '', 'provenance': self.prov}, True)
        self.assertTrue(created['ok'], created)
        self.ident = created['result']['state']['activity_id']; self.base = self.root / created['result']['path']

    def record(self, kind, payload):
        return {'timestamp': '2026-11-09T00:00:00Z', 'type': kind, 'payload': payload}

    def message(self, kind, text, **fields):
        return self.record('event_msg', {'type': kind, 'message': text, **fields})

    def save(self):
        self.source.write_text(''.join(json.dumps(r) + '\n' for r in self.records), encoding='utf-8')

    def save_state(self):
        (self.root / '.hai_env/config/state.json').write_text(json.dumps(self.state))

    def call(self, op, request, apply=False):
        with mock.patch.dict(os.environ, self.env, clear=True):
            return recording.handle(op, self.root, request, apply)

    def binding(self, start=1):
        return {'activity_id': self.ident, 'start_position': start,
                'enabled_intervals': [{'start': {'source_session_id': SID, 'source_position': start},
                                       'end': None, 'provenance': 'fixture enabled before observed work prompt'}],
                'provenance': self.prov}

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def test_exact_identity_discovery_and_no_content_disclosure_or_writes(self):
        unrelated = self.source.with_name('rollout-other-' + OTHER + '.jsonl')
        unrelated.write_text('not JSON; must never be opened')
        before = self.snapshot()
        result = self.call('discover', {})
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['result']['path'], str(self.source))
        self.assertEqual(result['result']['latest_user_occurrence']['source_position'], 3)
        self.assertNotIn('same question', json.dumps(result))
        self.assertEqual(before, self.snapshot())

    def test_host_path_preferred_and_ambiguous_candidates_never_selected(self):
        copy = self.source.parent / ('rollout-copy-' + SID + '.jsonl'); copy.write_bytes(self.source.read_bytes())
        result = self.call('discover', {})
        self.assertFalse(result['ok']); self.assertIn('found 2', str(result['issues']))
        result = self.call('discover', {'source_path': str(self.source)})
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['result']['discovery_method'], 'host_supplied_path')

    def test_current_thread_preferred_to_inherited_parent_session(self):
        env = {**self.env, 'CODEX_SESSION_ID': OTHER}
        self.assertEqual(sources.resolve(self.root, {}, env)['session_id'], SID)
        with self.assertRaisesRegex(Exception, 'conflict'):
            sources.resolve(self.root, {'session_id': OTHER}, env)
        env.pop('CODEX_THREAD_ID'); env['CODEX_SESSION_ID'] = SID
        self.assertEqual(sources.resolve(self.root, {}, env)['session_id'], SID)

    def test_representation_requires_observed_user_not_implicit_guessing(self):
        self.records = [self.records[0],
                        self.record('response_item', {'type': 'message', 'role': 'user',
                            'content': [{'type': 'input_text', 'text': 'actual assigned user prompt'}]}),
                        self.record('response_item', {'type': 'message', 'role': 'assistant', 'phase': 'final_answer',
                            'content': [{'type': 'output_text', 'text': 'actual saved final'}]})]
        self.save()
        result = self.call('discover', {})
        self.assertFalse(result['ok']); self.assertIn('selected representation', str(result['issues']))
        result = self.call('discover', {'representation': 'response_item'})
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['result']['latest_user_occurrence']['source_position'], 1)
        request = self.binding(); request['representation'] = 'response_item'
        self.assertTrue(self.call('bind', request, True)['ok'])

    def test_missing_conflicting_identity_wrong_metadata_and_wrong_workspace(self):
        with self.assertRaisesRegex(Exception, 'identity unavailable'):
            sources.resolve(self.root, {}, {})
        for request in ({'session_id': OTHER}, {'session_id': '../escape'}):
            self.assertFalse(self.call('discover', request)['ok'])
        self.records[0]['payload']['id'] = OTHER; self.save()
        self.assertFalse(self.call('discover', {})['ok'])
        self.records[0]['payload']['id'] = SID
        self.records[0]['payload']['cwd'] = str(self.root / 'elsewhere'); self.save()
        self.assertIn('workspace', str(self.call('discover', {})['issues']))
        self.source.unlink()
        self.assertIn('found 0', str(self.call('discover', {})['issues']))

    def test_symlinks_hardlinks_and_malformed_tail_fail(self):
        with self.source.open('a') as stream:
            stream.write('{')
        self.assertFalse(self.call('discover', {})['ok'])
        self.save()
        link = self.root / 'linked.jsonl'
        try:
            link.symlink_to(self.source)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(str(exc))
        self.assertFalse(self.call('discover', {'source_path': str(link)})['ok'])
        link.unlink(); link.hardlink_to(self.source)
        self.assertFalse(self.call('discover', {})['ok'])

    def test_disabled_recording_does_not_discover_or_create_defaults(self):
        self.state['features']['chronicles']['enabled'] = False; self.save_state()
        before = self.snapshot()
        with mock.patch.object(sources, 'resolve', side_effect=AssertionError('discovery forbidden when disabled')):
            for op, req in [('discover', {}), ('bind', self.binding())]:
                result = self.call(op, req, op == 'bind')
                self.assertTrue(result['ok'], result)
                self.assertEqual(result['result']['status'], 'disabled')
        self.assertEqual(before, self.snapshot())
        req = self.binding(); req['mandatory'] = True
        self.assertTrue(self.call('bind', req, True)['ok'])
        self.assertFalse(json.loads((self.root / '.hai_env/config/state.json').read_text())['features']['chronicles']['enabled'])

    def test_observed_occurrence_preview_first_bind_resume_and_exact_duplicate_text(self):
        before = self.snapshot(); result = self.call('bind', self.binding(), False)
        self.assertTrue(result['ok'], result); self.assertEqual(before, self.snapshot())
        self.assertFalse(self.call('bind', self.binding(2), True)['ok'])  # Assistant, not user.
        self.assertFalse(self.call('bind', self.binding(True), True)['ok'])
        result = self.call('bind', self.binding(), True); self.assertTrue(result['ok'], result)
        segment = self.base / result['result']['segments'][0]
        self.assertEqual(segment.read_text().count('same question'), 2)  # Occurrences, not text deduplication.
        first = segment.read_bytes()
        self.assertTrue(self.call('bind', self.binding(), True)['ok'])
        self.assertEqual(first, segment.read_bytes())
        changed = self.binding(3)
        self.assertFalse(self.call('bind', changed, True)['ok'])  # Existing boundary cannot silently move.
        self.assertTrue(self.call('verify', {'activity_id': self.ident})['ok'])

    def test_startup_reports_readiness_without_mutation_and_early_failure(self):
        def context():
            with mock.patch.dict(os.environ, self.env, clear=True):
                return startup.handle('', self.root, {}, False)
        before = self.snapshot(); result = context()
        self.assertTrue(result['ok']); self.assertEqual(result['result']['recording_context']['status'], 'needs_binding')
        self.assertEqual(before, self.snapshot())
        self.assertTrue(self.call('bind', self.binding(), True)['ok'])
        self.assertEqual(context()['result']['recording_context']['status'], 'verified')
        self.records.append(self.message('user_message', 'new task')); self.save()
        self.assertEqual(context()['result']['recording_context']['status'], 'needs_synchronization')
        self.assertTrue(self.call('synchronize', {'activity_id': self.ident, 'provenance': self.prov}, True)['ok'])
        self.source.unlink()
        result = context()
        self.assertTrue(result['ok'])  # Core validity remains independent of recording readiness.
        self.assertEqual(result['result']['recording_context']['status'], 'blocked')

    def test_missing_current_identity_never_claims_prior_binding_is_ready(self):
        self.assertTrue(self.call('bind', self.binding(), True)['ok'])
        with mock.patch.dict(os.environ, {}, clear=True):
            result = startup.handle('', self.root, {}, False)
        self.assertTrue(result['ok'])
        readiness = result['result']['recording_context']
        self.assertEqual(readiness['status'], 'unverified')
        self.assertEqual(readiness['registered_source_count'], 1)

    def test_partial_write_preserves_evidence_and_blocks_unsafe_retry(self):
        from runtime import chronicles
        original = chronicles.write_json
        def fail(root, path, value, expected=None):
            if path.endswith('core.json'):
                raise OSError('injected binding-ledger failure')
            return original(root, path, value, expected)
        with mock.patch.object(chronicles, 'write_json', side_effect=fail):
            result = self.call('bind', self.binding(), True)
        self.assertEqual(result['status'], 'partial', result)
        self.assertTrue(list((self.base / 'chronicles').glob('*segment*.md')))
        self.assertFalse(self.call('bind', self.binding(), True)['ok'])

    def test_bound_source_rewrite_and_resumed_metadata(self):
        self.assertTrue(self.call('bind', self.binding(), True)['ok'])
        self.records.append(self.record('session_meta', dict(self.records[0]['payload'])))
        self.save()
        self.assertTrue(self.call('synchronize', {'activity_id': self.ident, 'provenance': self.prov}, True)['ok'])
        self.records[1]['payload']['message'] = 'rewritten'
        self.save()
        self.assertFalse(self.call('synchronize', {'activity_id': self.ident, 'provenance': self.prov}, True)['ok'])

    def test_native_delegation_uses_verified_assignment_range_not_environment_user(self):
        self.assertTrue(self.call('bind', self.binding(), True)['ok'])
        child = self.source.with_name('rollout-child-' + OTHER + '.jsonl')
        records = [self.record('session_meta', {'id': OTHER, 'timestamp': '2026-11-09T00:00:00Z', 'cwd': str(self.root)}),
                   self.record('response_item', {'type': 'message', 'role': 'user',
                       'content': [{'type': 'input_text', 'text': '<environment_context>metadata only</environment_context>'}]}),
                   self.record('response_item', {'type': 'agent_message', 'author': '/root', 'recipient': '/root/reviewer',
                       'content': [{'type': 'text', 'text': 'Native assignment; not a human prompt'}]}),
                   self.record('response_item', {'type': 'message', 'role': 'assistant', 'phase': 'final_answer',
                       'content': [{'type': 'output_text', 'text': 'Verified reviewer outcome'}]})]
        child.write_text(''.join(json.dumps(r) + '\n' for r in records))
        assignment = {'path': str(child), 'session_id': OTHER, 'representation': 'response_item', 'start_position': 2,
                      'enabled_intervals': [{'start': {'source_session_id': OTHER, 'source_position': 2}, 'end': None,
                                            'provenance': 'host verified native assignment author/recipient and exact occurrence'}]}
        result = self.call('synchronize', {'activity_id': self.ident, 'sources': [assignment], 'provenance': self.prov}, True)
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['result']['source_count'], 2)
        segments = '\n'.join((self.base / p).read_text() for p in result['result']['segments'])
        self.assertIn('Verified reviewer outcome', segments)
        self.assertNotIn('environment_context', segments)
        self.assertNotIn('Native assignment;', segments)


if __name__ == '__main__':
    unittest.main()
