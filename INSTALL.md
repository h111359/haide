# Installing and upgrading HAI

HAI is a prototype framework of agent instructions and Python validation tools.
It is not a Python package or a service that starts when a ZIP is extracted.

The current source is **unreleased development beyond the recorded 0.2.0 candidate**,
with current environment state format **3** and format **2** recognized as read-only
specification-migration context. The immutable **0.1.0** bundle supports format **1** and retains
its original behavior. Its [release notes](release-notes/0.1.0.md) and
[preserved manifest](release-notes/0.1.0-manifest.json) describe that bundle; they
do not identify this source as a published release. The selected candidate has
[0.2.0 notes](release-notes/0.2.0.md) and a
[current manifest](.hai/release-0.2.0.json); publication remains pending.

## Requirements

- An AI coding environment that reads workspace files and follows
  [startup instructions](.hai/start.md). Runtime spawning, model/effort support and
  tools depend on that environment; HAI does not install or guarantee them.
- Python 3.11 or newer for standard-library validation helpers. Verify an available
  interpreter; an unavailable launcher does not establish that Python is absent.
- Git/GitHub access only for chosen enabled operations. GitHub CLI is unnecessary
  when a sufficient connector or other supported transport is available.

## Historical 0.1.0 installation

1. Inspect `hai-0.1.0.zip` in a temporary directory. It contains reusable `.hai/`,
   license, package-root documentation and release notes, with its original manifest.
2. Copy `.hai/` to the intended workspace. Do not overwrite a project's README or
   license with package-root files. Retain the MIT license with the framework, for
   example at `.hai/LICENSE`, and retain extracted documentation separately.
3. Ask the coding environment to read the installed `.hai/start.md`. Follow that
   bundle's instructions: it initializes safely absent format-1 state and fixed
   instructions, then offers optional requests, specification and global chronicles.
   These are historical 0.1.0 capabilities, not Activity development defaults.
4. Configure supported model profiles and chosen integrations/features. Automated
   push is a separate opt-in requiring verified readiness. Packages exclude this
   repository's local environment, profiles, credentials, workspace agents and history.

## Recorded 0.2.0 candidate

Inspect the candidate source or its exact-commit package in a temporary directory.
Verify the package's current manifest declares version `0.2.0`, environment state
`2` with support `[2]`, and specification compatibility `1`. Preserve the MIT license
and avoid overwriting project-root documentation. Copy the complete reusable
`.hai/` tree and ask the coding environment to read its `.hai/start.md`.

Safely absent state initializes at format 2 with mandatory fixed instructions and
`activities.location`, default `.hai_env/activities`. Specification and chronicles
start off. Activity records are created when meaningful substantive work begins;
startup and a new chat alone create none. Existing current work resumes through
the candidate's historical record owner. Current-source ownership is described below. Optional chat setup configures specification, recording and
supported model profiles; there is no Activity switch or global transcript location.
Git/GitHub and automated push retain their independent setup gates.

For a read-only check, use a verified Python 3.11+ executable with
`-B .hai/tools/startup/startup_check.py --workspace .`. Read the
[helper instructions](.hai/tools/startup/README.md) for output and limits. The
helper validates configuration without discovering Activity records or writing files.

## Current source: specification-owned settings

Current core defaults use format 3 with mandatory Activity location and central
chronicles. Specification-manager's contract format 2 supplies Boolean enabled and
a safe workspace-relative directory location; its saved file remains config format
1. Missing files default disabled at `.hai_env/specifications`, without creating
that directory. Startup reports only the registered installed owner's separate
status and requires no optional owner for core validity.

For an existing format-2 workspace, use Environment-manager's explicit read-only
extraction review followed by authorized apply; preserve complete specification
settings in `.hai_env/config/agents/specification-manager.json`, verify readback,
then remove only the old feature entry and set state 3. Retain chronicles exactly.
The helper requires the installed registered owner contract for this conversion;
it never executes a library fallback. Ordinary specification setup goes to that
owner, independently of core/Activity assurance and tree compatibility. Copying a
package does not migrate values, enable work or adopt a tree. Preserved candidate
manifests remain release evidence; later development needs its own authorized
release assessment before packaging/publication claims.

## Existing installations and migration

Back up framework, environment and configured data before changing an installation.
Inspect the source or bundle contract targets. Replace reusable `.hai/` as a whole;
avoid overlays leaving stale role folders or manifests. Preserve `.hai_env/`, all
configured record/specification data and product files. A framework copy is not a
state, record or transcript migration.

The recorded 0.2.0 candidate supports format 2 only; the later working source
uses current format 3 and recognizes format 2 for explicit specification extraction. Existing format-1 or older state must
be reported and preserved until a scoped migration is authorized; do not reset it
or merely change the version marker. Environment-manager owns configuration mapping;
Environment-manager owns Activity record maintenance/migration; optional installed Codex Chronicle-manager handles exact-source transcripts under Leader's coordination. Historical input and source remain attributable;
missing transcript source is reported, never reconstructed. See
[Activity migration notes](release-notes/activity-migration.md).

