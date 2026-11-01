# Mandatory pre-delivery recording

## Description

Record the supplied exact final response under the mandatory pre-delivery requirement, returning that same text with verified coverage or a precise blocker.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:recording_requirement] | Validated chronicles flag and effective enablement boundary, or independent mandatory workspace recording/timing requirement. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:activity_assignment] | Leader-assigned existing stable Activity ID, safe folder and exact source-exchange boundaries. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:source_metadata] | Authoritative source session ID, original start time, durable saved local source path and readable completed messages. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:coverage_context] | Relevant prior session attribution/segment metadata across affected Activities, or precise segments to inspect for overlap checks. | Mandatory | Leader plus available authoritative metadata | Missing coverage context is an explicit verification limit and blocks writes that could overlap unresolved assignments. |
| [input:existing_segments] | Existing segment paths. | Optional | Caller and selected Activity metadata | Inspect relevant assigned metadata only; never broadly reread unrelated history. |
| [input:operation_evidence] | Verified completed domain operation with a descriptive label and its actual result/message. | Optional | Leader and the responsible domain owner's verified evidence | Omit operation metadata; never infer a completed operation from a proposal. |
| [input:historical_import] | Explicitly authorized historical import and provenance. | Optional | The user's permission relayed by Leader | Exclude earlier off periods. Authorized byte-preserving moves retain original paths/import dates/source limitations separately in Activity provenance. |
| [input:final_text] | Leader's exact prepared final response text. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |

## Prerequisites

A validated recording requirement or applicable independent mandatory instruction, an assigned existing Activity and exact source context are available. Read the [transcript segment convention](../conventions/transcript-segment_conv.md) before segment writes. Applicable mandatory instructions explicitly require pre-delivery recording and leader supplies exact final text.

## Rules

- **Prepared final text.** Activity-manager MAY append Leader's exact supplied final text before it is saved only when mandatory workspace timing requires pre-delivery recording.
- **Delivery text.** Activity-manager MUST return the recorded final text unchanged for delivery.
- **Later reconciliation.** Activity-manager MUST reconcile the prepared entry with later saved delivery without duplication when that source becomes available during a later synchronization invocation.

## Steps

1. Establish [input:workspace_root], load [input:instructions], and verify the mandatory pre-delivery requirement in [input:recording_requirement] within [input:authority]. Resolve the exact [input:final_text] before recording.

2. Execute [Synchronize segments](synchronize-segments.md) for preceding eligible saved source, explicitly passing [input:workspace_root] to target `workspace_root`, [input:instructions] to `instructions`, [input:authority] to `authority`, [input:recording_requirement] to `recording_requirement`, [input:activity_assignment] to `activity_assignment`, [input:source_metadata] to `source_metadata`, [input:coverage_context] to `coverage_context`, [input:existing_segments] to `existing_segments`, [input:operation_evidence] to `operation_evidence`, and [input:historical_import] to `historical_import`.

3. Inspect its coverage and any gap/divergence/assignment blocker. If preceding required source or safe append placement is unresolved, return the exact [output:pre_delivery_status] without claiming the timing requirement passed.

4. Retain sole mutation ownership, recheck Activity identity, assignment, existing segment contents and final-text placement, then append [input:final_text] exactly and read back identity, source order, text and coverage. Update the safe checkpoint's pending prepared-entry reconciliation separately from verified saved-source coverage; preserve any existing gaps.

5. Return the identical verified [output:delivery_text] and [output:pre_delivery_status] for delivery, or actual partial-write/blocker findings.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:delivery_text] | The same exact final text, verified as recorded for delivery. | Required append/readback succeeds and returned text matches the recorded prepared text exactly; no future saved-source outcome is claimed. |
| [output:pre_delivery_status] | Verified paths/coverage or precise blocker/partial status. | Mandatory timing is satisfied or exact unresolved work remains explicit; never claim unsaved source outcome is already durable. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
