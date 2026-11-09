"""Temporary-workspace migration rehearsal, preservation and interruption fixtures."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from migrate_git_configuration import ConfigurationError, migrate
from validate_git_configuration import check


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / '.hai_env/config').mkdir(parents=True)
        self.source = self.root / '.hai_env/config/state.json'
        self.destination = self.root / '.hai_env/config/agents/git-manager.json'
        self.state = {'state_format_version': 2, 'activities': {'location': '.hai_env/activities'},
                      'features': {'custom': ['keep'], 'specification': {'enabled': False, 'location': '.hai_env/specifications'}, 'chronicles': {'enabled': False}},
                      'integrations': {'git': {'enabled': True, 'auto_push': {'enabled': False, 'unknown': 4}, 'future': ['α']},
                                       'github': {'enabled': True, 'unknown': {'preserve': None}}, 'sibling': {'enabled': True}},
                      'other': {'nested': ['unchanged']}}
        self.source.write_text(json.dumps(self.state), encoding='utf-8')
        self.original = self.source.read_bytes()

    def apply(self, **kwargs):
        plan = migrate(self.root, **kwargs)
        return migrate(self.root, apply=True, expected_source_sha256=plan['source_sha256'], **kwargs)

    def test_rehearsal_has_no_writes(self):
        plan = migrate(self.root)
        self.assertEqual(plan['mode'], 'dry_run')
        self.assertEqual(plan['source_state_format_version'], self.state['state_format_version'])
        self.assertEqual(self.source.read_bytes(), self.original)
        self.assertFalse(self.destination.parent.exists())

    def test_preserves_complete_owned_subtrees_and_every_unrelated_value(self):
        result = self.apply()
        after = copy.deepcopy(self.state)
        owned = {key: after['integrations'].pop(key) for key in ('git', 'github')}
        self.assertEqual(json.loads(self.source.read_text()), after)
        self.assertEqual(json.loads(self.destination.read_text()), {'config_format_version': 1, 'settings': owned})
        self.assertEqual((self.root / result['backups'][0]).read_bytes(), self.original)
        self.assertEqual(result['completed'][-1], 'readback_verified')
        status = check(self.root)['integrations']
        self.assertTrue(status['git']['enabled'])
        self.assertTrue(status['github']['enabled'])
        self.assertFalse(status['git']['auto_push']['enabled'])
        self.assertEqual(status['git']['auto_push']['readiness'], 'not_checked')
        with self.assertRaises(ConfigurationError):
            migrate(self.root)

    def test_conflicts_rejected_and_identical_destination_needs_explicit_resolution(self):
        self.destination.parent.mkdir(parents=True)
        self.destination.write_text('{"config_format_version":1,"settings":{}}')
        with self.assertRaises(ConfigurationError):
            migrate(self.root)
        with self.assertRaises(ConfigurationError):
            migrate(self.root, accept_identical=True)
        owned = {key: self.state['integrations'][key] for key in ('git', 'github')}
        self.destination.write_text(json.dumps({'config_format_version': 1, 'settings': owned}))
        with self.assertRaises(ConfigurationError):
            migrate(self.root)
        before = self.destination.read_bytes()
        result = self.apply(accept_identical=True)
        self.assertEqual(self.destination.read_bytes(), before)
        self.assertEqual(len(result['backups']), 2)

    def test_changed_source_and_missing_plan_hash_stop_before_writes(self):
        with self.assertRaises(ConfigurationError):
            migrate(self.root, apply=True)
        plan = migrate(self.root)
        self.source.write_text(self.source.read_text() + '\n')
        with self.assertRaises(ConfigurationError):
            migrate(self.root, apply=True, expected_source_sha256=plan['source_sha256'])
        self.assertFalse(self.destination.exists())

    def test_partial_failure_retains_old_authority_and_verified_backup(self):
        def fail(stage):
            if stage == 'after_destination_write':
                raise OSError('injected interruption')
        with patch('migrate_git_configuration._checkpoint', fail):
            with self.assertRaisesRegex(ConfigurationError, 'partial_result'):
                self.apply()
        self.assertEqual(self.source.read_bytes(), self.original)
        self.assertTrue(self.destination.exists())
        backups = list((self.root / '.hai_env/config/migration-backups').glob('*-state.json'))
        self.assertEqual(backups[0].read_bytes(), self.original)
        with self.assertRaises(ConfigurationError):
            migrate(self.root)

    def test_changed_input_after_destination_write_stops_removal(self):
        def change(stage):
            if stage == 'after_destination_write':
                self.source.write_text(self.source.read_text() + '\n')
        with patch('migrate_git_configuration._checkpoint', change):
            with self.assertRaisesRegex(ConfigurationError, 'changed'):
                self.apply()
        self.assertIn('git', json.loads(self.source.read_text())['integrations'])

    def test_malformed_legacy_data_is_not_repaired(self):
        for invalid in ('{"integrations":{},"integrations":{}}', '[]', '{"bad":NaN}'):
            self.source.write_text(invalid)
            with self.assertRaises(ConfigurationError):
                migrate(self.root)
        self.state['integrations']['git']['enabled'] = 1
        self.source.write_text(json.dumps(self.state))
        with self.assertRaises(ConfigurationError):
            migrate(self.root)
        self.assertFalse(self.destination.exists())

    def test_symlink_destination_refused(self):
        self.destination.parent.mkdir(parents=True)
        other = self.root / 'other.json'
        other.write_text('{}')
        try:
            self.destination.symlink_to(other)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable')
        with self.assertRaises(ConfigurationError):
            migrate(self.root)
        self.assertEqual(other.read_text(), '{}')

    def test_hardlinked_source_and_destination_refused(self):
        alias = self.root / 'source-alias.json'
        try:
            os.link(self.source, alias)
        except (OSError, NotImplementedError):
            self.skipTest('Hardlinks unavailable')
        with self.assertRaises(ConfigurationError):
            migrate(self.root)
        alias.unlink()
        self.destination.parent.mkdir(parents=True)
        other = self.root / 'other.json'
        other.write_text('{}')
        os.link(other, self.destination)
        with self.assertRaises(ConfigurationError):
            migrate(self.root)

    def test_core_location_alias_and_invalid_complete_state_refused(self):
        for location in ('.hai_env/config', '.hai_env/config/migration-backups'):
            self.state['activities']['location'] = location
            self.source.write_text(json.dumps(self.state))
            with self.assertRaises(ConfigurationError):
                migrate(self.root)
        del self.state['activities']
        self.source.write_text(json.dumps(self.state))
        with self.assertRaises(ConfigurationError):
            migrate(self.root)

    def test_unsupported_core_versions_fail_without_writes(self):
        for version in (1, 999, True):
            self.state['state_format_version'] = version
            self.source.write_text(json.dumps(self.state))
            with self.assertRaises(ConfigurationError):
                migrate(self.root)
            self.assertFalse(self.destination.exists())


class FormatThreeMigrationTests(MigrationTests):
    """Run the complete guarded extraction suite against current core schema."""

    def setUp(self):
        super().setUp()
        self.state['state_format_version'] = 3
        del self.state['features']['specification']
        self.source.write_text(json.dumps(self.state), encoding='utf-8')
        self.original = self.source.read_bytes()


if __name__ == '__main__':
    unittest.main()
