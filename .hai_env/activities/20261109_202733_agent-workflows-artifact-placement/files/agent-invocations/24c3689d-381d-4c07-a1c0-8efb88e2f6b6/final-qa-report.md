# Independent final QA report

Activity: `088c1e8e-caa9-4971-9328-cb742a4db998`. Invocation: `24c3689d-381d-4c07-a1c0-8efb88e2f6b6`.

Outcome: no remaining actionable blockers found in the reviewed source packages. The final tested bytes are identified in `source-hashes-final.json`. Live installation, commits and Activity closure were not performed by QA.

## Actual checks

- Disposable installed layout with copied compatible `.hai`, installed Business analyst peer and both target source packages: both definition validators pass.
- Final focused suites: architect 14/14 and developer 21/21 pass on Linux, `/usr/bin/python3` 3.12.3, with `-B` and invocation-local TMPDIR.
- Independent regressions: 18/18 pass. These cover valid direct/standalone-plan inputs; absent substance in Markdown bullets, fences, comments, list/inline comments and empty HTML; hardlink rejection; optional-only failed acceptance; protected-path omission; unplanned delivery paths; unknown plan sections and nonexistent phase dependencies; actual CLI CRLF/Unicode exact-byte hashing; input/shared-inode preservation.
- Earlier plan-inventory ordering reproduction now rejects; final permanent suites also cover supported optional sections, valid prior-phase dependencies and invalid references.
- Both coverage records together account for all 146 individual numbered story criteria, with no unexpected or duplicate IDs per record. Role-specific omissions are supplied by the peer record.
- Targeted `git diff --check` passes. Final source snapshot rechecked unchanged after tests.

Evidence: `final-results.json`, `*-final.log`, `independent-regressions.py`, `independent-regression-results.json`, `adversarial-results-original.json`, `adversarial-results-followup.json` and `inline-html-results.json`. Original prior-review evidence was not modified.

## Findings resolved by author and independently checked

1. Direct parser accepted required sections inside fenced examples and comment-only template bodies. Follow-up also exposed list/inline comments and empty HTML. Final parser rejects these, with permanent regressions.
2. Plan parser accepted an early File inventory, unsupported H2 sections and invalid phase dependencies. Final schema/order/reference checks reject these, with permanent regressions.
3. US-21.5 secret/PII exclusion was claimed adopted without a corresponding role instruction. Both roles now contain a Generated information rule that excludes sensitive material from generated handoffs while preserving existing ownership of exact human-source retention. This resolution was checked semantically, not through automatic secret detection.
4. Coverage language overstated structural fixtures as whole-agent demonstrations. Both records now label mechanical evidence as partial and explicitly disclose semantic/model-execution limits.

Prior QA placeholder, hardlink, optional-only acceptance, CRLF hash, omitted-protected-path and unplanned-change corrections also passed the final focused suites and relevant independent checks.

## Contract assessment and limits

Reviewed against the approved plan and supplied concept stories. Instructions preserve current authority, distinct plan/direct and normal/accelerated modes, Business analyst peer gates, host ownership of records/questions/owner work, immutable source evidence, predecessor retention, changed-input stops and truthful blocked/partial outcomes. Documentation and proportionate verification adaptations match the approved plan. A10 activation remains outside this QA result and requires host runtime evidence.

Fixture success establishes structural/helper behavior only. Semantic review does not prove actual model compliance or authenticity/completeness of host-supplied authority, inventories or results. No live role/model demonstration, real clarification UI, external-service test, product history/retention lifecycle, Windows/macOS run or OS-enforced containment test was performed. Scope reflects plan A9's stated limits.

All controlled QA writes and test side effects stayed inside this invocation; runtime chat posts used the authorized shared communication operation. No product repairs or canonical-record edits were made by QA. No background worker was launched.

## Source attribution

Current thread verified by read-only recording discovery: `01a1c1bc-bd04-7dc2-83e6-90474ff4f6f2`, response_item source `/home/hromar/.codex/sessions/2026/11/09/rollout-2026-11-09T21-15-34-01a1c1bc-bd04-7dc2-83e6-90474ff4f6f2.jsonl`. Discovery evidence is retained locally. Default event_msg had no saved user occurrence. The response_item user at physical zero-based position 7 is environment-only; position 11 is native trigger metadata without assignment content/author. Exact assignment range is therefore unavailable to this reviewer. No inherited parent identity, token value or charge was inferred.

Writer status: no further QA filesystem work planned after final chat/handoff; host may record the completed review in coverage metadata.
