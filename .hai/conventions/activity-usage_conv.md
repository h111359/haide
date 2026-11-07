# Activity usage records

## Purpose and files

An Activity's `usage.md` is its readable token/credit snapshot; `usage.json` is the
managed source/checkpoint record behind it. Both are optional until the first
update, and both move with the Activity on archival. Core state format is unchanged.

The runtime updates these files on `activity usage-update` and automatically before
an applied `activity close`. `activity usage-read` reads the retained snapshot,
including archived Activities, without refreshing or creating files. Closed
Activities reject ordinary updates so live sources cannot silently charge later
work to a finished Activity.

These files are runtime-managed, not free-form notes. Existing malformed state,
an edited report, or a report without its checkpoint is preserved and reported for
explicit resolution. No implicit adoption, repair or rollback occurs. Usage format 2 contains tokens and
credits only. Unreleased format-1 checkpoints with null monetary fields remain
readable and are written as format 2 on the next applied update; non-null legacy
monetary data requires explicit preservation before replacement.
Notes and audit explanations belong in the Activity's ordinary supporting files.

## Explicit source attribution

The host assigns every relevant session explicitly. A binding contains `path`,
`session_id`, inclusive `start_position` and optional inclusive `end_position`.
Positions are physical zero-based JSONL record positions; omitted/null end means
read the latest complete saved source during each update. A canonical regular
nonlinked source may be outside the workspace only under explicit source authority.
The runtime never searches Codex home, other sessions or account data.

The host supplies boundaries for the work assigned to this Activity, not an entire
long conversation by default. It adds separate parent/sub-agent sessions only when
their actual saved source identity and attribution are available, and avoids
assigning overlapping consumption to multiple Activities. Allocation or a host
agent handle does not prove a source path or token count. Unknown sessions remain
a coverage limit; registered sources alone never prove coverage of all related work.

`sources` on update adds bindings or repeats identical ones. Existing path/session
boundaries are immutable; changed attribution needs explicit owner-led resolution.
Duplicate session IDs are rejected. Omitting sources refreshes all registered
bindings; it does not remove earlier assignments or add discovered sessions.

## Supported saved Codex source

The reader requires strict UTF-8 JSONL retained from `session_meta`, matching the
assigned ID. Consistent repeated resume metadata is accepted. It reads model labels
from `turn_context` and cumulative `event_msg` / `token_count` counters from
`info.total_token_usage`. Other record contents are not copied into usage files.

For the selected range it computes counter increments from the last preceding
snapshot, or session-start zero when no earlier snapshot exists in the retained
source. Repeated cumulative snapshots add zero rather than being summed twice.
It preserves source positions, observed timestamps and prefix hashes. Rewritten
or truncated prefixes, reset/decreasing counters, malformed data and wrong session
identity do not become zero or trigger an inferred reset.

Reported counters are input, cached input, output, reasoning output and total.
Cached input is part of input, reasoning is part of output, and total equals input
plus output. Subsets are never added again to the total. Cache-write data is not a
separate credit charge or an extra token subtotal here.

Model changes are accumulated separately. Missing model labels are `(unknown)`;
token evidence can still be shown, but missing model rates prevent a full estimate.
Limit-only events without counter data supply no new measurement. With no usable
snapshot in range, token values are unavailable, not inferred zero.

Previously observed source prefixes are checked on refresh. A source that becomes
unreadable or changes retains its last-good observation as `stale`. New inaccessible
sources are `unavailable`. `partial` coverage explicitly identifies stale/missing
data and labels retained totals as last-known; fresh full estimates are withheld.
`observed` means only that all registered ranges were read, not that every related
session was found or that unsaved future usage was measured.

## Credits and rate snapshots

Observed token use, caller-reported charges and estimates are separate fields.
Remaining credit balances and rate-limit percentages are never subtracted or
presented as Activity spend. Subscription allowance consumption is not inferred
from API pricing or credit rates.

An optional `pricing` snapshot contains a `rates` model map, nonblank `source` and
UTC `captured_at`. Each model declares these nonnegative decimal-string rates:

- `input_credits_per_million`
- `cached_input_credits_per_million`
- `output_credits_per_million`

The credit equivalent uses `(input - cached) × input_rate + cached × cached_rate
+ output × output_rate`, divided by one million, per observed model. Reasoning is
already included in output. Estimates require current observations and rates for
every observed model. Arithmetic uses decimal values, not binary floating point.

Money estimates, currency conversion and monetary configuration are outside scope.
Omitting pricing retains its previous snapshot; explicit `pricing: null` clears it.

Optional `reported_spend` accepts caller-attributed Activity billing evidence:
`credits` (decimal string or null), `source` and `through` (source-session ID to observed token-position map). It is
displayed as current only while those cutoffs match all current bindings. Growing
usage makes old reported spend stale, not silently extended. The retained statement
remains audit evidence. The runtime validates structure, not billing authenticity.

Official rate and subscription semantics are described in
[OpenAI pricing guidance](https://learn.chatgpt.com/docs/pricing). A supplied rate
snapshot records its own model, date and applicable billing assumptions; this
convention does not freeze a current rate card as a framework default.

## Update, closure and partial results

An applied update holds the shared runtime lock, validates the current stable
Activity, checks existing checkpoint/report identities, reads assigned sources and
optimistically writes checkpoint then Markdown with readback. Preview performs
the calculation but writes nothing. Concurrent changes and partial persistence
return changed paths without rollback or automatic retry.

Immediately before closure, the runtime refreshes registered sources and creates
the latest usage snapshot before lifecycle writes. No sources produces an explicit
unavailable report; data unavailability is recorded rather than claimed as zero.
Invalid retained state or persistence failure stops closure, preserving actual
partial results. Missing source data retains stale/unavailable status visibly.

Usage is bounded by the latest saved token event available at refresh. The future
closure acknowledgement, later billing data and still-running/unsaved work cannot
be included. The host first resolves invocation writers under the invocation
contract, registers their known sources, and then requests closure.

Usage snapshots are not transcript/checkpoint artifacts in closure recording proof:
they are refreshed during close. Do not bind their old hashes as transcript proof.
If supplied recording artifacts change during refresh, closure stops before its
lifecycle writes. Exact-source chronicle verification remains a separate obligation.

## References

- [Runtime commands](../tools/runtime/README.md) — source/rate requests and updates.
- [Activity convention](activity_conv.md) — ownership and archival.
- [Invocation working folders](agent-invocation_conv.md) — real host evidence and writers.
- [Recording evidence](recording-evidence_conv.md) — independent closure-source proof.
