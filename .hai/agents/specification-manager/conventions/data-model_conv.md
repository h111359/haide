# Data model convention

## Type

`data-model`

Definition and classification scope: [Data model](../concepts/specification.md#data-model).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Model context:** the domain, model level (conceptual, logical, or physical), and owning components.
- **Entities and structures:** identities, keys, aggregates, document shapes, and links to field definitions.
- **Relationships:** cardinality, optionality, ownership, references, and lifecycle coupling.
- **Structural constraints:** uniqueness, referential integrity, state consistency, and storage mapping as applicable.
- **Evolution and unknowns:** schema version compatibility, migration constraints, linked decisions, and unsettled modeling issues.

## Writing rules

- Identify the model level so conceptual entities are not mistaken for actual tables or collections.
- Include text explanations alongside diagrams or fenced schema excerpts.
- Link field semantics, domain rules, interface schemas, and privacy policies rather than maintaining competing definitions.
