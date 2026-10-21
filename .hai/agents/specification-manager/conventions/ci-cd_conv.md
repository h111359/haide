# CI/CD convention

## Type

`ci-cd`

Definition and classification scope: [CI/CD](../references/specification.md#cicd).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`. Link canonical pipeline configuration in the workspace.

## Required content

- **Pipeline context:** repositories, triggers, branches or tags, environments, and automation responsibilities.
- **Stages and dependencies:** jobs, ordering, execution environments, inputs, outputs, caching, and concurrency rules.
- **Checks and gates:** linked tests, security checks, approval conditions, failure behavior, and exception handling.
- **Artifacts and delivery:** versioning, provenance, storage, promotion, deployment automation, and automated rollback conditions.
- **Maintenance and unknowns:** configuration sources, ownership, secret references, troubleshooting links, and unresolved pipeline limitations.

## Writing rules

- Describe automated behavior here and human deployment decisions in Deployment guide.
- Link test definitions and security policy instead of maintaining duplicate thresholds or controls.
- Distinguish a successful build from successful deployment and verified product behavior.
