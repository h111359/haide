"""Stage the ownership split without installing, registering or reading user records."""
from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'.hai/tools/agents'))
sys.path.insert(0, str(ROOT/'.hai/tools/startup'))
from agent_tools import audit, read_definition, validate
import startup_check


NAMES = ('business-analyst', 'solution-architect', 'software-developer',
         'quality-assurance')


def copy_core(target):
    # Simulate the final retired layout even while the real owner finishes retirement.
    def ignore(directory, names):
        if Path(directory).name == 'agents' and Path(directory).parent.name == '.hai':
            return ['activity-manager'] if 'activity-manager' in names else []
        return ['__pycache__'] if '__pycache__' in names else []
    shutil.copytree(ROOT/'.hai', target/'.hai', ignore=ignore)


def catalogue(root, origin, names):
    rows = ['# Test catalogue', '', '| Agent | Selection guide | Definition |', '| --- | --- | --- |']
    for name in names:
        definition = read_definition(root/origin/'agents'/name/'SKILL.md', workspace=root)
        text = definition['description'].replace('&', '&amp;').replace('\\', '&#92;').replace('|', '&#124;')
        rows.append(f'| `{name}` | {text} | [SKILL.md]({name}/SKILL.md) |')
    path = root/origin/'agents/catalogue.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(rows)+'\n', encoding='utf-8')


def snapshot(root):
    return {str(path.relative_to(root)): path.read_bytes()
            for path in root.rglob('*') if path.is_file()}


class CoreIsolationTests(unittest.TestCase):
    def test_enabled_recording_without_optional_owner_does_not_break_core_or_discover_records(self):
        with tempfile.TemporaryDirectory(prefix='hai-core-only-') as directory:
            stage = Path(directory).resolve()
            copy_core(stage)
            env = stage/'.hai_env'
            env.mkdir()
            state = json.loads((stage/'.hai/templates/state.json').read_text(encoding='utf-8'))
            state['state_format_version'] = 3
            state['features']['chronicles']['enabled'] = True
            (env/'config').mkdir()
            (env/'config/state.json').write_text(json.dumps(state), encoding='utf-8')
            (env/'config/agent_instructions.md').write_text('', encoding='utf-8')
            # Existing corrupt record data must not be scanned by startup validation.
            record = env/'activities/00000000_000000_active'
            record.mkdir(parents=True)
            (record/'state.json').write_text('not a record; not read at startup', encoding='utf-8')
            before = snapshot(stage)
            result = startup_check.check(stage)
            self.assertTrue(result['ok'], result)
            self.assertEqual(result['environment'], 'valid')
            self.assertTrue(result['features']['chronicles']['enabled'])
            self.assertEqual(result['agents'], [])
            self.assertFalse((env/'agents/codex-chronicle-manager').exists())
            self.assertEqual(snapshot(stage), before)

    def test_bootstrap_and_recording_have_separate_owners_and_prerequisites(self):
        runtime = (ROOT/'.hai/tools/runtime/recording.py').read_text(encoding='utf-8')
        self.assertIn('unsupported', runtime)
        self.assertIn('unverified', runtime)

    def test_live_core_and_consumers_have_no_retired_owner_routing(self):
        paths = [ROOT/'README.md', ROOT/'INSTALL.md', ROOT/'.hai/start.md']
        for directory in (ROOT/'.hai/concepts', ROOT/'.hai/conventions'):
            paths.extend(directory.rglob('*.md'))
        for path in paths:
            with self.subTest(path=path):
                text = path.read_text(encoding='utf-8')
                self.assertNotRegex(text, r'(?i)activity-manager')


@unittest.skipUnless((ROOT/'hai_agents_library/agents').is_dir(), 'repository source-package fixtures unavailable in core-only distribution')
class SourceStagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='hai-role-migration-')
        cls.stage = Path(cls.temp.name).resolve()
        copy_core(cls.stage)
        source = ROOT/'hai_agents_library/agents'
        cls.source_before = snapshot(source)
        shutil.copytree(source, cls.stage/'.hai_env/agents', ignore=shutil.ignore_patterns('__pycache__'))
        names = sorted(path.name for path in (cls.stage/'.hai_env/agents').iterdir() if path.is_dir())
        catalogue(cls.stage, '.hai_env', names)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_complete_staged_packages_validate_and_audit_with_library_absent(self):
        self.assertFalse((self.stage/'hai_agents_library').exists())
        result = audit(self.stage)
        self.assertTrue(result['ok'], result)
        self.assertTrue(set(NAMES).issubset({agent['name'] for agent in result['agents']}))
        for name in NAMES:
            self.assertFalse((self.stage/'.hai/agents'/name).exists())
            self.assertTrue(validate(self.stage, f'.hai_env/agents/{name}/SKILL.md')['ok'])
        self.assertEqual(snapshot(ROOT/'hai_agents_library/agents'), self.source_before)

    def test_portable_supporting_links_resolve_after_complete_installation(self):
        missing = []
        # Source-package fixture syntax is literal only inside fenced examples.
        for base in (self.stage/'.hai', self.stage/'.hai_env/agents'):
            for path in base.rglob('*.md'):
                text = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)
                for target in re.findall(r'\[[^\]\n]+\]\(([^)\s]+)\)', text):
                    if target.startswith(('http:', 'https:', '#', 'mailto:')):
                        continue
                    target = target.split('#', 1)[0]
                    if target and not (path.parent/target).exists():
                        missing.append(f'{path.relative_to(self.stage)} -> {target}')
        self.assertEqual(missing, [])

    def test_domain_owners_return_record_evidence_and_preserve_specialist_ownership(self):
        for name in NAMES[:4]:
            skill = (self.stage/f'.hai_env/agents/{name}/SKILL.md').read_text(encoding='utf-8')
            self.assertIn('MUST NOT invoke or coordinate other agents', skill)
            self.assertIn('rather than mutate Activity records', skill)
        package = self.stage/'.hai_env/agents/software-developer'
        skill = (package/'SKILL.md').read_text(encoding='utf-8')
        procedure_paths = re.findall(r'\]\((procedures/[^)]+\.md)\)', skill)
        self.assertTrue(procedure_paths, 'developer must index its execution procedures')
        developer = '\n'.join((package/path).read_text(encoding='utf-8') for path in procedure_paths)
        self.assertRegex(developer, r'original (?:Activity |runtime )?implementation-start (?:marker|evidence)')
        self.assertTrue((self.stage/'.hai/tools/hai.py').is_file())
        self.assertFalse((self.stage/'.hai/agents').exists())


if __name__ == '__main__':
    unittest.main()
