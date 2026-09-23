import base64
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from security import Workspace, BoundaryError, validate_registry, digest
from storage import Store, StorageError, ConflictError, loads, screen_sensitive, sanitize

BASE = Path(__file__).resolve().parents[3] / "tests" / "runtime-fixtures"

class SecurityTests(unittest.TestCase):
    def setUp(self):
        BASE.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="boundary-", dir=BASE)
        self.base = Path(self.temp.name)
        for name in ("home", "backend", "reference", "outside"):
            (self.base / name).mkdir()
        self.home = self.base / "home"
        self.registry = {"revision": 3, "roots": [
            {"id": "home", "path": str(self.home), "access": "read-write"},
            {"id": "backend", "path": str(self.base / "backend"), "access": "read-write"},
            {"id": "reference", "path": str(self.base / "reference"), "access": "read-only"}]}
        self.workspace = Workspace(self.home, self.registry)

    def tearDown(self):
        self.temp.cleanup()

    def test_explicit_union_scope_and_read_only(self):
        self.workspace.atomic_write("backend:src/api.py", "value=1", scope=["backend:src"])
        self.assertEqual(self.workspace.read_text("backend:src/api.py"), "value=1")
        for ref, scope in [("outside:bad", ["outside:bad"]), ("home:../outside/bad", ["home:"]),
                           ("reference:bad", ["reference:"]), ("home:.aih/engine.py", ["home:"]),
                           ("home:.aih_product/state.yaml", ["home:"]), ("backend:other.py", ["backend:src"])]:
            with self.subTest(ref=ref), self.assertRaises(BoundaryError):
                self.workspace.atomic_write(ref, "bad", scope=scope)
        with self.assertRaises(BoundaryError):
            self.workspace.atomic_write("home:unscoped", "bad")
        self.assertFalse((self.base / "outside" / "bad").exists())

    def test_duplicate_nested_alias_and_home_registration(self):
        for root in [{"id": "other", "path": str(self.home), "access": "read-only"},
                     {"id": "other", "path": str(self.home / "child"), "access": "read-write"}]:
            (self.home / "child").mkdir(exist_ok=True)
            with self.assertRaises(BoundaryError):
                validate_registry(self.home, {"revision": 1, "roots": self.registry["roots"] + [root]})
        (self.base / "alias").symlink_to(self.base / "backend", target_is_directory=True)
        with self.assertRaises(BoundaryError):
            validate_registry(self.home, {"revision": 1, "roots": [*self.registry["roots"], {"id": "alias", "path": str(self.base / "alias"), "access": "read-write"}]})
        broken = {"revision": 1, "roots": [{**self.registry["roots"][0], "access": "read-only"}]}
        with self.assertRaises(BoundaryError):
            Workspace(self.home, broken)

    def test_symlink_hardlink_and_changed_target(self):
        external = self.base / "outside" / "file"
        external.write_text("retained")
        (self.home / "escape").symlink_to(external)
        os.link(external, self.home / "hard")
        for ref in ("home:escape", "home:hard"):
            with self.assertRaises(BoundaryError):
                self.workspace.read_text(ref)
            with self.assertRaises(BoundaryError):
                self.workspace.atomic_write(ref, "bad", scope=["home:"])
        (self.home / "dir").mkdir()
        self.workspace.resolve("home:dir/target", write=True, scope=["home:dir"])
        (self.home / "dir").rmdir()
        (self.home / "dir").symlink_to(self.base / "outside", target_is_directory=True)
        with self.assertRaises((BoundaryError, OSError)):
            self.workspace.atomic_write("home:dir/target", "bad", scope=["home:dir"])
        self.assertEqual(external.read_text(), "retained")
        self.assertFalse((self.base / "outside" / "target").exists())

    def test_root_relocation_does_not_rebind_old_identity(self):
        old = self.base / "old-backend"
        (self.base / "backend").rename(old)
        (self.base / "backend").mkdir()
        with self.assertRaises(BoundaryError):
            self.workspace.resolve("backend:foo")
        with self.assertRaises(BoundaryError):
            self.workspace.resolve({"root_id": "home", "path": "x", "workspace_revision": 2})

    def test_missing_root_remains_a_problem(self):
        (self.base / "backend").rmdir()
        result = Workspace(self.home, self.registry).inventory()
        self.assertFalse(result["complete"])
        self.assertIn("backend", {p.get("root_id") for p in result["problems"]})

    def test_move_delete_validate_both_ends_and_expected_content(self):
        self.workspace.atomic_write("home:src/a", "a", scope=["home:src"])
        with self.assertRaises(BoundaryError):
            self.workspace.move("home:src/a", "reference:a", scope=["home:src", "reference:"])
        self.workspace.move("home:src/a", "backend:b", scope=["home:src", "backend:b"])
        self.assertEqual(self.workspace.read_text("backend:b"), "a")
        with self.assertRaises(BoundaryError):
            self.workspace.unlink("backend:b", scope=["backend:b"], expected_hash=digest("changed"))
        self.workspace.unlink("backend:b", scope=["backend:b"], expected_hash=digest("a"))
        self.assertFalse((self.base / "backend" / "b").exists())

    def test_state_inert_core_immutable_inventory_exclusions(self):
        self.workspace.atomic_write("home:.aih_product/state.yaml", "{}", internal=True)
        with self.assertRaises(BoundaryError):
            self.workspace.atomic_write("home:.aih_product/tmp/run.py", "print(1)", internal=True)
        before = self.workspace.fingerprint()
        self.workspace.atomic_write("home:.aih_product/tmp/data.json", "{}", internal=True)
        self.assertEqual(before, self.workspace.fingerprint())
        for suffix in ("rb", "tsx", "whl", "sqlite3"):
            with self.subTest(suffix=suffix), self.assertRaises(BoundaryError):
                self.workspace.atomic_write("home:.aih_product/tmp/artifact." + suffix, "unsafe", internal=True)
        with self.assertRaises(BoundaryError):
            self.workspace.mkdir("home:.aih_product/tmp/.venv", internal=True)
        with self.assertRaises(BoundaryError):
            self.workspace.atomic_write("home:.aih_product/tmp/site-packages/info.txt", "package", internal=True)

    def test_path_special_components(self):
        for path in ("home:/etc/passwd", "home:a/../b", "home:C:\\a", "home:foo:stream", "home:NUL", "home:x.", "home:a//b"):
            with self.subTest(path=path), self.assertRaises(BoundaryError):
                self.workspace.resolve(path)


