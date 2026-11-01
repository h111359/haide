"""Explicitly migrate format-2 specification settings into agent configuration."""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import stat
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "agents"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "configuration"))
import startup_check as startup
from agent_tools import Invalid, load_json
from configuration_tools import (ConfigurationError, configuration_path,
                                 load_contract, workspace_directory_path)

SPEC_AGENT = "specification-manager"
CONTRACT = f".hai_env/agents/{SPEC_AGENT}/configuration/contract.json"
STATE = ".hai_env/state.json"
BACKUP = ".hai_env/state.json.format2-backup"
TEMP_STATE = ".hai_env/state.json.format3-candidate"


def _bytes_json(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=True, indent=2) + "\n").encode("utf-8")


def _write_exclusive(path: Path, content: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        offset = 0
        while offset < len(content):
            offset += os.write(descriptor, content[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _ensure_unaliased(workspace: Path, relative: str, *, kind: str,
                      must_exist: bool = True) -> tuple[int, int, int] | None:
    """Reject symlink components and hard-linked files used by this migration."""
    current = workspace
    parts = Path(relative).parts
    for index, part in enumerate(parts):
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError:
            if must_exist and index == len(parts) - 1:
                raise Invalid(f"Migration {kind} path is missing: {relative}")
            continue
        if stat.S_ISLNK(info.st_mode):
            raise Invalid(f"Migration {kind} path must not use symlinks: {relative}")
        if index < len(parts) - 1 and not stat.S_ISDIR(info.st_mode):
            raise Invalid(f"Migration {kind} parent must be a directory: {relative}")
    if not current.exists():
        return None
    info = current.stat()
    if kind == "file":
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise Invalid(f"Migration file must be a regular unaliased file: {relative}")
        return info.st_dev, info.st_ino, info.st_nlink
    if kind == "directory" and not stat.S_ISDIR(info.st_mode):
        raise Invalid(f"Migration directory must be a directory: {relative}")
    return info.st_dev, info.st_ino, info.st_nlink


def _contract(workspace: Path, registered: list[dict]) -> tuple[dict, bytes]:
    if not any(item.get("name") == SPEC_AGENT and item.get("origin") == ".hai_env"
               for item in registered):
        raise Invalid("Specification-manager must be validly registered as an installed workspace agent")
    package = startup.safe_path(workspace, f".hai_env/agents/{SPEC_AGENT}")
    path = startup.safe_path(workspace, CONTRACT)
    if not path.is_relative_to(package):
        raise Invalid("Specification-manager contract resolves outside its installed package")
    contract = load_contract(path, SPEC_AGENT)
    required = {"enabled", "location"}
    if (contract["contract_format_version"] != 2
            or contract["current_config_format_version"] != 1
            or set(contract["settings"]) != required
            or contract["settings"]["enabled"] != {"type": "boolean", "default": False}
            or contract["settings"]["location"].get("type") != "workspace-relative-directory"
            or contract["settings"]["location"].get("default") != ".hai_env/specifications"):
        raise Invalid("Installed Specification-manager contract is not compatible with this extraction")
    return contract, path.read_bytes()


def _write_status(path: str, exists: bool) -> dict:
    return {"path": path, "created": exists}


def migrate(workspace: Path, apply: bool = False) -> dict:
    workspace = workspace.resolve(strict=True)
    if not workspace.is_dir():
        raise Invalid("Workspace must be an existing directory")
    startup_result = startup.check(workspace)
    if (startup_result.get("environment") != "valid"
            or startup_result.get("instructions_status") != "loaded"):
        raise Invalid("A valid initialized environment and readable mandatory instructions are required")
    if startup_result.get("state_format_version") != 2:
        raise Invalid("Migration source must be a valid format-2 state; current or invalid formats are not rewritten")
    original_path = startup.safe_path(workspace, STATE)
    original_identity = _ensure_unaliased(workspace, STATE, kind="file")
    original_bytes = original_path.read_bytes()
    original_mode = stat.S_IMODE(original_path.stat().st_mode)
    original = load_json(original_path)
    template = load_json(startup.safe_path(workspace, startup.TEMPLATE))
    state_format_contract = startup.state_contract()
    startup.state_context(workspace, original, template, state_format_contract)
    legacy = original["features"]["specification"]

    owner_contract, contract_bytes = _contract(workspace, startup_result["agents"])
    target = configuration_path(workspace, SPEC_AGENT)
    if target.exists():
        raise Invalid("Specification-manager configuration already exists; resolve the destination before extraction")
    workspace_directory_path(workspace, legacy["location"],
                              ignore_legacy_specification=True)
    backup = startup.safe_path(workspace, BACKUP)
    candidate_path = startup.safe_path(workspace, TEMP_STATE)
    _ensure_unaliased(workspace, ".hai_env/config", kind="directory", must_exist=False)
    _ensure_unaliased(workspace, ".hai_env/config/agents", kind="directory", must_exist=False)
    _ensure_unaliased(workspace, BACKUP, kind="file", must_exist=False)
    _ensure_unaliased(workspace, TEMP_STATE, kind="file", must_exist=False)
    if backup.exists() or candidate_path.exists():
        raise Invalid("A prior migration backup or candidate exists; inspect it and resolve the partial result")

    candidate_state = copy.deepcopy(original)
    candidate_state["state_format_version"] = 3
    del candidate_state["features"]["specification"]
    startup.state_context(workspace, candidate_state, template, state_format_contract)
    config_document = {
        "config_format_version": owner_contract["current_config_format_version"],
        "settings": copy.deepcopy(legacy),
    }
    config_bytes = _bytes_json(config_document)
    state_bytes = _bytes_json(candidate_state)
    plan = {"ok": True, "status": "ready" if not apply else "in_progress",
            "source_state_format_version": 2, "target_state_format_version": 3,
            "specification": {"enabled": legacy["enabled"], "location": legacy["location"]},
            "configuration": _write_status(".hai_env/config/agents/specification-manager.json", False),
            "backup": _write_status(BACKUP, False), "state_updated": False,
            "applied": bool(apply), "issues": []}
    if not apply:
        return plan

    current_contract_path = startup.safe_path(workspace, CONTRACT)
    if (original_path.read_bytes() != original_bytes
            or current_contract_path.read_bytes() != contract_bytes
            or target.exists() or backup.exists() or candidate_path.exists()):
        raise Invalid("Inspected migration inputs changed before the first write")
    try:
        _write_exclusive(backup, original_bytes)
        plan["backup"] = _write_status(BACKUP, backup.exists())
        backup_identity = _ensure_unaliased(workspace, BACKUP, kind="file")
        if backup.read_bytes() != original_bytes:
            raise Invalid("Recoverable backup verification failed; preserve the partial backup")
        if (original_path.read_bytes() != original_bytes
                or _ensure_unaliased(workspace, STATE, kind="file") != original_identity):
            raise Invalid("Source state changed after its recoverable backup was created")
        current_contract_path = startup.safe_path(workspace, CONTRACT)
        if current_contract_path.read_bytes() != contract_bytes or target.exists():
            raise Invalid("Contract or destination changed before configuration creation")
        configuration_path(workspace, SPEC_AGENT)
        for relative in (".hai_env/config", ".hai_env/config/agents"):
            directory = startup.safe_path(workspace, relative)
            if not directory.exists():
                directory.mkdir()
                plan.setdefault("created_directories", []).append(relative)
            _ensure_unaliased(workspace, relative, kind="directory")
        target = configuration_path(workspace, SPEC_AGENT)
        _write_exclusive(target, config_bytes)
        plan["configuration"] = _write_status(".hai_env/config/agents/specification-manager.json", target.exists())
        configuration_identity = _ensure_unaliased(
            workspace, ".hai_env/config/agents/specification-manager.json", kind="file")
        if (target.read_bytes() != config_bytes or original_path.read_bytes() != original_bytes
                or _ensure_unaliased(workspace, STATE, kind="file") != original_identity
                or current_contract_path.read_bytes() != contract_bytes):
            raise Invalid("Configuration verification or source recheck failed; preserve partial results")
        workspace_directory_path(workspace, legacy["location"],
                                  ignore_legacy_specification=True)
        if candidate_path.exists():
            raise Invalid("Migration candidate path appeared concurrently")
        _write_exclusive(candidate_path, state_bytes)
        os.chmod(candidate_path, original_mode)
        candidate_identity = _ensure_unaliased(workspace, TEMP_STATE, kind="file")
        if (load_json(candidate_path) != candidate_state
                or original_path.read_bytes() != original_bytes
                or _ensure_unaliased(workspace, STATE, kind="file") != original_identity
                or target.read_bytes() != config_bytes):
            raise Invalid("Candidate state or source recheck failed; preserve partial results")
        current_contract_path = startup.safe_path(workspace, CONTRACT)
        if current_contract_path.read_bytes() != contract_bytes:
            raise Invalid("Contract changed before state replacement; preserve partial results")
        if (original_path.read_bytes() != original_bytes
                or _ensure_unaliased(workspace, STATE, kind="file") != original_identity
                or target.read_bytes() != config_bytes
                or _ensure_unaliased(workspace, ".hai_env/config/agents/specification-manager.json",
                                     kind="file") != configuration_identity
                or backup.read_bytes() != original_bytes
                or _ensure_unaliased(workspace, BACKUP, kind="file") != backup_identity
                or load_json(candidate_path) != candidate_state
                or _ensure_unaliased(workspace, TEMP_STATE, kind="file") != candidate_identity):
            raise Invalid("Source, destination, or candidate changed immediately before state replacement")
        os.replace(candidate_path, original_path)
        plan["state_updated"] = True
        if original_path.read_bytes() != state_bytes:
            raise Invalid("Replaced state bytes differ from the complete validated candidate")
        verified = startup.check(workspace)
        spec_status = verified.get("agent_configurations", {}).get(SPEC_AGENT, {})
        expected_effective = {"enabled": legacy["enabled"], "location": legacy["location"]}
        if (verified.get("environment") != "valid"
                or verified.get("state_format_version") != 3
                or spec_status.get("status") != "configured"
                or spec_status.get("settings") != expected_effective
                or load_json(original_path) != candidate_state
                or load_json(target) != config_document):
            raise Invalid("Post-write startup verification failed; preserve backup and partial results")
        plan["status"] = "migrated"
        return plan
    except Exception as exc:
        plan["ok"] = False
        plan["status"] = "partial" if (backup.exists() or target.exists() or candidate_path.exists()) else "failed"
        plan["issues"].append({"code": "migration", "message": str(exc)})
        return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--apply", action="store_true",
                        help="Apply the explicit migration; omission performs a read-only rehearsal")
    args = parser.parse_args()
    try:
        result = migrate(args.workspace, args.apply)
        code = 0 if result["ok"] else 1
    except (Invalid, ConfigurationError, OSError, UnicodeError, RuntimeError) as exc:
        result = {"ok": False, "status": "blocked",
                  "issues": [{"code": "migration", "message": str(exc)}]}
        code = 1
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
