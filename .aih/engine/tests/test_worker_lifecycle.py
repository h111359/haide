"""Independent real worker lifecycle tests; all semantic answers are synthetic.

Background Python CLI processes, subprocess ownership, confined fake-agent events,
Stop and explicit Resume are real. This is not a claim of live-model compliance.
"""
from __future__ import annotations
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contracts import Error, dumps
from execution import confinement_diagnostics, process_alive, stop_process
from demo_fixtures import clarification, documentation_result
import test_workflow as workflow_fixture


class WorkerLifecycleTests(unittest.TestCase):
    # Reuse setup/helpers only; this class does not inherit or duplicate workflow tests.
    setUpClass = workflow_fixture.WorkflowTests.setUpClass
    set_response = workflow_fixture.WorkflowTests.set_response
    call = workflow_fixture.WorkflowTests.call
    baseline = workflow_fixture.WorkflowTests.baseline
    open_request = workflow_fixture.WorkflowTests.open_request

    def setUp(self):
        workflow_fixture.WorkflowTests.setUp(self)
        self.children = []

    def tearDown(self):
        try:
            status = self.engine.status()
            if status["busy"]:
                self.engine.dispatch("stop")
                deadline = time.monotonic() + 8
                while time.monotonic() < deadline and self.engine.status()["busy"]:
                    time.sleep(.05)
            for identity in self.children:
                if process_alive(identity):
                    stop_process(identity)
        finally:
            workflow_fixture.WorkflowTests.tearDown(self)

    def await_operation(self, opid, statuses=("completed", "blocked", "failed", "stopped"), timeout=20):
        deadline = time.monotonic() + timeout
        path = "ledger/operations/" + opid + "/operation.yaml"
        while time.monotonic() < deadline:
            record = self.engine.store.read(path, {})
            if record.get("status") in statuses:
                return record
            time.sleep(.04)
        self.fail("Timed out waiting for operation " + opid + ": " + dumps(self.engine.status()))

    def cli(self, command, payload=None, key=None):
        args = [sys.executable, "-B", str(self.home / ".aih/engine/cli.py"), "--home", str(self.home), command]
        if payload is not None:
            args += ["--payload", json.dumps(payload)]
        if key:
            args += ["--idempotency-key", key]
        completed = subprocess.run(args, cwd=self.home.parent, capture_output=True, text=True, timeout=20,
                                   env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        self.assertEqual(completed.returncode, 0, completed.stderr + completed.stdout)
        return json.loads(completed.stdout)

    def test_cli_async_clarify_reuses_action_and_does_not_advance_phase(self):
        self.baseline()
        self.call("save-draft", {"lane": "change", "text": "Return the requested greeting."})
        self.set_response(clarification())
        first = self.cli("clarify", {}, "async-clarification")
        self.assertEqual(first["status"], "starting")
        repeated = self.cli("clarify", {}, "async-clarification")
        self.assertEqual(repeated["operation_id"], first["operation_id"])
        self.assertTrue(repeated["reused"])
        record = self.await_operation(first["operation_id"])
        self.assertEqual(record["status"], "completed", record)
        self.assertTrue(record["worker_started"])
        self.assertNotEqual(record["pid"], os.getpid())
        status = self.engine.status()
        self.assertFalse(status["busy"])
        self.assertEqual(status["active_request"]["phase"], "clarification")
        self.assertEqual(status["active_request"]["plan_revision"], 0)
        self.assertFalse(status["active_request"]["tasks"])
        self.assertEqual(len([r for r in status["runs"] if r["action"] == "clarify"]), 1)
        self.assertEqual(status["active_request"]["clarification_status"], "ready-for-analysis")
        self.assertEqual(status["active_request"]["submitted_input"], "Return the requested greeting.")
        self.assertEqual(len(status["active_request"]["submissions"]), 1)
        self.assertEqual(status["active_request"]["clarification_rounds"][0]["id"], first["operation_id"])
        run = next(r for r in status["runs"] if r["id"] == first["operation_id"])
        self.assertEqual(run["checkpoint"]["owner"], first["operation_id"])
        self.assertTrue(run["segments"])
        self.assertIn("Requirements ready", self.engine.artifact(run["results_path"])["text"])

    def test_async_initial_baseline_completes_without_opening_request(self):
        self.set_response(documentation_result(self.engine))
        accepted = self.engine.dispatch("reverse-engineer", {"mode": "initial"}, idempotency_key="async-baseline")
        self.assertEqual(accepted["status"], "starting")
        record = self.await_operation(accepted["operation_id"])
        self.assertEqual(record["status"], "completed", record)
        state = self.engine.status()
        self.assertFalse(state["busy"])
        self.assertEqual(state["setup"]["status"], "complete")
        self.assertIsNone(state["active_request"])
        self.assertFalse([r for r in state["runs"] if r["action"] in ("clarify", "analyze", "implement")])

    @unittest.skipUnless(confinement_diagnostics()["available"], "Managed child execution requires supported confinement")
    def test_stop_long_confined_agent_preserves_submission_logs_and_explicit_resume(self):
        self.baseline()
        self.call("save-draft", {"lane": "change", "text": "Return the required greeting after review."})
        self.set_response(clarification())
        fake = self.home / ".aih_runtime/fake-codex"
        fake.write_text("#!/usr/bin/python3\nimport json,sys,time\nsys.stdin.read()\nprint(json.dumps({'type':'thread.started','thread_id':'synthetic-slow-thread'}),flush=True)\nprint(json.dumps({'type':'item.started','item':{'type':'agent_message','text':'Synthetic transport waiting; no task completed.'}}),flush=True)\ntime.sleep(60)\n", encoding="utf-8")
        fake.chmod(0o700)
        self.call("profile-save", {"profile_id": "slow-transport", "profile": {"adapter": "codex", "executable": str(fake), "timeout": 90, "permissions": {"network": False, "product_write": False}}})
        payload = {"profile": "slow-transport"}
        accepted = self.engine.dispatch("clarify", payload, idempotency_key="slow-clarification")
        opid = accepted["operation_id"]
        self.assertEqual(accepted["status"], "starting")
        deadline = time.monotonic() + 15
        process = None
        events = []
        while time.monotonic() < deadline:
            process = self.engine.store.read("ledger/operations/" + opid + "/process.json", {})
            paths = list((self.home / ".aih_product/ledger/operations" / opid / "segments").glob("*/events.jsonl"))
            events = [p.read_text() for p in paths]
            if process.get("identity") and any("synthetic-slow-thread" in e for e in events):
                break
            record = self.engine.store.read("ledger/operations/" + opid + "/operation.yaml", {})
            if record.get("status") in ("blocked", "failed"):
                self.fail("Fake transport failed before Stop could be tested: " + dumps(record))
            time.sleep(.04)
        self.assertTrue(process and process.get("identity"), process)
        self.assertTrue(any("synthetic-slow-thread" in e for e in events), events)
        self.children.append(process["identity"])
        before = self.engine.status()
        self.assertTrue(before["busy"])
        duplicate = self.engine.dispatch("clarify", payload, idempotency_key="slow-clarification")
        self.assertEqual(duplicate["operation_id"], opid)
        for action, body in [("save-draft", {"lane": "change", "text": "Must not be queued"}), ("analyze", {}), ("ask", {"text": "A separate question"}), ("settings-save", {"appearance": {"theme": "clear", "size": 16}})]:
            with self.subTest(action=action), self.assertRaises(Error) as exc:
                self.engine.dispatch(action, body)
            self.assertEqual(exc.exception.code, "busy")
        stopped = self.engine.dispatch("stop")
        self.assertIn(stopped["status"], ("stopping", "stopped"))
        record = self.await_operation(opid)
        self.assertEqual(record["status"], "stopped", record)
        after = self.engine.status()
        self.assertFalse(after["busy"])
        self.assertEqual(after["active_request"]["id"], before["active_request"]["id"])
        self.assertEqual(after["active_request"]["submission"], before["active_request"]["submission"])
        self.assertFalse(after["active_request"]["tasks"])
        self.assertFalse(process_alive(process["identity"]))
        checkpoint = self.engine.store.read("ledger/operations/" + opid + "/checkpoint.yaml")
        self.assertIn("incomplete", checkpoint["boundary"])
        self.assertTrue(list((self.home / ".aih_product/ledger/operations" / opid / "segments").glob("*/events.jsonl")))
        self.set_response(clarification())
        resumed = self.engine.dispatch("resume", {"operation_id": opid, "profile": "synthetic"}, idempotency_key="resume-stopped")
        result = self.await_operation(resumed["operation_id"])
        self.assertEqual(result["status"], "completed", result)
        self.assertEqual(result["resumes"], opid)
        final = self.engine.status()["active_request"]
        self.assertEqual(final["id"], before["active_request"]["id"])
        self.assertEqual(final["phase"], "clarification")
        self.assertEqual(final["plan_revision"], 0)

    def test_import_launch_failure_retains_reviewed_snapshot_and_explicit_resume(self):
        self.baseline()
        self.call("save-draft", {"lane": "change", "text": "Improve the greeting for our members."})
        question = {"id": "Q-1", "revision": 1, "respondent": "Requestor", "kind": "text", "blocker": True, "category": "requirement", "question": "Who receives the greeting?", "explanation": "The greeting is displayed to members.", "why": "Determines the intended audience.", "instructions": "Describe the audience in ordinary language.", "options": [], "answer": "", "comments": ""}
        self.set_response(clarification(False, [question]))
        self.call("clarify")
        form = self.engine.status()["active_request"]["forms"][-1]
        returned = form["text"].replace("Answer: \n", "Answer: Existing and new members.\n")
        receipt = self.call("receive-answers", {"text": returned})["receipt"]
        payload = {"receipt_id": receipt["id"], "review_revision": receipt["review_revision"], "decisions": [{"question_id": "Q-1", "choice": "accept"}]}
        before_submission = self.engine.status()["active_request"]["submission"]
        self.set_response(clarification(True, [dict(question, answer="Existing and new members.")]))
        with patch("workflow.subprocess.Popen", side_effect=OSError("synthetic worker launch failure")):
            with self.assertRaises(Error) as exc:
                self.engine.dispatch("import-and-clarify", payload, idempotency_key="combined-import")
            self.assertEqual(exc.exception.code, "launch-failed")
        failed = self.engine.status()
        self.assertFalse(failed["busy"])
        self.assertNotEqual(failed["active_request"]["submission"], before_submission)
        self.assertEqual(failed["active_request"]["questions"][0]["answer"], "Existing and new members.")
        op = next(r for r in failed["runs"] if r["action"] == "import-and-clarify")
        self.assertEqual(op["status"], "failed")
        duplicate = self.engine.dispatch("import-and-clarify", payload, idempotency_key="combined-import")
        self.assertEqual(duplicate["operation_id"], op["id"])
        self.assertFalse(self.engine.status()["busy"])
        resumed = self.engine.dispatch("resume", {"operation_id": op["id"]}, idempotency_key="resume-import")
        complete = self.await_operation(resumed["operation_id"])
        self.assertEqual(complete["status"], "completed", complete)
        final = self.engine.status()
        self.assertEqual(final["active_request"]["questions"][0]["answer"], "Existing and new members.")
        self.assertEqual(final["active_request"]["clarification_status"], "ready-for-analysis")
        self.assertEqual(final["active_request"]["plan_revision"], 0)
        self.assertEqual(len([r for r in final["runs"] if r["action"] == "import-and-clarify"]), 1)


if __name__ == '__main__':
    unittest.main()
