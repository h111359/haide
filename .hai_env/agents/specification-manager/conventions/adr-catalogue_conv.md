# ADR catalogue convention

## Type

`adr-catalogue`

Definition and classification scope: [ADR catalogue](../concepts/specification.md#adr-catalogue).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Catalogue scope:** the system or domain whose decisions are indexed.
- **Decision table:** stable decision ID, title, decision state, date, short subject summary, and relative link to each record.
- **Decision relationships:** supersedes, superseded by, and related decisions where applicable.
- **Navigation:** useful topic grouping or ordering without repeating complete decision records.
- **Consistency notes:** unresolved missing records or inconsistencies requiring correction.

## Writing rules

- Derive index facts from canonical Architectural decision leaves; update the index when those facts change.
- Distinguish decision state from document status and implementation status.
- Preserve entries for rejected and superseded decisions when they explain the architecture's history.