The existing candidate manifest retains its previously recorded specification target; this library migration does not rewrite release metadata. Specification-manager is now an optional installed package, acquired separately from the current core-only release allowlist. Specification compatibility **1** remains independent. Existing unmarked or
incompatible trees require specification-manager's assessment and an explicitly
approved adoption/migration before dependent edits. Neither extracting a bundle
nor changing a marker performs that migration. Candidate selection, packaging and
public publication are separate steps; a prepared candidate is not a published
release.


## Agent configuration contracts and upgrades

All agents, including the two core roles, ship `configuration/contract.json`
and declare it in SKILL metadata. No-settings agents use an empty settings map;
no workspace values file is needed. Saved values belong at
`.hai_env/config/agents/<agent-name>.json` and survive complete package replacement.
Do not copy workspace values into a reusable package or include credentials.

Upgrade the core conventions/helpers and selected optional packages together to
this definition standard. Stage and validate complete packages first; older packages
without declarations need a scoped definition update, not silent reinterpretation.
Inspect existing saved configuration versions/defaults, preserve their bytes and
report incompatible versions for owner migration. Installation and registration
never implicitly enable capabilities or create defaults files. Existing model
profiles and the mandatory instruction/Activity prerequisites remain independent.

Git-manager's explicit migration extracts legacy `integrations.git` and
`integrations.github`, verifies the new file, then removes only those old keys.
See the [migration guide](release-notes/agent-configuration-migration.md) for conflict,
backup and partial-failure handling. Specification enabled/location now belong to its installed owner file. Core
format 3 retains Activity location and chronicles; format 2 is a read-only transition
source. Recording settings remain core-owned; exact-source procedures and contracts now belong to the optional `codex-chronicle-manager` package.

## Selective optional-agent installation

External workspaces initially need only the complete `.hai` bundle. Its Leader,
Environment-manager provide startup, environment creation and Activity record/lifecycle maintenance;
no `hai_agents_library` checkout or optional authoring agent is needed.

For a later optional agent, ask Leader to route the explicitly selected package
and source/version to core Environment-manager. The installer:

1. Validates core context, fixed instructions, Activity and both runtime catalogues
   plus immediate agent-folder collections, including unregistered name conflicts.
2. Acquires only the selected complete package, or uses the supplied local package
   as data. It stages safe ordinary files in a disposable canonical installed layout,
   reads declared dependencies and runs trusted shared definition/contract validation
   directly. Missing peers are reported rather than auto-installed; no whole-library
   download or source-role invocation occurs.
3. Exclusively installs an absent `.hai_env/agents/<name>/` after validation, or
   reviews complete differences and preserves a recovery copy before an explicitly
   authorized existing-package replacement. Whole packages replace whole packages;
   overlays do not leave stale files. External agent config, profiles, instructions,
   records and unrelated packages remain preserved.
4. Registers the installed target only when the user explicitly requested it,
   optionally together with installation. For an existing registered package it
   synchronizes the exact decoded description/canonical row under the covering
   update scope, preserving membership. Both runtime catalogues belong to this owner.
5. Reads back installed bytes and catalogue evidence, reports actual checks and any
   partial results, and leaves execution to Leader. Copying/registering an agent
   does not enable specification, Git/GitHub or auto-push, or authorize domain work.

Agent-definition-manager creates/maintains definitions and verifies conventions;
it does not install packages or change catalogues. Creation can produce a local
unregistered definition or a reusable source package. Combined create/install/
register requests remain separate owner steps coordinated by Leader. An authoring
result includes exact identity/decoded description and validation evidence;
Environment-manager rereads the installed target before changing its row. Missing
optional authorship blocks authoring, not first-package installation.

This repository's `hai_agents_library/agents/` is one development/distribution source
for optional packages, not an external-workspace prerequisite. Shared edits belong
there first. Source edits leave installed snapshots unchanged; ask Environment-manager
for an explicitly selected update. Local differences or an unknown baseline require
review and a covering replacement decision, including unattributed differences.
No automatic updater, uninstall workflow, package-version/provenance scheme or
implicit dependency installation is introduced. Partial writes stop dependent work
and preserve actual results; there is no automatic retry, cleanup or rollback.

## Current source: Activity ownership split

The current core contains Leader and Environment-manager. Five complete optional
packages have golden definitions in `hai_agents_library/agents/`: `business-analyst`,
`solution-architect`, `software-developer`, `quality-assurance` and
`codex-chronicle-manager`. Install selected packages into `.hai_env/agents/` and
register them in the workspace catalogue through Environment-manager; never put
their runtime definitions in `.hai/` or execute a library source. No whole-library
download is required. Profiles, agent installation/registration and Activity records
remain Environment-manager duties; Leader retains orchestration and scheduling.

Upgrade complete core resources and optional consumers together. Retire the old
retired core record-owner folder and its framework registration only after new owners,
canonical references, workspace registration and verification are ready. Preserve
all Activity IDs, record paths, original inputs, revision history and transcript
bytes; this ownership migration requires no environment state-version change.
Missing optional Chronicle support/source blocks dependent recording and required
closure, not core validation, initialization, discovery or disabled-recording closure.
Required closure uses fresh operation-bound Chronicle evidence through Leader and
Environment-manager rechecks unchanged sources/artifacts before archival. Historical
candidate notes/manifests retain their original role/version descriptions.
