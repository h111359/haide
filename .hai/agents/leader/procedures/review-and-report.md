# Review and report

## Description

Review delegated evidence against the task and agreed scope, then report verified outcomes, material limits, unresolved work, and applicable startup next actions.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:task] | Human question or task. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:activity_context] | Stable current Activity ID, path and relevant record context for substantive work; applicable bootstrap/diagnosis exception when no record is needed. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:returned_results] | Specialist results, evidence, verification limits and unresolved issues. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:acceptance_criteria] | Agreed criteria and authorized task scope. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |

## Prerequisites

Actual returned results and the agreed objective/acceptance criteria are available for review.

## Rules

None.

## Steps

1. Establish [input:workspace_root], load [input:instructions] and relate [input:activity_context] to [input:task] and [input:authority].

2. Compare [input:returned_results] and their verification against [input:acceptance_criteria], task objective and allowed scope.

3. If required work or evidence remains unresolved, route the concrete gaps to their owners and review returned results again. Report a genuinely unresolved blocker with its effect on completion.

4. Prepare [output:human_report] with completed work, evidence, verification limits and unresolved issues. If only asynchronous transcript catch-up remains, state its actual pending/deferred status.

5. For startup, include verified environment/current-work outcomes and a concise relevant menu even when no further task exists; use the startup procedure's prepared validated results.

6. Deliver [output:human_report] after the review outcome is established.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:human_report] | A completed delegated task organized under its Activity and reported accurately to the human, including material verification limits and unresolved issues. Required user-task work must be finished; asynchronous chronicles may remain pending or deferred only with accurate status, without claiming transcript synchronization has completed. | Review evidence against the objective and scope; route remaining gaps, state material limits, and never claim deferred transcript work completed. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
