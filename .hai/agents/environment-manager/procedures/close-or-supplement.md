# Close or supplement

## Description

Close authorized work or append an attributable closed-record supplement while preserving history, and return verified lifecycle, outcome, and reference results.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:operation] | Selected record/lifecycle operation. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:environment_context] | Caller-validated compatible environment and safe activities.location; direct HAI calls have no standalone bypass. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:selected_activity] | Selected consistent current or closed record with stable ID/path. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:closure_instruction] | Explicit authorized closure decision and relevant objective/evidence. | Optional | Human instruction relayed by leader | No closure; finishing a step or response does not authorize it. |
| [input:supplement_provenance] | Author/source, UTC date, reason and supporting evidence for a closed-record supplement. | Optional | Attributable supplied evidence | Supplement writes wait for all provenance; new substantive work needs a new linked Activity. |
| [input:archive_label_outcome] | Short archive label and closure outcome. | Optional | Caller choices or verified subject/evidence | Derive from subject/evidence; return ambiguous outcome/label rather than guess. |
| [input:recording_context] | Current validated recording requirement; for required recording, exact closure operation ID, Activity/source cutoff and enabled intervals, fresh Chronicle verification proof, explicit authorized source/artifact paths and stopped-writer assurance returned through Leader. | Optional | Leader's validated environment, source assignment and returned recording progress | Retrieve authorized context; disabled/no-independent-obligation closure needs no source inspection. Enabled or independently mandatory recording blocks closure until its exact source context and fresh verification are available. |

## Prerequisites

Read the package [Activity concept](../concepts/activity.md) and [Activity convention](../conventions/activity_conv.md). Caller-validated compatible environment/store context and local path/type validation are required. Closure requires the actual authorized closure decision, sole mutation ownership and verified current recording requirement. When recording is enabled or independently mandatory, usable exact recording context through the closure request is required; Leader returns fresh operation-bound Chronicle verification and stopped-writer assurance before lifecycle mutation. A closed-record supplement requires attributable provenance and relevant evidence.

## Rules

- **Archive destination.** Environment-manager MUST use a rename that fails without overwrite if the chosen archive destination appears between check and mutation.
- **Partial closure.** Environment-manager MUST stop dependent work when closure is only partially complete.

## Steps

1. Establish [input:workspace_root], load [input:instructions], and resolve [input:operation]/[input:authority]. Select [input:selected_activity] under [input:environment_context] and validate lifecycle, identity, store consistency and safe paths.

2. Select the requested branch: closure requires the active current record and [input:closure_instruction], while supplement requires a closed record. Return a lifecycle/operation mismatch or existing closed status instead of mutating it. For closure, compare actual evidence/remaining work with the objective and derive or validate [input:archive_label_outcome], returning ambiguity for decision.

3. Before closure, return a verification dependency to Leader unless this assignment already carries the required fresh evidence. Leader finishes or resolves active mutating assignments for this stable Activity. Resolve the current recording requirement from [input:environment_context]/[input:recording_context]. If recording is disabled with no independent mandatory obligation, record that verified condition and continue without source inspection, optional-owner invocation or transcript/checkpoint writes. Otherwise require a fresh unique closure operation ID, exact completed-source cutoff through the user's closure request across required enabled intervals and all earlier eligible gaps. Missing source/assignment, optional Chronicle registration or usable verification remains a closure blocker, not a core startup failure.

4. For required recording, inspect Leader-returned Codex Chronicle-manager proof under the core recording-evidence convention. Do not invoke that specialist or execute its procedures. Require exact stable Activity ID, closure operation ID, cutoff, intervals and current requirement, fresh complete retained-source coverage, empty gaps/conflicts and actual stopped writers. Validate explicit authorized source paths and Activity-relative artifact targets; independently hash those exact files and compare with proof snapshots. With a verified interpreter, run the core read-only recording gate using this current requirement/operation, returned evidence, fresh `current_sources`/`current_artifacts` maps and Leader-reconciled `writers_stopped`. Treat any missing, stale, changed, partial or blocked proof as a dependency returned to Leader for new verification. Do not require a future closure acknowledgement in saved source.

5. After that prerequisite passes or is verified inapplicable, prepare outcome.md with the actual outcome, performed/skipped work, checks, external completion evidence, recording verification/disabled status and unresolved limits. Select the actual UTC closure time and an absent convention-compliant archive destination; prepare affected persistent-reference updates.

6. Recheck sole mutation ownership, recording evidence/cutoff, inspected inputs and destination absence. Rehash the authorized source/artifact files and rerun the gate immediately before mutation. If new eligible completed source, changed requirement/cutoff/intervals, altered artifacts or an uncertain writer appeared, stop and return the changed inputs to Leader for fresh verification; never reuse an earlier operation's proof. Then coordinate outcome/state closure, guarded archive rename and reference updates, preserving stable identity and history. Keep checkpoint/segment paths valid relative to the archived Activity and do not rename while recording writes remain active.

7. After that closure update, verify archive/state timestamp and naming agreement, closed identity, required outcome, absent current path, store consistency and affected references. Return any partial inconsistency before further dependent work.

8. For a closed-record supplement instead, validate [input:supplement_provenance] author/source, UTC date, reason, evidence and earlier assertion supplemented. Append the attributable supplement and read it back. Return separately requested exact old-source synchronization to Leader for an explicit recording assignment with its existing Activity/source boundary.

9. Return [output:lifecycle_result] for the selected closure/supplement branch, with stable IDs/paths, lifecycle, performed steps, actual outcome, fresh recording evidence or verified disabled status and remaining work.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:lifecycle_result] | Stable IDs/paths, lifecycle, performed steps, actual outcome, changes, checks, recording verification/disabled status and unresolved work. | Verify closure/archive/reference consistency or append-only attributable supplement; enabled/mandatory closure has fresh complete required-source coverage through its cutoff, disabled/no-obligation closure does not require transcript synchronization. Preserve history and do not reopen closed work. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
- [Recording evidence](../conventions/recording-evidence_conv.md) and [core gate README](../../../tools/activities/README.md) — required for closure; the core contract is available without the optional Chronicle package.
