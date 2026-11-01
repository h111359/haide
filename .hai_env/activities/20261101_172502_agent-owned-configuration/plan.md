# Plan: configuration owned by each agent

The agreed direction is to make configuration ownership standard for all agents. This is a proposed implementation plan; implementation has not started.

## Main ideas

- Every agent declares a **configuration contract**: its supported settings, defaults and validation rules. Agents without settings declare that explicitly.
- Save workspace settings only when needed, in `.hai_env/config/agents/<agent-name>.json`. Keeping them outside agent packages protects them during upgrades.
- Add proposed SKILL metadata `hai-configuration-contract: "configuration/contract.json"`, pointing to the contract inside each package.
- Keep minimal shared `.hai_env/state.json`, including the Activity location. Instructions, catalogues and model profiles keep their existing locations.
- Move Git settings first. Moving specification and chronicles settings is a separate, optional later step.

## Affected files

| Area | Main files and changes |
| --- | --- |
| New shared rules | Add `.hai/concepts/agent-configuration.md` and `.hai/conventions/agent-configuration_conv.md` to explain ownership, defaults, validation and migration. |
| Existing rules | Update `.hai/conventions/` files `agent_conv.md`, `state_conv.md`, `framework-layout_conv.md`, `model-profiles_conv.md`; update `.hai/concepts/` files `agent.md`, `environment.md`, `hai.md`. |
| Every agent | Update each `SKILL.md` and add `configuration/contract.json` in the core, installed and source packages listed below. |
| Agent-definition-manager | Update its `SKILL.md`, `concepts/definition-management.md` and applicable `procedures/` so creation, updates, validation, registration and installation enforce the new standard. |
| Shared tools | Add `.hai/tools/configuration/`; update `.hai/tools/agents/agent_tools.py` and `.hai/tools/startup/startup_check.py`, their documentation and tests. |
| Git-manager | In source and installed packages, update `conventions/git-configuration_conv.md`, `procedures/configure-integrations.md`, `scripts/validate_git_configuration.py`, related SKILL/procedure references and tests. |
| Documentation and packaging | Update `.hai/start.md`, `README.md`, `INSTALL.md`, `hai_agents_library/README.md`, migration guidance and Release-manager's packaging checks. Ship contracts and helpers; exclude workspace settings. |

All **eight runtime agents** are covered:

- Core (`.hai/agents/`): Leader, Environment-manager, Activity-manager.
- Workspace (`.hai_env/agents/`): Advisor, Agent-definition-manager, Git-manager, Specification-manager, Release-manager.

The **four source packages** under `hai_agents_library/agents/` are `agent-definition-manager`, `git-manager`, `specification-manager` and `release-manager`. Update these sources first, then install reviewed complete packages while preserving workspace settings.

## Implementation order

1. **Define the standard.** Agree the contract format, setting ownership and behavior for missing or invalid files. Missing files use declared defaults; invalid settings produce clear errors.
2. **Build validation.** Add the shared reader and definition checks. Invalid optional-agent settings must not block unrelated agents or core startup. Loading configuration must not depend on invoking its owner first.
3. **Update every agent.** Add contracts and metadata. Make Agent-definition-manager enforce them for every future agent. Keep settings-free agents free of unnecessary workspace files.
4. **Move Git settings.** Transfer Git, GitHub and auto-push values into Git-manager's configuration. Verify the new file before removing old authoritative fields. Preserve unrelated state and resolve conflicting values explicitly.
5. **Update documentation and migrate safely.** Recheck source/installed differences, keep recoverable copies, rehearse the migration, and preserve settings and Activity records. Report partial failures rather than silently retrying.

**Optional later step:** move specification settings to Specification-manager and chronicles settings to Activity-manager. This also affects Environment-manager's state contract/templates/migration procedures, Leader's startup/recording handoffs and both feature owners' procedures. The proposed state-format-3 migration needs separate acceptance; it is not part of the initial Git move.

## Checks before completion

- Run agent-definition, startup, shared-configuration and Git tests; audit all eight runtime contracts and four source packages.
- Check defaults, invalid files, safe paths, missing optional agents and startup without the source library.
- Rehearse settings migration and interrupted updates. Confirm one authoritative location per moved setting, unchanged effective values, preserved records and upgrades that retain workspace settings.

No implementation tests were needed for this editorial revision. The [previous detailed plan](files/revisions/plan/20261101_143853_01.md) remains available for implementation detail and reference.