class StorageTests(unittest.TestCase):
    def setUp(self):
        BASE.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="storage-", dir=BASE)
        self.store = Store(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_nested_lock_and_revision_transaction(self):
        with self.store.lock():
            self.store.transaction({"state.yaml": {"revision": 1}, "output/a.md": "first"})
            with Store(self.temp.name).lock():
                self.assertEqual(self.store.read("state.yaml")["revision"], 1)
        before = self.store.hash("state.yaml")
        self.store.transaction({"state.yaml": {"revision": 2}}, expected={"state.yaml": before})
        with self.assertRaises(ConflictError):
            self.store.transaction({"state.yaml": {"revision": 3}}, expected={"state.yaml": before})
        self.assertEqual(self.store.read("state.yaml")["revision"], 2)

    def test_shared_read_lock_never_creates_or_upgrades_state(self):
        with self.assertRaises(FileNotFoundError):
            with self.store.read_lock():
                pass
        self.assertFalse(self.store.root.exists())
        with self.store.lock():
            self.store.write("state.yaml", {"revision": 1})
            with self.store.read_lock():
                self.assertEqual(self.store.read("state.yaml")["revision"], 1)
        before = self.store.hash("state.yaml")
        with self.store.read_lock():
            with Store(self.temp.name).read_lock():
                self.assertEqual(self.store.hash("state.yaml"), before)
            with self.assertRaises(StorageError):
                with self.store.lock():
                    self.store.write("state.yaml", {"revision": 2})
        self.assertEqual(self.store.hash("state.yaml"), before)

    def test_journal_recovery_after_partial_write(self):
        original = self.store.write
        interrupted = False
        def crash(path, value, **kwargs):
            nonlocal interrupted
            if path == "output/b.md" and not interrupted:
                interrupted = True
                raise OSError("simulated interruption")
            return original(path, value, **kwargs)
        with patch.object(self.store, "write", side_effect=crash), self.assertRaises(OSError):
            self.store.transaction({"output/a.md": "a", "output/b.md": "b"})
        self.assertEqual(self.store.read("output/a.md", raw=True), "a")
        pending = self.store.recover()
        self.assertEqual(pending[0]["status"], "recoverable")
        self.assertEqual(self.store.recover(apply=True)[0]["status"], "committed")
        self.assertEqual(self.store.read("output/b.md", raw=True), "b")
        self.assertEqual(self.store.recover(apply=True), [])

    def test_recovery_preserves_competing_human_edit(self):
        self.store.write("output/a.md", "original")
        original = self.store.write
        def crash(path, value, **kwargs):
            if path == "output/b.md":
                raise OSError("interrupted")
            return original(path, value, **kwargs)
        with patch.object(self.store, "write", side_effect=crash), self.assertRaises(OSError):
            self.store.transaction({"output/a.md": "one", "output/b.md": "two"})
        self.store.write("output/a.md", "human edit")
        result = self.store.recover(apply=True)
        self.assertEqual(result[0]["status"], "conflict")
        self.assertEqual(self.store.read("output/a.md", raw=True), "human edit")

    def test_lock_serializes_threads(self):
        entered = threading.Event()
        finished = threading.Event()
        def worker():
            entered.set()
            with self.store.lock():
                finished.set()
        with self.store.lock():
            thread = threading.Thread(target=worker)
            thread.start()
            entered.wait(1)
            self.assertFalse(finished.wait(0.05))
        thread.join(1)
        self.assertTrue(finished.is_set())

    def test_safe_parser_sensitive_input_and_private_reasoning(self):
        for value in ('{"a":1,"a":2}', '{"a":NaN}', '!!python/object:evil {}'):
            with self.assertRaises(StorageError):
                loads(value)
        secret = "sk-proj-" + "x" * 32
        with self.assertRaises(StorageError):
            screen_sensitive(secret)
        self.assertNotIn(secret, sanitize(secret))
        self.assertEqual(sanitize({"type": "reasoning", "text": "private"}), {"type": "private_reasoning_omitted"})

    def test_temporary_cleanup_requires_reconciled_idle_owner(self):
        path = self.store.temp_create("op-1")
        self.store.write("state.yaml", {"owner": {"id": "op-1"}})
        with self.assertRaises(StorageError):
            self.store.temp_cleanup(path, operation_id="op-1", reconciled=True)
        self.store.write("state.yaml", {"owner": None})
        self.store.temp_cleanup(path, operation_id="op-1", reconciled=True)
        self.assertFalse(self.store.path(path).exists())


class AcceptedConfigurationTests(unittest.TestCase):
    def test_unsubmitted_registry_edit_cannot_expand_artifacts_or_piggyback_theme_save(self):
        from workflow import Engine
        from contracts import Error
        BASE.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="config-", dir=BASE) as temp:
            base = Path(temp)
            home, neighbor = base / "home", base / "neighbor"
            (home / ".aih" / "engine").mkdir(parents=True)
            (home / ".aih" / "engine" / "cli.py").write_text("# installation marker for fixture\n")
            neighbor.mkdir()
            (neighbor / "private.txt").write_text("outside data")
            engine = Engine(home)
            engine.initialize()
            draft = engine.store.read("config.yaml")
            draft["workspace"]["roots"].append({"id": "neighbor", "name": "Neighbor", "path": str(neighbor), "purpose": "Unsubmitted", "access": "read-write"})
            draft["profiles"]["codex"]["executable"] = "/untrusted/program"
            engine.store.write("config.yaml", draft)
            with self.assertRaises(BoundaryError):
                engine.artifact("neighbor:private.txt")
            with self.assertRaises(Error):
                engine.dispatch("save-draft", {"lane": "change", "text": "request"})
            engine.dispatch("settings-save", {"theme": "light"})
            accepted = engine.store.read("config.yaml")
            self.assertEqual([r["id"] for r in accepted["workspace"]["roots"]], ["home"])
            self.assertEqual(accepted["profiles"]["codex"]["executable"], "codex")
            self.assertEqual(accepted["theme"], "light")
            preserved = list((home / ".aih_product" / "ledger" / "configurations" / "drafts").glob("*.yaml"))
            self.assertEqual(len(preserved), 1)
            self.assertIn("/untrusted/program", preserved[0].read_text())
            self.assertEqual(engine.store.read("ledger/configurations/current.yaml"), accepted)


