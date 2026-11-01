# Prepare and verify

## Description

Prepare authorized release metadata, notes, and an exact-commit package, and return a reviewable candidate with verified identity and readiness evidence.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:candidate_assessment] | Reviewed version, change impact and resolved owner dependencies | Mandatory | Establish the candidate result | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:selected_version] | Human-selected or explicitly authorized recommended bundle version | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:source_export] | Full commit identity and verified exact-commit export supplied through leader for packaging | Optional | Caller or authorized context | Continue independent authorized metadata/check preparation; obtain verified export before packaging. |
| [input:destination] | Verified repository/publication destination | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:preparation_authority] | Scope authorizing metadata, notes, checks, packaging and any automation | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:automation_request] | Explicit automation scope | Optional | Caller or authorized context | Prepare no release automation. |

## Prerequisites

Verified `candidate_assessment` output from [Establish the candidate](establish-candidate.md), supplied as [input:candidate_assessment]. Selected version, preparation authority and verified destination; packaging additionally requires the verified exact-commit [input:source_export], while independent metadata/check preparation can precede it.

## Rules

- **Manifest permission:** Release-manager MUST NOT create a manifest without a selected release candidate covered by the user's permission.
- **Prior metadata removal:** Release-manager MUST NOT remove superseded metadata without identifying it and confirming that the user's candidate or upgrade request covers its removal.
- **Historical evidence:** Release-manager MUST preserve unrelated and historical release evidence during metadata changes.
- **Archive contents:** Release-manager MUST follow the package contract's allowlist, exclusions and link rules when inspecting an archive.
- **Archive path safety:** Release-manager MUST NOT traverse an unsafe source boundary during archive inspection.
- **Digest evidence:** Release-manager MUST treat an archive digest as external evidence rather than self-authentication stored inside that archive.
- **Infrastructure permission:** Release-manager MUST have permission for the specific ignore-rule or release-infrastructure changes before making them.
- **Output location:** Release-manager MUST verify current ignore status for the output location before writing release output.
- **CI availability:** Release-manager MUST place requested CI packaging logic outside `.hai_env/` so a clean checkout can use it.
- **Release triggers:** Release-manager MUST target intentional release tags rather than every commit when preparing a release workflow.
- **Publication permissions:** Release-manager MUST use narrowly scoped publication permissions when preparing automation.
- **Platform authentication:** Release-manager MAY use platform-provided authentication when appropriate for the requested automation.
- **No token assumption:** Release-manager MUST NOT require a personal token by default.

## Steps

1. Establish [input:candidate_assessment], [input:selected_version], [input:preparation_authority] and [input:destination]. Prepare authorized manifest metadata under the exact schema and notes describing changes, breaking behavior, compatibility/upgrade requirements and limitations.
2. Validate the owning state declaration and compare the manifest's environment-state entry field for field, including the supported-version array, against the same candidate source. Check version/filename/planned tag/asset identity together; record checked paths, source, values and results. If the declaration/history/owner decisions are invalid/unresolved, return that dependency before affected claims/writes.
3. For a superseded current manifest in authorized source preparation, preserve its exact bytes outside `.hai/` as historical evidence (for example `release-notes/<version>-manifest.json`) and update the historical notes' link without changing published compatibility claims. Prepare removal of only the positively identified superseded current metadata from the candidate; distinguish an unreleased tree lacking selected identity from a ready release.
4. Run applicable pre-commit checks. Pass exact metadata/source paths and required full source identity/export outcome through Leader to Git-manager; receive its actual verified commit/export before packaging. A completed ZIP is not a prerequisite for that source commit.
5. Revalidate manifest/state declaration/version identity on [input:source_export], using the exported declaration rather than installed workspace copies. If source content changes, return to the commit/export stage and regenerate the package/check evidence.
6. Obtain current output-ignore assurance through Leader before writing `dist/hai-<version>.zip`. Inspect allowlisted source for accidental secrets, unsafe paths and escaping links; if boundary/link behavior is unresolved, return that blocker instead of traversing it.
7. Build the ZIP from the exact export using the package contract's allowlist: reusable `.hai/`, one selected manifest, license and required same-commit documentation. Exclude `.hai_env/` (including this release role and Git extension), state/profiles/Activities/specifications/transcripts, `.git/`, secrets/local configuration/caches/generated/unrelated material.
8. Inspect archive paths, unpacked exclusions, documentation links and manifest; repeat declaration/identity comparisons on unpacked bytes. Compare contents with the supplied commit and record SHA-256 digest, asset path/name and source identity.
9. Read helper documentation/verify interpreter and run applicable core agent/catalogue/startup/package checks for the changed scope. Return Git-executing checks through Leader; execute filesystem/package checks here. Record actual commands/results, unrun checks and limits; resolve release-blocking failures before readiness.
10. If [input:automation_request] explicitly includes automation, verify current action versions/policy and prepare a tag-specific workflow: exact tagged checkout, identity verification, tests, build/inspection, prepared notes/assets and a single intended release path. Add only demonstrated helpers with tooling docs/checks. Otherwise retain the ready candidate for the verified connector/CLI/API path through Leader.
11. Present selected version/rationale, exact source, contract assessment, manifest, archive contents/digest, notes, checks, destination and external effects. Obtain only missing version/publication decisions through Leader or the human when direct; retain existing authority for its scope.
12. For a requested authorized publication handoff, pass [output:ready_candidate] as `ready_candidate` and [input:destination] as `publication_destination` to [Publish and reconcile](publish-and-reconcile.md), with established authority separately as `publication_authority`. After that handoff, or when no authorized publication handoff is requested, return the prepared/readiness evidence and outstanding dependencies.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:ready_candidate] | Reviewable metadata, notes, exact-commit package identity and readiness evidence | Manifest/state declaration verified in source/export/archive; digest, checks, limits and any missing publication authority reported. |

## References

- [Release policy](../conventions/release_conv.md) — bundle versioning and readiness — required for every release.
- [Contract versioning](../conventions/contract-versioning_conv.md) — references to owning compatibility rules and release dependencies — required for every release.
- [Publishing policy](../conventions/publishing_conv.md) — packaging, authority, GitHub, and recovery — required for every release.
- [Agent convention](../../../../.hai/conventions/agent_conv.md) — receiver checks, role boundaries, and references — required for all operations.
- [Git-manager](../../git-manager/SKILL.md) — Git/GitHub execution boundary — conditional when specifying a repository/service dependency; leader performs routing, do not adopt or invoke that role.
- [State convention](../../../../.hai/conventions/state_conv.md) — state-format authority and configured context — required for release contract checks; conditional when interpreting environment state.
- [State contract](../../../../.hai/agents/environment-manager/contract.json) — installed target to snapshot and verify against the candidate's own declaration — required for every release.
- [Tooling convention](../../../../.hai/conventions/tooling_conv.md) — runtime and helper requirements — conditional when executing, creating, or changing supporting Python tools.
