# BL-0012 implementation plan

Consolidate environment state, model profiles and mandatory instructions under `.hai_env/config/`, adapt their consumers, and provide an explicit migration for existing environments without losing workspace data.

Status: proposed design, prepared on 2026-11-09 for Activity `d44d0ee7-4250-494a-ba54-40b4729b94d2`. This plan authorizes no implementation, migration, installation or release.

| Phase | Goal | Depends on | Expected result |
| --- | --- | --- | --- |
| 1 — Define paths and compatibility | Establish one layout contract | None | Shared paths and explicit legacy diagnostics |
| 2 — Update core consumers | Make fresh environments work | 1, to use the same contract | New layout works across core operations |
| 3 — Implement explicit migration | Preserve existing environments | 1–2, to validate the destination | Previewable, guarded relocation |
| 4 — Adapt packages and guidance | Bring dependent resources into agreement | 1–3, for stable paths and commands | Source packages, selected installations and docs agree |
| 5 — Verify and prepare delivery | Demonstrate the complete change | 2–4, for end-to-end coverage | Tests, independent review and delivery evidence |

## Agreed requirements

- Move `.hai_env/state.json` to `.hai_env/config/state.json`.
- Move `.hai_env/model_profiles.json` to `.hai_env/config/model_profiles.json` when present; profiles remain optional.
- Move `.hai_env/agent_instructions.md` to `.hai_env/config/agent_instructions.md`; readable empty instructions remain valid.
- Adapt every affected definition, script and other current resource.
- Include migration of existing environments. User clarification: “yes, migrate existing env as well”.
- Preserve configuration values, instruction content and unrelated workspace data.

The purpose is a clearer `.hai_env/` arrangement. Requirements come from [BL-0012](../../../backlog/new/BL-0012.md) and the [recorded user decision](decisions.md).

## Proposed design and constraints

- Centralize fixed environment paths in a small dependency-free module. Preserve existing helper interfaces where possible; do not create a configurable second layout.
- Ordinary operation uses only the new locations. Legacy paths are recognized for diagnosis and explicitly requested migration, without silent fallback or automatic relocation.
- Propose `environment migrate-layout`, using the existing request/provenance format, read-only preview and explicit `--apply`. This command does not exist yet.
- Keep relocation separate from state-schema conversion. Preserve file bytes and schema versions; supported older schemas still require their existing explicit conversion before ordinary use.
- Allow the migration entry point to validate safe legacy instructions/state without requiring successful new-layout startup. Initialization must reject a legacy environment rather than create competing defaults.
- Preserve the runtime lock at `.hai_env/.runtime.lock`, agent settings under `.hai_env/config/agents/`, Activity records and their individual `state.json` files.
- Update reusable source packages and installed copies as distinct operations. Runtime replacement must review local differences and retain backups; copying a library edit does not update an installation.
- Historical Activities, transcripts, backlog history and published release evidence retain their original paths as historical text. Audit current operational references rather than globally replacing all `state.json` strings.

No human decision currently blocks this plan. Migration mechanics below are proposed engineering choices; unexpected compatibility or data conflicts must be reported before dependent writes.

## Phase 1 — Define paths and compatibility

**Purpose**
- Give every consumer the same canonical paths and distinguish layout from state schema.

**Why now**
- Existing paths are repeated across startup, runtime, configuration validation and optional packages.

**Visible result**
- Old-path literals used for ordinary operation become named canonical paths; legacy diagnostics remain explicit.

**Scope**
- Cover the three relocated resources and their reserved-path rules. Leave Activity filenames and agent configuration ownership unchanged.

### Actions

| Step | Action | Purpose or expected result |
| --- | --- | --- |
| 1.1 | Inventory current consumers and their import entry points | Include direct helper scripts and installed-package execution |
| 1.2 | Add a dependency-free environment-path module | Provide canonical paths and a clearly separated legacy mapping |
| 1.3 | Define absent, legacy-only, new-only, mixed and unsafe layouts | Produce deterministic diagnostics and allowed operations |
| 1.4 | Specify schema-conversion ordering | Support valid format-2 and format-3 relocation without rewriting their contents |
| 1.5 | Specify initialization refusal for legacy or partial layouts | Prevent a second environment from obscuring existing data |

### Affected files

Inventory groups A and D below; proposed environment-path module.

### Complete when

- Every current consumer has an assigned update or documented historical exemption.
- Layout diagnostics distinguish invalid state from absence and never imply that migration ran.
- Proposed path imports work from runtime and standalone helper entry points without circular imports.

## Phase 2 — Update core consumers

