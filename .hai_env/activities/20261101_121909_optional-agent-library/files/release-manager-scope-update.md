# Release-manager scope cleanup

Completed the authorized definition cleanup under Activity `64608fd8-1ab8-461c-9b92-f31e05d86377`, after Root confirmed the first implementation marker was recorded. No library migration, package installation, registration addition/removal, Git operation, commit, push or release was performed.

## Result

Release-manager now owns HAI core/bundle SemVer, release metadata/packaging/readiness/publication review and environment-state compatibility checks. Specification content, specification compatibility tracking, library versioning and individual-agent versioning are explicitly outside scope. Removed specification ownership/dependency links, the specification term/marker definition, transition-ledger/tree-migration requirements, specification validation steps and specification fields from new-candidate manifest schema instructions. The existing package allowlist/exclusions remain unchanged.

Changed eight files:

- `.hai_env/agents/release-manager/SKILL.md`
- `.hai_env/agents/release-manager/concepts/release.md`
- `.hai_env/agents/release-manager/conventions/contract-versioning_conv.md`
- `.hai_env/agents/release-manager/conventions/release_conv.md`
- `.hai_env/agents/release-manager/procedures/establish-candidate.md`
- `.hai_env/agents/release-manager/procedures/prepare-and-verify.md`
- `.hai_env/agents/release-manager/procedures/publish-and-reconcile.md`
- `.hai_env/agents/catalogue.md` — synchronized the existing Release-manager description only; no registration change.

## Verification

Passed on Python 3.12.3 (`/usr/bin/python3`):

`/usr/bin/python3 -B .hai/tools/agents/agent_tools.py validate --definition .hai_env/agents/release-manager/SKILL.md`

Scoped follow-up checks passed: exact decoded catalogue-description equality and canonical row link; unrelated catalogue bytes unchanged; 54 relative Markdown file links resolve inside the workspace; the manifest example parses as JSON and has only `contracts.environment_state`; only the eight authorized files differ from their snapshots. Remaining specification mentions are limited to the explicit out-of-scope statement and preserved package-content exclusions. Manual semantic review retained core state-format ownership, Git/Leader handoffs, authority, exact-source evidence, immutability and preservation constraints.

Byte comparisons confirmed unchanged: `.hai/release-0.2.0.json`, historical `release-notes/0.1.0-manifest.json`, Specification-manager's contract, environment state, profiles, fixed instructions and `conventions/publishing_conv.md`. The unchanged allowlist still includes `.hai/` plus license/docs; no library was added.

Verification evidence: `/tmp/hai-release-manager-scope-verification.json`. Pre-change snapshots: `/tmp/hai-release-manager-scope-before`.

## Existing-manifest consequence and limits

The existing `.hai/release-0.2.0.json` still contains `contracts.specification`. It would not match the narrowed schema if reused as a newly prepared candidate manifest. Its bytes and historical release evidence were deliberately preserved. This cleanup neither authorizes manifest conversion nor retroactively rewrites a release's recorded policy. A future candidate-preparation task must address its actual metadata under the applicable authority before claiming readiness.

No test suites were run because this changed prose/contracts, not helper implementations. No broad registered-agent audit, package build, release-readiness assessment or publication check was run; none is claimed. There are no unresolved dependencies for this scoped definition cleanup. The broader library proposal remains on hold.
