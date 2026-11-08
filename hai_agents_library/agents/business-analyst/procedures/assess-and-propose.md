# Assess and propose

## Description

Assess requirements readiness and return a complete replacement-input proposal
for human review and responsible-owner application.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:clarification_result] | Context, original human authority, verified dialogue, effective decisions and blockers. | Mandatory | Clarify intent result or host-supplied equivalent. | Retrieve current evidence; hold dependent proposal. |
| [input:target] | Proposed current Activity input or caller-specified request section. | Optional | Host/caller. | Use proposed current Activity input; presume no legacy container. |
| [input:path_evidence] | Initial/touched path snapshots and explicit covering maintenance authority. | Mandatory | Host and current writer. | Report unavailable inspection; stop affected finalization. |

## Prerequisites

Validated active Activity and configuration; relevant context and dialogue are
readable. Human answers used by assessment have verified durable records.

## Rules

- **Proposal headings.** Business analyst MUST use only headings at level three or deeper inside proposed replacement text.
- **Proposal separation.** Business analyst MUST keep the dialogue history in the ledger rather than embed a transcript in the proposal.

## Steps

1. Compare [input:clarification_result] with the latest request and decisions.
   Identify changed goals, scope or acceptance and invalidate stale readiness.
2. Evaluate every current readiness item with an attributable evidence reference.
   For an exemption, record its exact kind, reason and qualifying observed scope;
   for assumptions/deferrals, record resolved uncertainty and consequences if
   false. Explicit human decisions are not replaced with assumed answers.
3. Return failed item IDs and unresolved decisions through host coordinator. Hold
   the request from downstream technical analysis/planning/implementation. Pass
   failures explicitly as `context_result` to Clarify intent only with the current
   request/Activity/context needed there; then resume Acquire context if relevant
   sources changed. No later role is invoked by this procedure.
4. After pass or justified exemption and no remaining blocker or unverified
   response, prepare a copy-ready proposal for [input:target]. Include Intent,
   Effective decisions, Context with source attributions, Outcomes, Scope,
   Exclusions, Constraints and assumptions, and Acceptance criteria. Map every
   named deliverable to a verifiable condition; keep constraints separate. Mark
   its target and proposed status outside replacement text. Do not add technical
   architecture, implementation plans or product QA as clarification deliverables.
5. Inspect [input:path_evidence] under the protection contract. Retain exact
   covering human maintenance authorization and source for any downstream
   analysis/planning handoff. On unauthorized changes, emit the specified error
   with sorted exact paths and stop affected finalization without reverting.
6. Return [output:proposal_result] to the human/host with actual work, questions,
   answers, revisions, readiness evidence, artifact paths and unresolved
   dependencies. Host/runtime owns any authorized Activity input append and
   records original input/provenance/revisions. Backlog changes go to the
   authorized backlog owner; durable specifications go to Specification-manager.
   Keep such owner work pending until actual verified evidence returns. Proposal
   readiness grants neither acceptance, execution nor Activity closure.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:proposal_result] | Readiness assessment or failure, proposed replacement text/target, decisions, ledger paths, protection evidence and owner handoffs. | Actual evidence supports status; review/application/closure remain distinct and dependencies are explicit. |

## References

- [Role definition](../SKILL.md) — inherited rules and ownership.
- [Readiness convention](../conventions/requirements-readiness.md) — evidence checks and extensions.
- [Protection contract](../conventions/framework-protection.md) — final touched-path review.
- [Dialogue contract](../conventions/clarification-dialogue.md) — effective decisions and host persistence.