**Purpose**
- Make initialization, startup and normal operations use the new layout consistently.

**Why now**
- Migration needs a working destination validator before it can claim success.

**Visible result**
- A disposable fresh workspace initializes and operates using `.hai_env/config/`.

**Scope**
- Change paths and affected safety rules; preserve current schemas, optionality and unrelated settings.

### Actions

| Step | Action | Purpose or expected result |
| --- | --- | --- |
| 2.1 | Update startup readers and initialization writers | Create only mandatory files at the new paths |
| 2.2 | Adjust instruction alias validation | Permit the exact canonical instruction file under `config/` while rejecting aliases to other resources |
| 2.3 | Update state, profile and agent-configuration helpers | Preserve strict parsing, defaults and isolated configuration diagnostics |
| 2.4 | Update Activity and recording consumers | Preserve current Activity identity, chronicles flags and synchronization behavior |
| 2.5 | Update specification-schema migration paths | Make schema conversion work after relocation, with recoverable backups |
| 2.6 | Add fresh-layout and path-safety regression cases | Verify the destination before writing relocation code |

### Affected files

Inventory groups A–C; corresponding startup, configuration, agent and runtime test files.

### Complete when

- Fresh initialization creates state and instructions under `config/`, without fabricating optional profiles.
- Startup loads empty and nonempty instructions correctly and reports profile errors independently.
- Activity, profile, configuration and recording operations use the new state path.
- Content roots remain prohibited from overlapping configuration; canonical instructions are no longer rejected merely because their parent is `config/`.

## Phase 3 — Implement explicit migration

**Purpose**
- Move an existing environment safely while retaining evidence needed for recovery.

**Why now**
- Phase 2 supplies the readers and validators needed to verify the migrated environment.

**Visible result**
- Preview reports exact moves; explicit apply yields a working new layout or a precise partial-result report.

**Scope**
- Relocate the three fixed files. Do not alter settings, relocate Activities or enable features.

### Actions

| Step | Action | Purpose or expected result |
| --- | --- | --- |
| 3.1 | Add a migration branch before normal new-layout mutation checks | Avoid requiring migration to have already completed |
| 3.2 | Validate all source/destination paths and source contents | Reject unsafe parents, links, malformed input and ambiguous layouts before writes |
| 3.3 | Produce a read-only move and preservation preview | Include absent optional profiles, expected hashes and conversion requirements |
| 3.4 | Quiesce participating writers before apply | Prevent old processes from reading or rewriting files during relocation |
| 3.5 | Acquire the existing runtime lock and recheck inspected inputs | Reject concurrent changes and pre-existing unexplained locks |
| 3.6 | Save exclusive recovery copies and an attributable operation manifest | Preserve exact original bytes and report the backup location |
| 3.7 | Create destinations exclusively and verify their bytes | Preserve values, unknown fields, instruction text and optional absence |
| 3.8 | Validate the complete new layout before retiring originals | Establish destination integrity before source removal |
| 3.9 | Retire originals only after successful checks | Leave one canonical layout on success; report every actual changed path |
| 3.10 | Verify startup and required schema-conversion diagnostics | Distinguish successful relocation from schema conversion still required |

### Affected files

Inventory group B; proposed layout-migration module and regression tests.

### Complete when

- Preview writes nothing; apply preserves source bytes in both destination and recovery evidence.
- Missing mandatory input blocks migration; absent profiles remain absent.
- Mixed layouts and existing destination files block automatic overwrite or merge, including identical duplicates requiring explicit reconciliation.
- Repeating a completed migration reports unchanged. Interrupted operations retain their manifest and partial changes for explicit recovery, without automatic retry or rollback.
- Failure injection between writes and removals produces accurate changed paths and actionable recovery instructions.
- Valid format-2 input can be relocated byte-for-byte, then explicitly converted using the existing schema-migration workflow; it is never reported as ready for ordinary format-3 operations prematurely.

A multi-file migration is not atomic. Keep originals until destination validation, retire state last, and make partial layouts fail clearly rather than guessing precedence.

## Phase 4 — Adapt packages and guidance

**Purpose**
- Make definitions, helpers and user instructions match the implemented layout.

**Why now**
- Migration behavior and its command contract are stable enough to document and consume.

**Visible result**
- A reader can initialize or migrate an environment using current instructions, and affected packages work from their installed locations.

**Scope**
- Update current operational resources. Preserve historical evidence and existing registration membership.

### Actions

