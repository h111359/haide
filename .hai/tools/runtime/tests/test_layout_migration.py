"""Real relocation, safety, preservation and failure behavior in disposable roots."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(TOOLS))
from runtime import environment, layout_migration as migration
from environment_paths import STATE, INSTRUCTIONS, PROFILES, LEGACY


class LayoutMigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='hai-layout-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write('.hai/templates/state.json', (TOOLS.parent / 'templates/state.json').read_bytes())
        self.state = {'state_format_version': 3, 'activities': {'location': 'work/activities'},
                      'features': {'chronicles': {'enabled': False, 'record_every_prompts': 9}},
                      'custom': {'keep': [1, 'value']}}
        self.write(LEGACY[STATE], json.dumps(self.state).encode() + b'\n')
        self.write(LEGACY[INSTRUCTIONS], b'\xef\xbb\xbfKeep these instructions.\r\n')
        self.write('.hai_env/config/agents/custom.json', b'{"keep":"untouched"}\n')
        self.write('work/activities/retained/input.md', b'existing activity evidence')
        self.request = {'provenance': {'source': 'test', 'reason': 'explicit layout migration'}}

    def write(self, relative, content):
        p = self.root / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)
        return p

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob('*') if p.is_file()}

    def call(self, apply=False):
        return environment.handle('environment/migrate-layout', self.root, self.request, apply)

    def test_preview_and_apply_preserve_bytes_and_unrelated_data(self):
        profiles = b'{"format_version":1,"models":{"light":"a","standard":"b","advanced":"c"}}\n'
        self.write(LEGACY[PROFILES], profiles)
        before = self.snapshot()
        preview = self.call()
        self.assertTrue(preview['ok'], preview)
        self.assertEqual(before, self.snapshot())
        result = self.call(True)
        self.assertTrue(result['ok'], result)
        for new, old in LEGACY.items():
            self.assertEqual((self.root / new).read_bytes(), before[old])
            self.assertFalse((self.root / old).exists())
            backup = self.root / result['result']['backup_path'] / Path(old).name
            self.assertEqual(backup.read_bytes(), before[old])
        self.assertEqual((self.root / '.hai_env/config/agents/custom.json').read_bytes(), before['.hai_env/config/agents/custom.json'])
        self.assertEqual((self.root / 'work/activities/retained/input.md').read_bytes(), before['work/activities/retained/input.md'])
        self.assertTrue(environment.startup.check(self.root)['ok'])
        self.assertEqual(self.call(True)['status'], 'unchanged')

    def test_optional_absence_and_empty_instructions(self):
        self.write(LEGACY[INSTRUCTIONS], b'')
        self.assertTrue(self.call(True)['ok'])
        self.assertFalse((self.root / PROFILES).exists())
        self.assertEqual((self.root / INSTRUCTIONS).read_bytes(), b'')

    def test_legacy_names_remain_reserved_for_content_directories(self):
        self.assertTrue(self.call(True)['ok'])
        before = self.snapshot()
        for old in LEGACY.values():
            with self.subTest(path=old), self.assertRaises(environment.startup.Invalid):
                environment.handle('environment/configure', self.root,
                                   {**self.request, 'changes': {'activities.location': old}}, True)
        self.assertEqual(before, self.snapshot())

    def test_schema_two_relocation_is_not_schema_conversion(self):
        state = copy.deepcopy(self.state)
        state['state_format_version'] = 2
        state['features']['specification'] = {'enabled': False, 'location': 'specifications'}
        self.write(LEGACY[STATE], json.dumps(state).encode())
        result = self.call(True)
        self.assertTrue(result['ok'], result)
        self.assertEqual(json.loads((self.root / STATE).read_bytes()), state)
        self.assertEqual(environment.startup.check(self.root)['state_format_version'], 2)
        self.assertFalse(environment.startup.check(self.root)['ok'])

    def test_schema_two_layout_then_schema_conversion_end_to_end(self):
        owner = TOOLS.parent.parent / '.hai_env/agents/specification-manager'
        if not owner.exists() and not owner.is_symlink():
            self.skipTest('optional Specification-manager integration unavailable in core-only distribution')
        state = copy.deepcopy(self.state)
        state['state_format_version'] = 2
        state['features']['specification'] = {'enabled': False, 'location': 'specifications', 'note': 'preserve'}
        self.write(LEGACY[STATE], json.dumps(state).encode())
        self.write('.hai_env/agents/specification-manager/SKILL.md', b'Installed fixture')
        self.write('.hai_env/agents/catalogue.md', b'| Agent | Selection guide | Definition |\n| --- | --- | --- |\n| `specification-manager` | Manage specifications. | [SKILL.md](specification-manager/SKILL.md) |\n')
        source_contract = owner / 'configuration/contract.json'
        self.write('.hai_env/agents/specification-manager/configuration/contract.json', source_contract.read_bytes())
        self.assertTrue(self.call(True)['ok'])
        result = environment.handle('environment/migrate-specification', self.root, self.request, True)
        self.assertTrue(result['ok'], result)
        self.assertTrue(environment.startup.check(self.root)['ok'])
        current = json.loads((self.root / STATE).read_bytes())
        self.assertEqual(current['custom'], state['custom'])
        owner = json.loads((self.root / '.hai_env/config/agents/specification-manager.json').read_bytes())
        self.assertEqual(owner['settings'], state['features']['specification'])

    def test_invalid_sources_block_without_writes(self):
        for old, content in ((LEGACY[STATE], b'{"state_format_version":3,"state_format_version":3}'),
                             (LEGACY[PROFILES], b'not json'),
                             (LEGACY[INSTRUCTIONS], b'\xff')):
            with self.subTest(old=old):
                before = self.snapshot()
                self.write(old, content)
                candidate = self.snapshot()
                self.assertFalse(self.call(True)['ok'])
                self.assertEqual(self.snapshot(), candidate)
                for p, data in before.items(): self.write(p, data)
                if old not in before: (self.root / old).unlink()

    def test_missing_mandatory_source_blocks(self):
        (self.root / LEGACY[INSTRUCTIONS]).unlink()
        before = self.snapshot()
        self.assertFalse(self.call(True)['ok'])
        self.assertEqual(before, self.snapshot())

    def test_mixed_layout_never_merges_even_identical_files(self):
        self.write(STATE, (self.root / LEGACY[STATE]).read_bytes())
        before = self.snapshot()
        self.assertFalse(self.call(True)['ok'])
        self.assertEqual(before, self.snapshot())

    def test_legacy_startup_and_initialization_are_blocked(self):
        self.assertFalse(environment.startup.check(self.root)['ok'])
        before = self.snapshot()
        with self.assertRaises(environment.SafetyError):
            environment.handle('environment/initialize', self.root, self.request, True)
        self.assertEqual(before, self.snapshot())

    def test_initialization_refuses_incomplete_migration_without_legacy_files(self):
        for old in LEGACY.values():
            (self.root / old).unlink(missing_ok=True)
        self.write(migration.MANIFEST, b'{"status":"in_progress"}')
        before = self.snapshot()
        with self.assertRaises(environment.SafetyError):
            environment.handle('environment/initialize', self.root, self.request, True)
        self.assertEqual(before, self.snapshot())

    def test_lock_blocks_without_discarding_lock(self):
        self.write('.hai_env/.runtime.lock', b'existing writer')
        before = self.snapshot()
        self.assertFalse(self.call(True)['ok'])
        self.assertEqual(before, self.snapshot())

    def test_links_are_rejected(self):
        source = self.root / LEGACY[STATE]
        source.rename(self.root / 'retained.json')
        try:
            source.symlink_to(self.root / 'retained.json')
        except OSError as exc:
            if getattr(exc, 'winerror', None) == 1314:
                self.skipTest('Windows symlink privilege unavailable')
            raise
        self.assertFalse(self.call(True)['ok'])
        self.assertTrue(source.is_symlink())

    def test_startup_rejects_instruction_alias_to_manifest_or_backup(self):
        self.assertTrue(self.call(True)['ok'])
        canonical = self.root / INSTRUCTIONS
        canonical.unlink()
        for relative in (migration.MANIFEST, '.hai_env/config/migration-backups/instructions.md'):
            if relative != migration.MANIFEST: self.write(relative, b'Untrusted backup content')
            try:
                canonical.symlink_to(self.root / relative)
            except OSError as exc:
                if getattr(exc, 'winerror', None) == 1314:
                    self.skipTest('Windows symlink privilege unavailable')
                raise
            result = environment.startup.check(self.root)
            self.assertFalse(result['ok'])
            self.assertEqual(result['instructions_status'], 'invalid')
            canonical.unlink()

    def test_failure_preserves_sources_backups_and_partial_destinations(self):
        original = migration.write_bytes
        def fail(root, relative, data, expected=None):
            if relative == STATE: raise OSError('injected destination failure')
            return original(root, relative, data, expected)
        with patch.object(migration, 'write_bytes', side_effect=fail):
            result = self.call(True)
        self.assertEqual(result['status'], 'partial', result)
        self.assertTrue((self.root / LEGACY[STATE]).exists())
        self.assertTrue((self.root / LEGACY[INSTRUCTIONS]).exists())
        self.assertTrue((self.root / INSTRUCTIONS).exists())
        before = self.snapshot()
        self.assertFalse(self.call(True)['ok'])
        self.assertEqual(before, self.snapshot())
        self.assertFalse(environment.startup.check(self.root)['ok'])

    def test_changed_inputs_between_inspection_and_lock_block_all_writes(self):
        original = migration._inspect
        calls = []
        def inspect(root):
            if calls: self.write(LEGACY[INSTRUCTIONS], b'new concurrent instructions')
            calls.append(True)
            return original(root)
        with patch.object(migration, '_inspect', side_effect=inspect):
            result = self.call(True)
        self.assertFalse(result['ok'])
        self.assertEqual(result['changed_files'], [])
        self.assertFalse((self.root / migration.MANIFEST).exists())

    def test_removal_failure_retains_recovery_evidence_and_blocks_startup(self):
        original = Path.unlink
        def unlink(path, *args, **kwargs):
            if path == self.root / LEGACY[STATE]: raise OSError('injected removal failure')
            return original(path, *args, **kwargs)
        with patch.object(Path, 'unlink', unlink):
            result = self.call(True)
        self.assertEqual(result['status'], 'partial')
        self.assertTrue((self.root / LEGACY[STATE]).exists())
        self.assertTrue((self.root / STATE).exists())
        self.assertFalse(environment.startup.check(self.root)['ok'])
        marker = json.loads((self.root / migration.MANIFEST).read_bytes())
        self.assertEqual(marker['status'], 'in_progress')
        backup = self.root / marker['backup_path'] / 'state.json'
        self.assertEqual(backup.read_bytes(), (self.root / LEGACY[STATE]).read_bytes())

    def test_new_layout_initialization_creates_only_mandatory_resources(self):
        fresh = self.root / 'fresh'; fresh.mkdir()
        self.write('fresh/.hai/templates/state.json', (TOOLS.parent / 'templates/state.json').read_bytes())
        result = environment.handle('environment/initialize', fresh, self.request, True)
        self.assertTrue(result['ok'], result)
        self.assertTrue((fresh / STATE).exists())
        self.assertTrue((fresh / INSTRUCTIONS).exists())
        self.assertFalse((fresh / PROFILES).exists())
        self.assertTrue(environment.startup.check(fresh)['ok'])

    def test_cli_preview_apply_and_idempotence(self):
        self.write('request.json', json.dumps(self.request).encode())
        cmd = [sys.executable, '-B', str(TOOLS / 'hai.py'), 'environment', 'migrate-layout',
               '--workspace', str(self.root), '--request', str(self.root / 'request.json')]
        preview = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
        self.assertTrue((self.root / LEGACY[STATE]).exists())
        applied = subprocess.run(cmd + ['--apply'], capture_output=True, text=True)
        self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
        again = subprocess.run(cmd + ['--apply'], capture_output=True, text=True)
        self.assertEqual(json.loads(again.stdout)['status'], 'unchanged')


if __name__ == '__main__':
    unittest.main()
