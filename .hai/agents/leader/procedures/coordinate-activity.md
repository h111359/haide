# Coordinate Activity

## Description

Coordinate Activity discovery, continuity, and authorized record maintenance, and return verified work identity and actual recording results.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:task] | Human question or task. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:environment_context] | Validated compatible environment and mandatory activities.location. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:current_record] | Existing current-work continuity, if any. | Optional | Environment-manager | Route discovery; meaningful new work without a current record creates one as part of the user's requested work. |

## Prerequisites

Validated compatible environment with its mandatory Activity location. Normal Environment-manager invocation uses supported resolved settings under the model-profile convention.

## Rules

None.

## Steps

1. Establish [input:workspace_root] and load [input:instructions]. Resolve the requested work and scope from [input:task] and [input:authority].

2. Extract the validated store from [input:environment_context]. If compatibility/location assurance is missing or conflicting, return the specific setup dependency before record discovery.

3. Prepare an Environment-manager discovery assignment with workspace root, instructions, validated environment/store, requested operation and permitted scope. Include [input:current_record] as previously supplied continuity to recheck, not as a replacement for discovery.

4. Select the registered Environment-manager and delegate that assignment under [Delegate work](delegate-work.md), supplying its task, catalogue, exact runtime settings and record-discovery context through that procedure's declared inputs. Receive its actual discovery result.

5. If discovery reports invalid, inconsistent or ambiguous current work, return the precise boundary/dependency and keep affected work pending.

6. If a valid current record exists, compare its objective with [input:task]. For compatible work, return its stable ID/path and continuity for resumption; for conflicting intent, obtain the user's decision before requesting closure or replacement.

7. If discovery verifies no current record and the request is only startup/diagnosis, return verified absence. If meaningful substantive new work is authorized, assign creation to Environment-manager with the human objective/source and existing validated context, then receive its readback verification.

8. Pass the verified stable ID/path and relevant record context into substantive specialist assignments. Route actual results, material decisions and record/lifecycle requests to Environment-manager and receive record evidence. Before first implementation changes or implementation tests, obtain its verified original implementation-start marker and pass it to the execution owner. Source recording is a separate Codex Chronicle-manager assignment through Coordinate recording. For required-recording closure, route the fresh verification dependency through that procedure and return operation-bound proof and stopped-writer assurance to Environment-manager; do not reuse prior-operation evidence.

9. Return [output:activity_context] and [output:recording_requests], distinguishing verified record, valid absence, creation, recorded results and unresolved dependencies.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:activity_context] | Stable Activity ID/path and continuity for substantive handoffs. | Current record, valid absence before meaningful work, or authorized creation is verified; conflicting or invalid boundaries remain unresolved. |
| [output:recording_requests] | Actual results and decisions routed for Activity recording. | No automatic closure; material revisions, performed steps and closure outcomes remain distinct. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
