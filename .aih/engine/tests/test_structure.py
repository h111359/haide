"""Structural validation detects unsafe external files without repairing them."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contracts import CORE, digest, dumps
from workflow import Engine
from demo_fixtures import documentation_result
import documentation

BASE = CORE.parent / "tests/runtime-fixtures"


class StructureTests(unittest.TestCase):
    def setUp(self):
        BASE.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="structure-", dir=BASE)
        self.home = Path(self.temp.name)
        shutil.copytree(CORE, self.home / ".aih", ignore=shutil.ignore_patterns("__pycache__"))
        (self.home / "app.py").write_text("def greet(name):\n    return 'Hi ' + name\n")
        self.engine = Engine(self.home)
        self.engine.initialize()

    def tearDown(self):
        self.temp.cleanup()

    def check(self, name):
        return self.engine.validate_all()["validation"][name]

    def test_expected_layout_information_and_schema_checks_are_read_only(self):
        self.engine.store.write("instructions/human.md", "Human-owned instruction text")
        before = {path.relative_to(self.home).as_posix(): digest(path.read_bytes()) for path in (self.home / ".aih_product").rglob("*") if path.is_file()}
        result = self.engine.validate_all()
        for name in ("organization", "inert_product_state", "state", "config", "accepted_authority", "profiles", "test_inventory", "documentation", "runtime_records"):
            self.assertTrue(result["validation"][name]["valid"], (name, result["validation"][name]))
        after = {path.relative_to(self.home).as_posix(): digest(path.read_bytes()) for path in (self.home / ".aih_product").rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_extra_overlapping_immediate_directory_and_environment_are_reported(self):
        (self.home / ".aih_product/skills").mkdir()
        (self.home / ".aih_product/tmp/.venv").mkdir()
        result = self.engine.validate_all()
        self.assertFalse(result["valid"])
        self.assertFalse(result["validation"]["organization"]["valid"])
        self.assertFalse(result["validation"]["inert_product_state"]["valid"])
        self.assertTrue((self.home / ".aih_product/skills").exists())
        self.assertTrue(any(gap["code"] == "framework-gap" for gap in result["framework_gaps"]))

    def test_executable_bytecode_binary_and_aliased_state_never_execute(self):
        temp = self.home / ".aih_product/tmp"
        (temp / "script.py").write_text("raise RuntimeError('must never execute')")
        (temp / "cached.pyc").write_bytes(b"bytecode")
        (temp / "renamed.txt").write_bytes(b"\x7fELFunsafe")
        (temp / "external.txt").symlink_to(self.home / "app.py")
        record = self.check("inert_product_state")
        self.assertFalse(record["valid"])
        self.assertEqual({item["path"] for item in record["problems"]}, {"tmp/script.py", "tmp/cached.pyc", "tmp/renamed.txt", "tmp/external.txt"})
        self.assertTrue((temp / "script.py").exists())

    def test_malformed_retained_operation_and_current_state_have_named_errors(self):
        self.engine.store.write("ledger/operations/OP-invalid/operation.yaml", {"id": "OP-invalid"})
        self.assertFalse(self.check("runtime_records")["valid"])
        self.engine.store.write("state.yaml", {"schema_version": "1.0"})
        self.assertFalse(self.check("state")["valid"])
        self.assertEqual(self.engine.store.read("state.yaml"), {"schema_version": "1.0"})

    def test_invalid_profile_and_required_suite_are_actionable_without_execution(self):
        config = self.engine.store.read("ledger/configurations/current.yaml")
        config["profiles"]["bad"] = {"adapter": "arbitrary-shell", "command": "must-not-run"}
        self.engine.store.write("ledger/configurations/current.yaml", config)
        self.engine.store.write("documentation/test_inventory.yaml", {"schema_version": "1.0", "suites": [{"id": "required-broken", "required": True}]})
        self.assertFalse(self.check("profiles")["valid"])
        suites = self.check("test_inventory")
        self.assertFalse(suites["valid"])
        self.assertEqual(suites["suites"][0]["id"], "required-broken")

    def test_catalog_links_must_match_canonical_balanced_documentation_tree(self):
        documentation.apply_proposal(self.engine.store, self.engine.workspace, documentation_result(self.engine), self.engine.workspace.inventory(), "OP-structure-fixture")
        self.assertTrue(self.check("documentation")["valid"])
        catalog = self.engine.store.read("documentation/index.yaml")
        catalog["children"][0]["path"] = "leaves/missing.md"
        self.engine.store.write("documentation/index.yaml", catalog)
        result = self.check("documentation")
        self.assertFalse(result["valid"])
        self.assertEqual(result["code"], "documentation-navigation")

    def test_unexpected_core_file_is_not_ignored_by_integrity_validation(self):
        installed = self.home / ".aih"
        files = {path.relative_to(installed).as_posix(): digest(path.read_bytes()) for path in installed.rglob("*") if path.is_file() and path.name != "integrity.json"}
        (installed / "integrity.json").write_text(dumps({"schema_version": "1.0", "version": "1.0.0", "files": files}))
        (self.home / ".aih/engine/unexpected.txt").write_text("unreviewed core material")
        result = self.check("core_integrity")
        self.assertFalse(result["valid"])
        self.assertEqual(result["code"], "core-integrity")
        self.assertIn("engine/unexpected.txt", result["details"]["unexpected"])


if __name__ == "__main__":
    unittest.main()
