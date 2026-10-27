# Installing HAI 0.1.0

HAI is a prototype framework of agent instructions and Python validation tools.
It is used inside an AI-assisted development workspace; it is not a Python package
or a service that starts automatically when the ZIP is extracted.

## Requirements

- An AI coding environment that can read workspace files and follow
  [the startup instructions](.hai/start.md). Agent spawning, supported model/effort
  combinations, and available tools depend on that environment; HAI does not install
  or guarantee those capabilities.
- A working Python 3.11 or newer for the bundled validation helpers. They use the
  standard library and do not install dependencies. Verify the actual interpreter
  before running helpers; an unavailable launcher is not proof Python is absent.
- Git and GitHub access only for the operations you choose to enable. GitHub CLI is
  not required when another supported connector or transport meets the task's needs.

## New installation

1. Extract `hai-0.1.0.zip` into a temporary directory and inspect its contents. The
   package contains `.hai/`, `LICENSE`, `README.md`, this guide, and the release notes.
2. Copy `.hai/` into the root of the intended workspace. Do not extract package-root
   documentation over an existing project's `README.md` or `LICENSE`. Retain the
   supplied MIT license with the installed framework, for example by copying the
   package's `LICENSE` to `.hai/LICENSE`. Retain the extracted package as a
   documentation/reference copy when its root filenames would conflict with project files.
3. In your AI coding environment, ask it to read `.hai/start.md`. HAI loads the
   leader role and validates the workspace. If core state is safely absent,
   environment-manager initializes `.hai_env/state.json` and the fixed
   `.hai_env/agent_instructions.md`, preserving existing unrelated material.
4. Use **Additional setup** to configure supported specialist model profiles and
   any optional features. Requests, specification and chronicles start off. Git and
   GitHub integrations also start off; automated push is a separate opt-in that
   requires verified tooling, authentication and write readiness before enablement.
5. Ask for an ordinary task or select a registered framework agent. The package
   supplies framework agents; it does not supply this repository's workspace agents,
   model profiles, credentials, specifications or session history.

For a read-only environment check from the workspace root, run a verified Python
3.11+ executable with `-B .hai/tools/startup/startup_check.py --workspace .`.
See [helper instructions](.hai/tools/startup/README.md) for interpreter discovery,
output and limitations. An absent environment is an initialization dependency,
not something that this helper creates or repairs.

## Existing installations and prototype workspaces

Back up the existing `.hai/` and `.hai_env/` before an upgrade. Read the release
notes and compare the manifest's contract targets with the existing environment
and any specification tree before dependent work.

Replace the reusable `.hai/` as one unit from the inspected package, retaining
workspace-specific custom material separately. Avoid overlay extraction that leaves
stale framework files or multiple `release-*.json` manifests. Keep the supplied MIT
license with the new copy. Preserve `.hai_env/`, its configured feature data and
all product files; the release does not contain replacements for them.

This release supports environment state format **1**. Older prototype state using
`compatible_version` is unsupported legacy metadata and must not be silently
reinterpreted or reset. Ask environment-manager for a scoped, authorized plan when
existing state is incompatible. Specification compatibility **1** is independent;
existing unmarked or incompatible trees require specification-manager's assessment
and an explicitly approved adoption or migration before dependent edits. Extracting
a bundle or changing a version marker does not perform either migration.

## Version and license

The installed bundle identifies itself in
[release-0.1.0.json](.hai/release-0.1.0.json). State-format and specification
compatibility targets are independent of the `0.1.0` bundle version.

See [release notes](release-notes/0.1.0.md) for the experimental versioning policy,
capabilities and known limits. HAI is distributed under the [MIT license](LICENSE).
