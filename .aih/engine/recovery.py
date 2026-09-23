"""Explicit idle recovery without invalidating the state journal being recovered.

The local OS lock covers the whole synchronous action. Its durable reservation is
kept in the ledger, so accepting recovery does not rewrite state.yaml before the
pending state transition can be reconciled. No agent or subprocess is launched.
"""
from __future__ import annotations
import base64
import copy
import os
from pathlib import Path
import re
from contracts import Error, digest, dumps, identifier, now, uid, validate_record
from execution import process_identity, process_alive
from security import Workspace, validate_registry
from storage import loads, StorageError

TERMINAL = {"completed", "failed", "blocked", "stopped", "released"}
RESERVATION = "ledger/recovery-reservation.yaml"


def assert_recovery_available(store, *, recovering=False):
    reservation = store.read(RESERVATION, None)
    if not reservation or reservation.get("status") in TERMINAL:
        return
    identity = reservation.get("identity")
    if identity and process_alive(identity):
        raise Error("busy", "A recovery action owns the product. Wait for its locked operation to finish; no new action was queued.", {"recovery": reservation.get("operation_id")})
    if not recovering:
        raise Error("recovery-pending", "An interrupted recovery reservation remains. Explicitly inspect/reconcile recovery before accepting another action.", {"recovery": reservation.get("operation_id")})


def _current(store, home):
    state = store.read("state.yaml", None)
    if state is not None:
        validate_record("state", state)
        if state.get("owner"):
            raise Error("busy", "Stop and reconcile the recorded execution owner before recovery; deleting a lock does not prove termination.", {"owner": state["owner"]})
    accepted = store.read("ledger/configurations/current.yaml", None)
    config = store.read("config.yaml", None)
    if accepted is not None:
        validate_record("config", accepted)
    if config is not None:
        validate_record("config", config)
    # The accepted snapshot may itself be one already-written step of an
    # interrupted configuration commit. Registry history names the last state-
    # acknowledged mapping until the complete transaction is reconciled.
    registry = None
    if state is not None:
        registry = store.read(f"ledger/workspaces/{state['workspace_revision']}.yaml", None)
        if registry is None and accepted and digest(accepted) == state.get("config_hash"):
            registry = accepted["workspace"]
        if registry is None:
            raise Error("recovery-workspace", "The acknowledged workspace mapping is missing; recovery cannot invent or restore old permissions.")
        registry = validate_registry(home, registry, allow_missing=True)
    workspace = Workspace(home, registry)
    processes = []
    directory = store.path("ledger/operations")
    if directory.exists():
        for path in sorted(directory.glob("*/process.json")):
            record = store.read(path.relative_to(store.root).as_posix())
            if record.get("termination_confirmed"):
                continue
            try:
                alive = process_alive(record)
            except (KeyError, TypeError, ValueError):
                raise Error("termination-uncertain", "A process identity record is invalid; preserve ownership and reconcile it before recovery.")
            if alive:
                raise Error("termination-uncertain", "A recorded process or descendant may still be active. Use Stop before recovery.", {"process_record": path.relative_to(store.root).as_posix()})
            processes.append({"record": path.relative_to(store.root).as_posix(), "observed": "recorded leader and group absent", "termination_confirmed": True})
    return state, accepted or config, workspace, processes


