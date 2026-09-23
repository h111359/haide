"""Fault injection for explicit recovery without resetting authoritative state."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contracts import Error, digest, now
from workflow import Engine
from storage import StorageError

BASE = Path(__file__).resolve().parents[3] / "tests" / "runtime-fixtures"


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        BASE.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="recovery-", dir=BASE)
        self.home = Path(self.temp.name)
        (self.home / ".aih/engine").mkdir(parents=True)
        (self.home / ".aih/engine/cli.py").write_text("# isolated installation marker\n")
        self.engine = Engine(self.home)
        self.store = self.engine.store

    def tearDown(self):
        self.temp.cleanup()

    def interrupted(self, action, target="state.yaml"):
        original = self.store.write
        crashed = False
        def fail_once(path, value, **kwargs):
            nonlocal crashed
            if path == target and not crashed:
                crashed = True
                raise OSError("injected process interruption")
            return original(path, value, **kwargs)
        with patch.object(self.store, "write", side_effect=fail_once):
            with self.assertRaisesRegex(OSError, "injected"):
                action()

    def recover(self, **payload):
        return self.engine.dispatch("recover", {"apply": True, **payload}, background=False)

    def archive_fixture(self, renamed=True):
        self.engine.initialize()
        rid, opid = "CR-recovery-fixture", "OP-close-fixture"
        state = self.store.read("state.yaml")
        state["active_request"] = rid
        self.store.write("state.yaml", state)
        record = {"schema_version": "1.0", "id": rid, "title": "Retained closure", "summary": "Partial fixture",
                  "status": "cancelled", "phase": "outcome", "created": now(), "closed": now(),
                  "scope_revision": 1, "workspace_revision": 1, "tasks": [], "blockers": [],
                  "closure": {"by": "Framework user", "operation": opid, "outcome": "cancelled", "gates": []}}
        source, destination = "change_requests/active/" + rid, "change_requests/history/" + rid
        self.store.write(source + "/request.yaml", record)
        entry = {"id": rid, "title": record["title"], "status": "cancelled", "location": destination, "workspace_revision": 1}
        catalog = {"schema_version": "1.0", "requests": [entry]}
        journal = {"id": opid, "source": source, "destination": destination, "status": "prepared", "catalog": catalog,
                   "workspace_revision": 1, "request_sha256": digest(record)}
        path = "ledger/archives/" + opid + ".yaml"
        self.store.write(path, journal)
        self.engine._load()
        if renamed:
            self.engine.workspace.mkdir("home:.aih_product/change_requests/history", internal=True)
            self.engine.workspace.move("home:.aih_product/" + source, "home:.aih_product/" + destination, internal=True)
        return rid, source, destination, path, journal

    def test_interrupted_initialization_recovers_without_reset_or_automatic_setup(self):
        (self.home / "product.txt").write_text("human source")
        self.interrupted(self.engine.initialize)
        self.assertFalse(self.engine.initialized())
        with self.assertRaisesRegex(Error, "incomplete"):
            self.engine.initialize()
        result = self.recover()
        self.assertEqual(result["status"], "completed")
        self.assertTrue(result["initialized"])
        self.assertEqual(self.store.read("state.yaml")["setup"]["status"], "pending")
        self.assertIsNone(self.store.read("state.yaml")["owner"])
        self.assertEqual((self.home / "product.txt").read_text(), "human source")
        self.assertTrue(self.engine.initialize()["reused"])

    def test_pending_information_state_commit_is_not_invalidated_by_recovery_owner(self):
        self.engine.initialize()
        after = self.store.read("state.yaml")
        after["revision"] += 1
        after["current_state_notices"] = ["NOTICE-retained"]
        self.interrupted(lambda: self.store.transaction({"output/recovery.md": "retained evidence", "state.yaml": after}))
        result = self.recover()
        self.assertEqual(result["status"], "completed")
        self.assertEqual(self.store.read("state.yaml"), after)
        self.assertEqual(self.store.read("output/recovery.md", raw=True), "retained evidence")

    def test_invalid_existing_state_is_preserved(self):
        self.engine.initialize()
        self.store.write("state.yaml", "{invalid content")
        before = self.store.hash("state.yaml")
        with self.assertRaises((Error, StorageError)):
            self.recover()
        self.assertEqual(self.store.hash("state.yaml"), before)

    def test_existing_owner_requires_stop_before_recovery(self):
        self.engine.initialize()
        state = self.store.read("state.yaml")
        state["owner"] = {"id": "OP-retained-owner", "status": "running", "pid": None}
        self.store.write("state.yaml", state)
        with self.assertRaisesRegex(Error, "Stop"):
            self.recover()
        self.assertEqual(self.store.read("state.yaml"), state)

    def test_archive_rename_before_catalog_and_state_commit_reconciles(self):
        rid, source, destination, path, journal = self.archive_fixture()
        result = self.recover()
        self.assertEqual(result["status"], "completed", result)
        self.assertEqual(result["archives"][0]["status"], "committed")
        self.assertIsNone(self.store.read("state.yaml")["active_request"])
        self.assertEqual(self.store.read("change_requests/catalog.yaml")["requests"][0]["id"], rid)
        self.assertFalse(self.store.path(source).exists())
        self.assertTrue(self.store.path(destination).exists())
        self.assertEqual(self.recover()["archives"], [])

    def test_archive_prepared_before_rename_finishes_same_home_move(self):
        rid, source, destination, path, journal = self.archive_fixture(renamed=False)
        result = self.recover()
        self.assertEqual(result["status"], "completed", result)
        self.assertFalse(self.store.path(source).exists())
        self.assertTrue(self.store.path(destination).exists())

    def test_archive_info_commit_after_stop_preserves_new_idle_state(self):
        rid, source, destination, path, journal = self.archive_fixture()
        before = self.store.read("state.yaml")
        before["owner"] = {"id": journal["id"], "status": "running"}
        self.store.write("state.yaml", before)
        after = copy.deepcopy(before)
        after["active_request"] = None
        journal["status"] = "committed"
        self.interrupted(lambda: self.store.transaction({"change_requests/catalog.yaml": journal["catalog"], path: journal, "state.yaml": after}))
        stopped = copy.deepcopy(before)
        stopped["owner"] = None
        stopped["revision"] += 1
        stopped["current_state_notices"] = ["NOTICE-stop-preserved"]
        self.store.write("state.yaml", stopped)
        result = self.recover()
        self.assertEqual(result["status"], "completed", result)
        self.assertEqual(result["recovery"][0]["status"], "reconciled")
        final = self.store.read("state.yaml")
        self.assertIsNone(final["owner"])
        self.assertIsNone(final["active_request"])
        self.assertEqual(final["current_state_notices"], ["NOTICE-stop-preserved"])
        self.assertGreater(final["revision"], stopped["revision"])

    def test_archive_conflicting_human_record_is_preserved(self):
        rid, source, destination, path, journal = self.archive_fixture()
        record = self.store.read(destination + "/request.yaml")
        record["title"] = "human correction"
        self.store.write(destination + "/request.yaml", record)
        result = self.recover()
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(self.store.read("state.yaml")["active_request"], rid)
        self.assertEqual(self.store.read(destination + "/request.yaml")["title"], "human correction")

    def test_dispatch_exception_after_rename_does_not_recreate_active_record(self):
        rid, source, destination, path, journal = self.archive_fixture(renamed=False)
        self.store.workspace.unlink(self.store._ref(path), internal=True)
        original = self.engine.workspace.move
        from security import Workspace
        real_move = Workspace.move
        def rename_then_fail(workspace, src, dst, **kwargs):
            real_move(workspace, src, dst, **kwargs)
            raise OSError("injected after archive rename")
        with patch.object(Engine, "_completion_gates", return_value=[]), patch.object(Workspace, "move", new=rename_then_fail):
            with self.assertRaisesRegex(OSError, "after archive"):
                self.engine.dispatch("close", {"outcome": "cancelled"}, background=False)
        self.assertFalse(self.store.path(source).exists())
        self.assertTrue(self.store.path(destination).exists())
        self.assertEqual(self.store.read("state.yaml")["active_request"], rid)
        self.assertEqual(self.recover()["status"], "completed")

    def test_old_workspace_permission_cannot_be_restored(self):
        self.engine.initialize()
        old = self.store.read("state.yaml")
        self.interrupted(lambda: self.store.transaction({"output/old.md": "old", "state.yaml": {**old, "revision": 2}}))
        registry = self.store.read("ledger/workspaces/1.yaml")
        registry["revision"] = 2
        self.store.write("ledger/workspaces/2.yaml", registry)
        self.store.write("state.yaml", {**old, "revision": 3, "workspace_revision": 2})
        with self.assertRaisesRegex(Error, "older workspace"):
            self.recover()
        self.assertEqual(self.store.read("state.yaml")["workspace_revision"], 2)


if __name__ == "__main__":
    unittest.main()
