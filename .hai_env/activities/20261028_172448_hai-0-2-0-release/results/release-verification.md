# HAI 0.2.0 local package verification

Activity: `333a3192-1975-4575-a1ba-426910950b9a`.
Status: **prepared and verified locally; not published**.

## Source and artifact identity

- Source commit: `466e231439a27876bbbe008165360ef72f205ff4` (`Prepare HAI 0.2.0 Activity release`).
- Parent: `bd2537bbff1e8f00c15d5c0fa0ddb17e7ad93c05`.
- Verified exact-commit export supplied by git-manager: `/tmp/hai-0.2.0-source-466e231439a2-v9_8zh9q`.
- Package: `dist/hai-0.2.0.zip`.
- Archive size: **182,818 bytes**.
- Archive SHA-256: `3e53d365d1d6fcc9003ce820343f5ed4aba2e46d871ea1d4f6e619f3bd4c57df`.
- Contents: **71 regular files**, **500,499 uncompressed bytes**.
- Source/export/unpacked content fingerprint: `2692d7bb6236c98d83e7fc462227f3c6c335ab22c2dc3d8a63d3ee28bc3dd0f4` using the formula in `release-preparation.md`.

Git-manager verified every export byte against committed blobs, with modes 100644/100755. Release-manager independently matched the frozen source fingerprint before packaging, matched every archived file byte to the export, and matched the unpacked fingerprint afterward. The ZIP originated only from this source commit; a later records-only commit does not change that origin. No Git or remote operation was executed by release-manager.

## Package construction and inspection

Built with Python 3.12.3 standard-library `zipfile`, DEFLATE level 9, sorted relative entries, normalized 1980 timestamps and exported regular-file modes. Exclusive creation preserved existing artifacts. Every preexisting `dist/` regular file retained its SHA-256, including `hai-0.1.0.zip` (`dd52bf0172d4fdc4d50739b2e75fcba89ff678f2e0b931315ef1bbb56dc2809c`).

The explicit allowlist is all reusable `.hai/` files plus `LICENSE`, `README.md`, `INSTALL.md`, `release-notes/0.1.0.md`, `release-notes/0.1.0-manifest.json`, `release-notes/0.2.0.md` and `release-notes/activity-migration.md`. The archive contains no `.hai_env/`, local state/profiles/agents, Activity records, specifications, chronicles, Git metadata, caches or generated output. No symlinks, duplicate entries, parent traversal, absolute paths, Windows-style path separators, encrypted entries or nonregular files were accepted. ZIP CRC verification passed.

Strict JSON checks on both exact export and unpacked archive reject duplicate keys and nonstandard constants, validate exact manifest/declaration schemas and positive non-Boolean integers, and establish the sole current manifest `.hai/release-0.2.0.json` matches state current **2**, supported **[2]**, and specification **1** field for field. Version `0.2.0`, manifest filename and archive filename agree; `v0.2.0` is only the planned tag identity, not a created tag. The historical 0.1.0 manifest remains byte-identical with SHA-256 `7a0125d38bfa9eabb589882a50964664f403b92e2b2a5fa547f0e8bc901ea1a1`.

All **189** simple local Markdown links across **59** packaged documents resolve inside the unpacked package. This checks target existence, not network reachability or anchors. Bounded private-key, GitHub-token and AWS-access-key pattern scans found no matches; this is not a universal secret-detection claim.

## Checks executed from the unpacked archive

Using verified `/usr/bin/python3 -B` on Linux:

| Script | Passed | Skipped |
| --- | --- | --- |
| `.hai/tools/agents/test_agent_tools.py` | 57 | 0 |
| `.hai/tools/startup/test_startup_check.py` | 44 | 2 |
| `.hai/agents/specification-manager/scripts/test_audit_specification.py` | 40 | 1 |
| Total | **141** | **3** |

All suite commands exited 0. The three skips are Windows-only fixtures. Running packaged `agent_tools.py --workspace <unpacked-root> audit` also exited 0: **7 framework agents**, **0 issues**, profiles absent as expected because workspace configuration is excluded. Prior live-workspace checks covered 9 agents and valid local profiles; those workspace-only resources were not packaged.

Windows and macOS execution has not been established. Mechanical checks do not prove product implementation, semantic completeness, migration approval or automatic upgrade support. This package introduces state format 2; existing consumers still require the documented scoped migration.

## Authority and remaining steps

The user selected 0.2.0 and authorized local preparation and commits. The source commit and verified ZIP are complete. This report is local Activity evidence, excluded from the package, and may be committed separately under the current task. No tags, pushes, remote drafts, uploaded assets or publication were performed or claimed. Publication remains outside the authorized scope.
