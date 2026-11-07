# BL-0002 — Usage records

Implement Activity-local usage.md plus usage.json checkpoint. Usage updates read
only explicitly assigned saved Codex JSONL sources and source-position ranges;
there is no session discovery or assumption that one whole chat equals one Activity.
Cumulative token snapshots are differenced once, cached/reasoning subsets are not
added twice, source prefixes are checked for rewriting and multi-session totals
remain bounded to registered ranges. Missing data remains unavailable/stale.

The user explicitly chose labelled estimates from configured rates, otherwise
unavailable. Credits/money reported by a host remain distinct from calculated
equivalents. Credit balance and quota percentages are not charges. Decimal rates
are supplied with provenance; no dynamic pricing is fetched by runtime. Optional
money-per-credit/currency conversion is explicit and never guessed.

Add usage-update and usage-read, with previews, runtime locking and optimistic
writes. Refresh automatically before activity close; persist unavailable status
when no sources were assigned. Invalid existing usage state or partial writes stop
closure instead of being overwritten or treated as absence. Reports include the
latest observed source cutoff, known coverage and unsaved/future usage limits.

Test cumulative/deduplicated accounting, model changes, multiple sessions, interval
bounds, unavailable/stale data, unsafe targets, rate arithmetic, actual-vs-estimated
spend, idempotent refresh, partial persistence and pre-closure refresh/archive. Run
relevant core regressions and generate a live report for this Activity's root
session from the current task prompt. Do not implement a billing service, infer
subscription charges, scan unrelated sessions, migrate past Activities or commit.


Revision provenance: source: User BL-0002 request and explicit estimate-policy answer; reason: Start authorized usage-record implementation before code/tests; reason: Implement usage records against observed saved token counters and user-selected estimate policy; recorded 2026-11-06T17:28:05Z.

## Superseding scope change: tokens and credits only (2026-11-07T05:13:06Z)

User instructed: “OK, disregard money estimate - put the token and credits only”. Removed monetary report fields, estimates and currency/value-per-credit configuration. Tokens, caller-reported credits and configured-rate credit equivalents remain. Earlier EUR/list-price policy is superseded; historical records remain audit evidence only. Format 2 is token/credit-only; format-1 checkpoints with null money values remain readable and update to format 2. Non-null legacy monetary values require explicit preservation. Verification: all 54 runtime tests passed, including 19 usage tests covering omission, rejected monetary configuration and null legacy compatibility. Earlier unaffected suites had 168 passes and two Windows-specific skips; combined matrix is 224 tests, 222 passed and two skipped. No commit or Activity closure.


Revision provenance: source: User 2026-11-07 tokens-and-credits-only instruction; reason: Remove superseded monetary estimation scope; reason: Record superseding user scope and verified token/credit-only implementation; recorded 2026-11-07T05:13:06Z.
