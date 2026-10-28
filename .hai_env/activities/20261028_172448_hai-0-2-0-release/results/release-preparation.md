# HAI 0.2.0 source preparation

Activity: `333a3192-1975-4575-a1ba-426910950b9a`.
The human explicitly selected `0.2.0` and authorized preparation and a commit.
Tags, pushes, remote drafts and publication remain outside this authorization.

## Baseline and impact

Leader supplied git-manager's live verification of published HAI 0.1.0:
<https://github.com/h111359/haide/releases/tag/v0.1.0>, published
`2026-10-28T03:51:02Z`, annotated tag
`68490524c2c4421d7d1af51312ec1debf0b3e4e0`, source
`a91baa66be3c6b62078355f2756f08a6b9652905`.
The preparation baseline is main HEAD
`bd2537bbff1e8f00c15d5c0fa0ddb17e7ad93c05`; git-manager reported matching live
remote main, an empty index, clean whitespace check, ignored `dist/` at
`.gitignore:13`, and no tracked publication workflows. Release-manager did not
execute Git or service operations.

Mandatory Activities, the Request-manager rename, Activity-local chronicles and
state format 1 to 2 break existing consumer behavior. The established experimental
0.x policy therefore warrants MINOR, and the human selected 0.2.0. Independent
specification obligations are preserved, so its target remains 1.

## Prepared files

- `.hai/release-0.2.0.json` — selected bundle and owning contract snapshot.
- `release-notes/0.2.0.md` — candidate changes, breaking effects, migration and limits.
- `README.md`, `INSTALL.md` — selected candidate identity and usage guidance.
- `release-notes/activity-migration.md` — candidate links and measured validation.
- This local evidence record, excluded from the reusable package.

Prior Activity implementation and historical-manifest relocation changes remain
part of the authorized source change set, subject to git-manager's final review.
The historical 0.1.0 manifest bytes remain unchanged: SHA-256
`7a0125d38bfa9eabb589882a50964664f403b92e2b2a5fa547f0e8bc901ea1a1`.

## Measured pre-commit checks

Executed on Linux using verified `/usr/bin/python3`, Python 3.12.3:

| Command after `/usr/bin/python3 -B` | Result |
| --- | --- |
| `.hai/tools/agents/test_agent_tools.py` | 57 passed |
| `.hai/tools/startup/test_startup_check.py` | 46 total: 44 passed, 2 Windows-only skips |
| `.hai/agents/specification-manager/scripts/test_audit_specification.py` | 41 total: 40 passed, 1 Windows-only skip |
| `.hai/tools/agents/agent_tools.py audit` | 9 registered agents, no issues, profiles valid |
| `.hai/tools/startup/startup_check.py --workspace .` | valid format-2 environment, loaded empty instructions, no issues |

All commands exited 0. The correct aggregate is **141 passed and 3 skipped**, 144
tests total. Earlier implementation reports interpreted startup's 46 total as
46 passed; the fresh run corrects that counting error. Historical 0.1.0 release
results are unaffected. Windows and macOS execution was not established.

A strict standard-library JSON check rejected duplicate keys/nonstandard constants,
validated exact schema and positive non-Boolean contract integers, and verified
the sole current manifest matches both owning declarations field for field:
state current 2, supported [2], specification 1. Candidate identity is
`0.2.0`, planned tag `v0.2.0`, archive `hai-0.2.0.zip`; no tag was created.

The planned package allowlist contains 71 regular files: complete reusable `.hai/`,
`LICENSE`, `README.md`, `INSTALL.md`, `release-notes/0.1.0.md`,
`release-notes/0.1.0-manifest.json`, `release-notes/0.2.0.md`, and
`release-notes/activity-migration.md`. It contains no symlinks, caches, forbidden
workspace/Git paths or matches for inspected private-key, GitHub-token or AWS
access-key patterns. This pattern scan is bounded evidence, not a universal
secret-detection claim. All 189 simple local Markdown links across 59 documents
resolve within the planned package; target existence was checked, not network
reachability or anchors.

The preparation content fingerprint is
`2692d7bb6236c98d83e7fc462227f3c6c335ab22c2dc3d8a63d3ee28bc3dd0f4`:
SHA-256 over sorted workspace-relative UTF-8 paths, each followed by a NUL byte
and that file's raw SHA-256 digest, concatenated. This describes the inspected
71-file source allowlist, not an archive digest or commit identity.

## Commit and package handoff

Source preparation is ready for leader's fresh pre-commit chronicle gate and
git-manager's final source/index review and authorized commit. Packaging awaits
the full commit identity and verified exact-commit export. Revalidate contracts,
allowlist, links and content fingerprint there, build the ignored ZIP, inspect the
archive and unpacked declarations, then record its digest and actual checks.
A source change requires reassessment before freezing the package. No archive,
commit, tag or publication is claimed by this pre-commit evidence.
