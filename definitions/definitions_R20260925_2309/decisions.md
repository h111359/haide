- [A] 322. The canonical framework home MUST contain the sole `.aih/` versioned core and central `.aih_product/` product-state tree and be registered with stable writable ID `home`; these paths MUST resolve from home independently of process working directory.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:20,34-37`.

- [A] 323. Containment validation MUST resolve existing parents, symlinks, Windows junctions/reparse points, aliases, and hard links for registrations and access targets, including mutation sources/destinations/cleanup, and account for changes between validation and use.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:24`.

- [A] 324. Product artifact references MUST encode stable root ID plus relative path and workspace revision, retaining historical resolved mappings rather than rebinding old evidence after moves.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:26`.

- [A] 325. Runtime launch MUST configure or disable temp/cache/session/browser/dependency-manager side effects before execution and preserve host permission checks for all child processes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:28,566`.

- [A] 326. Runnable tests, build outputs, environments, deployment scripts, IaC, fixtures, and product code MUST live in approved ordinary source/test/build locations outside inert `.aih_product/` and immutable core; portal assets MUST live in `.aih/engine/`.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:30,110`.

- [A] 327. All framework behavior, helpers, adapters, workers, orchestration, bookkeeping, and backend components MUST be Python.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:39`.

- [A] 328. Optional `.aih/menu.cmd` and `.aih/menu.sh` wrappers MUST be limited to locating/invoking the shared Python menu and minimal startup/runtime errors without workflow/state/agent/business logic.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:39,664`.

- [A] 329. HTML, CSS, and JavaScript are OPTIONAL permitted implementation languages for the browser portal.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:39`.

- [A] 330. Product implementation languages MUST remain unrestricted.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:39`.

- [A] 331. Markdown and validated YAML/JSON files MUST be authoritative storage; AIH MUST NOT use SQLite, embedded databases, database caches, or other databases.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:41`.

- [A] 332. Search indexes are OPTIONAL and MUST be disposable files or in-memory structures if used.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:41`.

- [A] 333. Git integration MUST be packaged as an optional configurable skill extension rather than a required core dependency.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:43`.

- [A] 334. The immediate `.aih/` directories MUST be `prompts/` for on-demand behavior, `conventions/` for authoritative formats/contracts, `skills/` for packages/catalogs, and `engine/` for shared Python infrastructure and portal assets/tests.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:53-58`.

- [A] 335. Core root files MUST include the single `.aih/run.md` entry point, `.aih/README.md`, and `.aih/USER_GUIDE.md`; OS launchers and core version/integrity manifests are OPTIONAL, with menu infrastructure under `engine/` rather than additional immediate directories.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:60`.

- [A] 336. Prompts MUST reference authoritative conventions rather than redefine schemas/templates/structure; conventions MUST NOT depend on prompts, and validators MUST implement the same authoritative contracts.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:62`.

- [A] 337. `run.md` MUST remain concise/stable and route from submitted action, validated state/instructions, discovered metadata, and owning request/system operation without a hard-coded skill roster or profile names.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:64`.

- [A] 338. Core/bundled-skill execution MUST disable Python bytecode generation and route durable runtime records to their owner and inert temporary data to `.aih_product/tmp/`, never redirecting executable bytecode into product state.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:66`.

- [A] 339. Every deterministic framework operation MUST have named Python entry points/shared APIs used by agents and portal instead of ad hoc model-generated commands/scripts, manual state edits, or duplicated implementations.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:72-74`.

- [A] 340. Deterministic helper coverage MUST include initialization, registry/history/containment/path resolution/scope impact/temp handling, inventories/fact extraction/hashes/diffs, schema/input screening/redaction, submissions/questionnaires/forms/imports/amendments, revisions/ownership/handoffs/transitions/locks/transactions/edit application, catalogs/tasks/tests/repair budgets, logs/checkpoints/archival/diagnostics/upgrades.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:74`.

- [A] 341. Helpers MUST collect/validate facts and apply specified operations while agents interpret evidence, resolve ambiguity, choose authorized solutions, produce semantic content/patches, and diagnose failures; heuristic output MUST NOT establish business intent or semantic correctness by itself.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:76`.

- [A] 342. The deterministic-operation catalog MUST expose typed operation IDs, inputs/effects/permissions/results, concise status/changed artifacts/actionable errors/conflicts, and linked verbose evidence rather than generic command templates.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:78`.

- [A] 343. Context loading MUST read metadata/relevant catalog branches before leaves and skill bodies/resources only on demand, using fingerprints/dependency maps and still-valid summaries/checkpoints to select affected material.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:86`.

- [A] 344. Reusable summaries MUST preserve source/version, decisions, unresolved issues, and recovery context, and be invalidated for relevant source/instruction/workspace/extractor/schema/core changes, with cache identity scoped by root and registry revision.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:86`.

- [A] 345. Reusable summaries/indexes MUST be validated files or memory, never a database or ordinary write into core.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:88`.

- [A] 346. Central product state MUST use `config.yaml`, `state.yaml`, and immediate `input/`, `output/`, `change_requests/`, `documentation/`, `ledger/`, `instructions/`, and `tmp/` under `.aih_product/`, without extra memory/checkpoint/execution/communication/skills roots or overlapping immediate core names.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:96-108`.

- [A] 347. Inert temporary data MUST use unique operation-owned `.aih_product/tmp/` subdirectories with containment/sensitivity/access checks, exclude executable material, and be excluded from semantic inventories/baselines/content fingerprints.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:112`.

- [A] 348. Durable evidence, journals, checkpoints, reservations, and authorization MUST remain in owning records rather than solely temporary storage; cleanup MUST reconcile ownership, preserve active/uncertain data, and recover interrupted removal without path escapes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:112`.

- [A] 349. Configuration MUST hold declarative settings/registry, state MUST hold current execution/workspace/reconciliation references, and detailed history MUST stay in its owning records rather than enlarge global state indefinitely.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:114`.

- [A] 350. Workspace schema MUST be authored in `.aih/conventions/` with values in `.aih_product/config.yaml`, including product/workspace identity, home, stable IDs, names, canonical paths, purposes, access, and revision, separating observed accessibility/freshness/diagnostics from human permissions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:118`.

- [A] 351. Folder IDs MUST survive deliberate relocation and MUST NOT be reassigned to unrelated content.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:118`.

- [A] 352. Registry commits MUST revision-check before/after mappings and record explicit human change and affected dispositions in the existing ledger and owner records without adding an immediate product directory.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:124,130`.

- [A] 353. Request conventions MUST specify metadata, submissions/attachments, evolving definitions, clarification/questionnaires/exchanges/amendment history, separate solution analysis, plans/tasks, responses, execution/checkpoints/verification/documentation/outcomes, creating artifacts on demand rather than empty templates.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:134`.

- [A] 354. The active request MUST be stored at `change_requests/active/<request-id>/` and archived recoverably to `change_requests/history/<request-id>/`, with a `change_requests/` catalog of stable ID, scope/outcome summary, status, dates, location, and significant document/decision links.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:136`.

- [A] 355. Request links MUST resolve through stable identities so moving the record on archival does not break references.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:136`.

- [A] 356. Bootstrap/standalone-maintenance records MUST use stable system-operation IDs under `ledger/operations/<operation-id>/`, user summaries under `output/operations/<operation-id>/`, and linked append-only ledger events.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:140`.

- [A] 357. In-request documentation tasks MUST store evidence/increments in the request; system-operation status MUST remain distinct from request, Q&A, and product verification.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:142`.

- [A] 358. Current change input MUST use `.aih_product/input/current.md` and an attachments directory.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:158`.

- [A] 359. Submission snapshots MUST retain immutable saved inputs, reviewed answer/amendment/form references, attachment identities/hashes, action/time/request, effective registry revision, and root-qualified paths with idempotent command/submission identities.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:162`.

- [A] 360. CLI, API, helpers, and portal MUST enforce the same busy gate and idempotent accepted-operation identity; normal adoption/release MUST use an acknowledged recorded whole-task/segment boundary or explicit incomplete Stop checkpoint.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:166`.

- [A] 361. The current response MUST use `.aih_product/output/current.md`, archiving each prior version in its request and linking requestor forms as separate exchange artifacts.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:170`.

