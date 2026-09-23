"""Reproducible, explicitly synthetic demonstrations with real confined product tests."""
from __future__ import annotations
import copy
from pathlib import Path
import shutil

from contracts import CORE, Error, digest, dumps, now, uid
from workflow import Engine
from demo_fixtures import documentation_result, clarification, plan_result
import exchange


class Example:
    def __init__(self, home):
        self.home = Path(home)
        self.home.mkdir(parents=True, exist_ok=False)
        shutil.copytree(CORE, self.home / ".aih", ignore=shutil.ignore_patterns("__pycache__"))
        (self.home / "app.py").write_text("def greet(name):\n    return 'Hi ' + name\n", encoding="utf-8")
        (self.home / ".aih_runtime").mkdir()
        self.response_path = self.home / ".aih_runtime/fixture-response.json"
        self.engine = Engine(self.home)
        self.engine.initialize()
        self.actions = []
        self.call("profile-save", {"profile_id": "synthetic-example", "profile": {"adapter": "fixture", "settings": {"fixture": True, "response_ref": "home:.aih_runtime/fixture-response.json"}}, "default": True})

    def response(self, result):
        self.response_path.write_text(dumps(result), encoding="utf-8")

    def call(self, action, payload=None, expected_status=None):
        result = self.engine.dispatch(action, payload or {}, background=False)
        self.actions.append({"time": now(), "action": action, "operation_id": result.get("operation_id"), "status": result.get("status"), "fixture_semantics": True})
        if expected_status and result.get("status") != expected_status:
            raise Error("demo-failed", f"Demo action {action} did not reach {expected_status}.", {"response": self.engine.status().get("current_response")})
        return result

    def baseline(self):
        self.response(documentation_result(self.engine))
        self.call("reverse-engineer", expected_status="completed")

    def implementation(self):
        self.engine._load()
        app = "def greet(name):\n    return f'Hello {name}!'\n"
        test = "import unittest\nfrom app import greet\n\nclass Greeting(unittest.TestCase):\n    def test_greeting(self):\n        self.assertEqual(greet('Ada'), 'Hello Ada!')\n"
        contract = {"id": "greeting-tests", "workspace_revision": self.engine.workspace.revision, "runner": "python-unittest", "environment": "python3", "working_directory": "home:", "source_paths": ["home:tests"], "start_directory": "home:tests", "write_paths": [], "prerequisites": [], "isolation": "landlock", "cleanup": "operation-runtime", "authorization": "request-implementation", "required": True}
        return {"fixture_responses": {"clarify-requirements": clarification(), "analyze-and-plan": plan_result(self.engine), "T1": {"summary": "Implement greeting acceptance", "edits": [{"path": "home:app.py", "action": "modify", "content": app, "expected_hash": digest((self.home / "app.py").read_bytes())}], "requirements_trace": ["greeting-acceptance"]}, "T2": {"summary": "Retain greeting regression", "edits": [{"path": "home:tests/test_app.py", "action": "create", "content": test, "expected_hash": None}], "test_contracts": [contract], "requirements_trace": ["greeting-acceptance"]}, "T4": documentation_result(self.engine, ["home:app.py", "home:tests/test_app.py"]), "T5": {"summary": "Greeting acceptance demonstrated by the actual required suite.", "acceptance": [{"criterion": "greeting-acceptance", "suite_ids": ["greeting-tests"], "evidence": "Retained unit test passed against the final source manifest."}], "unmet": []}}}

    def save(self):
        report = {"label": "Synthetic test example, not user product requirements or a live agent run", "home": str(self.home), "actions": self.actions, "final_status": self.engine.status()}
        (self.home.parent / (self.home.name + "-evidence.json")).write_text(dumps(report), encoding="utf-8")
        return report


