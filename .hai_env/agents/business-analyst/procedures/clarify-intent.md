# Clarify intent

## Description

Resolve consequential gaps through identifiable, durably verified questions and
attributable answers while preserving every decision revision.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:context_result] | Current request, authority, Activity, relevant context and prior dialogue from Acquire context. | Mandatory | Explicit prior procedure result. | Retrieve context before dependent clarification. |
| [input:human_response] | Actual human response and host-observed source/event identity. | Optional | Current chat through host. | Preserve unanswered status and wait; no inferred answer. |
| [input:persistence] | Host's authorized serialized activity record operation and readback capability. | Mandatory | Host/runtime. | Report exact unavailable operation/ledger path; stop dependent display/application. |

## Prerequisites

Validated current context and compatible active Activity; recorded dialogue is
readable, or confirmed absent/empty. Received answers have identifiable provenance.

## Rules

- **Question rationale.** Business analyst MUST summarize each remaining blocker in one sentence immediately before its question.
- **Logical batches.** Business analyst MUST collect all currently necessary questions in one logical batch and wait for actual answers before deciding on a further batch or advancing dependent work; interface splitting preserves the one batch and IDs.

## Steps

1. Reconcile [input:context_result] with current chat and the ledger. Use prior
   event IDs for already recorded occurrences; redisplay an unanswered question
   from readback without appending another event. Do not recycle IDs.
2. Compare intent, expected outcomes, actors, motivation, success measures,
   terminology, workflows, behavior and business rules with effective decisions.
   Examine boundaries, priorities, exclusions, acceptance/completion, technical
   restrictions, dependencies, integrations and external resources; inputs,
   outputs, formats, origins, schemas and validation; stakeholders, permissions,
   security, privacy and applicable compliance. Consider relevant edge cases,
   errors, fallback/recovery, performance/scale, availability, accessibility,
   region/language, compatibility, migration, deployment, configuration,
   observability, rollback and verification. This inventory does not add features.
3. Detect internal contradictions and conflicts with known requirements,
   specifications, architecture and conventions. Separate safe implementation
   choices and supported assumptions from consequential human decisions. If no
   blocker remains, proceed to assessment without manufacturing questions.
4. Prepare all necessary questions under the dialogue contract with the next
   Activity-scoped batch/question IDs, rationale, full wording, impact, complete
   options, marked recommendation if any, unchecked choices, Other placeholder
   and unanswered status. Send exact blocks plus predecessor evidence through
   [input:persistence]. On first question, this creates the meaningful ledger even
   before a proposal exists. Read back and verify exact saved blocks before
   displaying them and the compact copyable answer form. Respect host limits by
   displaying sequential parts of the same saved batch; explain how to answer all
   IDs before reassessment. Wait for actual human response.
5. For [input:human_response], preserve raw choices and explanations verbatim and
   map each multipart answer to its exact ID/part. For ambiguity, first persist
   an unresolved event with raw text/candidate IDs; ask a new recorded mapping
   question, and hold application until an actual mapping answer is saved.
   Subsequent response events retain original raw text and mapping provenance.
6. Append per-question numbered responses in reception order. Changed decisions
   are explicit revisions linking the latest superseded response. Verify each
   exact event by reading the ledger before using it. A failed read/write/readback
   reports path and underlying error, stops dependent display/application/proposal,
   retains partial evidence and does not automatically retry or repair.
7. After verified persistence, reassess context and blockers. Reapply readiness
   when goals/scope/acceptance change. Ask another batch only for remaining
   consequential gaps; do not ask answered questions again. Return
   [output:clarification_result] and explicitly pass it as `clarification_result`
   to [Assess and propose](assess-and-propose.md).

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:clarification_result] | Current context, verified event IDs/paths, effective decisions, received raw responses, blockers and capability failures. | No unverified answer is applied; unanswered/ambiguous work remains explicit and complete ledger preserved. |

## References

- [Role definition](../SKILL.md) — inherited rules and boundaries.
- [Dialogue contract](../conventions/clarification-dialogue.md) — canonical blocks, IDs and host transaction/readback.
- [Readiness convention](../conventions/requirements-readiness.md) — reassessment conditions.