- [A] 362. Q&A MUST use `input/questions/current.md`, stable submitted records under `input/questions/`, answers under `output/questions/<question-id>/` as Markdown and useful inert files, and a compact navigation index distinct from change output.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:176`.

- [A] 363. Read-only question execution MUST use supported read-only agent permissions with the trusted worker writing communication records.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:182`.

- [A] 364. The repeated requirements-understanding CLI operation MUST be named `clarify`.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:229`.

- [A] 365. The canonical evolving request definition MUST be `analysis/interpretation.md`, with source-linked version history and clear accepted versus proposed/inferred requirements; no competing definition MUST be maintained.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:233,265`.

- [A] 366. Amendment conventions MUST define request-owned drafts, immutable captured revisions, a compact catalog, stable identities/statuses, and append-only supersession/withdrawal events linked to rounds/sources without duplicating requirements.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:243`.

- [A] 367. The repeated analysis-and-plan CLI operation MUST be named `analyze`; a standalone `plan` operation MUST NOT remain in the workflow.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:253`.

- [A] 368. Each generated plan MUST bind to interpretation, submission, instructions, workspace registry, and relevant documentation/content revisions while retaining prior plan/task history.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:259`.

- [A] 369. `analysis/questions.md` MUST catalog stable question IDs/revisions/category/context/respondent/status/submitted summaries and authoritative Markdown answer/export/round/amendment links without a second independently editable answer store.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:266`.

- [A] 370. `analysis/solution_assessment.md` MUST preserve evidence-based feasibility, alternatives/tradeoffs, applicable practices, recommendations, and unresolved design with security/performance/integrity/maintainability/dependency/compatibility/deployment/migration/recovery considerations and observed/assumed distinctions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:267`.

- [A] 371. `analysis/unrelated_issues.md` MUST record stable issue IDs, evidence, affected areas, test impact, investigation, user disposition, and current known-defect links.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:268`.

- [A] 372. The sequential versioned implementation plan MUST be stored in `analysis/plan.md`, whether produced by Analyze or internally by direct implementation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:269`.

- [A] 373. Every request MUST keep `analysis/documentation_increment.yaml` for planned changes and their application/verification evidence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:270,373`.

- [A] 374. Separate `impact_analysis.md`, `risks_and_decisions.md`, and `verification_strategy.md` MUST be used when substantive detail warrants them; simple changes MUST use concise equivalent assessment/plan sections covering current/affected behavior, interfaces, dependencies, risks/rationale, and requirement-to-verification mapping.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:274`.

- [A] 375. Task records MUST include stable ID, order, outcome, requirement/decision references, concrete changes, root-qualified existing/new paths, create/modify/move/delete types, dependencies, and completion evidence across all affected roots.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:278`.

- [A] 376. Executable current/regression tests MUST stay in ordinary workspace source locations, with one central suite inventory/acceptance mapping; archived evidence MUST NOT be used as executable historical test copies.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:288`.

- [A] 377. Each suite's validated test-run contract MUST declare environment, prerequisites, effects, isolation/cleanup, root-qualified working/source/output/cache/temp locations, registry revision, access, and authorization, with centrally recorded results.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:288`.

- [A] 378. Repair tracking MUST use stable unresolved-failure identity with diagnosis/authorized repair/rerun evidence, persistent attempts across resumes, default three unsuccessful cycles, configured elapsed/reliable-token limits, no-progress detection, and recorded authorized extensions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:292`.

- [A] 379. Request-owned editable Markdown checkbox questionnaires MUST be authoritative, with exact formats in conventions and portal/CLI editing the same files through revision checks.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:306`.

- [A] 380. Immutable outgoing forms MUST use `clarification/exports/<form-id>/`, accepted originals/reviews `clarification/received/<receipt-id>/`, and rounds `clarification/rounds/<round-id>/` within the owner request, with versioned request/form/UTC filenames and no normal received record for rejected intake.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:334`.

- [A] 381. Exchange metadata MUST preserve submission/interpretation/question revisions, fingerprints, and audience, with exact rendering/matching conventions and the explicit historical-redaction exception.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:334`.

- [A] 382. Answer matching MUST use request/form identity and stable question ID/revision rather than filename, display order, or guessed meaning.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:343`.

- [A] 383. Combined reviewed import/Clarify MUST atomically reserve one action before recoverably committing reviewed merge, immutable submission, and starting execution identity, then launching the worker with retry-safe receipt/amendment/run effects.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:347`.

- [A] 384. Unassigned accepted receipts MUST use defined temporary intake under existing `input/`, then recoverably move/link to the explicitly associated request while retaining identity/source.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:349`.

- [A] 385. Python helpers MUST own import parsing/matching/rendering/revision checks/audit; clarification skill and human review MUST own semantic explanations, interpretation, and ambiguity resolution.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:353`.

- [A] 386. Documentation dependencies/fingerprints MUST bind provenance to folder identity, location mapping, and registry revision, allowing metadata scans while semantically reading only relevant content.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:367`.

- [A] 387. Documentation increments MUST record affected canonical IDs/sections, proposed amendments/reasons, source requirements/decisions, owner tasks, actual status, before/after fingerprints/diffs, and verification, refreshed as scope/results change.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:373`.

- [A] 388. A Python `reverse-engineer` command MUST offer initial/incremental modes with deterministic inventory and status/resume interfaces, reused by first-portal bootstrap.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:383`.

- [A] 389. Reverse engineering MUST use deterministic authorized inventory/fact extraction followed by configured-agent semantic synthesis into the existing balanced documentation/applicability tree.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:385-387`.

- [A] 390. Incremental reverse engineering MUST compare content fingerprints/dependencies, update affected leaves/catalogs, and validate tree/links through scripts while persisting before/after evidence and progress.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:391`.

- [A] 391. Documentation MUST use internal navigation catalogs and terminal content leaves, a small root catalog, stable node IDs, exactly one parent per non-root node, nonstructural cross-links, and one canonical topic copy.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:403-405`.

- [A] 392. Child catalog metadata MUST include node identity, location, title, scope summary, applicability/status, and when to read it.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:407`.

- [A] 393. Tree validators MUST enforce initially at most eight direct children, depth difference at most one, target 1,500-word leaves with justified indivisible exceptions, and no cycles/missing targets/multiple parents/unreachable content/duplicate IDs, supporting configured limits and meaningful rebalance.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:409-420`.

- [A] 394. Rebalancing MUST use revision-checked recoverable multi-file transactions, preserve continuing-topic IDs and old-reference mappings, resolve IDs independently of paths, and validate committed invariants.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:418-420`.

- [A] 395. Supported documentation readers MUST use shared read locks, versioned snapshots, or revision-change detection/retry to avoid partially rewritten trees.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:420`.

- [A] 396. The ledger MUST use append-only structured change/decision events plus a generated readable index, stable event IDs, owner/submission/run/artifact/decision links, historical root mappings, and recoverable idempotent state updates.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:450-455`.

- [A] 397. Sensitive intake MUST use bounded admission before durable storage and unsafe spooling, retaining only non-sensitive rejection metadata and sanitizing execution output separately from exact accepted human originals.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:461-463`.

- [A] 398. Authorized historical redaction MUST reconcile all affected AIH-owned retained/recovery copies, derived hashes/indexes, and a non-sensitive authorization audit without secret-bearing backups or regeneration of removed values.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:465-467`.

- [A] 399. Per-run/segment `implementation_log.jsonl` and `implementation_summary.md` MUST be defined in conventions and initialized before changes; helpers MUST flush observable intent/result/evidence/checkpoint events incrementally.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:471-475`.

- [A] 400. The worker/recovery path MUST reconcile persisted events and observed effects into a labeled reconstructed summary when crashes prevent an authored final summary.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:477-479`.

- [A] 401. Each skill MUST follow the published Agent Skills format with `SKILL.md`, valid YAML metadata, behavioral guidance, and AIH-specific fields through the standard metadata extension mechanism.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:481-483`.

- [A] 402. Shared formats/templates MUST be authored under `.aih/conventions/` and bundled as generated versioned conventions/guidance/Python helpers during core build/release, with source hashes/versions, equivalence checks, and rejection of stale/conflicting bundles.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:489-495`.

- [A] 403. Installed integration MUST use canonical contracts, standalone packages matching bundled resources, and lifecycle state transitions MUST remain in the engine integration layer.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:493-497`.

