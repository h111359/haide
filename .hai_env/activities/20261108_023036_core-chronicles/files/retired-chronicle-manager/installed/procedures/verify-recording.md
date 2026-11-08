# Verify recording

## Description

Verify completed-source coverage synchronously for an identified operation and return fresh recording evidence, verified disabled/no-obligation status or precise blockers. The requesting domain owner decides how to use that result.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:recording_requirement] | Validated chronicles flag and effective enablement boundary, or independent mandatory workspace recording/timing requirement. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:activity_assignment] | host coordinator-assigned existing stable Activity ID, safe folder and exact source-exchange boundaries. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:source_metadata] | Authoritative source session ID, original start time, durable saved local source path and readable completed messages. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:coverage_context] | Relevant prior session attribution/segment metadata across affected Activities, or precise segments to inspect for overlap checks. | Mandatory | host coordinator plus available authoritative metadata | Missing coverage context is an explicit verification limit and blocks writes that could overlap unresolved assignments. |
| [input:existing_segments] | Existing segment paths. | Optional | Caller and selected Activity metadata | Inspect relevant assigned metadata only; never broadly reread unrelated history. |
| [input:operation_evidence] | Verified completed domain operation with a descriptive label and its actual result/message. | Optional | host coordinator and the responsible domain owner's verified evidence | Omit operation metadata; never infer a completed operation from a proposal. |
| [input:historical_import] | Explicitly authorized historical import and provenance. | Optional | The user's permission relayed by host coordinator | Exclude earlier off periods. Authorized byte-preserving moves retain original paths/import dates/source limitations separately in Activity provenance. |
| [input:planned_operation] | Specific identified operation and the relevant completed-source boundary; execution may still be planned. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |

## Prerequisites

A validated recording requirement or applicable independent mandatory instruction, an assigned existing Activity and exact source context are available. Read the [transcript segment convention](../conventions/transcript-segment_conv.md) before segment writes.

## Rules

- **Completed source.** Codex Chronicle-manager MUST limit this verification to completed saved source for the identified operation.
- **Future results.** Codex Chronicle-manager MUST NOT require future operation results or an undelivered final response to verify completed saved source.
- **Result use.** Codex Chronicle-manager MUST leave the decision about how verification affects the requested action to the specialist responsible for that action.

## Steps

1. Establish [input:workspace_root], load [input:instructions], identify [input:planned_operation] and resolve [input:authority]/[input:recording_requirement] and the effective source boundary.

2. If optional recording is off with no independent obligation, return freshly verified disabled/no-obligation [output:recording_verification] without files.

3. Otherwise execute [Synchronize segments](synchronize-segments.md), explicitly passing [input:workspace_root] to target `workspace_root`, [input:instructions] to `instructions`, [input:authority] to `authority`, [input:recording_requirement] to `recording_requirement`, [input:activity_assignment] to `activity_assignment`, [input:source_metadata] to `source_metadata`, [input:coverage_context] to `coverage_context`, [input:existing_segments] to `existing_segments`, [input:operation_evidence] to `operation_evidence`, and [input:historical_import] to `historical_import`.

4. Freshly check every relevant assigned segment against the identified operation, source boundary and returned coverage, including earlier pending eligible ranges across the assigned enabled intervals. For closure, inspect retained-source completeness and all required coverage through the closure-request cutoff, not only the latest batch or checkpoint timestamp. If required source or segment verification remains missing/divergent/conflicting, return the exact blockers; otherwise include fresh verification even when no new eligible text exists.

5. For closure, return the core recording-evidence convention's complete proof, including a unique verification ID, exact Activity/operation/cutoff and enabled intervals, retained-source completeness, gaps/conflicts, active-write status and SHA-256 snapshots of the assigned source files and relevant Activity-relative segments/checkpoint. Obtain snapshots from actual readback, stop writes, and pass the result to host coordinator; do not close or rename the Activity. Return [output:recording_verification] synchronously with operation identity, Activity IDs, segment paths, source identity, completed-source boundaries, coverage and actual partial/blocked status.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:recording_verification] | Identified operation, Activity IDs, segment paths, source identity and fresh completed-source coverage; verified disabled/no-obligation status; or exact blocker/partial status. | Every relevant assigned segment is freshly verified for this operation, or an explicit disabled/no-obligation result or unresolved source/coverage blocker is returned. Recording is never implicitly enabled and no domain action is performed. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
