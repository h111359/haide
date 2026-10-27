# HAI packaging and publication policy

## Source and package

Identify the intended repository and remote from verified context. Inspect actual
published GitHub releases and remote tags; local tags alone are incomplete evidence.
Verify relevant tool capabilities and authentication without printing credentials.
Use current official documentation or installed help for command details when needed.

Build `dist/hai-<version>.zip` from the exact recorded release commit, not an
uncommitted working-tree snapshot. `dist/` is already ignored in this repository;
verify that it remains so before writing output. Changes to ignore rules or other
release infrastructure require their own authorized scope. Do not include local
uncommitted work or discard it to obtain a clean source.

Use an explicit package allowlist:

- The reusable `.hai/` tree from the candidate commit, with exactly one agreed
  versioned release manifest.
- The repository license and installation/use documentation needed for the bundle,
  selected from that same commit and checked for working relative references.

Exclude `.hai_env/` and its workspace agents, state, profiles, requests,
specifications, and chronicles; also exclude `.git/`, credentials and secret files,
local configuration, caches, generated output, and unrelated workspace material.
The release-manager itself is workspace tooling and is not distributed in this
framework-only bundle. An allowlisted tree still needs inspection for accidental
secrets, unsafe paths, and escaping links. Reject unsafe archive entries or
unresolved link behavior instead of traversing outside the source boundary.

Inspect archive member paths and the unpacked manifest, check exclusions and
necessary documentation links, and verify the package corresponds to the recorded
commit. Record a SHA-256 asset digest. The source version, manifest filename and
content, tag, release identity, and asset name must agree. Do not put an archive's
own digest inside that archive and assume it can authenticate itself.

## Authority and review

Preparing a candidate does not imply authority to commit, create or push tags,
write remote drafts, or publish publicly. Determine each action's established
scope from the handoff and conversation. Do not request redundant confirmation
when explicit authority already covers the action and candidate.

Before asking for any missing final publication permission, finish authorized
preparation and present the concrete version, source commit, checks, contract and
upgrade assessment, notes, asset name/digest/contents, destination, and external
effects. A public tag push can trigger release automation, so approval must precede
that trigger. If a candidate materially changes, resolve whether existing authority
still covers it before publishing. Missing tool permissions or credentials are
specific dependencies, not permission to change repository security settings.

## Recommended automation

When separately requested, prepare `.github/workflows/release.yml` for intentional
`v<version>` tag pushes. It should check out the exact tagged commit, verify release
identity, run applicable validation and tests, build and inspect the ZIP, then
create the GitHub release and attach the asset and prepared notes. It must not
release on every commit. Use narrowly scoped `contents: write` for the publication
job and the platform-provided token; do not require a personal token by default.
Choose and verify current action versions and repository settings when implementing
it rather than freezing unverified examples into this policy.

Keep packaging logic usable outside `.hai_env/` if automation needs to run it:
workspace agent files are excluded from the bundle and may not be available in a
CI checkout. Add helpers only for demonstrated reuse or validation needs, with
usage documentation and appropriate tests under the tooling convention. Agent
creation alone does not create workflows, helpers, or other release infrastructure.

## Local publication and drafts

Support a local Git/GitHub CLI path when automation is absent or unsuitable.
Verify the intended tag points to the exact candidate commit, push it only with
applicable authority, and create the release with the verified tag, prepared notes,
and inspected ZIP. For GitHub CLI, `gh release create` supports `--verify-tag` and
`--notes-file`; a requested draft uses `--draft`. Check installed help and current
official behavior at execution time. `--verify-tag` checks remote existence; also
independently verify the tag's commit because existence is not source agreement.
Do not let a CLI implicitly create a tag from an unspecified branch.

Drafts remain remote writes and are not public-release completion. Publishing an
existing draft requires public-publication authority. If tag automation exists,
inspect its trigger behavior before any push and choose a single publication path
to avoid races between local creation and CI. Do not enable a workflow or push a
trigger merely to test whether it publishes.

## Verification and partial failure

Observe actual workflow/job state or local command results; starting a process is
not completion. After publication, verify the release URL, draft/prerelease status,
remote tag and peeled commit, notes, asset name and bytes/digest, and manifest
agreement. Download or otherwise verify the published asset when available rather
than assuming a successful upload produced the intended bytes. Report unavailable
network or repository checks and distinguish a draft from a published release.

If validation, packaging, upload, or release creation fails, stop dependent actions.
Inspect existing remote tag, release, and assets before proposing recovery. Preserve
local evidence and partial remote state; report what succeeded and what remains.
Never force-move a published tag, silently overwrite an asset, delete a release, or
retry publication blindly. Resume only within established authority and after the
failure's cause and current remote state are understood. Do not promise background
monitoring without an actual running, observable mechanism.