- [A] 404. The compact standalone contract MUST persist explicit roots/access, input/output, scope/effects, initiating instruction, constraints, applicable plan/approval/direct authority, and result/evidence references beside output without depending on global AIH state.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:497-499`.

- [A] 405. Skill package directory IDs MUST be `clarify-requirements`, `analyze-and-plan`, `implement-plan`, `test-and-verify`, `reverse-engineer-product`, `maintain-documentation`, `answer-product-questions`, and `git-workflow`, with only the last disabled by default.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:503-517`.

- [A] 406. `clarify-requirements` MUST own iterative requirements, reviewed answers/amendments, explained questionnaires, source-linked interpretation/rounds/dispositions, and unresolved requirements, allowing read-only investigation/narrow factual bookkeeping without design.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:510`.

- [A] 407. `analyze-and-plan` MUST own feasibility/alternatives/dependencies/risks/unrelated issues and sequential implementation/test/documentation/evidence planning with required analysis records, affected paths, mappings, verification strategy, and planned increments.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:511`.

- [A] 408. `implement-plan` MUST own authorized sequential changes and repairs with prerequisite checks, task evidence, incremental logs/results, and recoverable incomplete state in both normal/direct modes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:512`.

- [A] 409. `test-and-verify` MUST own authorized test creation/update, complete-suite execution via helpers, failure investigation/scope reporting, acceptance/content evidence and unexecuted/stale checks; test-file changes/execution MUST respect current authorization.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:513`.

- [A] 410. `reverse-engineer-product` MUST own authorized baseline/refresh evidence discovery and interpretation, fingerprints/issues/gaps/limits, distinguishing observation/inference/unknowns without implementation changes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:514`.

- [A] 411. `maintain-documentation` MUST own authorized increments, current knowledge/defects/applicability/traceability, catalogs/links/balance, and applied/verified/structural-change evidence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:515`.

- [A] 412. `answer-product-questions` MUST own independent source-grounded read-only answers and question records under the global single-action rule without implementation, scope, instruction, or durable-documentation effects.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:516`.

- [A] 413. `git-workflow` MUST declare Git/repository and operation dependencies and produce evidence only for separately scoped authorized inspection/branch/diff/commit/push/PR work, with no authority from installation/enablement alone.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:517`.

- [A] 414. Standalone clarification MUST bundle rounds/forms/import/amendment guidance/helpers; standalone direct implementation MUST bundle necessary planning capability without requiring another installed skill.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:519-521`.

- [A] 415. Baseline discovery and documentation application MUST share contracts/helpers and reusable evidence under a common authorized operation instead of generating competing knowledge.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:525`.

- [A] 416. Initialization, approval/state changes, locks, snapshots, execution, catalogs, archival, and routine recovery MUST remain deterministic engine operations rather than additional skills; routing MUST remain shared in `run.md`.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:527`.

- [A] 417. `.aih/skills/catalog.yaml` and `.aih/skills/README.md` MUST derive from package metadata with convention-defined schema covering stable ID/name/version/purpose, selection/exclusions, I/O and standalone parameters, effects/scope/authority, dependencies/compatibility, location and resource hashes/versions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:531-540`.

- [A] 418. Catalog generation/validation MUST run in Python during build/install/upgrade/explicit core maintenance from the same metadata, including all eight packages; ordinary discovery/listing/execution MUST NOT regenerate or write core catalogs.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:542`.

- [A] 419. Read-only discovery MUST compare validated installed metadata with catalogs, permit an effective in-memory inventory of newly installed metadata, report identity/integrity/stale conflicts, and MUST NOT execute package code.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:544`.

- [A] 420. Dynamic skill enablement MUST be stored by stable ID in `.aih_product/config.yaml`; effective enabled/available/compatible state MUST derive from validated product configuration and diagnostics, not product-specific edits to core metadata.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:546`.

- [A] 421. Agent integration MUST use a shared Python adapter contract with a functional Codex CLI implementation and manual-handoff route.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:554`.

- [A] 422. Profile schemas MUST hold adapter/trusted executable/model/settings/timeout/permissions, credential environment-variable references only, and supported cache/session locations inside writable roots, recording effective precedence and registry revision per segment.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:556`.

- [A] 423. Adapter schemas MUST reject executable configuration, arbitrary command templates, and unrestricted argument strings, with privileged executable references resolved only through deliberate local administration.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:558`.

- [A] 424. Codex invocation MUST be verified against official documentation and installed help, use documented noninteractive/events/non-Git options where compatible, and verify resume syntax separately rather than reuse assumed start arguments.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:562`.

- [A] 425. Adapters MUST declare availability, start, streamable outputs/events, run/session IDs, exit, timeout, cancel, and supported native resume or clearly identified persisted-state restart behavior.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:564`.

- [A] 426. Process invocation MUST use argument arrays without shell interpolation, explicit root-qualified working directories, a minimal required operational/authentication environment, and the complete root/access registry revision.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:566`.

- [A] 427. Agent invocations MUST identify `.aih/run.md`, required helpers, action, request/question/system-operation ownership, submission where applicable, profile/segment, roots/access/revision, and use explicit parent/run checks to prevent recursive spawning of the same run.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:568`.

- [A] 428. Portal execution MUST use documented noninteractive modes and acknowledged task/segment ownership boundaries, without assuming conversational state transfers across CLIs.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:570`.

- [A] 429. Manual reservations MUST persist initiating instruction/scope, owner/submission where applicable, plan/approval/direct authority, profile, roots/access/revision, and handoff ID before exposing executable instructions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:572`.

- [A] 430. Resolved CLI versions and non-secret effective settings MUST be persisted, with events sanitized before storage/display and private reasoning excluded.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:574`.

- [A] 431. Core conventions MUST define versioned schemas for configuration/registry/revisions/state/skills/integrity, requests/catalogs/submissions/analysis/rounds/amendments/forms/receipts/reviews, plans/questions/approvals/defects/increments, system/bootstrap/inventory/extraction/reuse/usage/events/checkpoints/docs/evidence/logs/runs, owners/handoffs/baselines/readiness/notices/repair/test/standalone/redaction/temp contracts.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:578`.

- [A] 432. Global state MUST hold active request/phase/status/artifacts, submission/analysis/plan/workspace revisions, root availability/baselines/impacts, current round/draft references/task/blockers/next action/checkpoint/run/segment/profile/revision, verification hashes/documentation/notices, with Q&A/system and baseline/test statuses distinct.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:580`.

- [A] 433. A shared atomic operational reservation MUST precede submission/launch acceptance across every root; startup MUST count as busy, same-ID retries MUST reuse recorded ownership, and drafts MUST NOT become queued commands.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:582-584`.

- [A] 434. Persistence MUST use safe YAML parsing, validation, atomic file replacement, optimistic revisions, and locking; multi-file operations MUST use a journal or equivalent recoverable protocol rather than assume single-file atomicity covers them.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:586`.

- [A] 435. Cross-root transactions MUST journal root identities, source/destination versions, completed effects, and outstanding steps durably in central product state, without assuming cross-filesystem rename/whole-product atomicity.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:586`.

- [A] 436. Workspace administration MUST validate canonical disjoint roots, host permissions, mandatory writable home, stable identity, access and revisions before recoverable commit, retaining historical mappings and affected-evidence dispositions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:588`.

- [A] 437. Recovery MUST implement documented process-identity-aware stale-lock handling, interrupted-transaction reconciliation, and content/revision conflict detection for direct edits.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:592`.

- [A] 438. Checkpoints MUST precede consequential partial operations/interruption and retain completed/outstanding work, content versions, uncertain effects, and acknowledged boundaries; every recovery step MUST revalidate current roots/access/authority and inspect prior success before idempotent retry.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:594-596`.

- [A] 439. Verification MUST use defined root-qualified content manifests/dependency fingerprints and registry revisions, recording test selection/invocation/results/environment/checked versions under suite authorization and repair-budget contracts.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:598`.

- [A] 440. Product-content fingerprints MUST exclude volatile logs, answer timestamps, bookkeeping revisions, and operation-owned temporary data; documentation freshness and tests MUST track distinct dependencies where appropriate.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:600`.

- [A] 441. Supported-platform process control MUST terminate child processes safely and make Stop idempotent without releasing uncertain ownership or conflating it with request closure.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:602`.

