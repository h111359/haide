"""Manual-result parity, defect scope and durable bounded repair integration."""
import copy
from pathlib import Path
import sys
import unittest
sys.path[:0] = [str(Path(__file__).resolve().parents[1]), str(Path(__file__).resolve().parent)]
import test_workflow
from contracts import Error, digest
from demo_fixtures import documentation_result, clarification, plan_result


class ManualAndRepairTests(unittest.TestCase):
    def setUp(self):
        self.f = test_workflow.WorkflowTests("test_complete_lifecycle_requires_explicit_successful_close")
        self.f.setUpClass(); self.f.setUp()

    def tearDown(self):
        self.f.tearDown()

    def handoff(self, action, results):
        prepared = self.f.call("handoff", {"action": action, "instruction": "Generate only typed semantic proposals for the captured synthetic greeting scope; inspect product source read-only."})
        opid = prepared["operation_id"]
        self.f.call("stop", {"confirm_external_stopped": True, "evidence": {"results": results}})
        self.assertFalse(self.f.engine.status()["busy"])
        return self.f.call("resume", {"operation_id": opid})

    def test_manual_baseline_clarify_analyze_and_implementation_use_same_gates(self):
        self.f.call("profile-save", {"profile_id": "manual", "profile": {"adapter": "manual"}, "default": True})
        result = self.handoff("reverse-engineer", {"reverse-engineer-product": documentation_result(self.f.engine)})
        self.assertEqual(result["status"], "completed", self.f.engine.status()["current_response"])
        self.f.call("save-draft", {"lane": "change", "text": "Make greet Ada return Hello Ada!"})
        self.assertEqual(self.handoff("clarify", {"clarify-requirements": clarification()})["status"], "completed")
        self.assertEqual(self.handoff("analyze", {"analyze-and-plan": plan_result(self.f.engine)})["status"], "completed")
        self.f.call("approve", {"plan_revision": self.f.engine.status()["active_request"]["plan_revision"]})
        proposed = self.f.implementation_response()["fixture_responses"]
        result = self.handoff("implement", proposed)
        self.assertEqual(result["status"], "completed", self.f.engine.status()["current_response"])
        self.assertTrue(self.f.engine.status()["active_request"]["ready_to_close"])
        self.f.call("close", {"outcome": "completed"})

    def test_manual_result_staleness_is_not_authority(self):
        self.f.open_request()
        prepared = self.f.call("handoff", {"action": "analyze", "instruction": "Prepare a typed plan for the submitted greeting request."})
        self.f.call("stop", {"confirm_external_stopped": True, "evidence": {"results": {"analyze-and-plan": plan_result(self.f.engine)}}})
        self.f.call("save-draft", {"lane": "change", "text": "A different scope than the manual agent observed."})
        with self.assertRaisesRegex(Error, "changed since the manual handoff"):
            self.f.call("resume", {"operation_id": prepared["operation_id"]})
        self.assertIsNone(self.f.engine.status()["active_request"]["approval"])

    def test_in_scope_failure_automatically_repairs_and_reruns_complete_suite(self):
        self.f.analyzed()
        response = self.f.implementation_response(bad=True)
        bad = response["fixture_responses"]["T1"]["edits"][0]["content"]
        response["fixture_responses"]["repair-1"] = {"scope": "in-scope", "diagnosis": "The implementation contradicts the authorized greeting acceptance.", "edits": [{"path": "home:app.py", "action": "modify", "expected_hash": digest(bad), "content": "def greet(name):\n    return f'Hello {name}!'\n"}], "requirements_trace": ["greeting-acceptance"]}
        self.f.set_response(response)
        result = self.f.call("implement")
        self.assertEqual(result["status"], "completed", self.f.engine.status()["current_response"])
        request = self.f.engine.status()["active_request"]
        self.assertTrue(request["ready_to_close"])
        self.assertEqual(len(next(iter(request["repair_attempts"].values()))["attempts"]), 1)

    def test_budget_survives_and_explicit_extension_does_not_waive_tests(self):
        self.f.analyzed()
        self.f.call("settings-save", {"repair_budget": {"max_cycles": 1}})
        response = self.f.implementation_response(bad=True)
        bad = response["fixture_responses"]["T1"]["edits"][0]["content"]
        still_bad = "def greet(name):\n    return 'still wrong'\n"
        response["fixture_responses"]["repair-1"] = {"scope": "in-scope", "diagnosis": "First bounded attempted repair.", "edits": [{"path": "home:app.py", "action": "modify", "expected_hash": digest(bad), "content": still_bad}], "requirements_trace": ["greeting-acceptance"]}
        self.f.set_response(response)
        result = self.f.call("implement")
        self.assertEqual(result["status"], "blocked")
        request = self.f.engine.status()["active_request"]
        fid = next(iter(request["repair_attempts"]))
        self.assertEqual(len(request["repair_attempts"][fid]["attempts"]), 1)
        with self.assertRaises(Error):
            self.f.call("close", {"outcome": "completed"})
        self.f.call("extend-repair-budget", {"failure_id": fid, "additional": 1, "reason": "Try one corrected in-scope greeting repair."})
        response["fixture_responses"]["repair-2"] = {"scope": "in-scope", "diagnosis": "Use the accepted exact greeting.", "edits": [{"path": "home:app.py", "action": "modify", "expected_hash": digest(still_bad), "content": "def greet(name):\n    return f'Hello {name}!'\n"}], "requirements_trace": ["greeting-acceptance"]}
        self.f.set_response(response)
        self.assertEqual(self.f.call("resume", {"operation_id": result["operation_id"]})["status"], "completed", self.f.engine.status()["current_response"])
        self.assertEqual(len(self.f.engine.status()["active_request"]["repair_attempts"][fid]["attempts"]), 2)

    def test_unrelated_deferred_defect_never_waives_failed_required_suite(self):
        self.f.analyzed()
        response = self.f.implementation_response(bad=True)
        response["fixture_responses"]["repair-1"] = {"scope": "unrelated", "diagnosis": "Fixture classifies failure as an unrelated preexisting issue for triage testing.", "defect": {"id": "DEF-1", "symptoms": "A required greeting test fails.", "evidence": ["required suite greeting-tests failure"], "disposition": "unselected", "status": "confirmed"}}
        self.f.set_response(response)
        self.assertEqual(self.f.call("implement")["status"], "blocked")
        self.f.call("defect-disposition", {"id": "DEF-1", "disposition": "defer", "reason": "Demonstrate that deferral cannot waive required tests."})
        with self.assertRaises(Error):
            self.f.call("close", {"outcome": "completed"})
        self.assertEqual(self.f.engine.status()["documentation"]["known_defects"]["defects"][0]["disposition"], "defer")
        self.f.call("close", {"outcome": "cancelled", "reason": "Retain the failing test and defect as an unfinished state notice."})
        self.assertTrue(self.f.engine.status()["documentation"]["notices"])


if __name__ == "__main__":
    unittest.main()
