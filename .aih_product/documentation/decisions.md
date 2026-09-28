# Contents

- [1. Framework architecture and deterministic operations](#1-framework-architecture-and-deterministic-operations)
  - [1.1. Languages, storage, and optional dependencies](#11-languages-storage-and-optional-dependencies)
  - [1.2. Installed core and authoritative contracts](#12-installed-core-and-authoritative-contracts)
  - [1.3. Shared Python operations and agent responsibilities](#13-shared-python-operations-and-agent-responsibilities)
  - [1.4. Incremental context loading and reuse](#14-incremental-context-loading-and-reuse)
  - [1.5. Compact evidence and usage verification](#15-compact-evidence-and-usage-verification)
- [2. Product state and workspace mechanisms](#2-product-state-and-workspace-mechanisms)
  - [2.1. State layout and durable record ownership](#21-state-layout-and-durable-record-ownership)
  - [2.2. Temporary data and executable artifact placement](#22-temporary-data-and-executable-artifact-placement)
  - [2.3. Registry schema, identity, and administration](#23-registry-schema-identity-and-administration)
  - [2.4. Mapping changes and evidence validity](#24-mapping-changes-and-evidence-validity)
  - [2.5. New roots and retained obligations](#25-new-roots-and-retained-obligations)
- [3. Filesystem confinement](#3-filesystem-confinement)
  - [3.1. Resolved targets and host enforcement](#31-resolved-targets-and-host-enforcement)
  - [3.2. Runtime and optional Git side effects](#32-runtime-and-optional-git-side-effects)
- [4. Execution ownership and recoverable state](#4-execution-ownership-and-recoverable-state)
  - [4.1. Action reservation and duplicate prevention](#41-action-reservation-and-duplicate-prevention)
  - [4.2. Transactions, checkpoints, and stale ownership](#42-transactions-checkpoints-and-stale-ownership)
  - [4.3. Cross-filesystem progress and recovery](#43-cross-filesystem-progress-and-recovery)
  - [4.4. Process termination and Stop behavior](#44-process-termination-and-stop-behavior)
- [5. Request persistence and workflow](#5-request-persistence-and-workflow)
  - [5.1. Input snapshots, responses, and archival](#51-input-snapshots-responses-and-archival)
  - [5.2. Clarification definition and semantic boundaries](#52-clarification-definition-and-semantic-boundaries)
  - [5.3. Amendments and captured revisions](#53-amendments-and-captured-revisions)
  - [5.4. Analysis records and design assessment](#54-analysis-records-and-design-assessment)
  - [5.5. Plans, tasks, and implementation authority](#55-plans-tasks-and-implementation-authority)
  - [5.6. Unrelated issues and repair scope](#56-unrelated-issues-and-repair-scope)
  - [5.7. Successful closure and current evidence](#57-successful-closure-and-current-evidence)
  - [5.8. Unsuccessful closure and current-state notices](#58-unsuccessful-closure-and-current-state-notices)
  - [5.9. Request identity and documentation generation](#59-request-identity-and-documentation-generation)
- [6. Questionnaire and exchange implementation](#6-questionnaire-and-exchange-implementation)
  - [6.1. Authoritative questionnaires and form records](#61-authoritative-questionnaires-and-form-records)
  - [6.2. Answer matching, intake, and review](#62-answer-matching-intake-and-review)
  - [6.3. Combined import and launch recovery](#63-combined-import-and-launch-recovery)
- [7. Read-only question execution](#7-read-only-question-execution)
- [8. Test execution and failure handling](#8-test-execution-and-failure-handling)
  - [8.1. Suite inventory, environments, and content evidence](#81-suite-inventory-environments-and-content-evidence)
  - [8.2. Regression repairs and persistent budgets](#82-regression-repairs-and-persistent-budgets)
- [9. Documentation generation and maintenance](#9-documentation-generation-and-maintenance)
  - [9.1. System-operation records and ownership](#91-system-operation-records-and-ownership)
  - [9.2. Initial portal bootstrap and baseline checks](#92-initial-portal-bootstrap-and-baseline-checks)
  - [9.3. Reverse-engineering commands and provenance](#93-reverse-engineering-commands-and-provenance)
  - [9.4. Dependency tracking and documentation increments](#94-dependency-tracking-and-documentation-increments)
  - [9.5. Catalog structure, traversal, and rebalancing](#95-catalog-structure-traversal-and-rebalancing)
  - [9.6. Reconstruction evidence checks](#96-reconstruction-evidence-checks)
  - [9.7. Typed extension storage and identity](#97-typed-extension-storage-and-identity)
  - [9.8. Catalog and document reference contract](#98-catalog-and-document-reference-contract)
  - [9.9. Delta representation and baseline integrity](#99-delta-representation-and-baseline-integrity)
  - [9.10. Documentation collection verification](#910-documentation-collection-verification)
- [10. Audit records and sensitive data](#10-audit-records-and-sensitive-data)
  - [10.1. Ledger and incremental implementation evidence](#101-ledger-and-incremental-implementation-evidence)
  - [10.2. Admission, redaction, and unsafe-content checks](#102-admission-redaction-and-unsafe-content-checks)
- [11. Skill packaging and integration](#11-skill-packaging-and-integration)
  - [11.1. Format, bundled resources, and standalone contracts](#111-format-bundled-resources-and-standalone-contracts)
  - [11.2. Initial packages and capability ownership](#112-initial-packages-and-capability-ownership)
  - [11.3. Catalog generation, discovery, and enablement](#113-catalog-generation-discovery-and-enablement)
  - [11.4. Standalone portability verification](#114-standalone-portability-verification)
- [12. Agent adapters and handoffs](#12-agent-adapters-and-handoffs)
  - [12.1. Adapter configuration and profile selection](#121-adapter-configuration-and-profile-selection)
  - [12.2. Process invocation, events, and fault handling](#122-process-invocation-events-and-fault-handling)
  - [12.3. Manual reservation and Stop-release verification](#123-manual-reservation-and-stop-release-verification)
- [13. Portal implementation](#13-portal-implementation)
  - [13.1. Startup, workers, and event delivery](#131-startup-workers-and-event-delivery)
  - [13.2. File endpoints, origins, and privileged settings](#132-file-endpoints-origins-and-privileged-settings)
  - [13.3. Rendered pages and workflow state checks](#133-rendered-pages-and-workflow-state-checks)
- [14. CLI, installation, and maintained help](#14-cli-installation-and-maintained-help)
  - [14.1. Menu commands and home resolution](#141-menu-commands-and-home-resolution)
  - [14.2. Installation, upgrades, and host integration](#142-installation-upgrades-and-host-integration)
  - [14.3. Shared help sources and consistency](#143-shared-help-sources-and-consistency)
- [15. Verification fixtures and live validation](#15-verification-fixtures-and-live-validation)
  - [15.1. Automated fixtures, live CLI, and browser checks](#151-automated-fixtures-live-cli-and-browser-checks)
  - [15.2. End-to-end, recovery, and existing-product scenarios](#152-end-to-end-recovery-and-existing-product-scenarios)
- [Referenced documents](#referenced-documents)
- [Sources](#sources)

# 1. Framework architecture and deterministic operations

## 1.1. Languages, storage, and optional dependencies

- [A] 1.1.1. All framework behavior, helpers, adapters, workers, orchestration, bookkeeping, and backend components MUST be Python.
  {S1:L39}

- [A] 1.1.2. HTML, CSS, and JavaScript are OPTIONAL permitted implementation languages for the browser portal.
  {S1:L39}

- [A] 1.1.3. Product implementation languages MUST remain unrestricted.
  {S1:L39}

- [A] 1.1.4. Markdown and validated YAML/JSON files MUST be authoritative storage; AIH MUST NOT use SQLite, embedded databases, database caches, or other databases.
  {S1:L41}

- [A] 1.1.5. Search indexes are OPTIONAL and MUST be disposable files or in-memory structures if used.
  {S1:L41}

- [A] 1.1.6. Git integration MUST be packaged as an optional configurable skill extension rather than a required core dependency.
  {S1:L43}

- [A] 1.1.7. Acceptance verification of implementation languages and dependencies MUST cover this check: All framework behavior, helpers, adapters, workers, and backend code are Python.
  {S1:L716}

- [A] 1.1.8. Acceptance verification of implementation languages and dependencies MUST cover this check: The only non-Python harness scripts are the two optional menu launch wrappers with no framework business logic; direct Python operation remains complete.
  {S1:L716}

- [A] 1.1.9. Verification MUST demonstrate that AIH uses no database.
  {S1:L716}

- [A] 1.1.10. Verification MUST demonstrate that Git is not a default dependency.
  {S1:L716}

## 1.2. Installed core and authoritative contracts

- [A] 1.2.1. The canonical framework home MUST contain the sole `.aih/` versioned core and central `.aih_product/` product-state tree and be registered with stable writable ID `home`; these paths MUST resolve from home independently of process working directory.
  {S1:L20, S1:L34-37}

- [A] 1.2.2. The immediate `.aih/` directories MUST be `prompts/` for on-demand behavior, `conventions/` for authoritative formats/contracts, `skills/` for packages/catalogs, and `engine/` for shared Python infrastructure and portal assets/tests.
  {S1:L53-58}

- [A] 1.2.3. Core root files MUST include the single `.aih/run.md` entry point, `.aih/README.md`, and `.aih/USER_GUIDE.md`; OS launchers and core version/integrity manifests are OPTIONAL, with menu infrastructure under `engine/` rather than additional immediate directories.
  {S1:L60}

- [A] 1.2.4. Prompts MUST reference authoritative conventions rather than redefine schemas/templates/structure; conventions MUST NOT depend on prompts, and validators MUST implement the same authoritative contracts.
  {S1:L62}

- [A] 1.2.5. `run.md` MUST remain concise/stable and route from submitted action, validated state/instructions, discovered metadata, and owning request/system operation without a hard-coded skill roster or profile names.
  {S1:L64}

- [A] 1.2.6. Core conventions MUST define versioned schemas for configuration/registry/revisions/state/skills/integrity, requests/catalogs/submissions/analysis/rounds/amendments/forms/receipts/reviews, plans/questions/approvals/defects/increments, system/bootstrap/inventory/extraction/reuse/usage/events/checkpoints/docs/evidence/logs/runs, owners/handoffs/baselines/readiness/notices/repair/test/standalone/redaction/temp contracts.
  {S1:L578}

- [A] 1.2.7. Acceptance verification of directory organization and inert state MUST cover this check: Root organization is valid, immediate directory names do not overlap, and no product skills directory or executable product-state content is accepted. `.aih_product/tmp/` exists for operation-owned inert data; scripts, packages, virtual environments, bytecode, and runnable fixtures are excluded from it.
  {S1:L717}

- [A] 1.2.8. Acceptance verification of core and instruction immutability MUST cover this check: Ordinary runs leave the core and human-owned custom instructions unchanged.
  {S1:L718}

## 1.3. Shared Python operations and agent responsibilities

- [A] 1.3.1. Every deterministic framework operation MUST have named Python entry points/shared APIs used by agents and portal instead of ad hoc model-generated commands/scripts, manual state edits, or duplicated implementations.
  {S1:L72-74}

- [A] 1.3.2. Deterministic helper coverage MUST include initialization, registry/history/containment/path resolution/scope impact/temp handling, inventories/fact extraction/hashes/diffs, schema/input screening/redaction, submissions/questionnaires/forms/imports/amendments, revisions/ownership/handoffs/transitions/locks/transactions/edit application, catalogs/tasks/tests/repair budgets, logs/checkpoints/archival/diagnostics/upgrades.
  {S1:L74}

- [A] 1.3.3. Helpers MUST collect/validate facts and apply specified operations while agents interpret evidence, resolve ambiguity, choose authorized solutions, produce semantic content/patches, and diagnose failures; heuristic output MUST NOT establish business intent or semantic correctness by itself.
  {S1:L76}

- [A] 1.3.4. The deterministic-operation catalog MUST expose typed operation IDs, inputs/effects/permissions/results, concise status/changed artifacts/actionable errors/conflicts, and linked verbose evidence rather than generic command templates.
  {S1:L78}

- [A] 1.3.5. Initialization, approval/state changes, locks, snapshots, execution, catalogs, archival, and routine recovery MUST remain deterministic engine operations rather than additional skills; routing MUST remain shared in `run.md`.
  {S1:L527}

- [A] 1.3.6. Acceptance verification of deterministic helper use MUST cover this check: Inventory, parsing, validation, state updates, test execution/result capture, catalog maintenance, and archival route through tested deterministic helpers.
  {S1:L753}

- [A] 1.3.7. Acceptance verification of deterministic helper use MUST cover this check: Check equivalent bundled helpers for standalone skills.
  {S1:L753}

- [A] 1.3.8. Acceptance verification of deterministic helper use MUST cover this check: Test structural/helper behavior separately from actual agent compliance with the mandatory-use rule.
  {S1:L753}

## 1.4. Incremental context loading and reuse

- [A] 1.4.1. Context loading MUST read metadata/relevant catalog branches before leaves and skill bodies/resources only on demand, using fingerprints/dependency maps and still-valid summaries/checkpoints to select affected material.
  {S1:L86}

- [A] 1.4.2. Reusable summaries MUST preserve source/version, decisions, unresolved issues, and recovery context, and be invalidated for relevant source/instruction/workspace/extractor/schema/core changes. Cache validity MUST be checked against the current folder identity, location, and access settings without requiring workspace configuration revision history.
  {S1:L86, S3:section "Accepted policy"}

- [A] 1.4.3. Reusable summaries/indexes MUST be validated files or memory, never a database or ordinary write into core.
  {S1:L88}

- [A] 1.4.4. Acceptance verification of incremental context reuse MUST cover this check: Unchanged input sets reuse valid extraction/summaries and avoid unnecessary semantic generation.
  {S1:L754}

- [A] 1.4.5. Acceptance verification of incremental context reuse MUST cover this check: Source, instruction, extractor, or schema/core changes invalidate affected reuse.
  {S1:L754}

- [A] 1.4.6. Acceptance verification of incremental context reuse MUST cover this check: Incremental runs select relevant documents without dropping required coverage or full regression tests.
  {S1:L754}

## 1.5. Compact evidence and usage verification

- [A] 1.5.1. Acceptance verification of compact evidence and token telemetry MUST cover this check: Compact outputs retain evidence references and label omitted detail; full available sanitized evidence remains inspectable.
  {S1:L755}

- [A] 1.5.2. Acceptance verification of compact evidence and token telemetry MUST cover this check: Adapter-reported token usage is recorded accurately, and missing usage remains unavailable rather than fabricated as zero.
  {S1:L755}

- [A] 1.5.3. Acceptance verification of compact evidence and token telemetry MUST cover this check: Distinguish actual token measurements from proxy evidence.
  {S1:L755}

# 2. Product state and workspace mechanisms

## 2.1. State layout and durable record ownership

- [A] 2.1.1. Central product state MUST use `config.yaml`, `state.yaml`, and immediate `input/`, `output/`, `requests/`, `documentation/`, `ledger/`, `instructions/`, and `tmp/` under `.aih_product/`; `requests/` replaces `change_requests/` without adding extra memory/checkpoint/execution/communication/skills roots, parallel request roots, or overlapping immediate core names.
  {S1:L96-108, S2:section "Clarified request storage"}
  Details: {D1:section "Product and request ownership"}

- [A] 2.1.2. Configuration MUST hold declarative settings/registry, state MUST hold current execution/workspace/reconciliation references, and detailed history MUST stay in its owning records rather than enlarge global state indefinitely.
  {S1:L114}

- [A] 2.1.3. Global state MUST hold active request/phase/status/artifacts, submission/analysis/plan revisions, current validated workspace settings, root availability/baselines/impacts, current round/draft references/task/blockers/next action/checkpoint/run/segment/profile/revision, verification hashes/documentation/notices, with Q&A/system and baseline/test statuses distinct.
  {S1:L580, S3:section "Accepted policy"}

- [A] 2.1.4. Request conventions MUST specify metadata, submissions/attachments, evolving definitions, clarification/questionnaires/exchanges/amendment history, separate solution analysis, plans/tasks, responses, execution/checkpoints/verification/documentation/outcomes, creating artifacts on demand rather than empty templates.
  {S1:L134}

## 2.2. Temporary data and executable artifact placement

- [A] 2.2.1. Runnable tests, build outputs, environments, deployment scripts, IaC, fixtures, and product code MUST live in approved ordinary source/test/build locations outside inert `.aih_product/` and immutable core; portal assets MUST live in `.aih/engine/`.
  {S1:L30, S1:L110}

- [A] 2.2.2. Core/bundled-skill execution MUST disable Python bytecode generation and route durable runtime records to their owner and inert temporary data to `.aih_product/tmp/`, never redirecting executable bytecode into product state.
  {S1:L66}

- [A] 2.2.3. Inert temporary data MUST use unique operation-owned `.aih_product/tmp/` subdirectories with containment/sensitivity/access checks, exclude executable material, and be excluded from semantic inventories/baselines/content fingerprints.
  {S1:L112}

- [A] 2.2.4. Durable evidence, journals, checkpoints, reservations, and authorization MUST remain in owning records rather than solely temporary storage; cleanup MUST reconcile ownership, preserve active/uncertain data, and recover interrupted removal without path escapes.
  {S1:L112}

- [A] 2.2.5. Acceptance verification of temporary-data cleanup MUST cover this check: Temporary directories are uniquely owned by operations, excluded from semantic/source fingerprints and documentation inventories, and cleaned through confined deterministic helpers.
  {S1:L769}

- [A] 2.2.6. Acceptance verification of temporary-data cleanup MUST cover this check: Active operation data is protected, interrupted cleanup is recoverable, and temporary data never holds the only copy of durable evidence, checkpoints, or authorization.
  {S1:L769}

- [A] 2.2.7. Acceptance verification of temporary-data cleanup MUST cover this check: Executable temporary artifacts remain in authorized ordinary writable-root paths outside `.aih_product/`; Python bytecode writing into product state or the immutable core is disabled.
  {S1:L769}

## 2.3. Registry schema, identity, and administration

- [A] 2.3.1. Workspace schema MUST be authored in `.aih/conventions/` with values in `.aih_product/config.yaml`, including product/workspace identity, home, stable IDs, names, canonical paths, purposes, and access. Observed accessibility, freshness, and diagnostics MUST remain distinct from human permissions. Workspace configuration revision identifiers and a separate configuration history are not required.
  {S1:L118, S3:section "Accepted policy"}

- [A] 2.3.2. Folder IDs MUST survive deliberate relocation and MUST NOT be reassigned to unrelated content.
  {S1:L118}

- [A] 2.3.3. Workspace saves MUST reject stale edits and record the human change and affected review needs in the existing ledger and owner records without adding an immediate product directory. Stale-save detection MUST compare against the current configuration; it does not require a permanent history of configuration versions or location mappings.
  {S1:L124, S1:L130, S3:section "Accepted policy"}

- [A] 2.3.4. Workspace administration MUST validate canonical disjoint roots, host permissions, mandatory writable home, stable identity, and access before a recoverable save. Applying changes MUST require no open request and no active operation. Affected documentation, dependencies, and test coverage MUST be marked for review.
  {S1:L588, S3:section "Accepted policy"}

- [A] 2.3.5. Workspace candidate validation MUST be a bounded administration operation rather than a generic filesystem browser. Save MUST recheck that the current configuration has not changed and revalidate access and identity, without pre-registration mutation probes.
  {S1:L633, S3:section "Accepted policy"}

- [A] 2.3.6. Acceptance verification of Workspace administration MUST cover this check: Settings → Workspace lists stable root IDs, names, paths, purposes, and access modes, and supports explicit human Add folder, Edit, Validate access, and Remove from workspace operations.
  {S1:L771}

- [A] 2.3.7. Acceptance verification of Workspace administration MUST demonstrate that changes are accepted only when no request is open and global execution ownership is idle. Open requests MUST block changes even when their workers are stopped, blocked, or Ready to close.
  {S1:L771, S3:section "Accepted policy"}

- [A] 2.3.8. Acceptance verification of Workspace administration MUST demonstrate that an open request, a busy worker, uncertain termination, a reserved external handoff, or another operational action prevents configuration changes through the UI and backend. Direct file edits MUST NOT bypass these conditions or silently change execution authority.
  {S1:L771, S3:section "Accepted policy"}

- [A] 2.3.9. Acceptance verification of Workspace administration MUST demonstrate that validation and saving cannot race with request creation or execution. Agents cannot expand their own workspace, and saving configuration never starts an agent or grants implementation scope.
  {S1:L771, S3:section "Accepted policy"}

- [A] 2.3.10. Verification MUST demonstrate that the mandatory framework-home root cannot be removed or made read-only.
  {S1:L772}

## 2.4. Mapping changes and evidence validity

- [A] 2.4.1. Product artifact references MUST encode stable root ID plus relative path. Operations MUST resolve access through the current validated workspace configuration. Historical request records MUST remain intact without requiring a separate archive of configuration revisions or previous folder locations; old records MUST NOT grant current access or prove unchanged content after a move.
  {S1:L26, S3:section "Accepted policy"}

- [A] 2.4.2. Acceptance verification MUST demonstrate that operations use the current validated workspace configuration and that historical request records survive configuration changes without requiring configuration revision identifiers or historical location mappings.
  {S1:L772, S3:section "Accepted policy"}

- [A] 2.4.3. Acceptance verification MUST test adding, removing, relocating, and changing access to folders between requests. Affected documentation, dependencies, test coverage, and reusable extraction MUST be marked for review before reliance, and the next request MUST remain blocked until the required review is complete. The same configuration changes MUST be rejected while a request is open.
  {S1:L772, S3:section "Accepted policy"}

- [A] 2.4.4. Acceptance verification of workspace evidence invalidation MUST cover this check: Relocation revalidates actual content and access rather than treating an old relative path as proof of unchanged identity.
  {S1:L772}

- [A] 2.4.5. Acceptance verification of workspace evidence invalidation MUST cover this check: Unaffected evidence may remain valid with recorded justification.
  {S1:L772}

- [A] 2.4.6. Verification MUST demonstrate that missing or inaccessible roots produce actionable blocked states.
  {S1:L772}

## 2.5. New roots and retained obligations

- [A] 2.5.1. Acceptance verification MUST demonstrate that a newly added product root receives its required documentation baseline through an explicitly authorized setup or documentation-maintenance action when no request is open.
  {S1:L773, S3:section "Accepted policy"}

- [A] 2.5.2. Verification MUST demonstrate that the next request cannot start until affected documentation baselines, dependencies, and required test coverage have been reviewed for the current workspace.
  {S1:L773, S3:section "Accepted policy"}

- [A] 2.5.3. Acceptance verification of new-root documentation baselines MUST cover this check: Read-only source roots support evidence-based documentation written to the central product state, while test collection, build tools, cache generation, and attempted repairs cannot write back into them.
  {S1:L773}

- [A] 2.5.4. Acceptance verification of new-root documentation baselines MUST cover this check: Test host adapters with genuine multi-root access support and reject incompatible configurations without silently relocating content, broadening permissions, or reducing required tests.
  {S1:L773}

- [A] 2.5.5. Acceptance verification MUST demonstrate that removing workspace membership never deletes source files, historical request records, documentation-increment evidence, required failing-test obligations, or unresolved defects. A separate history of root-location mappings is not required.
  {S1:L774, S3:section "Accepted policy"}

- [A] 2.5.6. Acceptance verification of root removal and retained obligations MUST cover this check: Show affected dependencies and preserve their disposition for explicit review; removing a root cannot manufacture successful verification or closure.
  {S1:L774}

- [A] 2.5.7. Acceptance verification of root removal and retained obligations MUST cover this check: Archived requests remain intelligible through stable root-qualified references without granting access to removed locations.
  {S1:L774}

# 3. Filesystem confinement

## 3.1. Resolved targets and host enforcement

- [A] 3.1.1. Containment validation MUST resolve existing parents, symlinks, Windows junctions/reparse points, aliases, and hard links for registrations and access targets, including mutation sources/destinations/cleanup, and account for changes between validation and use.
  {S1:L24}

- [A] 3.1.2. Confinement/core/instruction protection MUST combine resolved-target helper validation and supported host permissions, covering aliases/junctions/links/indirect effects; checksums MUST NOT be represented as enforcement against unrestricted actors.
  {S1:L604}

- [A] 3.1.3. Acceptance verification of multi-root confinement MUST cover this check: The workspace is the union of explicitly registered canonical roots, with managed creates, writes, renames, deletions, and cleanup confined to its writable subset, including subprocesses and indirect runtime effects.
  {S1:L767}

- [A] 3.1.4. Acceptance verification of multi-root confinement MUST cover this check: The parent containing `.aih/` remains the mandatory writable framework home, not an authorization for other unregistered locations.
  {S1:L767}

- [A] 3.1.5. Acceptance verification of multi-root confinement MUST cover this check: Exercise noncontiguous roots, path traversal, prefix lookalikes, symlink/junction/reparse escapes, alternate aliases and hard links where supported, and changed targets between validation and use.
  {S1:L767}

- [A] 3.1.6. Acceptance verification of multi-root confinement MUST cover this check: Validate disjoint root registration and reject duplicate, nested, or aliasing roots that make membership/access ambiguous; resolving a path never grants access to an unregistered common ancestor.
  {S1:L767}

- [A] 3.1.7. Acceptance verification of multi-root confinement MUST cover this check: Check final targets and parent paths for create/rename/delete operations, including both roots involved in a move.
  {S1:L767}

- [A] 3.1.8. Acceptance verification of multi-root confinement MUST cover this check: Report platform-specific checks actually run; a lexical prefix check alone cannot establish confinement.
  {S1:L767}

## 3.2. Runtime and optional Git side effects

- [A] 3.2.1. Runtime launch MUST configure or disable temp/cache/session/browser/dependency-manager side effects before execution and preserve host permission checks for all child processes.
  {S1:L28, S1:L566}

- [A] 3.2.2. Optional Git helpers MUST confine worktree/config/cache/hook/credential/SSH side effects to current authorized writable roots even when remote operations are separately authorized.
  {S1:L707}

- [A] 3.2.3. Acceptance verification of external-runtime side effects MUST cover this check: Installed outside-workspace runtimes and host-permitted prerequisites may be read/invoked without granting outside-workspace mutation.
  {S1:L768}

- [A] 3.2.4. Acceptance verification of external-runtime side effects MUST cover this check: Exercise redirected or disabled temporary files, caches, session records, bytecode, global configuration, credential refresh, and optional Git/tool side effects.
  {S1:L768}

- [A] 3.2.5. Acceptance verification of external-runtime side effects MUST cover this check: A tool or adapter that cannot honor the registered roots, read-only modes, or host permissions is visibly blocked; a single-directory sandbox is never widened to a common ancestor to imitate multi-root support.
  {S1:L768}

- [A] 3.2.6. Acceptance verification of external-runtime side effects MUST cover this check: Credentials are not copied into tracked product files to work around confinement; direct external user application behavior is not falsely claimed to be controlled by AIH.
  {S1:L768}

# 4. Execution ownership and recoverable state

## 4.1. Action reservation and duplicate prevention

- [A] 4.1.1. CLI, API, helpers, and portal MUST enforce the same busy gate and idempotent accepted-operation identity; normal adoption/release MUST use an acknowledged recorded whole-task/segment boundary or explicit incomplete Stop checkpoint.
  {S1:L166}

- [A] 4.1.2. A shared atomic operational reservation MUST precede submission/launch acceptance across every root; startup MUST count as busy, same-ID retries MUST reuse recorded ownership, and drafts MUST NOT become queued commands.
  {S1:L582-584}

- [A] 4.1.3. Verification MUST demonstrate that only one request can be open.
  {S1:L720}

- [A] 4.1.4. Verification MUST demonstrate that AIH creates no request backlog.
  {S1:L720}

- [A] 4.1.5. Verification MUST demonstrate that consequential blockers stop change work.
  {S1:L720}

- [A] 4.1.6. Verification MUST demonstrate that repeated commands do not launch duplicate processes.
  {S1:L720}

- [A] 4.1.7. Acceptance verification of single request and operational ownership MUST cover this check: Starting, running, stopping, uncertain termination, and reserved external handoff all exclude a second operational action across change work, Q&A, setup, and maintenance.
  {S1:L720}

- [A] 4.1.8. Acceptance verification of single request and operational ownership MUST cover this check: Busy portal controls expose only Stop as an operational action; Save, import, submit, Ask, approval, closure, and configuration changes are disabled, and the backend enforces the same rule.
  {S1:L720}

- [A] 4.1.9. Acceptance verification of single request and operational ownership MUST cover this check: Passive navigation, help, status/log viewing, and existing-artifact viewing/download remain available.
  {S1:L720}

- [A] 4.1.10. Acceptance verification of single request and operational ownership MUST cover this check: Duplicate requests can return the existing action identity without starting another action.
  {S1:L720}

## 4.2. Transactions, checkpoints, and stale ownership

- [A] 4.2.1. Persistence MUST use safe YAML parsing, validation, atomic file replacement, optimistic revisions, and locking; multi-file operations MUST use a journal or equivalent recoverable protocol rather than assume single-file atomicity covers them.
  {S1:L586}

- [A] 4.2.2. Recovery MUST implement documented process-identity-aware stale-lock handling, interrupted-transaction reconciliation, and content/revision conflict detection for direct edits.
  {S1:L592}

- [A] 4.2.3. Checkpoints MUST precede consequential partial operations/interruption and retain completed/outstanding work, content versions, uncertain effects, and acknowledged boundaries; every recovery step MUST revalidate current roots/access/authority and inspect prior success before idempotent retry.
  {S1:L594-596}

- [A] 4.2.4. Acceptance verification of state transaction recovery MUST cover this check: Atomic writes, revision conflicts, transaction recovery, stale-lock handling, and duplicate-action reconciliation work under simulated interruptions/concurrency.
  {S1:L737}

## 4.3. Cross-filesystem progress and recovery

- [A] 4.3.1. Cross-root transactions MUST journal root identities, source/destination versions, completed effects, and outstanding steps durably in central product state, without assuming cross-filesystem rename/whole-product atomicity.
  {S1:L586}

- [A] 4.3.2. Acceptance verification of cross-filesystem recovery MUST cover this check: Interrupt a task or transaction spanning roots on different filesystems.
  {S1:L775}

- [A] 4.3.3. Acceptance verification of cross-filesystem recovery MUST cover this check: Preserve per-root progress and reconcile partial outcomes without claiming an atomic cross-filesystem commit, silently rolling back, or executing duplicate changes.
  {S1:L775}

- [A] 4.3.4. Acceptance verification of cross-filesystem recovery MUST demonstrate that recovery uses current authorized access. If a location needed for recovery is no longer permitted, recovery MUST block the prohibited write and report the need for explicit authorized resolution. Recovery MUST NOT restore old permissions from a journal, and workspace changes MUST remain blocked while any request is open or execution ownership is active or uncertain.
  {S1:L775, S3:section "Accepted policy"}

- [A] 4.3.5. Acceptance verification of cross-filesystem recovery MUST cover this check: Scope, pending recovery, test obligations, and the single action/request rules remain enforced across every root.
  {S1:L775}

## 4.4. Process termination and Stop behavior

- [A] 4.4.1. Supported-platform process control MUST terminate child processes safely and make Stop idempotent without releasing uncertain ownership or conflating it with request closure.
  {S1:L602}

- [A] 4.4.2. Acceptance verification of Stop and unsuccessful closure MUST cover this check: Stopping execution differs from closing a request.
  {S1:L722}

- [A] 4.4.3. Acceptance verification of Stop and unsuccessful closure MUST cover this check: Stop may safely terminate an incomplete task or segment after its indivisible operation is finished or controlled termination is confirmed; unfinished work remains unfinished, and no subsequent action starts automatically.
  {S1:L722}

# 5. Request persistence and workflow

## 5.1. Input snapshots, responses, and archival

- [A] 5.1.1. Each request MUST be stored at `.aih_product/requests/<request-id>_<normalized-name>/` throughout its lifecycle, with a request catalog recording stable ID, display name, slug, scope/outcome summary, status, dates, location, and significant document/decision links; closure MUST NOT move it between active/history folders.
  {S1:L136, S2:section "Clarified request storage"}
  Details: {D2:section "Collection identity"}

- [A] 5.1.2. Request links MUST resolve through stable identities, and any explicitly authorized naming migration MUST preserve old-reference mappings; ordinary lifecycle changes MUST keep the request folder unchanged.
  {S1:L136, S2:section "Clarified request storage"}
  Details: {D2:section "Collection identity"}

- [A] 5.1.3. Current change input MUST use `.aih_product/input/current.md` and an attachments directory.
  {S1:L158}

- [A] 5.1.4. Submission snapshots MUST retain immutable saved inputs, reviewed answer/amendment/form references, attachment identities/hashes, action/time/request, root-qualified paths with idempotent command/submission identities.
  {S1:L162, S3:section "Accepted policy"}

- [A] 5.1.5. The current response MUST use `.aih_product/output/current.md`, archiving each prior version in its request and linking requestor forms as separate exchange artifacts.
  {S1:L170}

- [A] 5.1.6. Acceptance verification of current response history MUST cover this check: One current change response is maintained with history in request records.
  {S1:L724}

- [A] 5.1.7. Acceptance verification of archival and historical access MUST show that explicit successful or cancelled/rejected closure records archival/lifecycle status without moving the request folder, preserving IDs, links, outcomes, and summaries, subject only to the documented human-authorized sensitive-data correction exception.
  {S1:L748, S2:section "Clarified request storage"}
  Details: {D1:section "Product and request ownership"}

- [A] 5.1.8. Acceptance verification of archival and historical access MUST cover this check: Normal execution reads current documentation and the active request, including unresolved current-state notices; historical evidence is fetched on demand through its catalog.
  {S1:L748}

- [A] 5.1.9. Verification MUST demonstrate that historical browsing does not reopen requests or queue work.
  {S1:L759}

## 5.2. Clarification definition and semantic boundaries

- [A] 5.2.1. The repeated requirements-understanding CLI operation MUST be named `clarify`.
  {S1:L229}

- [A] 5.2.2. The canonical evolving request definition MUST be the request documentation/ collection of requirements.md, decisions.md, context.md, unresolved.md, catalog.yaml, and needed typed extensions; any analysis/interpretation.md MUST only navigate to that collection, retaining source-linked history and distinguishing accepted findings from proposed/inferred ones without a competing editable definition.
  {S1:L233, S1:L265, S2:section "Migration and request-specific documentation"}
  Details: {D4:section "Compute the change set"}

- [A] 5.2.3. Acceptance verification of Clarify semantic boundaries MUST cover this check: Clarification artifacts and questionnaires capture what and why, scope, constraints, and observable acceptance criteria without selecting an implementation.
  {S1:L740}

- [A] 5.2.4. Acceptance verification of Clarify semantic boundaries MUST cover this check: Preserve explicit user technical constraints and distinguish them from observed existing technology.
  {S1:L740}

- [A] 5.2.5. Acceptance verification of Clarify semantic boundaries MUST cover this check: Exercise read-only investigation, Analysis-owned design choices, and a requirement gap discovered during Analysis that returns to clarification.
  {S1:L740}

- [A] 5.2.6. Acceptance verification of Clarify semantic boundaries MUST cover this check: Clarify may add evidence-backed known-defect entries or stale-topic markers with source/request references, but may not repair the product, redesign it, rewrite substantive business documentation, or treat an inference as approved intent.
  {S1:L740}

- [A] 5.2.7. Acceptance verification of Clarify semantic boundaries MUST cover this check: Test structural/state contracts automatically; claim the semantic phase boundary was followed only when an actual agent exercised it.
  {S1:L740}

- [A] 5.2.8. Acceptance verification of iterative clarification MUST cover this check: Repeat Clarify through initial questions, framework-user answers, imported requestor answers, changed wishes/additional information, partial responses, and an unchanged invocation.
  {S1:L760}

- [A] 5.2.9. Acceptance verification of iterative clarification MUST cover this check: Preserve the single interpretation and prior revisions, reassess stale answers and affected downstream approval/evidence, and finish ready for Analysis without invoking Analyze or implementation automatically.
  {S1:L760}

## 5.3. Amendments and captured revisions

- [A] 5.3.1. Amendment conventions MUST define request-owned drafts, immutable captured revisions, a compact catalog, stable identities/statuses, and append-only supersession/withdrawal events linked to rounds/sources without duplicating requirements.
  {S1:L243}

- [A] 5.3.2. Acceptance verification of draft submission and revision boundaries MUST cover this check: Draft edits never trigger work; explicit actions accepted only while idle snapshot revisions.
  {S1:L719}

- [A] 5.3.3. Acceptance verification of draft submission and revision boundaries MUST cover this check: No new submission or replacement command is accepted or queued while an action is busy.
  {S1:L719}

- [A] 5.3.4. Acceptance verification of draft submission and revision boundaries MUST cover this check: At the next explicit idle action, submitted amendments invalidate affected approvals/evidence and are adopted through a recorded, acknowledged complete-task or complete-segment handoff, or reconciliation of the explicitly incomplete checkpoint after a safe Stop.
  {S1:L719}

- [A] 5.3.5. Acceptance verification of draft submission and revision boundaries MUST cover this check: An external edit during execution remains unsubmitted and cannot silently alter the executing instruction.
  {S1:L719}

- [A] 5.3.6. Acceptance verification of amendment history MUST cover this check: Preserve amendment IDs, every accepted framework-saved/submitted revision and observed external edit, original wording, source, sequence, supersession/withdrawal, and interpretation effects, subject to sensitive-input rejection and explicitly authorized historical redaction.
  {S1:L764}

- [A] 5.3.7. Acceptance verification of amendment history MUST cover this check: Exercise an amendment contradicting an imported answer, direct edits of current input, repeated submission of the same amendment, and explicit correction of earlier wishes.
  {S1:L764}

- [A] 5.3.8. Acceptance verification of amendment history MUST cover this check: Verify traceability survives completed/cancelled/rejected archival and ordinary later runs use current interpretation rather than reapplying historical amendments.
  {S1:L764}

## 5.4. Analysis records and design assessment

- [A] 5.4.1. The repeated analysis-and-plan CLI operation MUST be named `analyze`; a standalone `plan` operation MUST NOT remain in the workflow.
  {S1:L253}

- [A] 5.4.2. `analysis/questions.md` MUST catalog stable question IDs/revisions/category/context/respondent/status/submitted summaries and authoritative Markdown answer/export/round/amendment links without a second independently editable answer store.
  {S1:L266}

- [A] 5.4.3. `analysis/solution_assessment.md` MUST preserve evidence-based feasibility, alternatives/tradeoffs, applicable practices, recommendations, and unresolved design with security/performance/integrity/maintainability/dependency/compatibility/deployment/migration/recovery considerations and observed/assumed distinctions.
  {S1:L267}

- [A] 5.4.4. Separate `impact_analysis.md`, `risks_and_decisions.md`, and `verification_strategy.md` MUST be used when substantive detail warrants them; simple changes MUST use concise equivalent assessment/plan sections covering current/affected behavior, interfaces, dependencies, risks/rationale, and requirement-to-verification mapping.
  {S1:L274}

- [A] 5.4.5. Acceptance verification of iterative Analysis MUST cover this check: Repeated Analyze invocations handle initial analysis, submitted answers, additional directions, unchanged inputs, and plan generation/regeneration without a separate Plan command or automatic implementation.
  {S1:L741}

- [A] 5.4.6. Acceptance verification of iterative Analysis MUST cover this check: Preserve valid completed-task history and invalidate affected approvals/evidence.
  {S1:L741}

- [A] 5.4.7. Acceptance verification of analysis records and plan traceability MUST show that the request documentation collection is the single current change definition, any interpretation.md is navigation only, and the questions catalog points to authoritative submitted answers without another editable answer store.
  {S1:L742, S2:section "Migration and request-specific documentation"}
  Details: {D4:section "Compute the change set"}

- [A] 5.4.8. Acceptance verification of analysis records and plan traceability MUST cover this check: Validate required analysis records, optional supporting files, sequential task order, affected paths identified by stable root ID and relative path, the current validated workspace configuration, and requirements-to-task/test traceability.
  {S1:L742, S3:section "Accepted policy"}

## 5.5. Plans, tasks, and implementation authority

- [A] 5.5.1. Each generated plan MUST bind to interpretation, submission, instructions, relevant documentation/content revisions, and the current validated workspace configuration while retaining prior plan/task history.
  {S1:L259, S3:section "Accepted policy"}

- [A] 5.5.2. The sequential versioned implementation plan MUST be stored in `analysis/plan.md`, whether produced by Analyze or internally by direct implementation.
  {S1:L269}

- [A] 5.5.3. Task records MUST include stable ID, order, outcome, requirement/decision references, concrete changes, root-qualified existing/new paths, create/modify/move/delete types, dependencies, and completion evidence across all affected roots.
  {S1:L278}

- [A] 5.5.4. Acceptance verification of approval and direct authorization MUST cover this check: Plan approval alone does not implement; ordinary implementation requires current approval.
  {S1:L721}

- [A] 5.5.5. Acceptance verification of approval and direct authorization MUST cover this check: Implement directly records its authorized exception to separate analysis invocation/approval while persisting the required plan before product changes.
  {S1:L721}

- [A] 5.5.6. Acceptance verification of sequential implementation evidence MUST cover this check: Normal and direct implementation both persist plans with mandatory test and documentation tasks and execute tasks sequentially.
  {S1:L743}

- [A] 5.5.7. Acceptance verification of sequential implementation evidence MUST cover this check: No shortcut omits logs, results, tests, documentation, or user selection of unrelated defects.
  {S1:L743}

## 5.6. Unrelated issues and repair scope

- [A] 5.6.1. `analysis/unrelated_issues.md` MUST record stable issue IDs, evidence, affected areas, test impact, investigation, user disposition, and current known-defect links.
  {S1:L268}

- [A] 5.6.2. Acceptance verification of unrelated-defect disposition MUST cover this check: Unrelated defects require user scope disposition, unfixed established defects appear in current known-defect documentation, and a deferred defect failing a required test blocks completion without exception.
  {S1:L745}

- [A] 5.6.3. Acceptance verification of unrelated-defect disposition MUST cover this check: Recording the blocker must not launch unauthorized repairs or another request.
  {S1:L745}

## 5.7. Successful closure and current evidence

- [A] 5.7.1. Acceptance verification of readiness and explicit successful closure MUST cover this check: Passing all required tests, valid verification, documentation, and evidence produces Ready to close while retaining the sole open-request slot.
  {S1:L723}

- [A] 5.7.2. Acceptance verification of readiness and explicit successful closure MUST cover this check: Only the explicit human Close successfully action revalidates the gates, archives the request, and releases that slot.
  {S1:L723}

- [A] 5.7.3. Acceptance verification of readiness and explicit successful closure MUST cover this check: Changed sources or invalidated evidence remove readiness.
  {S1:L723}

- [A] 5.7.4. Acceptance verification of readiness and explicit successful closure MUST cover this check: Neither zero exit status nor automatic completion of the last task closes a request.
  {S1:L723}

## 5.8. Unsuccessful closure and current-state notices

- [A] 5.8.1. Acceptance verification of Stop and unsuccessful closure MUST cover this check: Cancelled/rejected closure preserves partial outcomes and creates a persistent current-state notice linking retained changes, affected documentation, unresolved defects, verification uncertainty, and archived evidence.
  {S1:L722}

- [A] 5.8.2. Verification MUST demonstrate that cancelled/rejected closure permits a subsequent request without requiring passing tests or a complete documentation rewrite merely to cancel.
  {S1:L722}

- [A] 5.8.3. Verification MUST demonstrate that subsequent authorized work reconciles knowledge affected by unsuccessful closure before relying on it.
  {S1:L722}

- [A] 5.8.4. Verification MUST demonstrate that cancelled/rejected closure preserves a current-state notice for unfinished documentation reconciliation.
  {S1:L746}

## 5.9. Request identity and documentation generation

- [A] 5.9.1. The request documentation generator MUST remain at `definitions/definitions_R20260925_2309/attachments/update_documentation.md` for now, replacing extract_context.md and accepting sources, request_id, and required request_name.
  {S2:section "Clarified request storage"}
  Details: {D4:section "Input and baseline"}

- [A] 5.9.2. Request-name normalization MUST follow the documented Unicode-to-ASCII hyphenated slug algorithm; exact IDs, normalized names, and the resulting folder identity MUST be validated before writing.
  {S2:section "Clarified request storage"}
  Details: {D2:section "Collection identity"}

- [A] 5.9.3. The generator MUST compare `.aih_product/documentation/` and write only `.aih_product/requests/<request-id>_<normalized-name>/documentation/`, preserving the request folder and all sibling records.
  {S2:section "Clarified request storage"}
  Details: {D4:section "Commit and subsequent integration"}

- [A] 5.9.4. A request documentation collection MUST contain the four entry files and catalog.yaml, creating extensions/<type>/<subject>.<format> only when changed or new detailed knowledge needs it.
  {S2:section "Clarified request storage"}
  Details: {D1:section "Product and request ownership"}

- [A] 5.9.5. Generation MUST record request identity and baseline/input fingerprints in the catalog without changing lifecycle status or bypassing request/action ownership.
  {S2:section "Clarified request storage"}
  Details: {D2:section "Collection identity", D2:section "Baseline and change operations"}

- [A] 5.9.6. Regeneration MUST recompute semantic changes from current supplied sources and the product baseline; prior request metadata may preserve D identity/retirement only, and closed or already applied history MUST NOT be silently overwritten.
  {S2:section "Clarified request storage"}
  Details: {D4:section "Typed detail and references"}

- [A] 5.9.7. Validation MUST reject duplicate or case-only request IDs, colliding folders, unsafe or empty normalized names, and unapproved slug changes for existing IDs.
  {S2:section "Clarified request storage"}
  Details: {D2:section "Collection identity"}

# 6. Questionnaire and exchange implementation

## 6.1. Authoritative questionnaires and form records

- [A] 6.1.1. Request-owned editable Markdown checkbox questionnaires MUST be authoritative, with exact formats in conventions and portal/CLI editing the same files through revision checks.
  {S1:L306}

- [A] 6.1.2. Immutable outgoing forms MUST use `clarification/exports/<form-id>/`, accepted originals/reviews `clarification/received/<receipt-id>/`, and rounds `clarification/rounds/<round-id>/` within the owner request, with versioned request/form/UTC filenames and no normal received record for rejected intake.
  {S1:L334}

- [A] 6.1.3. Exchange metadata MUST preserve submission/interpretation/question revisions, fingerprints, and audience, with exact rendering/matching conventions and the explicit historical-redaction exception.
  {S1:L334}

- [A] 6.1.4. Acceptance verification of questionnaire round trips MUST cover this check: Markdown questionnaires round-trip through file and portal editing, including free text, contradictory selections, partial submissions, respondent assignment, explanations, and revision conflicts.
  {S1:L726}

- [A] 6.1.5. Acceptance verification of questionnaire round trips MUST cover this check: The authoritative answer source remains the request Markdown; exported forms and raw returned files are linked exchange records.
  {S1:L726}

- [A] 6.1.6. Acceptance verification of requestor form export MUST cover this check: Generate a versioned plain-text requestor form at the end of a waiting clarification round with only the applicable marked questions.
  {S1:L761}

- [A] 6.1.7. Acceptance verification of requestor form export MUST cover this check: Check each question has an explanation, why it matters, answer instructions, and a neutral example where useful.
  {S1:L761}

- [A] 6.1.8. Acceptance verification of requestor form export MUST cover this check: Verify the file can be completed in an ordinary text editor, contains stable form/question references, keeps earlier exports, and does not require portal access.
  {S1:L761}

- [A] 6.1.9. Acceptance verification of requestor form export MUST cover this check: Review explanation usefulness with meaningful examples; structural checks alone cannot prove clarity for a non-technical reader.
  {S1:L761}

## 6.2. Answer matching, intake, and review

- [A] 6.2.1. Answer matching MUST use request/form identity and stable question ID/revision rather than filename, display order, or guessed meaning.
  {S1:L343}

- [A] 6.2.2. Unassigned accepted receipts MUST use defined temporary intake under existing `input/`, then recoverably move/link to the explicitly associated request while retaining identity/source.
  {S1:L349}

- [A] 6.2.3. Python helpers MUST own import parsing/matching/rendering/revision checks/audit; clarification skill and human review MUST own semantic explanations, interpretation, and ambiguity resolution.
  {S1:L353}

- [A] 6.2.4. Acceptance verification of answer-import review MUST cover this check: Exercise upload/drop and paste, review of matched answers, partial and unknown answers, duplicate IDs/receipts, missing references with manual matching, altered question text, stale forms, newer local answers, answers for withdrawn questions, wrong/closed-request forms, and free-text proposed amendments.
  {S1:L762}

- [A] 6.2.5. Acceptance verification of answer-import review MUST cover this check: Apply sensitive-input rejection before persistence; preserve accepted originals, distinguish attributed requestor from actual submitter, prevent unreviewed answer adoption, and verify these inputs cannot grant plan approval or implementation authority.
  {S1:L762}

- [A] 6.2.6. Acceptance verification of answer-import review MUST cover this check: Busy-state refusal must not retain the attempted import as a queued submission.
  {S1:L762}

## 6.3. Combined import and launch recovery

- [A] 6.3.1. Combined reviewed import/Clarify MUST atomically reserve one action before recoverably committing reviewed merge, immutable submission, and starting execution identity, then launching the worker with retry-safe receipt/amendment/run effects.
  {S1:L347}

- [A] 6.3.2. Acceptance verification of combined import-and-Clarify recovery MUST cover this check: Verify Save reviewed answers only saves drafts, while Import answers and clarify commits the reviewed merge and explicit submission when idle.
  {S1:L763}

- [A] 6.3.3. Acceptance verification of combined import-and-Clarify recovery MUST cover this check: Atomically reserve the single accepted action across merge, submission, and worker launch.
  {S1:L763}

- [A] 6.3.4. Acceptance verification of combined import-and-Clarify recovery MUST cover this check: Simulate revision changes during review, repeated clicks, interruption between merge/submission/worker launch, and a launch failure.
  {S1:L763}

- [A] 6.3.5. Acceptance verification of combined import-and-Clarify recovery MUST cover this check: Recover without lost newer edits, duplicate effects, a second writer, or a pending replacement command; report draft, submitted, starting, running, and failed states accurately.
  {S1:L763}

- [A] 6.3.6. Acceptance verification of combined import-and-Clarify recovery MUST cover this check: Recovery of the accepted action is not a queue of later actions.
  {S1:L763}

# 7. Read-only question execution

- [A] 7.1. Q&A MUST use `input/questions/current.md`, stable submitted records under `input/questions/`, answers under `output/questions/<question-id>/` as Markdown and useful inert files, and a compact navigation index distinct from change output.
  {S1:L176}

- [A] 7.2. Read-only question execution MUST use supported read-only agent permissions with the trusted worker writing communication records.
  {S1:L182}

- [A] 7.3. Acceptance verification of independent Q&A MUST cover this check: Independent Q&A works with no request and while a request is open or blocked with its worker stopped, writes answer files, preserves request state, and makes no product changes.
  {S1:L725}

- [A] 7.4. Acceptance verification of independent Q&A MUST cover this check: It is refused while any operational action or external reservation is busy.
  {S1:L725}

- [A] 7.5. Acceptance verification of independent Q&A MUST cover this check: External file changes affecting an answer's observed sources are detected and reported instead of presenting mixed observations as a verified snapshot.
  {S1:L725}

- [A] 7.6. Verification MUST demonstrate that independent Q&A remains available when blocked change work has safely stopped and no other action or external reservation is busy.
  {S1:L759}

# 8. Test execution and failure handling

## 8.1. Suite inventory, environments, and content evidence

- [A] 8.1.1. Executable current/regression tests MUST stay in ordinary workspace source locations, with one central suite inventory/acceptance mapping; archived evidence MUST NOT be used as executable historical test copies.
  {S1:L288}

- [A] 8.1.2. Each suite's validated test-run contract MUST declare environment, prerequisites, effects, isolation/cleanup, root-qualified working/source/output/cache/temp locations, access, and authorization, with centrally recorded results.
  {S1:L288, S3:section "Accepted policy"}

- [A] 8.1.3. Verification MUST use defined root-qualified content manifests/dependency fingerprints checked against the current validated workspace configuration, recording test selection/invocation/results/environment/checked versions under suite authorization and repair-budget contracts.
  {S1:L598, S3:section "Accepted policy"}

- [A] 8.1.4. Product-content fingerprints MUST exclude volatile logs, answer timestamps, bookkeeping revisions, and operation-owned temporary data; documentation freshness and tests MUST track distinct dependencies where appropriate.
  {S1:L600}

- [A] 8.1.5. Acceptance verification of drift and verification freshness MUST cover this check: Documentation drift and verification invalidation detect relevant non-Git file changes without self-invalidating on bookkeeping.
  {S1:L730}

- [A] 8.1.6. Acceptance verification of suite environment contracts MUST cover this check: Every registered test suite has a validated test-run contract naming its environment, prerequisites, expected effects, isolation/cleanup, and required authorization, including root-qualified filesystem/cache effects and required access modes, all validated against the current workspace configuration.
  {S1:L765, S3:section "Accepted policy"}

- [A] 8.1.7. Acceptance verification of suite environment contracts MUST cover this check: Missing permissions or infrastructure block required execution and closure.
  {S1:L765}

- [A] 8.1.8. Acceptance verification of suite environment contracts MUST cover this check: Tests run only in configured environments with authorized effects; independently authorized external-service effects do not permit filesystem writes outside registered writable roots or into read-only roots.
  {S1:L765}

## 8.2. Regression repairs and persistent budgets

- [A] 8.2.1. Repair tracking MUST use stable unresolved-failure identity with diagnosis/authorized repair/rerun evidence, persistent attempts across resumes, default three unsuccessful cycles, configured elapsed/reliable-token limits, no-progress detection, and recorded authorized extensions.
  {S1:L292}

- [A] 8.2.2. Acceptance verification of regression repairs and budgets MUST cover this check: Run retained regression tests from earlier requests as part of the complete maintained suite.
  {S1:L744}

- [A] 8.2.3. Acceptance verification of regression repairs and budgets MUST cover this check: Repair authorized failures and rerun the suite; test suppression or unexecuted required tests cannot produce successful completion.
  {S1:L744}

- [A] 8.2.4. Acceptance verification of regression repairs and budgets MUST cover this check: Exercise the configurable repair budget, defaulting to three unsuccessful repair cycles for the same unresolved failure, and no-progress detection.
  {S1:L744}

- [A] 8.2.5. Acceptance verification of regression repairs and budgets MUST cover this check: Reaching the applicable cycle, time, or available measured-token limit stops the worker as blocked with attempt history and evidence preserved.
  {S1:L744}

- [A] 8.2.6. Acceptance verification of regression repairs and budgets MUST cover this check: Only explicit authorized continuation extends a budget; it never silently resets the history or relaxes completion gates.
  {S1:L744}

- [A] 8.2.7. Verification MUST demonstrate that a failed required test cannot be accepted as an exception allowing successful completion.
  {S1:L759}

# 9. Documentation generation and maintenance

## 9.1. System-operation records and ownership

- [A] 9.1.1. Bootstrap/standalone-maintenance records MUST use stable system-operation IDs under `ledger/operations/<operation-id>/`, user summaries under `output/operations/<operation-id>/`, and linked append-only ledger events.
  {S1:L140}

- [A] 9.1.2. In-request documentation tasks MUST store evidence/increments in the request; system-operation status MUST remain distinct from request, Q&A, and product verification.
  {S1:L142}

- [A] 9.1.3. Acceptance verification of system-operation ownership MUST cover this check: Bootstrap and standalone documentation maintenance keep audit/checkpoint records in the single framework-home product state without a synthetic request, duplicate framework/product-state home, database, or Git.
  {S1:L752}

- [A] 9.1.4. Acceptance verification of system-operation ownership MUST cover this check: Every operation obeys global single-action ownership.
  {S1:L752}

- [A] 9.1.5. Acceptance verification of system-operation ownership MUST cover this check: Documentation work within an open request uses that request's authorization and documentation increment; core maintenance/upgrades remain prohibited until there is no open request and all other execution ownership has been released.
  {S1:L752}

## 9.2. Initial portal bootstrap and baseline checks

- [A] 9.2.1. First-run bootstrap MUST persist an exclusive recoverable operation before worker launch, perform Python initialization/registry validation/inventory, configured-agent synthesis, and documentation validation outside HTTP handlers, reusing operation identity on concurrent starts.
  {S1:L612-614}

- [A] 9.2.2. Acceptance verification of first-start baseline generation MUST cover this check: First portal startup without product state initializes the single framework-home state, inventories configured product roots, and starts configured-agent documentation generation once.
  {S1:L749}

- [A] 9.2.3. Acceptance verification of first-start baseline generation MUST cover this check: Refresh/restart/concurrent-start scenarios do not duplicate workers, operation IDs, or writes.
  {S1:L749}

- [A] 9.2.4. Acceptance verification of first-start baseline generation MUST cover this check: A request cannot be opened until the complete initial documentation baseline for the configured product roots passes its coverage/completeness gate; adding a root makes its required local coverage part of that gate.
  {S1:L749}

- [A] 9.2.5. Acceptance verification of first-start baseline generation MUST cover this check: Explicitly recorded unknown external facts do not alone prevent baseline completion; missing required local coverage does.
  {S1:L749}

- [A] 9.2.6. Acceptance verification of first-start baseline generation MUST cover this check: Setup, Q&A, and local drafting remain available when setup is pending and no action is busy, while active bootstrap obeys Stop-only operational controls.
  {S1:L749}

- [A] 9.2.7. Acceptance verification of bootstrap recovery MUST cover this check: Interrupted bootstrap resumes without overwriting human content.
  {S1:L750}

- [A] 9.2.8. Acceptance verification of bootstrap recovery MUST cover this check: Invalid existing state is reported rather than reset.
  {S1:L750}

- [A] 9.2.9. Acceptance verification of bootstrap recovery MUST cover this check: Missing profile, incompatible CLI, unavailable authentication, or permission limitations leave semantic work visibly pending with actionable guidance and no silent fallback.
  {S1:L750}

## 9.3. Reverse-engineering commands and provenance

- [A] 9.3.1. A Python `reverse-engineer` command MUST offer initial/incremental modes with deterministic inventory and status/resume interfaces, reused by first-portal bootstrap.
  {S1:L383}

- [A] 9.3.2. Reverse engineering MUST use deterministic authorized inventory/fact extraction followed by configured-agent semantic synthesis into the existing balanced documentation/applicability tree.
  {S1:L385-387}

- [A] 9.3.3. Incremental reverse engineering MUST compare content fingerprints/dependencies, update affected leaves/catalogs, and validate tree/links through scripts while persisting before/after evidence and progress.
  {S1:L391}

- [A] 9.3.4. Acceptance verification of reverse-engineering provenance MUST cover this check: Initial and incremental reverse engineering preserve implementation/source/test/instruction fingerprints across configured roots while writing evidence-based documentation, recording stable root IDs and relative paths under the current validated workspace configuration.
  {S1:L751, S3:section "Accepted policy"}

- [A] 9.3.5. Acceptance verification of reverse-engineering provenance MUST cover this check: Extracted facts, inferred requirements, unknowns, generated content, and actually verified behavior remain distinguishable.
  {S1:L751}

## 9.4. Dependency tracking and documentation increments

- [A] 9.4.1. Every request MUST keep `analysis/documentation_increment.yaml` for planned changes and their application/verification evidence.
  {S1:L270, S1:L373}

- [A] 9.4.2. Documentation dependencies/fingerprints MUST bind provenance to folder identity and the current validated folder location and access settings, allowing metadata scans while semantically reading only relevant content.
  {S1:L367, S3:section "Accepted policy"}

- [A] 9.4.3. Documentation increments MUST record affected canonical IDs/sections, proposed amendments/reasons, source requirements/decisions, owner tasks, actual status, before/after fingerprints/diffs, and verification, refreshed as scope/results change.
  {S1:L373}

- [A] 9.4.4. Acceptance verification of documentation increments MUST cover this check: Every request has a documentation increment with planned/applied/verified distinctions or a justified no-impact result.
  {S1:L746}

- [A] 9.4.5. Verification MUST demonstrate that a request documentation increment is reconciled against actual changes, evidence, and current documentation before successful closure.
  {S1:L746}

## 9.5. Catalog structure, traversal, and rebalancing

- [A] 9.5.1. Documentation MUST use requirements.md, decisions.md, and context.md as its entry layer, with a separate logical extension-navigation tree of small internal catalogs and terminal typed detail; extension nodes MUST have stable IDs, one structural parent, nonstructural cross-links, and one canonical topic copy.
  {S1:L403-405, S2:section "Accepted document organization and references"}
  Details: {D1:section "Entry layer and extension navigation"}

- [A] 9.5.2. Child catalog metadata MUST include node identity, location, title, scope summary, applicability/status, and when to read it.
  {S1:L407}

- [A] 9.5.3. Extension-navigation validators MUST enforce initially at most eight children per logical catalog, leaf-depth difference at most one, target 1,500-word prose leaves with justified indivisible exceptions and type-appropriate checks for other formats, and no cycles/missing targets/multiple parents/unreachable content/duplicate IDs. Validators MUST support configured limits and meaningful rebalance; entry files and physical type-directory counts MUST be excluded from those tree-size calculations.
  {S1:L409-420, S2:section "Accepted document organization and references"}
  Details: {D1:section "Entry layer and extension navigation"}

- [A] 9.5.4. Rebalancing MUST use revision-checked recoverable multi-file transactions, preserve continuing-topic IDs and old-reference mappings, resolve IDs independently of paths, and validate committed invariants.
  {S1:L418-420}

- [A] 9.5.5. Supported documentation readers MUST use shared read locks, versioned snapshots, or revision-change detection/retry to avoid partially rewritten trees.
  {S1:L420}

- [A] 9.5.6. Acceptance verification of documentation traversal MUST cover this check: Documentation traversal reaches relevant leaves without loading unrelated content; applicability and provenance remain visible.
  {S1:L727}

- [A] 9.5.7. Acceptance verification of extension growth and reorganization MUST exercise capacity boundaries and validate eight-child/depth limits in the logical extension tree, stable D IDs, unique parents, reachability, cross-links, preserved content, and repaired entry references independently of physical type-folder layout.
  {S1:L728, S2:section "Accepted document organization and references"}
  Details: {D1:section "Entry layer and extension navigation"}

- [A] 9.5.8. Acceptance verification of documentation transaction recovery MUST cover this check: Interrupted documentation transactions recover safely; external edits conflict or serialize without data loss.
  {S1:L729}

## 9.6. Reconstruction evidence checks

- [A] 9.6.1. Acceptance verification of reconstruction status MUST cover this check: The reconstruction documentation gate reviews completeness and traceability of business rules, interfaces, expected results, dependencies, and recovery prerequisites.
  {S1:L766}

- [A] 9.6.2. Verification MUST demonstrate that passing the reconstruction completeness/traceability review is reported as specified but not demonstrated until an independent reconstruction exercise supplies evidence.
  {S1:L766}

- [A] 9.6.3. Verification MUST demonstrate that an independent reconstruction exercise is not silently added as a mandatory initial completion gate.
  {S1:L766}

- [A] 9.6.4. Verification MUST demonstrate that ordinary implementation tests do not establish reconstructed equivalence.
  {S1:L766}

## 9.7. Typed extension storage and identity

- [A] 9.7.1. Product entry files and catalog.yaml MUST reside in `.aih_product/documentation/`, with typed detail under extensions/<type>/<subject>.<format> and optional meaningful product-area subdivisions within a type.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D1:section "Product collection"}

- [A] 9.7.2. Each extension MUST declare one predefined primary type with format/content/provenance checks; the initial registry MUST cover the types in D3 and be extended through explicit convention changes.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D3}

- [A] 9.7.3. Current extension filenames MUST use descriptive lowercase hyphenated subjects without dates, request IDs, or entry-number prefixes.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D1:section "Product collection"}

- [A] 9.7.4. The catalog MUST assign D-prefixed positive-integer identities shared across a collection; renames and moves MUST preserve them, and retirement MUST retain identity records and prevent reuse.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Document registry"}

- [A] 9.7.5. Request catalogs MUST have a distinct D namespace and explicitly map product_document_id for existing product details; numeric coincidence MUST NOT establish identity.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Document registry"}

- [A] 9.7.6. Format-specific files MUST retain required provenance in native metadata or the catalog without adding invalid fields to a standard artifact format.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Citation and backlink contract"}

- [A] 9.7.7. The documentation catalog and all product-state extension content MUST remain inert; executable scripts, tests, packages, and operational implementation artifacts MUST remain outside .aih_product/.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D1:section "Product collection"}

## 9.8. Catalog and document reference contract

- [A] 9.8.1. catalog.yaml MUST record collection identity, document IDs/types/formats/paths, maintenance and authority roles, status/freshness, observed fingerprints, source provenance, and reciprocal entry references under the D2 contract.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2}

- [A] 9.8.2. Entry Details metadata MUST use brace references such as `Details: {D3:field "customer_id"}`; a whole-document reference is OPTIONAL when all of that document applies, and source/acceptance evidence MUST remain separate.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Citation and backlink contract"}

- [A] 9.8.3. Each entry file MUST generate an unnumbered Referenced documents section listing exactly its cited D IDs with linked titles and types, and link that section from its contents.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Citation and backlink contract"}

- [A] 9.8.4. Catalog backlinks MUST identify entry filenames and complete hierarchical IDs, and updates MUST repair them together with forward references.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Citation and backlink contract"}

- [A] 9.8.5. External document records MUST preserve root-qualified location, authority, freshness, observed version, and external-request-controlled maintenance; normal documentation writes MUST NOT modify the external target.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D1:section "External materials"}

- [A] 9.8.6. Original request attachments MUST stay unchanged; any deliberate documentation copy MUST retain original location/version and an explicit source/copy relationship.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D1:section "Product collection"}

- [A] 9.8.7. Catalog navigation MUST provide one structural parent for managed detail, use cross-links for external/product references, and support progressive validated branches without changing the collection D namespace.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Navigation and applicability"}

- [A] 9.8.8. Product integration MUST copy required request evidence into immutable product sources/ and required detail into typed product extensions/ before publishing references; validators MUST reject product links resolving to request-folder files, while retaining request-ID/filename/digest provenance without request-file dependencies.
  {S2:section "Product reference boundary"}
  Details: {D2:section "Document registry"}

## 9.9. Delta representation and baseline integrity

- [A] 9.9.1. The request catalog MUST bind comparison to baseline entry/catalog and relevant extension fingerprints; missing expected baseline files MUST block generation rather than imply an empty product.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Baseline and change operations"}

- [A] 9.9.2. Every settled request entry MUST carry add/modify/remove Change metadata, with file-qualified baseline Target metadata for modifications/removals and source-supported change intent.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Baseline and change operations"}

- [A] 9.9.3. The catalog changes inventory MUST associate findings and typed fragments with operations, product targets, exact locators, and expected prior fingerprints.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Baseline and change operations"}

- [A] 9.9.4. Coverage metadata MUST account for add/modify/remove/unchanged/unresolved/excluded source findings; unchanged records MUST contain references instead of duplicate statements.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Baseline and change operations"}

- [A] 9.9.5. Unchanged product detail MUST use reference-only request records; partial changes MUST use scoped changed fragments, and only new detail may require a complete new document.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Baseline and change operations"}

- [A] 9.9.6. Necessary format scaffolding for a changed fragment MUST be minimal and identified; it MUST NOT become a wholesale copy of unchanged product knowledge.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Baseline and change operations"}

- [A] 9.9.7. Generation MUST use independent source/baseline-first review, followed by review of the entire candidate entry/catalog/extension collection, with renewed review after corrections.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D4:section "Prepare and verify"}

- [A] 9.9.8. Only the verified request documentation subtree MUST be replaced through revision-checked recoverable operations after rechecking sources, baseline, request state, and preserved sibling/history records.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D4:section "Commit and subsequent integration"}

- [A] 9.9.9. Later integration MUST translate request D identities, preserve unaffected product knowledge and source history, and recompare stale baselines; documentation generation MUST NOT itself perform integration.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D4:section "Commit and subsequent integration"}

## 9.10. Documentation collection verification

- [A] 9.10.1. Verification MUST detect missing, duplicate, retired-reused, or incorrectly scoped D IDs and invalid type/format combinations.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Validation and update integrity"}

- [A] 9.10.2. Verification MUST resolve document paths and semantic locators, source locators, entry targets, and reciprocal links against the recorded baseline and final output locations.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D2:section "Validation and update integrity"}

- [A] 9.10.3. Delta verification MUST check both changed-source coverage and justified unchanged exclusions, preserving all changed conditions, exceptions, scope, and certainty across entry and extension content.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D4:section "Prepare and verify"}

- [A] 9.10.4. Verification MUST check original attachment and external-material preservation, request-sibling preservation, stale-baseline detection, and recovery from interrupted collection replacement.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D4:section "Commit and subsequent integration"}

- [A] 9.10.5. Verification MUST distinguish specified documentation contracts from implemented behavior, and MUST NOT treat valid file structure or successful generation as proof of runtime implementation.
  {S2:section "Implementation conventions derived from the accepted design"}
  Details: {D1:section "Maintenance"}

# 10. Audit records and sensitive data

## 10.1. Ledger and incremental implementation evidence

- [A] 10.1.1. The ledger MUST use append-only structured change/decision events plus a generated readable index, stable event IDs, owner/submission/run/artifact/decision links, and recoverable idempotent state updates.
  {S1:L450-455, S3:section "Accepted policy"}

- [A] 10.1.2. Per-run/segment `implementation_log.jsonl` and `implementation_summary.md` MUST be defined in conventions and initialized before changes; helpers MUST flush observable intent/result/evidence/checkpoint events incrementally.
  {S1:L471-475}

- [A] 10.1.3. The worker/recovery path MUST reconcile persisted events and observed effects into a labeled reconstructed summary when crashes prevent an authored final summary.
  {S1:L477-479}

- [A] 10.1.4. Acceptance verification of incremental implementation records MUST cover this check: Every implementation attempt has durable incremental logs and a readable results summary.
  {S1:L747}

- [A] 10.1.5. Acceptance verification of incremental implementation records MUST cover this check: Simulate crashes between action intent and result, recover an explicitly reconstructed summary, retain uncertain outcomes, and prevent blind duplicate execution.
  {S1:L747}

## 10.2. Admission, redaction, and unsafe-content checks

- [A] 10.2.1. Sensitive intake MUST use bounded admission before durable storage and unsafe spooling, retaining only non-sensitive rejection metadata and sanitizing execution output separately from exact accepted human originals.
  {S1:L461-463}

- [A] 10.2.2. Authorized historical redaction MUST reconcile all affected AIH-owned retained/recovery copies, derived hashes/indexes, and a non-sensitive authorization audit without secret-bearing backups or regeneration of removed values.
  {S1:L465-467}

- [A] 10.2.3. Acceptance verification of unsafe content and sensitive-input handling MUST cover this check: Product content cannot become arbitrary commands, dynamic imports, privileged configuration, or executable portal content.
  {S1:L739}

- [A] 10.2.4. Acceptance verification of unsafe content and sensitive-input handling MUST cover this check: Seeded sensitive input detected before acceptance is rejected without persisting its content in normal AIH records or echoing it in displayed diagnostics; only non-sensitive rejection metadata is kept, and corrected resubmission is required.
  {S1:L739}

- [A] 10.2.5. Acceptance verification of unsafe content and sensitive-input handling MUST cover this check: Test best-effort detection limitations explicitly.
  {S1:L739}

- [A] 10.2.6. Acceptance verification of unsafe content and sensitive-input handling MUST cover this check: For secrets discovered in stored records, test the explicit human-authorized historical-redaction exception: remove the secret from affected AIH-owned copies and append a non-sensitive audit event without general rewriting of history or claiming erasure of external copies.
  {S1:L739}

# 11. Skill packaging and integration

## 11.1. Format, bundled resources, and standalone contracts

- [A] 11.1.1. Each skill MUST follow the published Agent Skills format with `SKILL.md`, valid YAML metadata, behavioral guidance, and AIH-specific fields through the standard metadata extension mechanism.
  {S1:L481-483}

- [A] 11.1.2. Shared formats/templates MUST be authored under `.aih/conventions/` and bundled as generated versioned conventions/guidance/Python helpers during core build/release, with source hashes/versions, equivalence checks, and rejection of stale/conflicting bundles.
  {S1:L489-495}

- [A] 11.1.3. Installed integration MUST use canonical contracts, standalone packages matching bundled resources, and lifecycle state transitions MUST remain in the engine integration layer.
  {S1:L493-497}

- [A] 11.1.4. The compact standalone contract MUST persist explicit roots/access, input/output, scope/effects, initiating instruction, constraints, applicable plan/approval/direct authority, and result/evidence references beside output without depending on global AIH state.
  {S1:L497-499}

- [A] 11.1.5. Standalone clarification MUST bundle rounds/forms/import/amendment guidance/helpers; standalone direct implementation MUST bundle necessary planning capability without requiring another installed skill.
  {S1:L519-521}

- [A] 11.1.6. Baseline discovery and documentation application MUST share contracts/helpers and reusable evidence under a common authorized operation instead of generating competing knowledge.
  {S1:L525}

## 11.2. Initial packages and capability ownership

- [A] 11.2.1. Skill package directory IDs MUST be `clarify-requirements`, `analyze-and-plan`, `implement-plan`, `test-and-verify`, `reverse-engineer-product`, `maintain-documentation`, `answer-product-questions`, and `git-workflow`, with only the last disabled by default.
  {S1:L503-517}

- [A] 11.2.2. `clarify-requirements` MUST own iterative requirements, reviewed answers/amendments, explained questionnaires, source-linked interpretation/rounds/dispositions, and unresolved requirements, allowing read-only investigation/narrow factual bookkeeping without design.
  {S1:L510}

- [A] 11.2.3. `analyze-and-plan` MUST own feasibility/alternatives/dependencies/risks/unrelated issues and sequential implementation/test/documentation/evidence planning with required analysis records, affected paths, mappings, verification strategy, and planned increments.
  {S1:L511}

- [A] 11.2.4. `implement-plan` MUST own authorized sequential changes and repairs with prerequisite checks, task evidence, incremental logs/results, and recoverable incomplete state in both normal/direct modes.
  {S1:L512}

- [A] 11.2.5. `test-and-verify` MUST own authorized test creation/update, complete-suite execution via helpers, failure investigation/scope reporting, acceptance/content evidence and unexecuted/stale checks; test-file changes/execution MUST respect current authorization.
  {S1:L513}

- [A] 11.2.6. `reverse-engineer-product` MUST own authorized baseline/refresh evidence discovery and interpretation, fingerprints/issues/gaps/limits, distinguishing observation/inference/unknowns without implementation changes.
  {S1:L514}

- [A] 11.2.7. `maintain-documentation` MUST own authorized increments, current knowledge/defects/applicability/traceability, catalogs/links/balance, and applied/verified/structural-change evidence.
  {S1:L515}

- [A] 11.2.8. `answer-product-questions` MUST own independent source-grounded read-only answers and question records under the global single-action rule without implementation, scope, instruction, or durable-documentation effects.
  {S1:L516}

- [A] 11.2.9. `git-workflow` MUST declare Git/repository and operation dependencies and produce evidence only for separately scoped authorized inspection/branch/diff/commit/push/PR work, with no authority from installation/enablement alone.
  {S1:L517}

## 11.3. Catalog generation, discovery, and enablement

- [A] 11.3.1. `.aih/skills/catalog.yaml` and `.aih/skills/README.md` MUST derive from package metadata with convention-defined schema covering stable ID/name/version/purpose, selection/exclusions, I/O and standalone parameters, effects/scope/authority, dependencies/compatibility, location and resource hashes/versions.
  {S1:L531-540}

- [A] 11.3.2. Catalog generation/validation MUST run in Python during build/install/upgrade/explicit core maintenance from the same metadata, including all eight packages; ordinary discovery/listing/execution MUST NOT regenerate or write core catalogs.
  {S1:L542}

- [A] 11.3.3. Read-only discovery MUST compare validated installed metadata with catalogs, permit an effective in-memory inventory of newly installed metadata, report identity/integrity/stale conflicts, and MUST NOT execute package code.
  {S1:L544}

- [A] 11.3.4. Dynamic skill enablement MUST be stored by stable ID in `.aih_product/config.yaml`; effective enabled/available/compatible state MUST derive from validated product configuration and diagnostics, not product-specific edits to core metadata.
  {S1:L546}

- [A] 11.3.5. Acceptance verification of skill discovery and catalogs MUST cover this check: Skill discovery exposes metadata without bodies and detects new, disabled, malformed, duplicate, and incompatible skills without changing `run.md`.
  {S1:L731}

- [A] 11.3.6. Acceptance verification of skill discovery and catalogs MUST cover this check: Validate all eight required initial packages, the seven enabled defaults, the disabled optional Git default, matching YAML/README catalogs, schema validity, resource/version fingerprints, and actionable stale-catalog diagnostics.
  {S1:L731}

- [A] 11.3.7. Acceptance verification of skill discovery and catalogs MUST cover this check: Ordinary discovery, portal listing, and enablement leave the core catalogs unchanged; explicit maintenance regenerates them deterministically.
  {S1:L731}

- [A] 11.3.8. Acceptance verification of skill discovery and catalogs MUST cover this check: CLI and portal show consistent installed/enabled/available states, and enablement alone cannot authorize work.
  {S1:L731}

## 11.4. Standalone portability verification

- [A] 11.4.1. Acceptance verification of standalone skill portability MUST cover this check: Copy each of the eight delivered skill directories outside the installed AIH core, but still inside a registered writable workspace root, and validate its declared input/output contract, usage example, resources, and helpers in clean fixtures without an installed AIH engine or fixed product-state path, supplying only declared dependencies.
  {S1:L732}

- [A] 11.4.2. Acceptance verification of standalone skill portability MUST cover this check: Validate the compact standalone invocation contract: explicit workspace roots and their access modes, root-qualified input/output locations, permitted scope/effects, relevant plan and current approval or direct-mode authorization where applicable, initiating instruction, and effective host permission boundaries recorded with results.
  {S1:L732}

- [A] 11.4.3. Acceptance verification of standalone skill portability MUST cover this check: No full AIH lifecycle or stronger identity assurance is implied.
  {S1:L732}

- [A] 11.4.4. Acceptance verification of standalone skill portability MUST cover this check: Use a separate workspace-contained repository fixture for `git-workflow`, including its declared operation-tool dependencies where needed.
  {S1:L732}

- [A] 11.4.5. Acceptance verification of standalone skill portability MUST cover this check: Detect altered bundled conventions.
  {S1:L732}

- [A] 11.4.6. Acceptance verification of standalone skill portability MUST cover this check: Claim behavioral portability only if an agent actually exercises the skill; distinguish package/helper checks from observed agent behavior.
  {S1:L732}

# 12. Agent adapters and handoffs

## 12.1. Adapter configuration and profile selection

- [A] 12.1.1. Agent integration MUST use a shared Python adapter contract with a functional Codex CLI implementation and manual-handoff route.
  {S1:L554}

- [A] 12.1.2. Profile schemas MUST hold adapter/trusted executable/model/settings/timeout/permissions, credential environment-variable references only, and supported cache/session locations inside writable roots, recording effective precedence per segment and checking access against the current validated workspace configuration.
  {S1:L556, S3:section "Accepted policy"}

- [A] 12.1.3. Adapter schemas MUST reject executable configuration, arbitrary command templates, and unrestricted argument strings, with privileged executable references resolved only through deliberate local administration.
  {S1:L558}

- [A] 12.1.4. Codex invocation MUST be verified against official documentation and installed help, use documented noninteractive/events/non-Git options where compatible, and verify resume syntax separately rather than reuse assumed start arguments.
  {S1:L562}

- [A] 12.1.5. Adapters MUST declare availability, start, streamable outputs/events, run/session IDs, exit, timeout, cancel, and supported native resume or clearly identified persisted-state restart behavior.
  {S1:L564}

- [A] 12.1.6. Acceptance verification of profile precedence MUST cover this check: Multiple profiles coexist; default, per-run, and capability assignments follow documented precedence.
  {S1:L733}

- [A] 12.1.7. Acceptance verification of profile precedence MUST cover this check: Changes are accepted only while idle and take effect for the applicable next segment at a recorded boundary, without altering a running segment.
  {S1:L733}

- [A] 12.1.8. Acceptance verification of adapter prerequisites MUST cover this check: Adapter selection supports a product directory without Git.
  {S1:L735}

- [A] 12.1.9. Acceptance verification of adapter prerequisites MUST cover this check: Missing CLIs, invalid settings, unsupported versions, and unavailable authentication produce actionable errors without silent fallback.
  {S1:L735}

## 12.2. Process invocation, events, and fault handling

- [A] 12.2.1. Process invocation MUST use argument arrays without shell interpolation, explicit root-qualified working directories, a minimal required operational/authentication environment, and the complete current validated root/access configuration.
  {S1:L566, S3:section "Accepted policy"}

- [A] 12.2.2. Agent invocations MUST identify `.aih/run.md`, required helpers, action, request/question/system-operation ownership, submission where applicable, profile/segment, roots/access/revision, and use explicit parent/run checks to prevent recursive spawning of the same run.
  {S1:L568}

- [A] 12.2.3. Portal execution MUST use documented noninteractive modes and acknowledged task/segment ownership boundaries, without assuming conversational state transfers across CLIs.
  {S1:L570}

- [A] 12.2.4. Resolved CLI versions and non-secret effective settings MUST be persisted, with events sanitized before storage/display and private reasoning excluded.
  {S1:L574}

- [A] 12.2.5. Acceptance verification of controlled CLI fault handling MUST cover this check: A controlled fake CLI tests streaming, Unicode and special-character arguments, spaces in paths, authentication/version errors, malformed events, nonzero exits, timeouts, cancellation, child processes, and resumption limitations.
  {S1:L734}

## 12.3. Manual reservation and Stop-release verification

- [A] 12.3.1. Manual reservations MUST persist initiating instruction/scope, owner/submission where applicable, plan/approval/direct authority, profile, roots/access/revision, and handoff ID before exposing executable instructions.
  {S1:L572}

- [A] 12.3.2. Acceptance verification of manual-handoff ownership MUST cover this check: Manual handoff is functional, accurately labeled, and cannot falsely mark work as executed or verified.
  {S1:L736}

- [A] 12.3.3. Acceptance verification of manual-handoff ownership MUST cover this check: Its durable reservation binds the request/scope, submission, applicable plan, and handoff ID, survives portal restart, and excludes every other operational action until the Stop/release flow confirms the external worker has stopped and reconciles returned files/evidence.
  {S1:L736}

- [A] 12.3.4. Acceptance verification of manual-handoff ownership MUST cover this check: Uncertain ownership or attribution remains explicit.
  {S1:L736}

- [A] 12.3.5. Verification MUST demonstrate that required handoff evidence intake and external-stop confirmation occur within the reserved Stop/release flow and do not enable unrelated actions.
  {S1:L736}

- [A] 12.3.6. Acceptance verification of manual-handoff ownership MUST cover this check: Cancelling a prepared but unstarted handoff releases its reservation safely.
  {S1:L736}

# 13. Portal implementation

## 13.1. Startup, workers, and event delivery

- [A] 13.1.1. Portal startup MUST use Python, bind loopback by default, support configured port/no-browser, and launch only browsers whose managed profile/cache writes are confined; unsupported browser launch MUST fall back to URL-only guidance.
  {S1:L608}

- [A] 13.1.2. Agent work MUST run in controlled workers/subprocesses outside HTTP handlers, with backend transactional idle/authorization checks and idempotent retries across refresh/click/retry behavior.
  {S1:L652}

- [A] 13.1.3. Sanitized portal execution-event delivery MUST use streaming or polling with readable progress summaries.
  {S1:L650}

- [A] 13.1.4. Acceptance verification of portal startup and confinement MUST cover this check: Portal browser/no-browser startup, port conflicts, shutdown, primary workflow, separate Q&A, safe Markdown, origin protections, and file-boundary checks are exercised.
  {S1:L738}

- [A] 13.1.5. Acceptance verification of portal startup and confinement MUST cover this check: Framework-launched browsers use registered writable-root profiles/cache; an uncontrolled browser launch that would write outside the workspace is replaced with the documented URL-only path.
  {S1:L738}

## 13.2. File endpoints, origins, and privileged settings

- [A] 13.2.1. Product-file endpoints MUST accept root ID plus relative path through the current validated registry/access/scope contract rather than unrestricted absolute paths; administration MUST limit absolute candidate paths to explicit bounded validation/registration.
  {S1:L656}

- [A] 13.2.2. The portal MUST validate origins/hosts and protect state-changing requests, safely render Markdown, and serve untrusted outputs without executing supplied active content.
  {S1:L656}

- [A] 13.2.3. Privileged executable/permission configuration MUST be separate from ordinary content endpoints, and credential storage MUST contain permitted references only.
  {S1:L658}

## 13.3. Rendered pages and workflow state checks

- [A] 13.3.1. Acceptance verification of portal pages and tabs MUST cover this check: Exercise all eight portal pages and six Current request tabs with meaningful workflow states, inspecting the rendered interface.
  {S1:L758}

- [A] 13.3.2. Acceptance verification of portal pages and tabs MUST cover this check: Verify explicit draft/submission differences, repeated Analyze and generated plan approval, direct-implementation explanation, defect scope selection, revision conflicts, profile effective boundaries, and distinct stop/closure actions.
  {S1:L758}

- [A] 13.3.3. Acceptance verification of portal state explanations MUST cover this check: Portal next-action/disabled-action explanations match validated state.
  {S1:L759}

- [A] 13.3.4. Acceptance verification of portal state explanations MUST cover this check: Confirm log/result views distinguish process status from task outcomes, Ready to close from closed, and bootstrap documentation from product verification.
  {S1:L759}

# 14. CLI, installation, and maintained help

## 14.1. Menu commands and home resolution

- [A] 14.1.1. Optional `.aih/menu.cmd` and `.aih/menu.sh` wrappers MUST be limited to locating/invoking the shared Python menu and minimal startup/runtime errors without workflow/state/agent/business logic.
  {S1:L39, S1:L664}

- [A] 14.1.2. The shared terminal menu MUST be the Python CLI `menu` operation with rendering, input validation, root resolution, settings, dispatch, lifecycle, and workflow errors implemented in Python.
  {S1:L664}

- [A] 14.1.3. Direct menu invocation MUST support `py .aih/engine/cli.py menu` on Windows and `python3 .aih/engine/cli.py menu` on Linux, with documented supported Python selection and Linux executable/terminal behavior.
  {S1:L666}

- [A] 14.1.4. Startup MUST locate canonical home from the directory containing `.aih/`, validate that registry, and accept alternate explicit home only for a valid installation; root-selection arguments MUST NOT register new folders.
  {S1:L670}

- [A] 14.1.5. The discoverable CLI MUST support `python .aih/engine/cli.py <command>` at home and explicit valid-home operation from other directories, with consistent exact arguments and `--help` per command.
  {S1:L682}

- [A] 14.1.6. Acceptance verification of menu launch wrappers MUST cover this check: Windows/Linux launch wrappers invoke the shared Python menu without duplicating logic; direct Python invocation also works.
  {S1:L756}

- [A] 14.1.7. Acceptance verification of menu launch wrappers MUST cover this check: Exercise root resolution from another working directory, paths with spaces/special characters, missing runtime diagnostics, repeated launch deduplication, and menu exit/shutdown behavior.
  {S1:L756}

- [A] 14.1.8. Acceptance verification of menu launch wrappers MUST cover this check: Report which OS launcher paths were actually exercised rather than inferring cross-platform success.
  {S1:L756}

## 14.2. Installation, upgrades, and host integration

- [A] 14.2.1. Installation MUST use a pinned core from an explicitly supplied local directory, validate destination home, and confine writes there without requiring a release URL or Git.
  {S1:L684}

- [A] 14.2.2. Host integration snippets MUST point to `.aih/run.md` and preserve existing instruction files.
  {S1:L703}

- [A] 14.2.3. Upgrade staging MUST keep inert data under home `.aih_product/tmp/` when state exists and executable incoming core/staging in authorized ordinary writable-root locations outside product state, with validated recoverable replacement/migrations/cleanup.
  {S1:L705}

- [A] 14.2.4. Verification MUST demonstrate that installation and repeated initialization preserve existing content.
  {S1:L715}

- [A] 14.2.5. Verification MUST demonstrate that core upgrades preserve product state and report required migrations or conflicts.
  {S1:L715}

- [A] 14.2.6. Acceptance verification of installation and core maintenance MUST cover this check: Core maintenance and upgrades are refused while any request is open or any setup, maintenance, or external execution owner remains active; an idle blocked request is still open.
  {S1:L715}

- [A] 14.2.7. Verification MUST demonstrate that a broken helper does not bypass the core-maintenance gate requiring no open request and no operational execution owner.
  {S1:L715}

## 14.3. Shared help sources and consistency

- [A] 14.3.1. Portal and menu help MUST render maintained `.aih/USER_GUIDE.md` and shared command metadata with stable checked section anchors instead of independent conflicting help sources.
  {S1:L629, S1:L678}

- [A] 14.3.2. User help MUST NOT be duplicated into behavioral prompts or loaded in full into every agent run.
  {S1:L678}

- [A] 14.3.3. Acceptance verification of shared help consistency MUST cover this check: README quick-start commands, USER_GUIDE command references, menu help, portal help, and contextual section links match the implemented catalog and installed version.
  {S1:L757}

- [A] 14.3.4. Acceptance verification of shared help consistency MUST cover this check: Help is accessible before initialization/authentication and does not invoke an agent or modify the core.
  {S1:L757}

# 15. Verification fixtures and live validation

## 15.1. Automated fixtures, live CLI, and browser checks

- [A] 15.1.1. Automated verification MUST exercise meaningful Python behavior/contracts in temporary plain non-Git and separate-root fixtures, keeping runnable fixtures outside core/product-state and all runtime/browser/cache effects in writable roots.
  {S1:L711}

- [A] 15.1.2. Live Codex verification MUST use an isolated confined compatible fixture when installed/authenticated/permitted, with a multi-root live case only where genuine adapter/host support exists and absent prerequisites reported explicitly.
  {S1:L777}

- [A] 15.1.3. Rendered portal walkthroughs MUST inspect primary screens including Workspace using browser profiles/caches inside authorized writable roots and report actual platform/storage coverage separately from automated checks.
  {S1:L779}

## 15.2. End-to-end, recovery, and existing-product scenarios

- [A] 15.2.1. The end-to-end synthetic fixture MUST exercise baseline, request creation, multiple clarification rounds, explained external forms, reviewed partial return, amendment supersession, iterative Analysis, plan approval, sequential tasks, full passing suite, applied documentation, Ready to close, and explicit human successful archival, waiting for each preceding action to finish/stop.
  {S1:L781}

- [A] 15.2.2. Additional fixtures MUST exercise direct-mode internal planning, idle blocked Q&A, unrelated-defect triage/deferred required failure, repair exhaustion/extension, interrupted incremental records, handoff reservation/release, history lookup, and cancelled closure with retained-state notice.
  {S1:L781}

- [A] 15.2.3. An existing-product fixture MUST exercise automatic first-portal initialization, baseline request gate, reverse engineering, profile-unavailable recovery, and incremental refresh.
  {S1:L781}

- [A] 15.2.4. A multi-root fixture MUST use writable frontend/backend, read-only reference, and unrelated unregistered sibling areas, exercise idle root addition during an open request, explicit baseline/reconciliation, cross-root implementation/tests, and denied outside/read-only writes; fixtures MUST be labeled examples rather than user-product requirements.
  {S1:L781}

# Referenced documents

- **D1:** [Documentation organization](extensions/architecture/documentation-organization.md) — architecture
- **D2:** [Documentation catalog contract](extensions/interface-contract/documentation-catalog.md) — interface-contract
- **D3:** [Documentation extension types](extensions/data-dictionary/document-types.yaml) — data-dictionary
- **D4:** [Request documentation update flow](extensions/processing-flow/request-documentation-update.md) — processing-flow

# Sources

- **S1:** `sources/AIH_Build_Prompt_v20260922_173409Z.md`
- **S2:** `sources/documentation-evolution.md`

- **S3:** `sources/workspace-administration-20260927.md` — accepted clarification; supersedes conflicting earlier workspace policy.
