"""Read-only HAI agent format audit and exact runtime model resolution."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML 6.x is required; see .hai/tools/agents/README.md")

NAMES = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
CLASSES = {"light", "standard", "advanced"}
EFFORTS = {"low", "medium", "high", "xhigh", "max", "ultra"}
HEADINGS = ["Purpose", "Scope", "Definitions", "Required inputs", "Optional inputs",
            "Rules", "Procedures", "Expected outcome", "References"]
EXTENSIONS = {"hai-model-class", "hai-reasoning-effort"}


class Invalid(ValueError):
    pass


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise Invalid(f"Nonstring or duplicate property: {key!r}")
        result[key] = value
    return result


class UniqueLoader(yaml.SafeLoader):
    pass


def yaml_mapping(loader, node):
    return unique_pairs(loader.construct_pairs(node, deep=True))


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, yaml_mapping)


def load_json(path):
    try:
        if not path.is_file():
            raise Invalid("Expected a readable regular JSON file")
        return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_pairs)
    except (OSError, UnicodeError, ValueError) as exc:
        raise Invalid(f"Cannot read valid JSON: {exc}") from exc


def contained(workspace, relative):
    """Resolve existing ancestors, rejecting traversal and foreign path syntax."""
    if (not isinstance(relative, str) or not relative or "\\" in relative
            or ":" in relative or "?" in relative or "#" in relative
            or relative.startswith("/") or ".." in relative.split("/")):
        raise Invalid(f"Unsafe workspace-relative path: {relative!r}")
    try:
        target = (workspace / relative).resolve()
    except (OSError, RuntimeError) as exc:
        raise Invalid(f"Cannot resolve path: {relative}: {exc}") from exc
    if target == workspace or not target.is_relative_to(workspace):
        raise Invalid(f"Path escapes workspace: {relative}")
    return target


def read_definition(path):
    try:
        if not path.is_file():
            raise Invalid("Expected a readable regular definition file")
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise Invalid(f"Cannot read definition: {exc}") from exc
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise Invalid("Definition requires YAML frontmatter")
    try:
        end = lines.index("---", 1)
        fields = yaml.load("\n".join(lines[1:end]), Loader=UniqueLoader)
    except (ValueError, yaml.YAMLError) as exc:
        raise Invalid(f"Invalid YAML frontmatter: {exc}") from exc
    if not isinstance(fields, dict):
        raise Invalid("Frontmatter must be a mapping")
    if set(fields) - {"name", "description", "metadata", "license", "compatibility", "allowed-tools"}:
        raise Invalid("HAI extensions must be under metadata")
    name, description = fields.get("name"), fields.get("description")
    if (not isinstance(name, str) or len(name) > 64 or not NAMES.fullmatch(name)
            or name != path.parent.name):
        raise Invalid("Name must be valid and exactly match the parent directory")
    if (not isinstance(description, str) or not description.strip() or len(description) > 1024
            or "\n" in description or "\r" in description):
        raise Invalid("Description must be a nonblank single paragraph of at most 1024 characters")
    for key in ("license", "compatibility", "allowed-tools"):
        if key in fields and (not isinstance(fields[key], str) or not fields[key].strip()):
            raise Invalid(f"{key} must be a nonblank string")
    if len(fields.get("compatibility", "")) > 500:
        raise Invalid("Compatibility exceeds 500 characters")
    metadata = fields.get("metadata", {})
    if (not isinstance(metadata, dict)
            or any(not isinstance(k, str) or not isinstance(v, str) for k, v in metadata.items())):
        raise Invalid("Metadata keys and values must be strings")
    if name == "leader":
        if EXTENSIONS & metadata.keys():
            raise Invalid("Leader must omit specialist execution metadata")
    elif (metadata.get("hai-model-class") not in CLASSES
          or metadata.get("hai-reasoning-effort") not in EFFORTS):
        raise Invalid("Specialist requires valid hai-model-class and hai-reasoning-effort metadata")
    headings = []
    fenced = False
    for line in lines[end + 1:]:
        if line.startswith("```") or line.startswith("~~~"):
            fenced = not fenced
        if not fenced:
            if re.match(r"^#\s", line):
                raise Invalid("Agent body must not contain an H1 title")
            if line.startswith("## "):
                headings.append(line[3:].strip())
    if headings != HEADINGS:
        raise Invalid("Body must contain exactly the nine required headings in order")
    return fields


def read_profiles(path):
    data = load_json(path)
    if (not isinstance(data, dict) or type(data.get("format_version")) is not int
            or data["format_version"] != 1 or not isinstance(data.get("models"), dict)):
        raise Invalid("Profiles require format_version 1 and a models mapping")
    if any(not isinstance(data["models"].get(k), str) or not data["models"][k].strip() for k in CLASSES):
        raise Invalid("Profiles require nonblank model IDs for light, standard, and advanced")
    return data


def resolve(workspace, definition, runtime):
    path = contained(workspace, definition)
    if not re.fullmatch(r"(?:\.hai|\.hai_env)/agents/[^/]+/SKILL\.md", definition):
        raise Invalid("Definition must use a canonical HAI agent path")
    if path.with_name("knowledge.md").exists():
        raise Invalid("Both legacy and current definitions exist; explicit conflict resolution required")
    fields = read_definition(path)
    if fields["name"] == "leader":
        raise Invalid("Leader uses interface settings and is not spawned")
    metadata = fields["metadata"]
    request = {"agent": fields["name"], "model_class": metadata["hai-model-class"],
               "reasoning_effort": metadata["hai-reasoning-effort"]}
    try:
        profiles = read_profiles(contained(workspace, ".hai_env/model_profiles.json"))
        request["model"] = profiles["models"][request["model_class"]]
        models = runtime.get("models") if isinstance(runtime, dict) else None
        if (not isinstance(models, dict) or not models
                or any(not isinstance(k, str) or not isinstance(v, list)
                       or any(not isinstance(e, str) for e in v) for k, v in models.items())):
            raise Invalid("Runtime snapshot requires model IDs mapped to supported effort lists")
        if request["model"] not in models:
            raise Invalid("Configured model is not advertised by the current runtime")
        if request["reasoning_effort"] not in models[request["model"]]:
            raise Invalid("Requested effort is not advertised for the configured model")
    except Invalid as exc:
        return {"ok": False, "request": request, "issues": [{"code": "unavailable", "message": str(exc)}]}
    return {"ok": True, "request": request, "issues": []}


def decode_cell(cell):
    # Decode exactly the three catalogue entities once; do not interpret arbitrary HTML.
    return re.sub(r"&(?:amp|#92|#124);", lambda m: html.unescape(m.group()), cell)


def audit(workspace):
    issues, agents = [], []
    framework_names = set()
    for origin in (".hai", ".hai_env"):
        relative = f"{origin}/agents/catalogue.md"
        try:
            catalogue = contained(workspace, relative)
            if (origin == ".hai_env" and not catalogue.exists()
                    and not (workspace / relative).is_symlink()):
                continue
            if not catalogue.is_file():
                raise Invalid("Expected a readable regular catalogue file")
            lines = catalogue.read_text(encoding="utf-8-sig").splitlines()
            tables = [i for i, line in enumerate(lines) if line.lstrip().startswith("|")
                      and (i == 0 or not lines[i - 1].lstrip().startswith("|"))]
            if len(tables) != 1:
                raise Invalid("Catalogue must contain exactly one table")
            start = tables[0]
            cells = lambda line: [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells(lines[start]) != ["Agent", "Selection guide", "Definition"]:
                raise Invalid("Unexpected catalogue columns")
            if start + 1 >= len(lines) or cells(lines[start + 1]) != ["---"] * 3:
                raise Invalid("Invalid catalogue table separator")
            rows = []
            for line in lines[start + 2:]:
                if not line.lstrip().startswith("|"):
                    break
                row = cells(line)
                match = re.fullmatch(r"`([^`]+)`", row[0]) if len(row) == 3 else None
                name = match[1] if match else ""
                rows.append((name, row))
            duplicates = {name.casefold() for name, _ in rows
                          if sum(other.casefold() == name.casefold() for other, _ in rows) > 1}
            if origin == ".hai":
                framework_names = {name.casefold() for name, _ in rows if name}
            for name, row in rows:
                try:
                    if (not NAMES.fullmatch(name) or len(name) > 64 or name.casefold() in duplicates
                            or (origin == ".hai_env" and name.casefold() in framework_names)):
                        raise Invalid("Invalid, duplicate, or conflicting agent name")
                    if not row[1].strip():
                        raise Invalid("Blank selection description")
                    if row[2] == f"[knowledge.md]({name}/knowledge.md)":
                        raise Invalid("Legacy registration preserved; authorized agent-format migration required")
                    if row[2] != f"[SKILL.md]({name}/SKILL.md)":
                        raise Invalid("Definition link must use canonical <name>/SKILL.md")
                    path = contained(workspace, f"{origin}/agents/{name}/SKILL.md")
                    if path.with_name("knowledge.md").exists():
                        raise Invalid("Conflicting legacy knowledge.md remains")
                    definition = read_definition(path)
                    if decode_cell(row[1]) != definition["description"]:
                        raise Invalid("Catalogue copy differs from canonical decoded description")
                    agents.append({"name": name, "definition": f"{origin}/agents/{name}/SKILL.md"})
                except (Invalid, OSError, UnicodeError) as exc:
                    issues.append({"code": "agent", "path": relative, "agent": name, "message": str(exc)})
        except (Invalid, OSError, UnicodeError) as exc:
            issues.append({"code": "catalogue", "path": relative, "message": str(exc)})
    profile_status = "absent"
    try:
        profile = contained(workspace, ".hai_env/model_profiles.json")
        if profile.exists() or (workspace / ".hai_env/model_profiles.json").is_symlink():
            read_profiles(profile)
            profile_status = "valid"
    except Invalid as exc:
        profile_status = "invalid"
        issues.append({"code": "profiles", "message": str(exc)})
    return {"ok": not issues, "agents": agents, "profiles": profile_status, "issues": issues}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=".")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("audit")
    selected = commands.add_parser("resolve")
    selected.add_argument("--definition", required=True)
    selected.add_argument("--runtime", required=True, help="Explicit JSON runtime capability snapshot")
    args = parser.parse_args()
    try:
        workspace = Path(args.workspace).resolve(strict=True)
        if not workspace.is_dir():
            raise Invalid("Workspace must be a directory")
        result = audit(workspace) if args.command == "audit" else resolve(
            workspace, args.definition, load_json(Path(args.runtime)))
    except (Invalid, OSError, UnicodeError) as exc:
        result = {"ok": False, "issues": [{"code": "input", "message": str(exc)}]}
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
