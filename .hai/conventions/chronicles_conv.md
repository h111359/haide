# Chronicles

Core owns source synchronization, exact transcript segments, checkpoints and fresh coverage verification. The host supplies the stable Activity, explicit authorized source paths, original session identities, exact assignment ranges, enablement intervals and attributable provenance; core never discovers sessions or guesses attribution. The host serializes recording and Activity writers and resolves ambiguous or overlapping assignments. No separate manager, agent profile or library package is required.

Apply validated recording settings and mandatory workspace instructions. Disabled recording without an independent obligation creates no transcript directory, segment or checkpoint. Enabling covers subsequent eligible exchanges; earlier off periods require explicit historical-import authority. Configuration changes preserve existing files, gaps and coverage. Host scheduling uses the prompt threshold for ordinary batches, and must synchronize on cadence and synchronously before closure regardless of threshold. Do not promise background continuation without host support; catch up on the next active turn when necessary.

Use only completed, durable saved source for exchange text, except the explicit [mandatory pre-delivery procedure](../procedures/mandatory-pre-delivery-recording.md). Preserve human prompts, clarification exchanges and delivered final outcomes verbatim and in source order. Exclude tool calls, internal instructions, environment metadata and progress. Keep source identities, boundaries and verified coverage separate from exact text. Never reconstruct missing messages, deduplicate equal text, record one occurrence in overlapping Activities or segments, claim a proposed operation was completed, or treat a prepared outcome as already saved. Retain historical bytes and optional labels, and do not reject an older label alone. Closed-record catch-up is permitted only for assigned completed old-source exchanges and does not reopen the Activity or authorize new substantive work.

The ordinary synchronization command updates only the current active Activity.
Read-only verification also accepts archived Activities. Closed-record catch-up,
legacy adoption and prepared-text reconciliation remain explicit core maintenance
procedures; these commands do not implement those mutations. Report that limit
before dependent work rather than claiming catch-up or appending around the ledger.
Pending/prepared or interrupted checkpoint state blocks ordinary synchronization
until explicitly reconciled; it is never erased by a later successful batch.

Before reads and again before writes, validate containment, target types, safe direct-child store consistency and the selected Activity identity; load only relevant assigned records and artifacts rather than recursively reading unrelated history. Use sole mutation ownership, recheck inspected source, assignment, coverage and target contents immediately before writes, exclusively create new directories and segments, and never overwrite another source or segment. Preserve unrelated material. On changed inputs, gaps, divergence, unsafe paths, ambiguous coverage or partial failure stop affected work, preserve and report actual partial results; never silently truncate, repair, retry or roll back. Recheck exact contents and occurrence coverage after writes. Source hashes and scheduling cursors alone do not establish coverage.

The [transcript convention](transcript-segment_conv.md) retains checkpoint format 1. Core maintains a supplemental `chronicles/core.json` binding/hash ledger; existing checkpoint or segments lacking that ledger require explicit adoption, and unsupported, malformed or unknown legacy state blocks rather than being rewritten implicitly. See [Codex source convention](codex-source_conv.md) for supported representations and immutable-prefix safeguards.

An actual enable/disable change through environment configuration increments the
internal `features.chronicles.enablement_revision` (absent means zero). Cadence-only
changes do not increment it. After an enablement transition, synchronization
requires explicit updated enabled intervals for every already registered source,
with attributable boundaries and no removal of previously recorded exchanges.
It never assumes that an intervening disabled period was eligible. Unchanged
identity/path/assignment bounds remain required; only interval reconciliation is
permitted for that transition. Unknown boundaries block dependent recording.

Enabled or independently mandatory recording must be synchronized and verified afresh through the completed closure-request cutoff before Activity closure. Core close synchronizes registered sources and validates exact evidence; missing, pending, divergent or ambiguous required source, outstanding writes or coverage gaps block close. Closure synchronization finalizes a live source assignment end at the completed eligible closure cutoff so later Activity source ranges do not overlap. The future undelivered acknowledgement is outside that cutoff. Disabled/no-obligation closure requires no recording writes or source. See [recording evidence](recording-evidence_conv.md), [synchronize](../procedures/synchronize-chronicles.md) and [verify](../procedures/verify-chronicles.md).
