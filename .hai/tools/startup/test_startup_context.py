"""Behavioral checks for read-only startup orchestration and discovery."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import startup_context as context
import test_startup_check as fixtures

SCRIPT = Path(context.__file__).resolve()


class ContextTests(unittest.TestCase):
    setUp = fixtures.StartupTests.setUp
    write = fixtures.StartupTests.write
    save_state = fixtures.StartupTests.save_state
    table = fixtures.StartupTests.table
    snapshot = fixtures.StartupTests.snapshot

    def activity(self, name='00000000_000000_active', ident='5f99ff6b-793b-475e-b184-8618582598ef', lifecycle='active'):
        base = '.hai_env/activities/' + name
        state = {'activity_id': ident, 'lifecycle': lifecycle, 'created_at': '2026-11-03T18:04:42Z',
                 'closed_at': None if lifecycle == 'active' else '2026-11-04T03:21:20Z',
                 'outcome': None if lifecycle == 'active' else 'completed',
                 'implementation_started_at': None,
                 'steps': dict.fromkeys(('clarification', 'analysis', 'planning', 'implementation', 'verification'), 'not_started')}
        self.write(base + '/state.json', json.dumps(state))
        self.write(base + '/input.md', 'Subject')
        self.write(base + '/log.md', 'Log')
        if lifecycle == 'closed':
            self.write(base + '/outcome.md', 'Done')
        return base

    def test_absent_current_and_instructions_exact(self):
        for instructions in ('', 'α\r\n' * 5000):
            self.write('.hai_env/config/agent_instructions.md', instructions)
            before = self.snapshot()
            result = context.context(self.root)
            self.assertTrue(result['ok'], result)
            self.assertEqual(result['activity_context']['status'], 'absent')
            self.assertEqual(result['agent_instructions']['text'], instructions)
            self.assertEqual(before, self.snapshot())

    def test_current_and_bounded_continuity(self):
        base = self.activity()
        self.write(base + '/log.md', 'z' * 8000 + 'end')
        result = context.context(self.root)
        self.assertTrue(result['ok'], result)
        current = result['activity_context']
        self.assertEqual(current['status'], 'current')
        self.assertEqual(current['path'], base)
        log = current['continuity']['log.md']
        self.assertTrue(log['truncated'])
        self.assertTrue(log['text'].endswith('end'))
        self.assertLessEqual(len(log['text'].encode()), log['limit_bytes'])

    def test_invalid_states_and_required_records(self):
        base = self.activity()
        statepath = self.root / base / 'state.json'
        original = statepath.read_text(encoding='utf-8')
        for bad in ('{', '{"activity_id": 1}', original.replace('"active"', '"unknown"')):
            with self.subTest(bad=bad):
                statepath.write_text(bad, encoding='utf-8')
                self.assertEqual(context.context(self.root)['activity_context']['status'], 'invalid')
        statepath.write_text(original, encoding='utf-8')
        (self.root / base / 'log.md').unlink()
        result = context.context(self.root)
        self.assertEqual(result['activity_context']['status'], 'invalid')
        self.assertTrue(result['activity_context']['issues'])
        self.assertEqual(result['state_status'], 'valid')

    def test_unreadable_required_record(self):
        self.activity()
        from discovery import _regular
        def denied(path):
            if path.name == 'log.md':
                raise PermissionError('unreadable fixture')
            return _regular(path)
        with patch('discovery._regular', side_effect=denied):
            result = context.context(self.root)
        self.assertEqual(result['activity_context']['status'], 'invalid')
        self.assertIn('unreadable fixture', str(result['issues']))

    def test_multiple_active_and_duplicate_id(self):
        self.activity()
        self.activity('other', ident='a8b99ccb-d0b0-4836-aa3b-69ecc05cd8c1')
        result = context.context(self.root)
        self.assertEqual(result['activity_context']['status'], 'invalid')
        self.assertIn('Multiple active', str(result['issues']))
        self.activity('other', lifecycle='closed')
        result = context.context(self.root)
        self.assertIn('Duplicate Activity ID', str(result['issues']))

    def test_unsafe_links(self):
        base = self.activity()
        log = self.root / base / 'log.md'
        log.unlink()
        try:
            log.symlink_to(self.root / '.hai_env/config/agent_instructions.md')
        except (OSError, NotImplementedError):
            self.skipTest('symbolic links unavailable')
        result = context.context(self.root)
        self.assertEqual(result['activity_context']['status'], 'invalid')
        self.assertTrue(result['activity_context']['issues'])

    def test_duplicate_uuid_alternate_representation(self):
        self.activity()
        self.activity('20261104_032120_old-record',
                      ident='5F99FF6B793B475EB1848618582598EF', lifecycle='closed')
        self.assertIn('Duplicate Activity ID', str(context.context(self.root)['issues']))

    def test_closed_archive_name_and_closure_timestamp(self):
        name = '20261104_032120_old-record'
        base = self.activity(name, lifecycle='closed')
        self.assertEqual(context.context(self.root)['activity_context']['status'], 'absent')
        folder = self.root / base
        for invalid in ('old-record', '20261104_032121_old-record', '20261104_032120_old-record_01'):
            renamed = folder.with_name(invalid)
            folder.rename(renamed)
            self.assertEqual(context.context(self.root)['activity_context']['status'], 'invalid')
            renamed.rename(folder)

    def test_optional_canonical_artifact_link_rejected(self):
        base = self.activity()
        optional = self.root / base / 'analysis.md'
        try:
            optional.symlink_to(self.root / '.hai_env/config/agent_instructions.md')
        except (OSError, NotImplementedError):
            self.skipTest('symbolic links unavailable')
        self.assertEqual(context.context(self.root)['activity_context']['status'], 'invalid')

    def test_hardlinked_record_rejected(self):
        base = self.activity()
        record = self.root / base / 'log.md'
        alias = self.root / 'alias.md'
        try:
            os.link(record, alias)
        except OSError:
            self.skipTest('hard links unavailable')
        result = context.context(self.root)
        self.assertEqual(result['activity_context']['status'], 'invalid')
        self.assertTrue(result['activity_context']['issues'])

    def test_independent_failures_and_missing_instructions(self):
        self.activity()
        self.write('.hai_env/config/model_profiles.json', '{broken')
        (self.root / '.hai_env/config/agent_instructions.md').unlink()
        result = context.context(self.root)
        self.assertFalse(result['ok'])
        self.assertEqual(result['instructions_status'], 'missing')
        self.assertEqual(result['state_status'], 'valid')
        self.assertEqual(result['profiles']['status'], 'invalid')
        self.assertEqual(result['activity_context']['status'], 'current')
        self.assertGreaterEqual(len(result['issues']), 2)
        self.write('.hai_env/config/state.json', '{broken')
        self.assertEqual(context.context(self.root)['activity_context']['status'], 'unverified')

    def test_production_cli_no_mutation(self):
        self.activity()
        before = self.snapshot()
        proc = subprocess.run([sys.executable, '-B', str(SCRIPT), '--workspace', str(self.root)],
                              capture_output=True, text=True, cwd=self.root)
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertEqual(json.loads(proc.stdout)['activity_context']['status'], 'current')
        self.assertEqual(before, self.snapshot())


if __name__ == '__main__':
    unittest.main()
