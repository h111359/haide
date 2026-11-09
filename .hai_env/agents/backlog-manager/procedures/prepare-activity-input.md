# Prepare Activity input

## Description

Prepare a selected pending item as attributable work input and record verified Activity linkage returned by the host.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit workspace and current Activity context. | Mandatory | Host coordinator. | Retrieve validated context. |
| [input:item_id] | Exact pending backlog item selected for work. | Mandatory | Caller. | Resolve selection before preparing work. |
| [input:activity_result] | Stable Activity ID/path returned by the host after an authorized handoff. | Optional | Host coordinator runtime evidence. | Return proposed input without inventing an Activity or recording a claimed assignment. |

## Prerequisites

Validated settings, safe backlog and selected pending item; handoff is within the user-requested scope.

## Rules

None.

## Steps

1. Inspect [input:item_id] in the selected backlog of [input:workspace_root]. Verify it is pending and its catalogue entry agrees. Read What, Why, Acceptance Criteria, prior clarification and dependencies without treating unresolved proposals as approvals.

2. Prepare an attributable input containing item ID/path, supplied requirements and criteria, known dependencies and unresolved questions. Return domain-clarification needs through the host coordinator to the appropriate optional specialist; do not select or invoke that specialist.

3. Return the proposed input to the host coordinator for authorized use in the current Activity or a user-selected new boundary. Do not create, close or replace an Activity, overwrite existing Activity input, or imply that starting work accepts the requirements.

4. When [input:activity_result] contains actual verified runtime evidence, record its stable ID and path in the item Activities field and append dated linkage history. Use Maintain items with [input:workspace_root] as workspace_root, the authorized linkage edit as request and the selected ID/evidence as items. Keep the item pending until a separate evidenced terminal decision.

5. Return prepared input, confirmed linkage or the precise pending handoff. A later Activity closure is not automatic backlog completion.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:handoff] | Attributable work input, unresolved questions and verified or pending Activity linkage. | No lifecycle action or acceptance claim is invented; any written linkage matches host-supplied evidence. |

## References

- [Role rules and references](../SKILL.md) — shared ownership, constraints and required reading.
- [Backlog format](../conventions/backlog_conv.md) — record, catalogue and history contracts; required for this procedure.
- [Audit helper](../scripts/README.md) — required before helper execution.
