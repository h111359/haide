# Configure integrations

## Description

Validate this optional extension's saved switches and apply explicitly requested configuration or scoped repair, returning verified settings and readiness limits.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root | Mandatory | Caller | Retrieve authorized context; pause dependent setup if unresolved. |
| [input:instructions] | Applicable fixed mandatory and workspace/session instructions | Mandatory | Caller and safe readable instruction file | Empty fixed instructions are valid; missing/unreadable instructions block dependent work. |
| [input:authority] | Requested validation, chosen settings or explicitly scoped repair | Mandatory | Human request relayed through Leader or direct call | Read-only prerequisite diagnosis remains available; do not infer mutation authority. |
| [input:activity_context] | Current Activity ID/path and task context, or valid bounded diagnosis exception | Mandatory | Leader or applicable direct context | Retrieve before substantive setup; report unresolved dependency. |
| [input:integration_choices] | Explicit Git/GitHub/auto-push Boolean choices | Optional | Human's established choices | Validate only and preserve every saved value. |
| [input:push_readiness] | Fresh actual repository/remote tooling, noninteractive authentication, write access and non-force target readiness evidence | Optional | This role's scoped readiness assessment | Required before enabling auto-push; refuse enablement if missing, stale or failed. |
| [input:legacy_migration] | Explicit authority to extract legacy Git-owned state into the owner file, with reviewed dry-run and any destination resolution | Optional | Human request relayed through Leader or direct call | No legacy settings read as active values, extracted or removed. |

## Prerequisites

Applicable instructions and task/Activity context; writes additionally require independent usable core assurance and explicit chosen Boolean/repair scope. Effective auto-push enablement requires enabled Git and complete fresh actual-destination readiness.

## Rules

- **Effective enablement:** Git-manager MUST require permission to enable auto-push and fresh push checks when a change makes a saved true push switch effective, including re-enabling Git.
- **Unchosen switch:** Git-manager MUST NOT silently reset an unchosen switch to create a staging path.
- **No off-state probe:** Git-manager MAY validate settings, preserve push-off or turn push off within the chosen scope without a network readiness probe.
- **Stale true value:** Git-manager MUST NOT treat an old saved true value as proof of current push readiness or permission to rewrite an unchosen setting.

## Steps

1. Establish [input:workspace_root], [input:instructions], [input:authority] and [input:activity_context]. Load the adjacent configuration contract and run the local validator for independent saved statuses in `.hai_env/config/agents/git-manager.json`; capture complete duplicate-free owner-file data and bytes when present. Separately establish core assurance. If the core envelope is uninitialized/invalid, return the core dependency through Leader before writes and retain independent read-only diagnosis. Never obtain active settings from legacy state.
2. When [input:legacy_migration] is present, run the migration helper's read-only dry-run against the complete strict legacy state. Review preserved owned subtrees, unrelated state and destination conflicts. Resolve any existing destination explicitly; only a complete identical envelope is accepted by the helper. Under verified migration authority and fresh core assurance, apply using the inspected source hash. Require verified backups, unchanged inputs and old/new readback before old-key removal; preserve/report partial writes and stop on failure without retry. Run local configuration and independent core checks afterward, verify preserved values including unknown nested data and state version, and return actual migration stages. Preserving existing choices does not itself enable auto-push or require readiness probes. If both new and legacy settings remain after interruption, report partial migration for reviewed resolution.
3. If [input:integration_choices] is absent, return read-only [output:integration_result] or the verified migration result. Otherwise prepare only chosen owned `enabled` Booleans under `settings.git` and `settings.github`, adding absent containers/entries and the contract-version envelope as needed. For malformed affected data without scoped repair authority, return the repair dependency before replacement; report unrelated isolated issues separately.
4. Determine whether the candidate newly enables effective auto-push. If so, verify authority and fresh complete [input:push_readiness], or obtain an assessment from [Branches, synchronization, and conflicts](synchronize.md#automated-push-enablement-assessment). Supply verified preflight from [Operation workflow](operate.md) as target `operation_context` and the explicit assessment request as `ref_request`; receive actual readiness as `push_readiness` for this configuration operation.
5. If Git was off, execute/verify an explicitly chosen safe Git-enablement stage before assessment only when it does not reactivate retained true push without its gate. If a safe staging choice or readiness is missing/stale/failed, refuse auto-push enablement and return the precise dependency. Preserve false, or set false only under the chosen configuration/repair scope; report staged results without implying atomicity.
6. Validate prepared settings under the owner contract; recheck independent core assurance and original owner-file bytes/absence, containment and source facts immediately before guarded write. Stop on changed/conflicting input. Apply only authorized candidate changes, using exclusive creation for an absent destination, and preserve all owner-file unknown values and every unrelated resource.
7. Read back; run local configuration validation and independent bounded core validation. Compare instructions, unchanged core state/version, chosen/unchanged switches and unknown/unrelated values with the inspected source. On partial failure return actual writes/checks without retry.
8. Return [output:integration_result] with actual statuses, readiness source/freshness, core/helper results, stages/partial writes and blockers. Any later actual push proceeds under inherited fresh live-precondition and authority rules.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:integration_result] | Saved extension statuses, chosen changes, readiness evidence and limits | Readback/local helper verify authorized changes and preserved data; core checks remain independent; no secrets, smoke push, implied publication or unobserved readiness claimed. |

## References

- [Role definition](../SKILL.md) — ownership, authority and gates; required.
- [Git configuration contract](../conventions/git-configuration_conv.md) — saved schema, independent failures and preservation; required.
- [Extension helper](../scripts/README.md) — safe read-only configuration validation; required before first use.
- [Core state convention](../../../../.hai/conventions/state_conv.md) — envelope and mandatory instructions; required before writes.
- [Agent configuration convention](../../../../.hai/conventions/agent-configuration_conv.md) — owner-file envelope, defaults and isolated validation; required.