| Step | Action | Purpose or expected result |
| --- | --- | --- |
| 4.1 | Update affected reusable package helpers and fixtures | Remove direct reads of the retired operational paths |
| 4.2 | Update core conventions, startup instructions and command examples | Explain new paths, compatibility and explicit migration |
| 4.3 | Review affected installed packages against their sources | Identify local differences before any replacement |
| 4.4 | Apply separately authorized package updates through runtime operations | Retain backups and external settings |
| 4.5 | Validate affected definitions and registrations | Refresh registered descriptions only if their actual canonical descriptions changed |
| 4.6 | Audit remaining old-path references | Retain only justified legacy handling, negative tests and historical evidence |

### Affected files

Inventory group D and the discovered source/installed package files in group E.

### Complete when

- Startup documentation loads the new fixed instructions before dependent work and explains safe legacy diagnosis.
- Affected helpers run from an installed layout without a source-library fallback.
- Documentation and fixtures agree with the new paths; historical records remain intact.
- Source changes, actual installed updates and any pending deployment work are reported separately.

## Phase 5 — Verify and prepare delivery

**Purpose**
- Establish that both new and existing environments work and unrelated data survives.

**Why now**
- End-to-end evidence requires the complete core, migration and package changes.

**Visible result**
- Reproducible test results and an independent review cover every acceptance criterion.

**Scope**
- Use disposable workspaces first. Real workspace migration waits for implementation authority and ended writers.

### Actions

| Step | Action | Purpose or expected result |
| --- | --- | --- |
| 5.1 | Run targeted and full relevant Python suites | Cover startup, configuration, runtime, schema migration and affected packages |
| 5.2 | Exercise a disposable legacy workspace through migration | Preserve a current Activity, chronicles, agent settings and custom values |
| 5.3 | Exercise a fresh workspace and a migrated workspace identically | Compare observable operations after reaching supported schema state |
| 5.4 | Assign a separate reviewer for runtime and persistence changes | Independently assess requirements, safety and test evidence |
| 5.5 | Record platform limits and unresolved findings | Avoid treating fixture success as real host or cross-platform proof |
| 5.6 | Prepare upgrade guidance and a justified release recommendation | Describe the path compatibility break without publishing a release |

### Affected files

Inventory test files, current documentation and Activity verification evidence. Release artifact filenames remain a delivery decision; existing published manifests are historical evidence.

### Complete when

- Developer checks and separate review agree that all five backlog acceptance conditions are demonstrated.
- Active Activity identity, input, history, transcripts and agent settings are preserved across the disposable migration.
- Live migration, installation, commits, publication and Activity closure occur only under their covering instructions and recording requirements.

## File inventory

All paths below are repository-relative. Existing paths link to current files; proposed paths name files that do not yet exist.

