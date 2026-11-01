# Close or supplement

## Description

Close authorized work or append an attributable closed-record supplement while preserving history, and return verified lifecycle, outcome, and reference results.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:operation] | Selected record/lifecycle or assigned substantive-work operation. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:environment_context] | Caller-validated compatible environment and safe activities.location; direct HAI calls have no standalone bypass. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:selected_activity] | Selected consistent current or closed record with stable ID/path. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:closure_instruction] | Explicit authorized closure decision and relevant objective/evidence. | Optional | Human instruction relayed by leader | No closure; finishing a step or response does not authorize it. |
| [input:supplement_provenance] | Author/source, UTC date, reason and supporting evidence for a closed-record supplement. | Optional | Attributable supplied evidence | Supplement writes wait for all provenance; new substantive work needs a new linked Activity. |
| [input:archive_label_outcome] | Short archive label and closure outcome. | Optional | Caller choices or verified subject/evidence | Derive from subject/evidence; return ambiguous outcome/label rather than guess. |
| [input:recording_context] | Validated recording requirement and, when required for closure, exact Activity/source assignment through the closure request, source metadata, coverage context and optional existing segments/import/evidence. | Optional | Leader's validated environment, source assignment and returned recording progress | Retrieve authorized context; disabled/no-independent-obligation closure needs no source inspection. Enabled or independently mandatory recording blocks closure until its exact source context and fresh verification are available. |

## Prerequisites

Read the package [Activity concept](../concepts/activity.md) and [Activity convention](../conventions/activity_conv.md). Caller-validated compatible environment/store context and local path/type validation are required. Closure requires the actual authorized closure decision, sole mutation ownership and verified current recording requirement. When recording is enabled or independently mandatory, usable exact recording context through the closure request is required; this procedure obtains fresh verification before lifecycle mutation. A closed-record supplement requires attributable provenance and relevant evidence.

## Rules

- **Archive destination.** Activity-manager MUST use a rename that fails without overwrite if the chosen archive destination appears between check and mutation.
- **Partial closure.** Activity-manager MUST stop dependent work when closure is only partially complete.

## Steps

1. Establish [input:workspace_root], load [input:instructions], and resolve [input:operation]/[input:authority]. Select [input:selected_activity] under [input:environment_context] and validate lifecycle, identity, store consistency and safe paths.

2. Select the requested branch: closure requires the active current record and [input:closure_instruction], while supplement requires a closed record. Return a lifecycle/operation mismatch or existing closed status instead of mutating it. For closure, compare actual evidence/remaining work with the objective and derive or validate [input:archive_label_outcome], returning ambiguity for decision.

3. Before closure, ask Leader to finish or resolve active mutating assignments for this stable Activity and retain the sole mutation assignment for verification and archive. Resolve the current validated recording requirement from [input:environment_context]/[input:recording_context]. If recording is disabled with no independent mandatory obligation, record that verified condition and continue without source synchronization. Otherwise obtain the exact completed-source cutoff through the user's closure request across required enabled intervals and all earlier eligible gaps; return missing source/assignment as a blocker.

4. For that enabled/mandatory branch, execute [Verify recording](verify-recording.md) in this same Activity-manager invocation: pass [input:workspace_root] to target `workspace_root`, [input:instructions] to `instructions`, and [input:authority] to `authority`. Pass the `recording_requirement`, `activity_assignment`, `source_metadata`, `coverage_context`, `existing_segments`, `operation_evidence` and `historical_import` fields of [input:recording_context] explicitly to those respective target inputs; omit absent optional fields. Pass this closure's stable Activity ID, requested operation and exact closure-request cutoff to target `planned_operation`. Review the returned verification for that operation and cutoff; stop closure on missing retained source, gaps, divergence, conflicts, partial status or unresolved writes. Do not require a future closure acknowledgement to exist in saved source.

5. After that prerequisite passes or is verified inapplicable, prepare outcome.md with the actual outcome, performed/skipped work, checks, external completion evidence, recording verification/disabled status and unresolved limits. Select the actual UTC closure time and an absent convention-compliant archive destination; prepare affected persistent-reference updates.

6. Recheck sole mutation ownership, recording evidence/cutoff, inspected inputs and destination absence. If new eligible completed source arrived before mutation, refresh step 4 verification first. Then coordinate outcome/state closure, guarded archive rename and reference updates, preserving stable identity and history. Keep checkpoint/segment paths valid relative to the archived Activity and do not rename while recording writes remain active.

7. After that closure update, verify archive/state timestamp and naming agreement, closed identity, required outcome, absent current path, store consistency and affected references. Return any partial inconsistency before further dependent work.

8. For a closed-record supplement instead, validate [input:supplement_provenance] author/source, UTC date, reason, evidence and earlier assertion supplemented. Append the attributable supplement and read it back. Return separately requested exact old-source synchronization to Leader for an explicit recording assignment with its existing Activity/source boundary.

9. Return [output:lifecycle_result] for the selected closure/supplement branch, with stable IDs/paths, lifecycle, performed steps, actual outcome, fresh recording evidence or verified disabled status and remaining work.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:lifecycle_result] | Stable IDs/paths, lifecycle, performed steps, actual outcome, changes, checks, recording verification/disabled status and unresolved work. | Verify closure/archive/reference consistency or append-only attributable supplement; enabled/mandatory closure has fresh complete required-source coverage through its cutoff, disabled/no-obligation closure does not require transcript synchronization. Preserve history and do not reopen closed work. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
