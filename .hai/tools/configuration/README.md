# Agent configuration tools

`configuration_tools.py` provides a read-only Python 3.11+ standard-library
loader for settings owned by one selected agent. Agent packages declare
`hai-configuration-contract: "configuration/contract.json"` in their `SKILL.md`.
The contract stays with the package; workspace overrides live at
`.hai_env/config/agents/<agent-name>.json`.

Run a bounded check for one selected agent from the workspace root:

```text
<absolute-python-executable> -B .hai/tools/configuration/configuration_tools.py \
  --agent git-manager \
  --contract .hai_env/agents/git-manager/configuration/contract.json
<absolute-python-executable> -B .hai/tools/configuration/test_configuration_tools.py
```

Pass `--workspace /path/to/workspace` when running from elsewhere. The contract
argument must be the canonical `configuration/contract.json` inside that agent's
framework or workspace package. The command reads that one contract and that
agent's saved configuration. It does not scan catalogues, definitions, or other
agents' configurations.

Contract format 1 supports Boolean leaves. Contract format 2 also supports
`workspace-relative-directory` leaves with string defaults; a matching `agent`
name, current and supported positive configuration versions, and a `settings`
object are required for both. Each dotted setting name declares exactly a `type`
and compatible `default`. A settings-free agent uses an empty object. Saved files use a
`config_format_version` and nested `settings` object. Missing files and missing
declared leaves use contract defaults. A present malformed file, unsupported
version, wrong container, or wrong type is reported as invalid and never silently
falls back to defaults. Unknown values in a configurable agent's file are ignored
and never returned as active settings; a settings-free agent's nonempty override is
invalid.

The Python API is `load_contract(path, expected_agent)`,
`read_configuration(workspace, agent, contract)`, `configuration_path(workspace,
agent)`, `workspace_directory_path(workspace, value, reserved_paths=())`, and
`load_json(path)`. `workspace_directory_path` checks workspace containment,
reserved core/config/profile/Activity paths and existing directory type even when
the owning setting is disabled. It accepts extra caller-supplied reservation paths
for candidate-state validation. `load_contract` and `load_json` raise
`ConfigurationError` for invalid or unreadable input. `read_configuration` returns
`status` (`defaulted`, `configured`, `invalid`, or `unverified`), the canonical
configuration path, effective declared settings, configured dotted fields, and
isolated issues. It performs no writes. Configuration targets that escape the
workspace or overlap core state, mandatory instructions, profiles, Activities,
specifications, or other agent configuration files are rejected.

The command emits JSON. Exit `0` means the selected agent's saved file is valid or
absent and its defaults can be used; exit `1` reports an isolated configuration
path/file/schema issue; exit `2` reports an invalid command input or contract.
Core state is validated independently by the startup helper. A missing agent
configuration remains `defaulted` even when core state is invalid; an invalid
state does not silently become valid or block unrelated read-only configuration
diagnostics.

The startup helper reserves `.hai_env/config` against core state, Activity,
specification, profile, and mandatory-instructions paths. Normal startup does not
open agent definitions or contracts and does not load agent configuration. A
configuration issue therefore remains isolated to an explicit check or the owner
agent's operation.
