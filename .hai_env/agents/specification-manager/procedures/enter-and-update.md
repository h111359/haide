# Enter and update information

## Description

Enter or update authorized durable product knowledge while preserving meaning, identity, and source lifecycle, and return verified content and navigation changes.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:inspection] | Root and compatibility assessment | Mandatory | Locate and inspect the specification result | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:sources] | Meaningful human input, agreed decisions or verified product evidence | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:change_scope] | Authorized content scope and established decisions | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:source_lifecycle] | Activity or temporary-source lifecycle context when promoting information | Optional | Caller or authorized context | No temporary-source promotion is inferred; obtain lifecycle context when promotion requires it. |

## Prerequisites

Verified `inspection` output from [Locate and inspect the specification](locate-and-inspect.md), supplied as [input:inspection]. Meaningful authorized sources and settled decisions for the affected content.

## Rules

None.

## Steps

1. Identify durable meaning, audience and scope from [input:sources], [input:change_scope] and [input:inspection]. Separate product knowledge from temporary plans/logs/conversations, using supplied [input:source_lifecycle] for any promotion.
2. Classify items against registered leaf scopes and the affected type conventions. Select an applicable specialized type; for unresolved classification, return a caller decision. Separate different questions and connect related canonical leaves with descriptive links.
3. Update the fitting canonical leaf, or create a meaningful new leaf with its convention's filename/format and separate `__ncf__.md`/single content file. Record unknowns and preserved stable identifiers/source relationships.
4. Set a new leaf to `draft` unless approval is established. If substantive revision invalidates an existing approval, mark the affected leaf `draft` and report that change; otherwise preserve established approval history/status.
5. Refresh affected node descriptions and parent Children tables. When inventory fields change, obtain the read-only root-catalogue rendering and save the authorized derived update.
6. Pass [output:content_changes] as `task_result` to [Verification and handoff](verify-and-handoff.md), with the verified explicit root as `specification_root`; receive actual verification before returning [output:content_changes] with evidence and limits.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:content_changes] | Canonical content, status and navigation changes | Meaning/IDs preserved; sources, classification, approval and unknowns handled; affected descriptions and derived catalogue refreshed. |

## References

- [Role rules and references](../SKILL.md) — shared invocation, contract, sources and type conventions.
- [Specification format](../concepts/specification.md) - structure, classification, type registry, and lifecycle - required before specification work.
- [Contract versioning](../conventions/contract-versioning_conv.md) and [package contract](../contract.json) - target version, baseline, transition ledger, adoption/migration gates and verification - required when specification work begins; not general startup.
- This package's `conventions/<type>_conv.md` files - leaf content formats - conditional for types created or changed; read only those types.
- [Workspace structure convention](../conventions/workspace-structure_conv.md#discovery-boundaries) - discovery exclusions and library boundaries - required before mapping workspace paths or reverse-engineering implementation.
- [Audit helper instructions](../scripts/README.md) - runtime, paths, usage, and limits - required on first audit use.
- [Audit fixture tests](../scripts/test_audit_specification.py) - helper verification - conditional when changing the helper itself.
- Caller-supplied workspace instructions, HAI validation context, and source lifecycle information — required as applicable to HAI-managed work, including validated enabled-feature/location assurance; standalone package invocation requires no HAI files, but HAI-managed work must not be reclassified as standalone to bypass missing or invalid context.