class WorkerStartupTests(unittest.TestCase):
    def test_quick_worker_completion_and_declared_credential_environment(self):
        from workflow import Engine
        from types import SimpleNamespace
        BASE.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="startup-", dir=BASE) as temp:
            home = Path(temp)
            (home / ".aih" / "engine").mkdir(parents=True)
            (home / ".aih" / "engine" / "cli.py").write_text("# fixture marker\n")
            engine = Engine(home)
            engine.initialize()
            engine.dispatch("profile-save", {"profile_id": "custom", "profile": {"adapter": "manual", "credential_env": ["CUSTOM_AGENT_TOKEN"]}})
            state = engine.store.read("state.yaml")
            state["owner"] = {"id": "quick-worker", "status": "starting"}
            engine.store.write("state.yaml", state)
            def instant(*args, **kwargs):
                self.assertEqual(kwargs["env"]["CUSTOM_AGENT_TOKEN"], "opaque-reference-value")
                self.assertEqual(kwargs["env"].get("HOME"), os.environ.get("HOME"))
                self.assertNotIn("LD_PRELOAD", kwargs["env"])
                state = engine.store.read("state.yaml")
                state["owner"] = None
                engine.store.write("state.yaml", state)
                return SimpleNamespace(pid=99999999, wait=lambda: 0)
            with patch.dict(os.environ, {"CUSTOM_AGENT_TOKEN": "opaque-reference-value", "LD_PRELOAD": "/untrusted.so"}), patch("workflow.subprocess.Popen", side_effect=instant):
                engine._launch("quick-worker")
            self.assertIsNone(engine.store.read("state.yaml")["owner"])
            with patch.dict(os.environ, {"AIH_MANAGED_CHILD": "1"}):
                with self.assertRaises(Exception):
                    engine._launch("nested-worker")

if __name__ == "__main__":
    unittest.main()
