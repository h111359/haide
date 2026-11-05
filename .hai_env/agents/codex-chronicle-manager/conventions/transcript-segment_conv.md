# Transcript segment convention

## Segment identity and paths

Segments are UTF-8 Markdown under the assigned existing Activity's `chronicles/`.
Identity comprises source session, stable Activity ID and exact assigned source
boundaries; session identity alone is not a unique segment. Multiple segments may
legitimately share one session/Activity. Identical message text can represent
separate source occurrences.

A normal filename derives from original session start in `Europe/Sofia`:
`YYYYMMDD_HHMM_segment-01.md`, followed by unused increasing segment numbers per
session and Activity. Seconds distinguish different sessions starting in the same
minute. A name identifies only its assigned source/segment and cannot overwrite
another. Authorized historical byte-preserving moves may retain original names.

## Metadata and exchange layout

`## Source:` contains source session ID, durable saved local source path, original
start time, stable Activity ID, exact assigned start/end boundaries and the last
verified completed-source boundary. Metadata is distinct from verbatim text and
claims only verified coverage. A prepared pre-delivery entry identifies its
prepared status separately; it is not yet a completed durable-source outcome.

Repeated `## Prompt:` and `## Outcome:` headings contain the exact human prompts,
delivered clarification questions/answers and final assistant outcomes in source
order. Spelling, escaping, whitespace and Markdown remain exact. Metadata,
system/developer instructions, tool calls and intermediate progress are outside
exchange text; human formatting that resembles instructions remains human text.

Optional `## Operation result:` metadata contains an actual completed operation's
descriptive label and verified exact result/message. A proposed operation/message
is not completed-operation evidence. This metadata is separate from verbatim
exchanges and does not imply that recording performed the domain operation.

## Coverage and historical compatibility

Coverage identifies assigned eligible source occurrences. Off-period messages are
excluded, while a genuine unresolved missing-source gap is incomplete coverage.
Later catch-up can include an outstanding earlier eligible boundary without
including intervening off-period exchanges. Earlier off periods require explicit
historical-import permission to enter coverage.

Existing segment bytes and older optional operation-specific headings remain
historical records. An earlier optional label alone is no source/assignment defect
and does not require rewriting or reinterpretation. Byte-preserving historical
imports retain their original bytes; Activity provenance separately identifies
assignment, original path, actual import date and exact-source limitations.

## Recording checkpoint

Codex Chronicle-manager owns the optional `chronicles/checkpoint.json` inside the stable
Activity. It is operational progress, separate from global environment settings,
Activity lifecycle state and verbatim segment text.

The UTF-8 JSON root is an object with unique property names and these fields:

| Field | Content |
| --- | --- |
| `checkpoint_format_version` | Integer `1`. |
| `activity_id` | The existing stable Activity UUID. |
| `sources` | Array of Source objects with source-session identities, durable paths, exact Activity assignment ranges and attributable enabled intervals. |
| `verified_ranges` | Array of Verified objects identifying exact source-backed ranges and segment paths. |
| `pending_ranges` | Array of Pending objects distinguishing gaps, unsaved outcomes, prepared-text reconciliation and conflicts. |
| `cadence_cursors` | Object mapping source-session IDs to the last observed user-prompt Occurrence at the most recent batch dispatch; scheduling only, never recording completeness. |
| `last_attempt` | Attempt object with actual status, or `null` before the first attempt. |
| `last_successful_at` | Actual UTC completion time of the last fully verified assigned batch, or `null`; a recent success does not erase earlier pending ranges. |
| `in_flight` | Current invocation/attempt identity and assigned cutoff, or `null`. An interrupted invocation is unresolved until host coordinator reconciles it with actual runtime and files. |

Nested shapes use the following field names and types. Every listed field is
present unless explicitly optional; timestamps use `YYYY-MM-DDTHH:MM:SSZ`.

- **Occurrence:** `source_session_id` is a nonblank string, with exactly one of `message_id` (nonblank authoritative string) or `source_position` (nonnegative integer excluding Boolean). An occurrence names existing source, never a future message.
- **Range:** `start` and `end` are inclusive Occurrence objects in the same session, in authoritative source order.
- **Source:** `source_session_id` is a nonblank string; `durable_path` is the authoritative path string or `null` if unavailable; `original_started_at` is the authoritative original timestamp string or `null`; `assigned_ranges` is an array of Range objects; `enabled_intervals` is an array of Interval objects; `retained_source_complete` is `true`, `false` or `null` when unverified.
- **Interval:** `start` is an Occurrence; `end` is an Occurrence or `null` while enablement continues; `provenance` is a nonblank attributable configuration-boundary string. The source-session identity follows the occurrences. Unverified boundaries are Pending objects, not guessed intervals.
- **Verified:** `range` is a Range; `segment_path` is a contained Activity-relative string; `verified_at` is an actual UTC timestamp string.
- **Pending:** `source_session_id` is a known nonblank string or `null`; `range` is a Range or `null` when exact boundaries are unavailable; `reason` is `missing_source`, `unknown_boundary`, `pending_outcome`, `prepared_delivery`, `divergence`, `overlap` or `partial_write`; `status` is `pending`, `blocked` or `partial`; `details` is a nonblank explanation. A missing future outcome can reference its known prompt range without inventing an outcome identity.
- **Attempt:** `attempt_id` is a nonblank generated operational identity; `dispatch_cursors` has the same object shape as `cadence_cursors`; `started_at` is an actual UTC timestamp; `finished_at` is an actual UTC timestamp or `null`; `status` is `running`, `verified`, `pending`, `blocked`, `partial`, `failed` or `disabled`; `error` is a nonblank string or `null`.
- **In-flight:** `attempt_id` is the matching Attempt identity; `invocation_id` is the actual runtime identity string or `null` if not exposed; `cutoffs` is an array of existing Occurrence objects, one per assigned source boundary. It is never evidence that a runtime job has stopped.

A source occurrence is identified by its authoritative session/message identity.
If the source has no message IDs, its stable source position and session identity
identify an occurrence. Identical text, a timestamp alone, or a content hash alone
cannot distinguish repeated messages. Missing authoritative identities remain a
blocker, never an invented count or verified range. Ranges cannot cross unassigned
or disabled intervals and cannot conceal gaps. Each pending range remains separate
until actual verification resolves it; newer coverage or scheduling cursors cannot
clear it. Source assignments survive Activity switches and archive renames by
stable Activity ID, with contained relative segment paths.

## Closure verification evidence

A closure verification result identifies the requested closure operation, stable
Activity ID, current validated recording requirement, effective enabled intervals,
source-session cutoffs through the completed closure-request occurrence, exact
verified ranges, unresolved gaps/conflicts and active-write status. Relevant source
identities and retained-source completeness accompany the ranges. A disabled result
states the verified disabled/no-independent-obligation condition instead of claiming
source coverage. Prepared final-text entries remain distinct from saved source.

## References

- [Codex Chronicle-manager](../SKILL.md) — inherited recording and exact-text rules and owner procedures.
- [Activity convention](../../../../.hai/conventions/activity_conv.md) — Activity identity, paths and lifecycle.
- [State convention](../../../../.hai/conventions/state_conv.md) — enablement and prompt threshold; configuration remains runtime's responsibility.
- [Durable session source](../concepts/durable-session-source.md) — source meaning and evidence limits.
- [Source coverage](../concepts/source-coverage.md) — exact coverage meaning.
