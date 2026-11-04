# Implementation plan format

## Purpose and scope

This convention defines a readable output format for implementation plans created or revised by Solution architect. The plan explains the work to a human who has not read the conversation.

The format applies to the assigned work, without requiring a particular project, phase count or technical design. Planning remains separate from permission to implement.

## Plan overview

The plan starts with a short objective and an overview table:

| Phase | Goal | Depends on | Expected result |
| --- | --- | --- | --- |
| Unique phase number and action title | One concise goal | Earlier phase numbers and short reasons, or None | Observable result |

Agreed requirements, proposed design and open decisions have distinct labels. An unresolved decision appears before the actions that depend on it, with those actions marked as waiting for the decision.

Dependencies include their logical reasons, rather than phase numbers alone. Independent work is identified explicitly where it affects the execution order.

## Phase structure

Each phase uses the following sections in this order:

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

## Affected files

File changes use a separate table with three columns:

| Path | Change | Purpose |
| --- | --- | --- |
| Exact repository-relative path, labeled Existing or Proposed | Add, Edit, Move or Delete | Short explanation of the change |

Existing files have links to their actual paths. Proposed files are labeled clearly without links suggesting that they already exist. Moves show both source and destination paths.

Unknown filenames or unresolved locations are stated as open decisions rather than presented as exact paths. A large inventory lives in its own section or linked appendix; phases reference the relevant entries instead of repeating it.

## Completion and supporting detail

Completion checks name the behavior, artifact or verification to inspect and its expected outcome. Planned checks remain distinct from checks already performed; a proposed command is not a successful result.

Dependencies, material risks, acceptance mapping and critical constraints remain visible beside the affected work or through explicit references. Technical detail belongs in a linked appendix when it would obscure the main sequence; the phase retains enough information to understand and perform its actions.

## Readability

Explanatory paragraphs contain at most two sentences and 40 words. Table cells contain short phrases or one short sentence; extended explanations belong in bullets outside the table.

Familiar words introduce the work, and necessary technical terms are explained on first use. Exact identifiers retain their spelling. The plan contains the context needed to understand its phases without asking for a separate explanation from the chat.

## References

- [Agent definition](../SKILL.md) — scope and the requirement to use this format.
- [Perform assigned work](../procedures/perform-assigned-work.md) — plan preparation and self-review workflow.
