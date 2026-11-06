# HAI 0.3.0 release preparation

Status: source metadata and notes prepared; exact-commit package pending.

## Authority and identity

User requested “Prepare release” and explicitly selected “Use 0.3.0”. The agreed
experimental policy increments MINOR for capabilities and breaking changes.
No commit, tag, push, remote draft or public publication was requested.
Reviewed source base: c2a1e9246f21bc1f0ac30abc105fbc17757a6cb6, branch main.
Verified destination: https://github.com/h111359/haide, default branch main.
Public GitHub API inspection confirmed latest published release v0.2.0, published
2026-10-28, with hai-0.2.0.zip (182818 bytes). Local baseline commit:
466e231439a27876bbbe008165360ef72f205ff4. Authenticated write access was not checked.

## Prepared source

- .hai/release-0.3.0.json: selected version and exact environment-state snapshot.
- release-notes/0.3.0.md: capabilities, breaking changes, compatibility, migrations,
  performed checks and package limitations.
- release-notes/0.2.0-manifest.json: exact bytes preserved from the former current
  manifest. Removed only .hai/release-0.2.0.json from current metadata.
- README.md and INSTALL.md: selected candidate and pending package status.
- release-notes/0.2.0.md and release-notes/activity-migration.md: historical manifest
  links; repaired stale current-runtime introduction and removed-role reference.
  Historical compatibility targets and test claims were preserved.

## Compatibility assessment

The Python runtime replaces built-in coordinator/administration agents; optional
packages are separately installed and registered. Agent-owned external configuration
is separate from package content. Current state format is 3, recognized versions
[2, 3]; format 2 is read-only migration context requiring explicit extraction with
an installed registered compatible Specification-manager. Format 1 requires separate
ordered owner-led migration. No consumer migration was performed for this release.
Core has no remaining built-in agent packages or configuration contracts; shared
configuration tooling is included. Optional contracts remain in their separate
packages. No specification-tree compatibility target is asserted by the bundle.

## Checks

Python /usr/bin/python3, version 3.12.3, Linux:
- Startup and migration suite: 66 run, 64 passed, 2 Windows-only skipped.
- Agent tools: 75 passed.
- Configuration: 13 passed.
- Activities/recording: 16 passed.
- Runtime workflows: 6 passed.
- Total: 176 run, 174 passed, 2 skipped.
- Registered package audit: 10 agents, no issues; profiles valid.
- Strict manifest identity/schema and candidate state contract equality: passed.
- Former manifest byte preservation against HEAD: passed.
- Documentation scan outside fenced examples: 124 local links, no missing targets.
  Target existence was checked; heading anchors and remote links were not validated.
- Fresh initialization/startup from disposable core copy with no optional agents:
  passed. Replacing reusable content preserved synthetic external configuration
  bytes including unknown data and CRLF. This is a bounded fixture rehearsal.
- git diff --check: passed.
- dist/hai-0.3.0.zip is ignored by .gitignore line 13.

Raw evidence: files/release-test-results.json and files/release-preparation-checks.json.
No Windows/macOS execution or whole-product semantic certification is claimed.

## Pending exact-commit package

Release instructions require a source commit before export/package creation and
explicitly exclude commit authority from release preparation. The new manifest
and notes are uncommitted, so the old HEAD cannot authenticate a 0.3.0 archive.
Next: obtain scoped commit authority, satisfy fresh operation-specific chronicle
verification, commit reviewed release changes, export that full revision, build
and inspect dist/hai-0.3.0.zip, record SHA-256 and review readiness again.
There is no assigned explicit durable Codex source, so optional recording coverage
is unverified and no transcript was invented. Commit recording requirements remain
a separate unresolved dependency; no commit or recording exception was inferred.

Expected package: reusable .hai/, LICENSE, README.md, INSTALL.md and required
same-commit release documentation. Exclude .hai_env/, optional source library,
Git metadata, configuration, profiles, Activities, transcripts, caches and secrets.
Archive/digest/download verification is unrun; no ZIP, tag, remote draft or release
was created. Automatic push is disabled. Publication requires separate explicit
candidate-specific authority. Activity remains active; closure was not requested.


Revision provenance: source: Actual release preparation results and selected version; reason: Record reviewable candidate and precise remaining dependencies; reason: Reviewable release preparation and readiness dependencies; recorded 2026-11-05T20:17:39Z.
