"""Read-only validation and loading for agent-owned workspace configuration."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from environment_paths import STATE, PROFILES, INSTRUCTIONS, LEGACY, legacy_entries


class ConfigurationError(ValueError):
    """A contract or saved configuration does not satisfy its declared format."""


_NAME = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
_SETTING = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*(?:\.[a-z][a-z0-9]*(?:_[a-z0-9]+)*)*\Z")
_CONTRACT_KEYS = {
    "contract_format_version", "agent", "current_config_format_version",
    "supported_config_format_versions", "settings",
}


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise ConfigurationError(f"Nonstring or duplicate JSON property: {key!r}")
        result[key] = value
    return result


def _reject_constant(value):
    raise ConfigurationError(f"Non-JSON numeric constant: {value}")


def _load_json(path: Path):
    try:
        if not path.is_file():
            raise ConfigurationError("Expected a readable regular JSON file")
        return json.loads(path.read_text(encoding="utf-8-sig"),
                          object_pairs_hook=_unique_pairs,
                          parse_constant=_reject_constant)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ConfigurationError(f"Cannot read valid JSON: {exc}") from exc


def load_json(path):
    """Read duplicate-free strict JSON for owners with scoped validation policy."""
    return _load_json(Path(path))


def load_contract(path, expected_agent):
    """Load and validate one agent's configuration contract."""
    path = Path(path)
    contract = _load_json(path)
    if not isinstance(contract, dict) or set(contract) != _CONTRACT_KEYS:
        raise ConfigurationError("Contract must contain exactly the required format, agent, version, and settings fields")
    contract_version = contract["contract_format_version"]
    if type(contract_version) is not int or contract_version not in {1, 2}:
        raise ConfigurationError("contract_format_version must be a supported integer version (1 or 2)")
    if contract["agent"] != expected_agent or not isinstance(expected_agent, str) or not _NAME.fullmatch(expected_agent):
        raise ConfigurationError("Contract agent must match the expected canonical agent name")
    current = contract["current_config_format_version"]
    supported = contract["supported_config_format_versions"]
    if (type(current) is not int or current <= 0 or not isinstance(supported, list)
            or not supported or any(type(item) is not int or item <= 0 for item in supported)
            or len(set(supported)) != len(supported) or current not in supported):
        raise ConfigurationError("Contract has invalid configuration versions")
    settings = contract["settings"]
    if not isinstance(settings, dict):
        raise ConfigurationError("Contract settings must be an object")
    names = list(settings)
    for name in names:
        if not _SETTING.fullmatch(name):
            raise ConfigurationError(f"Invalid dotted setting name: {name!r}")
        for other in names:
            if name != other and other.startswith(name + "."):
                raise ConfigurationError(f"Setting declarations may not overlap: {name} and {other}")
        declaration = settings[name]
        if not isinstance(declaration, dict) or set(declaration) != {"type", "default"}:
            raise ConfigurationError(f"Setting {name} must declare exactly type and default")
        if declaration["type"] == "boolean":
            valid_default = type(declaration["default"]) is bool
        elif contract_version == 2 and declaration["type"] == "workspace-relative-directory":
            valid_default = isinstance(declaration["default"], str) and bool(declaration["default"].strip())
        else:
            raise ConfigurationError(f"Unsupported setting type for {name}: {declaration['type']!r}")
        if not valid_default:
            raise ConfigurationError(f"Setting {name} has a default incompatible with its declared type")
    return contract


def _safe_path(workspace: Path, relative: str) -> Path:
    if (not isinstance(relative, str) or not relative.strip()
            or any(char in relative for char in "\\:?#\x00\r\n")
            or relative.startswith("/") or ".." in relative.split("/")):
        raise ConfigurationError(f"Unsafe workspace-relative path: {relative!r}")
    current = workspace
    try:
        for part in Path(relative).parts:
            if part.endswith((".", " ")) or re.fullmatch(
                    r"(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?", part, re.IGNORECASE):
                raise ConfigurationError(f"Nonportable path component: {part}")
            current = current / part
            try:
                current.lstat()
            except FileNotFoundError:
                continue
            resolved = current.resolve(strict=True)
            if not resolved.is_relative_to(workspace):
                raise ConfigurationError(f"Path escapes workspace: {relative}")
        target = current.resolve()
        if target == workspace or not target.is_relative_to(workspace):
            raise ConfigurationError(f"Path is workspace root or escapes workspace: {relative}")
        return target
    except (OSError, RuntimeError) as exc:
        raise ConfigurationError(f"Unreadable, dangling, or invalid path {relative}: {exc}") from exc


