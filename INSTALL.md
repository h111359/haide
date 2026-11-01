# Installing and upgrading HAI

HAI is a prototype framework of agent instructions and Python validation tools.
It is not a Python package or a service that starts when a ZIP is extracted.

The current source is the **HAI 0.2.0 candidate**, with environment
state format **2**. The immutable **0.1.0** bundle supports format **1** and retains
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

## Current 0.2.0 candidate

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

## Existing installations and migration

Back up framework, environment and configured data before changing an installation.
Inspect the source or bundle contract targets. Replace reusable `.hai/` as a whole;
avoid overlays leaving stale role folders or manifests. Preserve `.hai_env/`, all
configured record/specification data and product files. A framework copy is not a
state, record or transcript migration.

The 0.2.0 candidate supports format 2 only. Existing format-1 or older state must
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
   Include `SKILL.md`, procedures, concepts and all supporting resources; do not
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