- [A] 442. Confinement/core/instruction protection MUST combine resolved-target helper validation and supported host permissions, covering aliases/junctions/links/indirect effects; checksums MUST NOT be represented as enforcement against unrestricted actors.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:604`.

- [A] 443. Portal startup MUST use Python, bind loopback by default, support configured port/no-browser, and launch only browsers whose managed profile/cache writes are confined; unsupported browser launch MUST fall back to URL-only guidance.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:608`.

- [A] 444. First-run bootstrap MUST persist an exclusive recoverable operation before worker launch, perform Python initialization/registry validation/inventory, configured-agent synthesis, and documentation validation outside HTTP handlers, reusing operation identity on concurrent starts.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:612-614`.

- [A] 445. Portal and menu help MUST render maintained `.aih/USER_GUIDE.md` and shared command metadata with stable checked section anchors instead of independent conflicting help sources.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:629,678`.

- [A] 446. Workspace candidate validation MUST be a bounded administration operation rather than a generic filesystem browser and MUST revalidate revision/access/identity on Save without pre-registration mutation probes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:633`.

- [A] 447. Agent work MUST run in controlled workers/subprocesses outside HTTP handlers, with backend transactional idle/authorization checks and idempotent retries across refresh/click/retry behavior.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:652`.

- [A] 448. Sanitized portal execution-event delivery MUST use streaming or polling with readable progress summaries.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:650`.

- [A] 449. Product-file endpoints MUST accept root ID plus relative path through the current validated registry/access/scope contract rather than unrestricted absolute paths; administration MUST limit absolute candidate paths to explicit bounded validation/registration.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:656`.

- [A] 450. The portal MUST validate origins/hosts and protect state-changing requests, safely render Markdown, and serve untrusted outputs without executing supplied active content.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:656`.

- [A] 451. Privileged executable/permission configuration MUST be separate from ordinary content endpoints, and credential storage MUST contain permitted references only.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:658`.

- [A] 452. The shared terminal menu MUST be the Python CLI `menu` operation with rendering, input validation, root resolution, settings, dispatch, lifecycle, and workflow errors implemented in Python.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:664`.

- [A] 453. Direct menu invocation MUST support `py .aih/engine/cli.py menu` on Windows and `python3 .aih/engine/cli.py menu` on Linux, with documented supported Python selection and Linux executable/terminal behavior.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:666`.

- [A] 454. Startup MUST locate canonical home from the directory containing `.aih/`, validate that registry, and accept alternate explicit home only for a valid installation; root-selection arguments MUST NOT register new folders.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:670`.

- [A] 455. The discoverable CLI MUST support `python .aih/engine/cli.py <command>` at home and explicit valid-home operation from other directories, with consistent exact arguments and `--help` per command.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:682`.

- [A] 456. Installation MUST use a pinned core from an explicitly supplied local directory, validate destination home, and confine writes there without requiring a release URL or Git.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:684`.

- [A] 457. Host integration snippets MUST point to `.aih/run.md` and preserve existing instruction files.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:703`.

- [A] 458. Upgrade staging MUST keep inert data under home `.aih_product/tmp/` when state exists and executable incoming core/staging in authorized ordinary writable-root locations outside product state, with validated recoverable replacement/migrations/cleanup.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:705`.

- [A] 459. Optional Git helpers MUST confine worktree/config/cache/hook/credential/SSH side effects to current authorized writable roots even when remote operations are separately authorized.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:707`.

- [A] 460. Automated verification MUST exercise meaningful Python behavior/contracts in temporary plain non-Git and separate-root fixtures, keeping runnable fixtures outside core/product-state and all runtime/browser/cache effects in writable roots.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:711`.

- [A] 461. Live Codex verification MUST use an isolated confined compatible fixture when installed/authenticated/permitted, with a multi-root live case only where genuine adapter/host support exists and absent prerequisites reported explicitly.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:777`.

- [A] 462. Rendered portal walkthroughs MUST inspect primary screens including Workspace using browser profiles/caches inside authorized writable roots and report actual platform/storage coverage separately from automated checks.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:779`.

- [A] 463. The end-to-end synthetic fixture MUST exercise baseline, request creation, multiple clarification rounds, explained external forms, reviewed partial return, amendment supersession, iterative Analysis, plan approval, sequential tasks, full passing suite, applied documentation, Ready to close, and explicit human successful archival, waiting for each preceding action to finish/stop.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:781`.

- [A] 464. Additional fixtures MUST exercise direct-mode internal planning, idle blocked Q&A, unrelated-defect triage/deferred required failure, repair exhaustion/extension, interrupted incremental records, handoff reservation/release, history lookup, and cancelled closure with retained-state notice.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:781`.

- [A] 465. An existing-product fixture MUST exercise automatic first-portal initialization, baseline request gate, reverse engineering, profile-unavailable recovery, and incremental refresh.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:781`.

- [A] 466. A multi-root fixture MUST use writable frontend/backend, read-only reference, and unrelated unregistered sibling areas, exercise idle root addition during an open request, explicit baseline/reconciliation, cross-root implementation/tests, and denied outside/read-only writes; fixtures MUST be labeled examples rather than user-product requirements.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:781`.

- [A] 467. Verification MUST demonstrate that installation and repeated initialization preserve existing content.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:715`.

- [A] 468. Verification MUST demonstrate that core upgrades preserve product state and report required migrations or conflicts.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:715`.

- [A] 469. Acceptance verification of installation and core maintenance MUST cover this check: Core maintenance and upgrades are refused while any request is open or any setup, maintenance, or external execution owner remains active; an idle blocked request is still open.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:715`.

- [A] 470. Verification MUST demonstrate that a broken helper does not bypass the core-maintenance gate requiring no open request and no operational execution owner.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:715`.

- [A] 471. Acceptance verification of implementation languages and dependencies MUST cover this check: All framework behavior, helpers, adapters, workers, and backend code are Python.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:716`.

- [A] 472. Acceptance verification of implementation languages and dependencies MUST cover this check: The only non-Python harness scripts are the two optional menu launch wrappers with no framework business logic; direct Python operation remains complete.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:716`.

- [A] 473. Verification MUST demonstrate that AIH uses no database.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:716`.

- [A] 474. Verification MUST demonstrate that Git is not a default dependency.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:716`.

- [A] 475. Acceptance verification of directory organization and inert state MUST cover this check: Root organization is valid, immediate directory names do not overlap, and no product skills directory or executable product-state content is accepted. `.aih_product/tmp/` exists for operation-owned inert data; scripts, packages, virtual environments, bytecode, and runnable fixtures are excluded from it.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:717`.

- [A] 476. Acceptance verification of core and instruction immutability MUST cover this check: Ordinary runs leave the core and human-owned custom instructions unchanged.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:718`.

- [A] 477. Acceptance verification of draft submission and revision boundaries MUST cover this check: Draft edits never trigger work; explicit actions accepted only while idle snapshot revisions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:719`.

- [A] 478. Acceptance verification of draft submission and revision boundaries MUST cover this check: No new submission or replacement command is accepted or queued while an action is busy.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:719`.

- [A] 479. Acceptance verification of draft submission and revision boundaries MUST cover this check: At the next explicit idle action, submitted amendments invalidate affected approvals/evidence and are adopted through a recorded, acknowledged complete-task or complete-segment handoff, or reconciliation of the explicitly incomplete checkpoint after a safe Stop.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:719`.

- [A] 480. Acceptance verification of draft submission and revision boundaries MUST cover this check: An external edit during execution remains unsubmitted and cannot silently alter the executing instruction.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:719`.

- [A] 481. Verification MUST demonstrate that only one request can be open.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:720`.

- [A] 482. Verification MUST demonstrate that AIH creates no request backlog.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:720`.

- [A] 483. Verification MUST demonstrate that consequential blockers stop change work.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:720`.

- [A] 484. Verification MUST demonstrate that repeated commands do not launch duplicate processes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:720`.

- [A] 485. Acceptance verification of single request and operational ownership MUST cover this check: Starting, running, stopping, uncertain termination, and reserved external handoff all exclude a second operational action across change work, Q&A, setup, and maintenance.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:720`.

