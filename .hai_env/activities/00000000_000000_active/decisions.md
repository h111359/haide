# Decisions

## Run notebooks and context

- **HAI coordinator notebook:** The user answered yes: HAI, acting as coordinator, has its own run notebook. The exact boundary among chat, turn, and Activity for creating that coordinator run remains unspecified.
- **Fresh context:** Each invocation starts with fresh host context. HAI may provide references to other invocations when needed.
- **Prior notebooks:** Runs do not browse other run notebooks automatically. HAI must explicitly decide to refer to them.
- **Shared edits:** The user chose “no blocking” for concurrent edits. A more detailed coordination or conflict-handling policy remains unspecified.
- **Specification/product updates:** An agent may directly update specification or product when the work is within its assigned scope and definition; a separate invocation requirement is not imposed.

Source: user chat at 2026-11-03T20:21:51Z; exact supplied text is preserved in `input.md`. These are user decisions on the five prior questions. Other architecture details in `analysis.md` remain proposals unless separately decided.


## Transcript decisions and open question — 2026-11-03T20:33:14Z

- **Transcript content:** The user accepted user/assistant messages as transcript content, with tool activity kept in separate linked logs.
- **Incomplete-transcript closure policy:** Undecided. The user asked for an explanation of the question before answering. No nonblocking default was accepted; current closure rules remain unchanged.

Source: user chat at 2026-11-03T20:33:14Z; exact supplied response is preserved in `input.md`.


## Closure and transcript preservation — 2026-11-03T20:37:22Z

- **User intent:** Activity closure should not be blocked by transcript synchronization, and transcript preservation remains desired.
- **Mechanics:** The user has not approved a specific synchronization design. The proposal below remains under consideration.

Source: user chat at 2026-11-03T20:37:22Z; exact supplied wording is preserved in `input.md`.


## Correction: attribution of answer 4 — 2026-11-03T20:44:38Z

The Business-analyst’s read-only review verified that the preceding user-facing question for answer 4 was: “Should missing token telemetry block execution? I recommend allowing execution while marking usage unavailable.” Therefore the user’s “4 No, no blocking” settles token-telemetry absence as nonblocking, with usage marked unavailable rather than zero. The earlier “Shared edits” bullet above misattributed that answer; it is preserved as historical text, but this correction supersedes its interpretation. The policy for concurrent writes remains unresolved. This corrects the record and does not change the user’s decision.

Source: corrected prompt mapping returned by Business-analyst during the read-only clarification review at 2026-11-03T20:44:38Z.


## Runtime integration, host scope, and transcript limitations — 2026-11-04

- **Agent integration:** HAI uses a small integration contract; specialist behavior stays in external agent definitions.
- **First host release:** Fully support Codex first while designing for additional hosts.
- **Limited transcript hosts:** Support hosts that cannot expose or save every message; preserve everything available and report transcript limitations. Activity closure remains nonblocking.

Source: three exact question/answer pairs supplied through the UI on 2026-11-04; exact wording is in `input.md`. These settle the corresponding priority questions. Implementation mechanics remain proposals.


## Upgrade, coordinator continuity, and conflict decisions — 2026-11-04

- **Existing environments:** Upgrade only when explicitly requested; preserve configuration, agents, Activity history, and transcript evidence.
- **Same Activity in another chat:** Create a new linked coordinator notebook and explicitly select carried-forward context.
- **Conflicting agent edits:** Preserve both contributions and resolve conflicts before declaring affected work complete. HAI handles routine choices; ask the user only for new business decisions.

Source: three exact question/answer pairs supplied through the UI on 2026-11-04; exact wording is preserved in `input.md`.


## Test and repository temporary-file placement — 2026-11-04

- **Testing:** All test execution and test-generated work must stay under the current Activity folder.
- **Repository runtime:** Do not create temporary or scratch files in the repository’s real `.hai/`.

Source: user chat on 2026-11-04; exact wording is preserved in `input.md`. Activity-local scratch for non-test operations is a plan preference when safe, not an additional user constraint.
