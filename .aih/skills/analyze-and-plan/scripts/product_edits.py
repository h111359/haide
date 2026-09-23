"""Recoverable, scoped product edits across disjoint roots/filesystems.

The central journal records each observed effect. There is deliberately no claim
of an atomic cross-root commit. Recovery requires current scope and current root
permissions; historical mappings never authorize future writes.
"""
from __future__ import annotations
import copy
import re
from pathlib import Path
from security import BoundaryError, digest
from storage import now, screen_sensitive


class ProductEditError(ValueError):
    def __init__(self, message, code="product_edit_blocked", details=None):
        super().__init__(message)
        self.code, self.details = code, details or {}


def _id(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,100}", value):
        raise ProductEditError("Invalid edit operation/task identity")
    return value


def _journal_path(operation_id, task_id):
    return f"ledger/operations/{_id(operation_id)}/edits-{_id(task_id)}-journal.yaml"


def _hash(workspace, ref):
    try:
        return digest(workspace.read_bytes(ref))
    except FileNotFoundError:
        return None


def _authorized(workspace, ref, scope):
    workspace.resolve(ref, write=True, scope=scope)
    rid, parts = workspace.parse(ref)
    if not parts:
        raise ProductEditError("Edits must identify ordinary product files")
    return rid


def _mapping(workspace, refs):
    ids = {workspace.parse(ref)[0] for ref in refs}
    return {rid: {k: workspace.roots[rid][k] for k in ("path", "access")} for rid in ids}


def _current_authority(workspace, step, scope):
    refs = [step["path"]] + ([step["destination"]] if step.get("destination") else [])
    for ref in refs:
        rid = _authorized(workspace, ref, scope)
        old = step["root_mapping"].get(rid)
        current = workspace.roots[rid]
        if not old or old["path"] != current["path"]:
            raise ProductEditError("A journal root was removed or relocated. Explicitly resolve the partial outcome; historical mappings cannot restore permission.", "recovery_workspace_changed", {"ref": ref, "recorded": old, "current": current})
        if current["access"] != "read-write":
            raise ProductEditError("Recovery cannot mutate a root whose write access was revoked", "recovery_read_only")


def _observe(workspace, step):
    actual = _hash(workspace, step["path"])
    action = step["action"]
    if action == "move":
        target = _hash(workspace, step["destination"])
        if actual is None and target == step["after_hash"]:
            return "after", {"source": actual, "destination": target}
        if actual == step["before_hash"] and target is None:
            return "before", {"source": actual, "destination": target}
        if actual == step["before_hash"] and target == step["after_hash"]:
            return "destination_written", {"source": actual, "destination": target}
        return "conflict", {"source": actual, "destination": target}
    if actual == step["after_hash"]:
        return "after", {"actual": actual}
    if actual == step["before_hash"]:
        return "before", {"actual": actual}
    return "conflict", {"actual": actual}


