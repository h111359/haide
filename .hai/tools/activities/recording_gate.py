"""Read-only comparison gate for host-returned closure recording evidence."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True


def _nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def _snapshots(value):
    return (isinstance(value, dict) and bool(value)
            and all(_nonblank(key) and isinstance(digest, str)
                    and re.fullmatch(r"[a-f0-9]{64}", digest)
                    for key, digest in value.items()))


def _cutoff(value):
    if not isinstance(value, list) or not value:
        return False
    sessions = set()
    for item in value:
        if not isinstance(item, dict) or not _nonblank(item.get("source_session_id")):
            return False
        session = item["source_session_id"]
        if session in sessions:
            return False
        sessions.add(session)
        has_id, has_position = "message_id" in item, "source_position" in item
        if has_id == has_position:
            return False
        if has_id and not _nonblank(item["message_id"]):
            return False
        if has_position and (type(item["source_position"]) is not int or item["source_position"] < 0):
            return False
    return True


def _requirement(value):
    return (isinstance(value, dict) and set(value) == {"enabled", "mandatory"}
            and all(type(value[key]) is bool for key in value))


def _intervals(value):
    if not isinstance(value, list) or not value:
        return False
    for item in value:
        if (not isinstance(item, dict) or not _nonblank(item.get("provenance"))
                or not _cutoff([item.get("start")]) or "end" not in item):
            return False
        if item["end"] is not None:
            if (not _cutoff([item["end"]])
                    or item["start"]["source_session_id"] != item["end"]["source_session_id"]):
                return False
    return True


def _same_json(first, second):
    # Python equality conflates True with 1 (and 1 with 1.0); proofs must not.
    return json.dumps(first, sort_keys=True, allow_nan=False) == json.dumps(second, sort_keys=True, allow_nan=False)


def assess_closure(request):
    """Check supplied evidence only; callers obtain actual fresh hashes/permissions."""
    issues = []
    if not isinstance(request, dict):
        return {"ok": False, "status": "blocked", "issues": ["request must be an object"]}
    requirement = request.get("recording_requirement")
    if not _requirement(requirement):
        return {"ok": False, "status": "blocked", "issues": ["current recording requirement is unverified"]}
    if not any(requirement.values()):
        return {"ok": True, "status": "disabled_no_obligation", "issues": []}
    operation, evidence = request.get("operation"), request.get("evidence")
    if not isinstance(operation, dict) or not isinstance(evidence, dict):
        return {"ok": False, "status": "blocked", "issues": ["required operation or fresh verification evidence is missing"]}
    for key in ("activity_id", "operation_id"):
        if not _nonblank(operation.get(key)) or operation.get(key) != evidence.get(key):
            issues.append(f"{key} does not match this closure")
    if (not _cutoff(operation.get("cutoff")) or not _cutoff(evidence.get("cutoff"))
            or not _same_json(operation["cutoff"], evidence["cutoff"])):
        issues.append("exact cutoff is missing, invalid or changed")
    if (not _intervals(operation.get("enabled_intervals")) or not _intervals(evidence.get("enabled_intervals"))
            or not _same_json(operation["enabled_intervals"], evidence["enabled_intervals"])):
        issues.append("enabled intervals are missing or changed")
    if (not _requirement(evidence.get("recording_requirement"))
            or evidence["recording_requirement"] != requirement):
        issues.append("recording requirement changed")
    if evidence.get("status") != "verified" or not _nonblank(evidence.get("verification_id")):
        issues.append("fresh completed verification identity/status is missing")
    try:
        stamp = evidence["verified_at"]
        datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")
    except (KeyError, TypeError, ValueError):
        issues.append("actual UTC verification timestamp is missing or invalid")
    if evidence.get("retained_source_complete") is not True:
        issues.append("required retained source is incomplete or unverified")
    for key in ("gaps", "conflicts"):
        if evidence.get(key) != []:
            issues.append(f"{key} are unresolved or unverified")
    if evidence.get("active_writes") is not False or request.get("writers_stopped") is not True:
        issues.append("recording writers are active or uncertain")
    for key, current_key in (("source_snapshots", "current_sources"), ("artifact_snapshots", "current_artifacts")):
        snapshots = evidence.get(key)
        if not _snapshots(snapshots) or snapshots != request.get(current_key):
            issues.append(f"{key} are missing or changed since verification")
    if _cutoff(operation.get("cutoff")) and isinstance(evidence.get("source_snapshots"), dict):
        if set(evidence["source_snapshots"]) != {item["source_session_id"] for item in operation["cutoff"]}:
            issues.append("source snapshots do not match the assigned cutoff sources")
    return {"ok": not issues, "status": "verified" if not issues else "blocked", "issues": issues}


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path, help="Explicit UTF-8 JSON gate request; read only")
    args = parser.parse_args()
    try:
        request = json.loads(args.request.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs,
                             parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"invalid constant: {value}")))
        result = assess_closure(request)
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"ok": False, "status": "blocked", "issues": [str(error)]}))
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
