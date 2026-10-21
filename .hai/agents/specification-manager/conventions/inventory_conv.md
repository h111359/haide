# Inventory convention

## Type

`inventory`

Definition and classification scope: [Inventory](../references/specification.md#inventory).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Register scope:** asset category, environments covered, and inclusion or exclusion criteria.
- **Asset entries:** stable identifier, name, role, version or revision, location reference, owner, and lifecycle state as applicable.
- **Dependencies and obligations:** supplier, consumers, license, support period, and linked usage or policy constraints.
- **Evidence and freshness:** source of each fact, observation date, verification method, and update responsibility.
- **Gaps and relationships:** unknown values, stale entries, and links to intended designs or replacement decisions.

## Writing rules

- Record observed facts separately from planned assets; mark stale or unverified information explicitly.
- For models and datasets, include provenance, revision, licensing, and linked quality or privacy limitations.
- Store references to sensitive systems or secret locations, never credentials or secret values.
