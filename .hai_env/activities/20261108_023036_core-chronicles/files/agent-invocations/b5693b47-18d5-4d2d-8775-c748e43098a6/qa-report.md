# Independent QA report

Activity: a666e07b-a570-4182-abc0-c40445046294. Invocation: b5693b47-18d5-4d2d-8775-c748e43098a6. Original implementation start supplied by host: 2026-11-07T20:31:19Z. Startup validated environment and current Activity, and loaded empty fixed instructions. Invocation manifest matches Activity, agent and invocation. Role configuration declares empty defaults. Review performed independently; no product or Activity record changes. Findings reflect the implementation inspected during this invocation and require revalidation after fixes.

## Findings

1. **High — reconciliation can remove recorded content.** In `.hai/tools/runtime/chronicles.py:195-198`, the previous prefix's line count excludes a valid final JSONL record lacking a trailing newline, although the adapter accepts it. Isolated fixture: initial synchronization records final assistant message at position 3 in such a source; after enablement revision changes, reconcile interval to end at position 2. Synchronization returns success and overwrites the transcript without the previously recorded answer. This violates preservation of recorded exchanges.

2. **High — closure cutoff can become unrecoverable after a concurrent exchange.** `.hai/tools/runtime/chronicles.py:174-180,199-203,275-278` persists a finalized binding while an Activity is still active. Isolated fixture: synchronize, finalize, then append eligible message. Source-less synchronize returns verified but keeps old cutoff; retry close returns partial and reports a new eligible exchange; resupplying the original open binding is blocked as a binding change. No supported synchronization can extend the cutoff, and the intermediate success misrepresents current coverage.

3. **Medium — independent mandatory recording cannot register core sources while feature disabled.** `.hai/tools/runtime/recording.py:30-32` always derives required from the feature flag, and its request schema provides no independent obligation. Isolated fixture with disabled feature: synchronize with explicit source returns disabled with no writes; close with `recording_requirement={enabled:false,mandatory:true}` blocks because no source was registered. The core workflow described by the synchronization procedure and runtime README is therefore unavailable for this case. Legacy supplied proof is a separate compatibility path.

4. **Low — documented synchronization request is invalid.** `.hai/procedures/synchronize-chronicles.md:17` gives a string for `provenance`; core calls `provenance` expecting an object containing source and reason. Following the example fails validation.

## Actual checks and limitations

- Adapter suite: 14 tests passed with `/usr/bin/python3 -B .hai/tools/chronicles/test_read_codex_source.py`.
- Core focused suite: 12 tests passed with `/usr/bin/python3 -B -m unittest discover -s .hai/tools/runtime/tests -p 'test_chronicles.py'`. These tests do not cover the reproduced failure cases above.
- Three defects above reproduced in isolated temporary fixtures using the project's fixture harness. No production source, transcript, checkpoint, ledger or Activity state was touched.
- Search for old manager dependency references in `.hai` and installed agent definitions, excluding test files, returned no matches.
- Reviewed source assignment, ledger, synchronization, verification and close flow. This is risk-based review, not exhaustive concurrency or proof of transcript coverage. Host owns broader regressions and all product changes.
- No usage-source identity or charge metadata was exposed to this agent by the host/runtime for this invocation; no source or costs inferred.
- Writer status: report write completed; no background writers launched. Follow-up QA is needed after fixes.

5. **Documentation scope mismatch — closed-record catch-up.** `.hai/conventions/chronicles_conv.md:7` says closed-record catch-up is permitted; `.hai/tools/runtime/recording.py:24-27` requires a sole current Activity for synchronization and verification. No supported closed-record synchronization was identified in this review. Clarify the supported scope or provide the explicit safe operation.

## Follow-up revalidation

Re-ran the three initial isolated reproductions: the unterminated final outcome is preserved and reconciliation is blocked; stale finalized active verification blocks and synchronization resumes the live assignment, records the new exchange, and then closes; mandatory synchronization while disabled records and closes with an independent obligation. The example now uses object provenance and documentation qualifies unsupported maintenance paths. Core focused suite passed 20 tests; adapter suite passed 14 tests.

New findings, on the reviewed follow-up version:

6. **High — malformed neighboring core ledger permits duplicate assignment.** `.hai/tools/runtime/chronicles.py` `check_overlaps` reads neighboring `core.json` without validating the ledger or requiring nonempty sources. Isolated reproduction: sync and close an Activity with a source; corrupt its core ledger by setting `sources` to `[]`; create another Activity and synchronize the identical assignment. Synchronization returns success, duplicating the previously recorded exchanges. Invalid neighboring metadata must block an overlap decision. Legacy source entries also require type and identity validation before treating them as unrelated.

7. **Medium — changing global enablement makes archived records unverifiable.** `chronicles.verify` compares the ledger's enablement revision with current workspace settings for closed records. Isolated reproduction: verify a newly archived Activity successfully, change feature enablement/revision, verify it again; verification blocks asking for interval synchronization, which is not available for an archived Activity. Later settings do not alter the already finalized historical assignment.

Follow-up checks use isolated temporary fixtures only. No product or Activity record writes were made. This report write is complete; no background writers are running. Findings 6–7 require revalidation after correction.

## Final targeted revalidation

Re-ran findings 6 and 7 in isolated fixtures against the revised implementation. A neighboring core ledger with an empty source list now blocks the overlapping assignment with `Invalid chronicle core sources/artifacts`; archived verification succeeds before and after a global enablement revision. Inspected the targeted strict neighboring-ledger validation and active-only revision check. These two findings are resolved in the cases reproduced. No residual high or medium findings were identified within this targeted follow-up; it was not an exhaustive new review. No product, Activity record, or Chronicle source changes were made. Report writing has ended; no background writers were launched.
