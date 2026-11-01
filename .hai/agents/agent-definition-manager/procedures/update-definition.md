# Update a definition

## Description

Apply scoped definition and resource changes, synchronize any affected existing catalogue entry, and report verification results or remaining inconsistencies.

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

1. Establish the baseline of [input:target], registration status, affected resources/references and [input:change_request] against [input:inspection]. Identify any explicitly authorized identity migration.
2. Prepare the scoped changes. Review each statement's semantic destination: shared constraints in SKILL Rules, unique local constraints in procedure Rules, conditions in Prerequisites and ordered actions/branches in Steps. Correct misplaced behavior in supporting concepts/conventions within the requested scope; retain their domain meaning and data contracts.
3. Rewrite genuine rules in plain words with an explicit actor, action, object and applicable condition. Use only uppercase `MUST`, `MUST NOT` and `MAY` for their defined strengths, with one independent requirement per short bold title. Compare the before/after wording against the baseline for preserved defaults, preferences, permitted alternatives, conditions and exceptions; return unresolved meaning instead of silently changing strength. Do not treat a modal keyword as proof of clarity.
4. Prepare the existing catalogue row from the final decoded description and canonical reference when the target is registered. If an affected catalogue is malformed, return that dependency before coordinated writes. For an unregistered target, prepare no registration unless separately requested.
5. Recheck inspected bytes and containment, then apply the scoped definition/resource changes and existing-row synchronization. For an authorized identity migration, coordinate affected references and identity checks; on any changed input or partial result, stop dependent writes and report actual state.
6. Reread the definition, affected resources and existing row. Run [Validate or audit](validate-or-audit.md), passing [input:inspection] as `inspection` and the changed canonical [input:target] as `target`. Verify decoded description equality, canonical links, semantic separation and unrelated-content preservation. Return [output:changes], decisions and any remaining inconsistency.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:changes] | Definition/resource changes and existing-row synchronization | Exact description equality and links verified; completed writes, decisions and any inconsistency reported. |

## References

- [Role rules and references](../SKILL.md) — applicable ownership, safety, context and authoring rules.
- [Agent convention](../../../conventions/agent_conv.md) — definition format, identity,
  selection, and ownership — required for all operations.
- [Agent concept](../../../concepts/agent.md) — role boundaries — required when creating
  or changing responsibilities.
- [State convention](../../../conventions/state_conv.md) — catalogue encoding and workspace
  prerequisites — required for catalogue writes and HAI context; independent format
  checks and prerequisite diagnosis remain available without initialized state.
- [Framework catalogue](../../catalogue.md) and the workspace catalogue when present —
  registration and identity checks — required before mutations; conditional on audit scope.
- [Model profiles](../../../conventions/model-profiles_conv.md) — model metadata and
  runtime evidence boundaries — conditional when choosing execution declarations.
- [Framework layout](../../../conventions/framework-layout_conv.md) — canonical resource
  placement — required for creation or explicitly authorized relocation.
- [Agent tools](../../../tools/agents/README.md) — validation commands and limits —
  required before first helper use.
- [Tooling convention](../../../conventions/tooling_conv.md) — implementation and testing —
  conditional when creating, changing, or executing supporting helpers.
- Caller-supplied sources — target-role knowledge and authority — read only what
  the selected operation needs.
