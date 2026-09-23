"""Read-only deterministic substeps for an already reserved agent segment."""
from __future__ import annotations
import difflib
from contracts import Error, digest, parse, screen, validate_record
import documentation
import exchange

OPERATIONS = {
    "inventory": {"inputs": [], "effects": "read registered sources; no persistence"},
    "extract": {"inputs": [], "effects": "static fact extraction; never import product code"},
    "read": {"inputs": ["ref"], "effects": "screened read of a root-qualified UTF-8 file"},
    "hash": {"inputs": ["ref"], "effects": "hash an existing root-qualified file"},
    "diff": {"inputs": ["before", "after"], "effects": "unified textual comparison of admitted strings"},
    "questionnaire-parse": {"inputs": ["text"], "effects": "validate authoritative Markdown and return questions"},
    "record-validate": {"inputs": ["schema", "record"], "effects": "validate a proposed inert record against installed conventions"},
    "documentation-validate": {"inputs": [], "effects": "validate current balanced tree and references"},
}


def invoke(engine, operation, owner_id, payload):
    if operation not in OPERATIONS:
        raise Error("unknown-helper", "Use a named deterministic helper from the helper catalog.")
    with engine.store.read_lock():
        engine._load()
        engine._check_config()
        owner = engine.state.get("owner")
        if not owner or owner["id"] != owner_id or owner.get("status") not in ("starting", "running", "reserved"):
            raise Error("helper-owner", "This internal substep must identify the current accepted action; it cannot start another operation.")
        for field in OPERATIONS[operation]["inputs"]:
            if field not in payload:
                raise Error("helper-input", f"Helper {operation} requires {field}.")
        if operation == "inventory":
            result = engine.workspace.inventory(payload.get("roots"))
        elif operation == "extract":
            inventory = engine.workspace.inventory(payload.get("roots"))
            result = documentation.extract(engine.workspace, inventory)
        elif operation == "read":
            text = screen(engine.workspace.read_text(payload["ref"]), "agent evidence read")
            start = max(0, int(payload.get("start_line", 1)) - 1)
            count = min(500, max(1, int(payload.get("line_count", 200))))
            lines = text.splitlines()
            result = {"ref": payload["ref"], "text": "\n".join(lines[start:start + count]), "total_lines": len(lines), "first_line": start + 1, "omitted_before": start, "omitted_after": max(0, len(lines) - start - count), "sha256": digest(text), "workspace_revision": engine.workspace.revision}
        elif operation == "hash":
            result = {"ref": payload["ref"], "sha256": digest(engine.workspace.read_bytes(payload["ref"])), "workspace_revision": engine.workspace.revision}
        elif operation == "diff":
            before, after = screen(payload["before"]), screen(payload["after"])
            result = {"diff": "".join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile="captured-before", tofile="proposed-after")), "before_sha256": digest(before), "after_sha256": digest(after)}
        elif operation == "questionnaire-parse":
            result = {"questions": exchange.parse_questionnaire(payload["text"])}
        elif operation == "record-validate":
            validate_record(payload["schema"], payload["record"])
            result = {"valid": True, "schema": payload["schema"]}
        else:
            result = documentation.validate_tree(engine.store.read("documentation/tree.yaml"), lambda path: engine._text("documentation/" + path))
        return {"ok": True, "owner_id": owner_id, "operation": operation, "read_only": True, "result": result}
