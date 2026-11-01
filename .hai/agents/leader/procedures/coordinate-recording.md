# Coordinate recording

## Description

Coordinate prompt-batched Activity recording and requested verification, and return actual source coverage, scheduling progress and unresolved recording status.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:task] | Human question or task. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:activity_context] | Stable current Activity ID, path and relevant record context for substantive work; applicable bootstrap/diagnosis exception when no record is needed. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:recording_context] | Validated chronicles enablement, effective record_every_prompts threshold and mandatory recording/timing instructions. | Mandatory | Startup/settings result and applicable instructions | Retrieve validated context; absent threshold defaults to 5 under the state convention, while invalid values block affected scheduling. |
| [input:source_assignment] | Stable Activity assignments, authoritative source occurrence IDs, completed saved-source cutoffs, enabled intervals and relevant segment attribution. | Optional | Current source context and attributable existing assignments | Disabled/no-obligation or below-threshold reporting needs no recording assignment. Retrieve exact context before a due batch/verification; if unavailable, report pending source/count rather than guess or invent source. |
| [input:recording_progress] | Activity-manager checkpoint and current session count, dispatch cursors, in-flight invocation and last reported blocker. | Optional | Activity-manager results and Leader's coordination context | Seed from an attributable dispatch/verified prompt or enabled Activity start; missing checkpoint does not reset observed prompts or block a first batch. Reconstruct source details once when genuinely needed, preserving unknown historical gaps separately from the live prompt count. |
| [input:final_text] | Exact final text when mandatory pre-delivery recording applies. | Optional | Leader prepared outcome | Do not invent it; obtain exact text before that mandatory exception. |

## Prerequisites

Validated recording requirement and usable Activity context. Actual recording assignments require exact source attribution. Activity-manager owns recording procedures, formats and checkpoint writes; counting from available source/progress context is Leader coordination, not permission to execute a new helper or mutate configuration.

## Rules

None.

## Steps

1. Establish [input:workspace_root], load [input:instructions], and inspect [input:task], [input:authority], [input:activity_context] and [input:recording_context].

2. If optional recording is off with no applicable independent obligation or authorized historical import, return the verified disabled status. Otherwise identify whether this is ordinary cadence, an explicit flush/verification, authorized closure or mandatory timing; exact recording assignments are resolved only before dispatch.

3. For ordinary cadence, use the latest attributable dispatch cursor, otherwise the latest verified recorded prompt, otherwise the first eligible prompt at the later Activity-assignment/enablement start. Count after an existing cursor or inclusively from that first start. Keep and increment the count for newly observed actual human prompts in Leader's current conversation context, without per-prompt source/file reads, writes or agent calls. Reconcile those observed occurrences with durable message IDs or stable source positions at batch dispatch or resumption. Missing checkpoint alone neither resets the known count nor prevents the first batch; preserve missing historical source as a separate coverage gap.

4. For an ordinary batch below the threshold, return pending coverage and the next batch condition. After a failed batch with no transcript changes, count new prompts after its dispatch cursors before ordinary retry; report an unchanged persistent blocker once until its status changes. Explicit repair/flush, operation verification, closure or mandatory timing bypasses the count. Preserve gaps independently of cadence. Resolve partial writes/conflicts explicitly before affected writes rather than silently retrying them.

5. If resumption or a missing attributable baseline genuinely needs source/progress inspection, delegate Activity-manager's [Synchronize segments](../../activity-manager/procedures/synchronize-segments.md) with `operation_mode` set to `inspect_progress`: pass [input:workspace_root] to target `workspace_root`, [input:instructions] to `instructions`, [input:authority] to `authority`, [input:recording_context] to `recording_requirement`, and stable identity/path from [input:activity_context] plus known source attribution from [input:source_assignment] to `activity_assignment`. Pass available source metadata, coverage attribution and segment paths from [input:source_assignment]/[input:recording_progress] to `source_metadata`, `coverage_context` and `existing_segments`, respectively; omit unavailable optional values. Receive its explicit `recording_progress` snapshot without file/cursor updates, not a synchronization. Retain any known live prompt count if historical reconstruction remains incomplete; report genuinely unknown boundaries rather than fabricate them. Reevaluate the ordinary count before dispatch and return pending if now known below threshold; do not repeat inspection per prompt.

6. For a due batch, explicit flush/verification, authorized closure or mandatory timing, reconcile actual in-flight jobs and serialize mutating assignments for the stable Activity. An active or uncertain earlier writer keeps the next assignment pending. Resolve exact source assignments and ambiguous attribution from [input:source_assignment] before writes, obtaining the human's decision only for unresolved necessary boundaries. If no current Activity is available, route discovery/authorized creation to Activity-manager, never assign old backlog to a later current Activity. Fix the saved-source cutoff, enabled-interval assignments and relevant segment/checkpoint context. Include an already saved threshold prompt, leaving its future reply pending.

7. For an ordinary due batch or explicit flush, mark the batch identity and dispatch cursors in flight in coordination context, then delegate one Activity-manager synchronization assignment through the normal delegation steps. Supply source assignments, recording requirement and batch identity/cursors/cutoff as the selected procedure's declared inputs. Continue independent work. Receive actual checkpoint/coverage results; clear the invocation marker only after its writers have stopped. Activity-manager alone persists recording progress. Ordinary Activity edits do not dispatch transcript batches.

8. For explicitly requested synchronous verification, delegate Activity-manager's verification procedure with the identified operation and exact source cutoff, then return its fresh evidence to the requester. For authorized closure, supply exact recording inputs to Activity-manager's close-or-supplement assignment; it performs its own fresh verification in the same role before closing when recording is enabled or independently mandatory. Disabled/no-obligation closure needs no transcript synchronization. Wait for active recording before any closure assignment.

9. For mandatory pre-delivery timing, supply [input:final_text] to Activity-manager's mandatory-pre-delivery procedure and receive its verified unchanged text/status before delivery. Return missing text or a recording blocker rather than claiming the timing requirement passed.

10. For pending final-response catch-up, check actual runtime continuation support. If supported and a batch/explicit flush or mandatory requirement is due, arrange only the supported later invocation; otherwise retain pending coverage for the next batch or explicit closure/flush. Without continuation support, report deferred catch-up to a later active turn. Never promise an after-turn worker or wait for a future undelivered source message.

11. Return [output:recording_status] with actual verified coverage, disabled status or pending/deferred/blocked/partial work, dispatch progress and evidence. A dispatch cursor or a recent successful batch does not resolve older gaps.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:recording_status] | Verified/disabled/pending/deferred/blocked/partial recording, source coverage, checkpoint/dispatch cursors and actual in-flight status. | Distinguish actual verified coverage from scheduling progress and retained gaps. Ordinary recording does not delay task delivery; mandatory timing and enabled-recording closure verification take precedence. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
