# Register or synchronize an agent

## Description

Register a validated installed definition or synchronize an existing catalogue row and return verified membership and metadata without executing the target.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace | Mandatory | Caller or authorized context | Retrieve before dependent writes. |
| [input:instructions] | Safe fixed instructions and applicable session/workspace instructions | Mandatory | Caller and fixed file | Empty readable content is valid; unavailable instructions block dependent writes. |
| [input:activity_context] | Stable current Activity ID/path and work context | Mandatory | Caller or authorized context | Retrieve before substantive registration work. |
| [input:authority] | Explicit registration request or authorized existing-definition/package update | Mandatory | Human request relayed through Leader or direct call | Inspect only; do not change a catalogue. |
| [input:target] | Canonical installed definition in either runtime origin | Mandatory | Caller, installation result or authoring result | Return missing identity/path; a source-only target needs installation first. |
| [input:validation_evidence] | Current definition/contract and semantic verification evidence | Optional | Trusted shared tools or authoring result | Run the trusted core definition validator directly and review relevant meaning; no Agent-definition-manager prerequisite. |
| [input:registration_intent] | Explicit new-registration choice | Optional | Human request, including combined install/register | Synchronize existing membership only; never add an unregistered agent. |

## Prerequisites

Compatible initialized context, fixed instructions, Activity, identified installed target and covering authority. New membership requires explicit registration intent. Synchronizing an existing row uses the authorized definition/package update scope without implying a new registration.

## Rules

- **New membership:** Environment-manager MUST have explicit registration intent before adding an unregistered target to either catalogue.
- **Catalogue creation:** Environment-manager MAY create a safely absent workspace catalogue with the standard header/table for explicitly authorized registration.
- **Framework dependency:** Environment-manager MUST report a missing or malformed framework catalogue rather than reconstruct it.
- **Accurate existing row:** Environment-manager MUST preserve an already accurate row without duplication.
- **Scoped metadata repair:** Environment-manager MUST have authority covering an existing conflicting/stale row before changing it.

## Steps

1. Establish inputs and inspect the installed canonical definition, both catalogues and immediate folder names. Confirm identity, origin, case-insensitive uniqueness, path containment and registration status. A source-library path is never registered or executed; return its separate installation dependency.
2. Validate the definition and package-local configuration contract with trusted shared tools; review supplied semantic evidence and reread changed inputs. Resolve missing dependencies without invoking the target or requiring an installed authoring agent. Missing valid-default override files do not block registration; saved-setting failures remain separate dependent-operation findings.
3. Derive the exact decoded description and canonical definition link from the verified installed file. Compare author-supplied metadata with that file; do not trust a stale handoff. If already accurate, return unchanged verified status. For a new row require [input:registration_intent]; for an existing metadata change retain membership and use the covering update authority. Malformed affected tables or unexplained identity conflicts stop writes.
4. Prepare the one row under the shared encoding contract, preserving unrelated rows/prose. For an absent workspace catalogue prepare its standard header/table. Recheck definition/catalogue bytes, instructions, authority and safe paths before an exclusive creation or guarded replacement. Do not rename, remove or unregister agents under a synchronization request.
5. Read back the catalogue and verify exact decoded description equality, canonical link, actual membership and unrelated-data preservation. Run the relevant audit/startup checks; distinguish their coverage from semantic and runtime proof. Stop/report partial results without automatic repair, rollback or retry.
6. Return [output:registration] with installed target, origin, actual membership, changed/unchanged row and verification. Target selection/execution remains Leader's separate work after eligibility is established.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:registration] | Verified target membership, canonical row and actual check results | Exact installed-description/link equality, preserved unrelated rows and actual registration status are verified, or precise partial results/dependencies are returned. |

## References

- [Role definition](../SKILL.md) — ownership, permission and preservation; required.
- [Agent convention](../../../conventions/agent_conv.md), [state convention](../../../conventions/state_conv.md) — identities, catalogues and encoding; required.
- [Agent tools](../../../tools/agents/README.md) — independent definition/contract validation; required before helper use.
- [Startup helper](../../../tools/startup/README.md) — independent core/registry context and limits; required before helper use.
