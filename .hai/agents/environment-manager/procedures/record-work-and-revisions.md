# Record work and revisions

## Description

Record assigned step transitions, material revisions and actual specialist evidence while preserving history and returning verified record changes and unresolved limits.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Leader or authorized caller | Retrieve context; return unresolved root before dependent work. |
| [input:instructions] | Applicable fixed mandatory and workspace/session instructions. | Mandatory | Caller and safe fixed instructions | Empty readable content is valid; missing/unreadable content blocks dependent work. |
| [input:authority] | Authorized record operation, scope, constraints and existing permissions. | Mandatory | Human request relayed by Leader | Retrieve authority; do not invent approval or perform substantive domain work. |
| [input:environment_context] | Validated compatible environment and safe Activity store. | Mandatory | Caller and startup/configuration evidence | Retrieve context; return missing or conflicting assurance. |
| [input:selected_activity] | Stable current active Activity ID/path and relevant context. | Mandatory | Leader and record discovery | Recheck discovery; stop dependent writes for inconsistent or closed work. |
| [input:work_context] | Selected record transition, actual decisions, source provenance, prepared artifacts, implementation-start assignment or deliberately skipped work. | Mandatory | Leader and attributable task evidence | Retrieve context; never infer performed work from a proposal. |
| [input:specialist_evidence] | Actual returned specialist results, checks and artifacts. | Optional | Leader and responsible owners | Keep required external work pending; never invoke specialists or invent success. |
| [input:related_activities] | Relevant stable related IDs and source references. | Optional | Authorized context | Leave absent rather than invent links. |

## Prerequisites

Read the core Activity concept and convention. A validated store, safe local targets, active consistent Activity and sole mutation assignment are available. Record decisions and result assertions require their actual attributable evidence; recording implementation start requires the authorized pending implementation assignment, before its first changes or implementation tests.

## Rules

None.

## Steps

1. Establish [input:workspace_root], load [input:instructions] and validate [input:selected_activity] under [input:environment_context]. Resolve [input:authority] and [input:work_context]; check stable identity, active lifecycle, sole mutation ownership and safe store consistency.

2. Inspect actual supplied decisions/source, [input:specialist_evidence] and relevant [input:related_activities]. Return missing or ambiguous provenance and substantive domain dependencies to Leader; continue only independent record work.

3. For a planned assignment, mark only the assigned step `in_progress` and log what is about to be assigned. Before first implementation changes or implementation tests, set implementation status and the original `implementation_started_at` together, then return the verified marker to Leader before the responsible specialist proceeds. Preserve that timestamp on retries; a plan is not evidence of completed execution.

4. Save supplied useful clarification, decisions, requirements, analysis, design, plan or questionnaire content with its actual source. Before replacing a material definition/analysis/plan, exclusively preserve the exact predecessor at the convention's unused revision path and record author/source, UTC date, reason, predecessor and dependent impact.

5. Record supplied reassessment of affected artifacts, assumptions, implementation and checks after a revision. Preserve earlier evidence and mark stale dependent results pending; return unresolved technical reassessment to Leader for the appropriate owner instead of performing it here.

6. Record actual specialist results and verification separately, including attempts, deviations, failed/blocked/skipped/unrun checks and deliberate omissions. Set step status only from supporting evidence; keep required external work pending. Record verification checks validate the record, not the product's acceptance criteria.

7. Recheck inputs, sole ownership and containment before writes, read back the changed records and verify preserved identity, history, original implementation start and evidence-supported statuses. Return [output:record_result] with actual paths, changes, checks and unresolved dependencies; do not synchronize transcripts or infer closure.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:record_result] | Verified record transitions, retained revisions, implementation-start evidence, recorded specialist results and limits. | Stable identity and original start are preserved; previous material versions remain attributable; actual work and proposed work are distinct; missing external results remain pending. |

## References

- [Role definition](../SKILL.md) — inherited rules and record references; required before execution.
