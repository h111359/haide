# Security convention

## Type

`security`

Definition and classification scope: [Security](../concepts/specification.md#security).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Protection context:** assets, actors, data classifications, trust boundaries, and applicable obligations.
- **Threats and abuse cases:** entry points, attacker capabilities, consequences, and risk assumptions.
- **Requirements and controls:** stable IDs, authorization, privacy, retention, secret handling, audit, and protective mechanisms as applicable.
- **Assurance and exceptions:** control ownership, linked verification, residual risks, accepted exceptions, and review conditions.
- **Sources and relationships:** authoritative obligations, effective dates, implementation leaves, response guides, and open questions.

## Writing rules

- Distinguish required policy, designed controls, and evidence that controls are implemented.
- For AI features, address untrusted context, prompt injection, tool permissions, data disclosure, harmful use, and human oversight where applicable.
- Record references to protected evidence or secrets instead of sensitive values; do not infer compliance from an approved document status.
