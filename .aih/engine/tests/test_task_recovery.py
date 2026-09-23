"""Real workflow retries must use retained task effects, never bypass source drift."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contracts import Error
from security import Workspace
import test_workflow as workflow_fixture


class TaskRecoveryTests(unittest.TestCase):
    setUpClass = classmethod(workflow_fixture.WorkflowTests.setUpClass.__func__)
    setUp = workflow_fixture.WorkflowTests.setUp
    tearDown = workflow_fixture.WorkflowTests.tearDown
    set_response = workflow_fixture.WorkflowTests.set_response
    call = workflow_fixture.WorkflowTests.call
    baseline = workflow_fixture.WorkflowTests.baseline
    open_request = workflow_fixture.WorkflowTests.open_request
    analyzed = workflow_fixture.WorkflowTests.analyzed
    implementation_response = workflow_fixture.WorkflowTests.implementation_response

    def interrupted_after_product_write(self):
        self.analyzed()
        result = self.implementation_response()
        self.set_response(result)
        original = Workspace.atomic_write
        interrupted = False
        def after_write(workspace, ref, data, **kwargs):
            nonlocal interrupted
            value = original(workspace, ref, data, **kwargs)
            if ref == "home:app.py" and not interrupted:
                interrupted = True
                raise OSError("injected interruption after one product effect")
            return value
        with patch.object(Workspace, "atomic_write", new=after_write):
            operation = self.call("implement")
        self.assertEqual(operation["status"], "blocked")
        self.assertIn("Hello", (self.home / "app.py").read_text())
        self.assertTrue(self.engine.store.read("ledger/operations/" + operation["operation_id"] + "/proposals/T1.yaml"))
        return operation, result

    def test_resume_reconciles_retained_effect_and_finishes_without_regenerating_task(self):
        operation, result = self.interrupted_after_product_write()
        result["fixture_responses"].pop("T1")
        self.set_response(result)
        resumed = self.call("resume", {"operation_id": operation["operation_id"]})
        self.assertEqual(resumed["status"], "completed", self.engine.status()["current_response"])
        state = self.engine.status()
        self.assertEqual(state["active_request"]["status"], "ready-to-close", state["current_response"])
        self.assertTrue(all(task["status"] == "completed" for task in state["active_request"]["tasks"]))

    def test_resume_refuses_unrelated_human_source_change(self):
        operation, result = self.interrupted_after_product_write()
        (self.home / "human.txt").write_text("new independent human content")
        with self.assertRaisesRegex(Error, "outside the interrupted"):
            self.call("resume", {"operation_id": operation["operation_id"]})
        self.assertFalse((self.home / "tests/test_app.py").exists())

    def test_resume_refuses_human_change_to_partially_applied_file(self):
        operation, result = self.interrupted_after_product_write()
        (self.home / "app.py").write_text("human correction\n")
        with self.assertRaisesRegex(Error, "permissions or content"):
            self.call("resume", {"operation_id": operation["operation_id"]})
        self.assertEqual((self.home / "app.py").read_text(), "human correction\n")

    def test_resume_preserves_new_business_blocker(self):
        operation, result = self.interrupted_after_product_write()
        self.engine._load()
        self.engine.request["blockers"].append("Framework user must choose the retention policy")
        self.engine._save()
        with self.assertRaisesRegex(Error, "recorded request blockers"):
            self.call("resume", {"operation_id": operation["operation_id"]})
        self.assertFalse((self.home / "tests/test_app.py").exists())

    def test_safe_stop_before_proposal_retries_the_same_approved_task(self):
        self.analyzed()
        self.set_response(self.implementation_response())
        with patch.object(self.engine, "_product_task", side_effect=Error("stopped", "Confirmed safe stop before task effects")):
            operation = self.call("implement")
        self.assertEqual(operation["status"], "stopped")
        resumed = self.call("resume", {"operation_id": operation["operation_id"]})
        self.assertEqual(resumed["status"], "completed", self.engine.status()["current_response"])
        self.assertEqual(self.engine.status()["active_request"]["status"], "ready-to-close")

    def test_launch_failure_retries_authorized_implementation(self):
        self.analyzed()
        self.set_response(self.implementation_response())
        with patch("workflow.subprocess.Popen", side_effect=OSError("injected startup failure")):
            with self.assertRaisesRegex(Error, "could not launch"):
                self.engine.dispatch("implement", background=True)
        self.engine._load()
        prior = self.engine.state["last_operation"]
        resumed = self.call("resume", {"operation_id": prior})
        self.assertEqual(resumed["status"], "completed", self.engine.status()["current_response"])

    def test_question_submission_snapshots_only_question_attachments(self):
        self.engine.store.write("input/questions/attachments/question.txt", "question-specific evidence")
        self.engine.store.write("input/attachments/change.txt", "unsubmitted change-lane evidence")
        self.set_response({"answer": "Fixture answer grounded in question attachment", "sources": [], "uncertainty": "Synthetic"})
        result = self.call("ask", {"text": "Read the attached question evidence"})
        operation = self.engine.store.read("ledger/operations/" + result["operation_id"] + "/operation.yaml")
        question = self.engine.store.read("input/questions/" + operation["question_id"] + ".yaml")
        self.assertEqual([item["text"] for item in question["attachments"]], ["question-specific evidence"])
