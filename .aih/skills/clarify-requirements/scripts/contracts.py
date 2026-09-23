"""Authoritative contract validation, safe admission and compact evidence utilities."""
from __future__ import annotations
import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.0"
SCHEMA_VERSION = "1.0"
CORE = Path(__file__).resolve().parents[1]
MAX_INTAKE = 1024 * 1024


class Error(Exception):
    def __init__(self, code, message, details=None):
        super().__init__(message)
        self.code, self.message, self.details = code, message, details or {}

    def result(self):
        return {"ok": False, "error": {"code": self.code, "message": self.message, "details": self.details}}


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def uid(prefix):
    return prefix + "-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:10]


def digest(value):
    if not isinstance(value, bytes):
        value = (value if isinstance(value, str) else json.dumps(value, sort_keys=True, ensure_ascii=False)).encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def dumps(value):
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def parse(text, label="record"):
    """JSON is the intentionally supported, unambiguous safe YAML 1.2 subset."""
    try:
        def pairs(items):
            result = {}
            for key, value in items:
                if key in result:
                    raise ValueError("Duplicate object key")
                result[key] = value
            return result
        return json.loads(text, object_pairs_hook=pairs)
    except (ValueError, TypeError) as exc:
        raise Error("invalid-record", f"{label} must use the documented JSON-compatible YAML format; it was not reset.") from exc


_SECRETS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:sk-(?:proj-)?[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})\b"),
    re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password|authorization)\s*[:=]\s*[\"']?(?!\$\{|env:|ENV\[|<|REDACTED|example|placeholder|none|null)([A-Za-z0-9_+/.=-]{8,})"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9_.-]{16,}"),
]


def screen(text, category="input"):
    if not isinstance(text, str):
        raise Error("invalid-input", "Provide UTF-8 plain text.")
    if len(text.encode("utf-8")) > MAX_INTAKE or "\x00" in text:
        raise Error("input-size", "Provide UTF-8 text without NUL bytes, at most 1 MiB.")
    if any(pattern.search(text) for pattern in _SECRETS):
        raise Error("sensitive-input", "Sensitive input detected. Correct the original and resubmit; the rejected content was not retained.", {"category": category})
    return text


def sanitize(text):
    result = str(text)
    for pattern in _SECRETS:
        result = pattern.sub("[REDACTED sensitive execution output]", result)
    return result


def identifier(value, label="identifier"):
    if not isinstance(value, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,100}", value):
        raise Error("invalid-id", f"Invalid {label}; use letters, digits, dot, dash or underscore.")
    return value


def validate(value, schema, path="$", root=None):
    """Small explicit JSON Schema subset; schemas carry contracts, Python executes them."""
    root = root or schema
    if "$ref" in schema:
        target = root
        for part in schema["$ref"].removeprefix("#/").split("/"):
            target = target[part]
        return validate(value, target, path, root)
    types = {"object": dict, "array": list, "string": str, "integer": int, "number": (int, float), "boolean": bool, "null": type(None)}
    kind = schema.get("type")
    if kind and (not isinstance(value, types[kind]) or kind in ("integer", "number") and isinstance(value, bool)):
        raise Error("schema", f"{path} must be {kind}.")
    if "enum" in schema and value not in schema["enum"]:
        raise Error("schema", f"{path} has an unsupported value.")
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                raise Error("schema", f"{path}.{key} is required.")
        for key, item in value.items():
            if key in schema.get("properties", {}):
                validate(item, schema["properties"][key], f"{path}.{key}", root)
            elif schema.get("additionalProperties") is False:
                raise Error("schema", f"{path}.{key} is unsupported.")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise Error("schema", f"{path} needs more entries.")
        for i, item in enumerate(value):
            validate(item, schema.get("items", {}), f"{path}[{i}]", root)
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise Error("schema", f"{path} cannot be empty.")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            raise Error("schema", f"{path} has an invalid format.")
    return value


def validate_record(name, value):
    schemas = parse((CORE / "conventions/runtime.schema.json").read_text("utf-8"))
    return validate(value, schemas["$defs"][name], root=schemas)


def json_result(text):
    """Agents return data. No code is evaluated, imported or executed from the result."""
    text = text.strip()
    if text.startswith("```json") and text.endswith("```"):
        text = text[7:-3].strip()
    result = parse(text, "agent result")
    if not isinstance(result, dict):
        raise Error("agent-contract", "The agent must return a JSON object matching the operation result contract.")
    screen(dumps(result), "agent result")
    return result
