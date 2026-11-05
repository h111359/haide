# Update a definition

## Description

Apply scoped definition/resource changes and return verified metadata for any required runtime catalogue synchronization, without installing packages or changing membership.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:inspection] | Verified scope, identity and prerequisite findings | Mandatory | Result of Establish scope and inspect | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:change_request] | Requested changes and explicit migration/repair scope | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:target] | Canonical existing definition and affected resources | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |

## Prerequisites

Verified `inspection` output from [Establish scope and inspect](establish-scope-and-inspect.md), supplied as [input:inspection]. Existing canonical target and explicitly requested change/migration scope.

## Rules

- **Identity continuity:** Agent-definition-manager MUST preserve the target's name, origin and defined path unless the requested migration or rename explicitly changes them.

## Steps

1. Establish the baseline of [input:target], installed or source-package kind, registration status, affected resources/references and [input:change_request] against [input:inspection]. Identify any explicitly authorized identity migration. A source update changes only the selected golden package; a requested installed snapshot replacement returns through host coordinator to runtime. Direct authorized workspace-only definition edits remain authoring work, not a source-package installation.
2. Review the mandatory configuration contract, supported versions and defaults against the existing contract and relevant saved values. Report breaking changes and owner migration dependencies; preserve external settings and do not implicitly migrate them. Prepare the scoped changes. Review each statement's semantic destination: shared constraints in SKILL Rules, unique local constraints in procedure Rules, conditions in Prerequisites and ordered actions/branches in Steps. Correct misplaced behavior in supporting concepts/conventions within the requested scope; retain their domain meaning and data contracts.
3. Rewrite genuine rules in plain words with an explicit actor, action, object and applicable condition. Use only uppercase `MUST`, `MUST NOT` and `MAY` for their defined strengths, with one independent requirement per short bold title. Compare the before/after wording against the baseline for preserved defaults, preferences, permitted alternatives, conditions and exceptions; return unresolved meaning instead of silently changing strength. Do not treat a modal keyword as proof of clarity.
4. Derive the final canonical identity, exact decoded description and definition/contract check evidence. For a registered installed target, identify any existing row that needs synchronization; for a source target, record its separate installed counterpart without changing either registration or snapshot. An unregistered target stays unregistered. Return malformed/conflicting catalogue findings without repairing the table.
5. Recheck inspected definition/resource bytes, scope and containment, then apply only authorized authoring changes. Preserve catalogues and installed snapshots for source-only edits. Stop dependent writes and report partial results on changed inputs or failure.
6. Reread and validate the changed definition/resources under [Validate or audit](validate-or-audit.md), supplying the current `inspection` and canonical `target`. Return the metadata and covering update authority through host coordinator for runtime's existing-row synchronization or separately authorized installation. Treat required catalogue coherence as pending until that owner's actual verified result, without invoking it yourself.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:changes] | Definition/resource changes and validated catalogue/installer handoff | Definition/resource checks and exact metadata are reported; catalogues remain unchanged here and required owner synchronization/installation is explicitly pending. |

## References

- [Role rules and references](../SKILL.md) — applicable ownership, safety, context and authoring rules.
- [Agent convention](../../../../.hai/conventions/agent_conv.md) — definition format, identity,
  selection, and ownership — required for all operations.
- [Agent concept](../../../../.hai/concepts/agent.md) — role boundaries — required when creating
  or changing responsibilities.
- [State convention](../../../../.hai/conventions/state_conv.md) — catalogue encoding and workspace
  prerequisites — required for interpreting catalogue identity and HAI context; independent format
  checks and prerequisite diagnosis remain available without initialized state.
- [Workspace catalogue](../../catalogue.md) when present —
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