- [A] 486. Acceptance verification of single request and operational ownership MUST cover this check: Busy portal controls expose only Stop as an operational action; Save, import, submit, Ask, approval, closure, and configuration changes are disabled, and the backend enforces the same rule.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:720`.

- [A] 487. Acceptance verification of single request and operational ownership MUST cover this check: Passive navigation, help, status/log viewing, and existing-artifact viewing/download remain available.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:720`.

- [A] 488. Acceptance verification of single request and operational ownership MUST cover this check: Duplicate requests can return the existing action identity without starting another action.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:720`.

- [A] 489. Acceptance verification of approval and direct authorization MUST cover this check: Plan approval alone does not implement; ordinary implementation requires current approval.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:721`.

- [A] 490. Acceptance verification of approval and direct authorization MUST cover this check: Implement directly records its authorized exception to separate analysis invocation/approval while persisting the required plan before product changes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:721`.

- [A] 491. Acceptance verification of Stop and unsuccessful closure MUST cover this check: Stopping execution differs from closing a request.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:722`.

- [A] 492. Acceptance verification of Stop and unsuccessful closure MUST cover this check: Stop may safely terminate an incomplete task or segment after its indivisible operation is finished or controlled termination is confirmed; unfinished work remains unfinished, and no subsequent action starts automatically.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:722`.

- [A] 493. Acceptance verification of Stop and unsuccessful closure MUST cover this check: Cancelled/rejected closure preserves partial outcomes and creates a persistent current-state notice linking retained changes, affected documentation, unresolved defects, verification uncertainty, and archived evidence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:722`.

- [A] 494. Verification MUST demonstrate that cancelled/rejected closure permits a subsequent request without requiring passing tests or a complete documentation rewrite merely to cancel.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:722`.

- [A] 495. Verification MUST demonstrate that subsequent authorized work reconciles knowledge affected by unsuccessful closure before relying on it.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:722`.

- [A] 496. Acceptance verification of readiness and explicit successful closure MUST cover this check: Passing all required tests, valid verification, documentation, and evidence produces Ready to close while retaining the sole open-request slot.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:723`.

- [A] 497. Acceptance verification of readiness and explicit successful closure MUST cover this check: Only the explicit human Close successfully action revalidates the gates, archives the request, and releases that slot.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:723`.

- [A] 498. Acceptance verification of readiness and explicit successful closure MUST cover this check: Changed sources or invalidated evidence remove readiness.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:723`.

- [A] 499. Acceptance verification of readiness and explicit successful closure MUST cover this check: Neither zero exit status nor automatic completion of the last task closes a request.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:723`.

- [A] 500. Acceptance verification of current response history MUST cover this check: One current change response is maintained with history in request records.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:724`.

- [A] 501. Acceptance verification of independent Q&A MUST cover this check: Independent Q&A works with no request and while a request is open or blocked with its worker stopped, writes answer files, preserves request state, and makes no product changes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:725`.

- [A] 502. Acceptance verification of independent Q&A MUST cover this check: It is refused while any operational action or external reservation is busy.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:725`.

- [A] 503. Acceptance verification of independent Q&A MUST cover this check: External file changes affecting an answer's observed sources are detected and reported instead of presenting mixed observations as a verified snapshot.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:725`.

- [A] 504. Acceptance verification of questionnaire round trips MUST cover this check: Markdown questionnaires round-trip through file and portal editing, including free text, contradictory selections, partial submissions, respondent assignment, explanations, and revision conflicts.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:726`.

- [A] 505. Acceptance verification of questionnaire round trips MUST cover this check: The authoritative answer source remains the request Markdown; exported forms and raw returned files are linked exchange records.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:726`.

- [A] 506. Acceptance verification of documentation traversal MUST cover this check: Documentation traversal reaches relevant leaves without loading unrelated content; applicability and provenance remain visible.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:727`.

- [A] 507. Acceptance verification of tree growth and reorganization MUST cover this check: Grow and reorganize documentation across multiple capacity boundaries; validate eight-child limits, depth difference at most one, stable IDs, unique parents, reachability, cross-links, and preserved content.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:728`.

- [A] 508. Acceptance verification of documentation transaction recovery MUST cover this check: Interrupted documentation transactions recover safely; external edits conflict or serialize without data loss.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:729`.

- [A] 509. Acceptance verification of drift and verification freshness MUST cover this check: Documentation drift and verification invalidation detect relevant non-Git file changes without self-invalidating on bookkeeping.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:730`.

- [A] 510. Acceptance verification of skill discovery and catalogs MUST cover this check: Skill discovery exposes metadata without bodies and detects new, disabled, malformed, duplicate, and incompatible skills without changing `run.md`.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:731`.

- [A] 511. Acceptance verification of skill discovery and catalogs MUST cover this check: Validate all eight required initial packages, the seven enabled defaults, the disabled optional Git default, matching YAML/README catalogs, schema validity, resource/version fingerprints, and actionable stale-catalog diagnostics.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:731`.

- [A] 512. Acceptance verification of skill discovery and catalogs MUST cover this check: Ordinary discovery, portal listing, and enablement leave the core catalogs unchanged; explicit maintenance regenerates them deterministically.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:731`.

- [A] 513. Acceptance verification of skill discovery and catalogs MUST cover this check: CLI and portal show consistent installed/enabled/available states, and enablement alone cannot authorize work.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:731`.

- [A] 514. Acceptance verification of standalone skill portability MUST cover this check: Copy each of the eight delivered skill directories outside the installed AIH core, but still inside a registered writable workspace root, and validate its declared input/output contract, usage example, resources, and helpers in clean fixtures without an installed AIH engine or fixed product-state path, supplying only declared dependencies.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:732`.

- [A] 515. Acceptance verification of standalone skill portability MUST cover this check: Validate the compact standalone invocation contract: explicit workspace roots and their access modes, root-qualified input/output locations, permitted scope/effects, relevant plan and current approval or direct-mode authorization where applicable, initiating instruction, and effective host permission boundaries recorded with results.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:732`.

- [A] 516. Acceptance verification of standalone skill portability MUST cover this check: No full AIH lifecycle or stronger identity assurance is implied.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:732`.

- [A] 517. Acceptance verification of standalone skill portability MUST cover this check: Use a separate workspace-contained repository fixture for `git-workflow`, including its declared operation-tool dependencies where needed.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:732`.

- [A] 518. Acceptance verification of standalone skill portability MUST cover this check: Detect altered bundled conventions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:732`.

- [A] 519. Acceptance verification of standalone skill portability MUST cover this check: Claim behavioral portability only if an agent actually exercises the skill; distinguish package/helper checks from observed agent behavior.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:732`.

- [A] 520. Acceptance verification of profile precedence MUST cover this check: Multiple profiles coexist; default, per-run, and capability assignments follow documented precedence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:733`.

- [A] 521. Acceptance verification of profile precedence MUST cover this check: Changes are accepted only while idle and take effect for the applicable next segment at a recorded boundary, without altering a running segment.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:733`.

- [A] 522. Acceptance verification of controlled CLI fault handling MUST cover this check: A controlled fake CLI tests streaming, Unicode and special-character arguments, spaces in paths, authentication/version errors, malformed events, nonzero exits, timeouts, cancellation, child processes, and resumption limitations.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:734`.

- [A] 523. Acceptance verification of adapter prerequisites MUST cover this check: Adapter selection supports a product directory without Git.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:735`.

- [A] 524. Acceptance verification of adapter prerequisites MUST cover this check: Missing CLIs, invalid settings, unsupported versions, and unavailable authentication produce actionable errors without silent fallback.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:735`.

- [A] 525. Acceptance verification of manual-handoff ownership MUST cover this check: Manual handoff is functional, accurately labeled, and cannot falsely mark work as executed or verified.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:736`.

- [A] 526. Acceptance verification of manual-handoff ownership MUST cover this check: Its durable reservation binds the request/scope, submission, applicable plan, and handoff ID, survives portal restart, and excludes every other operational action until the Stop/release flow confirms the external worker has stopped and reconciles returned files/evidence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:736`.

- [A] 527. Acceptance verification of manual-handoff ownership MUST cover this check: Uncertain ownership or attribution remains explicit.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:736`.

- [A] 528. Verification MUST demonstrate that required handoff evidence intake and external-stop confirmation occur within the reserved Stop/release flow and do not enable unrelated actions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:736`.

- [A] 529. Acceptance verification of manual-handoff ownership MUST cover this check: Cancelling a prepared but unstarted handoff releases its reservation safely.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:736`.

