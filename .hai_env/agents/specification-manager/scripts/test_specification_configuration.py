"""Isolated HAI settings fixtures; no product trees or live configuration writes."""
import copy
import json
import os
import stat
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import specification_configuration as settings


class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='hai-spec-config-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.state = self.root / '.hai_env/state.json'
        self.state.parent.mkdir()
        self.core = {'state_format_version': 3, 'activities': {'location': '.hai_env/activities'},
                     'features': {'chronicles': {'enabled': True, 'record_every_prompts': 5}}}
        self.state.write_text(json.dumps(self.core), encoding='utf-8')
        template = self.root / '.hai/agents/environment-manager/templates/state.json'
        template.parent.mkdir(parents=True)
        template.write_bytes((settings._INSTALLED_ROOT / '.hai/agents/environment-manager/templates/state.json').read_bytes())
        (self.root / '.hai_env/agent_instructions.md').write_text('', encoding='utf-8')
        self.path = self.root / settings.RELATIVE

    def save(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data), encoding='utf-8')

    def files(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def test_missing_defaults_are_read_only_and_no_tree_is_created(self):
        before = self.files()
        result = settings.check(self.root)
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['settings'], {'enabled': False, 'location': '.hai_env/specifications'})
        self.assertEqual(result['status'], 'defaulted')
        self.assertEqual(self.files(), before)
        self.assertFalse((self.root / '.hai_env/specifications').exists())

    def test_enabled_and_root_validation_even_while_disabled(self):
        for location in ('../outside', '.hai_env/config', '.hai_env/activities', '.hai', '.git',
                         '.hai_env/model_profiles.json', '.hai_env/agent_instructions.md', '/tmp/spec', 'C:/spec'):
            with self.subTest(location=location):
                self.save({'config_format_version': 1, 'settings': {'enabled': False, 'location': location}})
                self.assertFalse(settings.check(self.root)['ok'])
        for value in (1, 'false', None, []):
            self.save({'config_format_version': 1, 'settings': {'enabled': value}})
            self.assertFalse(settings.check(self.root)['ok'])

    def test_strict_json_versions_and_existing_file_type(self):
        self.path.parent.mkdir(parents=True)
        for value in ('[]', '{"config_format_version":true,"settings":{}}',
                      '{"config_format_version":1,"settings":{},"settings":{}}',
                      '{"config_format_version":1,"settings":{"enabled":NaN}}'):
            self.path.write_text(value)
            self.assertFalse(settings.check(self.root)['ok'])
        (self.root / 'not-a-directory').write_text('preserve')
        self.save({'config_format_version': 1, 'settings': {'location': 'not-a-directory'}})
        self.assertFalse(settings.check(self.root)['ok'])

    def test_setup_preserves_unknown_core_and_content_without_enablement(self):
        data = {'config_format_version': 1, 'extra': {'secret': 'not-output'},
                'settings': {'enabled': False, 'location': '.hai_env/specifications', 'other': ['keep']}}
        self.save(data)
        before_core = self.state.read_bytes()
        (self.root / 'product').mkdir()
        content = self.root / 'product/content.md'
        content.write_text('unchanged product')
        candidate = settings.configure(self.root, location='product')
        self.assertTrue(candidate['ok'], candidate)
        self.assertNotIn('not-output', json.dumps(candidate))
        self.assertEqual(json.loads(self.path.read_text()), data)
        result = settings.configure(self.root, location='product', apply=True,
                                    expected_source=candidate['source_sha256'])
        self.assertTrue(result['ok'], result)
        changed = copy.deepcopy(data); changed['settings']['location'] = 'product'
        self.assertEqual(json.loads(self.path.read_text()), changed)
        self.assertEqual(self.state.read_bytes(), before_core)
        self.assertEqual(content.read_text(), 'unchanged product')
        self.assertFalse(result['settings']['enabled'])

    def test_absent_creation_requires_reviewed_hash_and_preserves_defaults(self):
        with self.assertRaises(settings.ConfigurationError):
            settings.configure(self.root, enabled=False, apply=True, expected_source='wrong')
        self.assertFalse(self.path.exists())
        result = settings.configure(self.root, enabled=False, apply=True, expected_source='absent')
        self.assertTrue(result['ok'], result)
        self.assertFalse((self.root / '.hai_env/specifications').exists())
        self.assertEqual(json.loads(self.path.read_text())['settings'], {'enabled': False})

    def test_changed_inputs_and_partial_readback_are_reported(self):
        self.save({'config_format_version': 1, 'settings': {'enabled': False}})
        candidate = settings.configure(self.root, enabled=True)
        self.path.write_text('{"config_format_version":1,"settings":{"enabled":false},"new":1}')
        with self.assertRaises(settings.ConfigurationError):
            settings.configure(self.root, enabled=True, apply=True, expected_source=candidate['source_sha256'])
        candidate = settings.configure(self.root, enabled=True)
        original = settings.check
        calls = 0
        def fail_after_write(workspace):
            nonlocal calls
            calls += 1
            result = original(workspace)
            if calls == 3:
                result['ok'] = False
            return result
        with patch.object(settings, 'check', side_effect=fail_after_write):
            result = settings.configure(self.root, enabled=True, apply=True,
                                        expected_source=candidate['source_sha256'])
        self.assertFalse(result['ok'])
        self.assertEqual(result['stages'], ['owner_configuration_written'])
        self.assertTrue(json.loads(self.path.read_text())['settings']['enabled'])

    def test_unsafe_core_source_is_rejected_before_dependency_bytes_are_read(self):
        outside = self.root.parent / (self.root.name + '-outside-state.json')
        outside.write_text(json.dumps(self.core))
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        self.state.unlink()
        try:
            self.state.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable')
        read_bytes = Path.read_bytes
        reads = []
        def guarded(path):
            reads.append(path)
            if path == self.state or path == outside:
                raise AssertionError('Unsafe source bytes read before safe assurance')
            return read_bytes(path)
        with patch.object(Path, 'read_bytes', guarded):
            with self.assertRaises(settings.ConfigurationError):
                settings.configure(self.root, enabled=False)
        self.assertNotIn(self.state, reads)
        self.assertFalse(self.path.exists())

    def test_changed_target_alias_or_core_after_staging_stops_replacement(self):
        for change in ('alias', 'core'):
            with self.subTest(change=change):
                self.state.write_text(json.dumps(self.core))
                if self.path.is_symlink():
                    self.path.unlink()
                self.save({'config_format_version': 1, 'settings': {'enabled': False}})
                candidate = settings.configure(self.root, enabled=True)
                original = settings.tempfile.NamedTemporaryFile
                owner = self
                class SwapAfterStage:
                    def __init__(self, *args, **kwargs):
                        self.context = original(*args, **kwargs)
                    def __enter__(self):
                        return self.context.__enter__()
                    def __exit__(self, *args):
                        result = self.context.__exit__(*args)
                        if change == 'alias':
                            owner.path.unlink()
                            owner.path.symlink_to(owner.state)
                        else:
                            changed = copy.deepcopy(owner.core)
                            changed['features']['chronicles']['record_every_prompts'] = 7
                            owner.state.write_text(json.dumps(changed))
                        return result
                with patch.object(settings.tempfile, 'NamedTemporaryFile', SwapAfterStage):
                    result = settings.configure(self.root, enabled=True, apply=True,
                                                expected_source=candidate['source_sha256'])
                self.assertFalse(result['ok'], result)
                self.assertEqual(result['stages'], [])
                self.assertIn('temporary_path', result)
                self.assertNotIn('owner_configuration_written', result['stages'])
                if change == 'core':
                    self.assertFalse(json.loads(self.path.read_text())['settings']['enabled'])

    @unittest.skipIf(os.name == 'nt', 'POSIX file mode behavior')
    def test_existing_file_mode_is_preserved(self):
        self.save({'config_format_version': 1, 'settings': {'enabled': False}})
        self.path.chmod(0o640)
        candidate = settings.configure(self.root, enabled=True)
        result = settings.configure(self.root, enabled=True, apply=True,
                                    expected_source=candidate['source_sha256'])
        self.assertTrue(result['ok'], result)
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o640)

    def test_core2_requires_migration_before_setup(self):
        self.core['state_format_version'] = 2
        self.core['features']['specification'] = {'enabled': False, 'location': '.hai_env/specifications'}
        self.state.write_text(json.dumps(self.core))
        with self.assertRaises(settings.ConfigurationError):
            settings.configure(self.root, enabled=False)
        self.assertFalse(self.path.exists())

    def test_aliases_and_isolated_cli_do_not_write(self):
        target = self.root / 'spec-target'
        target.mkdir()
        alias = self.root / 'spec-alias'
        try:
            alias.symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable')
        self.save({'config_format_version': 1, 'settings': {'location': 'spec-alias'}})
        # A contained directory alias can be read safely; tree audit retains its stricter no-links contract.
        result = settings.check(self.root)
        self.assertTrue(result['ok'], result)
        before = self.files()
        proc = subprocess.run([sys.executable, '-I', '-S', '-B', str(Path(settings.__file__).resolve()),
                               '--workspace', str(self.root)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(self.files(), before)
        self.path.unlink()
        self.path.symlink_to(self.state)
        self.assertFalse(settings.check(self.root)['ok'])


if __name__ == '__main__':
    unittest.main()
