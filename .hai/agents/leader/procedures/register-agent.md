# Register an agent

## Description

Route explicit registration requests to the core Environment-manager and return verified target eligibility or precise unresolved dependencies without executing the target.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:activity_context] | Stable current Activity ID, path and relevant record context for substantive work; applicable bootstrap/diagnosis exception when no record is needed. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:registration_request] | Explicit human request to register the named target, including any combined creation plus registration. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:target_name] | Agent name selected for registration. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:target_path] | Canonical existing definition path, or agreed canonical destination for explicitly combined creation. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:catalogues] | Framework catalogue and valid independent workspace registrations. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:runtime_evidence] | Current profile mapping/runtime support for Environment-manager, or explicit supported human override. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |

## Prerequisites

An explicit registration request and an identified target; core Environment-manager must be validly registered and invocable. Package installation does not require an optional authoring agent.

## Rules

None.

## Steps

1. Establish [input:workspace_root], load [input:instructions], and compare [input:registration_request] with [input:authority]. If explicit registration permission is absent, return the missing decision.

2. Resolve [input:target_name] and [input:target_path] from authorized context, returning ambiguous identity before assignment.

3. Verify Environment-manager's valid framework entry in [input:catalogues], then load its registration procedure. Return core-owner or invocation dependencies without substituting the optional authoring agent. A source-only target first needs the explicitly authorized selective installation through Environment-manager; no whole library or source-role invocation is needed.

4. Prepare the registration assignment with target identity, origin, actual request, allowed changes and [input:activity_context]. If creation was explicitly combined, first obtain Agent-definition-manager's authorized authoring result through normal delegation, then pass its canonical target and verified metadata to Environment-manager. Do not assign authoring to the installer or registration to the author. An absent authoring owner is a separate optional-package installation dependency that Environment-manager can resolve under explicit scope.

5. Execute [Delegate work](delegate-work.md), mapping [input:workspace_root] to target `workspace_root`, [input:instructions] to `instructions`, the prepared [input:registration_request]/[input:target_name]/[input:target_path] assignment to `task`, [input:authority] to `authority`, [input:activity_context] to `activity_context`, [input:catalogues] to `catalogues`, the verified registered Environment-manager definition to `selected_role`, and [input:runtime_evidence] to `runtime_evidence`.

6. Receive Environment-manager's actual installed-definition/contract validation and catalogue evidence; its trusted shared tools do not depend on invoking Agent-definition-manager. If validation or coordinated updates are unresolved, return that status.

7. Recheck the returned target entry and definition evidence, then return [output:registration_result] with actual registration status and remaining dependencies.

8. If separate substantive target execution is authorized, send that work through normal selection and [Delegate work](delegate-work.md); otherwise finish after the registration report.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:registration_result] | Verified target identity/path, origin, actual registration status and definition/catalogue evidence, or exact dependency. | Core Environment-manager performed explicit registration or existing-row synchronization after any separately completed authoring/installation and its evidence was rechecked; target execution is separate and never implied. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
