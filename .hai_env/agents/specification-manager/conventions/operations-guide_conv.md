# Operations guide convention

## Type

`operations-guide`

Definition and classification scope: [Operations guide](../concepts/specification.md#operations-guide).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Operational context:** service, task or incident scenario, responsible roles, and access prerequisites.
- **Recognition and diagnosis:** symptoms, alert links, health checks, likely causes, and decision points.
- **Actions:** ordered maintenance, administration, or mitigation steps with expected observations and command context.
- **Verification and escalation:** success criteria, stop conditions, failure paths, escalation roles, and recovery or deployment handoffs.
- **Records and follow-up:** evidence to retain, communication duties, cleanup, review cadence, and known limitations.

## Writing rules

- Separate diagnostic checks from actions that change service state and describe their consequences.
- Link telemetry definitions, security policies, and canonical scripts instead of restating them.
- Keep restoration and disaster failover in Recovery guide and release changes in Deployment guide.
