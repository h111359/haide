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
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "configuration"))
from agent_tools import Invalid, NAMES, decode_cell, load_json, read_profiles
from configuration_tools import (ConfigurationError, load_contract as load_agent_contract,
                                 read_configuration)

FEATURES = {"chronicles": None}
ACTIVITIES_LOCATION = ".hai_env/activities"
CHRONICLES_RECORD_EVERY_PROMPTS = 5
INSTRUCTIONS = ".hai_env/agent_instructions.md"
TEMPLATE = ".hai/templates/state.json"
CONTRACT = Path(__file__).resolve().parents[2] / "contracts/state.json"


def state_contract(path: Path | None = None) -> dict:
    """Load and validate the authoritative format contract shipped with this helper."""
    path = CONTRACT if path is None else path
    try:
        contract = load_json(path)
    except (Invalid, OSError, UnicodeError) as exc:
        raise Invalid(f"State format contract is invalid: {exc}") from exc
    if (not isinstance(contract, dict)
            or set(contract) != {"current_state_format_version", "supported_state_format_versions"}):
        raise Invalid("State format contract must contain exactly current_state_format_version and supported_state_format_versions")
    current = contract["current_state_format_version"]
    supported = contract["supported_state_format_versions"]
    if (type(current) is not int or current <= 0 or not isinstance(supported, list)
            or not supported or any(type(version) is not int or version <= 0 for version in supported)
            or len(set(supported)) != len(supported) or current not in supported):
        raise Invalid("State format contract has invalid versions; use unique positive integers and include the current version")
    return contract


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
                     ".hai_env/config",
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


def state_context(workspace: Path, state: dict, template: dict,
                  contract: dict) -> tuple[dict, dict, dict]:
    if (not isinstance(template, dict)
            or not isinstance(template.get("activities"), dict)
            or template["activities"] != {"location": ACTIVITIES_LOCATION}
            or not isinstance(template.get("features"), dict)
            or set(template["features"]) != set(FEATURES)):
        raise Invalid("Canonical format-3 template is invalid")
    chronicles = template["features"].get("chronicles")
    if (not isinstance(chronicles, dict)
            or chronicles.get("enabled") is not False
            or type(chronicles.get("record_every_prompts")) is not int
            or chronicles.get("record_every_prompts") != CHRONICLES_RECORD_EVERY_PROMPTS):
        raise Invalid("Canonical format-3 template requires disabled chronicles and threshold defaults")
    if isinstance(state, dict) and "compatible_version" in state:
        raise Invalid("Incompatible core state: legacy compatible_version is unsupported; migrate explicitly to state_format_version")
    if isinstance(state, dict) and isinstance(state.get("features"), dict):
        legacy_features = state["features"]
        if "agent_instructions" in legacy_features:
            raise Invalid("Incompatible core state: retired features.agent_instructions is unsupported; use the fixed mandatory instructions file")
        if "requests" in legacy_features:
            raise Invalid("Incompatible core state: legacy features.requests is unsupported; Activities are the HAI work unit")
        chronicles = legacy_features.get("chronicles")
        if isinstance(chronicles, dict) and "location" in chronicles:
            raise Invalid("Incompatible core state: global features.chronicles.location is retired; transcripts are Activity-local")
    version = state.get("state_format_version") if isinstance(state, dict) else None
    if (not isinstance(state, dict) or type(version) is not int
            or version not in contract["supported_state_format_versions"]
            or "agents" in state or "requests" in state or "current_request" in state or "current_activity" in state
            or not isinstance(state.get("activities"), dict)
            or not isinstance(state.get("features"), dict)
            or "requests" in state["features"]
            or "agent_instructions" in state["features"]):
        raise Invalid("Incompatible core state: expected a supported state format with mandatory activities and features; legacy requests/current pointers and retired features.agent_instructions are unsupported")
    if version == 3 and "specification" in state["features"]:
        raise Invalid("Incompatible format-3 core state: features.specification is agent-owned and must be migrated to Specification-manager configuration")
    if version == 2 and "specification" not in state["features"]:
        raise Invalid("Incompatible format-2 core state: mandatory legacy features.specification is missing")
    activities = state["activities"]
    if ("enabled" in activities or not isinstance(activities.get("location"), str)
            or not activities["location"].strip()):
        raise Invalid("Mandatory activities requires a nonblank workspace-relative location and no enabled switch")
    reserved = [".hai", ".git", ".hai_env/state.json", ".hai_env/agents",
                ".hai_env/config", ".hai_env/model_profiles.json", INSTRUCTIONS]
    reserved_paths = [workspace / name for name in reserved]
    for name in reserved:
        try:
            reserved_paths.append(safe_path(workspace, name))
        except Invalid:
            if name != ".hai_env/model_profiles.json":
                raise
    locations, features = {}, {}
    activity_relative = activities["location"]
    activity_target = safe_path(workspace, activity_relative)
    activity_lexical = workspace / activity_relative
    if any(overlaps(candidate, reserved_path) for candidate in (activity_lexical, activity_target)
           for reserved_path in reserved_paths):
        raise Invalid("Mandatory Activity store overlaps a reserved location")
    if activity_target.exists() and not activity_target.is_dir():
        raise Invalid("Mandatory Activity store must target a directory")
    locations["activities"] = (activity_lexical, activity_target)
    activity_config = {"location": activity_relative,
                       "available": activity_target.exists(), "target_type": "directory"}
    for name, kind in FEATURES.items():
        value = state["features"].get(name)
        if name == "chronicles":
            if not isinstance(value, dict) or type(value.get("enabled")) is not bool or "location" in value:
                raise Invalid("Feature chronicles requires Boolean enabled and no global location")
            threshold = value.get("record_every_prompts", CHRONICLES_RECORD_EVERY_PROMPTS)
            if type(threshold) is not int or threshold <= 0:
                raise Invalid("Feature chronicles.record_every_prompts must be a positive integer")
            features[name] = {"enabled": value["enabled"],
                              "record_every_prompts": threshold}
    if version == 2:
        value = state["features"].get("specification")
        if (not isinstance(value, dict) or type(value.get("enabled")) is not bool
                or not isinstance(value.get("location"), str) or not value["location"].strip()):
            raise Invalid("Legacy format-2 specification requires Boolean enabled and nonblank location")
        relative = value["location"]
        target = safe_path(workspace, relative)
        lexical = workspace / relative
        if any(overlaps(candidate, reserved_path)
               for candidate in (lexical, target) for reserved_path in reserved_paths):
            raise Invalid("Legacy specification location overlaps a reserved location")
        for other, (other_lexical, other_target) in locations.items():
            if any(overlaps(candidate, previous) for candidate in (lexical, target)
                   for previous in (other_lexical, other_target)):
                raise Invalid(f"Legacy specification location collides with {other}")
        if target.exists() and not target.is_dir():
            raise Invalid("Legacy specification location must target a directory")
        locations["legacy_specification"] = (lexical, target)
    return features, locations, activity_config


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


