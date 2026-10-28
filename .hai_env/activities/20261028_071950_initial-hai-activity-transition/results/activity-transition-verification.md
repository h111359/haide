# Initial Activity transition verification

Recorded 2026-10-28T06:53:23Z by Activity-manager for Activity `5b79aa45-bbdb-4039-84ea-a09e7d3b6760`. This report concerns the current history-import and framework transition; it does not assert completion of every historical development task.

## History and record preservation

Activity-manager independently read the [import evidence](chronicles-import.md) and [manifest](../files/chronicles-import.tsv), then verified all 37 imported files against the recorded names, byte counts and SHA-256 values: **436,467 bytes**, every hash matched. The old `.hai_env/chronicles` path is absent. Leader additionally supplied Git-manager confirmation that all originals match Git HEAD bytes.

The imported `20261018_0734.md` lacks a source ID and remains unchanged. Direct header inspection confirmed that `20261021_082624.md` has session ID `01a15cec-ca98-77a1-bc90-f1d59cf1ede2` after a UTF-8 BOM; an initially inconsistent derived manifest source-ID field was referred to chronicles-manager for correction. Transcript preservation checks passed independently of that metadata correction.

The [current-session segment](../chronicles/20261028_0738_segment-01.md) identifies source `01a18104-220b-7593-a165-8c446248f746`, saved at `/home/hromar/.codex/sessions/2026/10/28/rollout-2026-10-28T07-38-14-01a18104-220b-7593-a165-8c446248f746.jsonl`, with original start `2026-10-28T05:38:14.170Z`. Its inspected metadata records eight completed exchanges through saved response-item 501. Chronicles-manager’s exact-source verification was supplied by leader. Prompt 508 awaits its final response and later source-backed synchronization; this ordinary pending exchange does not block the completed transition.

The exact initial human input and original Activity creation/implementation timestamps remain preserved. The [format-1 provenance snapshot](../files/environment-state-format1.json) remains exact, SHA-256 `8e8182edee1fd0cf03467ef760499c17a937a55a762ffe946fd283381604e94e`.

## Supplied implementation and verification evidence

The following results were supplied by leader from the responsible owners; Activity-manager records them without claiming to have rerun their tests or performed their Git/configuration work:

- Environment format 2 validation passed. Mandatory configurable `activities.location` is valid; specifications remain disabled at their old location, chronicles remain enabled with Activity-local storage, Git/GitHub remain enabled, and automatic push remains disabled.
- `activity-manager` replaces `request-manager`, with its concept/convention and the coordinated framework changes for mandatory Activities, independent optional steps, completion without implementation, revision history, segmented transcripts and leader-assigned boundaries.
- Environment checks: **46 passed, 2 Windows-only skipped**. Agent checks: **57 passed**. Specification checks: **40 passed, 1 Windows-only skipped**. Total: **143 passed, 3 skipped**.
- Registered-definition audit: **9 definitions, 0 issues**; model profiles valid. Local-target existence review: **180 links across 59 documents**, no missing targets; this was an existence check rather than proof of all semantic references.
- Independent semantic review found no remaining new findings after timestamp/status atomicity, pre-read child safety and prior-segment coverage fixes.
- Final read-only Git verification retained branch `main`, HEAD `bd2537bbff1e8f00c15d5c0fa0ddb17e7ad93c05`, and the originally empty index. Tracked and authored-new-file whitespace checks were clean; no unexpected edits, commit or push were reported.

The immutable historical release manifest was moved to `release-notes/0.1.0-manifest.json`; Activity-manager independently verified SHA-256 `7a0125d38bfa9eabb589882a50964664f403b92e2b2a5fa547f0e8bc901ea1a1`. The framework source is unreleased: no new version, package or publication is claimed. The release-notes owner is updating its final test evidence separately.

## Scope and lifecycle

Implementation and verification completion applies only to this authorized transition, supported by the evidence above. Earlier historical steps are not inferred complete. The Activity stays **active**, with null `closed_at` and `outcome`; closure requires the user’s later instruction. No closure artifact or archive rename is performed.

## Final record check — 2026-10-28T06:54:05Z

Chronicles-manager corrected the BOM-affected derived source-ID column. Activity-manager read back the corrected manifest and verified 37 files, 36 unique identified source sessions and one unknown source (`20261018_0734.md`), with every imported file still matching its recorded bytes/hash. Leader additionally supplied the final startup-helper result: exit 0, `ok: true`, format 2 valid, current Activity available, profiles/catalogues valid, and no issues. The release-notes owner has updated final evidence to 143 passed and 3 Windows-only skips. The metadata inconsistency is resolved. Implementation and verification are completed for this scoped transition; the sole remaining recording follow-up is the current exchange after its final outcome exists in saved source.