- [A] 530. Acceptance verification of state transaction recovery MUST cover this check: Atomic writes, revision conflicts, transaction recovery, stale-lock handling, and duplicate-action reconciliation work under simulated interruptions/concurrency.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:737`.

- [A] 531. Acceptance verification of portal startup and confinement MUST cover this check: Portal browser/no-browser startup, port conflicts, shutdown, primary workflow, separate Q&A, safe Markdown, origin protections, and file-boundary checks are exercised.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:738`.

- [A] 532. Acceptance verification of portal startup and confinement MUST cover this check: Framework-launched browsers use registered writable-root profiles/cache; an uncontrolled browser launch that would write outside the workspace is replaced with the documented URL-only path.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:738`.

- [A] 533. Acceptance verification of unsafe content and sensitive-input handling MUST cover this check: Product content cannot become arbitrary commands, dynamic imports, privileged configuration, or executable portal content.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:739`.

- [A] 534. Acceptance verification of unsafe content and sensitive-input handling MUST cover this check: Seeded sensitive input detected before acceptance is rejected without persisting its content in normal AIH records or echoing it in displayed diagnostics; only non-sensitive rejection metadata is kept, and corrected resubmission is required.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:739`.

- [A] 535. Acceptance verification of unsafe content and sensitive-input handling MUST cover this check: Test best-effort detection limitations explicitly.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:739`.

- [A] 536. Acceptance verification of unsafe content and sensitive-input handling MUST cover this check: For secrets discovered in stored records, test the explicit human-authorized historical-redaction exception: remove the secret from affected AIH-owned copies and append a non-sensitive audit event without general rewriting of history or claiming erasure of external copies.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:739`.

- [A] 537. Acceptance verification of Clarify semantic boundaries MUST cover this check: Clarification artifacts and questionnaires capture what and why, scope, constraints, and observable acceptance criteria without selecting an implementation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:740`.

- [A] 538. Acceptance verification of Clarify semantic boundaries MUST cover this check: Preserve explicit user technical constraints and distinguish them from observed existing technology.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:740`.

- [A] 539. Acceptance verification of Clarify semantic boundaries MUST cover this check: Exercise read-only investigation, Analysis-owned design choices, and a requirement gap discovered during Analysis that returns to clarification.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:740`.

- [A] 540. Acceptance verification of Clarify semantic boundaries MUST cover this check: Clarify may add evidence-backed known-defect entries or stale-topic markers with source/request references, but may not repair the product, redesign it, rewrite substantive business documentation, or treat an inference as approved intent.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:740`.

- [A] 541. Acceptance verification of Clarify semantic boundaries MUST cover this check: Test structural/state contracts automatically; claim the semantic phase boundary was followed only when an actual agent exercised it.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:740`.

- [A] 542. Acceptance verification of iterative Analysis MUST cover this check: Repeated Analyze invocations handle initial analysis, submitted answers, additional directions, unchanged inputs, and plan generation/regeneration without a separate Plan command or automatic implementation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:741`.

- [A] 543. Acceptance verification of iterative Analysis MUST cover this check: Preserve valid completed-task history and invalidate affected approvals/evidence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:741`.

- [A] 544. Acceptance verification of analysis records and plan traceability MUST cover this check: The interpretation remains the single current request definition, and the questions catalog points to authoritative submitted answers without creating another editable answer store.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:742`.

- [A] 545. Acceptance verification of analysis records and plan traceability MUST cover this check: Validate required analysis records, optional supporting files, sequential task order, affected paths identified by stable root ID and relative path, workspace configuration revisions, and requirements-to-task/test traceability.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:742`.

- [A] 546. Acceptance verification of sequential implementation evidence MUST cover this check: Normal and direct implementation both persist plans with mandatory test and documentation tasks and execute tasks sequentially.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:743`.

- [A] 547. Acceptance verification of sequential implementation evidence MUST cover this check: No shortcut omits logs, results, tests, documentation, or user selection of unrelated defects.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:743`.

- [A] 548. Acceptance verification of regression repairs and budgets MUST cover this check: Run retained regression tests from earlier requests as part of the complete maintained suite.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:744`.

- [A] 549. Acceptance verification of regression repairs and budgets MUST cover this check: Repair authorized failures and rerun the suite; test suppression or unexecuted required tests cannot produce successful completion.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:744`.

- [A] 550. Acceptance verification of regression repairs and budgets MUST cover this check: Exercise the configurable repair budget, defaulting to three unsuccessful repair cycles for the same unresolved failure, and no-progress detection.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:744`.

- [A] 551. Acceptance verification of regression repairs and budgets MUST cover this check: Reaching the applicable cycle, time, or available measured-token limit stops the worker as blocked with attempt history and evidence preserved.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:744`.

- [A] 552. Acceptance verification of regression repairs and budgets MUST cover this check: Only explicit authorized continuation extends a budget; it never silently resets the history or relaxes completion gates.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:744`.

- [A] 553. Acceptance verification of unrelated-defect disposition MUST cover this check: Unrelated defects require user scope disposition, unfixed established defects appear in current known-defect documentation, and a deferred defect failing a required test blocks completion without exception.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:745`.

- [A] 554. Acceptance verification of unrelated-defect disposition MUST cover this check: Recording the blocker must not launch unauthorized repairs or another request.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:745`.

- [A] 555. Acceptance verification of documentation increments MUST cover this check: Every request has a documentation increment with planned/applied/verified distinctions or a justified no-impact result.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:746`.

- [A] 556. Verification MUST demonstrate that a request documentation increment is reconciled against actual changes, evidence, and current documentation before successful closure.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:746`.

- [A] 557. Verification MUST demonstrate that cancelled/rejected closure preserves a current-state notice for unfinished documentation reconciliation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:746`.

- [A] 558. Acceptance verification of incremental implementation records MUST cover this check: Every implementation attempt has durable incremental logs and a readable results summary.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:747`.

- [A] 559. Acceptance verification of incremental implementation records MUST cover this check: Simulate crashes between action intent and result, recover an explicitly reconstructed summary, retain uncertain outcomes, and prevent blind duplicate execution.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:747`.

- [A] 560. Acceptance verification of archival and historical access MUST cover this check: Explicit successful or cancelled/rejected closure moves records to separate historical folders, preserving IDs, links, outcomes, and summaries, subject only to the documented human-authorized sensitive-data correction exception.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:748`.

- [A] 561. Acceptance verification of archival and historical access MUST cover this check: Normal execution reads current documentation and the active request, including unresolved current-state notices; historical evidence is fetched on demand through its catalog.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:748`.

- [A] 562. Acceptance verification of first-start baseline generation MUST cover this check: First portal startup without product state initializes the single framework-home state, inventories configured product roots, and starts configured-agent documentation generation once.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:749`.

- [A] 563. Acceptance verification of first-start baseline generation MUST cover this check: Refresh/restart/concurrent-start scenarios do not duplicate workers, operation IDs, or writes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:749`.

- [A] 564. Acceptance verification of first-start baseline generation MUST cover this check: A request cannot be opened until the complete initial documentation baseline for the configured product roots passes its coverage/completeness gate; adding a root makes its required local coverage part of that gate.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:749`.

- [A] 565. Acceptance verification of first-start baseline generation MUST cover this check: Explicitly recorded unknown external facts do not alone prevent baseline completion; missing required local coverage does.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:749`.

- [A] 566. Acceptance verification of first-start baseline generation MUST cover this check: Setup, Q&A, and local drafting remain available when setup is pending and no action is busy, while active bootstrap obeys Stop-only operational controls.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:749`.

- [A] 567. Acceptance verification of bootstrap recovery MUST cover this check: Interrupted bootstrap resumes without overwriting human content.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:750`.

- [A] 568. Acceptance verification of bootstrap recovery MUST cover this check: Invalid existing state is reported rather than reset.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:750`.

- [A] 569. Acceptance verification of bootstrap recovery MUST cover this check: Missing profile, incompatible CLI, unavailable authentication, or permission limitations leave semantic work visibly pending with actionable guidance and no silent fallback.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:750`.