def _main_story(example):
    example.baseline()
    example.call("save-draft", {"lane": "change", "text": "Give subscribers a personal greeting."})
    q1 = {"id": "Q-AUDIENCE", "revision": 1, "respondent": "Requestor", "kind": "text", "blocker": True, "category": "requirement", "question": "Who should receive a personal greeting?", "explanation": "A greeting is a short welcome shown to a person. We need to know which people should see it.", "why": "Your answer determines which users the changed behavior must support.", "instructions": "Describe the intended people in your own words, or write Needs discussion.", "example": "For example, people who have just joined a club.", "options": [], "answer": "", "comments": ""}
    q2 = {**q1, "id": "Q-OUTCOME", "question": "What exact greeting should Ada receive?", "explanation": "This is the visible text we will compare when accepting the change.", "why": "A concrete example makes success observable.", "instructions": "Write the greeting text, or explain that you do not know yet."}
    example.response(clarification(False, [q1, q2]))
    example.call("clarify", expected_status="completed")
    request = example.engine.status()["active_request"]
    form = request["forms"][-1]
    partial = form["text"].replace("Answer: \n", "Answer: New subscribers.\n", 1)
    received = example.call("receive-answers", {"text": partial})["receipt"]
    example.response(clarification(False, [dict(q1, answer="New subscribers."), q2]))
    example.call("import-and-clarify", {"receipt_id": received["id"], "review_revision": received["review_revision"], "decisions": [{"question_id": q1["id"], "choice": "accept"}, {"question_id": q2["id"], "choice": "unresolved"}]}, expected_status="completed")
    amendment = example.call("save-amendment", {"title": "Include existing subscribers", "text": "Correct the earlier audience: greet new and existing subscribers. Ada must receive Hello Ada!", "reason": "Returning subscribers should also be welcomed.", "source": "Framework user after requestor discussion"})["amendment"]
    answered = [dict(q1, answer="New and existing subscribers."), dict(q2, answer="Hello Ada!")]
    example.call("save-questionnaire", {"text": exchange.render(answered)})
    effects = [{"id": amendment["id"], "effect": "applied", "explanation": "Explicit correction supersedes the earlier imported audience; the observable greeting is now specified."}]
    example.response(clarification(True, answered, effects))
    example.call("clarify", expected_status="completed")
    # Unchanged clarification is deliberately repeated; no fixture response is consumed.
    example.response({"invalid": "This must not be consumed for an unchanged invocation"})
    example.call("clarify", expected_status="completed")
    design = {**q1, "id": "Q-DESIGN", "respondent": "Framework user", "category": "design", "question": "Should existing public greeting callers keep the same function name?", "explanation": "Changing the entry point could require updates to current callers.", "why": "This is a compatibility design decision inside the approved greeting scope.", "instructions": "Confirm the compatibility preference."}
    analysis = plan_result(example.engine)
    analysis.update(ready=False, questions=[design], plan=analysis["plan"])
    example.response(analysis); example.call("analyze", expected_status="completed")
    example.call("save-questionnaire", {"text": exchange.render([dict(design, answer="Keep the existing public function name.")])})
    analysis.update(ready=True, questions=[dict(design, answer="Keep the existing public function name.")])
    example.response(analysis); example.call("analyze", expected_status="completed")
    example.call("analyze", expected_status="completed")
    example.call("approve", {"plan_revision": example.engine.status()["active_request"]["plan_revision"]})
    example.response(example.implementation())
    example.call("implement", expected_status="completed")
    if not example.engine.status()["active_request"]["ready_to_close"]:
        raise Error("demo-failed", "The synthetic request did not satisfy every completion gate.")
    example.call("close", {"outcome": "completed"})
    # Subsequent blocked work leaves independent read-only Q&A available.
    example.call("save-draft", {"lane": "change", "text": "Consider a second greeting change, whose intended audience is unknown."})
    example.response(clarification(False, [q1])); example.call("clarify")
    example.response({"answer": "The prior request completed and its greeting regression passed. The current request remains blocked pending audience clarification.", "sources": ["home:app.py", "home:tests/test_app.py"], "uncertainty": "This is a fixture-authored read-only answer, not a live model observation."})
    example.call("ask", {"text": "What is currently implemented while this change is blocked?"})
    example.call("handoff", {"action": "ask", "instruction": "Read the existing greeting evidence without modifying the product."})
    example.call("stop")
    example.call("stop", {"confirm_external_stopped": True, "evidence": "The prepared external session was never started; no external product changes occurred."})
    example.call("close", {"outcome": "cancelled", "reason": "Synthetic demonstration of preserving an unfinished request and current-state notice."})


