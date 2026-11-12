"""Regression coverage for configured and invocation-owned runner work areas."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(TOOLS))
from run_tests import test_work_path
from runtime.storage import SafetyError


class TestRunnerPaths(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / '.hai_env/config').mkdir(parents=True)

    def configure(self, location):
        (self.root / '.hai_env/config/state.json').write_text(
            json.dumps({'activities': {'location': location}}), encoding='utf-8')

    def test_supported_layouts_and_nested_paths(self):
        for store in ('.hai_env/activities', 'records/activities', 'records'):
            self.configure(store)
            for suffix in ('files/test-work', 'files/test-work/nested',
                           'files/agent-invocations/reviewer/test-work/nested'):
                relative = store + '/ci/' + suffix
                self.assertEqual(test_work_path(self.root, relative), self.root / relative)
                self.assertFalse((self.root / relative).exists())

    def test_rejects_unowned_and_noncanonical_paths_without_writes(self):
        self.configure('records/activities')
        for relative in ('.hai_env/activities/ci/files/test-work',
                         'records/activities-extra/ci/files/test-work',
                         'records/activities/ci/files',
                         'records/activities/ci/files/agent-invocations/test-work',
                         'records/activities/ci/files/test-work/../config',
                         'records/activities/ci/files/test-work\\escape',
                         '.git/test-work'):
            with self.subTest(relative=relative), self.assertRaises(SafetyError):
                test_work_path(self.root, relative)
        self.assertFalse((self.root / 'records').exists())

    def test_invalid_configuration_does_not_fall_back(self):
        self.configure('../outside')
        with self.assertRaises(SafetyError):
            test_work_path(self.root, '.hai_env/activities/ci/files/test-work')

    def test_cli_runs_in_both_alternate_store_layouts(self):
        self.configure('records/activities')
        for suffix in ('files/test-work', 'files/agent-invocations/reviewer/test-work'):
            relative = 'records/activities/ci/' + suffix
            result = subprocess.run([sys.executable, '-B', str(TOOLS / 'run_tests.py'),
                                     '--workspace', str(self.root), '--work-dir', relative,
                                     '--suite', 'chronicles'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((self.root / relative / 'tmp').is_dir())
            self.assertIn('"exit_code": 0', result.stdout)
