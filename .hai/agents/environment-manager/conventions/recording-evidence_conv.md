# Recording evidence for Activity closure

## Ownership and purpose

Environment-manager owns Activity lifecycle and this closure interface. The optional
installed Codex Chronicle-manager owns exact-source coverage verification. Leader
assigns and returns that verification; neither specialist invokes another.
This contract does not depend on any optional package being installed to load,
validate or initialize core state, discover records or close with verified
disabled/no-independent-obligation recording.

## Closure request

Each authorized closure has a fresh unique `operation_id`, stable `activity_id`,
exact completed-source `cutoff` list and attributable `enabled_intervals` list.
The cutoff includes completed source through the user's closure request across
required sources; it excludes the future closure acknowledgement. Each cutoff
occurrence has `source_session_id` and exactly one authoritative nonblank
`message_id` or nonnegative integer `source_position` excluding Booleans.
Cutoffs and enabled intervals are supplied by Leader, never guessed by an owner.
Each enabled interval has an attributable nonblank `provenance`, a `start`
occurrence and an `end` occurrence or `null`; both boundaries belong to the same
source session. Occurrence types are strict on both request and proof: Boolean
values are never numeric source positions, and numeric values never replace flags.

`recording_requirement` has Boolean `enabled` and `mandatory` fields from current
validated state and applicable instructions. A threshold or timestamp alone never
establishes recording enablement or complete coverage.

## Verification evidence

For required recording, Leader returns the actual responsible owner's fresh proof:

| Field | Required value or meaning |
| --- | --- |
| `verification_id` | Nonblank unique identity of this completed verification. |
| `verified_at` | Actual UTC verification timestamp, not a promised future result. |
| `status` | `verified`; pending, blocked, disabled or partial evidence is insufficient here. |
| `activity_id`, `operation_id`, `cutoff`, `enabled_intervals` | Exact match to this closure assignment. |
| `recording_requirement` | Exact match to current `enabled` and `mandatory` values. |
| `retained_source_complete` | Boolean `true` for every required assigned retained source. |
| `gaps`, `conflicts` | Explicit empty arrays after fresh full assigned coverage inspection. |
| `active_writes` | Boolean `false`, reconciled with actual invocation state by Leader. |
| `source_snapshots` | Nonempty object mapping required source-session IDs to SHA-256 digests of actual readback source files; covers every cutoff source. |
| `artifact_snapshots` | Nonempty object mapping all relevant contained Activity-relative segment/checkpoint paths to SHA-256 digests of actual readback bytes. |

The existing generic transcript and checkpoint bytes, occurrence identities and
historical names remain compatible. Proof does not replace exact-source inspection:
Codex Chronicle-manager verifies all required ranges, including earlier gaps, then
returns these operation-bound fingerprints. A checkpoint timestamp, dispatch cursor,
latest batch success or QA result is not a substitute.

## Handoff and freshness

Leader resolves earlier writers, gives Chronicle sole mutation ownership for fresh
verification, receives its result and confirms its writes stopped. It then returns
the proof and sole mutation assignment to Environment-manager for this closure.
Environment-manager compares the proof with its current requirement, exact closure
assignment and fresh source/artifact snapshots. Source reads are limited to the
explicit authorized paths behind the assigned identities; hashes check freshness,
not transcript interpretation. It never discovers unrelated session sources.

An explicitly authorized immutable exact-byte source-prefix snapshot may be used
for a live append-only session under the installed source owner's convention.
The proof retains original source identity/path, physical cutoff, snapshot path,
byte length/hash and actual creation provenance. Before archival, independently
compare that prefix with the same bytes of the original and obtain fresh
Leader-returned Chronicle assurance that no later eligible source invalidates the
cutoff. Changed original prefix, unavailable original, ambiguous tail or new
eligible exchanges block closure; appended excluded tool/progress records alone
do not. Hashing an unchanged snapshot without those original-source checks is
insufficient evidence of freshness.

Any missing optional owner, missing retained source, gaps, conflicts, altered
artifacts, changed requirement/cutoff/intervals or uncertain writer status blocks
dependent closure. Changed proof inputs return to Leader for a new verification;
Environment-manager neither invokes Chronicle nor repairs evidence itself.
New eligible completed source before archival requires a new cutoff and fresh
verification through Leader. Future undelivered acknowledgement is not required.

The core read-only closure gate checks the supplied proof contract and exact
snapshot equality. Caller path/type checks and actual fresh file hashes remain
required; a successful schema comparison cannot prove truthful inputs or source
coverage. Disabled/no-independent-obligation closure uses verified current flags,
requires no source or optional owner, and creates no transcript/checkpoint.
