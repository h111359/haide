import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from security import Workspace, BoundaryError, digest
from storage import Store
from product_edits import apply_edits, reconcile, ProductEditError

BASE = Path(__file__).resolve().parents[3] / "tests" / "runtime-fixtures"

class ProductEditTests(unittest.TestCase):
    def setUp(self):
        BASE.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="edits-", dir=BASE)
        self.base = Path(self.temp.name)
        for name in ("home", "backend", "outside"):
            (self.base / name).mkdir()
        self.home = self.base / "home"
        self.registry = {"revision": 1, "roots": [{"id": "home", "path": str(self.home), "access": "read-write"},
                    {"id": "backend", "path": str(self.base / "backend"), "access": "read-write"}]}
        self.workspace, self.store = Workspace(self.home, self.registry), Store(self.home)
        self.scope = ["home:src", "backend:src"]

    def tearDown(self):
        self.temp.cleanup()

    def test_cross_root_create_modify_delete_and_idempotent_observation(self):
        edits = [{"path": "home:src/a.py", "action": "create", "content": "a=1", "expected_hash": None},
                 {"path": "backend:src/b.py", "action": "create", "content": "b=1", "expected_hash": None}]
        first = apply_edits(self.store, self.workspace, edits, self.scope, "op", "task")
        self.assertEqual(first["status"], "completed")
        self.assertFalse(first["atomic_cross_root"])
        again = apply_edits(self.store, self.workspace, edits, self.scope, "op", "task")
        self.assertEqual(len(again["changed_files"]), 2)
        apply_edits(self.store, self.workspace, [{"path": "home:src/a.py", "action": "modify", "content": "a=2", "expected_hash": digest("a=1")},
                    {"path": "backend:src/b.py", "action": "delete", "expected_hash": digest("b=1")}], self.scope, "op", "task2")
        self.assertEqual(self.workspace.read_text("home:src/a.py"), "a=2")
        self.assertFalse((self.base / "backend" / "src" / "b.py").exists())

    def test_completed_retry_never_reapplies_over_later_human_edit(self):
        self.workspace.atomic_write("home:src/a", "old", scope=self.scope)
        edit = [{"path": "home:src/a", "action": "modify", "content": "new", "expected_hash": digest("old")}]
        apply_edits(self.store, self.workspace, edit, self.scope, "op", "task")
        self.workspace.atomic_write("home:src/a", "old", scope=self.scope)
        with self.assertRaises(ProductEditError):
            apply_edits(self.store, self.workspace, edit, self.scope, "op", "task")
        self.assertEqual(self.workspace.read_text("home:src/a"), "old")

    def test_missing_review_hash_and_effect_mismatch_are_rejected_before_writes(self):
        with self.assertRaises(ProductEditError):
            apply_edits(self.store, self.workspace, [{"path": "home:src/a", "action": "create", "content": "a"}], self.scope, "op", "one")
        with self.assertRaises(ProductEditError):
            apply_edits(self.store, self.workspace, [{"path": "home:src/a", "action": "create", "content": "a", "expected_hash": None}], self.scope, "op", "two", allowed_changes={"home:src/a": "modify"})
        self.assertFalse((self.home / "src").exists())

    def test_interruption_across_roots_reconciles_partial_outcomes(self):
        edits = [{"path": "home:src/a", "action": "create", "content": "a", "expected_hash": None},
                 {"path": "backend:src/b", "action": "create", "content": "b", "expected_hash": None}]
        original = self.workspace.atomic_write
        def interrupted(ref, data, **kwargs):
            if ref.startswith("backend:"):
                raise OSError("simulated second filesystem interruption")
            return original(ref, data, **kwargs)
        with patch.object(self.workspace, "atomic_write", side_effect=interrupted), self.assertRaises(OSError):
            apply_edits(self.store, self.workspace, edits, self.scope, "op", "task")
        inspection = reconcile(self.store, self.workspace, "op", "task", self.scope)
        self.assertEqual([x["status"] for x in inspection["observations"]], ["after", "before"])
        result = reconcile(self.store, self.workspace, "op", "task", self.scope, apply=True)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(self.workspace.read_text("backend:src/b"), "b")

    def test_revoked_root_access_blocks_recovery_without_resurrecting_authority(self):
        stop = threading.Event(); stop.set()
        edits = [{"path": "backend:src/b", "action": "create", "content": "b", "expected_hash": None}]
        with self.assertRaises(ProductEditError):
            apply_edits(self.store, self.workspace, edits, self.scope, "op", "task", stop_event=stop)
        self.registry["revision"] = 2
        self.registry["roots"][1]["access"] = "read-only"
        current = Workspace(self.home, self.registry)
        with self.assertRaises(ProductEditError):
            reconcile(self.store, current, "op", "task", self.scope, apply=True)
        self.assertFalse((self.base / "backend" / "src").exists())

    def test_move_interruption_preserves_both_versions_then_reconciles(self):
        self.workspace.atomic_write("home:src/a", "moving", scope=self.scope)
        edit = [{"path": "home:src/a", "action": "move", "destination": "backend:src/b", "expected_hash": digest("moving")}]
        with patch.object(self.workspace, "unlink", side_effect=OSError("interrupted before source delete")), self.assertRaises(OSError):
            apply_edits(self.store, self.workspace, edit, self.scope, "op", "move")
        self.assertEqual(self.workspace.read_text("home:src/a"), "moving")
        self.assertEqual(self.workspace.read_text("backend:src/b"), "moving")
        observation = reconcile(self.store, self.workspace, "op", "move", self.scope)
        self.assertEqual(observation["observations"][0]["status"], "destination_written")
        reconcile(self.store, self.workspace, "op", "move", self.scope, apply=True)
        self.assertFalse((self.home / "src" / "a").exists())

    def test_human_edit_conflict_preserved_and_location_rebind_denied(self):
        self.workspace.atomic_write("home:src/a", "old", scope=self.scope)
        stop = threading.Event(); stop.set()
        edit = [{"path": "home:src/a", "action": "modify", "content": "new", "expected_hash": digest("old")}]
        with self.assertRaises(ProductEditError):
            apply_edits(self.store, self.workspace, edit, self.scope, "op", "task", stop_event=stop)
        self.workspace.atomic_write("home:src/a", "human", scope=self.scope)
        with self.assertRaises(ProductEditError):
            reconcile(self.store, self.workspace, "op", "task", self.scope, apply=True)
        self.assertEqual(self.workspace.read_text("home:src/a"), "human")

if __name__ == "__main__":
    unittest.main()
