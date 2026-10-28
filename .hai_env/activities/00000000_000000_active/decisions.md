# Release decisions

## 2026-10-28T07:23:19Z — Version selection completed

Source: explicit human answer supplied by leader.

Question: “Use version 0.2.0 for the Activity release, following the established policy that breaking changes increment MINOR during 0.x?”

Answer: “Use 0.2.0”

Decision: prepare version **0.2.0**. This completes the version-selection clarification only; it does not assert release preparation, verification, packaging or commit completion.

Leader supplied the verified published baseline [v0.1.0](https://github.com/h111359/haide/releases/tag/v0.1.0), source commit `a91baa66be3c6b62078355f2756f08a6b9652905`. Main and live remote HEAD remain `bd2537bbff1e8f00c15d5c0fa0ddb17e7ad93c05`, with an empty index. `dist` is ignored and no tracked CI was found. These are supplied Git-manager findings, not Git operations performed by Activity-manager.

The user authorized commit and local release preparation/package. No push, publication or tags are authorized in this task. The predecessor Activity is closed completed; all 38 then-existing transcript files were verified unchanged before delayed source catch-up.

## 2026-10-28T07:23:46Z — Attributable test-count correction supplement

Author: Activity-manager. Source: leader’s supplied fresh release-owner test results. Reason: correct the earlier aggregate’s arithmetic without rewriting its historical assertions or rerunning tests.

The environment/startup suite ran **46 total**, with **2 skipped**, hence **44 passed**. The specification suite ran **41 total**, with **1 skipped**, hence **40 passed**. The agent suite had **57 passed**. Correct combined result: **141 passed, 3 skipped, 144 total**, all commands exiting 0. All three skips are Windows-only. The earlier “143 passed” aggregate incorrectly treated the environment suite’s total count as its passing count; this is a reporting correction, not a newly discovered test failure.

This dated evidence supplements the earlier log, outcome and transition-verification report. Their original assertions remain preserved. The initial Activity stays closed completed with its original identity and timestamps; no historical transcript is edited or substantive work resumed under it. The release Activity remains active.
