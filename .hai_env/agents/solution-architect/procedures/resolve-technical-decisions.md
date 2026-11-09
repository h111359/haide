# Resolve technical decisions

## Description

Prepare focused technical clarifications and apply verified decisions to the current assessment.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit validated workspace root. | Mandatory | Host coordinator. | Retrieve before dependent work. |
| [input:instructions] | Fixed and applicable workspace/session instructions. | Mandatory | Caller and readable fixed instructions. | Empty readable file is valid; missing instructions block dependent work. |
| [input:authority] | Actual human task, scope, constraints and permissions. | Mandatory | Human request relayed by host. | Retrieve existing authority; never invent permission. |
| [input:activity_context] | Validated core state, stable active Activity and relevant current records. | Mandatory | Host and runtime evidence. | Return missing dependency; no standalone bypass. |
| [input:assessment] | Current attributable assessment and relevant source identity. | Mandatory | Assess solution result relayed by host. | Return inconsistent/missing assessment; do not reconstruct history. |
| [input:decisions] | Unresolved alternatives or actual revised answers with provenance. | Mandatory | Host and current ledger. | Retrieve current ledger before proposing new questions. |

## Prerequisites

Validated selected configuration, mandatory instructions, compatible environment, stable active Activity and meaningful authorized assignment. Verified current assessment and accessible host dialogue persistence handshake.

## Rules

None.

## Steps

1. Establish [input:workspace_root], [input:instructions], [input:authority] and [input:activity_context]; retrieve authorized missing context and stop dependent work on unresolved prerequisites.

2. Compare [input:assessment] and [input:decisions] with current Activity input and the saved dialogue ledger. Retrieve facts before questions; distinguish already settled choices from choices actually delegated and unresolved human decisions.

3. For each necessary unresolved decision prepare named alternatives, benefits, costs, implementation impact and a recommendation. Keep assessment alternatives neutral and recommendation separate; avoid quotas or questions for safely delegated implementation details.

4. Prepare the existing dialogue contract events with host-supplied occurrence identities and stable ledger IDs. Return candidates to host for serialized runtime persistence and exact readback; display only verified saved question blocks. Reuse unanswered IDs and split UI batches without duplicate questions.

5. Apply only host-verified actual answers. Preserve raw multipart responses and revisions; ambiguous mapping, recommendations, silence or unchecked fields are not answers. Return unresolved mappings and hold dependent finalization.

6. Reassess every affected assumption, alternative, action, acceptance condition and knowledge change. Ask host to retain predecessors using runtime revisions and persist the coherent current assessment. If there is no new input or answer, return no new work without manufacturing a revision.

7. Return the current assessment, effective decision identity and remaining dependencies to host; pass those values as assessment and work_context for Prepare implementation plan only when required readiness holds.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:work_result] | Verified effective decisions or proposed questions, revised assessment and explicit pending answers. | Actual results, evidence, current identity and unresolved dependencies are distinct; host persists canonical records. |

## References

- [Role definition](../SKILL.md) — inherited safeguards and conditional references; required throughout.
