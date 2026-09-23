"""Linux wrapper/direct startup, no-work menu exit and pinned-root resolution."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contracts import CORE, digest

BASE = CORE.parent / ".aih_runtime/launcher-tests"


class LauncherTests(unittest.TestCase):
    def setUp(self):
        BASE.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="home Ω & special $ ", dir=BASE)
        self.home = Path(self.temp.name)
        shutil.copytree(CORE, self.home / ".aih", ignore=shutil.ignore_patterns("__pycache__"))

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, arguments, **kwargs):
        return subprocess.run([sys.executable, "-B", str(self.home / ".aih/engine/cli.py"), *arguments], cwd=BASE, text=True, capture_output=True, timeout=20, **kwargs)

    def test_direct_help_and_root_resolution_before_initialization(self):
        result = self.run_cli(["status"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(self.home), result.stdout)
        self.assertIn('"initialized": false', result.stdout)
        help_result = self.run_cli(["help", "workspace"])
        self.assertEqual(help_result.returncode, 0)
        self.assertFalse((self.home / ".aih_product").exists())
        self.assertFalse(list((self.home / ".aih").rglob("*.pyc")))

    def test_linux_wrapper_exit_preserves_core_and_does_not_start_work(self):
        before = {p.relative_to(self.home).as_posix(): digest(p.read_bytes()) for p in (self.home / ".aih").rglob("*") if p.is_file()}
        result = subprocess.run(["/bin/sh", str(self.home / ".aih/menu.sh")], input="0\n", text=True, capture_output=True, cwd=BASE, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Existing workers and requests remain unchanged", result.stdout)
        after = {p.relative_to(self.home).as_posix(): digest(p.read_bytes()) for p in (self.home / ".aih").rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertFalse((self.home / ".aih_product").exists())

    def test_missing_linux_python_is_actionable_without_installing(self):
        result = subprocess.run(["/bin/sh", str(self.home / ".aih/menu.sh")], env={"PATH": "/aih-intentionally-unavailable"}, text=True, capture_output=True, cwd=BASE, timeout=10)
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires Python", result.stderr)
        self.assertFalse((self.home / ".aih_product").exists())

    def test_every_published_operation_has_cli_help_and_no_plan_command(self):
        from workflow import catalog
        import cli
        parser = cli.parser()
        choices = next(a for a in parser._actions if hasattr(a, "choices") and isinstance(a.choices, dict)).choices
        for operation in catalog():
            self.assertIn(operation["id"], choices)
            self.assertIn(operation["description"], choices[operation["id"]].description)
        self.assertNotIn("plan", choices)


if __name__ == "__main__":
    unittest.main()
