# Register a validated definition

## Description

Register a validated agent definition in its canonical catalogue and return the verified row and actual registration status.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:registration_authority] | Explicit registration intent | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:target] | Existing canonical definition | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:validation_evidence] | Successful definition and resource validation | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:inspection] | Identity, catalogue and prerequisite findings | Mandatory | Result of Establish scope and inspect | Retrieve from authorized context; return the specific dependency and pause dependent work. |

## Prerequisites

Verified `inspection` output from [Establish scope and inspect](establish-scope-and-inspect.md), supplied as [input:inspection]. Explicit registration authority, validated existing definition/resources and valid destination catalogue/context.

## Rules

- **Workspace catalogue creation:** Agent-definition-manager MAY create a safely absent workspace catalogue with the standard header/table for authorized registration.
- **Framework catalogue dependency:** Agent-definition-manager MUST report a missing or malformed framework catalogue as a dependency rather than reconstruct it.
- **Accurate existing row:** Agent-definition-manager MUST leave an already accurate registration row unduplicated.
- **Stale catalogue row:** Agent-definition-manager MUST NOT repair a conflicting or stale existing row without permission for that repair or update.

## Steps

1. Verify [input:registration_authority], [input:validation_evidence], canonical installed [input:target] and current [input:inspection] against origin, collisions, catalogue structure and workspace prerequisites. A library source path cannot be registered; explicitly authorized installation must first produce the canonical workspace copy. If required evidence is missing, return the dependency before writes.
2. Confirm configuration-contract validation evidence, including declared defaults or explicit no-settings behavior. Missing valid-default override files do not prevent registration; saved-setting failures remain separate dependent-operation findings. Inspect existing registration. If accurate, return verified existing status. If conflicting/stale without repair/update authority, report the issue and stop dependent row changes.
3. Prepare the single intended row using the exact decoded description, shared table encoding and canonical link. For a safely missing workspace catalogue prepare its standard header/table; for missing/malformed framework data report the dependency.
4. Recheck definition/catalogue bytes, identity/path facts and context. Create a missing workspace catalogue exclusively; otherwise validate the prepared content and replace only the unchanged inspected catalogue, using a temporary sibling where supported. Stop dependent writes on concurrent changes or partial failure.
5. Verify resulting row, exact decoded description equality, canonical target and preserved unrelated resources/state/profiles. Return [output:registration] with actual status and definition validation; report partial results and inconsistencies rather than claiming unverified registration.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:registration] | Verified row and actual registration status | Canonical target and exact decoded description equality verified; unrelated material preserved and partial results reported. |

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
