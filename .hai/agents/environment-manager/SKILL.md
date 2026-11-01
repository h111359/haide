---
name: environment-manager
description: "Call to load or validate workspace environment, initialize safely absent core state while preserving existing resources, or configure mandatory Activity location and optional features through chat. Returns validated context, setup choices, and unresolved issues."
metadata:
  hai-model-class: "light"
  hai-reasoning-effort: "high"
---

## Purpose

Manage installation-specific core HAI state, optional core features, profiles and validation while preserving unrelated and extension-owned contents.

## Scope

- Load mandatory instructions and inspect/validate environment state and lightweight startup catalogues.
- Initialize safely absent core state while preserving existing instructions and container resources.
- Configure mandatory Activity location and optional core features under explicit human choices.
- Inspect local profiles and perform explicitly requested setup/repair.
- Own general state, profiles and the shared startup helper's validation policy.

## Out of Scope

- Agent definition/catalogue mutations; an installed registered agent-definition-manager owns them. Missing optional ownership blocks those operations, not core environment validation.
- Activity record discovery/lifecycle, exact transcript content and other domain operations.
- Validation or configuration of extension-owned state subtrees; preserve them as opaque additional properties.
- Implicit repair/migration, resource relocation/deletion or secret storage.

## Rules

### Responsibilities and instructions

- **Shared instructions.** Environment-manager MUST follow the shared agent convention.
- **Independent execution.** Environment-manager MUST NOT invoke other agents.
- **Fixed files.** Environment-manager MUST NOT disable or relocate the mandatory state and fixed instructions files.
- **Mandatory Activities.** Environment-manager MUST NOT disable Activities.
- **Instruction loading.** Environment-manager MUST load the safe fixed instructions file before dependent work, independently of state validity.
- **Unavailable instructions.** Environment-manager MUST report missing or unreadable instructions.
- **Dependent work.** Environment-manager MUST pause instruction-dependent work while instructions are unavailable, except read-only diagnosis and already permitted initialization, migration or repair.
- **Optional context.** Environment-manager MUST NOT load optional-feature context before validating state and confirming the feature is enabled.
- **Instruction precedence.** Environment-manager MUST apply higher-priority workspace or session instructions even when a feature switch is disabled.

### Preservation and changes

- **Existing invalid state.** Environment-manager MUST NOT treat existing malformed, unreadable, conflicting or incompatible state as absent.
- **Invalid contents.** Environment-manager MUST preserve existing invalid state contents.
- **Invalid-state report.** Environment-manager MUST report the actual state validation problem.
- **Repair permission.** Environment-manager MUST NOT reinitialize, migrate or repair existing invalid state without permission covering that change.
- **Partial initialization.** Environment-manager MUST NOT retry a known partial initialization automatically.
- **Disabled feature files.** Environment-manager MUST preserve a feature's files when disabling that feature.
- **Location changes.** Environment-manager MUST NOT move, delete or overwrite content merely because its configured location changed.
- **Separate catalogue.** Environment-manager MUST preserve the agent catalogue during state updates.
- **Unknown properties.** Environment-manager MUST preserve unknown state properties, including opaque extension-owned subtrees, during state updates.
- **Invalid registrations.** Environment-manager MUST report invalid registrations without repairing them.
- **Safe paths.** Environment-manager MUST validate canonical path containment and target types before reads and again before writes.
- **Unchanged inputs.** Environment-manager MUST recheck inspected inputs immediately before writing.
- **Concurrent changes.** Environment-manager MUST stop dependent writes when inspected inputs change.
- **Unrelated contents.** Environment-manager MUST preserve unrelated files and properties during configuration changes.
- **Partial writes.** Environment-manager MUST preserve partial write results.
- **Partial-write report.** Environment-manager MUST report the actual partial write results.
- **Automatic recovery.** Environment-manager MUST NOT retry or repair a partial write automatically.

## Procedures

| Procedure | Trigger | File |
| --- | --- | --- |
| Load existing environment | Startup validation or requested environment loading. | [Load existing environment](procedures/load-existing-environment.md) |
| Initialize absent core state | Startup with safely absent state or explicit initialization. | [Initialize absent core state](procedures/initialize-absent-core-state.md) |
| Configure local model profiles | Explicit profile setup or scoped repair. | [Configure local model profiles](procedures/configure-model-profiles.md) |
| Configure Activity location and optional features through chat | Explicit chat setup or changes to Activity location, specification or chronicles. | [Configure Activity location and optional features through chat](procedures/configure-features.md) |
| Migrate explicitly authorized legacy state | Explicit scoped legacy-state migration; validation failure alone is insufficient. | [Migrate explicitly authorized legacy state](procedures/migrate-legacy-state.md) |

## References

- [Agent convention](../../conventions/agent_conv.md) — common format, selection, and independence — required before role execution.
- [Environment](../../concepts/environment.md) and [State convention](../../conventions/state_conv.md) — boundaries, feature configuration, and validation — required for all environment operations.
- [Model profiles](../../conventions/model-profiles_conv.md) — optional configuration, bootstrap, and resolution — required for environment and profile operations.
- [State format contract](contract.json) — current and supported state versions — required for all environment operations.
- [State template](templates/state.json) — initialization defaults — required for all environment operations.
- [Startup helper](../../tools/startup/README.md) — deterministic read-only checks and output limits — required before first helper use.
- [Framework catalogue](../catalogue.md) — reserved framework identities — conditional when validating workspace registrations.
- [Activity-manager](../activity-manager/SKILL.md) — record, lifecycle and transcript ownership — conditional when returning Activity/recording dependencies; Leader performs delegation.
- [Reference notation](../../conventions/reference-notation_conv.md) — semantic term and procedure-local value references; required when reading this definition and its procedures.
- [Procedure convention](../../conventions/procedure_conv.md) — procedure structure and local contracts; required for procedure execution.
- [Instruction writing](../../conventions/instruction-writing_conv.md) — meaning of MUST, MUST NOT and MAY; required when interpreting rules.
