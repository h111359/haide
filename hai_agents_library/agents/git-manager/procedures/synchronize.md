# Branches, synchronization, and conflicts

## Description

Manage authorized branches, synchronization, and conflicts or assess automated-push readiness, returning verified refs, checks, and unresolved prerequisites.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:operation_context] | Verified operation target, integration gates and authority | Mandatory | Operation workflow result | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:ref_request] | Requested refs, synchronization or readiness-assessment outcome | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:strategy] | Explicit merge strategy or established policy | Optional | Caller or authorized context | Use established request/repository policy; return unresolved strategy before dependent writes. |

## Prerequisites

Verified `operation_context` output from [Operation workflow](operate.md), supplied as [input:operation_context]. Requested refs/synchronization or explicit readiness assessment; resulting commits require [Commits and local changes](commit-and-export.md).

## Rules

- **Pre-existing operation:** Git-manager MUST NOT abort a merge, rebase or cherry-pick begun before this task without permission to abort it.
- **Unclear conflict:** Git-manager MUST NOT resolve a text conflict while its intended meaning is unclear.
- **Unresolved product choice:** Git-manager MUST return ambiguous product choices or unresolved synchronization strategy to the caller rather than guess a destructive fix.

## Steps

1. Establish [input:operation_context] and [input:ref_request]. Inspect branch/detached HEAD, local changes, existing operations and source/target refs; for requested branch/PR work prepare a noncolliding suitable branch and report its identity.
2. For pull/merge/rebase, verify upstream and inspect divergence with fresh available remote evidence. Select [input:strategy] or established request/repository policy; if unresolved, return the strategy dependency. Fetch is treated as fetch, without inferring push or shared-history-rewrite authority.
3. Resolve known-intent textual conflicts, preserve both sides' meaning and run affected checks. Before resulting commits, pass [input:operation_context] as `operation_context` and actual candidate as `commit_scope` to [Commits and local changes](commit-and-export.md); obtain its fresh recording result before any commit-producing effect.
4. For push, review destination, intended refs/commits, divergence, saved policy, authority, live authentication/write/branch prerequisites and triggered automation. Execute only the intended authorized update, then verify remote refs. If an unexpected remote update or unavailable gate appears, return the blocker/manual-push status instead of forcing through it.

### Automated-push enablement assessment

5. For an explicit enablement assessment with Git enabled, verify installed working Git and the actual transport tools (for example SSH or HTTPS credential helper). GitHub CLI is unnecessary when the selected Git transport is already installed/configured.
6. Verify actual repository, remote/destination, refs and branch/upstream/protection preconditions. Establish noninteractive authentication and receive/write capability using safe non-mutating evidence. Review hooks before any scoped noninteractive `git push --dry-run` with explicit refs; if safe verification is unavailable, report not ready rather than probing a real push.
7. Return fresh repository/transport/tooling/authentication/write/ref evidence and specific limits. Mark missing/failed/unverifiable prerequisites not ready, and pass actual assessment into [Configure integrations](configure-integrations.md) as `push_readiness` only under explicit setup authority. Assessment alone changes no saved setting; keeping push off needs no readiness probe.
8. Return [output:synchronization] with actual refs/state/conflicts/checks, readiness limits and manual-push or other dependencies.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:synchronization] | Verified refs, branch state, conflict/check results or fresh readiness assessment | Actual destination and result reported; unresolved strategy, conflicts, missing readiness or manual-push requirement explicit. |

## References

- [Role rules and references](../SKILL.md) — gates, authority, safety and applicable sources.
- [Agent convention](../../../../.hai/conventions/agent_conv.md) — receiver checks and host coordinator-only routing — required for all tasks.
- [State convention](../../../../.hai/conventions/state_conv.md) — generic core-state envelope and preservation requirements — required before extension configuration writes.
- [Startup helper](../../../../.hai/tools/startup/README.md) — core environment assurance only; it does not validate extension settings — conditional when interpreting core helper output.
- [Tooling convention](../../../../.hai/conventions/tooling_conv.md) — Python runtime and helpers — conditional when executing or changing supporting Python tools.
- Current installed tool help and official Git/GitHub documentation — command behavior and service limits — conditional when needed for the selected operation.
- [Git configuration contract](../conventions/git-configuration_conv.md) — independent switches, unavailable states and scoped preservation — required before configured operations or setup.
- [Extension helper](../scripts/README.md) — read-only saved-setting validation and limits — required before first local helper use.
