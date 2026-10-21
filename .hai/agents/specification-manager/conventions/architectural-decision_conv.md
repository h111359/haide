# Architectural decision convention

## Type

`architectural-decision`

Definition and classification scope: [Architectural decision](../references/specification.md#architectural-decision).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Identity:** stable decision ID, title, decision date, decision state, and responsible participants.
- **Context and drivers:** the problem, constraints, quality concerns, and evidence available at decision time.
- **Alternatives:** viable options and their meaningful tradeoffs.
- **Decision and consequences:** the chosen approach, reasons, benefits, costs, risks, and follow-up obligations.
- **Relationships and review:** affected leaves, related or superseding decisions, and reconsideration conditions.

## Writing rules

- Record one significant choice per leaf; describe the resulting current design in its own appropriate type.
- Use decision states proposed, accepted, rejected, or superseded, independently of the leaf's document status.
- Preserve accepted decision history; use a new linked decision to supersede a choice rather than rewriting its rationale.
