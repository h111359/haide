# Verification and handoff

## Description

Verify completed specification work against structural and semantic requirements, and return changed paths, supporting evidence, limits, and unresolved decisions.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:task_result] | Affected paths, changes or read-only findings | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:specification_root] | Explicit inspected root and invocation context | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:baseline] | Saved identity inventory when restructuring comparison requires it | Optional | Caller or authorized context | Capture outside the tree only when required for identity comparison; otherwise leave absent. |
| [input:migration_plan] | Approved target obligations and preservation evidence for migration | Optional | Caller or authorized context | Ordinary compatible-tree verification needs none; migration/adoption blocks until an explicitly scoped human-approved plan exists. |

## Prerequisites

Verified root/invocation from [Locate and inspect](locate-and-inspect.md), actual [input:task_result], and applicable approved [input:migration_plan]/identity [input:baseline].

## Rules

- **Renderer evidence:** Specification-manager MUST treat `--render-catalogue` output as a read-only candidate rather than adoption approval or compatibility validation.

## Steps

1. Read [audit helper instructions](../scripts/README.md) on first use and choose a working documented interpreter. Invoke the installed package script with explicit [input:specification_root]; for HAI-managed work supply the validated workspace with `--workspace` and configured workspace-relative `--root` to retain containment. Standalone absolute/current-relative roots use the documented standalone mode.
2. Run the read-only helper after final edits and before handoff. Review metadata/IDs/topology/global balance/configuration sizes/Children coverage/content names/simple links/compatibility/derived catalogue. Use `--inventory` for structure, `--baseline <saved-inventory.json>` for required identity comparison and the renderer for a catalogue candidate.
3. Resolve or report every error and review warnings. Inspect changed leaf content against type/classification/sources, approvals, meaning, canonical facts, navigation, external references, unsupported syntax and identity-change interpretation; avoid duplicating the helper's supported checks by reading every unchanged file.
4. For migration, compare complete target obligations and preservation evidence under [input:migration_plan]; verify the final tree. If marker finalization or retry decisions remain unresolved, return that dependency to [Adopt or migrate specification](adopt-or-migrate.md) rather than reporting applied status. On failure, report actual marker/files and failed/unrun checks, returning for plan-applicability reassessment before retry.
5. If the helper itself changed, run [fixture tests](../scripts/test_audit_specification.py); ordinary specification edits do not require those helper tests.
6. Return [output:handoff] with changed paths, content/organization changes, mechanical/manual evidence, limits, pre-existing issues and unresolved decisions. Report migration applied only after actual final success.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:handoff] | Changed paths, content/organization results, verification evidence and unresolved decisions | Final helper and semantic checks reported with limits and pre-existing issues; migration applied claimed only after successful target verification. |

## References

- [Role rules and references](../SKILL.md) — shared invocation, contract, sources and type conventions.
- [Specification format](../concepts/specification.md) - structure, classification, type registry, and lifecycle - required before specification work.
- [Contract versioning](../conventions/contract-versioning_conv.md) and [package contract](../contract.json) - target version, baseline, transition ledger, adoption/migration gates and verification - required when specification work begins; not general startup.
- This package's `conventions/<type>_conv.md` files - leaf content formats - conditional for types created or changed; read only those types.
- [Workspace structure convention](../conventions/workspace-structure_conv.md#discovery-boundaries) - discovery exclusions and library boundaries - required before mapping workspace paths or reverse-engineering implementation.
- [Audit helper instructions](../scripts/README.md) - runtime, paths, usage, and limits - required on first audit use.
- [Audit fixture tests](../scripts/test_audit_specification.py) - helper verification - conditional when changing the helper itself.
- Caller-supplied workspace instructions, HAI validation context, and source lifecycle information — required as applicable to HAI-managed work, including validated enabled-feature/location assurance; standalone package invocation requires no HAI files, but HAI-managed work must not be reclassified as standalone to bypass missing or invalid context.