| Path | Change | Purpose |
| --- | --- | --- |
| Proposed `.hai/tools/environment_paths.py` | Add | Dependency-free fixed paths and explicit legacy mapping |
| A: Existing [.hai/tools/startup/startup_check.py](../../../.hai/tools/startup/startup_check.py) | Edit | Canonical readers, legacy diagnostics and instruction alias rules |
| A: Existing [.hai/tools/configuration/configuration_tools.py](../../../.hai/tools/configuration/configuration_tools.py) | Edit | Reserved paths and state-based content reservations |
| A: Existing [.hai/tools/agents/agent_tools.py](../../../.hai/tools/agents/agent_tools.py) | Edit | Profile loading and package checks |
| B: Existing [.hai/tools/runtime/environment.py](../../../.hai/tools/runtime/environment.py) | Edit | Initialization, environment/profile writes and migration dispatch |
| B: Existing [.hai/tools/runtime/storage.py](../../../.hai/tools/runtime/storage.py) | Edit if needed | Reuse guarded writes and preserve lock semantics |
| B: Existing [.hai/tools/startup/migrate_specification_configuration.py](../../../.hai/tools/startup/migrate_specification_configuration.py) | Edit | Keep schema conversion separate and path-compatible |
| B: Proposed `.hai/tools/runtime/layout_migration.py` | Add | Explicit relocation preview/apply and recovery evidence |
| B: Proposed `.hai/tools/runtime/tests/test_layout_migration.py` | Add | Migration, conflicts and failure-injection tests |
| C: Existing [.hai/tools/runtime/activities.py](../../../.hai/tools/runtime/activities.py) | Edit | Environment-state reads; preserve Activity-local state filenames |
| C: Existing [.hai/tools/runtime/chronicles.py](../../../.hai/tools/runtime/chronicles.py) | Edit | Recording configuration and environment fingerprints |
| C: Existing [.hai/tools/runtime/recording.py](../../../.hai/tools/runtime/recording.py) | Edit | Environment-state reads for recording operations |
| C: Existing [.hai/tools/runtime/source_discovery.py](../../../.hai/tools/runtime/source_discovery.py) | Edit | Recording enablement lookup |
| D: Existing [.hai/start.md](../../../.hai/start.md) | Edit | Fixed instruction path and migration entry guidance |
| D: Existing [.hai/conventions/state_conv.md](../../../.hai/conventions/state_conv.md) | Edit | New canonical locations and explicit migration contract |
| D: Existing [.hai/conventions/agent_conv.md](../../../.hai/conventions/agent_conv.md) | Edit | Mandatory instruction-path references |
| D: Existing [.hai/conventions/model-profiles_conv.md](../../../.hai/conventions/model-profiles_conv.md) | Edit | Optional profile location |
| D: Existing [.hai/conventions/framework-layout_conv.md](../../../.hai/conventions/framework-layout_conv.md) | Edit | Environment layout and upgrade explanation |
| D: Existing [.hai/tools/runtime/README.md](../../../.hai/tools/runtime/README.md) | Edit | Proposed command, preview/apply and recovery behavior |
| D: Existing [.hai/tools/startup/README.md](../../../.hai/tools/startup/README.md) | Edit | Startup and schema-migration examples |
| D: Existing [.hai/tools/configuration/README.md](../../../.hai/tools/configuration/README.md) | Edit | Core and owner-settings path boundaries |
| E: Existing [git migration helper](../../../hai_agents_library/agents/git-manager/scripts/migrate_git_configuration.py) | Edit | Legacy Git-setting conversion dependencies |
| E: Existing [specification configuration helper](../../../hai_agents_library/agents/specification-manager/scripts/specification_configuration.py) | Edit | Fixed state and instruction access |
| Existing [.hai_env/state.json](../../state.json) → Proposed `.hai_env/config/state.json` | Move | Canonical environment state |
| Existing [.hai_env/model_profiles.json](../../model_profiles.json) → Proposed `.hai_env/config/model_profiles.json` | Move when present | Optional model profiles |
| Existing [.hai_env/agent_instructions.md](../../agent_instructions.md) → Proposed `.hai_env/config/agent_instructions.md` | Move | Mandatory instruction content |

The inventory is a starting map from actual searches, not a claim that every dependency has already been enumerated. Phase 1 expands it to each discovered test, package definition and example requiring a change.

## Verification matrix

These checks are planned; implementation tests have not been run for this plan.

| Acceptance condition | Evidence to produce |
| --- | --- |
| Three canonical files use new locations | Fresh and migrated layout assertions; optional profiles absent/present cases |
| Dependencies are adapted | Current-reference audit, helper execution and affected package validation |
| Operations work with the new layout | Startup, initialization, environment/profile configuration, package resolution, Activity and recording regressions |
| Existing environments preserve data | Byte comparisons, unknown fields, nonempty/empty instructions, custom Activity roots and unrelated-file hashes |
| Migrated environments work | End-to-end disposable migration and subsequent normal operations |

Migration cases also cover malformed JSON, missing instructions, unsupported schemas, unsafe paths, aliases, permission errors, lock contention, changed inputs, mixed layouts, repeated apply and interrupted writes/removals.

Use `/usr/bin/python3 -B` with the existing unittest suites under `.hai/tools/runtime/tests`, `.hai/tools/startup`, `.hai/tools/configuration` and `.hai/tools/agents`, plus affected installed-package suites. Confirm each suite's documented invocation during implementation.

## Risks and delivery boundaries

- Instruction validation currently reserves the entire `config/` directory; changing only path strings would make valid startup fail. Phase 2 changes the precise alias rules while retaining content-root protections.
- Old-layout mutation checks would block relocation before it begins. Phase 3 provides a narrow legacy-validation branch rather than weakening normal mutation guards.
- Concurrent old processes and multi-file failures can leave mixed layouts. Require ended writers, guarded operations, recovery copies and explicit partial-result diagnostics.
- Source packages, installed packages and archived evidence have different ownership. Update operational copies deliberately and retain historical text.
- The current task is planning only. Exact human authority: “Create a plan for realization of this backlog item.” Implementation, live migration and publication remain unperformed.


Revision provenance: source: Human request: Create a plan for realization of this backlog item.; reason: Save reviewable plan and evidence; implementation is not authorized by this operation.; reason: User-requested BL-0012 implementation plan and attributable planning evidence.; recorded 2026-11-09T16:42:08Z.
