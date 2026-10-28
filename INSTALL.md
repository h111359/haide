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
Activity-manager owns record migration and chronicles-manager exact-source transcript
handling under leader's coordination. Historical input and source remain attributable;
missing transcript source is reported, never reconstructed. See
[Activity migration notes](release-notes/activity-migration.md).

Specification compatibility **1** remains independent. Existing unmarked or
incompatible trees require specification-manager's assessment and an explicitly
approved adoption/migration before dependent edits. Neither extracting a bundle
nor changing a marker performs that migration. Candidate selection, packaging and
public publication are separate steps; a prepared candidate is not a published
release.
