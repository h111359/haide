# Adopt or migrate specification

## Description

Assess and execute an explicitly scoped specification adoption, compatibility migration or marker repair, returning verified applied status or a preserved decision dependency.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:inspection] | Read-only root/compatibility/source assessment | Mandatory | Locate and inspect the specification `inspection` output | Complete the prerequisite with authorized context. |
| [input:specification_root] | Explicit inspected specification root and invocation/workspace boundary | Mandatory | Caller and inspected context | Return the missing root/boundary dependency. |
| [input:migration_authority] | Requested adoption/migration/marker-repair scope | Mandatory | Human task, direct or relayed by caller | Keep assessment read-only; infer no migration authority. |
| [input:migration_plan] | Scoped plan under the contract convention's plan schema | Optional | Caller or assessment prepared here | Prepare the plan for human decision; no migration writes yet. |
| [input:human_approval] | Explicit human approval with scope/evidence, directly supplied or relayed | Optional | Human or attributable caller relay | Return plan/decision dependency before any migration write, including marker-only work. |

## Prerequisites

Verified `inspection` output from [Locate and inspect the specification](locate-and-inspect.md) supplied as [input:inspection], explicit root and requested compatibility-operation scope. Migration writes additionally require a complete applicable [input:migration_plan] and explicit [input:human_approval].

## Rules

- **Retry assessment:** Specification-manager MUST reassess the actual partial tree before retrying a migration operation.
- **Changed migration:** Specification-manager MUST obtain renewed human approval when the work, source evidence or planned changes differ on a retry.
- **Existing approval:** Specification-manager MUST identify the existing approval it reuses when that approval still covers the unchanged work.

## Steps

1. Compare [input:inspection] and [input:specification_root] with the valid package target and immutable transition ledger.
2. Branch on source state: for unmarked sources assess every target obligation; for older sources identify the exact version and complete ordered transition path; for newer sources obtain a supporting package or explicitly designed conversion; for invalid sources diagnose actual malformed contract/marker data. If required knowledge/valid target is missing, return a blocker with read-only assessment.
3. Prepare or verify [input:migration_plan] against the convention's plan schema, including source evidence/version, target, transition IDs, exact affected rules/files/transformations, preservation/unknowns, catalogue/links, checks and recovery boundaries. For unmarked or marker-only adoption, record which full target obligations hold and which need change.
4. Supply the plan and attributable [input:human_approval] provenance to the caller for its owning record role, or retain them in supplied context outside product facts; this procedure performs no Activity-record writes. If approval or scope is unresolved, return the decision dependency before migration writes; standalone invocation creates no HAI-record requirement.
5. After approval, recheck paths, source contents, authority and plan applicability. If changed/conflicting, return for assessment/decision before dependent writes.
6. Apply agreed transformations, preserving UUIDs, product meaning, sources, approval history and unknowns. Refresh derived catalogue/links for inventory changes; use the read-only renderer for an adoption candidate even without a current marker when useful.
7. Verify all target requirements, including manual content/behavior checks, against saved identity/content/approval evidence. If required, test the target marker on a staged candidate before asserting live compliance.
8. After agreed transformations and required checks succeed, write the live target marker and rerun final audit/manual checks.
9. On any write/check failure, stop dependent writes and report actual completed files, marker state, failed/unrun checks and remaining work. Before retry, reassess the actual partial state and approval applicability under the local rule.
10. On final success, pass actual changes/check evidence as `task_result`, [input:specification_root] as `specification_root` and the applicable plan as `migration_plan` to [Verification and handoff](verify-and-handoff.md); receive the verified handoff result.
11. Return [output:migration_result] as applied only after final success; otherwise return pending/partial status with exact dependencies.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:migration_result] | Assessment/plan/approval dependency or verified applied adoption/migration/repair | Source/target, applicable approval, transformed files, marker, preservation and final checks reported; no marker-only or partial-success completion claim. |

## References

- [Role definition](../SKILL.md) — inherited authority, preservation, context and failure rules; required.
- [Specification contract convention](../conventions/contract-versioning_conv.md) — package/marker/plan schema and immutable transition ledger; required.
- [Specification format](../concepts/specification.md) and [package contract](../contract.json) — complete target obligations; required.
- [Audit helper instructions](../scripts/README.md) — read-only checks/renderer and their limits; required before first helper use.
