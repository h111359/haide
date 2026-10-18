# Quality requirements convention

## Type

`quality-requirements`

Definition and classification scope: [Quality requirements](../concepts/specification.md#quality-requirements).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Context:** affected capabilities, environments, workloads, and stakeholders.
- **Quality scenarios:** stable IDs, triggering conditions, expected responses, and applicable operating conditions.
- **Measures and targets:** units, thresholds, measurement windows, percentiles or populations, and tolerances.
- **Constraints and tradeoffs:** resource or cost budgets, compatibility limits, priorities, and justified exceptions.
- **Verification links and unknowns:** measurement methods, linked test specifications, evidence sources, and unsettled targets.

## Writing rules

- Replace words such as fast or reliable with measurable scenarios; mark unagreed thresholds as unknown.
- Define dataset, sampling, and statistical interpretation for AI quality targets.
- Keep security obligations in Security and telemetry implementation in Observability.
