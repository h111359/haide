"""End-to-end workflow tests use an explicitly selected synthetic semantic adapter.

These prove engine contracts and real subprocess test execution, not agent compliance.
"""
import copy
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contracts import CORE, Error, digest, dumps
from workflow import Engine
import documentation
import exchange

BUILD = CORE.parent / ".aih_runtime/workflow-tests"


from demo_fixtures import documentation_result, clarification, plan_result


class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        BUILD.mkdir(parents=True, exist_ok=True)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=BUILD, prefix="plain product ")
        self.home = Path(self.temp.name)
        shutil.copytree(CORE, self.home / ".aih", ignore=shutil.ignore_patterns("__pycache__"))
        (self.home / "app.py").write_text("def greet(name):\n    return 'Hi ' + name\n", encoding="utf-8")
        self.engine = Engine(self.home)
        self.engine.initialize()
        (self.home / ".aih_runtime").mkdir(exist_ok=True)
        self.response = self.home / ".aih_runtime/semantic-result.json"
        self.set_response(documentation_result(self.engine))
        self.call("profile-save", {"profile_id": "synthetic", "profile": {"adapter": "fixture", "settings": {"fixture": True, "response_ref": "home:.aih_runtime/semantic-result.json"}}, "default": True})

    def tearDown(self):
        self.temp.cleanup()

    def set_response(self, value):
        self.response.write_text(dumps(value), encoding="utf-8")

    def call(self, operation, payload=None, **kwargs):
        return self.engine.dispatch(operation, payload or {}, background=False, **kwargs)

    def baseline(self):
        self.set_response(documentation_result(self.engine))
        result = self.call("reverse-engineer")
        self.assertEqual(result["status"], "completed", self.engine.status())
        self.assertEqual(self.engine.status()["setup"]["status"], "complete")

    def open_request(self):
        self.baseline()
        self.call("save-draft", {"lane": "change", "text": "Make greet('Ada') return Hello Ada!"})
        self.set_response(clarification())
        self.assertEqual(self.call("clarify")["status"], "completed")

    def analyzed(self):
        self.open_request()
        self.set_response(plan_result(self.engine))
        self.assertEqual(self.call("analyze")["status"], "completed", self.engine.status()["current_response"])
        request = self.engine.status()["active_request"]
        self.call("approve", {"plan_revision": request["plan_revision"]})
        return request

    def implementation_response(self, bad=False):
        self.engine._load()
        source = "def greet(name):\n    return f'Hello {name}!'\n" if not bad else "def greet(name):\n    return 'wrong'\n"
        test = "import unittest\nfrom app import greet\n\nclass Greeting(unittest.TestCase):\n    def test_greeting(self):\n        self.assertEqual(greet('Ada'), 'Hello Ada!')\n"
        docs = documentation_result(self.engine, ["home:app.py", "home:tests/test_app.py"])
        contract = {"id": "greeting-tests", "workspace_revision": self.engine.workspace.revision, "runner": "python-unittest", "environment": "python3", "working_directory": "home:", "source_paths": ["home:tests"], "start_directory": "home:tests", "write_paths": [], "prerequisites": [], "isolation": "landlock", "cleanup": "operation-runtime", "authorization": "request-implementation", "required": True}
        return {"fixture_responses": {"T1": {"summary": "Greeting implemented", "edits": [{"path": "home:app.py", "action": "modify", "expected_hash": digest((self.home / "app.py").read_bytes()), "content": source}], "requirements_trace": ["greeting-acceptance"]}, "T2": {"summary": "Regression test created", "edits": [{"path": "home:tests/test_app.py", "action": "create", "expected_hash": None, "content": test}], "test_contracts": [contract], "requirements_trace": ["greeting-acceptance"]}, "T4": docs, "T5": {"summary": "Greeting acceptance verified", "acceptance": [{"criterion": "greeting-acceptance", "suite_ids": ["greeting-tests"], "evidence": "The retained greeting regression test passed against final app.py content."}], "unmet": []}}}

    def test_initialization_preserves_content_and_baseline_gate(self):
        before = (self.home / "app.py").read_bytes()
        self.assertTrue(self.engine.initialize()["reused"])
        self.call("save-draft", {"lane": "change", "text": "A change"})
        with self.assertRaisesRegex(Error, "baseline"):
            self.call("clarify")
        self.assertEqual(before, (self.home / "app.py").read_bytes())
        self.assertIsNone(self.engine.status()["active_request"])

    def test_complete_lifecycle_requires_explicit_successful_close(self):
        self.analyzed()
        self.assertIn("Hi", (self.home / "app.py").read_text())
        self.set_response(self.implementation_response())
        result = self.call("implement")
        state = self.engine.status()
        self.assertEqual(result["status"], "completed", state["current_response"])
        self.assertEqual(state["active_request"]["status"], "ready-to-close", state["current_response"])
        self.assertTrue(all(g["passed"] for g in state["active_request"]["completion_gates"]))
        rid = state["active_request"]["id"]
        self.call("close", {"outcome": "completed"})
        self.assertIsNone(self.engine.status()["active_request"])
        self.assertEqual(self.engine.status()["history"][0]["status"], "completed")
        self.assertTrue((self.home / ".aih_product/change_requests/history" / rid / "analysis/interpretation.md").exists())

    def test_busy_rejects_drafts_submissions_questions_settings_and_no_queue(self):
        self.baseline()
        self.call("handoff", {"action": "ask", "instruction": "Inspect the greeting without modifying product or documentation."})
        before = self.engine.store.read("state.yaml")
        for operation, payload in [("save-draft", {"lane": "change", "text": "unexpected"}), ("ask", {"text": "question"}), ("clarify", {}), ("settings-save", {"theme": "dark"}), ("receive-answers", {"text": "answers"})]:
            with self.assertRaisesRegex(Error, "owns this product"):
                self.call(operation, payload)
        self.assertEqual(before, self.engine.store.read("state.yaml"))
        self.assertEqual(self.engine.status()["draft"]["change"], "")
        result = self.call("stop")
        self.assertEqual(result["status"], "external-stop-awaiting-confirmation")
        self.assertTrue(self.engine.status()["busy"])
        self.call("stop", {"confirm_external_stopped": True})
        self.assertFalse(self.engine.status()["busy"])

    def test_requestor_review_partial_round_and_amendment_history(self):
        self.baseline()
        self.call("save-draft", {"lane": "change", "text": "Improve greeting."})
        q = {"id": "Q-1", "revision": 1, "respondent": "Requestor", "kind": "text", "blocker": True, "category": "requirement", "question": "Who receives the greeting?", "explanation": "We need to know which people use the greeting.", "why": "This determines whose names should be accepted.", "instructions": "Describe the intended users in your own words.", "example": "For example, new members of a club.", "options": [], "answer": "", "comments": ""}
        self.set_response(clarification(False, [q]))
        self.call("clarify")
        request = self.engine.status()["active_request"]
        self.assertEqual(request["clarification_status"], "waiting-for-requestor")
        form = request["forms"][-1]
        returned = form["text"].replace("Answer: \n", "Answer: New subscribers.\n")
        staged = self.call("receive-answers", {"text": returned})["receipt"]
        self.assertEqual(staged["rows"][0]["status"], "matched")
        self.assertFalse(exchange.answered(self.engine._questionnaire()[0]))
        self.call("review-answers", {"receipt_id": staged["id"], "review_revision": staged["review_revision"], "decisions": [{"question_id": "Q-1", "choice": "accept"}]})
        self.assertEqual(self.engine.status()["active_request"]["submission"], request["submission"])
        amendment = self.call("save-amendment", {"title": "Changed audience", "text": "Correct the earlier answer: existing subscribers also receive greetings.", "source": "Framework user"})["amendment"]
        self.set_response(clarification(True, [dict(q, answer="New and existing subscribers.")], [{"id": amendment["id"], "effect": "applied", "explanation": "Explicit correction expands the described audience."}]))
        self.call("clarify")
        self.assertEqual(self.engine.status()["active_request"]["amendments"][0]["status"], "applied")
        self.assertEqual(len(self.engine.status()["active_request"]["forms"]), 1)
        self.call("close", {"outcome": "cancelled", "reason": "Fixture complete."})
        self.assertTrue(self.engine.status()["documentation"]["notices"])

    def test_revision_conflict_idempotency_and_sensitive_intake(self):
        old = self.engine.status()["revision"]
        first = self.call("save-draft", {"lane": "change", "text": "A request"}, idempotency_key="same-action")
        again = self.call("save-draft", {"lane": "change", "text": "A request"}, idempotency_key="same-action")
        self.assertEqual(first["operation_id"], again["operation_id"])
        with self.assertRaisesRegex(Error, "State changed"):
            self.call("save-draft", {"lane": "change", "text": "lost edit"}, expected_revision=old)
        secret = "sk-" + "s" * 32
        with self.assertRaisesRegex(Error, "Sensitive"):
            self.call("receive-answers", {"text": secret})
        for path in (self.home / ".aih_product").rglob("*"):
            if path.is_file():
                self.assertNotIn(secret.encode(), path.read_bytes())

    def test_source_drift_blocks_approval_and_closure(self):
        self.open_request()
        self.set_response(plan_result(self.engine)); self.call("analyze")
        (self.home / "app.py").write_text("# external modification\n", encoding="utf-8")
        with self.assertRaisesRegex(Error, "plan"):
            self.call("approve", {"plan_revision": 1})
        with self.assertRaisesRegex(Error, "completion gate"):
            self.call("close", {"outcome": "completed"})
        self.call("close", {"outcome": "rejected", "reason": "Source changed."})
        self.assertIsNone(self.engine.status()["active_request"])

    def test_independent_question_preserves_request_and_documentation(self):
        self.open_request()
        before = copy.deepcopy(self.engine.store.read(self.engine.reqpath("request.yaml")))
        tree = self.engine.store.read("documentation/tree.yaml")
        self.set_response({"answer": "The greeting is implemented in app.py. Its observed current return value begins with Hi.", "sources": ["home:app.py"], "uncertainty": "Read-only static observation; no modification performed."})
        self.call("ask", {"text": "How does greeting work?"})
        self.assertEqual(before, self.engine.store.read(self.engine.reqpath("request.yaml")))
        self.assertEqual(tree, self.engine.store.read("documentation/tree.yaml"))
        self.assertEqual(len(self.engine.status()["questions"]), 1)

    def test_unchanged_clarify_and_reverse_engineer_reuse(self):
        self.open_request()
        old = self.engine.status()["active_request"]["interpretation_revision"]
        self.set_response({"invalid": "A model call would fail this test"})
        self.assertEqual(self.call("clarify")["status"], "completed")
        self.assertEqual(self.engine.status()["active_request"]["interpretation_revision"], old)
        self.call("close", {"outcome": "cancelled"})
        self.assertEqual(self.call("reverse-engineer")["status"], "completed")

    def test_launch_failure_keeps_submission_without_busy_or_queue(self):
        self.baseline()
        self.call("save-draft", {"lane": "change", "text": "Greeting change"})
        with patch("workflow.subprocess.Popen", side_effect=OSError("synthetic launch failure")):
            with self.assertRaisesRegex(Error, "submission was saved"):
                self.engine.dispatch("clarify")
        status = self.engine.status()
        self.assertFalse(status["busy"])
        self.assertTrue(status["active_request"]["submission"])
        self.assertEqual(status["runs"][0]["status"], "failed")

    def test_workspace_idle_change_preserves_request_and_baselines_new_root(self):
        self.open_request()
        other = self.home.parent / (self.home.name + "-reference")
        other.mkdir()
        self.addCleanup(shutil.rmtree, other)
        (other / "reference.md").write_text("Reference business facts.", encoding="utf-8")
        roots = self.engine.status()["config"]["workspace"]["roots"]
        roots.append({"id": "reference", "name": "Reference", "path": str(other), "purpose": "Read-only reference", "access": "read-only"})
        self.call("workspace-save", {"roots": roots})
        status = self.engine.status()
        self.assertEqual(status["setup"]["status"], "pending")
        self.assertIsNotNone(status["active_request"])
        with self.assertRaisesRegex(Error, "open request"):
            self.call("reverse-engineer")
        self.set_response(documentation_result(self.engine))
        self.call("reverse-engineer", {"within_request": True})
        self.assertEqual(self.engine.status()["setup"]["status"], "complete")
        self.set_response(clarification()); self.call("clarify")
        self.assertEqual(self.engine.status()["state"]["workspace_impacts"], [])


if __name__ == "__main__":
    unittest.main()
