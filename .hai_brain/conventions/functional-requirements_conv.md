# Functional requirements convention

## Type

`functional-requirements`

Definition and classification scope: [Functional requirements](../concepts/specification.md#functional-requirements).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Context:** the capability, actors, goals, and system boundary.
- **Requirements:** stable requirement IDs, observable behavior, triggers, preconditions, inputs, and outcomes.
- **Alternative and failure behavior:** invalid inputs, unavailable dependencies, cancellation, and relevant edge cases.
- **Acceptance criteria:** observable conditions that demonstrate each requirement is satisfied.
- **Relationships and unknowns:** linked business rules, quality constraints, interfaces, tests, dependencies, and open questions.

## Writing rules

- Describe what the product must do without prescribing internal implementation unless it is an explicit constraint.
- For AI behavior, define permitted actions, output expectations, uncertainty handling, and human handoffs where applicable.
- Link shared policies and thresholds to their canonical leaves; keep requirement IDs stable when wording changes.
