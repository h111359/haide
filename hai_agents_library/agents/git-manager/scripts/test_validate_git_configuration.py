"""Fixtures require no Git executable, remote, credentials or live-state writes."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_git_configuration import Invalid, check, validate_settings

SCRIPT = Path(__file__).with_name('validate_git_configuration.py')


class SavedPolicyTests(unittest.TestCase):
    def test_missing_settings_and_unknown_values_remain_unchanged(self):
        for settings in ({}, {'git': {}}, {'other': {'token': 'never-output'}}):
            before = copy.deepcopy(settings)
            result = validate_settings(settings)
            self.assertTrue(result['ok'])
            self.assertEqual(result['integrations']['git']['status'], 'unconfigured')
            self.assertEqual(result['integrations']['github']['status'], 'unconfigured')
            self.assertNotIn('never-output', json.dumps(result))
            self.assertEqual(settings, before)

    def test_independent_switches_and_invalid_entries(self):
        for invalid in (None, True, 1, 'true', [], {'enabled': 1}, {'enabled': 'false'}):
            with self.subTest(invalid=invalid):
                result = validate_settings({'git': {'enabled': True}, 'github': invalid})
                self.assertFalse(result['ok'])
                self.assertTrue(result['integrations']['git']['enabled'])
                self.assertEqual(result['integrations']['github']['status'], 'invalid')
        result = validate_settings({'git': None, 'github': {'enabled': True}})
        self.assertTrue(result['integrations']['github']['enabled'])
        self.assertFalse(result['integrations']['git']['enabled'])

    def test_malformed_container_is_not_absent(self):
        for value in (None, False, [], 'value', 0):
            with self.assertRaises(Invalid):
                validate_settings(value)

    def test_automatic_push_never_implies_live_readiness(self):
        for enabled in (False, True):
            for push in (False, True):
                result = validate_settings({'git': {'enabled': enabled, 'auto_push': {'enabled': push}}})
                policy = result['integrations']['git']['auto_push']
                self.assertEqual(policy['enabled'], enabled and push)
                self.assertEqual(policy['readiness'], 'not_checked')
                self.assertEqual(result['ok'], enabled or not push)
        for malformed in (None, True, [], {'enabled': 1}):
            result = validate_settings({'git': {'enabled': True, 'auto_push': malformed}})
            self.assertTrue(result['integrations']['git']['enabled'])
            self.assertEqual(result['integrations']['git']['auto_push']['status'], 'invalid')
        result = validate_settings({'git': {'auto_push': {'enabled': True}}, 'github': {'enabled': True}})
        self.assertFalse(result['integrations']['git']['auto_push']['enabled'])
        self.assertTrue(result['integrations']['github']['enabled'])

    def test_unknown_data_is_not_returned_or_changed(self):
        settings = {'git': {'enabled': True, 'unknown': {'keep': 7}}, 'github': {}, 'other': ['α']}
        before = copy.deepcopy(settings)
        result = validate_settings(settings)
        self.assertEqual(settings, before)
        self.assertNotIn('unknown', json.dumps(result))


class FileAndCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.path = self.root / '.hai_env/config/agents/git-manager.json'
        self.path.parent.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def save(self, settings):
        self.path.write_text(json.dumps({'config_format_version': 1, 'settings': settings}), encoding='utf-8')

    def test_unicode_crlf_and_read_only_cli_without_site_packages(self):
        self.path.write_bytes('{\r\n"config_format_version":1,"settings":{"git":{"enabled":true}},"проба":"да"\r\n}\r\n'.encode())
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        proc = subprocess.run([sys.executable, '-I', '-S', '-B', str(SCRIPT), '--workspace', str(self.root)], capture_output=True, text=True, check=False)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(json.loads(proc.stdout)['integrations']['git']['enabled'])
        self.assertEqual({str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}, before)

    def test_duplicate_json_malformed_envelope_and_wrong_version_fail(self):
        for value in ('{"settings":{},"settings":{}}', '[]', '{"bad":NaN}', '{"config_format_version":true,"settings":{}}', '{"config_format_version":2,"settings":{}}', '{"config_format_version":1,"settings":null}'):
            self.path.write_text(value)
            with self.assertRaises((Invalid, ValueError)):
                check(self.root)

    def test_missing_defaults_and_invalid_core_are_independent(self):
        (self.root / '.hai_env/config/state.json').write_text('{malformed')
        result = check(self.root)
        self.assertTrue(result['ok'])
        self.assertEqual(result['configuration_status'], 'defaulted')
        self.save({'github': {'enabled': True}})
        self.assertTrue(check(self.root)['integrations']['github']['enabled'])
        self.path.unlink()
        (self.root / '.hai_env/config/state.json').write_text('{"integrations":{"git":{"enabled":true}}}')
        self.assertFalse(check(self.root)['integrations']['git']['enabled'])
        self.path.mkdir()
        with self.assertRaises((Invalid, OSError)):
            check(self.root)

    def test_escaping_dangling_and_reserved_aliases(self):
        outside = self.root.parent / (self.root.name + '-outside.json')
        outside.write_text('{}')
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        reserved = self.root / '.hai_env/config/agent_instructions.md'
        reserved.write_text('{}')
        for target in (outside, self.root / 'absent.json', reserved):
            try:
                self.path.symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest('Symlinks unavailable on this platform')
            with self.assertRaises(Invalid):
                check(self.root)
            self.path.unlink()


if __name__ == '__main__':
    unittest.main()
