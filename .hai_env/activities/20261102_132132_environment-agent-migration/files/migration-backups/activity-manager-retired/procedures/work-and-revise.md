# Work and revise

## Description

Perform and record assigned Activity work while preserving material revisions, and return step status, implementation or verification evidence, and unresolved limits.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:operation] | Selected record/lifecycle or assigned substantive-work operation. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:environment_context] | Caller-validated compatible environment and safe activities.location; direct HAI calls have no standalone bypass. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:selected_activity] | Current active valid consistent record with stable ID/path. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:work_context] | Available intent, source, constraints, acceptance criteria and selected assigned steps. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:specialist_evidence] | Actual specialist results and verification returned by leader. | Optional | Leader and verified sources | Keep required external work pending; never invoke specialists or invent evidence. |
| [input:related_activities] | Relevant stable related IDs and source references. | Optional | Authorized caller/source context | Remain absent; do not invent links. |

## Prerequisites

Read the package [Activity concept](../concepts/activity.md) and [Activity convention](../conventions/activity_conv.md). Caller-validated compatible environment/store context and local path/type validation are required. The selected record must be active and consistent; assigned work and its meaningful authorized source must be available.

## Rules

None.

## Steps

1. Establish [input:workspace_root], load [input:instructions], and bind [input:selected_activity] to [input:environment_context]. Validate its identity, active lifecycle, store consistency and safe targets before selecting [input:operation] within [input:authority].

2. Inspect [input:work_context], existing decisions/source, [input:specialist_evidence] and relevant [input:related_activities]. Retrieve context and clarify only unresolved intent/criteria before affected work.

3. For an assigned nonimplementation step, mark it `in_progress` and log the actual work. Save useful questions/answers, decisions, definition, analysis, plan or questionnaire artifacts as the assignment requires.

4. For a material replacement of definition/analysis/plan, exclusively preserve the exact prior version in the convention's revision location before publishing the replacement. Record source/author, date, reason, predecessor and dependent impact.

5. Reassess affected artifacts, assumptions, implementation and checks after that revision. Preserve earlier evidence, mark stale dependent step results pending, and identify what must be repeated.

6. Before the first implementation attempt, update implementation status and its original start timestamp together, then perform scoped changes and appropriate checks. On retries use the retained original timestamp.

7. For required external work, return the dependency with sources and expected results to leader. Record actual returned [input:specialist_evidence] when available.

8. Record actual results and verification separately, including attempts, deviations, failed/blocked/unrun checks and deliberately skipped work. Set each step's status from its supporting evidence.

9. Return [output:work_result] with progress, preserved revisions, implementation/verification evidence, relevant related IDs and unresolved dependencies.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:work_result] | Recorded assigned work, preserved revisions, step status, implementation/verification evidence and limits. | Keep immutable original implementation start; prior material versions/evidence retained, stale dependents reassessed and unfinished work explicit. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
