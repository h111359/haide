import json
from pathlib import Path
import sys
import shutil
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runtime import activities, recording, chronicles, environment


class CoreChronicleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / '.hai_env/activities').mkdir(parents=True)
        (self.root / '.hai_env/config').mkdir()
        (self.root / '.hai/templates').mkdir(parents=True)
        shutil.copy(Path(__file__).resolve().parents[3] / 'templates/state.json', self.root / '.hai/templates/state.json')
        (self.root / '.hai_env/config/agent_instructions.md').write_text('', encoding='utf-8')
        self.state = {'state_format_version': 3, 'activities': {'location': '.hai_env/activities'},
                      'features': {'chronicles': {'enabled': True, 'record_every_prompts': 5}}}
        self.save_state()
        self.prov = {'source': 'fixture explicit source assignment', 'reason': 'verify core recording'}
        c = activities.handle('create', self.root, {'initial_input': '', 'provenance': self.prov}, True)
        self.assertTrue(c['ok'], c)
        self.ident = c['result']['state']['activity_id']; self.base = self.root / c['result']['path']
        self.source = self.root / 'session.jsonl'
        self.lines = [self.record('session_meta', {'id': 'one', 'timestamp': '2026-11-07T00:00:00Z'}),
                      self.message('user_message', 'outside assigned Activity'),
                      self.message('user_message', 'Exact\n\n## Outcome:\n  user text  \n'),
                      self.message('agent_message', 'Exact answer\n', phase='final_answer'),
                      self.message('agent_message', 'progress omitted', phase='commentary')]
        self.save()
        self.assignment = {'path': str(self.source), 'session_id': 'one', 'start_position': 2,
                           'representation': 'event_msg', 'enabled_intervals': [{'start': {'source_session_id': 'one', 'source_position': 2}, 'end': None, 'provenance': 'fixture recording enabled before assigned Activity'}]}

    def tearDown(self): self.temp.cleanup()
    def save_state(self): (self.root / '.hai_env/config/state.json').write_text(json.dumps(self.state), encoding='utf-8')
    def record(self, kind, payload): return {'timestamp': '2026-11-07T00:00:00Z', 'type': kind, 'payload': payload}
    def message(self, kind, text, **kw): return self.record('event_msg', {'type': kind, 'message': text, **kw})
    def save(self): self.source.write_text(''.join(json.dumps(r) + '\n' for r in self.lines), encoding='utf-8')
    def sync(self, apply=True, **kw):
        return recording.handle('synchronize', self.root, {'activity_id': self.ident, 'provenance': self.prov, **kw}, apply)
    def close(self, **kw):
        return activities.handle('close', self.root, {'activity_id': self.ident, 'outcome': 'completed', 'archive_label': 'core-chronicles', 'outcome_text': 'done', 'recording': {'status': 'pending', 'details': 'core must flush'}, 'provenance': self.prov, **kw}, True)

    def test_unrelated_archived_content_does_not_block_new_source_assignment(self):
        self.assertTrue(self.sync(sources=[self.assignment])['ok'])
        closed = self.close(); self.assertTrue(closed['ok'], closed)
        archive = self.root / closed['result']['archive_path']
        ledger = json.loads((archive / 'chronicles/core.json').read_text(encoding='utf-8'))
        segment = archive / ledger['sources'][0]['segment_path']
        segment.write_bytes(b'retained altered historical content')
        created = activities.handle('create', self.root, {'initial_input': '', 'provenance': self.prov}, True)
        self.ident = created['result']['state']['activity_id']
        self.base = self.root / created['result']['path']
        # A matching session still needs full historical verification.
        same = self.sync(sources=[self.assignment])
        self.assertFalse(same['ok']); self.assertIn('artifact changed', str(same['issues']))
        # A distinct source only needs validated historical assignment metadata.
        self.lines[0]['payload']['id'] = 'two'; self.save()
        other = {**self.assignment, 'session_id': 'two', 'enabled_intervals': [
            {'start': {'source_session_id': 'two', 'source_position': 2}, 'end': None, 'provenance': 'new assignment'}]}
        result = self.sync(sources=[other]); self.assertTrue(result['ok'], result)
        self.assertEqual(segment.read_bytes(), b'retained altered historical content')
        # Corrupt ledger assignments remain blockers even for unrelated sources.
        ledger['sources'][0]['binding']['start_position'] = -1
        (archive / 'chronicles/core.json').write_text(json.dumps(ledger), encoding='utf-8')
        self.assertFalse(self.sync()['ok'])

    def test_exact_text_idempotence_preview_and_read_only_verify(self):
        r = self.sync(False, sources=[self.assignment]); self.assertTrue(r['ok'], r)
        self.assertFalse((self.base / 'chronicles').exists())
        r = self.sync(sources=[self.assignment]); self.assertTrue(r['ok'], r)
        segment = self.base / r['result']['segments'][0]; text = segment.read_text(encoding='utf-8')
        self.assertIn('Exact\n\n## Outcome:\n  user text  \n', text)
        self.assertIn('Exact answer\n', text)
        self.assertNotIn('outside assigned Activity', text); self.assertNotIn('progress omitted', text)
        old = segment.read_bytes(); self.assertTrue(self.sync()['ok']); self.assertEqual(old, segment.read_bytes())
        self.assertTrue(recording.handle('verify', self.root, {'activity_id': self.ident}, False)['ok'])
        self.assertFalse(recording.handle('verify', self.root, {'activity_id': self.ident}, True)['ok'])

    def test_enabled_close_cannot_bypass_with_optional_pending_status(self):
        r = self.close(recording_requirement={'enabled': True, 'mandatory': False})
        self.assertFalse(r['ok'], r); self.assertEqual(json.loads((self.base / 'state.json').read_text(encoding='utf-8'))['lifecycle'], 'active')
        self.assertFalse((self.base / 'outcome.md').exists())

    def test_close_flushes_below_cadence_and_finalizes_bounds(self):
        self.assertTrue(self.sync(sources=[self.assignment])['ok'])
        self.lines.append(self.message('user_message', 'close this Activity')); self.save()
        r = self.close(); self.assertTrue(r['ok'], r)
        archive = self.root / r['result']['archive_path']
        self.assertIn('close this Activity', next((archive / 'chronicles').glob('*segment*.md')).read_text(encoding='utf-8'))
        ledger = json.loads((archive / 'chronicles/core.json').read_text(encoding='utf-8'))
        self.assertEqual(ledger['sources'][0]['binding']['end_position'], 5)
        self.assertEqual(r['result']['recording']['status'], 'verified')
        self.assertTrue(chronicles.verify(self.root, archive.relative_to(self.root).as_posix(), self.ident)['status'] == 'verified')
        self.assertFalse(self.sync()['ok'])

    def test_disabled_no_obligation_needs_no_source_and_writes_no_transcript(self):
        self.state['features']['chronicles']['enabled'] = False; self.save_state()
        r = self.sync(sources=[self.assignment]); self.assertTrue(r['ok'], r)
        self.assertEqual(r['changed_files'], []); self.assertFalse((self.base / 'chronicles').exists())
        self.assertTrue(self.close(recording={'status': 'disabled', 'details': 'off'})['ok'])

    def test_missing_rewritten_and_incomplete_sources_block_without_lifecycle_writes(self):
        self.assertTrue(self.sync(sources=[self.assignment])['ok'])
        self.source.unlink(); self.assertFalse(self.close()['ok']); self.assertTrue(self.base.exists())
        self.save(); self.lines[2]['payload']['message'] = 'rewritten'; self.save()
        self.assertFalse(self.sync()['ok']); self.assertFalse((self.base / 'outcome.md').exists())

    def test_wrong_identity_and_incomplete_source_are_not_recorded(self):
        self.lines[0]['payload']['id'] = 'other'; self.save()
        self.assertFalse(self.sync(sources=[self.assignment])['ok'])
        self.lines[0]['payload']['id'] = 'one'; self.save(); self.source.write_bytes(self.source.read_bytes()[:-1] + b'{')
        self.assertFalse(self.sync(sources=[self.assignment])['ok']); self.assertFalse((self.base / 'chronicles').exists())

    def test_tampered_segment_and_legacy_checkpoint_are_preserved(self):
        r = self.sync(sources=[self.assignment]); segment = self.base / r['result']['segments'][0]
        segment.write_text('manual edit', encoding='utf-8'); self.assertFalse(self.sync()['ok']); self.assertEqual(segment.read_text(encoding='utf-8'), 'manual edit')
        (self.base / 'chronicles/core.json').unlink(); self.assertFalse(self.sync(sources=[self.assignment])['ok'])
        self.assertEqual(segment.read_text(encoding='utf-8'), 'manual edit')

    def test_disabled_intervals_and_duplicate_bindings(self):
        self.assignment['enabled_intervals'][0]['end'] = {'source_session_id': 'one', 'source_position': 2}
        r = self.sync(sources=[self.assignment]); self.assertTrue(r['ok'], r)
        self.assertNotIn('Exact answer', (self.base / r['result']['segments'][0]).read_text(encoding='utf-8'))
        self.assertFalse(self.sync(sources=[self.assignment, self.assignment])['ok'])
        changed = {**self.assignment, 'start_position': 0}; self.assertFalse(self.sync(sources=[changed])['ok'])

    def test_partial_checkpoint_write_stops_closure_and_preserves_segment(self):
        original = chronicles.write_bytes
        def fail(root, path, raw, expected=None):
            if path.endswith('/checkpoint.json'): raise OSError('injected checkpoint failure')
            return original(root, path, raw, expected)
        with mock.patch.object(chronicles, 'write_bytes', side_effect=fail):
            r = self.sync(sources=[self.assignment])
        self.assertEqual(r['status'], 'partial', r)
        self.assertTrue(list((self.base / 'chronicles').glob('*segment*.md')))
        self.assertFalse(self.close()['ok']); self.assertFalse((self.base / 'outcome.md').exists())

    def test_new_activity_can_use_later_same_session_range(self):
        self.assertTrue(self.sync(sources=[self.assignment])['ok']); self.assertTrue(self.close()['ok'])
        self.lines.append(self.message('user_message', 'new Activity')); self.save()
        c = activities.handle('create', self.root, {'initial_input': '', 'provenance': self.prov}, True)
        self.ident = c['result']['state']['activity_id']; self.base = self.root / c['result']['path']
        later = {**self.assignment, 'start_position': 5, 'enabled_intervals': [{'start': {'source_session_id': 'one', 'source_position': 5}, 'end': None, 'provenance': 'new Activity'}]}
        self.assertTrue(self.sync(sources=[later])['ok'])

    def test_overlap_with_previous_activity_is_rejected(self):
        self.assertTrue(self.sync(sources=[self.assignment])['ok']); self.assertTrue(self.close()['ok'])
        c = activities.handle('create', self.root, {'initial_input': '', 'provenance': self.prov}, True); self.ident = c['result']['state']['activity_id']; self.base = self.root / c['result']['path']
        self.assertFalse(self.sync(sources=[self.assignment])['ok'])

    def test_corrupt_neighbor_ledger_cannot_hide_overlapping_recorded_ranges(self):
        self.assertTrue(self.sync(sources=[self.assignment])['ok']); closed = self.close(); self.assertTrue(closed['ok'])
        ledger = self.root / closed['result']['archive_path'] / 'chronicles/core.json'
        data = json.loads(ledger.read_text(encoding='utf-8')); data['sources'] = []; ledger.write_text(json.dumps(data), encoding='utf-8')
        c = activities.handle('create', self.root, {'initial_input': '', 'provenance': self.prov}, True)
        self.ident = c['result']['state']['activity_id']; self.base = self.root / c['result']['path']
        self.assertFalse(self.sync(sources=[self.assignment])['ok']); self.assertFalse((self.base / 'chronicles').exists())

    def test_archived_verification_survives_later_enablement_changes(self):
        self.assertTrue(self.sync(sources=[self.assignment])['ok']); self.assertTrue(self.close()['ok'])
        self.toggle(False)
        r = recording.handle('verify', self.root, {'activity_id': self.ident}, False)
        self.assertTrue(r['ok'], r)

    def test_new_eligible_source_after_finalize_blocks_fresh_closure_verification(self):
        self.assertTrue(self.sync(sources=[self.assignment])['ok'])
        base = self.base.relative_to(self.root).as_posix()
        chronicles.synchronize(self.root, base, self.ident, {'provenance': self.prov}, activities.now(), True,
            chronicles.fingerprint(self.base / 'state.json'), finalize=True)
        self.lines.append(self.message('user_message', 'new eligible input')); self.save()
        with self.assertRaisesRegex(Exception, 'New eligible exchange'):
            chronicles.verify(self.root, base, self.ident, closing=True)


    def toggle(self, enabled):
        r = environment.handle('environment/configure', self.root,
            {'changes': {'features.chronicles.enabled': enabled}, 'provenance': self.prov}, True)
        self.assertTrue(r['ok'], r)

    def test_explicit_sync_recovers_live_binding_after_interrupted_closure(self):
        self.assertTrue(self.sync(sources=[self.assignment])['ok'])
        base = self.base.relative_to(self.root).as_posix()
        chronicles.synchronize(self.root, base, self.ident, {'provenance': self.prov}, activities.now(), True,
            chronicles.fingerprint(self.base / 'state.json'), finalize=True)
        self.lines.append(self.message('user_message', 'new eligible input')); self.save()
        self.assertFalse(recording.handle('verify', self.root, {'activity_id': self.ident}, False)['ok'])
        r = self.sync(); self.assertTrue(r['ok'], r)
        self.assertIn('new eligible input', (self.base / r['result']['segments'][0]).read_text(encoding='utf-8'))
        self.assertTrue(self.close()['ok'])

    def test_independent_mandatory_recording_has_core_registration_when_setting_off(self):
        self.toggle(False)
        r = self.sync(sources=[self.assignment], mandatory=True); self.assertTrue(r['ok'], r)
        self.assertTrue((self.base / 'chronicles/checkpoint.json').is_file())
        self.assertTrue(self.close(recording_requirement={'enabled': False, 'mandatory': True})['ok'])
        self.assertFalse(json.loads((self.root / '.hai_env/config/state.json').read_text(encoding='utf-8'))['features']['chronicles']['enabled'])

    def test_enablement_reconciliation_excludes_off_period_and_preserves_recorded_text(self):
        self.assertTrue(self.sync(sources=[self.assignment])['ok'])
        self.toggle(False); self.lines.append(self.message('user_message', 'excluded off period')); self.save()
        self.toggle(True); self.lines.append(self.message('user_message', 'new enabled period')); self.save()
        self.assertFalse(self.sync()['ok'])
        b = {**self.assignment, 'enabled_intervals': [
            {'start': {'source_session_id': 'one', 'source_position': 2}, 'end': {'source_session_id': 'one', 'source_position': 4}, 'provenance': 'first enabled interval'},
            {'start': {'source_session_id': 'one', 'source_position': 6}, 'end': None, 'provenance': 're-enabled after off interval'}]}
        r = self.sync(sources=[b]); self.assertTrue(r['ok'], r)
        text = (self.base / r['result']['segments'][0]).read_text(encoding='utf-8')
        self.assertNotIn('excluded off period', text); self.assertIn('new enabled period', text)
        self.assertIn('Exact answer', text)

    def test_no_trailing_newline_does_not_allow_removal_of_last_recorded_message(self):
        self.lines = self.lines[:4]; self.save(); self.source.write_bytes(self.source.read_bytes().rstrip(b'\n'))
        r = self.sync(sources=[self.assignment]); self.assertTrue(r['ok'], r)
        old = (self.base / r['result']['segments'][0]).read_bytes()
        self.toggle(False); self.toggle(True)
        b = {**self.assignment, 'enabled_intervals': [{'start': {'source_session_id': 'one', 'source_position': 2}, 'end': {'source_session_id': 'one', 'source_position': 2}, 'provenance': 'invalid interval losing final outcome'}]}
        self.assertFalse(self.sync(sources=[b])['ok'])
        self.assertEqual((self.base / r['result']['segments'][0]).read_bytes(), old)

    def test_cadence_change_does_not_reset_enablement(self):
        self.assertTrue(self.sync(sources=[self.assignment])['ok'])
        r = environment.handle('environment/configure', self.root,
            {'changes': {'features.chronicles.record_every_prompts': 10}, 'provenance': self.prov}, True)
        self.assertTrue(r['ok'], r); self.assertTrue(self.sync()['ok'])

    def test_two_sessions_and_nonoverlapping_legacy_ranges(self):
        legacy = self.root / '.hai_env/activities/20261106_000000_legacy'
        legacy.mkdir(); (legacy / 'state.json').write_text(json.dumps({'activity_id': '00000000-0000-0000-0000-000000000001', 'lifecycle': 'closed', 'created_at': '2026-11-06T00:00:00Z', 'closed_at': '2026-11-06T00:00:00Z', 'outcome': 'completed', 'implementation_started_at': None, 'steps': {k: 'not_started' for k in ['analysis', 'clarification', 'planning', 'implementation', 'verification']}}), encoding='utf-8')
        (legacy / 'input.md').write_text('', encoding='utf-8'); (legacy / 'log.md').write_text('', encoding='utf-8'); (legacy / 'outcome.md').write_text('done', encoding='utf-8')
        (legacy / 'chronicles').mkdir(); (legacy / 'chronicles/checkpoint.json').write_text(json.dumps({'sources': [{'source_session_id': 'one', 'assigned_ranges': [{'start': {'source_session_id': 'one', 'source_position': 1}, 'end': {'source_session_id': 'one', 'source_position': 1}}]}]}), encoding='utf-8')
        other = self.root / 'other.jsonl'; other.write_text(json.dumps(self.record('session_meta', {'id': 'two', 'timestamp': '2026-11-07T00:00:00Z'})) + '\n' + json.dumps(self.message('user_message', 'second source')) + '\n', encoding='utf-8')
        b = {**self.assignment, 'path': str(other), 'session_id': 'two', 'start_position': 1,
             'enabled_intervals': [{'start': {'source_session_id': 'two', 'source_position': 1}, 'end': None, 'provenance': 'second session'}]}
        r = self.sync(sources=[self.assignment, b]); self.assertTrue(r['ok'], r)
        self.assertEqual(len(r['result']['segments']), 2)
        self.assertEqual(len(set(r['result']['segments'])), 2)

    def test_pending_checkpoint_is_not_erased_by_refresh(self):
        self.assertTrue(self.sync(sources=[self.assignment])['ok'])
        cp = self.base / 'chronicles/checkpoint.json'; data = json.loads(cp.read_text(encoding='utf-8')); data['pending_ranges'] = [{'reason': 'prepared_delivery'}]; cp.write_text(json.dumps(data), encoding='utf-8')
        ledger = self.base / 'chronicles/core.json'; core = json.loads(ledger.read_text(encoding='utf-8')); core['artifact_hashes']['chronicles/checkpoint.json'] = chronicles.digest(cp.read_bytes()); ledger.write_text(json.dumps(core), encoding='utf-8')
        before = cp.read_bytes(); self.assertFalse(self.sync()['ok']); self.assertEqual(cp.read_bytes(), before)

    def test_symlink_source_and_report_targets_are_rejected(self):
        try:
            link = self.root / 'alias.jsonl'; link.symlink_to(self.source)
        except OSError as exc:
            if getattr(exc, 'winerror', None) == 1314:
                self.skipTest('Windows symlink privilege unavailable')
            raise
        self.assertFalse(self.sync(sources=[{**self.assignment, 'path': str(link)}])['ok'])
        self.assertTrue(self.sync(sources=[self.assignment])['ok'])
        cp = self.base / 'chronicles/checkpoint.json'; cp.unlink(); cp.symlink_to(self.source)
        self.assertFalse(self.sync()['ok'])


if __name__ == '__main__': unittest.main()
