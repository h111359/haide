# Prepare implementation plan

## Description

Prepare a self-contained implementation brief that preserves current requirements, decisions and execution boundaries.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit validated workspace root. | Mandatory | Host coordinator. | Retrieve before dependent work. |
| [input:instructions] | Fixed and applicable workspace/session instructions. | Mandatory | Caller and readable fixed instructions. | Empty readable file is valid; missing instructions block dependent work. |
| [input:authority] | Actual human task, scope, constraints and permissions. | Mandatory | Human request relayed by host. | Retrieve existing authority; never invent permission. |
| [input:activity_context] | Validated core state, stable active Activity and relevant current records. | Mandatory | Host and runtime evidence. | Return missing dependency; no standalone bypass. |
| [input:work_context] | Current requirements, acceptance, evidence sources, attachments and decisions. | Mandatory | Host and authorized task sources. | Retrieve facts; return unresolved necessary decisions. |
| [input:assessment] | Current assessment and technical-readiness evidence. | Optional | Host and Assess solution result. | Required in normal mode; accelerated mode derives the same evidence from current authorized sources. |
| [input:mode] | normal or explicitly requested accelerated planning. | Optional | Actual caller instruction. | Default normal; no implied accelerated authority. |

## Prerequisites

Validated selected configuration, mandatory instructions, compatible environment, stable active Activity and meaningful authorized assignment. Passed business readiness or its evidenced narrow exemption. Normal mode has current assessment; accelerated mode has explicit selection and equivalent readiness evidence.

## Rules

None.

## Steps

1. Establish [input:workspace_root], [input:instructions], [input:authority] and [input:activity_context]; retrieve authorized missing context and stop dependent work on unresolved prerequisites.

2. Confirm [input:mode] against actual [input:authority], defaulting to normal. Compare [input:work_context] and any [input:assessment] with current input/decisions; stop dependent finalization on stale evidence or unresolved critical decisions. Explicit acceleration omits a separate assessment artifact, not required checks or permissions.

3. Build one coherent plan using the implementation-plan convention: execution contract, acceptance criteria, overview, seven-part phases and exact file inventory. Preserve all settled decisions, assumptions, constraints, authorization statements, task dependencies and cross-artifact conditions. Disclose every choice actually delegated.

4. Give every task a target, operation, expected result, dependency reason, acceptance mapping and completion check. Classify each planned artifact's purpose, owner, lifetime and canonical destination under the shared artifact placement contract before prescribing creation; distinguish maintained outputs from current-task working material and evidence. Specify commands/tools and output destinations for executable operations. Keep essential semantics directly in the plan; natural-language instructions precede implementation code, and unavailable references cannot carry required work.

5. Include knowledge/documentation deltas with target identity, exact structured edits where required, preserved intent and owner validation. Prefer staged owner-controlled replacement over destructive delete-then-insert; if no documentation update is needed state why. Include proportionate tests and explicit human/external acceptance methods.

6. Validate structure and current identity through plan_contract.py and independently review semantic completeness, feasibility, ordering and permissions. A blocked proposal remains labeled blocked; do not repair meaning automatically or treat a structural pass as authorization.

7. Return plan and validation evidence to host for serialized persistence and predecessor retention. Recheck source/decision identity before accepting host readback; keep prior plans as history rather than merging conflicting instructions. Planning does not authorize implementation.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:work_result] | Proposed current plan, input/decision identity, validation evidence and execution-readiness dependencies. | Actual results, evidence, current identity and unresolved dependencies are distinct; host persists canonical records. |

## References

- [Role definition](../SKILL.md) — inherited safeguards and conditional references; required throughout.
