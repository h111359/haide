# Operation workflow

## Description

Establish repository identity, configured capabilities, authority, and pre-mutation state, then perform scoped operations and return verified local or remote outcomes.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit workspace and verified repository | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:outcome] | Requested outcome, scope and authority | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:instructions] | Applicable instructions and shared handoff context | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:integration_context] | Locally validated saved Git/GitHub/auto-push settings and their inspected source | Optional | Extension helper or previously verified unchanged local result | Run this extension's read-only validator before dependent repository work; never infer settings from core startup. |
| [input:operation_options] | Repository, remote, branch, commit paths/message, PR/issue or merge details | Optional | Caller or authorized context | Preserve the current branch; discover remote/default branch; create branches or PRs only when explicitly requested. |

## Prerequisites

Explicit workspace, requested outcome/authority, applicable instructions and handoff context. Repository work additionally requires usable core assurance and valid relevant local extension settings; diagnosis/configuration requests retain their bounded exceptions.

## Rules

None.

## Steps

1. Establish [input:workspace_root], [input:outcome], [input:instructions] and supplied [input:operation_options]. Retrieve authorized missing context and return unresolved dependencies while continuing independent permitted diagnosis.
2. For configuration-only work, pass the explicit workspace/instructions, established setup authority, handoff Activity context and chosen switches to [Configure integrations](configure-integrations.md) as `workspace_root`, `instructions`, `authority`, `activity_context` and `integration_choices`; receive actual status before dependent repository work.
3. For repository work, obtain the local read-only saved-setting result when [input:integration_context] is absent/stale, and separately verify core assurance. Compare the intended operation with independent integration/push gates. If a required gate is unavailable, return the precise setup/manual-push dependency without performing that blocked operation.
4. Inspect the relevant repository/remote state: identity, branch/HEAD, requested worktree/index changes, destination/access, existing operation state and relevant automation. Discover rather than assume remotes/default branches; read installed help or official documentation when command behavior is uncertain.
5. Choose the smallest authorized sequence and prepare any unresolved destructive/publication effects for concrete review. Finalize [output:operation_context] after verified preflight.
6. Pass [output:operation_context] as `operation_context` to the selected [commit/export](commit-and-export.md), [synchronization](synchronize.md), [collaboration](collaborate.md), [release/recovery](release-and-recover.md) or [targeted discovery](inspect-discovery.md) procedure, along with actual scoped task values under that target's declared input names. Apply its operation-specific gates and recheck candidate facts before writes.
7. Verify actual local/remote outcomes and observe required checks. Request further owner evidence through Leader if needed, then return [output:result] with identifiers, paths/resources, URLs, checks, preserved work, publication status and dependencies. For release work include source/asset evidence for the product owner's final review.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:operation_context] | Verified repository identity, requested effects, integration gates, authority and pre-mutation state | Preflight steps 1–3 complete before dependent specialized work. |
| [output:result] | Verified before/after repository or remote results | Object/ref IDs, paths, URLs, checks, preserved work, publication status and dependencies reported; no unsupported completion claim. |

## References

- [Role rules and references](../SKILL.md) — gates, authority, safety and applicable sources.
- [Agent convention](../../../../.hai/conventions/agent_conv.md) — receiver checks and leader-only routing — required for all tasks.
- [State convention](../../../../.hai/conventions/state_conv.md) — generic core-state envelope and preservation requirements — required before extension configuration writes.
- [Startup helper](../../../../.hai/tools/startup/README.md) — core environment assurance only; it does not validate extension settings — conditional when interpreting core helper output.
- [Tooling convention](../../../../.hai/conventions/tooling_conv.md) — Python runtime and helpers — conditional when executing or changing supporting Python tools.
- Current installed tool help and official Git/GitHub documentation — command behavior and service limits — conditional when needed for the selected operation.
- [Git configuration contract](../conventions/git-configuration_conv.md) — independent switches, unavailable states and scoped preservation — required before configured operations or setup.
- [Extension helper](../scripts/README.md) — read-only saved-setting validation and limits — required before first local helper use.
