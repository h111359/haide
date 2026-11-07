# Execution policy integration review

User selected proposed rules 1, 2, 3, 4, 5, 8, 9 and 11. The shared agent convention already owns role-independent selection, handoff and ownership; it is the canonical policy location. Startup now requires this policy before optional role work. The agent concept explains the distinction and links to the policy without duplicating its rules. No new coordinator role, runtime schema, profile, setting, registration or package replacement is introduced.

## Coverage of selected rules

| Proposed rule | Final shared policy |
| --- | --- |
| 1 | Applicable role instructions, Execution prerequisites |
| 2 | Direct execution default |
| 3 | Required separate execution, Useful delegation |
| 4 | Independent verification |
| 5 | Proportionate delegation |
| 8 | Execution reporting; existing Activity communication owns launch records |
| 9 | Unavailable delegation |
| 11 | Standing delegation authorization |

The unselected proposed rules 6, 7 and 10 were not introduced as new policy. Existing invocation allocation, handoff, handle logs, writer checks and retention remain in their existing shared contracts and are referenced rather than copied. The pre-existing sentence leaving invocation choice entirely to the host now points to the explicit selection policy instead of retaining two selection authorities.

## Conflict and duplication review

- Specialist prohibitions on delegation remain in force in both modes. Orchestration belongs to the host outside the specialist assignment; following a role directly does not expand its scope or permit nested delegation.
- Direct execution does not bypass registration, configuration, permissions or model/effort availability. Existing no-silent-substitution rules remain authoritative.
- Explicit separate-agent requests and independent-review requirements take precedence over the routine-work default. Required independence cannot be satisfied by self-review.
- Standing authorization is conditional on higher-priority permissions and existing user task scope. It grants no publication, destructive or external communication authority.
- Source library definitions remain data; installed registered roles are selected for execution. No per-role copies, installed snapshot changes or catalogue synchronization are needed.
- Policy is an instruction contract, not automatic spawning logic. Existing runtime allocation APIs still do not launch workers or enforce external process lifetime.

## Manual scenario review

| Scenario | Expected policy result | Review |
| --- | --- | --- |
| Routine scoped Git commit | Direct execution when prerequisites hold | Consistent |
| Small edit depending on current conversation | Direct default | Consistent |
| Substantial bounded specialist investigation | Delegation allowed when separation adds useful value | Consistent |
| Independent tasks with compatible file ownership | Concurrent delegation allowed | Consistent |
| User explicitly requests a separate agent for a tiny task | Required separate execution overrides size default | Consistent |
| Substantial persistence/concurrency implementation | Author checks plus separate independent reviewer | Consistent |
| Small low-impact documentation change | Separate reviewer optional | Consistent |
| Optional spawn unavailable, direct prerequisites satisfied | Disclosed direct fallback allowed | Consistent |
| Required independent reviewer unavailable | Report limitation; do not claim self-review equivalent | Consistent |
| Model combination unsupported | No silent model substitution or prerequisite bypass | Consistent |
| Specialist encounters cross-role dependency | Return to host; specialist does not delegate | Consistent |
| Role name merely appears in task | No spawn solely from its mention | Consistent |

## Verification

Core startup valid. Registered-agent authoring audit passed for ten definitions and profiles with no issues; this is structural coverage and does not prove policy semantics. New titled rules pass the existing rule-wording helper. Local links and section anchors in the three edited framework files passed (fenced definition examples excluded). Scoped git diff --check passed. Scenario/conflict review above was performed by the host directly, not an independent sub-agent. No runtime code changed and no real spawn tests or broad regression rerun were required for this documentation change. Unrelated BL-0003 edits preserved. Activity remains active; no commit or closure requested.


Revision provenance: source: User-selected delegation-policy instructions; reason: Record completed shared-policy integration and actual verification; reason: Preserve placement investigation, selected-rule mapping, conflict review and actual checks; recorded 2026-11-07T16:27:17Z.