def _pending_journals(store, state, workspace):
    directory = store.path("ledger/transactions")
    journals = []
    if not directory.exists():
        return journals
    for path in sorted(directory.glob("*.json")):
        relative = path.relative_to(store.root).as_posix()
        journal = store.read(relative)
        if journal.get("status") == "committed":
            continue
        if not isinstance(journal.get("steps"), list) or not journal["steps"]:
            raise Error("invalid-journal", "An incomplete transaction has an invalid step list; no existing file was reset.", {"journal": relative})
        candidates = {}
        for step in journal["steps"]:
            ref = store._ref(step["path"])
            workspace.resolve(ref, write=True, internal=True)
            if step.get("data_base64") is None:
                if store.hash(step["path"]) == step.get("after"):
                    continue
                raise Error("invalid-journal", "An incomplete transaction is missing its retained data; preserve it for explicit resolution.", {"journal": relative})
            try:
                raw = base64.b64decode(step["data_base64"], validate=True)
            except (ValueError, TypeError) as exc:
                raise Error("invalid-journal", "The retained transaction bytes are malformed.", {"journal": relative}) from exc
            if digest(raw) != step.get("after"):
                raise Error("invalid-journal", "Retained transaction data does not match its recorded content hash.", {"journal": relative, "path": step["path"]})
            if step["path"] in ("state.yaml", "config.yaml", "ledger/configurations/current.yaml"):
                candidates[step["path"]] = loads(raw.decode("utf-8"))
        after_state = candidates.get("state.yaml")
        after_config = candidates.get("ledger/configurations/current.yaml", candidates.get("config.yaml"))
        if after_state is not None:
            validate_record("state", after_state)
            if state and after_state["workspace_revision"] < state["workspace_revision"]:
                raise Error("stale-recovery-permission", "A pending journal would restore an older workspace revision. Explicitly resolve it; recovery cannot resurrect prior permissions.", {"journal": relative})
        if after_config is not None:
            validate_record("config", after_config)
            candidate_registry = validate_registry(workspace.home, after_config["workspace"], allow_missing=True)
            if state and candidate_registry["revision"] < state["workspace_revision"]:
                raise Error("stale-recovery-permission", "A pending configuration journal predates the current root permissions.", {"journal": relative})
            if state and candidate_registry["revision"] == workspace.revision and candidate_registry != workspace.registry:
                raise Error("stale-recovery-permission", "A pending configuration journal changes root authority without a new acknowledged workspace revision.", {"journal": relative})
            if state is None and (len(candidate_registry["roots"]) != 1 or candidate_registry["roots"][0]["id"] != "home"):
                raise Error("initialization-authority", "Initial-state recovery can establish only the mandatory framework home; add other folders through explicit workspace administration.")
        if state is None and after_state is not None:
            if after_state.get("owner") or after_state.get("active_request"):
                raise Error("initialization-authority", "Missing initial state cannot be reconstructed as an executing or open request from an unacknowledged journal.")
        journals.append({"path": relative, "journal": journal, "after_state": after_state, "after_config": after_config})
    if state is None and journals and not any(item["after_state"] is not None for item in journals):
        raise Error("initialization-journal", "No validated initialization state remains in the incomplete journals. Existing files were preserved.")
    return journals


def _archive_record(store, journal):
    source, destination = journal.get("source"), journal.get("destination")
    match = re.fullmatch(r"change_requests/active/([A-Za-z0-9][A-Za-z0-9_.-]{0,100})", source or "")
    if not match or destination != "change_requests/history/" + match.group(1):
        raise Error("archive-path", "An archive journal has unsupported source/destination paths; no move was attempted.")
    rid = match.group(1)
    src_path, dst_path = store.path(source), store.path(destination)
    src_exists, dst_exists = src_path.exists(), dst_path.exists()
    if src_exists == dst_exists:
        raise Error("archive-conflict", "Exactly one active or historical request record must exist before archive reconciliation.", {"request": rid, "source_exists": src_exists, "destination_exists": dst_exists})
    actual_base = source if src_exists else destination
    record = validate_record("request", store.read(actual_base + "/request.yaml"))
    if record["id"] != rid or record.get("status") not in ("completed", "cancelled", "rejected"):
        raise Error("archive-record", "The retained request does not record an explicit closure outcome.")
    closure = record.get("closure") or {}
    if closure.get("operation") != journal.get("id") or closure.get("by") != "Framework user" or closure.get("outcome") != record["status"]:
        raise Error("archive-authorization", "Archive recovery requires the matching previously recorded explicit human closure.")
    if journal.get("request_sha256") and digest(record) != journal["request_sha256"]:
        raise Error("archive-content-conflict", "The request record changed after its closure journal was prepared.")
    entries = [item for item in journal.get("catalog", {}).get("requests", []) if item.get("id") == rid]
    if len(entries) != 1 or entries[0].get("location") != destination or entries[0].get("status") != record["status"]:
        raise Error("archive-catalog", "The prepared closure catalog lacks the matching retained outcome.")
    return rid, record, entries[0], source, destination, src_exists


