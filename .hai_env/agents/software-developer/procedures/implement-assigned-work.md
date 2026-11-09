# Implement assigned work

## Description

Implement bounded current work while preserving scope, dependencies and attributable change evidence.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit validated workspace root. | Mandatory | Host coordinator. | Retrieve before dependent work. |
| [input:instructions] | Fixed and applicable workspace/session instructions. | Mandatory | Caller and readable fixed instructions. | Empty readable file is valid; missing instructions block dependent work. |
| [input:authority] | Actual human task, scope, constraints and permissions. | Mandatory | Human request relayed by host. | Retrieve existing authority; never invent permission. |
| [input:activity_context] | Validated core state, stable active Activity and relevant current records. | Mandatory | Host and runtime evidence. | Return missing dependency; no standalone bypass. |
| [input:validated_input] | Current validated directive, scope, identity and preflight results. | Mandatory | Validate execution input result relayed by host. | Return preflight dependency; do not begin product edits. |

## Prerequisites

Validated selected configuration, mandatory instructions, compatible environment, stable active Activity and meaningful authorized assignment. Current preflight and original runtime implementation-start evidence.

## Rules

None.

## Steps

1. Establish [input:workspace_root], [input:instructions], [input:authority] and [input:activity_context]; retrieve authorized missing context and stop dependent work on unresolved prerequisites.

2. Recheck [input:validated_input] against current source/decisions, runtime marker and destination baseline before writes. Return changed identity for refreshed preflight rather than relying on an old validation result.

3. Execute the directive tasks in dependency order at canonical locations. Before creating any newly needed artifact, establish its purpose, owner, lifetime and destination under the shared artifact placement contract; return consequential scope/destination conflicts rather than defaulting to product folders. Use authorized Activity/invocation scratch for helpers and configure caches before tools. Keep a per-task result and direct/indirect changed-path evidence; preserve unrelated existing modifications.

4. Investigate failures and correct authorized implementation defects, rerunning affected checks. Stop dependent work on mandatory tool failure, changed inputs or partial persistence failure; preserve partial bytes and diagnostics without automatic rollback or retry of the partial operation.

5. Return consequential deviations or newly discovered scope/permission conflicts through host for a coherent revised directive. Record out-of-scope concerns separately. Never rewrite the governing plan to authorize different behavior.

6. Provide concise progress at completed meaningful tasks. Return implementation notes, actual changes, decisions, checks and blockers to host as implementation_result for Verify and hand off; do not advance Activity state yourself.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:work_result] | Implementation results, attributable changed paths, task progress, checks and partial failures. | Actual results, evidence, current identity and unresolved dependencies are distinct; host persists canonical records. |

## References

- [Role definition](../SKILL.md) — inherited safeguards and conditional references; required throughout.
