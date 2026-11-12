# Approved portability implementation plan

Implement the user-approved proposal based on critical review of .sandbox/temp.md.

1. Separate native filesystem paths from canonical forward-slash workspace-relative strings across discovery, lifecycle, chronicles, packages, storage reports and consumers.
2. Preserve strict external-input validation, align portable name rules, native case handling and Python 3.11-compatible reparse protection.
3. Keep source representation independent from OS, preserve foreign absolute historical metadata without attempting relocation, and retain selected/related recording integrity checks.
4. Fix native Windows failures found by QA: binary raw writes for chat/migration and UTC naming without timezone-data dependencies. Preserve historical filenames/bytes.
5. Expose observed OS/Python execution context and update invocation, path and recording guidance.
6. Add native Windows/Linux Python 3.11/3.14 CI and workspace-contained regression runner; retain actual native coverage limits.
7. Independent plan QA, implementation QA and behavior QA must complete; resolve their findings before handoff.

Acceptance: canonical paths round-trip through public CLI operations; actual Windows lifecycle/recording/packages pass, unsafe aliases remain rejected, partial results retain evidence, and no unrun Linux/CI result is claimed. Changes remain local for review; do not close this Activity or publish.


Revision provenance: source: Approved proposal and actual independent QA returns; reason: Record plan, evidence and honest platform limits; reason: Persist approved implementation scope and acceptance gates; recorded 2026-11-12T09:11:48Z.
