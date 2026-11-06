# Maintain items

## Description

Capture or revise individual backlog records, apply attributable status decisions and keep the catalogue consistent.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit workspace and current Activity context. | Mandatory | Host coordinator. | Retrieve validated context before mutation. |
| [input:request] | Capture, edit, inspect, catalogue repair, terminal decision or reopening scope. | Mandatory | Caller. | Resolve intended operation; inspection grants no repair authority. |
| [input:items] | Selected IDs, supplied requirements and decision evidence. | Optional | Caller or selected catalogue records. | For creation use supplied content; for existing work resolve exact IDs before writes. |

## Prerequisites

Validated installed settings, safe selected backlog, fixed instructions and current Activity; mutation additionally has covering authority and sole backlog writer assignment.

## Rules

None.

## Steps

1. Load settings and validate the selected root as in Configure backlog, passing [input:workspace_root] as workspace_root and any explicitly requested setup as request. If no setup is requested, inspect existing context only. Audit the selected catalogue and item folders before dependent changes.

2. For capture, allocate the next unused numeric ID across new/ and closed/. Use the caller-supplied What, Why and Acceptance Criteria; mark missing information explicitly and distinguish proposed clarification from accepted text. Record actual creation/update times and source. Exclusively create one pending file in new/.

3. For an existing item from [input:items], verify its identity, current status, source and history. Recheck inspected bytes. For material content revisions preserve the exact predecessor in history/ before editing, record the source/reason and retain prior decisions; missing approval for a proposed requirement remains unresolved.

4. For a completed decision in [input:request], examine evidence against the supplied acceptance criteria and covering authority. Report remaining unverified criteria instead of inferring completion from an Activity state. If no criteria were supplied, retrieve an explicit attributable acceptance decision. For cancellation or rejection retain the decision source and reason.

5. For an authorized terminal transition, add actual Closed/Updated timestamps, Resolution and a history entry, then move the same ID to closed/ without overwriting. For explicit reopening, retain the earlier outcome/history, clear the current Closed value and move the same ID back to new/ as pending. Read back the resulting item and preserve partial results if a step fails.

6. Update exactly the affected catalogue rows and order them numerically. A requested full catalogue repair derives rows only from validated item files, preserves catalogue prose and reports invalid records rather than silently dropping them. Read-only inspection performs no repair or timestamp changes.

7. Rerun the auditor and verify item/cataloque agreement, IDs, paths, required sections, status-folder alignment and evidence. Return actual changes and unresolved decisions to the host coordinator; do not implement the backlog item or change Activity lifecycle.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:result] | Selected item IDs/paths, status decisions, catalogue evidence and unresolved details. | Readback confirms performed changes, or partial/blocked work names the exact affected paths and dependency. |

## References

- [Role rules and references](../SKILL.md) — shared ownership, constraints and required reading.
- [Backlog format](../conventions/backlog_conv.md) — record, catalogue and history contracts; required for this procedure.
- [Audit helper](../scripts/README.md) — required before helper execution.
