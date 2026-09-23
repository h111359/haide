"""No fixture or product initialization precedes maintenance admission."""
import contextlib
import io
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contracts import CORE
from workflow import Engine
from cli import main, maintenance_admission
from storage import StorageError

BASE = CORE.parent / "tests/runtime-fixtures"


class MaintenanceAdmissionTests(unittest.TestCase):
    def setUp(self):
        BASE.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="cli-admission-", dir=BASE)
        self.home = Path(self.temp.name)
        (self.home / ".aih/engine").mkdir(parents=True)
        (self.home / ".aih/engine/cli.py").write_text("# isolated installation marker")
        self.engine = Engine(self.home)

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, command):
        error = io.StringIO()
        with contextlib.redirect_stderr(error), contextlib.redirect_stdout(io.StringIO()):
            code = main(["--home", str(self.home), command])
        return code, error.getvalue()

    def test_busy_owner_blocks_demo_before_fixture_creation(self):
        self.engine.initialize()
        state = self.engine.store.read("state.yaml")
        state["owner"] = {"id": "OP-existing", "status": "running"}
        self.engine.store.write("state.yaml", state)
        with patch("demo.demonstrate") as demonstrate:
            code, message = self.run_cli("demo")
        self.assertEqual(code, 2)
        self.assertIn("busy", message)
        demonstrate.assert_not_called()
        self.assertFalse((self.home / ".aih_runtime").exists())
        self.assertEqual(self.engine.store.read("state.yaml"), state)

    def test_open_request_blocks_test_before_runner_or_fixture_creation(self):
        self.engine.initialize()
        state = self.engine.store.read("state.yaml")
        state["active_request"] = "CR-retained"
        self.engine.store.write("state.yaml", state)
        with patch("unittest.defaultTestLoader.discover") as discover:
            code, message = self.run_cli("test")
        self.assertEqual(code, 2)
        self.assertIn("open request", message)
        discover.assert_not_called()
        self.assertFalse((self.home / ".aih_runtime").exists())

    def test_uninitialized_home_reservation_creates_no_product_state_and_blocks_init(self):
        with maintenance_admission(self.engine):
            self.assertFalse(self.engine.store.root.exists())
            with self.assertRaises(StorageError):
                self.engine.initialize()
            self.assertFalse(self.engine.store.root.exists())
        self.assertFalse(self.engine.store.root.exists())
        self.engine.initialize()
        self.assertTrue(self.engine.initialized())

    def test_operational_action_is_rejected_instead_of_waiting_for_maintenance(self):
        self.engine.initialize()
        entered, release = threading.Event(), threading.Event()
        failures = []
        def maintain():
            try:
                with maintenance_admission(Engine(self.home)):
                    entered.set()
                    release.wait(3)
            except Exception as exc:
                failures.append(exc)
                entered.set()
        thread = threading.Thread(target=maintain)
        thread.start()
        try:
            self.assertTrue(entered.wait(2))
            self.assertEqual(failures, [])
            with self.assertRaises(StorageError):
                self.engine.dispatch("save-draft", {"lane": "change", "text": "must not queue"})
        finally:
            release.set()
            thread.join(3)
        self.assertEqual(self.engine.store.read("input/current.md", raw=True), "")

    def test_acknowledged_receipt_replay_remains_passive_during_exclusive_checkpoint(self):
        self.engine.initialize()
        payload = {"lane": "change", "text": "retained accepted draft"}
        first = self.engine.dispatch("save-draft", payload, idempotency_key="same-action")
        entered, release = threading.Event(), threading.Event()
        def checkpoint():
            with Engine(self.home).store.lock():
                entered.set()
                release.wait(3)
        thread = threading.Thread(target=checkpoint)
        thread.start()
        try:
            self.assertTrue(entered.wait(2))
            repeated = self.engine.dispatch("save-draft", payload, idempotency_key="same-action")
            self.assertEqual(repeated["operation_id"], first["operation_id"])
            self.assertTrue(repeated["reused"])
            with self.assertRaises(StorageError):
                self.engine.dispatch("save-draft", payload, idempotency_key="different-action")
        finally:
            release.set()
            thread.join(3)
