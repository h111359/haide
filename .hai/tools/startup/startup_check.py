"""Read-only, bounded HAI startup checks; never initializes or repairs files."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agents"))
from agent_tools import Invalid, NAMES, decode_cell, load_json, read_profiles

FEATURES = {"requests": "directory", "specification": "directory", "chronicles": "directory"}
INTEGRATIONS = ("git", "github")
INSTRUCTIONS = ".hai_env/agent_instructions.md"
TEMPLATE = ".hai/agents/environment-manager/templates/state.json"


def overlaps(left: Path, right: Path) -> bool:
    if left == right or left.is_relative_to(right) or right.is_relative_to(left):
        return True
    # Existing aliases can coincide on case-insensitive POSIX volumes or via hardlinks.
    for anchor, other in ((left, right), (right, left)):
        if anchor.exists():
            for ancestor in (other, *other.parents):
                try:
                    if anchor.samefile(ancestor):
                        return True
                except (OSError, ValueError):
                    continue
    return False


def safe_path(workspace: Path, relative: str) -> Path:
    """Resolve all existing prefixes, including dangling links and junctions."""
    if (not isinstance(relative, str) or not relative.strip()
            or any(c in relative for c in "\\:?#\x00\r\n")
            or relative.startswith("/") or ".." in relative.split("/")):
        raise Invalid(f"Unsafe workspace-relative path: {relative!r}")
    try:
        current = workspace
        for part in Path(relative).parts:
            # Reject Windows aliases/device names on every OS for portable saved paths.
            if (part.endswith((".", " ")) or re.fullmatch(
                    r"(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?", part, re.IGNORECASE)):
                raise Invalid(f"Nonportable path component: {part}")
            current = current / part
            try:
                current.lstat()
            except FileNotFoundError:
                # Strict resolution below still detects missing links in ancestors.
                continue
            resolved = current.resolve(strict=True)
            if not resolved.is_relative_to(workspace):
                raise Invalid(f"Path escapes workspace: {relative}")
        target = current.resolve()
        if target == workspace or not target.is_relative_to(workspace):
            raise Invalid(f"Path is workspace root or escapes workspace: {relative}")
        return target
    except (OSError, RuntimeError) as exc:
        raise Invalid(f"Unreadable, dangling, or invalid path {relative}: {exc}") from exc


def readable_file(path: Path) -> None:
    if not path.is_file():
        raise Invalid("Expected a readable regular file")
    with path.open("rb") as source:
        source.read(0)  # Check access, without loading a definition's content.


def instruction_path(workspace: Path) -> Path:
    target = safe_path(workspace, INSTRUCTIONS)
    for relative in (".hai", ".git", ".hai_env/state.json", ".hai_env/agents",
                     ".hai_env/model_profiles.json"):
        reserved_paths = [workspace / relative]
        try:
            reserved_paths.append(safe_path(workspace, relative))
        except Invalid:
            # An unrelated bad state/profile/registry path must not suppress safe instructions.
            pass
        if any(overlaps(target, reserved) for reserved in reserved_paths):
            raise Invalid("Mandatory instructions alias a reserved framework/environment location")
    return target


def state_context(workspace: Path, state: dict, template: dict) -> tuple[dict, dict, dict, list[dict]]:
    if (not isinstance(template, dict)
            or type(template.get("compatible_version")) is not int
            or template["compatible_version"] <= 0
            or not isinstance(template.get("features"), dict)
            or set(template["features"]) != set(FEATURES)):
        raise Invalid("Canonical state template is invalid")
    for feature in template["features"].values():
        if (not isinstance(feature, dict) or feature.get("enabled") is not False
                or not isinstance(feature.get("location"), str) or not feature["location"].strip()):
            raise Invalid("Canonical template requires disabled features and nonblank locations")
    template_integrations = template.get("integrations")
    if (not isinstance(template_integrations, dict)
            or set(template_integrations) != set(INTEGRATIONS)
            or any(not isinstance(template_integrations[name], dict)
                   or template_integrations[name].get("enabled") is not False
                   for name in INTEGRATIONS)):
        raise Invalid("Canonical template requires disabled Git and GitHub integrations")
    if (not isinstance(state, dict) or type(state.get("compatible_version")) is not int
            or state["compatible_version"] != template["compatible_version"]
            or "agents" in state or "current_request" in state
            or not isinstance(state.get("features"), dict)
            or "agent_instructions" in state["features"]):
        raise Invalid("Incompatible core state: expected template version and features; no legacy agents/current_request or retired agent_instructions setting")
    reserved = [".hai", ".git", ".hai_env/state.json", ".hai_env/agents", INSTRUCTIONS]
    # Validate both the spelling and resolved location, including aliases to reserved paths.
    reserved_paths = [workspace / name for name in reserved]
    reserved_paths += [safe_path(workspace, name) for name in reserved]
    locations, features = {}, {}
    for name, kind in FEATURES.items():
        value = state["features"].get(name)
        if (not isinstance(value, dict) or type(value.get("enabled")) is not bool
                or not isinstance(value.get("location"), str) or not value["location"].strip()):
            raise Invalid(f"Feature {name} requires Boolean enabled and nonblank location")
        relative = value["location"]
        target = safe_path(workspace, relative)
        lexical = workspace / relative
        if any(overlaps(candidate, reserved_path)
               for candidate in (lexical, target) for reserved_path in reserved_paths):
            raise Invalid(f"Feature {name} overlaps a reserved location")
        for other, (other_lexical, other_target) in locations.items():
            if any(overlaps(candidate, previous) for candidate in (lexical, target)
                   for previous in (other_lexical, other_target)):
                raise Invalid(f"Feature locations collide: {name} and {other}")
        if target.exists() and not (target.is_file() if kind == "file" else target.is_dir()):
            raise Invalid(f"Feature {name} must target a {kind}")
        locations[name] = (lexical, target)
        features[name] = {"enabled": value["enabled"], "location": relative,
                          "available": target.exists(), "target_type": kind}
    integrations, integration_issues = {}, []
    configured = state.get("integrations")
    if configured is None and "integrations" not in state:
        integrations = {name: {"enabled": False, "status": "unconfigured"}
                        for name in INTEGRATIONS}
    elif not isinstance(configured, dict):
        integration_issues.append({"code": "integration", "path": "integrations",
                                   "message": "Integrations must be an object; Git and GitHub are unavailable"})
        integrations = {name: {"enabled": False, "status": "invalid"}
                        for name in INTEGRATIONS}
    else:
        for name in INTEGRATIONS:
            value = configured.get(name)
            if value is None and name not in configured:
                integrations[name] = {"enabled": False, "status": "unconfigured"}
            elif not isinstance(value, dict) or type(value.get("enabled")) is not bool:
                integrations[name] = {"enabled": False, "status": "invalid"}
                integration_issues.append({
                    "code": "integration", "path": f"integrations.{name}",
                    "message": f"Integration {name} requires Boolean enabled; this integration is unavailable"})
            else:
                integrations[name] = {
                    "enabled": value["enabled"],
                    "status": "enabled" if value["enabled"] else "disabled"}
    return features, locations, integrations, integration_issues


def catalogue(workspace: Path, origin: str, reserved: set[str] | None = None) -> dict:
    relative = f"{origin}/agents/catalogue.md"
    result = {"status": "invalid", "entries": [], "names": set(), "issues": []}
    try:
        path = safe_path(workspace, relative)
        if origin == ".hai_env" and not path.exists():
            result["status"] = "absent"
            return result
        readable_file(path)
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        # Markdown examples inside fences are not registration tables.
        fence = None
        for index, line in enumerate(lines):
            marker = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
            if marker:
                token, suffix = marker.groups()
                if fence is None:
                    fence = token
                elif token[0] == fence[0] and len(token) >= len(fence) and not suffix.strip():
                    fence = None
                lines[index] = ""
            elif fence is not None:
                lines[index] = ""
        tables = [i for i, line in enumerate(lines) if line.lstrip().startswith("|")
                  and (i == 0 or not lines[i - 1].lstrip().startswith("|"))]
        if len(tables) != 1:
            raise Invalid("Catalogue must contain exactly one table")
        start = tables[0]
        def cells(line):
            return [cell.strip() for cell in line.strip().strip("|").split("|")]
        if (cells(lines[start]) != ["Agent", "Selection guide", "Definition"]
                or start + 1 >= len(lines) or cells(lines[start + 1]) != ["---"] * 3):
            raise Invalid("Invalid catalogue header or separator")
        rows = []
        for line in lines[start + 2:]:
            if not line.lstrip().startswith("|"):
                break
            row = cells(line)
            match = re.fullmatch(r"`([^`]+)`", row[0]) if row else None
            name = match[1] if match else ""
            rows.append((name, row))
        counts = Counter(name.casefold() for name, _ in rows if name)
        result["names"] = set(counts)
        for name, row in rows:
            try:
                if (len(row) != 3 or not NAMES.fullmatch(name) or len(name) > 64
                        or counts[name.casefold()] != 1
                        or (reserved is not None and name.casefold() in reserved)):
                    raise Invalid("Invalid, duplicate, or framework-conflicting row/name")
                guide = decode_cell(row[1])
                if not guide.strip() or len(guide) > 1024:
                    raise Invalid("Selection guide must be nonblank and at most 1024 characters")
                if row[2] == f"[knowledge.md]({name}/knowledge.md)":
                    raise Invalid(f"Legacy registration {name}/knowledge.md requires authorized migration")
                if row[2] != f"[SKILL.md]({name}/SKILL.md)":
                    raise Invalid("Definition link must use canonical <name>/SKILL.md")
                definition = f"{origin}/agents/{name}/SKILL.md"
                target = safe_path(workspace, definition)
                readable_file(target)
                legacy = safe_path(workspace, f"{origin}/agents/{name}/knowledge.md")
                if legacy.exists():
                    raise Invalid("Conflicting legacy knowledge.md requires explicit resolution")
                result["entries"].append({"name": name, "selection_guide": guide,
                                          "definition": definition, "origin": origin})
            except (Invalid, OSError, UnicodeError) as exc:
                result["issues"].append({"code": "registration", "path": relative,
                                         "agent": name, "message": str(exc)})
        result["status"] = "partial" if result["issues"] else "valid"
    except (Invalid, OSError, UnicodeError) as exc:
        result["issues"].append({"code": "catalogue", "path": relative, "message": str(exc)})
    return result


def check(workspace: Path) -> dict:
    workspace = workspace.resolve(strict=True)
    if not workspace.is_dir():
        raise Invalid("Workspace must be an existing directory")
    result = {"ok": False, "environment": "invalid", "features": {},
              "integrations": {name: {"enabled": False, "status": "unverified"}
                               for name in INTEGRATIONS},
              "agent_instructions": None, "instructions_status": "unverified",
              "agents": [], "catalogues": {},
              "profiles": {"status": "unverified", "runtime_availability": "not_checked"},
              "issues": []}
    issues = result["issues"]
    locations = {}
    # A fixed mandatory file is independent of state validity, flags, and version.
    try:
        path = instruction_path(workspace)
        if not path.exists():
            result["instructions_status"] = "missing"
            raise Invalid("Mandatory instructions file is missing; only an existing empty file means no extra instructions")
        readable_file(path)
        with path.open(encoding="utf-8-sig", newline="") as source:
            result["agent_instructions"] = {"path": INSTRUCTIONS, "text": source.read()}
        result["instructions_status"] = "loaded"
    except (Invalid, OSError, UnicodeError) as exc:
        if result["instructions_status"] != "missing":
            result["instructions_status"] = "invalid"
        issues.append({"code": "agent_instructions", "path": INSTRUCTIONS, "message": str(exc)})

    try:
        container = safe_path(workspace, ".hai_env")
        if container.exists() and not container.is_dir():
            raise Invalid(".hai_env must be a directory")
        state_path = safe_path(workspace, ".hai_env/state.json")
        if not state_path.exists():
            result["environment"] = "absent"
        else:
            state = load_json(state_path)
            template = load_json(safe_path(workspace, TEMPLATE))
            features, locations, integrations, integration_issues = state_context(workspace, state, template)
            result.update(environment="valid", features=features,
                          integrations=integrations,
                          compatible_version=state["compatible_version"])
            issues.extend(integration_issues)
    except (Invalid, OSError, UnicodeError) as exc:
        issues.append({"code": "state", "path": ".hai_env/state.json", "message": str(exc)})
        result["integrations"] = {name: {"enabled": False, "status": "unverified"}
                                   for name in INTEGRATIONS}
    result["state_status"] = result["environment"]

    framework = catalogue(workspace, ".hai")
    result["catalogues"]["framework"] = framework["status"]
    result["agents"].extend(framework["entries"])
    issues.extend(framework["issues"])
    if result["environment"] == "valid" and framework["status"] != "invalid":
        local = catalogue(workspace, ".hai_env", framework["names"])
        result["catalogues"]["workspace"] = local["status"]
        result["agents"].extend(local["entries"])
        issues.extend(local["issues"])
    else:
        result["catalogues"]["workspace"] = "unverified"

    try:
        path = safe_path(workspace, ".hai_env/model_profiles.json")
        if any(overlaps(candidate, feature_path)
               for candidate in (workspace / ".hai_env/model_profiles.json", path)
               for feature_pair in locations.values() for feature_path in feature_pair):
            raise Invalid("Model profiles overlap a configured feature location")
        instructions = safe_path(workspace, INSTRUCTIONS)
        if any(overlaps(candidate, target) for candidate in
               (workspace / ".hai_env/model_profiles.json", path)
               for target in (workspace / INSTRUCTIONS, instructions)):
            raise Invalid("Model profiles overlap the mandatory instructions file")
        if path.exists():
            profiles = read_profiles(path)
            result["profiles"].update(status="valid", models=profiles["models"],
                                      feature_conflicts_checked=bool(locations))
        else:
            result["profiles"]["status"] = "absent"
    except (Invalid, OSError, UnicodeError) as exc:
        result["profiles"]["status"] = "invalid"
        issues.append({"code": "profiles", "path": ".hai_env/model_profiles.json", "message": str(exc)})

    if result["environment"] == "valid" and result["instructions_status"] != "loaded":
        result["environment"] = "invalid"
    result["ok"] = result["environment"] == "valid" and not issues
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        result = check(args.workspace)
        code = 0 if result["ok"] else 1
    except (Invalid, OSError, RuntimeError) as exc:
        result = {"ok": False, "issues": [{"code": "input", "message": str(exc)}]}
        code = 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