def _existing_story(example):
    example.call("profile-save", {"profile_id": "unavailable", "profile": {"adapter": "codex", "executable": "aih-intentionally-missing-cli"}, "default": True})
    example.call("reverse-engineer", expected_status="blocked")
    example.call("profile-save", {"profile_id": "synthetic-example", "profile": {"adapter": "fixture", "settings": {"fixture": True, "response_ref": "home:.aih_runtime/fixture-response.json"}}, "default": True})
    example.response(documentation_result(example.engine)); example.call("resume", expected_status="completed")
    example.call("save-draft", {"lane": "change", "text": "Make greet Ada return Hello Ada! using direct implementation."})
    example.response(example.implementation())
    example.call("implement-directly", expected_status="completed")
    example.call("close", {"outcome": "completed"})
    # Explicitly refresh observed external changes with provenance.
    (example.home / "README.md").write_text("# Synthetic existing product\n\nThis is an example of a manually added user guide. Greeting behavior is covered by retained tests.\n", encoding="utf-8")
    example.response(documentation_result(example.engine)); example.call("reverse-engineer", {"mode": "incremental"}, expected_status="completed")


def _multi_story(example):
    base = example.home.parent
    for name in ("frontend", "backend", "reference", "unregistered-sibling"):
        (base / name).mkdir()
    shutil.move(str(example.home / "app.py"), str(base / "backend/app.py"))
    (base / "frontend/greeting.txt").write_text("Hi Ada", encoding="utf-8")
    (base / "reference/business.txt").write_text("Synthetic reference: greet people by their chosen name.", encoding="utf-8")
    (base / "unregistered-sibling/private.txt").write_text("This sibling is outside every fixture registry.", encoding="utf-8")
    roots = example.engine.status()["config"]["workspace"]["roots"]
    roots += [{"id": rid, "name": rid.title(), "path": str(base / rid), "purpose": "Synthetic product component", "access": "read-write"} for rid in ("frontend", "backend")]
    example.call("workspace-save", {"roots": roots})
    example.baseline()
    example.call("save-draft", {"lane": "change", "text": "Update the synthetic backend greeting and frontend display together."})
    example.response(clarification()); example.call("clarify")
    roots.append({"id": "reference", "name": "Read-only reference", "path": str(base / "reference"), "purpose": "Business reference", "access": "read-only"})
    example.call("workspace-save", {"roots": roots})
    example.response(documentation_result(example.engine)); example.call("reverse-engineer", {"within_request": True}, expected_status="completed")
    example.response(clarification()); example.call("clarify")
    analysis = plan_result(example.engine, source="backend:app.py", test="backend:tests/test_app.py")
    analysis["plan"]["tasks"][0]["changes"].append({"path": "frontend:greeting.txt", "action": "modify"})
    analysis["plan"]["tasks"][1]["changes"].append({"path": "frontend:tests/test_display.py", "action": "create"})
    example.response(analysis); example.call("analyze", expected_status="completed")
    example.call("approve", {"plan_revision": example.engine.status()["active_request"]["plan_revision"]})
    revision = example.engine.workspace.revision
    contracts = [{"id": rid + "-tests", "workspace_revision": revision, "runner": "python-unittest", "environment": "python3", "working_directory": rid + ":", "source_paths": [rid + ":tests"], "start_directory": rid + ":tests", "write_paths": [], "prerequisites": [], "isolation": "landlock", "cleanup": "operation-runtime", "authorization": "request-implementation", "required": True} for rid in ("backend", "frontend")]
    backend_test = "import unittest\nfrom app import greet\nclass Greeting(unittest.TestCase):\n    def test_greeting(self):\n        self.assertEqual(greet('Ada'), 'Hello Ada!')\n"
    frontend_test = "from pathlib import Path\nimport unittest\nclass Display(unittest.TestCase):\n    def test_display(self):\n        self.assertEqual((Path(__file__).parents[1] / 'greeting.txt').read_text(), 'Hello Ada!')\n"
    responses = {"T1": {"summary": "Update two components sequentially under one task journal", "edits": [{"path": "backend:app.py", "action": "modify", "expected_hash": digest((base / "backend/app.py").read_bytes()), "content": "def greet(name):\n    return f'Hello {name}!'\n"}, {"path": "frontend:greeting.txt", "action": "modify", "expected_hash": digest((base / "frontend/greeting.txt").read_bytes()), "content": "Hello Ada!"}], "requirements_trace": ["greeting-acceptance"]}, "T2": {"summary": "Retain separate component regressions", "edits": [{"path": "backend:tests/test_app.py", "action": "create", "expected_hash": None, "content": backend_test}, {"path": "frontend:tests/test_display.py", "action": "create", "expected_hash": None, "content": frontend_test}], "test_contracts": contracts, "requirements_trace": ["greeting-acceptance"]}, "T4": documentation_result(example.engine, ["backend:app.py", "backend:tests/test_app.py", "frontend:greeting.txt", "frontend:tests/test_display.py", "reference:business.txt"]), "T5": {"summary": "Both required component suites passed", "acceptance": [{"criterion": "greeting-acceptance", "suite_ids": ["backend-tests", "frontend-tests"], "evidence": "Both actual confined Python suites checked the backend behavior and frontend display."}], "unmet": []}}
    example.response({"fixture_responses": responses}); example.call("implement", expected_status="completed")
    for ref in ("reference:business.txt", "outside:private.txt", "home:../unregistered-sibling/private.txt"):
        try:
            example.engine.workspace.atomic_write(ref, "unauthorized", scope=[ref])
        except Exception as exc:
            example.actions.append({"time": now(), "action": "negative-write-test", "ref": ref, "status": "denied", "reason": str(exc)})
        else:
            raise Error("demo-boundary", "An unauthorized negative write unexpectedly succeeded.")
    example.call("close", {"outcome": "completed"})


