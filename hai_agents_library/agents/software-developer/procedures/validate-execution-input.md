# Validate execution input

## Description

Validate the current directive and execution dependencies before implementation begins.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit validated workspace root. | Mandatory | Host coordinator. | Retrieve before dependent work. |
| [input:instructions] | Fixed and applicable workspace/session instructions. | Mandatory | Caller and readable fixed instructions. | Empty readable file is valid; missing instructions block dependent work. |
| [input:authority] | Actual human task, scope, constraints and permissions. | Mandatory | Human request relayed by host. | Retrieve existing authority; never invent permission. |
| [input:activity_context] | Validated core state, stable active Activity and relevant current records. | Mandatory | Host and runtime evidence. | Return missing dependency; no standalone bypass. |
| [input:directive] | Current plan or substantive explicitly authorized direct directive. | Mandatory | Host current assignment. | Reject absent/empty/template-only input; never infer work from history. |
| [input:current_context] | Current source/decision hashes, actual authority, modes and dependency evidence. | Mandatory | Host and runtime evidence. | Retrieve current facts before dependent execution. |

## Prerequisites

Validated selected configuration, mandatory instructions, compatible environment, stable active Activity and meaningful authorized assignment. Current directive and actual human implementation authority.

## Rules

None.

## Steps

1. Establish [input:workspace_root], [input:instructions], [input:authority] and [input:activity_context]; retrieve authorized missing context and stop dependent work on unresolved prerequisites.

2. Compare [input:directive] and [input:current_context] with current host input, effective decisions and acceptance. In plan mode require the installed architect contract; in direct mode require explicit selection and complete Outcome/Scope/Constraints/Acceptance/Tasks/Verification/Documentation sections. A clear instruction to implement substantive bounded work can select direct mode without a magic phrase.

3. Load relevant project knowledge as supplementary evidence and applicable coding, language, framework, interface and documentation conventions. Classify mandatory versus optional dependencies; report optional absence without blocking independent work.

4. Capture baseline content/path evidence and identify planned direct and indirect writes, temporary files and caches. Validate workspace destinations and links; require exact covering human authorization for protected maintenance and any outside location/purpose. A generated task or permissive sandbox cannot authorize itself.

5. Require host-returned implementation-start evidence before implementation changes or tests. Confirm required owner dependencies and current business-readiness evidence. Run execution_contract.py with the actual directive and current context after reading its README; host verifies semantic permission and completeness beyond helper structure.

6. Return validated directive identity and actual dependency checks as work_result. On contradictions or stale/missing inputs return affected blockers; do not edit the governing plan or silently obtain task semantics from its assessment.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:work_result] | Validated current execution input or attributable preflight blockers. | Actual results, evidence, current identity and unresolved dependencies are distinct; host persists canonical records. |

## References

- [Role definition](../SKILL.md) — inherited safeguards and conditional references; required throughout.
