"""Read one explicitly supplied Codex JSONL source without changing any files."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import stat
import sys

sys.dont_write_bytecode = True


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def timestamp(value):
    if not nonblank(value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is not None and parsed.utcoffset().total_seconds() == 0
    except ValueError:
        return False


def read_source(path, representation, expected_session=None):
    """Return supported completed text; any interpretation issue prevents ok=true."""
    result = {"ok": False, "source_session_id": None, "original_started_at": None,
              "representation": representation, "source_sha256": None, "messages": [], "issues": []}
    if representation not in {"event_msg", "response_item"}:
        result["issues"].append("an explicit supported representation is required")
        return result
    path = Path(path).absolute()
    result["durable_path"] = str(path)
    try:
        if path.resolve(strict=True) != path or not stat.S_ISREG(path.lstat().st_mode):
            raise ValueError("source must be a canonical regular nonlinked file")
        before = path.stat()
        raw = path.read_bytes()
        after = path.stat()
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
                after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
            raise ValueError("source changed during reading")
        text = raw.decode("utf-8")
    except (OSError, UnicodeError, ValueError) as error:
        result["issues"].append(str(error))
        return result
    result["source_sha256"] = hashlib.sha256(raw).hexdigest()
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    for position, line in enumerate(lines):
        if not line.strip():
            result["issues"].append(f"source_position {position}: blank JSONL record")
            break
        try:
            record = json.loads(line, object_pairs_hook=unique_pairs,
                                parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"invalid constant: {value}")))
            if not isinstance(record, dict) or not isinstance(record.get("payload"), dict):
                raise ValueError("record and payload must be objects")
            payload = record["payload"]
            kind = record.get("type")
            if not nonblank(kind):
                raise ValueError("record type discriminator is missing or invalid")
            if kind == "session_meta":
                identity = payload.get("id")
                started = payload.get("timestamp", record.get("timestamp"))
                if not nonblank(identity) or not timestamp(started):
                    raise ValueError("original session ID or UTC start time is missing")
                if result["source_session_id"] is not None and (
                        identity != result["source_session_id"] or started != result["original_started_at"]):
                    raise ValueError("conflicting original session identity or start time")
                result["source_session_id"], result["original_started_at"] = identity, started
                continue
            if kind != representation:
                continue
            if not nonblank(payload.get("type")):
                raise ValueError("selected representation payload type discriminator is missing or invalid")
            if representation == "event_msg":
                message_type = payload.get("type")
                if message_type not in {"user_message", "agent_message"}:
                    if "message" in payload and message_type not in {"error", "warning"}:
                        raise ValueError("unsupported event message type")
                    continue
                role = "user" if message_type == "user_message" else "assistant"
                content = payload.get("message")
            else:
                if payload["type"] != "message":
                    continue
                if payload.get("role") in {"system", "developer"}:
                    continue
                if payload.get("role") not in {"user", "assistant"}:
                    raise ValueError("message role is missing or unsupported")
                role, content = payload["role"], payload.get("content")
            if role == "assistant":
                phase = payload.get("phase")
                if phase in {"commentary", "analysis"}:
                    continue
                if phase != "final_answer":
                    raise ValueError("assistant final-message phase is missing or unsupported")
            if representation == "response_item":
                if not isinstance(content, list) or not content:
                    raise ValueError("message text blocks are missing")
                parts = []
                for block in content:
                    allowed = {"input_text", "text"} if role == "user" else {"output_text", "text"}
                    if not isinstance(block, dict) or block.get("type") not in allowed or not isinstance(block.get("text"), str):
                        raise ValueError("unsupported or incomplete message content")
                    parts.append(block["text"])
                content = "".join(parts)
            if not isinstance(content, str):
                raise ValueError("message text is not a string")
            if not timestamp(record.get("timestamp")):
                raise ValueError("actual message UTC timestamp is missing")
            message = {"source_position": position, "role": role, "text": content,
                       "timestamp": record["timestamp"]}
            if nonblank(payload.get("id")):
                message["message_id"] = payload["id"]
            result["messages"].append(message)
        except (TypeError, ValueError) as error:
            result["issues"].append(f"source_position {position}: {error}")
            break
    if result["source_session_id"] is None:
        result["issues"].append("authoritative session metadata is missing")
    if expected_session is not None and expected_session != result["source_session_id"]:
        result["issues"].append("source session does not match the assigned session")
    for message in result["messages"]:
        message["source_session_id"] = result["source_session_id"]
    result["ok"] = not result["issues"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--representation", required=True, choices=["event_msg", "response_item"])
    parser.add_argument("--expected-session")
    args = parser.parse_args()
    result = read_source(args.source, args.representation, args.expected_session)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
