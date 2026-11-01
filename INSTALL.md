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
Activity-manager. Optional chat setup configures specification, recording and
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
Activity-manager owns record migration and exact-source transcript handling under
Leader's coordination. Historical input and source remain attributable;
missing transcript source is reported, never reconstructed. See
[Activity migration notes](release-notes/activity-migration.md).

The existing candidate manifest retains its previously recorded specification target; this library migration does not rewrite release metadata. Specification-manager is now an optional installed package, acquired separately from the current core-only release allowlist. Specification compatibility **1** remains independent. Existing unmarked or
incompatible trees require specification-manager's assessment and an explicitly
approved adoption/migration before dependent edits. Neither extracting a bundle
nor changing a marker performs that migration. Candidate selection, packaging and
public publication are separate steps; a prepared candidate is not a published
release.


## Agent configuration contracts and upgrades

All agents, including the three core roles, ship `configuration/contract.json`
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
source. Chronicles extraction is outside this change.

## Optional copied agents and manual bootstrap

The core provides Leader, Environment-manager and Activity-manager. Obtain selected
complete optional packages separately; this source repository keeps them at
`hai_agents_library/agents/`, but the current release allowlist does not ship that
library. Never execute a library definition or import its helpers as a runtime
fallback. A copied package's own local resources and compatible core/installed
peers provide its runtime knowledge.

When Agent-definition-manager is already installed and registered, ask Leader to
route explicit complete-package installation/update and any separately explicit
registration to it. If that owner is absent, the human can bootstrap manually:

1. Validate compatible initialized state and readable fixed instructions with the
   core startup helper. Preserve existing workspace data and inspect both runtime
   catalogues/folder names for conflicts; source counterparts are not runtime names.
2. Copy the whole selected `agent-definition-manager` package into an absent
   `.hai_env/agents/agent-definition-manager/` using ordinary independent files.
   Include `SKILL.md`, the mandatory configuration contract, procedures, concepts and all supporting resources; do not
   use a symlink/hardlink back to source. Stop on an existing target or conflicting name.
3. Run `python -B .hai/tools/agents/agent_tools.py validate --definition .hai_env/agents/agent-definition-manager/SKILL.md`
   with a verified Python 3.11+ interpreter. Read the shared helper instructions;
   validation does not register or prove semantic correctness/runtime support.
4. Explicitly add its single canonical row to `.hai_env/agents/catalogue.md` under
   the core state convention: exact decoded YAML description, required table
   encoding and `[SKILL.md](agent-definition-manager/SKILL.md)` destination. Preserve
   other rows/prose. If absent, the human creates the standard catalogue header/table.
5. Run core startup and `python -B .hai/tools/agents/agent_tools.py audit`; resolve
   actual findings and supported model settings before invocation. The same manual
   copy/validate/register process may install another explicitly selected package.

This human bootstrap is not permission for Leader to perform environment or
catalogue writes. Registration, feature/integration enablement and task authority
are separate; copying Specification-manager does not enable specification, and
copying Git-manager does not enable Git/GitHub or push.

Shared edits belong in the golden source. Installed snapshots change only after
an explicit human update choice. Compare whole packages and any known prior source
baseline; stop for human review if local edits or a missing baseline prevent attribution.
After reviewing the complete differences, the human may explicitly choose replacement
including unattributed changes; do not invent their source or infer that choice.
Preserve a recoverable prior copy in an agreed location, stage/validate the complete
candidate, then replace the full package without leaving stale overlay files and
synchronize an existing catalogue description. Report partial failure; no automatic
retry, rollback, merge or updater is implied. A core upgrade preserves installed
optional snapshots and does not silently upgrade them. Agent versions and provenance
schemes are deferred; no additional runtime state is required.