def _execute(store, workspace, journal, scope, path, stop_event=None):
    if journal.get('redaction_requires_reauthorization'):
        raise ProductEditError('This retained proposal was redacted; reconcile current evidence and obtain fresh explicit edit authority before replay.', 'redaction_reauthorization')
    if journal.get("status") == "completed":
        for step in journal["steps"]:
            _current_authority(workspace, step, scope)
            observed, versions = _observe(workspace, step)
            if observed != "after":
                raise ProductEditError("Content changed after this task was completed; an idempotent retry cannot reapply over later edits", "edit_conflict", {"path": step["path"], "versions": versions})
        return _result(journal, workspace, path)
    journal["status"] = "applying"
    journal["last_reconciled_revision"] = workspace.revision
    store.write(path, journal)
    try:
        for step in journal["steps"]:
            if stop_event and stop_event.is_set():
                raise ProductEditError("Stop requested; partial edit progress was retained", "stopped")
            _current_authority(workspace, step, scope)
            observed, versions = _observe(workspace, step)
            if observed == "conflict" or step.get("status") == "completed" and observed != "after":
                raise ProductEditError("Product content differs from both the recorded before and after versions; no overwrite was attempted", "edit_conflict", {"path": step["path"], "versions": versions})
            if observed == "after":
                step.update(status="completed", completed=step.get("completed", now()), evidence="observed matching after version; original actor may be uncertain")
                store.write(path, journal)
                continue
            if step["action"] in ("create", "modify"):
                workspace.atomic_write(step["path"], step["content"], scope=scope, expected_hash=step["before_hash"])
            elif step["action"] == "delete":
                workspace.unlink(step["path"], scope=scope, expected_hash=step["before_hash"])
            else:
                # Copy then delete works across filesystems. Each irreversible
                # effect has its own durable progress/versions in the journal.
                if observed == "before":
                    source = workspace.read_bytes(step["path"])
                    if digest(source) != step["before_hash"]:
                        raise ProductEditError("Move source changed while reading", "edit_conflict")
                    workspace.atomic_write(step["destination"], source, scope=scope, expected_hash=None)
                    step["status"] = "destination_written"
                    store.write(path, journal)
                _current_authority(workspace, step, scope)
                if _hash(workspace, step["destination"]) != step["after_hash"]:
                    raise ProductEditError("Move destination changed before source removal", "edit_conflict")
                workspace.unlink(step["path"], scope=scope, expected_hash=step["before_hash"])
            step.update(status="completed", completed=now(), evidence="managed effect confirmed against recorded content hashes")
            journal.setdefault("per_root_progress", {})[workspace.parse(step["path"])[0]] = {
                "last_completed": step["path"], "at": step["completed"]}
            if step.get("destination"):
                journal["per_root_progress"][workspace.parse(step["destination"])[0]] = {"last_completed": step["destination"], "at": step["completed"]}
            store.write(path, journal)
        journal.update(status="completed", completed=now())
        store.write(path, journal)
    except BaseException as exc:
        journal.update(status="interrupted", interruption={"at": now(), "code": getattr(exc, "code", "effect_interrupted"), "message": str(exc)})
        store.write(path, journal)
        raise
    return _result(journal, workspace, path)


def _result(journal, workspace, path):
    changed = [{"path": step["path"], "action": step["action"], "before_hash": step["before_hash"], "after_hash": step["after_hash"],
                "destination": step.get("destination"), "workspace_revision": journal["workspace_revision"], "root_mapping": step["root_mapping"],
                "status": step["status"], "evidence": step["evidence"]} for step in journal["steps"]]
    return {"status": "completed", "changed": changed, "changed_files": changed, "journal": path,
            "workspace_revision": workspace.revision, "atomic_cross_root": False}


