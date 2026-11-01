# HAI optional-agent library migration

Completed the user-authorized migration under Activity `64608fd8-1ab8-461c-9b92-f31e05d86377`, after Root's GO confirmed the implementation record and Git baseline. No Git commands, commits, pushes, publication, feature/profile changes or Activity-record writes were performed by this agent.

## Installed result

- Core `.hai/agents/` now contains and registers only `leader`, `environment-manager` and `activity-manager`.
- `hai_agents_library/agents/` holds complete golden packages for `specification-manager` (43 files), `agent-definition-manager` (8), `git-manager` (13) and `release-manager` (8). Its README is a non-executable index.
- The four installed `.hai_env/agents/` packages match their golden packages file-for-file and byte-for-byte using independent regular files, with no symlinks/hardlinks. Specification-manager and Agent-definition-manager are explicitly registered alongside existing Advisor, Git-manager and Release-manager. Existing Git/Release installations remain present.
- The canonical executable Agent-definition-manager is now `.hai_env/agents/agent-definition-manager/SKILL.md`. Source copies are data, not a third runtime origin or registration, and never a runtime fallback.

## Necessary supporting changes

Updated source/installed references, core concepts/conventions and Leader's optional-owner absence handling. Removed the unconditional core link to Specification-manager's package. Kept generic core validation code and its two-origin runtime audit unchanged. Added the definition owner's complete-package installation/update procedure and source-maintenance branches, including explicit source-to-installed registration and installed-only catalogue synchronization.

Documented manual human bootstrap when the optional definition owner is absent; no automatic installer/updater or Leader write exception was introduced. Golden source edits and installed updates remain separate explicit human choices. Updates stop for review of local or unattributed differences; an informed explicit replacement choice after full diff review can proceed without an invented provenance requirement. Version/provenance schemes remain deferred.

Updated current README/INSTALL, the current Activity migration guide's obsolete specification-owner path, helper usage examples, and specification/Git product-discovery exclusions for the library. Historical release notes/artifacts were not rewritten. The release package allowlist still ships only `.hai/` plus license/required docs; the library is repository source and is not shipped. No manifest/version/publication changes were made.

The scoped delta is 124 added files, 50 removed files and 19 changed files, primarily the package relocations/copies. Full path inventory: `/tmp/hai-library-migration-delta.json`. Before-write snapshots: `/tmp/hai-library-before`; reviewed/tested candidate: `/tmp/hai-library-stage`. Every touched existing file matched its snapshotted bytes before publication, and all final published bytes match the tested candidate. No partial-write errors occurred.

## Verification

Actual workspace core startup and full registered-agent audit both pass with no issues, eight registered agents, both catalogues valid and valid profiles. The audit verifies exact decoded catalogue-description equality. Staged source-package validation was performed through canonical installed layouts; no library path was added to execution discovery.

Requested suites passed on Linux/Python 3.12.3 in the staged installed layout, whose bytes match the published installation:

| Suite | Tests run | Passed | Skipped |
| --- | --- | --- | --- |
| Core agent tools | 73 | 73 | 0 |
| Core startup | 46 | 44 | 2 |
| Relocated specification helper | 41 | 40 | 1 |
| Git configuration helper | 10 | 10 | 0 |
| Total | 170 | 167 | 3 |

The three skips are Windows junction fixtures; Windows/macOS execution was not performed. Existing test code did not require path changes because its helpers/tests are package-relative.

Meaningful temporary-fixture checks passed:

1. A deliberately invalid source-only edit left all installed bytes unchanged and the eight-agent runtime audit valid.
2. With the fixture library removed, all four installed optional definitions validated, full startup/audit passed, and installed Git-settings and specification helpers operated successfully on fixture data.
3. A core-only fixture with no library, no optional agents and no workspace catalogue passed startup/audit with exactly the three core roles.

959 actual relative Markdown file links resolve inside the workspace (fenced examples excluded). No stale operational paths to the two outgoing core packages remain in inspected core/installed/source instructions. No installed Markdown links or Python imports point into the library. Source-management references are explicit data-operation instructions, not runtime dependencies.

Protected-byte checks passed for environment state, profiles, fixed instructions, current/historical release manifests, historical release notes, the entire installed Release-manager cleanup, its unchanged packaging convention, and core `agent_tools.py`/`startup_check.py`. Specification remains disabled; chronicles remain enabled with threshold five. Existing state schema/configuration coupling is intentionally deferred. Current manifest metadata and the previously reported new-schema compatibility consequence remain unchanged.

## Evidence and limits

- `/tmp/hai-library-migration-verification.json` — combined byte/link/suite/fixture findings.
- `/tmp/hai-library-final-startup.json` — actual workspace startup output.
- `/tmp/hai-library-final-registered_audit.json` — actual full registered audit.
- `/tmp/hai-library-independence-evidence.json` — temporary-fixture independence checks.
- `/tmp/check_hai_library_independence.py` — the one-off fixture verification used, outside the repository.

These are structural, helper, filesystem and manual semantic checks. No AI worker invocation, product specification migration, release build or publication was performed or claimed. No unresolved dependency remains for this authorized migration; Root's final review and Activity persistence can proceed.
