# Artifact placement correction

Implemented the current user request to make artifact placement a general HAI principle and move the architect/developer verification folders into this Activity.

## General rule and workflow

`.hai/conventions/artifact-placement_conv.md` defines purpose, owner, lifetime and canonical destination for all HAI work, including software, flows, documents, research and managed outputs. Requested deliverables and established retention contracts remain authoritative. Working material and per-run evidence stay with the Activity/invocation unless explicitly designated otherwise. Reusable tests/fixtures remain valid deliverables; filename/folder-name blacklists and automatic cleanup are not introduced.

Startup, shared agent execution/authoring/package review, Activity storage, framework layout, tooling and the HAI concept reference this rule. Existing required agent-convention references apply it to authoring roles without replacing their locally distinct definitions. Source and installed Solution architect/Software developer explicitly apply it during planning, new-artifact creation and final delivery review. No executable code or document-validator schema changed; this is a behavioral instruction contract, not an automatic semantic filesystem classifier.

## Exact evidence relocation

Four whole directories were moved with exclusive rename: source and installed `verification/` for each selected role. Their exact contents are retained under `files/verification/relocated-agent-evidence/{source,installed}/{solution-architect,software-developer}/verification/` in this Activity. `relocation-manifest.json` records origin, destination, SHA-256 and completed status for each move. All four hashes were verified after movement. No scope was inferred to move unrelated evidence or alter historical backups.

Fresh runtime replacements applied the reviewed role-instruction changes after those explicitly authorized moves. Live/source package contents match. The target source and installed packages have no verification folders or references to those folders. Original runtime backups remain retained under runtime ownership.

## Checks and actual limits

- Fresh workspace-local staged packages validate with the compatible shared core and Business analyst peer.
- Existing focused suites pass: architect 14 tests and developer 21 tests (35 total), without the removed folders.
- Installed definitions and selected empty configurations validate; post-update startup is valid with no issues.
- Shared/source/live supporting links and scoped whitespace checks pass.
- Relocation manifests prove unchanged evidence bytes; baseline inspection shows only authorized shared documents, selected agent documents/folder moves and runtime backups changed among protected paths.
- Settings/catalogue bytes remain unchanged; local Agent Instructions remains empty. Unrelated Agent-definition-manager origin-specific reference differences were preserved.

This correction changes instructions and artifact placement only, not executable implementation; no new code tests or separate model review were claimed. Prior independent QA remains evidence for unchanged helpers, not a review of this new instruction text. No live model/UI compliance, cross-platform execution or automatic semantic enforcement is demonstrated.

Root recording uses its existing source assignment. Earlier participant-source boundary limitations remain unchanged; no full-participant transcript/usage claim is made. No commit, publication or Activity closure performed.
