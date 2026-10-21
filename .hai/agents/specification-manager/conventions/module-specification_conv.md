# Module specification convention

## Type

`module-specification`

Definition and classification scope: [Module specification](../references/specification.md#module-specification).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Responsibility and boundaries:** module purpose, owned behavior, exclusions, and links to requirements.
- **Structure and dependencies:** internal parts, dependency direction, external collaborators, and source locations.
- **Internal behavior:** state, lifecycle, invariants, failure handling, concurrency, and extension points as applicable.
- **Configuration:** options, defaults, validation, feature switches, and compatibility constraints.
- **Relationships and unknowns:** linked contracts, data, flows, algorithms, tests, decisions, and unsettled design points.

## Writing rules

- Describe one bounded component; link system-wide context rather than repeating architecture.
- For AI modules, identify model dependencies, prompt assembly, retrieval context, environment boundaries, and tool access where applicable.
- Separate intended design from observations about current implementation and identify discrepancies explicitly.
