# Deployment guide convention

## Type

`deployment-guide`

Definition and classification scope: [Deployment guide](../references/specification.md#deployment-guide).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Procedure context:** installation or release scenario, operator role, supported versions, and target environment.
- **Prerequisites:** approved artifact, access, configuration, compatibility, backups, maintenance windows, and go or no-go checks as applicable.
- **Steps:** ordered actions, explicit command context, expected observations, and migration or coordination steps.
- **Verification and rollback:** health checks, acceptance evidence, stop conditions, rollback prerequisites, actions, and limitations.
- **Completion and escalation:** handover, cleanup, release records, responsible roles, and linked recovery procedures.

## Writing rules

- Mark destructive or irreversible steps and explain their concrete preconditions.
- Use placeholders for environment-specific values and secret references; never include credentials.
- Link pipeline automation and canonical scripts; identify when data migration prevents ordinary rollback.
