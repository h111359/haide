# GitHub collaboration and checks

## Description

Perform authorized GitHub collaboration and check operations, and return verified resource identities, URLs, states, and check results.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:operation_context] | Verified outcome, target, integration context and authority | Mandatory | Operation workflow result | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:resource_request] | Requested PR, issue, check/workflow action and content | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:remote_refs] | Existing verified remote head/base refs when required | Optional | Caller or authorized context | Retrieve required existing remote refs; report missing refs without bypassing push policy. |

## Prerequisites

Verified `operation_context` output from [Operation workflow](operate.md), supplied as [input:operation_context]. Requested GitHub resource/action and required existing remote refs; commit-producing merges additionally need the commit procedure recording gate.

## Rules

- **Inspection permission:** Git-manager MUST NOT treat inspection alone as permission to merge a PR, publish a review/comment or close an issue.
- **Workflow evidence:** Git-manager MUST NOT report a started or rerun workflow as a passing check without its observed result.

## Steps

1. Compare [input:operation_context], [input:resource_request] and required [input:remote_refs]. Verify authenticated account, target repository and sufficient access without exposing credentials; select a sufficient connector or installed CLI/API path. If the CLI invokes local Git, verify the Git gate as well; otherwise use an explicit service API path within the independent gate.
2. Inspect existing resources before creation/retry to avoid duplicates. For a PR review base/head, diff, desired state, title/body and required checks; for an issue review scope, exact content, labels and intended state. If a required remote ref is absent, report it under the inherited push policy rather than recreating it through a workaround.
3. Execute only the authorized resource/workflow effects. Before any merge producing a commit, pass [input:operation_context] as `operation_context` and the actual merge candidate as `commit_scope` to [Commits and local changes](commit-and-export.md) for its fresh recording gate; if the tool cannot pause to honor it, return that limitation.
4. Observe resulting resource state/checks, request missing evidence through host coordinator, and return [output:collaboration] with URLs, actual effects and pending/running/unavailable checks or dependencies.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:collaboration] | Verified GitHub resources, URLs, state and checks | Requested effects observed; pending/running/unavailable checks and access or ref dependencies reported. |

## References

- [Role rules and references](../SKILL.md) — gates, authority, safety and applicable sources.
- [Agent convention](../../../../.hai/conventions/agent_conv.md) — receiver checks and host coordinator-only routing — required for all tasks.
- [State convention](../../../../.hai/conventions/state_conv.md) — generic core-state envelope and preservation requirements — required before extension configuration writes.
- [Startup helper](../../../../.hai/tools/startup/README.md) — core environment assurance only; it does not validate extension settings — conditional when interpreting core helper output.
- [Tooling convention](../../../../.hai/conventions/tooling_conv.md) — Python runtime and helpers — conditional when executing or changing supporting Python tools.
- Current installed tool help and official Git/GitHub documentation — command behavior and service limits — conditional when needed for the selected operation.
- [Git configuration contract](../conventions/git-configuration_conv.md) — independent switches, unavailable states and scoped preservation — required before configured operations or setup.
- [Extension helper](../scripts/README.md) — read-only saved-setting validation and limits — required before first local helper use.
