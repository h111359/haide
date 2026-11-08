# Perform assigned work

## Description

Perform the assigned business analyst work and return attributable results, evidence and unresolved dependencies within the authorized scope.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | host coordinator or authorized caller | Retrieve authorized context; return unresolved root before dependent work. |
| [input:instructions] | Applicable fixed mandatory and workspace/session instructions. | Mandatory | Caller and safe readable fixed instructions | An empty readable file is valid; missing/unreadable instructions block dependent work. |
| [input:authority] | Requested work, scope, constraints and existing permissions. | Mandatory | Human request relayed by host coordinator | Retrieve existing authority; do not invent approval. |
| [input:activity_context] | Validated environment plus stable active Activity ID/path and relevant record context. | Mandatory | host coordinator and runtime evidence | Retrieve context or return the dependency; no substantive standalone bypass. |
| [input:work_context] | Intent, domain sources, available acceptance criteria, settled decisions, selected steps and relevant prior results. | Mandatory | host coordinator and authorized task sources | Retrieve available context; pause dependent work and continue independent diagnosis. |

## Prerequisites

Valid selected-agent configuration, compatible environment, safe mandatory instructions, active stable Activity and a meaningful scoped assignment. Required task decisions and operation-specific permission are available before dependent work.

## Rules

None.

## Steps

1. Establish [input:workspace_root], load [input:instructions], compare [input:authority], [input:activity_context] and [input:work_context] with the procedure requirements, and retrieve missing authorized context before affected work.

2. Read the supplied human input and relevant authorized domain sources; distinguish facts, assumptions, proposals and settled decisions.

3. Analyze the business need, users, constraints, workflows and acceptance criteria. Ask only necessary unresolved questions, retrieving available evidence first; continue independent analysis.

4. Prepare attributable requirements and clarification results, preserving exact supplied human quotations and identifying unresolved decisions and downstream dependencies. Do not imply silence establishes agreement.

5. Return [output:work_result] with performed work, attributable decisions, exact artifact paths or prepared record content, actual checks and limits. Keep external work pending until host coordinator returns the responsible owner's evidence; do not mark Activity steps or close records yourself.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:work_result] | Performed assigned work, decisions, artifacts, verification evidence, provenance and unresolved dependencies. | Results match the authorized scope; performed and unperformed work remain distinct; record changes are returned to host coordinator for runtime. |

## References

- [Role definition](../SKILL.md) — inherited scope, safeguards and required references.
