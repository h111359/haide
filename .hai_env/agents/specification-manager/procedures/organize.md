# Organize, split, and balance

## Description

Restructure the specification by coherent subjects while preserving content and identity relationships, and return verified topology, navigation, and reference results.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:inspection] | Root/compatibility and authorized scope | Mandatory | Locate and inspect the specification result | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:organization_request] | Requested structural outcome | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:baseline] | Existing error-free identity inventory baseline | Optional | Caller or authorized context | Capture outside the tree only when required for identity comparison; otherwise leave absent. |
| [input:preferences] | Explicit restructuring preferences | Optional | Caller or authorized context | Organize meaningfully under the existing tree contract; invent no caller preference. |

## Prerequisites

Verified `inspection` output from [Locate and inspect the specification](locate-and-inspect.md), supplied as [input:inspection]. Authorized structural outcome, relevant type conventions and an outside-tree identity baseline when comparison is required.

## Rules

- **Moved-node identity:** Specification-manager MUST retain a subject's UUID when moving or renaming its node.
- **New-node identity:** Specification-manager MUST assign a fresh UUID to a new node.
- **Split and merge identity:** Specification-manager MUST identify the continuing subject and retired-ID replacements when a split or merge changes identity.
- **No identity reuse:** Specification-manager MUST NOT reuse an ID for an unrelated subject.
- **Subject grouping:** Specification-manager MUST base regrouping and splitting on coherent subjects or classifications.
- **Configuration size:** Specification-manager MUST apply node-configuration size limits to `__ncf__.md` rather than assume they also limit leaf content.
- **Content size:** WHEN the relevant leaf convention defines additional content-file limits, Specification-manager MUST apply those limits.

## Steps

1. Run the audit helper with `--inventory` for [input:inspection] and [input:organization_request]. Use [input:baseline], or capture an error-free outside-tree baseline when identity comparison helps; retain supplied [input:preferences] and plan affected nodes before moves.
2. Design meaningful upper-level subject families and deeper subjects/domains/modules. Check exclusive branch/leaf form, at most eight immediate children and global shallowest/deepest leaf-depth difference at most one, with root depth zero; use permitted single-child branches where helpful. If meaningful structure cannot satisfy the contract, return the conflict before applying it.
3. Select coherent splits/merges for distinct questions, navigation difficulty or node-configuration size. Assign continuing/new/retired identities under the local identity rule and record replacements.
4. Move/regroup content and update affected ancestor navigation, relative links in moved files and incoming links from other specification files. Check known external references and record those outside repair scope or unavailable for repair.
5. Regenerate the root catalogue from final node metadata. Verify every node once, parent UUIDs, root-relative configuration links and deterministic order through the helper, without copying summaries/status.
6. Pass [output:organization] as `task_result` and applicable [input:baseline] as `baseline` to [Verification and handoff](verify-and-handoff.md), with the verified explicit root as `specification_root`; receive actual verification before returning [output:organization] with evidence and limits.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:organization] | Restructured nodes, identity relationships and updated navigation | No meaning loss; node invariants, UUID continuity, incoming links and derived catalogue verified; unresolved external references reported. |

## References

- [Role rules and references](../SKILL.md) — shared invocation, contract, sources and type conventions.
- [Specification format](../concepts/specification.md) - structure, classification, type registry, and lifecycle - required before specification work.
- [Contract versioning](../conventions/contract-versioning_conv.md) and [package contract](../contract.json) - target version, baseline, transition ledger, adoption/migration gates and verification - required when specification work begins; not general startup.
- This package's `conventions/<type>_conv.md` files - leaf content formats - conditional for types created or changed; read only those types.
- [Workspace structure convention](../conventions/workspace-structure_conv.md#discovery-boundaries) - discovery exclusions and library boundaries - required before mapping workspace paths or reverse-engineering implementation.
- [Audit helper instructions](../scripts/README.md) - runtime, paths, usage, and limits - required on first audit use.
- [Audit fixture tests](../scripts/test_audit_specification.py) - helper verification - conditional when changing the helper itself.
- Caller-supplied workspace instructions, HAI validation context, and source lifecycle information — required as applicable to HAI-managed work, including validated enabled-feature/location assurance; standalone package invocation requires no HAI files, but HAI-managed work must not be reclassified as standalone to bypass missing or invalid context.
