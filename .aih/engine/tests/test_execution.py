import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from security import Workspace
from execution import ExecutionError, confinement_diagnostics, run_process, run_registered_test, validate_test_contract
from adapters import validate_profile, resolve_profile, execute, ManualHandoff
from storage import Store

BASE = Path(__file__).resolve().parents[3] / "tests" / "runtime-fixtures"

@unittest.skipUnless(confinement_diagnostics()["available"], "Enforced Linux Landlock/seccomp unavailable")
class ExecutionTests(unittest.TestCase):
    def setUp(self):
        BASE.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="execution-", dir=BASE)
        self.base = Path(self.temp.name)
        for name in ("home", "backend", "reference", "outside"):
            (self.base / name).mkdir()
        self.home = self.base / "home"
        (self.home / "src").mkdir()
        (self.home / "build").mkdir()
        (self.home / ".aih").mkdir()
        (self.home / ".aih_product").mkdir()
        self.workspace = Workspace(self.home, {"revision": 1, "roots": [
            {"id": "home", "path": str(self.home), "access": "read-write"},
            {"id": "backend", "path": str(self.base / "backend"), "access": "read-write"},
            {"id": "reference", "path": str(self.base / "reference"), "access": "read-only"}]})

    def tearDown(self):
        self.temp.cleanup()

    def run_code(self, code, **kwargs):
        return run_process([sys.executable, "-B", "-c", code], self.workspace, **kwargs)

    def test_real_process_union_read_only_scope_core_and_outside_denials(self):
        paths = [self.base / "outside" / "bad", self.base / "reference" / "bad", self.home / ".aih" / "bad",
                 self.home / ".aih_product" / "bad", self.home / "src" / "bad"]
        code = 'from pathlib import Path\nimport json\nresults=[]\n'
        for path in paths:
            code += f'try:\n Path({str(path)!r}).write_text("bad")\n results.append("BREACH")\nexcept PermissionError:\n results.append("denied")\n'
        code += f'Path({str(self.home / "build" / "good")!r}).write_text("allowed")\nprint(json.dumps(results))\n'
        result = self.run_code(code, write_scope=["home:build"])
        self.assertEqual(result["returncode"], 0, result["stderr"])
        self.assertEqual(json.loads(result["stdout"]), ["denied"] * len(paths))
        self.assertEqual((self.home / "build" / "good").read_text(), "allowed")
        self.assertTrue(all(not path.exists() for path in paths))

    def test_real_process_writes_two_disjoint_roots_and_reads_reference(self):
        (self.base / "backend" / "build").mkdir()
        (self.base / "reference" / "rules.txt").write_text("reference knowledge")
        code = f'from pathlib import Path\nPath({str(self.home / "build" / "front.txt")!r}).write_text("front")\nPath({str(self.base / "backend" / "build" / "back.txt")!r}).write_text("back")\nprint(Path({str(self.base / "reference" / "rules.txt")!r}).read_text())'
        result = self.run_code(code, write_scope=["home:build", "backend:build"])
        self.assertEqual(result["returncode"], 0, result["stderr"])
        self.assertEqual(result["stdout"].strip(), "reference knowledge")
        self.assertEqual((self.base / "backend" / "build" / "back.txt").read_text(), "back")

    def test_confined_owner_helper_reads_with_shared_lock_and_no_state_mutation(self):
        from workflow import Engine
        core_cli = Path(__file__).resolve().parents[1] / "cli.py"
        (self.home / ".aih" / "engine").mkdir()
        (self.home / ".aih" / "engine" / "cli.py").write_text("# fixture installation marker\n")
        engine = Engine(self.home)
        engine.initialize()
        owner = "OP-fixture-owner-helper"
        state = engine.store.read("state.yaml")
        state["owner"] = {"id": owner, "status": "running", "action": "analyze"}
        engine.store.write("state.yaml", state)
        before = engine.store.hash("state.yaml")
        result = run_process([sys.executable, "-B", str(core_cli), "--home", str(self.home), "helper", "inventory", "--owner", owner],
                             Workspace(self.home), operation_id="OP-fixture-helper-child", timeout=20)
        self.assertEqual(result["returncode"], 0, result["stderr"] + result["stdout"])
        parsed = json.loads(result["stdout"])
        self.assertTrue(parsed["read_only"])
        self.assertEqual(parsed["owner_id"], owner)
        self.assertEqual(engine.store.hash("state.yaml"), before)

    def test_events_remove_reasoning_and_actual_credential_values(self):
        credential = "opaque-value-without-provider-prefix"
        code = 'import json,os\nprint(json.dumps({"type":"item.completed","item":{"type":"reasoning","text":"private chain"}}))\nprint(os.environ["EXAMPLE_TOKEN"])'
        result = self.run_code(code, env={"EXAMPLE_TOKEN": credential})
        self.assertEqual(result["returncode"], 0, result["stderr"])
        self.assertNotIn("private chain", result["stdout"])
        self.assertNotIn(credential, result["stdout"])
        self.assertIn("redacted credential", result["stdout"])

    def test_host_auth_reference_opaque_values_are_never_persisted(self):
        credential = "opaque-refresh-value-with-no-provider-prefix"
        credential_file = self.base / "outside" / "auth.json"
        credential_file.write_text(json.dumps({"refresh_token": credential}))
        code = f'import json\nfrom pathlib import Path\nprint(json.loads(Path({str(credential_file)!r}).read_text())["refresh_token"])'
        result = self.run_code(code, credential_paths=[str(credential_file)])
        self.assertEqual(result["returncode"], 0, result["stderr"])
        self.assertNotIn(credential, result["stdout"])
        self.assertIn("redacted credential", result["stdout"])

    def test_unregistered_read_and_metadata_changes_denied(self):
        outside = self.base / "outside" / "secret"
        outside.write_text("private")
        code = f'import os\nfrom pathlib import Path\ntry:\n Path({str(outside)!r}).read_text()\n raise RuntimeError("read escape")\nexcept PermissionError: pass\ntry:\n os.chmod({str(outside)!r},0o600)\n raise RuntimeError("metadata escape")\nexcept PermissionError: pass\nprint("denied")'
        result = self.run_code(code)
        self.assertEqual(result["returncode"], 0, result["stderr"])
        self.assertEqual(result["stdout"].strip(), "denied")

    def test_descendant_inherits_scope_and_cannot_detach(self):
        target = self.base / "outside" / "bad"
        nested = f'from pathlib import Path; Path({str(target)!r}).write_text("bad")'
        code = f'import subprocess,sys,os\np=subprocess.run([sys.executable,"-B","-c",{nested!r}])\nassert p.returncode != 0\ntry:\n os.setsid()\n raise RuntimeError("detached")\nexcept PermissionError: pass\nprint("confined")'
        result = self.run_code(code)
        self.assertEqual(result["returncode"], 0, result["stderr"])
        self.assertFalse(target.exists())

    def test_safe_stop_kills_descendants_and_records_identity(self):
        stop = threading.Event()
        threading.Timer(0.3, stop.set).start()
        result = self.run_code('import subprocess,sys,time\nsubprocess.Popen([sys.executable,"-c","import time;time.sleep(90)"])\nprint("started",flush=True)\ntime.sleep(90)', stop_event=stop, operation_id="stop-test")
        self.assertEqual(result["status"], "stopped")
        self.assertTrue(result["termination_confirmed"])
        self.assertTrue(Store(self.home).read("ledger/operations/stop-test/process.json")["termination_confirmed"])

    def test_leader_exit_reconciles_orphan_child(self):
        start = time.monotonic()
        result = self.run_code('import subprocess,sys\nsubprocess.Popen([sys.executable,"-c","import time;time.sleep(90)"])\nprint("leader exiting")')
        self.assertLess(time.monotonic() - start, 10)
        self.assertTrue(result["termination_confirmed"])

    def test_network_denied_without_contract(self):
        result = self.run_code('import socket\ntry:\n socket.socket()\n raise RuntimeError("network escape")\nexcept PermissionError: print("denied")')
        self.assertEqual(result["returncode"], 0, result["stderr"])

    def test_registered_required_suite_runs_in_declared_environment(self):
        (self.home / "src" / "test_example.py").write_text('import unittest\nclass Example(unittest.TestCase):\n def test_equal(self): self.assertEqual(1+1,2)\n')
        contract = {"id": "example", "workspace_revision": 1, "runner": "python-unittest", "environment": "python3",
                    "working_directory": "home:", "source_paths": ["home:src"], "write_paths": ["home:build"],
                    "prerequisites": [], "isolation": "landlock", "cleanup": "retain", "authorization": "request-implementation", "required": True}
        result = run_registered_test(contract, self.workspace, ["home:build"], authorization="request-implementation")
        self.assertEqual(result["outcome"], "passed", result)
        self.assertTrue(result["content_unchanged"])
        self.assertFalse((self.home / "src" / "__pycache__").exists())
        contract["workspace_revision"] = 0
        with self.assertRaises(ExecutionError):
            run_registered_test(contract, self.workspace, ["home:build"])

    def test_expected_build_outputs_do_not_make_required_suite_stale(self):
        (self.home / "src" / "test_output.py").write_text('import unittest\nfrom pathlib import Path\nclass Output(unittest.TestCase):\n def test_output(self):\n  Path("build/report.txt").write_text("verified")\n  self.assertTrue(True)\n')
        contract = {"id": "outputs", "workspace_revision": 1, "runner": "python-unittest", "environment": "python3",
                    "working_directory": "home:", "source_paths": ["home:src"], "write_paths": ["home:build"],
                    "prerequisites": [], "isolation": "landlock", "cleanup": "retain", "authorization": "request-implementation", "required": True}
        result = run_registered_test(contract, self.workspace, ["home:build"], authorization="request-implementation")
        self.assertEqual(result["outcome"], "passed", result)
        self.assertTrue(result["content_unchanged"])
        self.assertEqual(result["tests_collected"], 1)
        self.assertTrue((self.home / "build" / "report.txt").exists())
        contract["source_paths"] = ["home:"]
        with self.assertRaises(ExecutionError):
            validate_test_contract(contract, self.workspace, ["home:build"])

    def test_empty_required_unittest_suite_is_blocked(self):
        contract = {"id": "empty", "workspace_revision": 1, "runner": "python-unittest", "environment": "python3",
                    "working_directory": "home:", "source_paths": ["home:src"], "write_paths": [],
                    "prerequisites": [], "isolation": "landlock", "cleanup": "retain", "authorization": "request-implementation", "required": True}
        result = run_registered_test(contract, self.workspace, [], authorization="request-implementation")
        self.assertEqual(result["outcome"], "blocked")
        self.assertEqual(result["tests_collected"], 0)

    def test_declared_write_cannot_enroll_read_only_root(self):
        with self.assertRaises(Exception):
            self.run_code('print("unreachable")', write_scope=["reference:"])
        with self.assertRaises(ExecutionError):
            self.run_code('print("unreachable")', write_scope=["home:"])


