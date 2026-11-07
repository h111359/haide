"""Usage arithmetic, source attribution, stale data and closure fixtures."""
from decimal import Decimal
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

TOOLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(TOOLS))
from runtime import activities, usage


class UsageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='hai-usage-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / '.hai_env/activities').mkdir(parents=True)
        (self.root / '.hai/templates').mkdir(parents=True)
        shutil.copy(TOOLS.parent / 'templates/state.json', self.root / '.hai/templates/state.json')
        (self.root / '.hai_env/agent_instructions.md').write_text('')
        (self.root / '.hai_env/state.json').write_text(json.dumps({'state_format_version': 3,
            'activities': {'location': '.hai_env/activities'}, 'features': {'chronicles': {'enabled': False}}}))
        self.prov = {'source': 'fixture host', 'reason': 'verify assigned usage'}
        c = activities.handle('create', self.root, {'initial_input': '', 'provenance': self.prov}, True)
        self.assertTrue(c['ok'], c)
        self.ident = c['result']['state']['activity_id']
        self.base = self.root / c['result']['path']
        self.source = self.root / 'session.jsonl'
        self.lines = [self.record('session_meta', {'id': 'session', 'timestamp': '2026-11-06T00:00:00Z'}),
            self.record('turn_context', {'model': 'model-one'}), self.counter(100, 60, 20, 10),
            self.record('event_msg', {'type': 'user_message', 'message': 'Activity starts here'}),
            self.counter(160, 110, 40, 15), self.counter(160, 110, 40, 15),
            self.record('turn_context', {'model': 'model-two'}), self.counter(200, 130, 50, 18)]
        self.save()
        self.assignment = {'path': str(self.source), 'session_id': 'session', 'start_position': 3}
        self.rate = {'rates': {
            'model-one': {'input_credits_per_million': '10', 'cached_input_credits_per_million': '1', 'output_credits_per_million': '20'},
            'model-two': {'input_credits_per_million': '20', 'cached_input_credits_per_million': '2', 'output_credits_per_million': '40'}},
            'source': 'Synthetic fixture rates, not current prices', 'captured_at': '2026-11-06T00:00:00Z'}

    def record(self, kind, payload):
        return {'timestamp': '2026-11-06T00:01:00Z', 'type': kind, 'payload': payload}

    def counter(self, inp, cached, out, reasoning):
        return self.record('event_msg', {'type': 'token_count',
            'info': {'total_token_usage': {'input_tokens': inp, 'cached_input_tokens': cached,
                'output_tokens': out, 'reasoning_output_tokens': reasoning, 'total_tokens': inp + out}},
            'rate_limits': {'credits': {'balance': '98765'}, 'primary': {'used_percent': 50}}})

    def save(self):
        self.source.write_text(''.join(json.dumps(r) + '\n' for r in self.lines))

    def update(self, apply=True, **kw):
        return activities.handle('usage-update', self.root, {'activity_id': self.ident,
            'provenance': self.prov, **kw}, apply)

    def close(self):
        return activities.handle('close', self.root, {'activity_id': self.ident,
            'outcome': 'completed', 'archive_label': 'usage-test', 'outcome_text': 'Fixture completed',
            'recording': {'status': 'disabled', 'details': 'Fixture recording off'},
            'provenance': self.prov}, True)

    def test_cumulative_deltas_do_not_double_count_repeated_snapshots(self):
        r = self.update(sources=[self.assignment])
        self.assertTrue(r['ok'], r)
        expected = {'input_tokens': 100, 'cached_input_tokens': 70, 'output_tokens': 30,
                    'reasoning_output_tokens': 8, 'total_tokens': 130}
        self.assertEqual(r['result']['summary']['tokens'], expected)
        self.assertEqual(self.update()['result']['summary']['tokens'], expected)
        self.assertEqual(r['result']['summary']['coverage'], 'observed')
        self.assertIsNone(r['result']['summary']['reported_credits'])
        self.assertIsNone(r['result']['summary']['estimated_credits'])

    def test_model_rates_cached_input_and_reasoning_subset_arithmetic(self):
        r = self.update(sources=[self.assignment], pricing=self.rate)
        self.assertTrue(r['ok'], r)
        s = r['result']['summary']
        self.assertEqual(Decimal(s['estimated_credits']), Decimal('0.00139'))
        text = (self.base / 'usage.md').read_text()
        self.assertIn('not actual debited credits', text)
        self.assertIn('Caller-reported credits | Unavailable', text)

    def test_missing_model_rates_are_unavailable(self):
        rate = {**self.rate}
        s = self.update(sources=[self.assignment], pricing=rate)['result']['summary']
        self.assertIsNotNone(s['estimated_credits'])
        self.assertNotIn('estimated_money', s)
        rate['rates'] = {'model-one': self.rate['rates']['model-one']}
        s = self.update(pricing=rate)['result']['summary']
        self.assertIsNone(s['estimated_credits'])
        self.assertEqual(s['missing_rate_models'], ['model-two'])

    def test_tokens_and_credits_only_and_null_legacy_checkpoint(self):
        self.assertTrue(self.update(sources=[self.assignment], pricing=self.rate)['ok'])
        ledger = self.base / 'usage.json'
        data = json.loads(ledger.read_text())
        self.assertEqual(data['usage_format_version'], 2)
        self.assertNotIn('money', (self.base / 'usage.md').read_text().lower())
        self.assertNotIn('currency', data['pricing'])
        data['usage_format_version'] = 1
        data['pricing'].update(currency=None, money_per_credit=None)
        data['summary'].update(estimated_money=None, reported_money=None)
        ledger.write_text(json.dumps(data))
        self.assertTrue(self.update()['ok'])
        self.assertEqual(json.loads(ledger.read_text())['usage_format_version'], 2)
        for extra in [{'currency': 'EUR'}, {'money_per_credit': '0.04'}]:
            self.assertFalse(self.update(pricing={**self.rate, **extra})['ok'])
        self.assertFalse(self.update(reported_spend={'credits': '1', 'money': None,
            'source': 'fixture', 'through': {'session': 7}})['ok'])

    def test_multi_session_totals_and_duplicate_registration(self):
        other = self.root / 'other.jsonl'
        records = [self.record('session_meta', {'id': 'other', 'timestamp': '2026-11-06T00:00:00Z'}),
                   self.record('turn_context', {'model': 'model-one'}), self.counter(10, 0, 5, 0)]
        other.write_text(''.join(json.dumps(r) + '\n' for r in records))
        b = {'path': str(other), 'session_id': 'other', 'start_position': 0}
        r = self.update(sources=[self.assignment, b])
        self.assertEqual(r['result']['summary']['tokens']['total_tokens'], 145)
        self.assertEqual(self.update(sources=[self.assignment])['result']['summary']['tokens']['total_tokens'], 145)
        before = (self.base / 'usage.json').read_bytes()
        self.assertFalse(self.update(sources=[b, b])['ok'])
        self.assertEqual((self.base / 'usage.json').read_bytes(), before)

    def test_fixed_cutoff_ignores_later_records_and_source_rewrite_is_stale(self):
        b = {**self.assignment, 'end_position': 5}
        r = self.update(sources=[b])
        self.assertEqual(r['result']['summary']['tokens']['total_tokens'], 80)
        self.source.write_bytes(self.source.read_bytes() + b'{incomplete later record')
        self.assertEqual(self.update()['result']['summary']['tokens']['total_tokens'], 80)
        raw = self.source.read_text().replace('model-one', 'model-bad')
        self.source.write_text(raw)
        r = self.update()
        self.assertEqual(r['result']['summary']['coverage'], 'partial')
        self.assertEqual(r['result']['summary']['tokens']['total_tokens'], 80)
        state = json.loads((self.base / 'usage.json').read_text())
        self.assertEqual(state['sources'][0]['status'], 'stale')

    def test_missing_truncated_and_wrong_session_are_not_zero(self):
        self.source.unlink()
        s = self.update(sources=[self.assignment])['result']['summary']
        self.assertEqual(s['coverage'], 'unavailable')
        self.assertIsNone(s['tokens'])
        self.save()
        self.source.write_bytes(self.source.read_bytes()[:-1])
        self.assertIsNone(self.update()['result']['summary']['tokens'])
        self.lines[0]['payload']['id'] = 'different'; self.save()
        self.assertIsNone(self.update()['result']['summary']['tokens'])

    def test_counter_reset_and_boolean_counters_are_rejected(self):
        self.lines.append(self.counter(1, 0, 1, 0)); self.save()
        self.assertIsNone(self.update(sources=[self.assignment])['result']['summary']['tokens'])
        self.lines.pop(); self.lines[4]['payload']['info']['total_token_usage']['input_tokens'] = True; self.save()
        self.assertIsNone(self.update()['result']['summary']['tokens'])

    def test_reported_spend_is_separate_and_becomes_stale_at_new_cutoff(self):
        spend = {'credits': '1.23',
                 'source': 'Explicit fixture host billing evidence', 'through': {'session': 7}}
        r = self.update(sources=[self.assignment], pricing=self.rate, reported_spend=spend)
        s = r['result']['summary']
        self.assertEqual(s['reported_credits'], '1.23')
        self.assertNotEqual(s['estimated_credits'], s['reported_credits'])
        self.lines.append(self.counter(260, 160, 70, 25)); self.save()
        s = self.update()['result']['summary']
        self.assertFalse(s['reported_spend_current'])
        self.assertIsNone(s['reported_credits'])

    def test_preview_and_empty_read_have_no_side_effects(self):
        r = activities.handle('usage-read', self.root, {'activity_id': self.ident}, False)
        self.assertFalse(r['result']['available'])
        self.assertFalse((self.base / 'usage.md').exists())
        r = self.update(apply=False, sources=[self.assignment])
        self.assertEqual(r['status'], 'planned')
        self.assertEqual(r['changed_files'], [])
        self.assertFalse((self.base / 'usage.json').exists())

    def test_invalid_rates_bindings_and_noncanonical_sources(self):
        for rate in [float('nan'), 'NaN', '-1', '1e99999999', True]:
            pricing = {**self.rate, 'rates': {'model-one': {**self.rate['rates']['model-one'], 'input_credits_per_million': rate}}}
            self.assertFalse(self.update(pricing=pricing)['ok'])
        for b in [{**self.assignment, 'start_position': True}, {**self.assignment, 'path': '../escape'}]:
            self.assertFalse(self.update(sources=[b])['ok'])
        self.assertTrue(self.update(sources=[self.assignment])['ok'])
        self.assertFalse(self.update(sources=[{**self.assignment, 'start_position': 0}])['ok'])

    def test_close_refreshes_latest_tokens_and_archives_readable_record(self):
        self.assertTrue(self.update(sources=[self.assignment])['ok'])
        self.lines.append(self.counter(260, 160, 70, 25)); self.save()
        closed = self.close()
        self.assertTrue(closed['ok'], closed)
        result = closed['result']
        self.assertEqual(result['usage']['summary']['tokens']['total_tokens'], 210)
        self.assertTrue((self.root / result['usage']['path']).is_file())
        archived = activities.handle('usage-read', self.root, {'activity_id': self.ident}, False)
        self.assertEqual(archived['result']['summary']['tokens']['total_tokens'], 210)
        self.assertFalse(self.update()['ok'])

    def test_close_without_assigned_sources_records_unavailable(self):
        closed = self.close()
        self.assertTrue(closed['ok'], closed)
        ledger = json.loads((self.root / closed['result']['archive_path'] / 'usage.json').read_text())
        self.assertEqual(ledger['summary']['coverage'], 'unavailable')
        self.assertIsNone(ledger['summary']['tokens'])

    def test_invalid_existing_records_block_close_without_lifecycle_writes(self):
        self.update(sources=[self.assignment])
        (self.base / 'usage.json').write_text('{invalid')
        before = (self.base / 'log.md').read_bytes()
        r = self.close()
        self.assertFalse(r['ok'])
        self.assertEqual((self.base / 'log.md').read_bytes(), before)
        self.assertEqual(json.loads((self.base / 'state.json').read_text())['lifecycle'], 'active')
        self.assertFalse((self.base / 'outcome.md').exists())

    def test_partial_report_failure_stops_closure_and_retains_checkpoint(self):
        self.update(sources=[self.assignment])
        self.lines.append(self.counter(260, 160, 70, 25)); self.save()
        with mock.patch.object(usage, 'write_bytes', side_effect=OSError('injected report failure')):
            r = self.close()
        self.assertEqual(r['status'], 'partial', r)
        ledger = json.loads((self.base / 'usage.json').read_text())
        self.assertEqual(ledger['summary']['tokens']['total_tokens'], 210)
        self.assertEqual(json.loads((self.base / 'state.json').read_text())['lifecycle'], 'active')
        self.assertFalse((self.base / 'outcome.md').exists())

    def test_user_report_without_checkpoint_is_preserved(self):
        (self.base / 'usage.md').write_text('Existing human notes')
        self.assertFalse(self.update()['ok'])
        self.assertFalse(self.close()['ok'])
        self.assertEqual((self.base / 'usage.md').read_text(), 'Existing human notes')

    def test_external_activity_change_during_update_is_partial(self):
        original = usage.write_bytes
        def changed(root, relative, content, expected=None):
            original(root, relative, content, expected)
            path = self.base / 'state.json'
            data = json.loads(path.read_text()); data['external_change'] = True
            path.write_text(json.dumps(data))
        with mock.patch.object(usage, 'write_bytes', side_effect=changed):
            result = self.update(sources=[self.assignment])
        self.assertEqual(result['status'], 'partial', result)
        self.assertIn('Activity changed', result['issues'][0])
        self.assertTrue((self.base / 'usage.json').is_file())
        self.assertTrue((self.base / 'usage.md').is_file())

    def test_linked_source_and_report_are_not_followed(self):
        alias = self.root / 'alias.jsonl'
        try:
            alias.symlink_to(self.source)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable')
        s = self.update(sources=[{**self.assignment, 'path': str(alias)}])['result']['summary']
        self.assertIsNone(s['tokens'])
        (self.base / 'usage.md').unlink()
        (self.base / 'usage.md').symlink_to(self.root / 'human.md')
        self.assertFalse(self.update()['ok'])

    def test_cli_update_then_read(self):
        request = self.root / 'request.json'
        request.write_text(json.dumps({'activity_id': self.ident, 'sources': [self.assignment], 'provenance': self.prov}))
        args = [sys.executable, '-B', str(TOOLS / 'hai.py'), 'activity', 'usage-update', '--workspace', str(self.root), '--request', str(request)]
        r = subprocess.run(args + ['--apply'], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        request.write_text(json.dumps({'activity_id': self.ident})); args[4] = 'usage-read'
        r = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertTrue(json.loads(r.stdout)['result']['available'])


if __name__ == '__main__':
    unittest.main()