def _approved_example(example):
    example.baseline()
    example.call("save-draft", {"lane": "change", "text": "Make greet Ada return Hello Ada!"})
    example.response(clarification()); example.call("clarify", expected_status="completed")
    example.response(plan_result(example.engine)); example.call("analyze", expected_status="completed")
    example.call("approve", {"plan_revision": example.engine.status()["active_request"]["plan_revision"]})


def _repair_story(example):
    _approved_example(example)
    example.call("settings-save", {"repair_budget": {"max_cycles": 1}})
    response = example.implementation()
    wrong = "def greet(name):\n    return 'wrong'\n"
    still_wrong = "def greet(name):\n    return 'still wrong'\n"
    response["fixture_responses"]["T1"]["edits"][0]["content"] = wrong
    response["fixture_responses"]["repair-1"] = {"scope": "in-scope", "diagnosis": "First attempted in-scope correction; fixture intentionally retains a failing expectation to exercise the budget.", "edits": [{"path": "home:app.py", "action": "modify", "expected_hash": digest(wrong), "content": still_wrong}], "requirements_trace": ["greeting-acceptance"]}
    example.response(response)
    attempt = example.call("implement", expected_status="blocked")
    request = example.engine.status()["active_request"]
    fid = next(iter(request["repair_attempts"]))
    example.call("extend-repair-budget", {"failure_id": fid, "additional": 1, "reason": "Explicitly allow one additional in-scope correction while retaining failed attempts."})
    response["fixture_responses"]["repair-2"] = {"scope": "in-scope", "diagnosis": "The accepted behavior requires the exact Hello greeting.", "edits": [{"path": "home:app.py", "action": "modify", "expected_hash": digest(still_wrong), "content": "def greet(name):\n    return f'Hello {name}!'\n"}], "requirements_trace": ["greeting-acceptance"]}
    example.response(response)
    example.call("resume", {"operation_id": attempt["operation_id"]}, expected_status="completed")
    example.call("close", {"outcome": "completed"})


