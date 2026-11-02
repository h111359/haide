# Configure Activity location and optional features through chat

## Description

Apply explicit Activity-location and chronicles choices while preserving unmentioned settings and records, and return validated configuration and recording boundaries.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:activity_context] | Stable current Activity ID, path and relevant record context for substantive work; applicable bootstrap/diagnosis exception when no record is needed. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:setting_choices] | Human choices for properties to change; partial or deferred setup is valid. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:locations] | Explicit safe workspace-relative Activity location. | Optional | Human choices and existing validated state | Retain the existing Activity location; specification setup belongs to its owner. |

## Prerequisites

Read the shared Environment, state and model-profile references plus the installed [state contract](../contract.json) and [state template](../templates/state.json) as relevant. Read the startup-helper README before first use; do not reread unchanged knowledge already in context. Existing compatible state and supplied Activity context are required for substantive changes.

## Rules

None.

## Steps

1. Establish [input:workspace_root], load [input:instructions], and validate existing state under [input:authority]/[input:activity_context].

2. Present current mandatory Activity location, separate specification-owner status/location assurance and central chronicles enabled/prompt threshold. Reconcile [input:setting_choices] and optional [input:locations] with already supplied decisions; for deferred/no-change setup return the existing validated settings.

3. Require format-3 core and fresh valid specification-owner location assurance for dependent path changes, including disabled specification. Reject candidate Activity/profile overlaps and unresolved invalid/unverified/dormant owner roots; do not guess a default. Prepare only explicitly chosen Activity/chronicles properties, retaining unmentioned values and unknown/opaque properties. Validate complete candidate paths, types and collisions under the state convention; specification setup goes to its registered owner rather than a state candidate. Validate `features.chronicles.record_every_prompts` as a positive integer excluding Booleans, using effective default 5 when absent even while recording is disabled. Keep configuration separate from Activity-local coverage and scheduling progress; a threshold change does not reset either.

4. Identify the effective recording enablement boundary and any separately authorized record relocation/history work for a separate Environment-manager record assignment through Leader. Return exact-source recording/import dependencies to Leader for the registered installed Codex Chronicle-manager. Return the old/new threshold and enablement values without rewriting records, transcript coverage or performing a recording batch; missing optional recording support does not invalidate the core settings result.

5. Recheck unchanged state, paths and instructions, then write only the validated candidate. Read back and run the startup helper to verify requested settings and preserved resources/properties.

6. Return [output:feature_result] with old/new location references where changed, validated mandatory/optional context, effective recording boundary, changes, evidence and exact partial failures/dependencies.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:feature_result] | Validated mandatory Activity context, optional flags/location, effective recording prompt threshold/boundary, operations, evidence and dependencies. | Verify only chosen settings changed, unknown properties preserved and files/records untouched; changing references never claims relocation or historical backfill. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