def specification_configuration(workspace: Path, agents: list[dict]) -> dict:
    """Read only the registered installed Specification-manager package/config."""
    result = {"status": "unavailable", "path": ".hai_env/config/agents/specification-manager.json",
              "settings": {}, "configured_fields": [], "issues": []}
    entry = next((agent for agent in agents
                  if agent.get("name") == "specification-manager"
                  and agent.get("origin") == ".hai_env"), None)
    if entry is None:
        return result
    contract_relative = ".hai_env/agents/specification-manager/configuration/contract.json"
    try:
        definition = safe_path(workspace, entry["definition"])
        package = definition.parent
        contract_path = safe_path(workspace, contract_relative)
        if not contract_path.is_relative_to(package):
            raise Invalid("Specification-manager contract resolves outside its installed package")
        contract = load_agent_contract(contract_path, "specification-manager")
        expected = {"enabled", "location"}
        if (contract["contract_format_version"] != 2
                or contract["current_config_format_version"] != 1
                or set(contract["settings"]) != expected
                or contract["settings"]["enabled"] != {"type": "boolean", "default": False}
                or contract["settings"]["location"].get("type") != "workspace-relative-directory"
                or contract["settings"]["location"].get("default") != ".hai_env/specifications"):
            raise Invalid("Specification-manager contract must declare disabled-by-default enablement and a workspace-relative directory")
        result.update(read_configuration(workspace, "specification-manager", contract))
    except (Invalid, ConfigurationError, OSError, UnicodeError, RuntimeError) as exc:
        result["status"] = "invalid"
        result["issues"].append({"code": "agent_configuration", "path": contract_relative,
                                 "agent": "specification-manager", "message": str(exc)})
    return result


def check(workspace: Path) -> dict:
    workspace = workspace.resolve(strict=True)
    if not workspace.is_dir():
        raise Invalid("Workspace must be an existing directory")
    result = {"ok": False, "environment": "invalid", "activities": {}, "features": {},
              "agent_instructions": None, "instructions_status": "unverified",
              "agents": [], "catalogues": {},
              "agent_configurations": {"specification-manager": {
                  "status": "unavailable", "settings": {}, "configured_fields": [], "issues": []}},
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
        contract = state_contract()
        container = safe_path(workspace, ".hai_env")
        if container.exists() and not container.is_dir():
            raise Invalid(".hai_env must be a directory")
        state_path = safe_path(workspace, ".hai_env/state.json")
        if not state_path.exists():
            result["environment"] = "absent"
        else:
            state = load_json(state_path)
            template = load_json(safe_path(workspace, TEMPLATE))
            features, locations, activities = state_context(
                workspace, state, template, contract)
            result.update(environment="valid", activities=activities, features=features,
                          current_state_format_version=contract["current_state_format_version"],
                          state_format_version=state["state_format_version"])
            if state["state_format_version"] == 2:
                result["migration_required"] = {
                    "status": "required", "from_state_format_version": 2,
                    "to_state_format_version": 3,
                    "reason": "Specification settings remain in format-2 state; no agent-owned settings fallback is active"}
                result["agent_configurations"]["specification-manager"] = {
                    "status": "migration_required", "settings": {}, "configured_fields": [], "issues": []}
                issues.append({"code": "migration_required", "path": ".hai_env/state.json",
                               "message": "Explicitly migrate format-2 specification settings to Specification-manager configuration"})
    except (Invalid, OSError, UnicodeError) as exc:
        issues.append({"code": "state", "path": ".hai_env/state.json", "message": str(exc)})
    result["state_status"] = result["environment"]

    # The workspace catalogue is optional and independent of core validity.
    local = catalogue(workspace, ".hai_env")
    result["catalogues"]["workspace"] = local["status"]
    result["agents"].extend(local["entries"])
    issues.extend(local["issues"])

    if (result["environment"] == "valid"
            and result.get("state_format_version") == 3):
        specification = specification_configuration(workspace, result["agents"])
        result["agent_configurations"]["specification-manager"] = specification
        issues.extend(specification["issues"])

    try:
        path = safe_path(workspace, ".hai_env/model_profiles.json")
        config_root = safe_path(workspace, ".hai_env/config")
        if any(overlaps(candidate, root) for candidate in
               (workspace / ".hai_env/model_profiles.json", path)
               for root in (workspace / ".hai_env/config", config_root)):
            raise Invalid("Model profiles overlap agent configuration storage")
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
    result["ok"] = (result["environment"] == "valid" and result.get("state_format_version") == 3)
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