def apply_edits(store, workspace, edits, scope, operation_id, task_id, stop_event=None, allowed_changes=None):
    if not isinstance(edits, list):
        raise ProductEditError("An edit operation requires a typed edits list")
    if not isinstance(scope, list) or edits and not scope:
        raise ProductEditError("Product edits require the current action's explicit file scope")
    path = _journal_path(operation_id, task_id)
    with store.lock():
        existing = store.read(path)
        if existing:
            if existing.get("edit_signature") != digest(__import__("json").dumps(edits, sort_keys=True, ensure_ascii=False)):
                raise ProductEditError("This task journal already identifies different edits", "edit_identity_conflict")
            return _execute(store, workspace, existing, scope, path, stop_event)
        steps, seen = [], set()
        for edit in edits:
            if not isinstance(edit, dict) or edit.get("action") not in ("create", "modify", "delete", "move"):
                raise ProductEditError("Each edit must name a create/modify/delete/move action")
            ref, action = edit.get("path"), edit["action"]
            _authorized(workspace, ref, scope)
            if ref in seen:
                raise ProductEditError("One task may not contain ambiguous repeated file effects")
            seen.add(ref)
            if "expected_hash" not in edit:
                raise ProductEditError("Every edit must include its reviewed expected_hash (null for creation)")
            before = edit["expected_hash"]
            if action == "create" and before is not None:
                raise ProductEditError("Creation requires expected_hash=null")
            if action != "create" and (not isinstance(before, str) or not re.fullmatch(r"[0-9a-f]{64}", before)):
                raise ProductEditError("Destructive edits require a reviewed SHA-256 hash")
            if _hash(workspace, ref) != before:
                raise ProductEditError("Source content changed since the authorized proposal", "edit_conflict", {"path": ref})
            if allowed_changes is not None:
                allowed = allowed_changes.items() if isinstance(allowed_changes, dict) else [(x["path"], x["action"]) for x in allowed_changes]
                if not any(p == ref and (a == action or isinstance(a, list) and action in a) for p, a in allowed):
                    raise ProductEditError("The planned change kind does not authorize this effect", "edit_action_scope")
            content = edit.get("content")
            if action in ("create", "modify"):
                if not isinstance(content, str):
                    raise ProductEditError("Generated file edits must contain explicit UTF-8 content")
                screen_sensitive(content)
                after = digest(content)
            elif action == "delete":
                content, after = None, None
            else:
                content, after = None, before
                destination = edit.get("destination")
                _authorized(workspace, destination, scope)
                if destination in seen or _hash(workspace, destination) is not None:
                    raise ProductEditError("Move destination must be absent and distinct")
                seen.add(destination)
            refs = [ref] + ([edit["destination"]] if action == "move" else [])
            steps.append({"path": ref, "action": action, "content": content, "before_hash": before,
                          "after_hash": after, "destination": edit.get("destination"), "status": "prepared",
                          "root_mapping": _mapping(workspace, refs)})
        journal = {"schema_version": "1.0", "operation_id": operation_id, "task_id": task_id,
                   "created": now(), "status": "prepared", "workspace_revision": workspace.revision,
                   "scope": scope, "edit_signature": digest(__import__("json").dumps(edits, sort_keys=True, ensure_ascii=False)),
                   "steps": steps, "per_root_progress": {}, "atomic_cross_root": False}
        store.write(path, journal, expected_hash=None)
        return _execute(store, workspace, journal, scope, path, stop_event)


def reconcile(store, workspace, operation_id, task_id, scope=None, *, apply=False, stop_event=None):
    path = _journal_path(operation_id, task_id)
    with store.lock():
        journal = store.read(path)
        if not journal:
            raise ProductEditError("No recorded edit journal exists for this operation/task")
        if journal.get('redaction_requires_reauthorization'):
            if apply:
                raise ProductEditError('Redacted product proposals require fresh explicit authorization; historical correction cannot authorize product changes.', 'redaction_reauthorization')
            return {'journal':path,'status':'blocked-sensitive-redaction','observations':[],'conflicts':[{'reason':'Fresh explicit authorization required after historical redaction'}],'recoverable':False,'workspace_revision':workspace.revision,'atomic_cross_root':False}
        observations, conflicts = [], []
        for step in journal["steps"]:
            try:
                _current_authority(workspace, step, scope or [])
                status, versions = _observe(workspace, step)
                item = {"path": step["path"], "status": status, "versions": versions}
            except (BoundaryError, ProductEditError, OSError) as exc:
                item = {"path": step["path"], "status": "blocked", "error": str(exc), "code": getattr(exc, "code", "path_unavailable")}
            observations.append(item)
            if item["status"] in ("blocked", "conflict"):
                conflicts.append(item)
        if apply:
            if conflicts:
                raise ProductEditError("Current permission/content conflicts block recovery; recorded permissions were not reinstated", "recovery_blocked", {"conflicts": conflicts})
            return _execute(store, workspace, journal, scope, path, stop_event)
        return {"journal": path, "status": journal["status"], "observations": observations, "conflicts": conflicts,
                "recoverable": not conflicts, "workspace_revision": workspace.revision, "atomic_cross_root": False}
