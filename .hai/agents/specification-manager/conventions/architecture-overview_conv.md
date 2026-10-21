# Architecture overview convention

## Type

`architecture-overview`

Definition and classification scope: [Architecture overview](../references/specification.md#architecture-overview).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **System context:** users, external systems, responsibilities, boundaries, and major constraints.
- **Component view:** principal components, their roles, ownership boundaries, and dependency direction.
- **Interaction view:** major communication and data paths, trust zones, and runtime coordination.
- **Deployment view:** logical runtime units and their allocation to environment roles.
- **Relationships and unknowns:** linked modules, hosting designs, quality constraints, decisions, and unresolved architecture questions.

## Writing rules

- Use diagrams when they clarify relationships and explain each diagram's scope in text.
- Keep views consistent and distinguish current architecture from proposed changes.
- Link resource configuration, detailed workflows, and decision rationale to their canonical leaves.
