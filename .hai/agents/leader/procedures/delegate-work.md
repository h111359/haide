# Delegate work

## Description

Select an eligible specialist, prepare an authorized assignment with explicit context and execution settings, and monitor returned results and dependencies.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:task] | Human question or task. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:activity_context] | Stable current Activity ID, path and relevant record context for substantive work; applicable bootstrap/diagnosis exception when no record is needed. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:selected_role] | Requested role or previously selected registered role and definition. | Optional | Caller, task and valid catalogue guides | Select the appropriate registered role from the guides; unresolved eligibility blocks delegation. |
| [input:runtime_evidence] | Local profile mapping plus current runtime support for exact model/effort; or explicit supported human override. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:catalogues] | Framework catalogue and validated independent workspace entries. | Mandatory | Startup context and safe canonical catalogues | Retrieve available authorized catalogues; unresolved registration/structure blocks affected selection only. |

## Prerequisites

Usable Activity context for substantive work, or the startup/setup or read-only diagnosis exception described in the shared conventions. Current catalogues and runtime evidence are required for the selected invocation.

## Rules

None.

## Steps

1. Establish [input:workspace_root], load [input:instructions], and resolve [input:task], [input:authority] and [input:activity_context].

2. Classify the requested operation before choosing its execution owner. Route role responsibility/procedure/placement proposals or corrections to an installed registered agent-definition-manager for design review; if unavailable, return that optional authoring dependency and offer explicitly selected installation through core Environment-manager. Route package acquisition/installation, registration and catalogue synchronization directly to Environment-manager, without an Agent-definition-manager prerequisite. Preserve specific domain ownership, including definition, specification and repository owners' scoped analysis, planning, execution and verification. For general product work without a more specific owner, route business clarification/requirements to Business-analyst, technical analysis/architecture/planning to Solution-architect, implementation to Software-developer and product verification to Quality-assurance. Environment-manager maintains Activity records/lifecycle; Codex Chronicle-manager owns exact-source transcripts and coverage verification. Select only the steps actually required; a discussion-only objective may complete without implementation. Missing optional owner registration is a dependent task issue, not invalid core state or permission to perform its work as Environment-manager. Do not invoke a library source definition. Use domain sources for requirements. Treat an unregistered definition under inspection/design review as data, not the execution owner.

3. Read [input:catalogues] selection guides together and resolve the final execution owner, using [input:selected_role] as a candidate when supplied. Check that owner's valid registration before loading its definition.

4. If that execution target is unregistered, route only explicitly requested registration through [Register an agent](register-agent.md), passing this procedure's root, instructions, existing permissions, Activity, catalogues and runtime evidence to the corresponding target inputs, and the requested identity/request from [input:task] to `target_name`, `target_path` and `registration_request`. Otherwise return the unregistered-target dependency. Continue below for an already prepared registration assignment whose execution owner is verified registered Environment-manager.

5. Load the final selected owner's full definition and chosen procedure. Validate its declared package-local configuration contract and run the shared read-only configuration helper for that selected agent. Retain the status, path, effective known settings, configured fields and issues; missing files use declared defaults. For invalid/unverified settings, route diagnosis or stop only dependent work; an owner-specific validator can establish isolated valid capabilities. A no-settings contract rejects nonempty overrides. Then compare its Inputs/prerequisites with authorized context. Retrieve gaps, obtain necessary unresolved human decisions, and identify missing/not-applicable information explicitly. If the agreed plan requires another specialist’s result first, obtain it using step 9.

6. Before an implementation assignment's first changes or implementation tests, obtain Environment-manager's verified original implementation-start marker through a separate record assignment, and include it in the execution handoff. Record other planned step transitions through Environment-manager as appropriate without claiming execution already occurred. Prepare the shared five-field handoff with definition path, instructions, stable Activity ID/path or applicable exception, selected-agent configuration evidence and separate core/chronicles/profile assurance; for HAI specification work include locally validated enabled/root settings and require the owner to recheck their freshness, explicit selected-procedure values, expected output and verification requirements. For a follow-up, identify retained context and changed requirements.

7. Validate the exact configured model/effort with [input:runtime_evidence] under the model-profile convention. If unavailable, return the requested pair and setup/override dependency before spawning.

8. Spawn with the supported settings and prepared handoff. Where explicit overrides require `fork_turns="none"`, supply the handoff in the task message.

9. Monitor the specialist and resolve returned input requests from authorized evidence or the human. Send clarified decisions back. When another specialist’s work is needed, use steps 2–9 to assign it in the required order. Give the requesting specialist the actual result, relevant sources and versions, produced artifacts, check results and any limits. When an authoring result requires catalogue coherence, pass its validated installed identity/decoded description and covering update scope to Environment-manager for existing-row synchronization; do not claim the overall update complete until that owner returns actual evidence. New membership or installed snapshot replacement needs its own covering scope. The requesting specialist then checks its own prerequisites.

10. Route material decisions and actual results to Environment-manager for Activity records; this does not dispatch a Chronicle batch or claim product QA passed. Return [output:delegation] and [output:specialist_result] with actual results, evidence, pending dependencies and invocation settings/override.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:delegation] | Explicit authorized assignment with required context. | All five shared checklist fields, definition path, instructions, Activity or the stated setup/diagnosis exception, expected result and verification are supplied; exact supported settings/override are reported. |
| [output:specialist_result] | Actual returned progress, evidence and dependencies. | Monitor until finished, route dependencies, and retain pending status while required inputs remain unresolved. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
