# Data dictionary convention

## Type

`data-dictionary`

Definition and classification scope: [Data dictionary](../references/specification.md#data-dictionary).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Dataset context:** the entity, dataset, or namespace covered and its canonical model link.
- **Field definitions:** qualified name, meaning, data type, format, units, nullability, and default where applicable.
- **Value constraints:** enumerations, ranges, precision, normalization, validation, and sentinel meanings.
- **Provenance and quality:** source, ownership, derivation links, freshness expectations, and quality limitations.
- **Examples and relationships:** representative non-sensitive values, glossary links, security classifications, and unknowns.

## Writing rules

- Distinguish absent, null, empty, zero, and unknown when their meanings differ.
- Reference canonical wire schemas or storage schemas instead of copying definitions maintained there.
- Include source and licensing constraints for datasets by linking Inventory or Security as appropriate.
