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
        for state in ({}, {'integrations': {}}, {'integrations': {'other': {'token': 'never-output'}}}):
            before = copy.deepcopy(state)
            result = validate_settings(state)
            self.assertTrue(result['ok'])
            self.assertEqual(result['integrations']['git']['status'], 'unconfigured')
            self.assertEqual(result['integrations']['github']['status'], 'unconfigured')
            self.assertNotIn('never-output', json.dumps(result))
            self.assertEqual(state, before)

    def test_independent_switches_and_invalid_entries(self):
        for invalid in (None, True, 1, 'true', [], {}, {'enabled': 1}, {'enabled': 'false'}):
            with self.subTest(invalid=invalid):
                state = {'integrations': {'git': {'enabled': True}, 'github': invalid}}
                result = validate_settings(state)
                self.assertFalse(result['ok'])
                self.assertTrue(result['integrations']['git']['enabled'])
                self.assertEqual(result['integrations']['github']['status'], 'invalid')
        result = validate_settings({'integrations': {'git': None, 'github': {'enabled': True}}})
        self.assertTrue(result['integrations']['github']['enabled'])
        self.assertFalse(result['integrations']['git']['enabled'])

    def test_malformed_container_is_not_absent(self):
        for value in (None, False, [], 'value', 0):
            result = validate_settings({'integrations': value})
            self.assertFalse(result['ok'])
            self.assertEqual(result['integrations']['git']['status'], 'invalid')
            self.assertEqual(result['integrations']['github']['status'], 'invalid')

    def test_automatic_push_never_implies_live_readiness(self):
        for enabled in (False, True):
            for push in (False, True):
                result = validate_settings({'integrations': {'git': {'enabled': enabled, 'auto_push': {'enabled': push}}}})
                policy = result['integrations']['git']['auto_push']
                self.assertEqual(policy['enabled'], enabled and push)
                self.assertEqual(policy['readiness'], 'not_checked')
                self.assertEqual(result['ok'], enabled or not push)
        for malformed in (None, True, [], {}, {'enabled': 1}):
            result = validate_settings({'integrations': {'git': {'enabled': True, 'auto_push': malformed}}})
            self.assertTrue(result['integrations']['git']['enabled'])
            self.assertEqual(result['integrations']['git']['auto_push']['status'], 'invalid')

    def test_unknown_data_preserved_even_with_isolated_errors(self):
        state = {'state_format_version': 2, 'unknown': ['α'], 'integrations': {'git': {'enabled': True, 'unknown': {'keep': 7}}, 'github': {}, 'other': False}}
        before = copy.deepcopy(state)
        validate_settings(state)
        self.assertEqual(state, before)


class FileAndCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / '.hai_env').mkdir()
        self.state = self.root / '.hai_env/state.json'

    def tearDown(self):
        self.tmp.cleanup()

    def test_unicode_crlf_and_read_only_cli_without_site_packages(self):
        self.state.write_bytes('{\r\n"integrations":{"git":{"enabled":true}},"проба":"да"\r\n}\r\n'.encode())
        before = self.state.read_bytes()
        proc = subprocess.run([sys.executable, '-I', '-S', '-B', str(SCRIPT), '--workspace', str(self.root)], capture_output=True, text=True, check=False)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertTrue(result['integrations']['git']['enabled'])
        self.assertEqual(self.state.read_bytes(), before)
        self.assertEqual(sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob('*')), ['.hai_env', '.hai_env/state.json'])

    def test_duplicate_json_and_wrong_root_are_failures(self):
        for text in ('{"integrations":{},"integrations":{}}', '{"integrations":{"git":{"enabled":true,"enabled":false}}}', '[]', '{"bad":NaN}'):
            self.state.write_text(text)
            with self.assertRaises((Invalid, ValueError)):
                check(self.root)

    def test_missing_or_directory_state(self):
        with self.assertRaises((Invalid, OSError)):
            check(self.root)
        self.state.mkdir()
        with self.assertRaises((Invalid, OSError)):
            check(self.root)

    def test_escaping_and_dangling_symlinks(self):
        outside = self.root.parent / (self.root.name + '-outside.json')
        outside.write_text('{}')
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        try:
            self.state.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable on this platform')
        with self.assertRaises(Invalid):
            check(self.root)
        self.state.unlink()
        self.state.symlink_to(self.root / 'absent.json')
        with self.assertRaises(Invalid):
            check(self.root)

    def test_reserved_alias(self):
        target = self.root / '.hai_env/agent_instructions.md'
        target.write_text('{}')
        try:
            self.state.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable on this platform')
        with self.assertRaises(Invalid):
            check(self.root)


if __name__ == '__main__':
    unittest.main()
