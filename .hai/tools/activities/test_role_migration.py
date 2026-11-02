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
         'quality-assurance', 'codex-chronicle-manager')


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
            catalogue(stage, '.hai', ('leader', 'environment-manager'))
            env = stage/'.hai_env'
            env.mkdir()
            state = json.loads((stage/'.hai/agents/environment-manager/templates/state.json').read_text())
            state['state_format_version'] = 3
            state['features']['chronicles']['enabled'] = True
            (env/'state.json').write_text(json.dumps(state))
            (env/'agent_instructions.md').write_text('')
            # Existing corrupt record data must not be scanned by startup validation.
            record = env/'activities/00000000_000000_active'
            record.mkdir(parents=True)
            (record/'state.json').write_text('not a record; not read at startup')
            before = snapshot(stage)
            result = startup_check.check(stage)
            self.assertTrue(result['ok'], result)
            self.assertEqual(result['environment'], 'valid')
            self.assertTrue(result['features']['chronicles']['enabled'])
            self.assertEqual({agent['name'] for agent in result['agents']}, {'leader', 'environment-manager'})
            self.assertFalse((env/'agents/codex-chronicle-manager').exists())
            for name in ('leader', 'environment-manager'):
                result = validate(stage, f'.hai/agents/{name}/SKILL.md')
                self.assertTrue(result['ok'], result)
            self.assertEqual(snapshot(stage), before)

    def test_bootstrap_and_recording_have_separate_owners_and_prerequisites(self):
        profile = (ROOT/'.hai/conventions/model-profiles_conv.md').read_text()
        self.assertIn('create no model profiles, Activity records or', profile)
        self.assertIn('does not extend inherited bootstrap permission', profile)
        closure = (ROOT/'.hai/agents/environment-manager/procedures/close-or-supplement.md').read_text()
        self.assertIn('Do not invoke that specialist or execute its procedures', closure)
        self.assertIn('without source inspection, optional-owner invocation', closure)
        self.assertIn('rerun the gate immediately before mutation', closure)
        leader = (ROOT/'.hai/agents/leader/procedures/coordinate-recording.md').read_text()
        self.assertIn('fresh unique closure operation ID', leader)
        self.assertIn('Transfer sole mutation ownership', leader)
        self.assertIn('needs neither Chronicle registration nor transcript source', leader)

    def test_live_core_and_consumers_have_no_retired_owner_routing(self):
        paths = [ROOT/'README.md', ROOT/'INSTALL.md', ROOT/'.hai/start.md']
        for directory in (ROOT/'.hai/agents/leader', ROOT/'.hai/agents/environment-manager',
                          ROOT/'.hai/concepts', ROOT/'.hai/conventions'):
            paths.extend(directory.rglob('*.md'))
        for path in paths:
            with self.subTest(path=path):
                text = path.read_text()
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
        catalogue(cls.stage, '.hai', ('leader', 'environment-manager'))
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
                text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
                for target in re.findall(r'\[[^\]\n]+\]\(([^)\s]+)\)', text):
                    if target.startswith(('http:', 'https:', '#', 'mailto:')):
                        continue
                    target = target.split('#', 1)[0]
                    if target and not (path.parent/target).exists():
                        missing.append(f'{path.relative_to(self.stage)} -> {target}')
        self.assertEqual(missing, [])

    def test_domain_owners_return_record_evidence_and_preserve_specialist_ownership(self):
        for name in NAMES[:4]:
            skill = (self.stage/f'.hai_env/agents/{name}/SKILL.md').read_text()
            self.assertIn('MUST NOT invoke or coordinate other agents', skill)
            self.assertIn('rather than mutate Activity records', skill)
        developer = (self.stage/'.hai_env/agents/software-developer/procedures/perform-assigned-work.md').read_text()
        self.assertIn('original implementation-start marker', developer)
        route = (self.stage/'.hai/agents/leader/procedures/delegate-work.md').read_text()
        self.assertIn('without a more specific owner', route)
        self.assertIn('definition, specification and repository owners', route)


if __name__ == '__main__':
    unittest.main()
