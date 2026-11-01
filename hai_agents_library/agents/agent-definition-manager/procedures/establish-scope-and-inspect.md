# Establish scope and inspect

## Description

Establish the operation, authority, target identity, and prerequisites, and return verified inspection findings for subsequent definition work.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:operation] | Requested operation and scope of authority | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:workspace_root] | Explicit workspace root | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:target] | Canonical installed target, explicitly selected source package, or meaningful new-role purpose | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:instructions] | Applicable fixed mandatory and workspace/session instructions | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:activity_context] | Current Activity context for substantive HAI maintenance after bootstrap | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |

## Prerequisites

A requested operation, explicit workspace root, applicable instructions and authority; meaningful new-role purpose or an identified existing target as applicable.

## Rules

None.

## Steps

1. Resolve [input:operation], [input:workspace_root], [input:target], installed origin or source-package kind, and authority. Retrieve authorized missing context, then return unresolved necessary decisions while continuing independent diagnosis.
2. Load the shared agent convention and [input:instructions], including the safe fixed mandatory file. For workspace writes verify compatible initialized context; for substantive work verify [input:activity_context]. If required context is unavailable, report the affected dependency and keep only independent permitted diagnosis in scope.
3. Validate the installed canonical target or explicitly selected `hai_agents_library/agents/<name>/` source path and resolved containment. Read relevant catalogue entries and immediate folder names under both runtime origins; compare case-insensitive runtime identity and establish registration status. A source counterpart is not a runtime collision and is never executable or registered; record its installed counterpart separately. If the workspace catalogue is absent, record no workspace registrations; if an opposite-origin directory is absent, leave it absent. If catalogue/identity information is malformed or unreadable, report unknown registration status and continue only independent read-only work.
4. Load the selected definition, mandatory configuration contract and relevant resources. Inspect supported config versions/defaults, declared setting ownership, relevant external saved-file status and source/installed baselines without changing values. Compare catalogue guides first; inspect another definition only to resolve a concrete ownership question. Record baseline issues separately from the request.
5. Prepare [output:inspection] with target, operation/origin, authority, prerequisites, identity, registration status and dependencies. Identify its binding as target `inspection` for the caller-selected [create](create-definition.md), [update](update-definition.md), [validation/audit](validate-or-audit.md) or [registration](register-definition.md) continuation.
6. Return [output:inspection] and unresolved dependencies.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:inspection] | Operation, origin, target, identity, registration and prerequisite findings | Selected resources inspected; missing dependencies and pre-existing issues distinguished. |

## References

- [Role rules and references](../SKILL.md) — applicable ownership, safety, context and authoring rules.
- [Agent convention](../../../../.hai/conventions/agent_conv.md) — definition format, identity,
  selection, and ownership — required for all operations.
- [Agent concept](../../../../.hai/concepts/agent.md) — role boundaries — required when creating
  or changing responsibilities.
- [State convention](../../../../.hai/conventions/state_conv.md) — catalogue encoding and workspace
  prerequisites — required for catalogue writes and HAI context; independent format
  checks and prerequisite diagnosis remain available without initialized state.
- [Framework catalogue](../../../../.hai/agents/catalogue.md) and the workspace catalogue when present —
  registration and identity checks — required before mutations; conditional on audit scope.
- [Model profiles](../../../../.hai/conventions/model-profiles_conv.md) — model metadata and
  runtime evidence boundaries — conditional when choosing execution declarations.
- [Framework layout](../../../../.hai/conventions/framework-layout_conv.md) — canonical resource
  placement — required for creation or explicitly authorized relocation.
- [Agent tools](../../../../.hai/tools/agents/README.md) — validation commands and limits —
  required before first helper use.
- [Tooling convention](../../../../.hai/conventions/tooling_conv.md) — implementation and testing —
  conditional when creating, changing, or executing supporting helpers.
- Caller-supplied sources — target-role knowledge and authority — read only what
  the selected operation needs.
