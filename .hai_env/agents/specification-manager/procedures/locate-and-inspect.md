# Locate and inspect the specification

## Description

Inspect the supplied specification root, compatibility, and affected nodes, and return the authorized work scope and prerequisite findings without implicit creation or migration.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:task] | Requested task and scope of authority | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:specification_root] | Explicit standalone root or optional HAI root matching owner configuration | Optional | Caller or validated owner configuration | Standalone work requires an explicit root; HAI work derives the root only from validated owner settings. |
| [input:instructions] | Applicable workspace/session instructions | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:hai_context] | Compatible core, instructions and Activity context for HAI-managed work, with any owner-settings evidence | Optional | Caller or authorized context | Standalone work needs none; HAI-managed work blocks until independent core/Activity and local owner-settings checks succeed. |
| [input:sources] | Meaningful sources for content entry or tree creation | Optional | Caller or authorized context | Read-only assessment needs no new sources; content entry or tree creation blocks without meaningful sources. |

## Prerequisites

Explicit task and applicable instructions; an explicit specification root for standalone work, or valid core/Activity context and locally validated enabled owner settings for HAI-managed work. Meaningful sources are required before creation/content writes.

## Rules

None.

## Steps

1. Establish the supplied task/invocation and instructions. In standalone use require an explicit absolute or current-directory-relative root without loading HAI files. In HAI-managed use independently verify core/Activity assurance and run this installed package's settings helper against the supplied workspace. Require usable format-3 context, valid enabled owner settings and a safe configured directory. Resolve the specification root from that location; reject a supplied differing root and stale caller settings. Disabled/invalid settings return the precise dependency before tree loading; route explicit settings work to [Configure specification settings](configure-specification.md), passing the workspace, instructions, authority and Activity as its corresponding inputs. Never use legacy state as settings or relabel HAI work as standalone.
2. Read the [specification format](../concepts/specification.md), [contract convention](../conventions/contract-versioning_conv.md), [package contract](../contract.json) and relevant leaf-type conventions not already in context. Verify the supplied path, ancestor/descendant link boundary and any explicit workspace containment.
3. For an existing tree, inspect root `__ncf__.md` and run the read-only audit. Classify the marker as current, unmarked, older, newer or invalid under the contract; record source evidence and pre-existing issues. Add `--inventory` for paths/IDs/types/depths rather than manually loading every node configuration.
4. If the tree is not current, prepare the read-only assessment. When scoped adoption/migration is requested, pass it as `inspection`, the explicit [input:specification_root] as `specification_root` and the established task authority as `migration_authority` to [Adopt or migrate specification](adopt-or-migrate.md) and receive its actual verified result before dependent ordinary edits. Otherwise return the read-only assessment with adoption/migration pending.
5. If a new tree is explicitly authorized and meaningful content is supplied, create it directly at the valid current target, then verify the complete tree under [Verification and handoff](verify-and-handoff.md), passing [input:specification_root] as `specification_root` and the actual creation result as `task_result`. If creation/content authority or sources are absent, report the dependency rather than creating a tree for inspection.
6. For a compatible existing tree, use the root catalogue when structural overview helps, navigate descriptions to affected nodes, and inspect only needed content/linked context and type conventions. Separate requested changes from unrelated existing issues.
7. Prepare [output:inspection] and the continuation bindings for the caller: its target name is `inspection` to [content entry](enter-and-update.md), [workspace discovery](discover-workspace.md) or [organization](organize.md) as applicable. For [Verification and handoff](verify-and-handoff.md), supply [input:specification_root] as `specification_root` and actual findings as `task_result`.
8. Return [output:inspection] with pre-existing issues and unresolved dependencies.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:inspection] | Resolved root, invocation/core and owner-settings provenance, compatibility, authorized scope and affected-node assessment | Missing/conflicting prerequisites and pre-existing issues reported; no implicit creation, adoption or migration. |

## References

- [Role rules and references](../SKILL.md) — shared invocation, contract, sources and type conventions.
- [Specification format](../concepts/specification.md) - structure, classification, type registry, and lifecycle - required before specification work.
- [Contract versioning](../conventions/contract-versioning_conv.md) and [package contract](../contract.json) - target version, baseline, transition ledger, adoption/migration gates and verification - required when specification work begins; not general startup.
- This package's `conventions/<type>_conv.md` files - leaf content formats - conditional for types created or changed; read only those types.
- [Workspace structure convention](../conventions/workspace-structure_conv.md#discovery-boundaries) - discovery exclusions and library boundaries - required before mapping workspace paths or reverse-engineering implementation.
- [Audit helper instructions](../scripts/README.md) - runtime, paths, usage, and limits - required on first audit use.
- [Audit fixture tests](../scripts/test_audit_specification.py) - helper verification - conditional when changing the helper itself.
- Caller-supplied workspace instructions, HAI validation context, and source lifecycle information — required as applicable to HAI-managed work, including separate core/Activity and locally validated owner enablement/location assurance; standalone package invocation requires no HAI files, but HAI-managed work must not be reclassified as standalone to bypass missing or invalid context.
