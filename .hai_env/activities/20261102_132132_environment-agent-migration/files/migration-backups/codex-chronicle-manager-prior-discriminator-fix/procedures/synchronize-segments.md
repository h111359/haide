# Synchronize segments

## Description

Inspect recording progress or synchronize assigned completed-source exchanges into Activity-local transcript segments, returning source/cadence evidence and actual recording status.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:recording_requirement] | Validated chronicles flag and effective enablement boundary, or independent mandatory workspace recording/timing requirement. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:activity_assignment] | Leader-assigned existing stable Activity ID, safe folder and known source attribution; synchronization requires exact source-exchange boundaries. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; unresolved Activity identity blocks inspection and synchronization. Return unknown source boundaries explicitly from inspection; resolve them before writes. |
| [input:source_metadata] | Authoritative source identity/start time, durable path and completed messages when available. | Optional | Caller and authorized workspace context | Retrieve exact context before synchronization. Read-only progress inspection returns available source/count evidence and precise missing-source limits without inventing data. |
| [input:coverage_context] | Relevant prior session attribution/segment metadata across affected Activities, or precise segments to inspect for overlap checks. | Optional | Leader plus available authoritative metadata | Inspect only relevant assigned metadata for progress; unresolved attribution remains explicit and blocks potentially overlapping writes. |
| [input:existing_segments] | Existing segment paths. | Optional | Caller and selected Activity metadata | Inspect relevant assigned metadata only; never broadly reread unrelated history. |
| [input:operation_evidence] | Verified completed domain operation with a descriptive label and its actual result/message. | Optional | Leader and the responsible domain owner's verified evidence | Omit operation metadata; never infer a completed operation from a proposal. |
| [input:historical_import] | Explicitly authorized historical import and provenance. | Optional | The user's permission relayed by Leader | Exclude earlier off periods. Authorized byte-preserving moves retain original paths/import dates/source limitations separately in Activity provenance. |
| [input:batch_context] | Leader's bounded batch identity, fixed cutoff and observed source/prompt dispatch cursors. | Optional | Leader's recording assignment | For synchronization, generate an attempt identity and retain existing cadence cursors; inspection creates no attempt. Explicit verification or mandatory recording needs no prompt threshold. |
| [input:operation_mode] | `synchronize` or read-only `inspect_progress`. | Optional | Leader's requested operation | Default to `synchronize`; progress inspection creates no files, attempts or scheduling cursor updates. |

## Prerequisites

A validated recording requirement or applicable independent mandatory instruction and an assigned existing Activity are available. Synchronization additionally requires exact source identity, completed-source assignment and sufficient coverage context before writes. Read the [transcript segment convention](../conventions/transcript-segment_conv.md) before inspection or writes; read-only progress inspection can return missing-source limits without satisfying synchronization prerequisites.

## Rules

None.

## Steps

1. Establish [input:workspace_root], load [input:instructions], validate [input:operation_mode] and resolve [input:recording_requirement], effective enablement boundary, [input:activity_assignment] and [input:authority]. If recording is off without an independent obligation or authorized [input:historical_import], return disabled without writes.

2. Validate the assigned Activity identity/lifecycle, folder containment and canonical target types. Inspect the safe checkpoint and relevant assigned segment/source metadata. For [input:operation_mode] `inspect_progress`, derive the latest attributable dispatch cursor, otherwise the latest verified recorded prompt, otherwise the first eligible source occurrence at the later Activity-assignment/enablement start. Count available eligible prompts after a cursor or inclusively from that first start. Return [output:recording_progress], existing checkpoint/coverage and pending limits without creating or changing files, attempts or cursors; an absent checkpoint is valid, and uncertain concurrent writes limit this snapshot. Stop this read-only branch here. For synchronization, obtain sole mutation ownership and exact source/coverage context; return competing work or missing/conflicting inputs before writes. Record the attempt and supplied [input:batch_context] dispatch cursors while preserving verified ranges and gaps.

3. Locate only the explicit authorized Codex JSONL source from [input:source_metadata]. Read the Codex source convention and adapter README before using the read-only adapter with a verified interpreter. Select one representation explicitly; verify original identity/start time, exact completed messages and assigned occurrences. Missing source, malformed/truncated records or unknown final-message phase remain explicit blockers; never scan other sessions or reconstruct missing text. Return exact missing or divergent source inputs before affected recording.

4. Inspect [input:existing_segments] and relevant segment metadata using [input:coverage_context]. Match source session, stable Activity ID and boundaries, and check cross-Activity attribution, duplicate segment claims and overlaps; return missing/conflicting coverage before potentially overlapping writes.

5. Compare existing eligible messages with authoritative source by occurrence and order. Inspect only new assigned source, precise affected segments and relevant checkpoint ranges during an ordinary batch. For an earlier prepared final-text entry, match its later saved outcome without duplication; return differing delivery/order for explicit resolution, or pending source status when not yet saved. Identify the matching segment and unrecorded eligible range, including available earlier pending outcomes, stopping at genuine unresolved gaps/divergence and excluding off-period or unresolved assignment ranges.

6. For a needed segment, select the convention's collision-safe name and exclusively create the required directory/file with source metadata after rechecking target absence, source assignment and inspected inputs.

7. Append only unrecorded eligible completed exchanges in order using the convention's exact-message format. If the next outcome is not saved, synchronize preceding eligible messages and return pending for that remaining outcome.

8. If [input:operation_evidence] supplies verified completed-operation metadata, append its exact labelled result under the convention; otherwise omit that optional metadata. For authorized historical byte-preserving moves, retain original bytes/names and record provenance separately in the Activity.

9. Read back changed segments and verify source identity, Activity assignment, completed-source boundary, chronology, exact text and nonoverlapping occurrence coverage.

10. Recheck and update the safe checkpoint with actual readback-verified ranges, pending gaps/outcomes and this attempt's result, including a no-write failure when safe checkpoint access remains available. Clear this invocation's in-flight marker only when its actual writes have stopped. Preserve unresolved partial writes/conflicts for explicit resolution; a dispatch cursor never proves coverage. Return [output:segment_coverage], [output:recording_checkpoint], [output:recording_progress] and [output:synchronization_status] with precise disabled/pending/deferred/blocked/partial evidence and any later supported catch-up need. On an earlier blocker, return the actual checkpoint/attempt status or its unavailable-write limit without continuing affected transcript writes.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:segment_coverage] | Verified Activity-local segment paths, source identity, Activity IDs and completed-source boundaries. | Readback verifies assignment, exact chronology/text, identity and no overlap/duplication. |
| [output:recording_checkpoint] | Safe checkpoint path, verified occurrence ranges, pending gaps/outcomes, cadence cursors and actual attempt status, or precise unavailable/disabled status. | Only source-backed readback advances verified coverage; scheduling progress is separate, persistent gaps remain explicit and no checkpoint is created for disabled/no-obligation recording. |
| [output:recording_progress] | Actual source identities, baseline/cursor and inclusive/exclusive boundary, known eligible prompt occurrences/count or unknown limits, verified ranges, pending gaps/outcomes and in-flight status. | Inspection reports its read-only snapshot without advancing coverage/cursors or fabricating source; absent checkpoint uses attributable source/segment context. Synchronization returns actual resulting progress. |
| [output:synchronization_status] | Verified Activity-local transcript segments through reported completed-source boundaries, or precise disabled, pending, deferred, blocked or partial status. Return Activity IDs, source identity, segment paths and coverage. Never claim unsaved outcomes or unsupported after-turn work occurred. | Distinguish disabled, pending, deferred, blocked and partial results with evidence; never claim unsaved outcomes or unsupported continuation. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
