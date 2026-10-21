# Agent definition tools

`agent_tools.py` is a read-only Python 3.11+ format auditor and exact model
resolver for Windows, Linux, and macOS. It never spawns agents, changes state,
repairs registrations, or installs dependencies. Use a working interpreter per
[the tooling convention](../../conventions/tooling_conv.md).

It requires PyYAML 6.x for YAML parsing (tested with 6.0.1). If absent, explicitly
install into your chosen Python environment with `python -m pip install
'PyYAML>=6,<7'`; installation never runs automatically. HAI's state and
`.hai_env/` are not a Python virtual environment.

From the workspace root:

```text
python -B .hai/tools/agents/agent_tools.py audit
python -B .hai/tools/agents/agent_tools.py resolve --definition .hai/agents/environment-manager/SKILL.md --runtime /path/to/runtime.json
python -B .hai/tools/agents/test_agent_tools.py
```

Use `--workspace /path/to/workspace` before the command when running elsewhere.
The audit reads both catalogues, their referenced definitions, and optional model
profiles. This full authoring/migration audit is not ordinary startup discovery.
It checks YAML (including duplicate keys and string metadata), names, specialist
execution labels, the nine ordered headings, absence of agent H1 titles, canonical
links, catalogue description equality, collisions, path containment, legacy links,
and the profile schema. Missing workspace catalogue/profiles are valid and stay
absent. Legacy rows and conflicts are reported with names and never removed;
valid independent registrations remain in the result.

Provide a UTF-8 JSON capability snapshot using current runtime evidence, for
example a runtime advertising exactly these combinations:

```json
{
  "models": {
    "gpt-6-luna": ["low", "medium", "high", "xhigh", "max"],
    "gpt-6.1-sol": ["low", "medium", "high", "xhigh", "max", "ultra"],
    "gpt-6-astra": ["low", "medium", "high", "xhigh", "max", "ultra"]
  }
}
```

The resolver reads only the selected definition, local profiles, and the supplied
snapshot; it accepts no fallback. This example does not establish availability in
another session. It reports the requested class, effort, model when resolved, and
any unavailable combination. Missing profiles return an issue; the caller applies
the separately documented startup bootstrap or human override instead. Neither
exception is inferred by the helper. A supplied snapshot cannot prove freshness
or runtime fork/permission support; leader must verify those before spawning.

JSON output uses `ok` and `issues`; audit adds `agents` and profile status,
resolution adds `request`. Exit codes are `0` for supported checks passing, `1`
for detected validation/unavailability issues, and `2` for fatal input errors
(including unreadable selected definitions or runtime files). Missing Python or
PyYAML fails before structured output. No output is proof of semantic ownership,
input sufficiency, reference meaning, core-state validity, or successful spawning.
The auditor recognizes simple three-column catalogue tables, not arbitrary
Markdown. Review complex fences/Markdown manually; unrelated tables are rejected.
Unregistered definitions are not reconstructed or registered by the audit.

Tests use temporary fixtures and standard-library unittest with PyYAML; run them
when modifying the helper. OS-specific symlink checks may skip when unavailable.