class AdapterTests(unittest.TestCase):
    def test_profile_precedence_and_no_silent_fallback(self):
        config = {"profiles": {"default": {"adapter": "manual"}, "analysis": {"adapter": "manual"}, "chosen": {"adapter": "manual"}},
                  "default_profile": "default", "capability_profiles": {"analyze": "analysis"}}
        self.assertEqual(resolve_profile(config, "other")["id"], "default")
        self.assertEqual(resolve_profile(config, "analyze")["id"], "analysis")
        self.assertEqual(resolve_profile(config, "analyze", "chosen")["id"], "chosen")
        with self.assertRaises(ExecutionError):
            resolve_profile(config, "analyze", "missing")
        with self.assertRaises(ExecutionError):
            validate_profile({"adapter": "codex", "arguments": "--dangerously-bypass-approvals-and-sandbox"})
        with self.assertRaises(ExecutionError):
            validate_profile({"adapter": "fixture"})

    def test_durable_manual_handoff_requires_confirmation_and_reconciliation(self):
        BASE.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=BASE) as home:
            store = Store(home)
            helper = ManualHandoff(store)
            record = helper.prepare({"id": "op"}, {"operation_id": "op", "scope": [], "workspace_revision": 1,
                         "workspace": Workspace(home).registry, "initiating_instruction": "Review", "profile": "manual"}, "Review the registered product only.")
            self.assertEqual(record["status"], "prepared_reserved")
            waiting = helper.stop(record)
            self.assertFalse(waiting["released"])
            reconciled = helper.stop(waiting, never_started=True, reconciliation={"complete": True, "changed_files": []})
            self.assertTrue(reconciled["released"])
            self.assertTrue(Store(home).read(f"ledger/operations/op/{record['id']}.json")["released"])

if __name__ == "__main__":
    unittest.main()