- [A] 570. Acceptance verification of reverse-engineering provenance MUST cover this check: Initial and incremental reverse engineering preserve implementation/source/test/instruction fingerprints across configured roots while writing evidence-based documentation, recording stable root IDs, relative paths, and the observed workspace configuration revision.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:751`.

- [A] 571. Acceptance verification of reverse-engineering provenance MUST cover this check: Extracted facts, inferred requirements, unknowns, generated content, and actually verified behavior remain distinguishable.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:751`.

- [A] 572. Acceptance verification of system-operation ownership MUST cover this check: Bootstrap and standalone documentation maintenance keep audit/checkpoint records in the single framework-home product state without a synthetic request, duplicate framework/product-state home, database, or Git.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:752`.

- [A] 573. Acceptance verification of system-operation ownership MUST cover this check: Every operation obeys global single-action ownership.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:752`.

- [A] 574. Acceptance verification of system-operation ownership MUST cover this check: Documentation work within an open request uses that request's authorization and documentation increment; core maintenance/upgrades remain prohibited until there is no open request and all other execution ownership has been released.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:752`.

- [A] 575. Acceptance verification of deterministic helper use MUST cover this check: Inventory, parsing, validation, state updates, test execution/result capture, catalog maintenance, and archival route through tested deterministic helpers.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:753`.

- [A] 576. Acceptance verification of deterministic helper use MUST cover this check: Check equivalent bundled helpers for standalone skills.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:753`.

- [A] 577. Acceptance verification of deterministic helper use MUST cover this check: Test structural/helper behavior separately from actual agent compliance with the mandatory-use rule.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:753`.

- [A] 578. Acceptance verification of incremental context reuse MUST cover this check: Unchanged input sets reuse valid extraction/summaries and avoid unnecessary semantic generation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:754`.

- [A] 579. Acceptance verification of incremental context reuse MUST cover this check: Source, instruction, extractor, or schema/core changes invalidate affected reuse.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:754`.

- [A] 580. Acceptance verification of incremental context reuse MUST cover this check: Incremental runs select relevant documents without dropping required coverage or full regression tests.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:754`.

- [A] 581. Acceptance verification of compact evidence and token telemetry MUST cover this check: Compact outputs retain evidence references and label omitted detail; full available sanitized evidence remains inspectable.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:755`.

- [A] 582. Acceptance verification of compact evidence and token telemetry MUST cover this check: Adapter-reported token usage is recorded accurately, and missing usage remains unavailable rather than fabricated as zero.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:755`.

- [A] 583. Acceptance verification of compact evidence and token telemetry MUST cover this check: Distinguish actual token measurements from proxy evidence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:755`.

- [A] 584. Acceptance verification of menu launch wrappers MUST cover this check: Windows/Linux launch wrappers invoke the shared Python menu without duplicating logic; direct Python invocation also works.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:756`.

- [A] 585. Acceptance verification of menu launch wrappers MUST cover this check: Exercise root resolution from another working directory, paths with spaces/special characters, missing runtime diagnostics, repeated launch deduplication, and menu exit/shutdown behavior.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:756`.

- [A] 586. Acceptance verification of menu launch wrappers MUST cover this check: Report which OS launcher paths were actually exercised rather than inferring cross-platform success.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:756`.

- [A] 587. Acceptance verification of shared help consistency MUST cover this check: README quick-start commands, USER_GUIDE command references, menu help, portal help, and contextual section links match the implemented catalog and installed version.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:757`.

- [A] 588. Acceptance verification of shared help consistency MUST cover this check: Help is accessible before initialization/authentication and does not invoke an agent or modify the core.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:757`.

- [A] 589. Acceptance verification of portal pages and tabs MUST cover this check: Exercise all eight portal pages and six Current request tabs with meaningful workflow states, inspecting the rendered interface.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:758`.

- [A] 590. Acceptance verification of portal pages and tabs MUST cover this check: Verify explicit draft/submission differences, repeated Analyze and generated plan approval, direct-implementation explanation, defect scope selection, revision conflicts, profile effective boundaries, and distinct stop/closure actions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:758`.

- [A] 591. Acceptance verification of portal state explanations MUST cover this check: Portal next-action/disabled-action explanations match validated state.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:759`.

- [A] 592. Verification MUST demonstrate that a failed required test cannot be accepted as an exception allowing successful completion.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:759`.

- [A] 593. Verification MUST demonstrate that historical browsing does not reopen requests or queue work.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:759`.

- [A] 594. Verification MUST demonstrate that independent Q&A remains available when blocked change work has safely stopped and no other action or external reservation is busy.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:759`.

- [A] 595. Acceptance verification of portal state explanations MUST cover this check: Confirm log/result views distinguish process status from task outcomes, Ready to close from closed, and bootstrap documentation from product verification.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:759`.

- [A] 596. Acceptance verification of iterative clarification MUST cover this check: Repeat Clarify through initial questions, framework-user answers, imported requestor answers, changed wishes/additional information, partial responses, and an unchanged invocation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:760`.

- [A] 597. Acceptance verification of iterative clarification MUST cover this check: Preserve the single interpretation and prior revisions, reassess stale answers and affected downstream approval/evidence, and finish ready for Analysis without invoking Analyze or implementation automatically.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:760`.

- [A] 598. Acceptance verification of requestor form export MUST cover this check: Generate a versioned plain-text requestor form at the end of a waiting clarification round with only the applicable marked questions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:761`.

- [A] 599. Acceptance verification of requestor form export MUST cover this check: Check each question has an explanation, why it matters, answer instructions, and a neutral example where useful.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:761`.

- [A] 600. Acceptance verification of requestor form export MUST cover this check: Verify the file can be completed in an ordinary text editor, contains stable form/question references, keeps earlier exports, and does not require portal access.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:761`.

- [A] 601. Acceptance verification of requestor form export MUST cover this check: Review explanation usefulness with meaningful examples; structural checks alone cannot prove clarity for a non-technical reader.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:761`.

- [A] 602. Acceptance verification of answer-import review MUST cover this check: Exercise upload/drop and paste, review of matched answers, partial and unknown answers, duplicate IDs/receipts, missing references with manual matching, altered question text, stale forms, newer local answers, answers for withdrawn questions, wrong/closed-request forms, and free-text proposed amendments.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:762`.

- [A] 603. Acceptance verification of answer-import review MUST cover this check: Apply sensitive-input rejection before persistence; preserve accepted originals, distinguish attributed requestor from actual submitter, prevent unreviewed answer adoption, and verify these inputs cannot grant plan approval or implementation authority.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:762`.

- [A] 604. Acceptance verification of answer-import review MUST cover this check: Busy-state refusal must not retain the attempted import as a queued submission.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:762`.

- [A] 605. Acceptance verification of combined import-and-Clarify recovery MUST cover this check: Verify Save reviewed answers only saves drafts, while Import answers and clarify commits the reviewed merge and explicit submission when idle.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:763`.

- [A] 606. Acceptance verification of combined import-and-Clarify recovery MUST cover this check: Atomically reserve the single accepted action across merge, submission, and worker launch.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:763`.

- [A] 607. Acceptance verification of combined import-and-Clarify recovery MUST cover this check: Simulate revision changes during review, repeated clicks, interruption between merge/submission/worker launch, and a launch failure.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:763`.

- [A] 608. Acceptance verification of combined import-and-Clarify recovery MUST cover this check: Recover without lost newer edits, duplicate effects, a second writer, or a pending replacement command; report draft, submitted, starting, running, and failed states accurately.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:763`.

- [A] 609. Acceptance verification of combined import-and-Clarify recovery MUST cover this check: Recovery of the accepted action is not a queue of later actions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:763`.

- [A] 610. Acceptance verification of amendment history MUST cover this check: Preserve amendment IDs, every accepted framework-saved/submitted revision and observed external edit, original wording, source, sequence, supersession/withdrawal, and interpretation effects, subject to sensitive-input rejection and explicitly authorized historical redaction.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:764`.

- [A] 611. Acceptance verification of amendment history MUST cover this check: Exercise an amendment contradicting an imported answer, direct edits of current input, repeated submission of the same amendment, and explicit correction of earlier wishes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:764`.

- [A] 612. Acceptance verification of amendment history MUST cover this check: Verify traceability survives completed/cancelled/rejected archival and ordinary later runs use current interpretation rather than reapplying historical amendments.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:764`.