def configuration_path(workspace, agent):
    """Return a contained, nonaliasing path safe for one agent's configuration."""
    if not isinstance(agent, str) or not _NAME.fullmatch(agent) or len(agent) > 64:
        raise ConfigurationError("Agent name is not canonical")
    workspace = Path(workspace).resolve(strict=True)
    if not workspace.is_dir():
        raise ConfigurationError("Workspace must be an existing directory")
    target = _safe_path(workspace, f".hai_env/config/agents/{agent}.json")
    _validate_configuration_target(workspace, agent, target)
    return target


def workspace_directory_path(workspace, value, reserved_paths=(), *,
                             ignore_legacy_specification=False):
    """Validate one workspace-relative directory and return its safe target.

    The configured value must not overlap fixed framework/configuration resources,
    the configured Activity store, a reserved profile/instruction path, or any
    caller-supplied paths. An existing target must be a directory; absence is safe.
    """
    workspace = Path(workspace).resolve(strict=True)
    if not workspace.is_dir():
        raise ConfigurationError("Workspace must be an existing directory")
    target = _safe_path(workspace, value)
    target_lexical = workspace / value
    reserved = [".hai", ".git", STATE, INSTRUCTIONS,
                PROFILES, ".hai_env/agents", ".hai_env/config", *LEGACY.values()]
    reserved.extend(_configured_reserved_paths(
        workspace, include_specification=not ignore_legacy_specification))
    reserved.extend(reserved_paths)
    for relative in reserved:
        if not isinstance(relative, str):
            raise ConfigurationError("Reserved paths must be workspace-relative strings")
        try:
            previous = _safe_path(workspace, relative)
        except ConfigurationError:
            continue
        if _overlaps(target, previous) or _overlaps(target_lexical, workspace / relative):
            raise ConfigurationError(f"Workspace directory overlaps reserved path {relative}")
    if target.exists() and not target.is_dir():
        raise ConfigurationError("Workspace-relative directory must target a directory")
    return target


def _overlaps(left: Path, right: Path) -> bool:
    if left == right or left.is_relative_to(right) or right.is_relative_to(left):
        return True
    for anchor, other in ((left, right), (right, left)):
        if anchor.exists():
            for ancestor in (other, *other.parents):
                try:
                    if anchor.samefile(ancestor):
                        return True
                except (OSError, ValueError):
                    pass
    return False


def _effective_settings(contract, raw, workspace=None):
    effective, configured = {}, []
    for dotted, declaration in contract["settings"].items():
        parts = dotted.split(".")
        value = raw
        found = True
        for index, part in enumerate(parts):
            if not isinstance(value, dict):
                raise ConfigurationError(f"Setting container {'.'.join(parts[:index])} must be an object")
            if part not in value:
                found = False
                break
            value = value[part]
            if index < len(parts) - 1 and not isinstance(value, dict):
                raise ConfigurationError(f"Setting container {'.'.join(parts[:index + 1])} must be an object")
        setting_type = declaration["type"]
        if found:
            if setting_type == "boolean" and type(value) is not bool:
                raise ConfigurationError(f"Setting {dotted} must be a Boolean")
            if setting_type == "workspace-relative-directory" and not isinstance(value, str):
                raise ConfigurationError(f"Setting {dotted} must be a workspace-relative directory string")
            configured.append(dotted)
        else:
            value = declaration["default"]
        if setting_type == "workspace-relative-directory":
            if workspace is None:
                raise ConfigurationError("Workspace is required to validate a workspace-relative directory setting")
            workspace_directory_path(workspace, value)
        destination = effective
        for part in parts[:-1]:
            destination = destination.setdefault(part, {})
        destination[parts[-1]] = value
    return effective, configured


def _configured_reserved_paths(workspace, include_specification=True):
    """Return fixed and configured core paths without following optional content."""
    reserved = [".hai", ".git", STATE, INSTRUCTIONS,
                PROFILES, ".hai_env/agents", *LEGACY.values()]
    try:
        state_path = _safe_path(workspace, STATE)
    except ConfigurationError:
        # The fixed state path remains reserved even when its existing target is
        # unsafe; do not let unrelated state failure block isolated config reads.
        return reserved
    if not state_path.exists():
        return reserved
    try:
        state = _load_json(state_path)
    except ConfigurationError:
        # An invalid core state cannot authorize extra locations. Fixed paths still apply.
        return reserved
    if not isinstance(state, dict):
        return reserved
    activities = state.get("activities")
    if isinstance(activities, dict) and isinstance(activities.get("location"), str):
        reserved.append(activities["location"])
    features = state.get("features")
    if isinstance(features, dict):
        spec = features.get("specification")
        if (include_specification and isinstance(spec, dict)
                and isinstance(spec.get("location"), str)):
            reserved.append(spec["location"])
    return reserved


