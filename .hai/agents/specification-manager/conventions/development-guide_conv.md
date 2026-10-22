# Development guide convention

## Type

`development-guide`

Definition and classification scope: [Development guide](../concepts/specification.md#development-guide).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`. Link canonical contributor and AI instruction files in the workspace.

## Required content

- **Working context:** repository responsibilities, relevant architecture links, applicable contributor roles, and a link to a [Workspace structure](../concepts/specification.md#workspace-structure) leaf when available.
- **Local setup and commands:** toolchain versions, environment preparation, build, run, test, formatting, and troubleshooting instructions as applicable.
- **Engineering conventions:** naming, coding, dependency, review, and documentation practices for this workspace.
- **Human and AI workflow:** context discovery, instruction-file locations, task handoff, verification expectations, and workspace-specific action boundaries.
- **Maintenance and unknowns:** authoritative sources, ownership, update triggers, known setup gaps, and links to relevant decisions.

## Writing rules

- Keep instructions specific to development of this product; reusable agent and framework instructions remain in their own packages outside the product specification.
- Link authoritative instruction files instead of creating conflicting copies; identify which instructions apply to which workspace areas.
- Keep the directory map and path-based discovery guidance in Workspace structure; link it rather than maintaining a second map here.
- Keep temporary requests and execution records in caller-managed work records outside the specification, and runtime product AI behavior in its relevant product specification leaves.
