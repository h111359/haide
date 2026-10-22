# Algorithm specification convention

## Type

`algorithm-specification`

Definition and classification scope: [Algorithm specification](../concepts/specification.md#algorithm-specification).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`. Put pseudocode, formulas, or prompt templates in fenced blocks where useful.

## Required content

- **Problem and assumptions:** purpose, applicable domain, preconditions, and linked requirements or business policies.
- **Inputs and outputs:** types, units, ranges, validity conditions, and expected result properties.
- **Method:** ordered computation, formulas, parameters, invariants, tie breaking, and termination.
- **Limits and failure behavior:** precision, rounding, complexity, resource bounds, invalid inputs, and known weaknesses.
- **Examples and verification:** worked cases, boundary cases, linked tests or evaluations, and unresolved choices.

## Writing rules

- Describe the method precisely enough to reproduce its intended behavior independently of a programming language.
- For probabilistic or AI methods, state model assumptions, prompt or context structure, sampling parameters, reproducibility limits, and output validation.
- If an executable prompt or algorithm is canonical in the workspace, link its source rather than keeping a second editable copy.