def _archives(engine, state, config, workspace, *, apply, restore_active=False):
    store = engine.store
    directory = store.path("ledger/archives")
    results = []
    if not directory.exists():
        return results, state
    for path in sorted(directory.glob("*.yaml")):
        relative = path.relative_to(store.root).as_posix()
        journal = store.read(relative)
        if journal.get("status") == "restored-active":
            continue
        rid_hint = (journal.get("destination") or "").rsplit("/", 1)[-1]
        catalog = store.read("change_requests/catalog.yaml", {"schema_version": "1.0", "requests": []})
        existing = next((item for item in catalog.get("requests", []) if item.get("id") == rid_hint), None)
        if journal.get("status") in ("committed", "restored-active") and state.get("active_request") != rid_hint and existing:
            continue
        try:
            rid, request, entry, source, destination, source_exists = _archive_record(store, journal)
            if state.get("active_request") not in (None, rid):
                raise Error("archive-slot-conflict", "Another request owns the active slot; archive recovery cannot replace it.")
            if existing and existing != entry:
                raise Error("archive-catalog-conflict", "The historical metadata was edited after the prepared closure; preserve both versions for explicit review.")
            if not restore_active and journal.get("workspace_revision", request["workspace_revision"]) != workspace.revision:
                raise Error("archive-workspace-conflict", "Workspace configuration changed after the prepared closure; reconcile that impact explicitly.")
            if request["status"] == "completed" and not restore_active:
                proxy = copy.copy(engine)
                proxy.state, proxy.config, proxy.workspace = copy.deepcopy(state), config, workspace
                proxy.request = copy.deepcopy(request)
                proxy.reqpath = lambda path="", request_id=None: (source if source_exists else destination) + ("/" + path if path else "")
                if proxy.request.get("acceptance_evidence", "").startswith(source + "/") and not source_exists:
                    proxy.request["acceptance_evidence"] = destination + proxy.request["acceptance_evidence"][len(source):]
                gates = proxy._completion_gates()
                if not all(gate["passed"] for gate in gates):
                    raise Error("archive-gates", "Successful closure no longer satisfies its current evidence gates. Restore the active record explicitly with restore_active=true, or restore/reconcile the checked content before recovery.", {"gates": gates})
            result = {"journal": relative, "request_id": rid, "status": "recoverable", "location": source if source_exists else destination}
            if apply:
                updated = copy.deepcopy(state)
                if restore_active:
                    if existing:
                        raise Error("archive-restore", "An already cataloged closure cannot be silently reopened.")
                    if not source_exists:
                        workspace.mkdir("home:.aih_product/change_requests/active", internal=True)
                        workspace.move("home:.aih_product/" + destination, "home:.aih_product/" + source, internal=True)
                    restored = copy.deepcopy(request)
                    restored["interrupted_closure"] = {"recorded": request["closure"], "closed": request.get("closed"), "recovery": "explicit restore_active", "at": now()}
                    restored.update(status="blocked", phase="outcome", verification="stale", documentation="stale", approval=None, direct_authorization=None,
                                    blockers=["Interrupted closure restored explicitly; reconcile current source, scope and verification before continuing."])
                    restored.pop("closed", None)
                    restored.pop("closure", None)
                    updated["active_request"] = rid
                    journal.update(status="restored-active", recovered=now())
                    writes = {source + "/request.yaml": restored, relative: journal, "state.yaml": updated}
                else:
                    if source_exists:
                        workspace.mkdir("home:.aih_product/change_requests/history", internal=True)
                        workspace.move("home:.aih_product/" + source, "home:.aih_product/" + destination, internal=True)
                    if not existing:
                        catalog.setdefault("requests", []).append(entry)
                    updated["active_request"] = None
                    journal.update(status="committed", recovered=now())
                    writes = {"change_requests/catalog.yaml": catalog, relative: journal, "state.yaml": updated}
                updated["revision"] += 1
                store.transaction(writes, expected={"state.yaml": store.hash("state.yaml")})
                state = updated
                result["status"] = "restored-active" if restore_active else "committed"
                result["location"] = source if restore_active else destination
            results.append(result)
        except (Error, StorageError, OSError, ValueError) as exc:
            results.append({"journal": relative, "request_id": rid_hint, "status": "blocked", "error": str(exc), "code": getattr(exc, "code", "archive-conflict"), "details": getattr(exc, "details", {})})
    return results, state


def _reconcile_archive_transactions(store, information, archives, pending):
    """Retire only old closure commits whose exact effect was reconciled above.

    Stop may legitimately advance state after an interrupted rename. Replaying
    that old state would reinstate an owner or older settings. Keep those bytes
    as hash evidence while recording the newly reconciled state separately.
    """
    reconciled = {item["journal"]: item for item in archives if item["status"] == "committed"}
    state = store.read("state.yaml")
    if state and not state.get("owner") and not state.get("active_request"):
        for item in pending:
            for step in item["journal"]["steps"]:
                path = step["path"]
                if not re.fullmatch(r"ledger/archives/[A-Za-z0-9_.-]+\.yaml", path):
                    continue
                retained = store.read(path, {})
                if retained.get("status") != "committed":
                    continue
                try:
                    rid, _, entry, _, _, source_exists = _archive_record(store, retained)
                except (Error, StorageError, OSError, ValueError):
                    continue
                catalog = store.read("change_requests/catalog.yaml", {})
                if not source_exists and entry in catalog.get("requests", []):
                    reconciled[path] = {"request_id": rid, "status": "committed"}
    for result in information:
        if result["status"] != "conflict":
            continue
        item = next((item for item in pending if item["journal"]["id"] == result["id"]), None)
        if not item:
            continue
        journal = item["journal"]
        paths = {step["path"] for step in journal["steps"]}
        archive_paths = paths & reconciled.keys()
        if len(archive_paths) != 1:
            continue
        archive_path = next(iter(archive_paths))
        if paths != {"change_requests/catalog.yaml", archive_path, "state.yaml"}:
            continue
        archive = store.read(archive_path)
        old_step = next(step for step in journal["steps"] if step["path"] == archive_path)
        if not old_step.get("data_base64"):
            continue
        old_archive = loads(base64.b64decode(old_step["data_base64"]).decode("utf-8"))
        if any(old_archive.get(key) != archive.get(key) for key in ("id", "source", "destination", "catalog")):
            continue
        state = store.read("state.yaml")
        if state.get("owner") or state.get("active_request"):
            continue
        journal.update(status="committed", recovered=now(), recovery_mode="archive-effect-reconciled-with-current-state",
                       reconciled_state_sha256=store.hash("state.yaml"), archive_recovery=archive_path)
        for step in journal["steps"]:
            step.pop("data_base64", None)
        store.write(item["path"], journal)
        result.update(status="reconciled", resolution="Confirmed archive metadata and retained current idle state; historical state bytes were not replayed.")


