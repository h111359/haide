# Configure local model profiles

## Description

Configure explicitly requested specialist model mappings against current runtime evidence, and return verified profiles, override use, and unresolved combinations.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:activity_context] | Stable current Activity ID, path and relevant record context for substantive work; applicable bootstrap/diagnosis exception when no record is needed. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:profile_choices] | Requested or agreed class mappings for all three required classes. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:runtime_evidence] | Current supported model/effort combinations and any explicit supported invocation override. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |

## Prerequisites

Read the shared Environment, state and model-profile references plus the installed [state contract](../contract.json) and [state template](../templates/state.json) as relevant. Read the startup-helper README before first use; do not reread unchanged knowledge already in context. Supplied Activity context covers substantive setup/repair; missing profiles permit new configuration, while malformed existing material needs explicit repair scope.

## Rules

None.

## Steps

1. Establish [input:workspace_root], load [input:instructions] and record the substantive operation under [input:activity_context]/[input:authority].

2. Inspect existing safe canonical profiles and retrieve already supplied [input:profile_choices]. Compare requested model/effort combinations with [input:runtime_evidence]; report unresolved/unavailable combinations for decision before affected configuration.

3. Parse duplicate-free existing JSON, or establish safe absence. If malformed/conflicting material lacks explicit repair scope, return that dependency.

4. Prepare only chosen mappings while retaining unmentioned settings and additional properties; validate the complete three-class profile under the model-profile convention.

5. Recheck source contents and containment, then exclusively create an absent file or replace only the unchanged inspected file.

6. Read back and verify the chosen mappings, preserved properties and unchanged core state/catalogue. Return [output:profile_result] with runtime evidence limits, invocation/bootstrap/override use and exact partial failures or unresolved pairs.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:profile_result] | Configured mappings, runtime evidence, bootstrap/override use and unresolved pairs. | Verify safe duplicate-free file, requested mappings, preserved unrelated properties and unchanged state/catalogue; do not imply universal runtime support. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
