# Startup

## Description

Establish validated startup context through the read-only startup helper and necessary specialist handoffs, and return environment findings and relevant next actions.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:task] | Human question or task. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:environment_context] | Previously validated Activity/chronicles context, separate agent-config results and registered workspace entries. | Optional | Startup helper or environment-manager | Run read-only startup validation; absence does not prevent framework selection or independent diagnosis, while substantive work waits for usable Activity context. |

## Prerequisites

The startup helper README and shared state/model-profile conventions are available; previous observations are usable only while their inspected inputs remain unchanged.

## Rules

- **Minimal initialization.** Leader MAY request minimal startup initialization when core state is safely absent, creating an empty fixed instructions file only if that file is also safely absent and preserving existing contents.
- **Existing environment problems.** Leader MUST obtain the applicable repair or migration permission before changing existing invalid state, missing initialized instructions, incompatible state or known partial initialization.
- **Optional setup.** Leader MUST NOT make optional setup a prerequisite for otherwise valid ordinary work.
- **Relevant extensions.** Leader MAY include an optional extension in the startup menu ONLY IF it is registered and relevant to the user's task.

## Steps

1. Establish [input:workspace_root], [input:task] and [input:authority]. Load the safe fixed mandatory [input:instructions] independently of state validation, recording missing/unreadable status for the setup/diagnosis branch.

2. Validate Leader's own declared configuration contract and read its saved configuration with the shared read-only configuration helper; missing files use its empty defaults and nonempty settings are invalid. Preserve independent diagnosis if configuration is invalid. Run the shared read-only startup helper with the explicit workspace and a working interpreter. Compare any [input:environment_context] with its unchanged inspected inputs and retain only still-valid evidence.

3. If the helper cannot run, report that limit and prepare complete fallback validation for environment-manager. If state is safely absent, prepare its minimal initialization assignment. Otherwise retain the helper's actual core/isolated issues and route only explicitly authorized repairs or migration.

4. For a required environment-manager invocation, validate its configuration contract and read its configuration without requiring state, profiles or an owner invocation. Include that evidence in the handoff; invalid configuration permits diagnosis/scoped repair rather than ordinary dependent work. Resolve exact supported settings under the model-profile convention. If and only if profiles are absent and startup needs initialization/fallback validation, report inherited startup bootstrap settings and use a supported inherited invocation; a present invalid profile instead needs an explicit supported human override.

5. Monitor that assignment and receive verification, or retain its precise unresolved dependency. Build [output:startup_context] from actual core validation, independent registrations, instructions/profile status and available settings.

6. Validate/read Activity-manager's declared configuration through the shared helper and include its evidence when invoking it; its empty settings contract does not replace shared chronicles assurance. If compatible usable context and supported Activity-manager invocation are available, execute [Coordinate Activity](coordinate-activity.md): pass [input:workspace_root] to target `workspace_root`, [input:instructions] to `instructions`, [input:task] to `task`, [input:authority] to `authority`, and validated environment/store assurance from [output:startup_context] to `environment_context`; pass already verified continuity to `current_record` only when available.

7. Receive actual current-record/absence/creation evidence before describing current work. If context or invocation remains unusable, record discovery as unverified and keep substantive work pending.

8. Build [output:next_actions] from [output:startup_context] and the discovery result/limit: offer verified resumption, or meaningful new work after verified absence; recommend Additional setup after initialization and offer it for existing usable environments.

9. Present validated mandatory Activity location, central chronicles status/effective prompt threshold and the separate bounded `agent_configurations['specification-manager']` result when available. Report format-2 migration_required without reading legacy specification values as active settings. Include profile setup/repair or scoped core repair/migration where reported, and specification actions only when the registered installed owner has valid enabled settings, with accurate directory availability. An absent directory is not missing configuration and never authorizes creation. If Specification-manager is absent, report the optional installation dependency without invalidating core state or loading library resources. Add a task-relevant optional registered extension only when appropriate.

10. Collect only unresolved setting choices, accepting partial/deferred setup. Route Activity/chronicles/profile changes to Environment-manager and specification enablement/location setup to Specification-manager; include separate core/Activity and owner-settings evidence. Route explicitly authorized format-2-to-3 extraction to Environment-manager; include effective recording boundaries or separate location/history work in the request when relevant.

11. Execute [Review and report](review-and-report.md): pass [input:workspace_root] to target `workspace_root`, [input:instructions] to `instructions`, [input:task] to `task`, [input:authority] to `authority`, actual discovery evidence or the startup/diagnosis exception described in the shared conventions to `activity_context`, [output:startup_context]/[output:next_actions] and actual delegation evidence to `returned_results`, and the requested startup objective/criteria to `acceptance_criteria`.

12. Return [output:startup_context] and [output:next_actions] with reviewed outcomes and exact unresolved limits.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:startup_context] | Validated environment, mandatory instructions, profiles, independent registrations and settings. | Report actual validation and isolated errors; do not claim unavailable checks passed. |
| [output:next_actions] | Concise relevant next actions. | Include verified current Activity continuity and setup/repair needs; initialization itself does not wait for optional setup. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
