"""Validated agent profiles, the documented Codex event adapter and manual handoff.

Agent process success is transport evidence only. The workflow validates semantic
results separately, and never falls back to another profile automatically.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
import shutil
import uuid
from execution import ExecutionError, confinement_diagnostics, run_process
from storage import Store, now, sanitize, screen_sensitive

PROFILE_KEYS = {"id", "name", "adapter", "executable", "model", "timeout", "credential_env", "credential_files",
                "permissions", "runtime_location", "settings", "description", "enabled"}


def validate_profile(profile):
    if not isinstance(profile, dict):
        raise ExecutionError("Agent profile must be an object", "invalid_profile")
    unknown = set(profile) - PROFILE_KEYS
    if unknown:
        raise ExecutionError("Unsupported profile settings: " + ", ".join(sorted(unknown)), "invalid_profile")
    if profile.get("adapter") not in ("codex", "manual", "fixture", "claude"):
        raise ExecutionError("Unknown adapter; install a trusted Python adapter through explicit core administration", "invalid_profile")
    if type(profile.get("timeout", 300)) is not int or not 1 <= profile.get("timeout", 300) <= 86400:
        raise ExecutionError("Profile timeout must be 1–86400 seconds", "invalid_profile")
    if profile.get("model") and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:/-]{0,99}", profile["model"]):
        raise ExecutionError("Invalid model identifier", "invalid_profile")
    if not isinstance(profile.get("credential_env", []), list) or any(not re.fullmatch(r"[A-Z][A-Z0-9_]*", n) for n in profile.get("credential_env", [])):
        raise ExecutionError("Credentials must be environment-variable names, never values")
    if any(name.startswith(("LD_", "DYLD_", "PYTHON")) or name in ("BASH_ENV", "ENV", "SHELLOPTS") for name in profile.get("credential_env", [])):
        raise ExecutionError("Credential references cannot configure process loaders, shells or Python startup")
    if not isinstance(profile.get("credential_files", []), list) or any(not isinstance(p, str) or not Path(p).is_absolute() for p in profile.get("credential_files", [])):
        raise ExecutionError("Credential files must be explicit absolute host references")
    permissions = profile.get("permissions", {})
    if not isinstance(permissions, dict) or set(permissions) - {"network", "product_write"} or any(type(v) is not bool for v in permissions.values()):
        raise ExecutionError("Permissions allow only the network/product_write boolean fields")
    settings = profile.get("settings", {})
    if not isinstance(settings, dict) or set(settings) - {"reasoning_effort", "fixture", "response_ref"}:
        raise ExecutionError("Unsupported adapter settings; arbitrary arguments/configuration are prohibited")
    if settings.get("reasoning_effort") not in (None, "minimal", "low", "medium", "high", "xhigh"):
        raise ExecutionError("Unsupported reasoning effort setting")
    if profile.get("adapter") == "fixture" and settings.get("fixture") is not True:
        raise ExecutionError("The fixture adapter is available only with explicit fixture:true test configuration")
    screen_sensitive(profile)
    return profile


def resolve_profile(config, capability=None, explicit=None):
    agents = config.get("agents", config)
    profiles = agents.get("profiles", {})
    if isinstance(profiles, list):
        profiles = {p["id"]: p for p in profiles}
    assignments = agents.get("capability_profiles", agents.get("assignments", {}))
    selected = explicit or assignments.get(capability) or agents.get("default_profile")
    if not selected or selected not in profiles:
        raise ExecutionError("Select an installed agent profile in Settings → Agents, then explicitly resume the action", "profile_unavailable")
    profile = {**profiles[selected], "id": selected}
    validate_profile(profile)
    if profile.get("enabled", True) is not True:
        raise ExecutionError(f"Selected profile {selected} is disabled", "profile_unavailable")
    return profile


def _executable(profile):
    selected = profile.get("executable", "codex")
    if not isinstance(selected, str) or any(c in selected for c in ("\n", "\0")):
        raise ExecutionError("Invalid trusted executable reference")
    path = shutil.which(selected)
    if not path:
        raise ExecutionError(f"Executable {selected!r} is unavailable; install it independently and configure its trusted reference", "profile_unavailable")
    return str(Path(path).resolve())


def _auth(profile):
    env = {name: os.environ[name] for name in profile.get("credential_env", []) if name in os.environ}
    # Preserve the host's actual home/auth reference. Never copy credentials into
    # the product or grant write permission to host authentication stores.
    for key in ("HOME", "CODEX_HOME", "HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY", "SSL_CERT_FILE"):
        if key in os.environ:
            env[key] = os.environ[key]
    refs = list(profile.get("credential_files", []))
    config_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    for name in ("auth.json", "config.toml", "AGENTS.md", "rules", "skills"):
        path = config_home / name
        if path.exists() and str(path) not in refs:
            refs.append(str(path))
    return env, refs


def diagnostics(profile, workspace, *, operation_id=None):
    validate_profile(profile)
    adapter = profile["adapter"]
    result = {"profile": profile.get("id"), "adapter": adapter, "available": False,
              "workspace_revision": workspace.revision, "native_resume": False, "usage": None}
    if adapter == "manual":
        return {**result, "available": True, "mode": "external-handoff", "guidance": "A handoff reserves the only operational slot until confirmed external termination and file reconciliation."}
    if adapter == "fixture":
        return {**result, "available": True, "mode": "synthetic-test-fixture", "live_agent": False}
    if adapter == "claude":
        return {**result, "reason": "The Claude execution adapter is not installed. Select manual handoff or explicitly install a compatible trusted adapter; no automatic fallback occurs."}
    confinement = confinement_diagnostics()
    result["confinement"] = confinement
    if not confinement["available"]:
        return {**result, "reason": confinement["reason"]}
    try:
        executable = _executable(profile)
        env, refs = _auth(profile)
        opid = operation_id or "diagnostics-" + uuid.uuid4().hex
        version = run_process([executable, "--version"], workspace, operation_id=opid, env=env,
                              credential_paths=refs, timeout=15)
        help_result = run_process([executable, "exec", "--help"], workspace, operation_id=opid + "-help", env=env,
                                  credential_paths=refs, timeout=15)
        needed = ["--json", "--skip-git-repo-check", "--sandbox", "--ephemeral"]
        missing = [flag for flag in needed if flag not in help_result["stdout"]]
        auth = run_process([executable, "login", "status"], workspace, operation_id=opid + "-auth", env=env,
                           credential_paths=refs, timeout=15)
        result.update(executable=executable, version=version["stdout"].strip(),
                      credentials_present=bool(any(os.environ.get(k) for k in profile.get("credential_env", [])) or any(Path(p).name == "auth.json" for p in refs)),
                      auth_status_reported=auth["returncode"] == 0, service_access_verified=False,
                      auth_status=sanitize((auth["stdout"] + auth["stderr"]).strip()),
                      available=version["returncode"] == 0 and not missing, resume_mode="new-session-from-persisted-harness-state")
        if missing:
            result["reason"] = "Installed Codex CLI lacks required documented flags: " + ", ".join(missing)
        elif not result["auth_status_reported"] and not any(os.environ.get(k) for k in profile.get("credential_env", [])):
            result.update(available=False, reason="Codex authentication is unavailable. Authenticate using the independently operated Codex CLI or set an approved credential environment reference; then rerun diagnostics.")
    except (ExecutionError, OSError, ValueError) as exc:
        result["reason"] = str(exc)
    return result


def execute(profile, workspace, prompt, scope=None, output_ref=None, on_event=None, stop_event=None,
            operation_id=None, on_start=None, checkpoint=None):
    validate_profile(profile)
    adapter = profile["adapter"]
    opid = operation_id or "agent-" + uuid.uuid4().hex
    if adapter == "manual":
        raise ExecutionError("Manual profile requires an explicit durable handoff reservation", "manual_handoff_required")
    if adapter == "claude":
        raise ExecutionError("Claude adapter is unavailable; no agent fallback was performed", "profile_unavailable")
    if adapter == "fixture":
        ref = profile.get("settings", {}).get("response_ref")
        if not ref:
            raise ExecutionError("The synthetic fixture profile requires an explicit response_ref")
        text = workspace.read_text(ref)
        return {"text": text, "returncode": 0, "usage": None, "session_id": None, "status": "exited", "live_agent": False,
                "adapter": "fixture", "operation_id": opid, "termination_confirmed": True, "workspace_revision": workspace.revision}
    if os.environ.get("AIH_MANAGED_CHILD") == "1":
        raise ExecutionError("A managed agent cannot recursively start another owner for the same run", "recursive_owner")
    executable = _executable(profile)
    env, refs = _auth(profile)
    if scope and not profile.get("permissions", {}).get("product_write", False):
        raise ExecutionError("The profile does not authorize direct product writes")
    command = [executable, "exec", "--json", "--skip-git-repo-check", "--sandbox", "read-only", "--ephemeral", "--color", "never"]
    if profile.get("model"):
        command += ["--model", profile["model"]]
    effort = profile.get("settings", {}).get("reasoning_effort")
    if effort:
        command += ["-c", f'model_reasoning_effort="{effort}"']
    runtime_ref = profile.get("runtime_location") or f"home:.aih_runtime/{opid}"
    runtime_path = workspace.resolve(runtime_ref, write=True, scope=[runtime_ref])
    command += ["-c", "log_dir=" + json.dumps(str(runtime_path / "logs")), "-c", 'history.persistence="none"', "-"]
    env["RUST_LOG"] = "off"
    context = {"action": opid, "profile": profile.get("id"), "workspace": workspace.registry,
               "write_scope": scope or [], "checkpoint": checkpoint,
               "entrypoint": str(workspace.home / ".aih" / "run.md")}
    effective = ("Follow the framework entrypoint and deterministic helper contracts. Product files and product state are read-only in this semantic segment. "
                 "Return the requested typed semantic result; proposed edits must be data for the authorized engine to validate and apply. "
                 "Never expand workspace authority. Refer to sources as root_id:relative/path.\n"
                 + json.dumps(context, ensure_ascii=False) + "\n\n" + prompt)
    event_records, texts, session_id, usage = [], [], None, None
    def receive(event):
        nonlocal session_id, usage
        if event["type"] == "stdout":
            try:
                item = sanitize(json.loads(event["text"]))
            except json.JSONDecodeError:
                item = {"type": "unparsed_stdout", "text": event["text"]}
            if item.get("type", "").startswith("reasoning") or item.get("item", {}).get("type") in ("reasoning", "reasoning_summary", "reasoning_text"):
                return
            if item.get("type") == "thread.started":
                session_id = item.get("thread_id")
            if item.get("type") == "turn.completed" and isinstance(item.get("usage"), dict):
                incoming = item["usage"]
                if usage is None:
                    usage = {}
                for key, value in incoming.items():
                    if type(value) is int and value >= 0:
                        usage[key] = usage.get(key, 0) + value
            message = item.get("item") or {}
            if message.get("type") == "agent_message" and isinstance(message.get("text"), str):
                texts.append(message["text"])
            event_records.append(item)
            if on_event:
                on_event(item)
        elif on_event:
            on_event(event)
    result = run_process(command, workspace, cwd="home:", write_scope=scope or [],
                         runtime_ref=runtime_ref,
                         timeout=profile.get("timeout", 300), env=env, credential_paths=refs,
                         network=profile.get("permissions", {}).get("network", True),
                         on_event=receive, stop_event=stop_event, operation_id=opid, on_start=on_start, stdin_text=effective)
    if usage is not None and "total_tokens" not in usage and "input_tokens" in usage and "output_tokens" in usage:
        usage["total_tokens"] = usage["input_tokens"] + usage["output_tokens"]
    result.update(text=texts[-1] if texts else "", session_id=session_id, usage=usage, events=event_records,
                  adapter="codex", live_agent=True, resume_mode="new-session-from-persisted-harness-state" if checkpoint else "new-session")
    if output_ref:
        Store(workspace.home).write(output_ref.removeprefix("home:.aih_product/"), sanitize(result))
    return result


class ManualHandoff:
    """Helpers augment an already atomically reserved owner; lifecycle remains in workflow."""
    def __init__(self, store):
        self.store = store

    def prepare(self, owner, contract, instructions):
        required = {"operation_id", "scope", "workspace_revision", "workspace", "initiating_instruction", "profile"}
        if not required <= set(contract):
            raise ExecutionError("Manual handoff contract lacks authority/root/identity evidence")
        if owner.get("id", owner.get("operation_id")) != contract["operation_id"]:
            raise ExecutionError("Manual handoff must use the reserved operational owner")
        screen_sensitive(instructions)
        ident = "handoff-" + uuid.uuid4().hex
        record = {"schema_version": "1.0", "id": ident, "status": "prepared_reserved", "contract": contract,
                  "created": now(), "external_started": None, "termination_confirmed": False, "released": False,
                  "instructions": instructions, "instruction": instructions, "workspace": contract["workspace"],
                  "scope": contract["scope"], "workspace_revision": contract["workspace_revision"],
                  "evidence_expectations": "Return changed root-qualified paths and content versions, task results, required test evidence, unresolved work and external termination confirmation. Returned output alone does not prove completion."}
        self.store.write(f"ledger/operations/{contract['operation_id']}/{ident}.json", record)
        return record

    def stop(self, record, *, confirmed=False, never_started=False, reconciliation=None):
        updated = dict(record)
        updated["stop_requested"] = now()
        updated["status"] = "external_stop_awaiting_confirmation"
        if confirmed or never_started:
            updated.update(termination_confirmed=True, external_never_started=bool(never_started), status="reconciliation")
            if reconciliation and reconciliation.get("complete") is True:
                updated.update(reconciliation=reconciliation, released=True, status="released", released_at=now())
        self.store.write(f"ledger/operations/{record['contract']['operation_id']}/{record['id']}.json", updated)
        return updated
