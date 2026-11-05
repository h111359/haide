# Discover and create

## Description

Establish the sole-current Activity context, creating records only within the user's request and agreed scope, and return verified identity and continuity findings.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:operation] | Selected record/lifecycle or assigned substantive-work operation. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:environment_context] | Caller-validated compatible environment and safe activities.location; direct HAI calls have no standalone bypass. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:new_work] | Meaningful new substantive objective authorized by the human, or explicit scoped record migration. | Optional | Human task and caller scope | Discover only; selection or a new chat creates no record. |
| [input:initial_input] | Initial human input and source. | Optional | Human text and explicit migration provenance | Preserve as supplied; it may remain empty until supplied, never synthesize it. |

## Prerequisites

Read the package [Activity concept](../concepts/activity.md) and [Activity convention](../conventions/activity_conv.md). Caller-validated compatible environment/store context and local path/type validation are required. The shared startup context helper may independently perform the read-only discovery checks for Leader; record creation and mutation remain with Environment-manager.

## Rules

None.

## Steps

1. Establish [input:workspace_root], load [input:instructions] and resolve [input:operation]/[input:authority] with [input:environment_context]. Validate the supplied store and existing ancestors before inspection.

2. Validate each direct child candidate as a contained nonlinked directory before reading its regular safe state file. Check sole-current consistency, supported state, IDs and required records under the Activity convention; return invalid/missing/conflicting state if consistency cannot be established.

3. If current work exists, load only relevant artifacts and return [output:activity_context] with stable ID/path, subject, lifecycle, steps, unresolved decisions and continuity.

4. If no current record exists and [input:new_work] supplies no meaningful authorized creation objective, return verified absence without writes.

5. For authorized new work, recheck store consistency, target absence and safe paths. Exclusively create an absent store/current folder and mandatory state, input and log using the convention's initial schema.

6. Write [input:initial_input] exactly as supplied with source provenance, or retain it empty until supplied. Label an explicitly authorized migration summary as such.

7. Read back mandatory records and verify stable identity and sole active folder. Return [output:activity_context] with actual creation or precise partial-write/verification findings.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:activity_context] | Stable ID/path, subject, lifecycle, steps, continuity and unresolved decisions. | Verify sole-current consistency and mandatory records; actual creation only within the agreed scope, preserve partial failures. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
