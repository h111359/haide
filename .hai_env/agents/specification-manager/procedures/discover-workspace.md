# Discover workspace information

## Description

Discover product paths and source knowledge within verified roots and exclusions, and return evidence-grounded findings with unresolved coverage limits.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:inspection] | Validated invocation and specification root | Mandatory | Locate and inspect the specification result | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:source_roots] | Verified workspace/product source roots and discovery authority | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:ignore_evidence] | Targeted exclusion or repository-ignore evidence from a selected optional extension, when relevant | Optional | Caller or selected extension through host coordinator | Continue ordinary bounded filesystem discovery under known exclusions; report repository-specific ignore coverage as unverified. |
| [input:product_evidence] | Authoritative manifests, lockfiles or reliable documentation | Optional | Caller or authorized context | Discover authorized reliable evidence outside excluded descendants; report uncertain classifications. |

## Prerequisites

Verified `inspection` output from [Locate and inspect the specification](locate-and-inspect.md), supplied as [input:inspection]. Verified [input:source_roots] and explicit product-discovery authority; the specification root alone establishes neither.

## Rules

- **Bounded inspection:** Specification-manager MUST NOT recursively read unrelated, private, secret-bearing, generated or uncertain descendants to claim complete coverage.
- **Optional ignore interpretation:** Specification-manager MAY request repository-ignore interpretation from a selected optional extension through host coordinator ONLY IF it is relevant to the agreed discovery task.
- **Independent filesystem work:** Specification-manager MAY continue permitted filesystem discovery without [input:ignore_evidence].
- **Ignore-coverage limit:** Specification-manager MUST NOT claim verified repository-ignore coverage when the relevant evidence is missing.

## Steps

1. Establish [input:source_roots] against [input:inspection] and read the workspace-structure discovery boundaries. Identify caller exclusions, reusable packages/working records and dependency roots; in HAI use, exclude workspace-root `.hai/`, `.hai_env/` and `hai_agents_library/` descendants from product registration/reverse-engineering.
2. Inspect permitted directory entries and targeted authoritative files. Apply caller privacy/exclusions and relevant supplied [input:ignore_evidence]. If optional repository evidence is needed, return a specific extension request through host coordinator; continue independent bounded filesystem discovery and record unverified repository-ignore coverage.
3. Identify third-party/vendored libraries and dependency roots from permitted manifests, lockfiles, configuration or reliable documentation outside excluded descendants. Represent each verified library only by top folder and purpose. Distinguish first-party code and report uncertain classifications rather than inferring a dependency merely from `lib`/`libraries` names.
4. Verify mapped paths/purposes using directory entries and targeted authoritative evidence. Check new workspace registrations and inferred product details against exclusions/library limits. Record coverage gaps and [input:product_evidence] provenance without broadening scope.
5. Pass [output:discovery] as `task_result` to [Verification and handoff](verify-and-handoff.md), with the verified explicit root as `specification_root`; receive actual verification before returning [output:discovery] with evidence and limits.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:discovery] | Verified product-path and source knowledge within exclusions | Ignored paths and package/working-record exclusions respected; libraries represented only by verified root and purpose; gaps explicit. |

## References

- [Role rules and references](../SKILL.md) — shared invocation, contract, sources and type conventions.
- [Specification format](../concepts/specification.md) - structure, classification, type registry, and lifecycle - required before specification work.
- [Contract versioning](../conventions/contract-versioning_conv.md) and [package contract](../contract.json) - target version, baseline, transition ledger, adoption/migration gates and verification - required when specification work begins; not general startup.
- This package's `conventions/<type>_conv.md` files - leaf content formats - conditional for types created or changed; read only those types.
- [Workspace structure convention](../conventions/workspace-structure_conv.md#discovery-boundaries) - discovery exclusions and library boundaries - required before mapping workspace paths or reverse-engineering implementation.
- [Audit helper instructions](../scripts/README.md) - runtime, paths, usage, and limits - required on first audit use.
- [Audit fixture tests](../scripts/test_audit_specification.py) - helper verification - conditional when changing the helper itself.
- Caller-supplied workspace instructions, HAI validation context, and source lifecycle information — required as applicable to HAI-managed work, including validated enabled-feature/location assurance; standalone package invocation requires no HAI files, but HAI-managed work must not be reclassified as standalone to bypass missing or invalid context.
