"""Explicitly synthetic semantic responses for demonstrations; never selected implicitly."""
from pathlib import Path
import documentation

def documentation_result(engine, sources=None):
    engine._load()
    sources = sources or [f["ref"] for f in engine.workspace.inventory()["files"]]
    return {"topics": [{"id": "product", "title": "Synthetic greeting product", "summary": "A test example, not the user's product requirements.", "content": "# Synthetic greeting product\n\nThis deliberately small test example exposes a greeting function. Its accepted behavior is expressed in the associated test suite. Source observations and fixture-authored requirements are separate from live agent execution. External deployment is unknown and reconstruction has not been demonstrated.\n", "sources": sources, "when_to_read": "When evaluating the synthetic workflow fixture."}], "coverage": [{"id": c["id"], "status": "applicable", "rationale": "Synthetic fixture coverage is explained in its product topic; external facts remain explicitly unknown.", "topics": ["product"]} for c in documentation.coverage_categories()], "source_dispositions": [], "reconstruction_review": {k: "This test example records source and acceptance evidence; external infrastructure is unknown. Specified but not demonstrated." for k in ("business_rules", "interfaces", "expected_results", "dependencies", "acceptance_tests", "recovery")}}


def clarification(ready=True, questions=None, effects=None):
    return {"interpretation": "# Required greeting behavior\n\nProblem: callers need a clear greeting. Users: local application users. Outcome: greet a named person. Current behavior: basic greeting. Required behavior: return Hello followed by the name and an exclamation mark. Scope: the greeting function and its tests; deployment is excluded. Acceptance: greeting Ada returns Hello Ada!. Constraint: Python. No unknown local behavior is promoted to approved intent.\n", "acceptance_criteria": [{"id": "greeting-acceptance", "description": "Greeting Ada returns Hello Ada!", "source": "submitted greeting change"}], "ready": ready, "questions": questions or [], "blockers": [], "amendment_effects": effects or [], "workspace_scope_reconciled": True}


def plan_result(engine, content="def greet(name):\n    return f'Hello {name}!'\n", source="home:app.py", test="home:tests/test_app.py"):
    interpretation = clarification()
    tasks = [
        {"id": "T1", "kind": "implement", "outcome": "Update the greeting", "changes": [{"path": source, "action": "modify"}]},
        {"id": "T2", "kind": "tests", "outcome": "Create retained regression tests", "changes": [{"path": test, "action": "create"}]},
        {"id": "T3", "kind": "verify", "outcome": "Run and repair the complete required suite", "changes": []},
        {"id": "T4", "kind": "documentation", "outcome": "Apply and verify current product documentation", "changes": []},
        {"id": "T5", "kind": "evidence", "outcome": "Verify acceptance and record results", "changes": []},
    ]
    for i, task in enumerate(tasks):
        task.update(sequence=i + 1, requirements=["greeting-acceptance"], dependencies=[] if i == 0 else [tasks[i - 1]["id"]], completion_criteria=[task["outcome"] + " with inspectable evidence"])
    interpretation.update(solution_assessment="# Solution assessment\n\nModify the existing Python greeting function, retain regression tests, run the full suite and update the canonical product topic. No deployment or external service is required. The test contract records the environment and filesystem effects.\n", unrelated_issues="# Unrelated issues\n\nNo unrelated defect was found in this fixture's reviewed app and tests.\n", plan={"tasks": tasks}, documentation_increment={"topics": ["product"], "reason": "Reflect changed greeting behavior and evidence.", "proposed_changes": ["Update observed greeting output."]})
    return interpretation