- [A] 613. Acceptance verification of suite environment contracts MUST cover this check: Every registered test suite has a validated test-run contract naming its environment, prerequisites, expected effects, isolation/cleanup, and required authorization, including root-qualified filesystem/cache effects, required access modes, and the applicable workspace configuration revision.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:765`.

- [A] 614. Acceptance verification of suite environment contracts MUST cover this check: Missing permissions or infrastructure block required execution and closure.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:765`.

- [A] 615. Acceptance verification of suite environment contracts MUST cover this check: Tests run only in configured environments with authorized effects; independently authorized external-service effects do not permit filesystem writes outside registered writable roots or into read-only roots.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:765`.

- [A] 616. Acceptance verification of reconstruction status MUST cover this check: The reconstruction documentation gate reviews completeness and traceability of business rules, interfaces, expected results, dependencies, and recovery prerequisites.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:766`.

- [A] 617. Verification MUST demonstrate that passing the reconstruction completeness/traceability review is reported as specified but not demonstrated until an independent reconstruction exercise supplies evidence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:766`.

- [A] 618. Verification MUST demonstrate that an independent reconstruction exercise is not silently added as a mandatory initial completion gate.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:766`.

- [A] 619. Verification MUST demonstrate that ordinary implementation tests do not establish reconstructed equivalence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:766`.

- [A] 620. Acceptance verification of multi-root confinement MUST cover this check: The workspace is the union of explicitly registered canonical roots, with managed creates, writes, renames, deletions, and cleanup confined to its writable subset, including subprocesses and indirect runtime effects.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:767`.

- [A] 621. Acceptance verification of multi-root confinement MUST cover this check: The parent containing `.aih/` remains the mandatory writable framework home, not an authorization for other unregistered locations.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:767`.

- [A] 622. Acceptance verification of multi-root confinement MUST cover this check: Exercise noncontiguous roots, path traversal, prefix lookalikes, symlink/junction/reparse escapes, alternate aliases and hard links where supported, and changed targets between validation and use.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:767`.

- [A] 623. Acceptance verification of multi-root confinement MUST cover this check: Validate disjoint root registration and reject duplicate, nested, or aliasing roots that make membership/access ambiguous; resolving a path never grants access to an unregistered common ancestor.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:767`.

- [A] 624. Acceptance verification of multi-root confinement MUST cover this check: Check final targets and parent paths for create/rename/delete operations, including both roots involved in a move.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:767`.

- [A] 625. Acceptance verification of multi-root confinement MUST cover this check: Report platform-specific checks actually run; a lexical prefix check alone cannot establish confinement.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:767`.

- [A] 626. Acceptance verification of external-runtime side effects MUST cover this check: Installed outside-workspace runtimes and host-permitted prerequisites may be read/invoked without granting outside-workspace mutation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:768`.

- [A] 627. Acceptance verification of external-runtime side effects MUST cover this check: Exercise redirected or disabled temporary files, caches, session records, bytecode, global configuration, credential refresh, and optional Git/tool side effects.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:768`.

- [A] 628. Acceptance verification of external-runtime side effects MUST cover this check: A tool or adapter that cannot honor the registered roots, read-only modes, or host permissions is visibly blocked; a single-directory sandbox is never widened to a common ancestor to imitate multi-root support.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:768`.

- [A] 629. Acceptance verification of external-runtime side effects MUST cover this check: Credentials are not copied into tracked product files to work around confinement; direct external user application behavior is not falsely claimed to be controlled by AIH.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:768`.

- [A] 630. Acceptance verification of temporary-data cleanup MUST cover this check: Temporary directories are uniquely owned by operations, excluded from semantic/source fingerprints and documentation inventories, and cleaned through confined deterministic helpers.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:769`.

- [A] 631. Acceptance verification of temporary-data cleanup MUST cover this check: Active operation data is protected, interrupted cleanup is recoverable, and temporary data never holds the only copy of durable evidence, checkpoints, or authorization.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:769`.

- [A] 632. Acceptance verification of temporary-data cleanup MUST cover this check: Executable temporary artifacts remain in authorized ordinary writable-root paths outside `.aih_product/`; Python bytecode writing into product state or the immutable core is disabled.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:769`.

- [A] 633. Acceptance verification of Workspace administration MUST cover this check: Settings → Workspace lists stable root IDs, names, paths, purposes, and access modes, and supports explicit human Add folder, Edit, Validate access, and Remove from workspace operations.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:771`.

- [A] 634. Acceptance verification of Workspace administration MUST cover this check: Configuration changes are accepted only when global execution ownership is idle, including while a request is open or blocked with its worker stopped.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:771`.

- [A] 635. Acceptance verification of Workspace administration MUST cover this check: A busy worker, uncertain termination, reserved external handoff, or another operational action prevents both UI and backend changes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:771`.

- [A] 636. Acceptance verification of Workspace administration MUST cover this check: Validate and Save cannot overlap execution through a race; the agent cannot expand its own workspace, and saving configuration never starts an agent or grants implementation scope.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:771`.

- [A] 637. Acceptance verification of workspace evidence invalidation MUST cover this check: Workspace configuration revisions and audit history preserve root identity and prior mappings.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:772`.

- [A] 638. Acceptance verification of workspace evidence invalidation MUST cover this check: Test add, removal, relocation, and writable/read-only changes with an open request: affected analysis, plan approval, documentation, verification, and reusable extraction are marked stale and require explicit reconciliation before reliance.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:772`.

- [A] 639. Acceptance verification of workspace evidence invalidation MUST cover this check: Relocation revalidates actual content and access rather than treating an old relative path as proof of unchanged identity.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:772`.

- [A] 640. Acceptance verification of workspace evidence invalidation MUST cover this check: Unaffected evidence may remain valid with recorded justification.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:772`.

- [A] 641. Verification MUST demonstrate that missing or inaccessible roots produce actionable blocked states.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:772`.

- [A] 642. Verification MUST demonstrate that the mandatory framework-home root cannot be removed or made read-only.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:772`.

- [A] 643. Acceptance verification of new-root documentation baselines MUST cover this check: A newly added product root receives its required documentation baseline through an explicitly authorized reverse-engineering action; when a request is open, the work belongs to that request and its documentation increment.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:773`.

- [A] 644. Verification MUST demonstrate that implementation cannot rely on a newly added product area until its required documentation baseline coverage is reconciled.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:773`.

- [A] 645. Acceptance verification of new-root documentation baselines MUST cover this check: Read-only source roots support evidence-based documentation written to the central product state, while test collection, build tools, cache generation, and attempted repairs cannot write back into them.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:773`.

- [A] 646. Acceptance verification of new-root documentation baselines MUST cover this check: Test host adapters with genuine multi-root access support and reject incompatible configurations without silently relocating content, broadening permissions, or reducing required tests.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:773`.

- [A] 647. Acceptance verification of root removal and retained obligations MUST cover this check: Removing workspace membership never deletes source files, historical root mappings, documentation-increment evidence, required failing-test obligations, or unresolved defects.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:774`.

- [A] 648. Acceptance verification of root removal and retained obligations MUST cover this check: Show affected dependencies and preserve their disposition for explicit review; removing a root cannot manufacture successful verification or closure.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:774`.

- [A] 649. Acceptance verification of root removal and retained obligations MUST cover this check: Archived requests remain intelligible through stable root-qualified references without granting access to removed locations.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:774`.

- [A] 650. Acceptance verification of cross-filesystem recovery MUST cover this check: Interrupt a task or transaction spanning roots on different filesystems.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:775`.

- [A] 651. Acceptance verification of cross-filesystem recovery MUST cover this check: Preserve per-root progress and reconcile partial outcomes without claiming an atomic cross-filesystem commit, silently rolling back, or executing duplicate changes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:775`.

- [A] 652. Acceptance verification of cross-filesystem recovery MUST cover this check: If an idle workspace revision removes or restricts a path needed for recovery, recovery blocks the prohibited write and asks for an explicit authorized resolution; it never resurrects old permissions from a journal.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:775`.

- [A] 653. Acceptance verification of cross-filesystem recovery MUST cover this check: Scope, pending recovery, test obligations, and the single action/request rules remain enforced across every root.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:775`.

- [A] 654. User help MUST NOT be duplicated into behavioral prompts or loaded in full into every agent run.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:678`.
