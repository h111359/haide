# Interface contract convention

## Type

`interface-contract`

Definition and classification scope: [Interface contract](../references/specification.md#interface-contract).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`. Use fenced schemas and examples or links to canonical machine-readable contracts in the workspace.

## Required content

- **Boundary and participants:** provider, consumers, transport, purpose, and interface version.
- **Operations and messages:** names, inputs, outputs, payload schemas, validation, and representative examples.
- **Behavioral guarantees:** preconditions, side effects, errors, idempotency, ordering, retries, and limits as applicable.
- **Access and compatibility:** linked authentication and authorization policy, version negotiation, deprecation, and migration expectations.
- **Verification and unknowns:** contract test links, canonical schema locations, dependencies, and unresolved guarantees.

## Writing rules

- State guarantees from the consumer's perspective, independently of provider internals.
- Identify the authoritative source when schemas are maintained in code; link it rather than creating a conflicting copy.
- Use non-sensitive examples and define error semantics as precisely as success semantics.
