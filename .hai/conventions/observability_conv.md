# Observability convention

## Type

`observability`

Definition and classification scope: [Observability](../concepts/specification.md#observability).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Observation goals:** health questions, failure modes, user outcomes, and linked service targets.
- **Signals:** logs, metrics, traces, names, fields, units, aggregation, correlation, and emission points as applicable.
- **Collection and storage:** sampling, cardinality limits, routing, access, redaction, and retention configuration.
- **Interpretation and alerts:** indicator formulas, windows, dashboard links, alert conditions, severity, and response-guide links.
- **Verification and unknowns:** telemetry checks, known blind spots, ownership, and unresolved detection limits.

## Writing rules

- Keep normative service targets in Quality requirements and privacy or audit policy in Security.
- For AI features, distinguish operational signals from sampled quality evaluations and describe their interpretation limits.
- Link canonical dashboard and alert definitions; specify useful signals without exposing sensitive prompt or user content.
