# Cloud convention

## Type

`cloud`

Definition and classification scope: [Cloud](../references/specification.md#cloud).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`. Link canonical provider-specific infrastructure-as-code and configuration sources.

## Required content

- **Provider context:** provider, account or project organization, environment separation, ownership, and regions.
- **Service mapping:** provider services and resources implementing workload roles, dependencies, and selected capabilities.
- **Configuration:** resource settings, quotas, scaling, connectivity, identity bindings, and configuration-source references.
- **Cost and resilience controls:** budgets, allocation tags, regional constraints, availability mechanisms, and linked requirements.
- **Relationships and unknowns:** portable infrastructure, security policy, inventory, operating guides, decisions, and unresolved provider constraints.

## Writing rules

- Document provider-specific details once here and link them from architecture or portable infrastructure leaves.
- Record the source and verification date for provider limits or capabilities that affect the design.
- Link observed instance registers and secret references rather than copying volatile inventories or credentials.
