# Implementation plan format

## Purpose and scope

This convention defines a readable output format for implementation plans created or revised by Solution architect. The plan explains the work to a human who has not read the conversation.

The format applies to the assigned work, without requiring a particular project, phase count or technical design. Planning remains separate from permission to implement.

## Plan overview

The plan starts with one H1 title, a short objective, and these H2 sections in
order: Execution contract, Acceptance criteria, Plan overview. Follow those with
one H2 per phase and File inventory; optional Risks and References follow it.
New plans use format `hai-plan-v1`; older plans remain preserved and require
explicit host revision before use under the new execution contract.

Execution contract uses one `- Key: value` line per field, each unique and
nonblank: Format, Activity, Input revision, Decision revision, Mode, Readiness,
Authority, Business readiness, Readiness evidence, Business limits, Technical
limits, Timing limits, Authorization limits, Assumptions, Knowledge updates,
Required owners. Activity is the runtime UUID; revisions identify exact current
sources or `none` for an established absence of prior decisions.

Format is `hai-plan-v1`; Mode is `normal` or explicitly selected `accelerated`.
Readiness is `ready` or `blocked`; Business readiness is `passed`, `exempt` or
`blocked` with attributable evidence. Empty constraints use an explicit explanation
such as `No additional timing limit supplied`, not a blank field.

Authority preserves actual human scope and exact covering protected-maintenance
permission. Record consequences of assumptions, choices actually delegated,
required owners and precise knowledge deltas. No authorization is created by a
ready plan or a helper's success.

Acceptance criteria uses `ID | Criterion | Verification` with unique `A1`, `A2`,
etc. Each criterion has observable pass/fail evidence. The Plan overview contains:

| Phase | Goal | Depends on | Expected result |
| --- | --- | --- | --- |
| Unique phase number and action title | One concise goal | Earlier phase numbers and short reasons, or None | Observable result |

Agreed requirements, proposed design and open decisions have distinct labels. An unresolved decision appears before the actions that depend on it, with those actions marked as waiting for the decision.

Dependencies include their logical reasons, rather than phase numbers alone. Independent work is identified explicitly where it affects the execution order.

In the supported table, Depends on is `None` or earlier phase numbers with a
reason, formatted `1: contract required, 2: producer output required`. Separate
dependencies with commas and avoid commas inside each reason. Forward, nonexistent
or duplicate dependency references are invalid.

## Phase structure

Each phase heading is `## Phase N — Action title` with unique positive N in
execution order. Each phase uses these H3 sections in this order:

| Section | Content |
| --- | --- |
| Purpose | What the phase achieves, in familiar words |
| Why now | Why this work comes next, including the result needed from an earlier phase |
| Visible result | What a reader can inspect or demonstrate afterward; Before → After where useful |
| Scope | The smallest useful scenario or example and significant work deferred to later phases |
| Actions | Numbered actions in execution order, with their purpose or expected result |
| Affected files | A focused change table or references to entries in a separate file inventory |
| Complete when | Observable checks tied to the relevant acceptance criteria |

Purpose, Why now, Visible result and Scope use short bullets. Explanations give the reasoning specific to that phase rather than repeating boilerplate.

The Actions table has three columns:

| Step | Action | Purpose or expected result |
| --- | --- | --- |
| Unique identifier such as 2.1 | One action beginning with a concrete verb | Why it is needed or what it produces |

Phase numbers and step identifiers are unique within the plan. Each row or action bullet contains one action; routine actions need no extended explanation.

For machine-validated execution plans, Actions uses the table above and a second
table with exact columns `Task | Target | Operation | Depends on | Acceptance | Check`.
Both tables list the same task IDs in order. IDs are `N.M` with positive integers;
dependencies are earlier task IDs separated by commas, or `None`.

Target is one exact workspace-relative path, optionally enclosed in backticks,
and appears in File inventory. Operation gives actionable natural-language detail
or the exact command/tool invocation with output destination and expected result.
Acceptance lists criterion IDs separated by commas; every criterion is mapped.
Check identifies observable task completion. Record cross-target consistency as
dependencies or checks beside the relevant task, not an ambiguous multi-target row.

The supported mechanical plan schema contains workspace targets only. A requested
outside operation requires explicit human location/purpose permission and a scoped
host handoff; it is not silently encoded as a workspace target.

## Affected files

For each planned artifact, record its purpose, owner, intended lifetime and
canonical destination in the existing inventory or adjacent phase context under
the shared [artifact placement contract](../../../../.hai/conventions/artifact-placement_conv.md).
Distinguish deliverables/reusable resources from scratch and execution evidence;
implementation mappings and run results do not become package resources merely
because they were useful during the task. This adds no mandatory separate manifest
or new table schema. Resolve destination conflicts before dependent creation.

File changes use a separate table with three columns:

| Path | Change | Purpose |
| --- | --- | --- |
| Exact repository-relative path, labeled Existing or Proposed | Add, Edit, Move or Delete | Short explanation of the change |

Existing files have links to their actual paths. Proposed files are labeled clearly without links suggesting that they already exist. Moves show both source and destination paths.

Unknown filenames or unresolved locations are stated as open decisions rather than presented as exact paths. A large inventory lives in its own section or linked appendix; phases reference the relevant entries instead of repeating it.

Machine-validated plans use a local `## File inventory` with plain exact paths
(optionally in backticks), one unique row per target and Add/Edit/Move/Delete/Inspect
as Change. Keep existing-file links in adjacent supporting prose when needed;
required execution semantics stay directly in the plan, not unavailable appendices.

## Completion and supporting detail

Completion checks name the behavior, artifact or verification to inspect and its expected outcome. Planned checks remain distinct from checks already performed; a proposed command is not a successful result.

Include appropriate automated tests, documentation/knowledge changes and owner
validation. Where inspection alone suffices or no documentation change is needed,
record the reason. Name human/external acceptance methods for nonautomatic checks.
Missing mandatory decisions, paths, commands, conventions or permissions keep the
affected plan blocked; accelerated mode omits no safeguard.

Dependencies, material risks, acceptance mapping and critical constraints remain visible beside the affected work or through explicit references. Technical detail belongs in a linked appendix when it would obscure the main sequence; the phase retains enough information to understand and perform its actions.

## Readability

Explanatory paragraphs contain at most two sentences and 40 words. Table cells contain short phrases or one short sentence; extended explanations belong in bullets outside the table.

Familiar words introduce the work, and necessary technical terms are explained on first use. Exact identifiers retain their spelling. The plan contains the context needed to understand its phases without asking for a separate explanation from the chat.

## References

- [Agent definition](../SKILL.md) — scope and the requirement to use this format.
- [Prepare implementation plan](../procedures/prepare-implementation-plan.md) — plan preparation and self-review workflow.
- [Helper contract](../scripts/README.md) — exact supported syntax, validation commands and limits.