def recover_engine(engine, payload, expected_revision=None, idempotency_key=None, human=True):
    store = engine.store
    apply = payload.get("apply", False)
    if type(apply) is not bool or type(payload.get("restore_active", False)) is not bool:
        raise Error("recovery-input", "apply and restore_active must be explicit booleans.")
    if payload.get("restore_active") and not human:
        raise Error("human-administration", "Restoring an interrupted closure requires explicit framework-user administration.")
    key = identifier(idempotency_key or uid("ACTION"), "idempotency key")
    receipt_path = "ledger/receipts/" + key + ".yaml"
    request_hash = digest({"operation": "recover", "payload": payload})
    with store.lock(timeout=0):
        duplicate = store.read(receipt_path, None)
        if duplicate:
            if duplicate["request_hash"] != request_hash:
                raise Error("idempotency-conflict", "This recovery action key already identifies different input.")
            return {**duplicate["result"], "reused": True}
        assert_recovery_available(store, recovering=True)
        state, config, workspace, processes = _current(store, engine.home)
        revision = state["revision"] if state is not None else 0
        if expected_revision is not None and expected_revision != revision:
            raise Error("revision-conflict", "State changed before recovery was accepted.", {"expected": expected_revision, "actual": revision})
        pending = _pending_journals(store, state, workspace)
        opid = uid("RECOVERY")
        operation_path = "ledger/operations/" + opid + "/operation.yaml"
        operation = {"schema_version": "1.0", "id": opid, "action": "recover", "status": "running", "created": now(),
                     "workspace_revision": workspace.revision, "payload": payload, "human": human, "usage": None,
                     "reservation": "continuous local OS lock plus separate durable recovery ledger reservation",
                     "state_before": store.hash("state.yaml"), "process_observations": processes}
        reservation = {"schema_version": "1.0", "operation_id": opid, "status": "running", "identity": process_identity(os.getpid()), "created": now()}
        store.write(operation_path, operation)
        store.write(RESERVATION, reservation)
        try:
            information = store.recover(apply=apply)
            remaining_conflicts = [item for item in information if item["status"] == "conflict"]
            current_state, current_config, current_workspace, _ = _current(store, engine.home)
            # Information replay can reinstate a recorded owner. Do not launch
            # it or clear it merely because the original action was interrupted.
            archives = []
            if current_state is not None:
                archives, current_state = _archives(engine, current_state, current_config, current_workspace, apply=apply,
                                                    restore_active=payload.get("restore_active", False))
            if apply:
                _reconcile_archive_transactions(store, information, archives, pending)
                remaining_conflicts = [item for item in information if item["status"] == "conflict"]
            blocked = bool(remaining_conflicts or any(item["status"] == "blocked" for item in archives))
            operation.update(status="blocked" if blocked else "completed", completed=now(), state_after=store.hash("state.yaml"),
                             information=information, archives=archives, termination_confirmed=True)
            reservation.update(status=operation["status"], completed=now())
            result = {"ok": True, "operation_id": opid, "status": operation["status"], "revision": current_state["revision"] if current_state else 0,
                      "initialized": current_state is not None, "recovery": information, "archives": archives,
                      "applied": apply, "artifacts": [operation_path],
                      "message": "Recovery inspected/reconciled current permitted files; no agent was launched and no historical workspace permission was restored."}
            store.write(operation_path, operation)
            store.write(RESERVATION, reservation)
            store.write(receipt_path, {"request_hash": request_hash, "result": result})
            store.append_event({"type": "recovery-finished", "owner": opid, "status": operation["status"], "applied": apply})
            return result
        except BaseException as exc:
            operation.update(status="failed", completed=now(), error=str(exc), termination_confirmed=True, state_after=store.hash("state.yaml"))
            reservation.update(status="failed", completed=now())
            store.write(operation_path, operation)
            store.write(RESERVATION, reservation)
            raise
