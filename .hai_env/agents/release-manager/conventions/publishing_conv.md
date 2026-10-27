# HAI packaging and publication policy

## Ownership and source sequence

Release-manager owns version policy, metadata, notes, package preparation,
readiness checks, and final product review. Git-manager owns all Git/GitHub
execution, including inspection, commits, exports, tags, pushes, releases and
assets. Return dependencies to leader; neither specialist calls the other.

Use this order to avoid requiring a package before its source is committed:

1. Obtain repository and published-history evidence through leader; prepare source
   metadata/notes and run available pre-commit checks.
2. Return exact candidate paths and required source evidence to leader. With
   appropriate authority and the shared pre-commit chronicle gate satisfied,
   git-manager creates the source commit and supplies its
   full identity and a verified source export of the intended tracked paths.
3. Build and inspect the ZIP from that exact export; run release checks and record
   the asset digest. A source change requires a new commit/export and new package.
4. Return the frozen ready candidate through leader for authorized Git/GitHub
   publication. Review returned publication evidence against product requirements.

Do not execute Git locally to recover missing status, history, ignore information,
or exports. Ask leader for that evidence. Local tags alone do not establish actual
published history. Packaging and filesystem validation can continue independently
where their required evidence is already available.

## Package contents and identity

Build `dist/hai-<version>.zip` from the verified exact-commit export, not a working-tree
snapshot. `dist/` is already ignored in this repository; obtain current ignore
assurance through leader before writing output. Ignore-rule or other infrastructure
changes require authorized scope. Do not discard or package unrelated local work.

Use an explicit package allowlist:

- The reusable `.hai/` tree, with exactly one agreed versioned release manifest.
- The repository license and required installation/use documentation from that
  same commit, with working relative references.

Exclude `.hai_env/` and workspace agents, state, profiles, requests, specifications
and chronicles; also exclude `.git/`, credentials, secrets, local configuration,
caches, generated output and unrelated workspace material. Release-manager is
workspace tooling and is excluded; framework git-manager is included in `.hai/`.
Inspect allowlisted files for accidental secrets, unsafe paths and escaping links.
Reject unsafe archive entries or unresolved link behavior rather than traversing
outside the verified source boundary.

Inspect archive paths and the unpacked manifest, exclusions and documentation
links. Verify correspondence to the supplied source commit and record a SHA-256
digest. Source version, manifest filename/content, intended tag, release identity
and asset name must agree. An archive's digest is external evidence, not a field
that can authenticate that same archive from inside itself.

## Authority and publication handoff

Preparation does not imply authority to commit, push tags, write remote drafts or
publish publicly. Pass established authority through leader; avoid repeated requests
when it already covers the action and candidate. Before any missing final publication
permission is requested, finish authorized preparation and present version, source,
checks, compatibility and upgrade assessment, notes, asset path/name/digest/contents,
destination and external effects. A public tag push may trigger publication.

The frozen handoff includes those artifacts and evidence plus the selected draft,
prerelease or public state and intended automation/local path. Git-manager rechecks
actual repository/service state and executes only within authority. Missing access
is a dependency, not permission to alter repository security. Material candidate
changes require renewed readiness assessment and authority-scope review.

Agent-executed branch/tag pushes, including tag-triggered publication, require
`integrations.git.auto_push.enabled: true`. When off or invalid, return the required
manual push through leader and keep publication pending until verified remote refs
exist. Authorized non-push release APIs may use an already available remote target;
do not recreate missing remote commits/refs through an API or connector workaround.
The setting does not authorize publication or unsolicited pushes after commits.

## Automation and local alternatives

When separately requested, prepare release-specific workflow files for intentional
`v<version>` tag pushes. They should check out the exact tagged commit, verify release
identity, validate/test, build/inspect the ZIP, then create the release with prepared
notes and assets. Do not release on every commit. Git-manager handles repository
and GitHub execution or service configuration through leader.

Use narrowly scoped publication permissions and platform-provided authentication
where appropriate; do not require a personal token by default. Verify current action
versions and repository policy at implementation time. Packaging logic required by
CI must be available outside `.hai_env/`, which a clean CI checkout may not supply.
Add helpers only for demonstrated needs, with tooling documentation and checks.
Agent creation alone creates no workflows or helpers.

When automation is absent or unsuitable, return the same ready candidate through
leader for git-manager's verified connector/CLI/API publication path. Drafts are
remote writes and remain drafts until authorized publication. Git-manager inspects
tag-trigger behavior and chooses a single execution path to avoid CI/local races.

## Final verification and failures

Review returned actual workflow results, release URL/state, tag and full commit,
notes, asset name/bytes/digest and download evidence. Inspect supplied downloaded
assets with filesystem tools when available. Request missing service evidence through
leader; starting a workflow or upload is not completion.

For failures, preserve package/check evidence and return product-level blockers.
Git-manager owns inspection and recovery of partial repository/service operations.
Do not prescribe blind retries, deletion, tag movement or asset replacement. Report
prepared, draft, published, failed and unverified states accurately, without promises
of unsupported background monitoring.
