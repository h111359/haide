# Recovery guide convention

## Type

`recovery-guide`

Definition and classification scope: [Recovery guide](../concepts/specification.md#recovery-guide).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`.

## Required content

- **Recovery scenario:** failure or loss covered, scope, declaration authority, and linked recovery-time and recovery-point targets.
- **Readiness and backups:** dependencies, access, backup execution or source, integrity checks, and compatible restore versions.
- **Recovery steps:** containment, restoration or failover sequence, dependencies, checkpoints, and expected observations.
- **Validation and return:** data integrity, reconciliation, service checks, failback, and conditions for resuming writes or normal traffic.
- **Drills and evidence:** rehearsal method, evidence locations, ownership, escalation, and known unrecoverable gaps.

## Writing rules

- Identify destructive steps, irreversible data changes, split-brain risks, and concrete stop conditions where relevant.
- Link target requirements and backup infrastructure rather than redefining them.
- Distinguish a backup's existence from evidence that restoration succeeds; never claim recovery readiness without supporting evidence.
