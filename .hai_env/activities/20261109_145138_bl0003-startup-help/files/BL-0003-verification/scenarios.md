# BL-0003 verification results

Implementation authority: actual human “Implement”, root session position 1203. Scope: shared startup/Help host instructions and README. Developer followed installed Software-developer directly; separate QA /root/bl0003_qa used invocation dc79f40a-74ac-4a18-a2d3-1c0426d77c7d.

## Actual checks

| Check | Actual result |
| --- | --- |
| Startup validator regression suite | 49 run: 47 passed, 2 Windows junction checks skipped |
| Startup context regression suite | 12 passed |
| Runtime workflow regression suite | 6 passed |
| Total | 65 passed, 2 skipped, no failures |
| Actual primary startup CLI | Valid current core/Activity context, no changed_files |
| Startup nonmutation | 315 inspected core/package/settings/Activity input/state files unchanged |
| Local links and procedure structure | 29 local links resolved; required section order correct |
| Whitespace | git diff --check passed; new guide checked directly |
| Protected paths | Only .hai/start.md and new .hai/procedures/present-startup-guide.md changed, covered by human implementation instruction |
| Independent QA | All ten criteria assessed through explicit synthetic fixture responses; README conflict found, corrected, independently rechecked |

## Acceptance mapping

| Criteria | Evidence and assessment |
| --- | --- |
| AC1 | Startup and procedure explicitly wait for startup-only, including current Activity; independent fixture review passed after README correction |
| AC2 | Explicit-task summary proceeds without a menu gate; synthetic task fixture reviewed |
| AC3 | Valid registry rows provide individual choices; empty/changed/partial registries distinguished; fixture review passed |
| AC4 | Stable ID, lifecycle/steps and supplied goal or labelled excerpt; absence/invalid distinction; startup discovery regressions passed |
| AC5 | Stable identifiers and clear prose route through existing prerequisites; missing assignment/inputs requested; synthetic selection review passed |
| AC6 | Stale/unknown/numeric-without-mapping choices clarify rather than remap; fixture review passed |
| AC7 | Subsequent explicit Help refreshes overview; ordinary task mentioning help remains a task; fixture review passed |
| AC8 | Registration and operation availability remain distinct; blockers and independent capabilities retained; fixture review passed |
| AC9 | Partial startup keeps independent facts and reports actual issues; instruction review and existing regression checks passed |
| AC10 | Two-sentence introduction, compact individual entries, all agents visible, display-only effects prohibited; fixture and source review passed; actual startup read-only comparison passed |

## Limits

This implementation consists of host instructions. Synthetic candidate responses are evaluation data, not actual human exchanges, saved chronicles or proof that every host will follow the instructions. No live interactive acceptance session, real selected-agent dispatch or GUI behavior was tested. The startup nonmutation check proves the observed CLI read was read-only; it does not prove every future host interaction is read-only. Windows-only checks were skipped on Linux.

Independent report: ../agent-invocations/dc79f40a-74ac-4a18-a2d3-1c0426d77c7d/qa-report.md. Developer logs and startup snapshots: ../BL-0003-implementation/. Reviewer confirmed stopped writing after final recheck. Known root and reviewer sources are now registered and verified; no transcript was reconstructed or decrypted.

## Delivery status

Three product files delivered: .hai/start.md, .hai/procedures/present-startup-guide.md, README.md. Existing CLI/schema/state/configuration and role packages unchanged. The current Activity remains active; no commit, closure or publication was requested. BL-0003's original backlog record remains pending: the plan conditioned terminal reconciliation on authorized backlog ownership, and Backlog-manager is not installed/registered. No package installation or terminal acceptance decision was inferred from implementation.
