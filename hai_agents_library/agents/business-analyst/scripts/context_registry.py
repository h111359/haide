"""Read-only diagnostics for the optional Business-analyst context registry."""
import argparse
import json
import os
from pathlib import Path, PureWindowsPath
import re
import stat


FIELDS = ("Location", "Summary", "Convention", "Prompt", "Read", "Update")
EXCLUDED = {
    ".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules",
    "__pycache__", "__pypackages__", ".cache", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".tox", ".nox", ".eggs", "build", "dist",
}


def relative_parts(value):
    if (not isinstance(value, str) or not value.strip() or value != value.strip()
            or "\\" in value or ":" in value or "\x00" in value
            or Path(value).is_absolute() or PureWindowsPath(value).is_absolute()):
        raise ValueError("expected a workspace-relative path")
    parts = value.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise ValueError("empty or traversal path component")
    return parts


def resource_path(root, value, activity_store, *, registry=True):
    """Validate lexical and resolved containment; do not follow resource aliases."""
    root = Path(root).resolve(strict=True)
    parts = relative_parts(value)
    store = relative_parts(activity_store)
    if registry:
        folded = [p.casefold() for p in parts]
        if (any(p in EXCLUDED for p in folded)
                or any(re.match(r"^\d{8}_\d{6}_", p) for p in parts)
                or folded[:len(store)] == [p.casefold() for p in store]):
            raise ValueError("registry discovery into Activity/archive, metadata or cache paths is forbidden")
    current = root
    for part in parts:
        current /= part
        if current.is_symlink() or (hasattr(current, "is_junction") and current.is_junction()):
            raise ValueError("linked resource paths are forbidden")
        if current.exists() and os.path.normcase(str(current.resolve())) != os.path.normcase(str(current)):
            raise ValueError("resource alias is forbidden")
    if not current.resolve().is_relative_to(root):
        raise ValueError("path escapes workspace")
    if current.exists():
        info = current.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise ValueError("resource must be a regular, singly linked file")
    return current


def parse_registry(text):
    """The supported Markdown subset deliberately leaves every field independent."""
    entries = []
    active = False
    entry = None
    fence = None
    for line_number, line in enumerate(text.splitlines(), 1):
        stripped = line.lstrip()
        match = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence:
            if re.fullmatch(re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", stripped):
                fence = None
            continue
        if match:
            fence = match[1]
            continue
        if re.match(r"^#{1,2} ", line):
            active = line.strip() == "## References"
            entry = None
            continue
        if active and line.startswith("### "):
            entry = {"title": line[4:].strip(), "line": line_number, "fields": {}, "issues": []}
            entries.append(entry)
        elif active and entry:
            field = re.fullmatch(r"(?:- )?([A-Za-z]+):\s*(.*?)\s*", line)
            if field:
                name, value = field.groups()
                if name not in FIELDS:
                    entry["issues"].append("unknown field: " + name)
                elif name in entry["fields"]:
                    entry["issues"].append("duplicate field: " + name)
                else:
                    entry["fields"][name] = value
    if fence:
        raise ValueError("unclosed Markdown fence")
    return entries


def inspect_registry(workspace, document, activity_store):
    root = Path(workspace).resolve(strict=True)
    relative_parts(activity_store)  # Must be supplied from validated runtime context.
    primary = resource_path(root, document, activity_store, registry=False)
    entries = parse_registry(primary.read_text(encoding="utf-8"))
    diagnostics = []
    for entry in entries:
        fields = entry["fields"]
        read = fields.get("Read", "").casefold()
        entry["eligible"] = False
        entry["resources"] = {}
        if read == "no":
            entry["disposition"] = "skipped: Read=no"
            continue
        if read != "yes":
            entry["issues"].append("invalid Read value: " + repr(fields.get("Read")))
        if not entry["title"]:
            entry["issues"].append("empty entry title")
        if not fields.get("Summary"):
            entry["issues"].append("missing Summary")
        if not fields.get("Location"):
            entry["issues"].append("missing Location")
        for name in ("Location", "Convention", "Prompt"):
            value = fields.get(name)
            if not value:
                continue
            try:
                path = resource_path(root, value, activity_store)
                available = path.exists()
                if available:
                    # Check readability without reading or executing Prompt content.
                    with path.open("rb"):
                        pass
                entry["resources"][name] = {"path": value, "available": available}
                if not available:
                    diagnostics.append(f"WARNING: Context registry resource unavailable: {value}. Proceeding without that resource.")
            except (OSError, ValueError) as exc:
                entry["issues"].append(f"{name} {value}: {exc}")
        location = entry["resources"].get("Location", {})
        entry["eligible"] = read == "yes" and not entry["issues"] and location.get("available", False)
        entry["disposition"] = "evaluate semantic relevance" if entry["eligible"] else "skipped"
        diagnostics.extend(f"{entry['title']}: {issue}" for issue in entry["issues"])
    return {"document": document, "entries": entries, "diagnostics": diagnostics}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--document", required=True)
    parser.add_argument("--activity-store", required=True)
    args = parser.parse_args()
    try:
        result = inspect_registry(args.workspace, args.document, args.activity_store)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if any(e["issues"] for e in result["entries"]) else 0
    except (OSError, ValueError, UnicodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