def _defect_story(example):
    _approved_example(example)
    response = example.implementation()
    response["fixture_responses"]["T1"]["edits"][0]["content"] = "def greet(name):\n    return 'wrong'\n"
    response["fixture_responses"]["repair-1"] = {"scope": "unrelated", "diagnosis": "Synthetic unrelated-defect classification used to test user scope selection and strict required-test completion.", "defect": {"id": "DEF-RETAINED", "symptoms": "The retained greeting test fails.", "evidence": ["greeting-tests failed against the current content manifest"], "disposition": "awaiting-user-selection", "status": "confirmed"}}
    example.response(response); example.call("implement", expected_status="blocked")
    example.call("defect-disposition", {"id": "DEF-RETAINED", "disposition": "defer", "reason": "Demonstrate that deferral does not waive a required suite."})
    try:
        example.call("close", {"outcome": "completed"})
    except Error as exc:
        if exc.code != "completion-gates":
            raise
        example.actions.append({"time": now(), "action": "attempt-successful-close-with-deferred-failure", "status": "correctly-refused", "reason": "Failed required suites cannot be waived."})
    else:
        raise Error("demo-failed", "A deferred required-test failure incorrectly allowed successful closure.")
    example.call("close", {"outcome": "cancelled", "reason": "Preserve retained source changes, failed required checks and the deferred defect in a current-state notice."})


def _interrupted_story(example):
    from unittest.mock import patch
    from security import Workspace
    _approved_example(example)
    example.response(example.implementation())
    original = Workspace.atomic_write
    injected = [False]
    def interrupt_after_replace(workspace, ref, data, **kwargs):
        result = original(workspace, ref, data, **kwargs)
        if workspace.home == example.home and ref == "home:app.py" and not injected[0]:
            injected[0] = True
            raise OSError("Synthetic interruption after product replacement, before journal acknowledgement")
        return result
    with patch.object(Workspace, "atomic_write", interrupt_after_replace):
        attempt = example.call("implement", expected_status="blocked")
    example.actions.append({"time": now(), "action": "simulated-interruption", "status": "retained-partial-effect", "point": "after replacement before journal acknowledgement"})
    example.call("resume", {"operation_id": attempt["operation_id"]}, expected_status="completed")
    example.call("close", {"outcome": "completed"})


def demonstrate(home, destination=None):
    workspace_home = Path(home).resolve()
    base = Path(destination).absolute() if destination else workspace_home / ".aih_runtime/demonstrations" / uid("DEMO")
    from security import Workspace
    workspace = Workspace(workspace_home)
    ref = workspace.reference(base)
    workspace.mkdir(ref, scope=[ref])
    if any(base.iterdir()):
        raise Error("demo-destination", "Select an empty workspace-contained demonstration directory; existing content is preserved.")
    examples = []
    main = Example(base / "main-product"); _main_story(main); examples.append(main.save())
    existing = Example(base / "existing-product"); _existing_story(existing); examples.append(existing.save())
    multi = Example(base / "multi-home"); _multi_story(multi); examples.append(multi.save())
    repairs = Example(base / "repair-budget-product"); _repair_story(repairs); examples.append(repairs.save())
    defects = Example(base / "deferred-defect-product"); _defect_story(defects); examples.append(defects.save())
    interrupted = Example(base / "interrupted-product"); _interrupted_story(interrupted); examples.append(interrupted.save())
    summary = {"ok": True, "created": now(), "destination": str(base), "synthetic_semantics": True, "live_agent": False, "real_product_test_processes": True, "examples": [{"home": e["home"], "actions": len(e["actions"]), "history_outcomes": [h["status"] for h in e["final_status"]["history"]]} for e in examples], "limitations": ["These fixtures test engine workflows using explicitly selected fixture-authored semantic responses.", "They do not establish real agent compliance or independent product reconstruction.", "Cross-root directories in this demonstration share a local filesystem; cross-filesystem interruption is covered separately by edit-journal tests where available."]}
    (base / "README.md").write_text("# AIH synthetic demonstrations\n\nThese are test examples, not the user's product requirements. Semantic responses are explicitly fixture-authored; registered Python test suites execute under actual confinement. Each example has its own isolated installation and central state. No fixtures are placed in information-only product state.\n\n" + dumps(summary), encoding="utf-8")
    (base / "summary.json").write_text(dumps(summary), encoding="utf-8")
    return summary
