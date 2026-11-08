# Recording evidence for Activity closure

## Ownership and purpose

Core owns Activity lifecycle, source synchronization and exact-source coverage verification. The host assigns explicit sources, boundaries, provenance and serializes writers. Enabled or independently mandatory recording requires synchronization and verification before closure; disabled/no-independent-obligation closure needs no source or recording writes.

## Closure request

Each authorized closure has a fresh unique `operation_id`, stable `activity_id`,
exact completed-source `cutoff` list and attributable `enabled_intervals` list.
The cutoff includes completed source through the user's closure request across
required sources; it excludes the future closure acknowledgement. Each cutoff
occurrence has `source_session_id` and exactly one authoritative nonblank
`message_id` or nonnegative integer `source_position` excluding Booleans.
Cutoffs and enabled intervals are supplied by host coordinator, never guessed by an owner.
Each enabled interval has an attributable nonblank `provenance`, a `start`
occurrence and an `end` occurrence or `null`; both boundaries belong to the same
source session. Occurrence types are strict on both request and proof: Boolean
values are never numeric source positions, and numeric values never replace flags.

`recording_requirement` has Boolean `enabled` and `mandatory` fields from current
validated state and applicable instructions. A threshold or timestamp alone never
establishes recording enablement or complete coverage.

## Verification evidence

For required recording, core produces and validates fresh operation-bound proof:

| Field | Required value or meaning |
| --- | --- |
| `verification_id` | Nonblank unique identity of this completed verification. |
| `verified_at` | Actual UTC verification timestamp, not a promised future result. |
| `status` | `verified`; pending, blocked, disabled or partial evidence is insufficient here. |
| `activity_id`, `operation_id`, `cutoff`, `enabled_intervals` | Exact match to this closure assignment. |
| `recording_requirement` | Exact match to current `enabled` and `mandatory` values. |
| `retained_source_complete` | Boolean `true` for every required assigned retained source. |
| `gaps`, `conflicts` | Explicit empty arrays after fresh full assigned coverage inspection. |
| `active_writes` | Boolean `false`, reconciled with actual invocation state by host coordinator. |
| `source_snapshots` | Nonempty object mapping required source-session IDs to SHA-256 digests of actual readback source files; covers every cutoff source. |
| `artifact_snapshots` | Nonempty object mapping all relevant contained Activity-relative segment/checkpoint paths to SHA-256 digests of actual readback bytes. |

The existing generic transcript and checkpoint bytes, occurrence identities and
historical names remain compatible. Proof does not replace exact-source inspection:
Core verifies all required ranges, including earlier gaps, and produces operation-bound fingerprints. A checkpoint timestamp, dispatch cursor,
latest batch success or QA result is not a substitute.

## Handoff and freshness

The host resolves earlier writers and supplies explicit registered assignments. Core close synchronizes those sources and verifies the current requirement, exact closure assignment and fresh source/artifact snapshots. Reads are limited to authorized source paths; hashes check freshness, not transcript interpretation. It never discovers unrelated sessions.

An explicitly authorized immutable exact-byte source-prefix snapshot may be used only with the original-source provenance and freshness safeguards in the [source convention](codex-source_conv.md). Changed original prefix, unavailable original, ambiguous tail or new eligible exchanges block stale proof. New eligible completed source before archival requires a fresh cutoff and verification. Future undelivered acknowledgement is not required.

Missing or pending required source, gaps, conflicts, altered artifacts, changed requirement or assignment, or uncertain writer status blocks enabled or independently mandatory closure. Do not silently repair legacy state or partial operations. Disabled/no-independent-obligation closure requires no source and creates no transcript or checkpoint. A schema comparison or hash alone cannot prove truthful attribution or exact coverage.
