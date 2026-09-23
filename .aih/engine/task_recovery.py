"""Narrow explicit Resume proof for a retained, already authorized task proposal."""
from contracts import Error, digest, now
from product_edits import reconcile


def task_spec(task):
    return {key: task[key] for key in ("id", "sequence", "kind", "outcome", "requirements", "changes", "dependencies", "completion_criteria")}


def proposal_path(operation_id, task_id):
    return "ledger/operations/" + operation_id + "/proposals/" + task_id + ".yaml"


def retain(engine, op, task, result, inventory):
    if not inventory["complete"]:
        raise Error("incomplete-inventory", "A task proposal needs a complete source manifest before product effects.")
    plan = engine.store.read(engine.reqpath("analysis/plan.yaml"))
    if engine.workspace.fingerprint() != inventory["fingerprint"]:
        raise Error("source-drift", "Sources changed while the task proposal was prepared; the proposal was not applied.")
    record = {"schema_version": "1.0", "operation_id": op["id"], "task_id": task["id"], "request_id": engine.request["id"],
              "created": now(), "task": task_spec(task), "result": result, "before_inventory": inventory,
              "plan_sha256": digest(plan), "bindings": plan["bindings"], "workspace_revision": engine.workspace.revision}
    path = proposal_path(op["id"], task["id"])
    engine.store.write(path, record, expected_hash=None)
    return path


def inspect_resume(engine, prior, existing=None):
    """Return a read-only proof; never restore permissions or mutate product files."""
    if prior.get("request_id") and prior["request_id"] != engine.request["id"]:
        raise Error("task-recovery-request", "The interrupted operation belongs to another request and cannot authorize this request's implementation.")
    interruption = "Interrupted segment requires explicit reconciliation and Resume."
    ignored = [value for value in (prior.get("error"), interruption if prior.get("status") == "stopped" else None) if value]
    transient = prior.get("status") == "stopped" or str(prior.get("error", "")).startswith("Worker launch failed:") or prior.get("error_code") in {"profile_unavailable", "agent-failed", "confinement_unavailable", "launch-failed", "stopped"}
    task = next((task for task in engine.request["tasks"] if task.get("status") != "completed"), None)
    if task is None:
        return {"task_id": None, "ignored_blockers": ignored, "technical_retry": True} if transient else None
    path = (existing or {}).get("proposal") or proposal_path(prior["id"], task["id"])
    proposal = engine.store.read(path, None)
    if proposal is None and prior.get("task_recovery"):
        path = prior["task_recovery"].get("proposal")
        proposal = engine.store.read(path, None) if path else None
    if proposal is None:
        # Explicit stop and startup failure cannot waive a business blocker or
        # any source drift. Normal gates still compare the full fingerprint.
        if not transient:
            return None
        return {"task_id": task["id"], "ignored_blockers": ignored, "technical_retry": True}
    plan = engine.store.read(engine.reqpath("analysis/plan.yaml"))
    if proposal.get("request_id") != engine.request["id"] or proposal.get("task") != task_spec(task):
        raise Error("task-recovery-conflict", "The interrupted proposal does not identify the current first incomplete task.")
    if proposal.get("plan_sha256") != digest(plan) or proposal.get("bindings") != plan["bindings"] or proposal.get("workspace_revision") != engine.workspace.revision:
        raise Error("task-recovery-authorization", "The interrupted proposal's plan, instructions, submission or workspace authority changed; reconcile and authorize the new plan.")
    if existing and existing.get("proposal_sha256") != digest(proposal):
        raise Error("task-recovery-conflict", "The retained proposal changed after Resume was accepted.")
    result = proposal["result"]
    if result.get("blockers") or result.get("defects"):
        raise Error("task-recovery-blocked", "A proposal containing business blockers or unresolved defects cannot authorize recovery.")
    changes = {(item["path"], item["action"]): item for item in task["changes"]}
    refs = set()
    for edit in result.get("edits", []):
        change = changes.get((edit.get("path"), edit.get("action")))
        if not change or edit.get("destination") != change.get("destination"):
            raise Error("task-recovery-scope", "The retained proposal exceeds the current task's exact approved effects.")
        refs.add(edit["path"])
        if edit.get("destination"):
            refs.add(edit["destination"])
    before, current = proposal["before_inventory"], engine.workspace.inventory()
    if not before.get("complete") or not current["complete"]:
        raise Error("task-recovery-inventory", "Recovery requires complete available source inventories.")
    manifest = lambda inventory: {item["ref"]: item["sha256"] for item in inventory["files"] if item["ref"] not in refs}
    if manifest(before) != manifest(current):
        raise Error("source-drift", "Files outside the interrupted task journal changed. Reconcile those changes before resuming product effects.")
    journal_path = "ledger/operations/" + proposal["operation_id"] + "/edits-" + task["id"] + "-journal.yaml"
    journal = engine.store.read(journal_path, None)
    if journal:
        if journal.get("edit_signature") != digest(result.get("edits", [])):
            raise Error("task-recovery-conflict", "The retained edit journal no longer matches its typed proposal.")
        observation = reconcile(engine.store, engine.workspace, proposal["operation_id"], task["id"], engine._plan_paths())
        if not observation["recoverable"]:
            raise Error("task-recovery-conflict", "Current permissions or content prevent resuming the retained effects.", observation)
    elif before["fingerprint"] != current["fingerprint"]:
        raise Error("source-drift", "No edit journal accounts for source changes after the retained proposal.")
    return {"proposal": path, "proposal_sha256": digest(proposal), "source_operation": proposal["operation_id"],
            "task_id": task["id"], "checked_fingerprint": current["fingerprint"], "ignored_blockers": ignored,
            "journal": journal_path if journal else None, "checked": now()}
