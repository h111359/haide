# Initialize absent core state

## Description

Initialize safely absent mandatory state and instructions while preserving existing resources, and return verified creation results or precise partial failure.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:initialization_authority] | Startup permission to create safely absent state and fixed instructions, or the user's explicit initialization request. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:contract_template] | Installed state contract and canonical template defaults. | Mandatory | `../contract.json` and `../templates/state.json` | Return missing/invalid dependencies; do not infer versions/defaults. |

## Prerequisites

Read the shared Environment, state and model-profile references plus the installed [state contract](../contract.json) and [state template](../templates/state.json) as relevant. Read the startup-helper README before first use; do not reread unchanged knowledge already in context.

## Rules

- **No extra initialization question.** Environment-manager MUST NOT ask for another initialization permission or a feature location before performing already permitted minimal startup initialization.
- **Initial optional features.** Environment-manager MUST initialize chronicles as disabled and leave optional agent files untouched.
- **Absent container.** Environment-manager MUST NOT create the environment container when it already exists or its safe absence is unverified.
- **No optional scaffold.** Environment-manager MUST NOT create profiles, an agent catalogue, Activity records or optional content during minimal initialization.
- **Existing instructions.** Environment-manager MUST preserve existing safe instruction text and unrelated container contents during initialization.

## Steps

1. Establish [input:workspace_root], validate/load existing safe [input:instructions] independently of state validity, and verify [input:initialization_authority] against [input:authority]. Validate canonical container/state types and safe absence; return existing/conflicting/unsafe state without creation. Safely absent instructions are handled by the authorized initialization branch below.

2. Validate the installed [input:contract_template], reading the contract's current/supported versions and canonical template. Prepare a complete in-memory candidate from defaults plus the current state-format version and validate it under the state convention.

3. Create the container if safely absent. Validate/load an existing fixed [input:instructions], or exclusively create and verify an empty fixed file when safely absent under the existing initialization request or startup permission.

4. Recheck state absence, containment, inspected contract/template contents, instruction status and candidate validity immediately before exclusive state creation. If anything changed, return the conflict.

5. Create the state exclusively, then read back both mandatory resources. Verify current supported version, template defaults, mandatory location, disabled chronicles, intended instruction content and preserved unrelated contents; run the startup helper.

6. If creation or verification failed, return [output:initialization_result] identifying all actual partial writes and missing/invalid resources. Otherwise return verified initialization and [output:setup_choices] with validated settings and recommended additional chat setup.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:initialization_result] | Created mandatory state/instructions or exact partial failure. | Both mandatory resources verified, version current/supported, defaults preserved, no optional resources/catalogue created, unrelated content retained. |
| [output:setup_choices] | Recommended additional chat setup. | Return mandatory Activity location, separate optional-owner setup dependency and central chronicles flag/effective prompt threshold without delaying initialization for optional choices. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
