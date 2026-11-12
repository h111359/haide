# Final Windows/Linux portability verification

Implementation completed under the approved proposal. No release, push or commit performed.

## Actual aggregate regression result

Native Windows, Python 3.14.7: all six core suites exit 0. 301 tests discovered, 275 passed, 26 skipped for reported unavailable/platform-specific capabilities. Final output: verification/all-core-final.txt. Suites: runtime 117; startup 66; activity 16; source adapter 14; configuration 13; agents 75.

## Independent QA

- Plan review: 3b204810-9b3e-417e-aaa8-8201d3def598/plan-qa.md. Chat binary-write defect found, fixed and independently retested; no unresolved plan blocker.
- Implementation review: d895948e-15a4-47a4-b371-4f1b719ed166/implementation-qa.md and reviewed-hashes.json. 46 independent native safety checks, portability suite and targeted final regressions passed. Timezone dependency, reserved aliases and Python 3.11 reparse pruning findings fixed. Final migration reparse delta approved.
- Behavior review: f830df6c-2484-4608-a682-5a288f40ead5/behavior-qa.md. 61 public CLI checks across event_msg/response_item plus 18 safety probes passed, including actual Windows junction rejection and collision preservation. Full lifecycle, package install, recording verification and enabled closure verified in isolated fixtures.

All three reviewers confirmed ended writes. Their scratch remains under their own invocation folders; disposable fixture folders are ignored. Original partial chat evidence and historical records retained.

## Live workspace

Activity recording successfully bound using inspected actual first work prompt at saved source position 145 in response_item representation. Actual Activity updates and usage registration succeed. Core OS/Python context is available in startup. Final recording refresh and read-only verification performed by host at handoff.

## Limits

Native Linux, Python 3.11 and remote CI execution were not available/performed. WSL probe reports not installed. Added Windows/Linux x Python 3.11/3.14 CI matrix; its existence is not a claimed successful run. No runtime/dependency installed. Existing missing foreign session sources and previously transformed historical hashes are not repaired or waived. Unrelated historical assignment metadata can be inspected without validating unrelated transcript contents; selected and related records retain full verification.

## User-visible behavior

Workspace-relative results use canonical forward slashes; native absolute recording sources remain separate. Strict portable components and reparse safety apply. Binary chat/migration writes preserve exact bytes. New transcript names use UTC without timezone-data dependencies; prior names remain unchanged. Startup reports actual OS/Python separately from recording readiness. See .hai/tools/runtime/PORTABILITY.md.