def _validate_configuration_target(workspace, agent, target):
    config_relative = f".hai_env/config/agents/{agent}.json"
    target_lexical = workspace / config_relative
    for relative in _configured_reserved_paths(workspace):
        try:
            reserved = _safe_path(workspace, relative)
        except ConfigurationError:
            # An invalid unrelated state path does not suppress diagnostics for
            # this agent's isolated file.
            continue
        if _overlaps(target, reserved) or _overlaps(target_lexical, workspace / relative):
            raise ConfigurationError(f"Agent configuration overlaps reserved path {relative}")
    siblings = workspace / ".hai_env/config/agents"
    if siblings.exists():
        if not siblings.is_dir():
            raise ConfigurationError("Agent configuration directory must be a directory")
        for sibling in siblings.iterdir():
            if sibling.name == f"{agent}.json":
                continue
            if _overlaps(target, sibling.resolve()) or _overlaps(target_lexical, sibling):
                raise ConfigurationError(f"Agent configuration aliases another agent configuration: {sibling.name}")
    if target.exists() and not target.is_file():
        raise ConfigurationError("Agent configuration must target a regular file")


def read_configuration(workspace, agent, contract):
    """Return effective settings and isolated diagnostics for one named agent.

    Missing configuration files and declared leaves use contract defaults. Existing
    malformed values are errors and never fall back to defaults. Unknown values are
    ignored for contracts with declared settings; an empty contract rejects a
    nonempty settings override so settings-free agents cannot activate one.
    """
    workspace = Path(workspace).resolve(strict=True)
    config_relative = f".hai_env/config/agents/{agent}.json"
    result = {"status": "unverified", "path": config_relative, "settings": {},
              "configured_fields": [], "issues": []}
    try:
        if not _NAME.fullmatch(agent):
            raise ConfigurationError("Agent name is not canonical")
        if not isinstance(contract, dict) or contract.get("agent") != agent:
            raise ConfigurationError("Validated contract does not belong to the requested agent")
        target = configuration_path(workspace, agent)
        if not target.exists():
            result["status"] = "defaulted"
            result["settings"] = _effective_settings(contract, {}, workspace)[0]
            return result
        data = _load_json(target)
        if (not isinstance(data, dict) or type(data.get("config_format_version")) is not int
                or data["config_format_version"] not in contract["supported_config_format_versions"]
                or not isinstance(data.get("settings"), dict)):
            raise ConfigurationError("Configuration requires a supported config_format_version and settings object")
        raw = data["settings"]
        if not contract["settings"] and raw:
            raise ConfigurationError("This agent declares no settings; nonempty overrides are invalid")
        effective, configured = _effective_settings(contract, raw, workspace)
        result.update(status="configured", settings=effective, configured_fields=configured)
        return result
    except (ConfigurationError, OSError, UnicodeError, RuntimeError) as exc:
        result["status"] = "invalid" if isinstance(exc, ConfigurationError) else "unverified"
        result["issues"].append({"code": "configuration", "path": config_relative,
                                 "agent": agent, "message": str(exc)})
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--agent", required=True)
    parser.add_argument("--contract", required=True,
                        help="Workspace-relative contract.json for this one agent")
    args = parser.parse_args()
    try:
        workspace = args.workspace.resolve(strict=True)
        if not workspace.is_dir() or not _NAME.fullmatch(args.agent):
            raise ConfigurationError("Workspace must be a directory and agent must have a canonical name")
        contract_path = _safe_path(workspace, args.contract)
        expected = f"{args.agent}/configuration/contract.json"
        origins = (".hai", ".hai_env")
        origin = next((item for item in origins
                       if args.contract == f"{item}/agents/{expected}"), None)
        if origin is None or contract_path.name != "contract.json":
            raise ConfigurationError("Contract must use the canonical selected-agent configuration/contract.json path")
        package_path = _safe_path(workspace, f"{origin}/agents/{args.agent}")
        if not contract_path.is_relative_to(package_path):
            raise ConfigurationError("Resolved contract must remain inside the selected agent package")
        contract = load_contract(contract_path, args.agent)
        result = read_configuration(workspace, args.agent, contract)
        result["ok"] = result["status"] in {"defaulted", "configured"}
        code = 0 if result["ok"] else 1
    except (ConfigurationError, OSError, RuntimeError) as exc:
        result = {"ok": False, "status": "invalid",
                  "issues": [{"code": "input", "message": str(exc)}]}
        code = 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
