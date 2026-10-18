# Infrastructure convention

## Type

`infrastructure`

Definition and classification scope: [Infrastructure](../concepts/specification.md#infrastructure).

## Content file

`content.md`, in Markdown, alongside the leaf's `__ncf__.md`. Link canonical infrastructure-as-code and configuration sources.

## Required content

- **Hosting context:** environments, hosted workloads, ownership, and provider-independent constraints.
- **Topology:** compute, network, storage, orchestration, DNS, certificate dependencies, and resource relationships.
- **Configuration and capacity:** allocation, scaling, isolation, persistent state, and configuration-source references.
- **Resilience and protection:** design mechanisms linked to quality targets and security policies.
- **Relationships and unknowns:** cloud mappings, observed inventory, deployment and recovery guides, and unsettled design points.

## Writing rules

- Describe intended topology and configuration separately from observed resource instances.
- Put provider-specific resources in Cloud and link them from portable workload roles.
- Reference secret-management mechanisms and canonical configuration without recording secret values.
