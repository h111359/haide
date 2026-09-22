# Build AIH: a portable, file-based AI product-development harness

Prompt version: 20260922_090259Z
Generated (UTC): 2026-09-22 09:02:59Z

Act as a senior software architect and implementation engineer. Build the complete framework described below, including working Python infrastructure, agent instructions, conventions, portable skills, a local web portal, tests, and operating documentation.

Implement and verify the solution; do not deliver only a proposal, scaffolding, or a reduced first version. All requirements are in scope. Work in a sensible implementation sequence without asking me to prioritize features. Resolve routine engineering details yourself. Ask only about consequential ambiguities that cannot be resolved through inspection or this specification.

First inspect the available workspace and applicable host instructions. Preserve existing product content. Do not assume Git, a database, an installed agent CLI, or a published release exists. This prompt authorizes building AIH; the approval workflow below governs subsequent product change requests handled by AIH.

## 1. Purpose and non-negotiable boundaries

AIH helps an agent understand a product, clarify what needs to change and why, plan how to satisfy those requirements, implement authorized work, verify results, maintain product documentation, and resume interrupted work from files.

Support one product root per installation, with multiple components inside it. A product root may be a plain directory or a repository. Support Windows and Linux; distinguish intended support from platforms actually tested.

Use two roots:

- `.aih/`: versioned framework core, unchanged by ordinary product operations.
- `.aih_product/`: product-specific information, communication, history, documentation, and state.

Use `.aih_product/` consistently in generated files, commands, instructions, schemas, and documentation. Do not create alternative product-state roots.

All framework behavior, deterministic helpers, adapters, workers, and backend components must be Python. The only non-Python harness-script exception is the pair of optional `.aih/menu.cmd` and `.aih/menu.sh` launchers, limited to locating/invoking the shared Python menu and reporting minimal runtime/startup errors. They must contain no workflow, state, agent-execution, or other framework business logic. Browser HTML, CSS, and JavaScript are permitted for the portal interface. Product implementation languages are unrestricted. Direct Python operation must remain fully supported without the launch wrappers; do not require Node or PowerShell to operate the harness.

Markdown and validated YAML/JSON files are authoritative. Do not use a database, including SQLite, an embedded database, or a database cache. Optional search indexes must be disposable files or in-memory structures.

Do not require or initialize Git by default. Installation, history, diffs, revision checks, verification, and recovery must work without Git. Provide Git integration as an optional, configurable skill extension.

Only one change request may be open at a time. There is no backlog, queued future request, or concurrent change-request execution. Closed requests remain in separate historical folders with a metadata catalog and short summaries, loaded only when relevant. A separate read-only question channel is allowed. Initial bootstrap and explicitly invoked documentation-only maintenance are scoped system operations as specified below; they do not authorize product implementation changes.

## 2. Core organization

Organize `.aih/` around these immediate directories:

- `prompts/`: shared behavioral instructions, loaded when needed.
- `conventions/`: authoritative formats, schemas, structures, naming rules, templates, and validation contracts.
- `skills/`: one directory per portable skill, the generated metadata-only `catalog.yaml`, and the human-readable `README.md` catalog. Deliver the eight initial skills specified in section 13.
- `engine/`: all shared Python infrastructure, including the CLI, state helpers, adapters, workers, portal, tests, and supporting interface assets.

Place the single agent entry point at `.aih/run.md`. Include `.aih/README.md` for quick-start knowledge, `.aih/USER_GUIDE.md` as the maintained detailed user guide, and the optional `.aih/menu.cmd` and `.aih/menu.sh` launchers as core root files. Core version and integrity manifests may also be root files. Keep menu functionality and shared Python infrastructure under `engine/`; do not introduce additional immediate core directories for these features.

Prompts specify behavior. They reference conventions instead of redefining formats, schemas, directory structures, or templates. Conventions must not reference prompts or depend on which prompt consumes them. Engine validators implement the authoritative contracts without independently maintained conflicting schema definitions.

Keep `run.md` concise and stable. Do not hard-code a skill roster or profile names into it. It must route execution using submitted actions, validated product state, applicable instructions, discovered skill metadata, and the active request or identified system operation.

Ordinary runs must not modify `.aih/`, including generated catalogs, bytecode caches, logs, temporary files, or bundled skill resources. Route runtime material into its owning product communication/request/system-operation record or an appropriate OS temporary location. Core installation, explicit maintenance, and upgrades are separate operations.

### Deterministic operations belong to Python scripts

Provide named Python entry points and shared helper APIs for every deterministic framework operation. Agents must invoke these implementations instead of reimplementing their functionality through ad hoc commands, generated scripts, manual state edits, or repeated model reasoning. The portal and agent routes must use the same implementations and validation contracts.

Cover initialization, safe file inventories and supported fact extraction, content hashing/diffs, schema validation, submission snapshots, questionnaire parsing, revision checks, state transitions, locking and transactions, validated edit application, catalog/index/link maintenance, task status updates, registered test execution and result capture, logs/checkpoints, request archival, diagnostics, and upgrade mechanics. Product tools and test runtimes may retain their own languages; harness orchestration and bookkeeping remain Python. The optional OS menu launchers are limited to the bootstrap exception specified above.

Scripts collect and validate facts and apply specified operations. Agents interpret evidence, resolve ambiguity, choose authorized solutions, produce semantic content/patches, and diagnose failures. Do not turn extraction heuristics into asserted business requirements or expect a deterministic validator to prove semantic correctness.

Expose a compact metadata/help catalog with supported operation IDs, inputs, effects, required permissions, and structured result contracts. Return concise status, changed artifact references, actionable errors, and conflict details; keep verbose evidence available by reference. Use typed, validated operations rather than generic command templates or arbitrary-command endpoints. Agents should not need to read implementation source to invoke routine operations.

Missing or broken helper functionality must produce an explicit framework-gap diagnosis. Do not silently bypass its validation/transaction behavior or modify the immutable core during ordinary product work. Changes to helpers use the explicit core-maintenance workflow. Preserve direct human editing of permitted product files and detect/validate such edits; do not claim scripts enforce restrictions against external actors with filesystem access.

### Runtime token efficiency

Minimize avoidable model token consumption while preserving the full required analysis, documentation, tests, evidence, and instruction compliance. Keep orchestration instructions compact; delegate repeatable extraction, comparison, validation, and bookkeeping to Python.

Read metadata and relevant documentation branches before content leaves, load skill bodies/resources only on demand, and use source fingerprints and dependency maps to select affected material. Reuse still-valid analysis, compact checkpoints, and source-grounded summaries instead of repeatedly regenerating them. Summaries must retain source/version references, consequential decisions, unresolved issues, and recovery context. Invalidate affected reuse when source content, applicable instructions, extraction logic, or schema/core versions change.

Send compact operation and test summaries plus relevant failure details to the agent; retain complete available sanitized evidence in files for targeted inspection. Paginate or select verbose outputs and label omissions instead of silently truncating necessary context. Keep historical requests out of routine context unless a concrete question requires them. Persist any reusable indexes/summaries as validated files or in memory, never a database or a write inside the immutable core.

An unchanged, already documented input set should not require another semantic generation call merely to repeat validation. Initial baselining may require substantial reading; incremental refreshes should target affected sources and topics. Do not achieve token savings by skipping required tests, omitting required coverage, using stale assumptions, changing the selected agent silently, or discarding necessary instructions.

Record actual token usage by operation/run/segment when the adapter supplies it, and expose useful totals in diagnostics/portal status. Report unavailable usage as unavailable; do not invent counts or represent missing telemetry as zero. Distinguish measured token savings from proxy measurements such as model calls or context bytes.

## 3. Product information organization

The product root contains these files and immediate directories:

- `.aih_product/config.yaml`
- `.aih_product/state.yaml`
- `.aih_product/input/`
- `.aih_product/output/`
- `.aih_product/change_requests/`
- `.aih_product/documentation/`
- `.aih_product/ledger/`
- `.aih_product/instructions/`

Do not add separate top-level memory, checkpoint, execution, communication, or skills directories. Immediate directory names must not overlap between `.aih/` and `.aih_product/`.

Keep `.aih_product/` non-executable: information and validated state only. Do not place executable scripts, plugins, hooks, or application code there. Treat examples and attachments as inert data; never import or execute them. Actual deployment scripts, infrastructure code, tests, and product source belong in normal product source locations outside this folder. Core portal assets belong in `.aih/engine/`.

Configuration holds supported declarative settings. State holds current execution references and status. Keep detailed history in its owning records rather than continually enlarging global state.

Each change request has a stable identifier and its own directory. Define conventions for its request metadata, submitted input revisions and attachments, evolving requirements definition, questionnaires, separate solution analysis, approved implementation plan and tasks, response history, execution records, checkpoints, verification evidence, documentation impact, and closure outcome. Create artifacts when needed; avoid empty folder and template proliferation.

Store the sole open request under `change_requests/active/<request-id>/`. On closure, move its complete record to `change_requests/history/<request-id>/` through a recoverable transaction. Maintain a metadata catalog under `change_requests/` with each request's stable ID, short scope/outcome summary, status, dates, location, and significant documentation/decision references. Completed, cancelled, and rejected outcomes remain distinguishable. Resolve links through stable IDs so archival does not break references.

Normal runs consult current product documentation and the active request, not the complete historical request corpus. Read catalog summaries or historical details on demand when a concrete question requires them. Preserve durable product knowledge and applicable decisions in current documentation before successful closure; historical requests must not become hidden prerequisites for ordinary work. Catalog entries do not create a backlog or authorize future work.

Compact resumable context for change work belongs to the request and its checkpoints. Bootstrap and standalone documentation-maintenance runs instead have stable system-operation IDs and validated audit/checkpoint records under `ledger/operations/<operation-id>/`, with user-facing summaries under `output/operations/<operation-id>/`. Link append-only ledger events to those records. Do not invent a change request solely to own setup work or add another top-level product directory.

An authorized maintenance task inside an open request keeps its evidence and documentation increment in that request. Keep system-operation status separate from request, Q&A, and product-verification status. Do not depend on unavailable conversations or private agent memory.

## 4. Instruction ownership and precedence

Respect the hosting agent's instruction hierarchy, tool restrictions, permissions, and existing user authorization.

Within AIH, explicit user directions and human-authored product instructions govern product behavior, subject to those host restrictions. Product instructions normally supplement framework behavior. Explicit behavioral overrides are exceptions and must be identifiable. Framework formats, state schemas, interfaces, and validation contracts remain fixed; behavioral customization cannot bypass them.

Only humans may edit product custom instructions. The agent may suggest wording in an output file but must not create or modify instruction content, even when it infers a useful preference. Initialization may create the directory and explain how the user can add instructions. A portal editor may persist deliberate human edits with revision checks.

Historical requests, imported documents, logs, source comments, attachments, and memory are context, not automatically active instructions. In particular, they cannot change executable paths, enable skills, weaken permissions, approve plans, or authorize deployment.

Record which instruction versions apply to an execution segment. Human edits made during execution take effect at controlled boundaries and trigger reassessment where necessary.

## 5. Input submission and the current response

Use `input/current.md` and an attachments directory for the current change-work ask. The user must be able to operate entirely through files and explicit Python commands, without chat or the portal.

Saving input or questionnaire answers creates drafts only. It never starts execution or silently changes the scope of an active process.

Explicit Clarify, Analyze, Implement, Implement directly, or Resume actions submit the latest relevant saved input and answers. Capture immutable submission revisions, attachment identities and content fingerprints, action, timestamp, and owning request. Detect repeated submissions and commands idempotently.

Preserve the previous submitted version before reusing input. Do not overwrite newer user edits while snapshotting or clearing drafts. Validate partial or contradictory questionnaire edits and explain required corrections.

An active process may adopt a newly submitted revision only at a controlled checkpoint. Persist progress first, reassess affected work, and restart an execution segment when necessary. If a safe interruption cannot be confirmed, keep the submission pending and show its status. Pending amendments to the same request do not constitute a backlog.

Scope changes invalidate affected plan approval, verification, and documentation freshness. Cosmetic changes need not invalidate unrelated evidence; record the determination.

Use `output/current.md` as the single current response for change work. Before replacing it, preserve its previous version in the owning change request. Include request, submission, and run references, outcome, blockers/questions, and next action. Additional evidence belongs to the request and can be linked from this response.

## 6. Independent read-only questions

Provide a separate communication lane for questions, explanations, and investigation that do not modify the product. It is available when no request exists and while the sole request is active or blocked.

Use `input/questions/current.md` as its draft entry point, with stable submitted question records under `input/questions/`. Submit through an explicit Ask action. Store answers under `output/questions/<question-id>/`, as Markdown and, when useful, JSON or other inert files. Provide a compact navigation index. These files must not overwrite the current change-work response.

Questions do not create change requests, occupy the active-request slot, change request approval, or resume blocked work. They may refer to an existing request.

Read-only means no changes to product source, durable product documentation, product configuration, custom instructions, or change-work state. The harness may persist the question, answer, permitted attachments, and its own communication/execution metadata.

Use read-only agent permissions where supported and have the trusted worker write communication outputs. If read-only enforcement is unavailable, report the limitation and offer a constrained or manual route instead of claiming protection through prompting alone.

Answers identify sources, relevant observed content versions, and uncertainty. If concurrent implementation changes inspected files, report the changed or mixed observation rather than presenting it as a consistent verified snapshot. Do not modify the product to demonstrate an answer.

If a question requests a modification, explain that it requires an explicit change-work action. Never silently convert it into a second request. A question answer does not itself authorize implementation or resolve a blocking request questionnaire without explicit submission to that request.

## 7. Change-request lifecycle and authorization

Implement explicit stages:

1. Submit the initial ask and open the sole request, or amend that request.
2. Clarify what needs to change and why: establish the problem, intended outcomes, affected users, required behavior, scope, constraints, and acceptance criteria; preserve a refined requirements definition.
3. Invoke Analyze iteratively to assess how to satisfy the clarified requirements, apply submitted answers and amendments, resolve questions, and generate or revise a sequential task plan with tests and documentation work. Planning is an activity inside Analysis; there is no separate Plan command.
4. Obtain human approval of the identified plan and scope revision.
5. Start implementation only when explicitly requested.
6. Handle submitted modifications within the still-open request.
7. Verify, pass required tests, update documentation, and assemble evidence.
8. Close successfully when every completion condition is satisfied.

Clarification owns requirements understanding, not implementation design. Its deliverable records the problem and rationale, stakeholders/users, desired outcomes, current versus required behavior, in-scope and out-of-scope work, functional and nonfunctional requirements, explicit constraints, acceptance criteria, assumptions, and unresolved questions. Acceptance criteria express observable outcomes and conditions for success, not a prematurely selected implementation or test framework.

During clarification, the agent may perform read-only inspection of existing code, documentation, interfaces, and other available evidence to understand current behavior, identify dependencies or feasibility concerns, and discover missing requirements. Record observations and contradictions without choosing a solution, changing product implementation, or committing to architecture, technologies, algorithms, component changes, implementation tasks, or test tooling. Clarification may write its requirements, questions, evidence references, responses, and workflow records.

Technical constraints explicitly supplied by the user remain requirements and retain their provenance. Do not discard them merely because they concern technology, and do not infer that an existing implementation choice is a required constraint. For example, "must work offline" belongs in clarification; selecting a local storage technology belongs in planning unless the user has explicitly required that technology.

Analysis owns the implementation approach and includes planning: solution design, architecture and technology choices, affected components, implementation tasks, and the verification strategy. Preserve traceability to the clarified requirements and distinguish design decisions from requirements. If planning exposes a missing requirement or consequential ambiguity, preserve the draft plan and return that question to clarification within the same request. Stop change work when the gap is consequential. Update the requirements from submitted answers, reassess affected plan approval and evidence, and resume planning from the clarified definition. Do not silently redefine requirements to suit a preferred solution.

Clarify must neither implement nor decide how the change will be implemented. Analyze must not implement. Approving a plan alone must not start implementation. Offer a clearly labeled combined Approve and implement action if useful; record both actions.

The explicit Implement directly action skips a separate user-invoked Analyze command and separate plan approval, but never skips the task plan. Before changing product implementation, perform the necessary analysis internally and persist a sequential plan containing implementation, test creation/execution, documentation, and evidence tasks. Record direct implementation authorization bound to the submitted scope and resulting plan, not a fictional human approval. This route need not create every optional analysis file. It does not waive consequential clarification, user selection of unrelated defects to include, passing tests, documentation, execution logs, results summaries, or host approvals. Material scope expansion still requires explicit authorization.

Authorization applies to identified scope. Preserve valid prior authorization; do not repeatedly request it. Material scope amendments require current authorization rather than inheriting an unrelated approval or shortcut.

Distinguish workflow phase, request lifecycle, worker execution status, and task outcome. A stopped or successful CLI process is not a completed request.

When a consequential blocker occurs, record the immediate evidence, relevant known-defect/documentation status, response, and checkpoint, then stop the entire change-request workflow safely. These necessary records do not authorize repairs, further implementation tasks, or scope expansion. Do not continue independent implementation tasks or choose different product work. The portal and independent question lane remain usable. Optional unanswered questions may use clearly documented defaults.

Reject attempts to open another request while one is open. Do not silently close, replace, archive, or queue the active request.

Separate stopping an execution from closing a request. A stop/cancel-run action leaves the request resumable. The user may explicitly close a request as cancelled or rejected, preserving partial changes, evidence, and unresolved outcomes. Do not automatically roll back files. These outcomes are not successful completion.

Successful completion requires implemented scope, passing required tests, satisfied verification and acceptance criteria, current affected documentation or a justified no-impact result, and recorded evidence. Skipped, failing, stale, or unexecuted required tests do not count as passed. Define genuinely inapplicable checks explicitly rather than inventing test passes.

Integration and deployment are separate milestones. Do not require Git, merging, or production deployment to complete a request unless its explicit scope requires them. Subsequent changes after closure require a new request.

### Iterative Analysis command

Keep Clarify as the separate requirements-understanding command. Provide one repeatable Analyze command for the Analysis phase, with `analyze` as its CLI operation. Remove the standalone Plan action from CLI and portal workflows. The same Analyze command handles initial analysis, submitted questionnaire answers, submitted amendments/additional directions, updated human-authored product instructions, and plan generation or regeneration according to persisted state.

At each explicit invocation, snapshot the latest submitted input and answers, reconcile state, and identify changes since the previous analysis revision. Apply authorized amendments to the interpretation, review affected assumptions and design decisions, and update only impacted analysis artifacts. Human-owned instructions remain human-edited; applying directions does not authorize the agent to edit their files. Honor safe execution boundaries and the one-writer rule if an implementation process is still active.

When consequential information is missing, persist the analysis and questionnaire and pause. Requirement gaps return to clarification within the same request; implementation/design questions belong to Analysis. The next explicit Analyze invocation may apply submitted answers and continue the saved analysis; it must preserve the distinction between requirements understanding and design decisions. Do not require a different command merely to apply answered questions, and do not advance while consequential questions remain unanswered.

When requirements and necessary design decisions are sufficiently resolved, generate or revise the plan automatically and stop before implementation. Bind the plan to interpretation, submission, instruction, and relevant documentation/content revisions. Repeated Analyze invocations with unchanged relevant inputs should report the current result without gratuitously rewriting plans or resetting progress. Retain previous revisions and invalidate only affected approval/evidence when changes are material. Never erase completed task history during regeneration; record which tasks remain valid and which require rework.

### Analysis records

Define these files under the owning request's `analysis/` directory. Their formats belong in core conventions, not in behavioral prompts:

- `interpretation.md`: the canonical current request definition, rewording and consolidating submitted input, answers, and amendments. Include what and why, stakeholders, behavior, scope, explicit constraints, acceptance criteria, assumptions, open questions, and source/revision references. Clarify establishes this file; Analysis refines it only from submitted directions and decisions. Do not maintain another competing requirements definition. Distinguish inferred/proposed requirements from accepted ones.
- `questions.md`: a catalog of stable question IDs, category, context, status, submitted answer summaries, and links to the authoritative Markdown questionnaire/answer revisions. Preserve one editable source for each answer; this catalog must not become a second independent answer store. Distinguish draft answers from submitted answers.
- `solution_assessment.md`: an evidence-based architectural critique of feasibility, alternatives, tradeoffs, applicable practices, recommended approaches, and unresolved design choices. Consider relevant security, performance, data integrity, maintainability, dependencies, compatibility, deployment, migration, and recovery concerns. Distinguish observations from assumptions. Suggestions do not silently change requirements or authorize work.
- `unrelated_issues.md`: issues and defects discovered outside the current scope, with stable IDs, supporting evidence, affected areas, test impact, investigation status, user disposition, and links to the product known-defects catalog.
- `plan.md`: the versioned sequential implementation plan generated by Analysis, or generated internally by Implement directly before implementation changes.
- `documentation_increment.yaml`: the request's planned documentation changes and their subsequent application/verification evidence.

Keep the four interpretation, questions, assessment, and unrelated-issues records separate during normal Analysis. If no questions or unrelated issues are found, record that concise finding and its review scope rather than inventing content. Preserve revision history and relationships without duplicating full evidence in every file.

Use additional `impact_analysis.md`, `risks_and_decisions.md`, and `verification_strategy.md` files when substantive detail warrants them. For simple changes, keep concise equivalent sections in the assessment or plan. Cover current behavior, affected interfaces/components, dependencies, compatibility and operational consequences; risks, assumptions and decisions with rationale; and requirements-to-tests/verification mapping. Avoid empty files and generic best-practice boilerplate.

### Sequential plan and implementation contract

Each plan task has a stable ID, sequence, intended outcome, requirements/decision references, specific required changes, affected files and folders, action types such as create/modify/move/delete, dependencies, and completion criteria/evidence. Identify new paths as well as existing ones. If an affected path genuinely cannot be resolved yet, include a bounded investigation task and revise the plan from its evidence before performing the dependent change.

Execute implementation tasks sequentially in plan order. Record task states and outcomes; do not silently skip, reorder, or execute implementation tasks concurrently. Material changes to scope or approach require a revised plan and the applicable authorization. Preserve successful task evidence when valid and explicitly invalidate work affected by amendments.

Every plan includes explicit tasks to create or update tests for changed behavior, execute the complete maintained required test suite, repair authorized failures and rerun tests, apply the documentation increment, verify documentation, and record implementation results. Plan documentation work as part of the request rather than postponing it as future debt.

Implement is a separate explicit command. It uses the identified plan, its valid approval or direct-implementation authorization, current human-authored product instructions, and relevant current documentation. Before starting or resuming, reconcile changes to those inputs and the actual product files. Missing, stale, or materially inconsistent prerequisites prevent implementation until resolved.

### Tests and unrelated-defect disposition

The required test suite covers the current product tests and retained applicable regression tests from earlier change requests. Keep executable tests in normal product source locations; archived request evidence does not supply executable historical test copies. Maintain a defined suite inventory and coverage/acceptance mapping.

Run relevant checks during tasks and the complete required suite before successful completion. Diagnose failures, repair authorized in-scope defects, and rerun the complete suite after repairs until it passes against the final relevant content. An in-scope repairable failure starts this repair loop; it does not by itself require another authorization. Missing prerequisites, unexecuted required tests, and unresolved failures prevent a passing result.

Never remove, weaken, disable, or reclassify a test merely to obtain a pass. Changes to expected behavior and corresponding tests must trace to authorized requirements and remain reviewable. Do not execute obsolete incompatible historical test versions simply because an old request contains them.

When an unrelated issue is found, record it and ask the user which defects to include in this request, defer, or investigate further. Do not automatically expand implementation scope. Included defects become explicit interpretation amendments, plan tasks, test coverage, and documentation impacts; obtain the applicable approval for materially expanded scope. Implement directly does not bypass this user selection.

Maintain all established unfixed defects in the current product documentation's known-defects area, with stable IDs, symptoms, reproduction/evidence, affected content/components, impact, known workarounds when supported, disposition, and originating request or system-operation references. Label suspected issues as unconfirmed until evidence supports defect status. Keep request findings linked to this current catalog, and update resolved status after verified fixes. Defect entries describe product condition and do not create another active request or authorize future work.

A deferred defect that causes any required test to fail keeps the request blocked from successful completion. Recording or acknowledging that failure is never a waiver. The user may authorize its repair in the current request or close the request as cancelled/rejected; do not claim completion with a failed required test. Deferred defects that do not invalidate required tests or acceptance criteria may remain documented.

The independent read-only question lane retains its existing permissions. Findings from that lane may be reported in answers, but recording them in durable product documentation requires an explicitly invoked authorized change-work or documentation-maintenance action. A question answer never starts that action automatically.

## 8. Questionnaires

Editable Markdown checkbox questionnaires inside the change request are authoritative. The portal reads and edits the same files, using revision checks. Define their exact format in conventions.

Each question has a stable ID, context, single-choice or multiple-choice rules, clear options, a recommended option with a short reason, and an always-available free-text field for alternatives or modifications. Recommendations start unchecked and are not implied approval.

During clarification, questions and recommended choices concern the problem, rationale, outcomes, users, required behavior, scope, constraints, and acceptance criteria. Do not ask the user to select implementation approaches during this phase. Implementation alternatives belong to planning and must be identified as design choices rather than user requirements. Questions raised during planning that concern missing requirements return to clarification.

Gather questions in one batch after reasonable investigation. Ask later batches only when new information creates new consequential uncertainty. Make it easy to answer all questions in one copy-paste form.

Mark consequential blockers separately from optional choices. Explain documented defaults for optional unanswered questions. Preserve user wording and answer revisions. Handle mutually exclusive checks, malformed edits, partially answered forms, and a free-text answer modifying a checked choice without silently guessing.

Submitted answers remain linked to the definition, decisions, plan, and affected execution. Human approval and authorization fields cannot be self-issued by the agent.

## 9. Product documentation as current product knowledge

Maintain documentation automatically as a normal workflow responsibility. Consult relevant documentation during requirements clarification and before planning and implementation. During initialization, use deterministic inventory and agent-assisted reverse engineering to establish an evidence-based baseline, recording unknowns instead of fabricating facts.

Documentation describes current implementation in the local product files. Track intended requirements, observed implementation, verification, and deployment separately. Planned future behavior stays in its request until implemented; approved unmet requirements may appear in the requirements catalog with explicit status.

When documentation, implementation, and human intent disagree, record the discrepancy and distinguish observation from approved meaning. Ask before changing business meaning. Agent inference must never silently become an approved requirement.

Preserve human-authored content. Use file revisions and reviewable diffs without requiring Git. Update affected sections rather than rewriting all documentation on every run.

Track source dependencies and fingerprints. Check drift at run start and after relevant changes; metadata scans may cover the tree, but agents should read only relevant documentation content. External and manually managed components need provenance, last-known state, and explicit unknowns when live inspection is unavailable.

After each relevant change, identify affected documents, update them from evidence, link the owning request or system operation and verification, record unresolved issues, and refresh navigation. If an implementation stops partway through, do not present its old documentation as fully current: record known drift and reconcile it on resumption.

Every request maintains `analysis/documentation_increment.yaml`, including requests using Implement directly. During Analysis or internal plan preparation, record affected canonical document IDs/sections, proposed amendments, reasons, source requirements/decisions, and owning task IDs. During implementation, record actual changes, status, before/after content fingerprints or diff references, and verification evidence. Planned changes must never be reported as already applied.

The increment is a request-specific audit record; the documentation tree remains the canonical current product description. Refresh the increment when scope or actual implementation changes. Include known-defect catalog updates when relevant. If no documentation changes are needed, record a justified no-impact determination in the increment rather than omitting it.

Completion requires affected documentation updates or that justified no-impact determination, plus evidence that the increment is reconciled with actual results. Documentation failures remain visible and prevent successful completion.

The rebuild target is enough specification to recreate a functionally equivalent product and demonstrate equivalence through documented acceptance tests. Do not claim bit-for-bit reproduction or production data recovery from prose alone. Inventory necessary external resources and gaps. Actual operational scripts and IaC stay in normal source folders; documentation contains explanations, versioned/content-fingerprinted references, and inert examples.

### Reverse engineering existing products

Provide a Python `reverse-engineer` command with initial-baseline and incremental-refresh modes, plus deterministic inventory and operation status/resume interfaces. It must work on an existing plain product directory without Git, a database, or preexisting AIH documentation. Reuse the same pipeline for first-portal-start bootstrap.

First inventory available authorized source files, configurations, interfaces, tests, build/deployment definitions, and existing documentation through deterministic helpers. Extract supported facts without importing or executing inspected product code, hooks, or attachments. Preserve source references and extraction limitations; do not expose credential values. Inventory is evidence collection, not proof of runtime behavior.

Then use the configured agent to synthesize relevant architecture, components/dependencies, domain concepts, observed behavior, interfaces, data flows, operational context, and requirements supported by evidence. Populate the existing balanced documentation tree and applicability catalog, preserving human-authored content. Label inferred requirements, assumptions, contradictions, missing external information, and unverified behavior explicitly. Never convert inference into approved intent or mark product tests as passed because documentation was generated.

Reverse engineering writes product documentation and its own framework records while leaving product implementation, source configuration, executable tests, deployment code, and human-owned instructions unchanged. Newly identified defects are documented with evidence/uncertainty; repairs and refactoring require the established change-request workflow. This operation is distinct from read-only Q&A because it may maintain durable documentation.

For incremental refresh, compare source fingerprints and documented dependencies, inspect changed or newly relevant material, reconcile affected leaves/indexes, and preserve unaffected content. Record scope, provenance, gaps, before/after references, and validation results. Validate the tree and links through scripts. Do not claim that a structurally valid inventory or a partially generated tree is complete product documentation.

Initial bootstrap is an audited setup operation without a change request. Later standalone documentation maintenance is allowed only when no request is open. If a request is open, reverse engineering must be an explicitly authorized documentation task within it at a controlled execution boundary, using its documentation increment and evidence records. An idle worker does not remove an existing blocker. Reject competing standalone maintenance or report the blocker; do not silently interrupt implementation, unblock a request, or create a second workflow writer.

Persist progress before agent switches/interruption, reuse valid completed extraction/generation, and resume through the shared recovery helpers. If profile configuration, compatibility, credentials, or permissions prevent semantic generation, retain useful deterministic results and report documentation as pending/partial with actionable setup or manual-handoff guidance. Never silently select another agent or install a CLI.

## 10. Strictly balanced, progressively readable documentation tree

Use navigation catalog nodes internally and actual documentation only in terminal content leaves. The root catalog must be small enough to read first without loading the entire corpus.

Give every node a stable ID. Each non-root node has exactly one structural parent. Cross-references may link topics but are not structural edges. Maintain one canonical copy of a topic.

Every child catalog entry identifies its node ID, location, title, scope summary, applicability/status, and when to read it. An agent must be able to follow these entries to a needed topic without reading unrelated leaves.

Enforce these initial rules:

- At most eight direct children per catalog.
- Strict balance: the deepest and shallowest content leaves differ by at most one edge from the root.
- Target at most 1,500 words per content leaf. Split at meaningful boundaries; record justified exceptions for indivisible reference material.
- No structural cycles, missing targets, multiple parents, unreachable content, or duplicate canonical IDs.

These are supported configuration parameters, not schema overrides. Depth grows dynamically as content grows. Keep topic grouping meaningful while splitting, merging, or redistributing navigation catalogs. Do not replace strict balance with an unrestricted hierarchy. Avoid empty content and artificial padding documents.

Automatically reorganize when necessary. Preserve IDs and human-authored content, repair links, and record structural changes. When a topic is split, retain its ID for the continuing canonical topic, assign new IDs to new topics, and preserve mappings for old references.

Perform reorganizations through recoverable, revision-checked multi-file transactions. Supported readers must use shared read locks, versioned snapshots, or revision-change detection with retries to avoid observing a half-rewritten tree. Do not promise equivalent consistency to external readers bypassing that protocol. Validate the invariants after committed changes. Resolve IDs independently of physical paths. Search may supplement navigation but cannot replace the tree.

## 11. Documentation coverage

Maintain a progressively navigable applicability catalog covering every category below. Mark categories applicable, not applicable with rationale, or unknown needing investigation. Create substantive documents only when relevant; do not generate empty templates for every category.

Cover:

- Product purpose, scope, capabilities, stakeholders, users, terminology, domain knowledge, and definitions.
- Business requirements, rules, processes, acceptance criteria, and requirement-to-implementation-to-test traceability.
- Nonfunctional requirements, service objectives, performance, capacity, availability, accessibility, localization, and supported platforms.
- Architecture, component responsibilities, solution design, architectural decisions, alternatives, and tradeoffs.
- Product/repository structure, important folders and files, ownership, and entry points, without assuming a repository exists.
- Data structures, logical and physical models, storage, data ownership, lineage, quality, retention, privacy, and migrations.
- ETL and transformations, pipelines, orchestration, schedules, semantic models, reports, dashboards, and analytics definitions.
- Algorithms, functional logic, APIs, interface contracts, integrations, events, queues, and external services.
- UI definitions, visual and interaction design, web interfaces, navigation, user flows, error behavior, and user help.
- Networking, authentication, authorization, roles, secrets references, threat models, security controls, and relevant compliance constraints.
- Dependencies, versions, licenses, build requirements, configuration, feature flags, and environment differences.
- Deployment procedures and script references, releases, infrastructure, cloud services, resource inventories, and relevant cost assumptions.
- Unit, integration, system, acceptance, performance, and security testing; test data, fixtures, expected results, and evidence.
- Backup, recovery, disaster recovery, restore validation, operational continuity, and rebuild prerequisites.
- Logging, monitoring, alerting, incident response, troubleshooting, administration tools, and support interfaces.
- Operational processes, schedules, maintenance, data operations, escalation, and handover.
- User guides, onboarding, administration guides, support materials, known limitations, a dedicated known-defects catalog, deprecation, and retirement.
- Any additional product-specific knowledge needed to preserve its definition and support functional reconstruction.

For relevant content, record provenance, update dates, source fingerprints, owning requests or system operations and decisions, verification status, and unresolved review items. A navigation catalog must not become a huge flat copy of all documentation.

## 12. Changes ledger and evidence

Use append-only structured change and decision events under `ledger/`, plus a generated readable index. Corrections append superseding events; they do not silently rewrite history.

Give events stable IDs and links to requests or system operations, applicable submissions, runs, affected artifacts, and decisions. Detailed change-work evidence remains in its request; bootstrap/standalone maintenance evidence belongs to its system-operation record. Ledger and state updates must be recoverable and idempotent across interruptions.

Preserve decisions, outcomes, test and verification evidence, and sanitized execution events. Apply configurable retention to verbose CLI output; document the effective policy and never prune silently. Essential request history and decision evidence are not disposable verbose logs.

Record useful summaries and observable actions, not private chain-of-thought. Do not claim to capture unavailable conversations. Append-only files and hashes provide auditability but are not tamper-proof against an actor able to rewrite them.

### Implementation logs and results summaries

Every implementation attempt, including normal Implement, Implement directly, resumed segments, failed attempts, and cancelled execution, has durable records under its owning request's execution records. Use per-run/segment identities and define `implementation_log.jsonl` and `implementation_summary.md` in conventions. Create their initial records before product implementation starts, and update progress throughout the run.

The log records timestamps, run/segment and task IDs, relevant input/plan revisions, available execution events, intentions before consequential observable actions, results afterward, observed file changes and evidence references, test invocations/results/content versions, documentation updates, errors, cancellations, and checkpoints. Flush records incrementally through validated helpers rather than relying on a final model response. Distinguish attempted, confirmed, failed, and uncertain actions; summarize decisions without private chain-of-thought and redact sensitive data before persistence.

The human-readable summary explains what was requested and attempted, which tasks completed or remain incomplete, what actually changed, test and verification outcomes, documentation increment status, included/deferred defects, blockers, uncertain outcomes, recovery guidance, and next action. Link it to detailed evidence so a user can investigate an unexpected result or failure. Process exit status and product task outcome remain separate.

A crash can prevent a final agent-authored summary. The worker and recovery path must retain available events/checkpoints, reconcile files and side effects, and produce a clearly labeled reconstructed summary on recovery. Do not fabricate a complete action history or claim visibility into operations a CLI did not expose. Preserve unknown outcomes until evidence resolves them, and inspect whether an action succeeded before retrying it. Logs and summaries remain part of the archived request after closure.

## 13. Portable skills, catalog, and discovery

Follow the published Agent Skills specification: each skill directory contains `SKILL.md` with valid YAML metadata and behavioral instructions, plus optional resources. Use the standard metadata extension mechanism for AIH-specific information. Discovery returns metadata, compatibility, availability, enabled status, and locations without returning instruction bodies.

Load a skill body only when selected; load its resources only when needed. New installed skills must be discovered without editing `run.md`. Handle disabled, malformed, duplicate, and incompatible skills with actionable diagnostics. Ambiguous duplicate identities must not be resolved silently.

Every delivered skill must be usable outside AIH by copying its directory, without an exporter, installed AIH engine, portal, database, or hard-coded `.aih_product/` location. Ordinary skills must not require Git. A purpose-specific skill may declare intrinsic dependencies, such as Git and a repository for the optional Git skill. Declare genuine runtime/tool dependencies and accept explicit input/output locations.

Resolve shared conventions and portability as follows:

- `.aih/conventions/` is the authoritative authoring source for shared framework formats, schemas, and templates.
- During core build or release, bundle each skill's required conventions, guidance, and deterministic Python helpers into that skill as generated, versioned resources. Standalone skills must invoke their bundled helpers for those operations, preserving the same contracts without requiring an installed AIH engine.
- Record their source versions and hashes; validate equivalence and reject stale or conflicting bundles.
- AIH integration uses canonical contracts. Standalone execution uses the matching bundled resources.
- The delivered skill is already self-contained. Ordinary product runs never regenerate resources or change the core.
- Required behavioral guidance must also be available in the skill package; an external reference to a shared prompt cannot be its only implementation.

Keep framework state transitions in the engine integration layer. Standalone skill execution must not require recreating the entire AIH lifecycle.

### Initial skill roster

Create all eight skills in the initial complete delivery. The seven core skills are enabled by default; `git-workflow` is installed but disabled by default. Availability still depends on declared prerequisites and the selected profile. Enabled does not mean authorized to execute, and a required unavailable or disabled capability must produce an actionable blocker rather than silently skipping its work or enabling another skill.

Use the following stable IDs as package directory names under `.aih/skills/`. Each package must contain working behavioral guidance, its input/output contracts, needed resources/helpers, and standalone usage examples; catalog entries or placeholder `SKILL.md` files alone do not satisfy delivery.

| Skill ID | Responsibility and selection conditions | Main outputs |
|---|---|---|
| `clarify-requirements` | Establish what must change and why: problem, users, outcomes, current versus required behavior, scope, constraints, acceptance criteria, contradictions, assumptions, and unanswered questions. Use during Clarify or when a requirement gap is exposed by another authorized workflow. Read-only investigation is permitted; choosing an implementation is not. | Canonical request interpretation, clarification questionnaires, answer/source references, and explicit unresolved requirements. |
| `analyze-and-plan` | Iteratively apply submitted answers and amendments; assess feasibility, alternatives, dependencies, architectural and operational risks, affected components, and unrelated defects; generate or revise the sequential implementation, testing, documentation, and evidence plan. Use during Analyze and internally for explicitly authorized direct implementation. | Required analysis records, sequential tasks with affected paths, requirements-to-task/test mapping, verification strategy, and planned documentation increment. |
| `implement-plan` | Execute authorized tasks sequentially using the identified plan, current product instructions, and relevant documentation. Make scoped product changes and repair authorized defects. Support normal and direct implementation while preserving prerequisite checks and checkpoints. | Product changes, task outcomes and evidence, incremental implementation log, readable results summary, and recoverable incomplete-work records. |
| `test-and-verify` | Design and create/update tests during authorized implementation; execute the complete maintained required suite through deterministic helpers; investigate failures and verify acceptance criteria against the actual checked content. Test strategy may inform Analysis, but test-file changes and execution must respect the current action's authorization. | Product tests, suite inventory and requirement-to-test mapping, execution results, failure analysis, content-bound verification evidence, and explicit unexecuted or stale checks. |
| `reverse-engineer-product` | Establish or refresh understanding of an existing product from authorized source, configuration, tests, interfaces, and existing documentation. Use for initial baselining, authorized incremental refresh, and evidence collection where appropriate. Distinguish observed facts, inferences, and unknowns without changing product implementation. | Evidence-backed baseline content, source references and fingerprints, discovered issues, documentation gaps, and explicit extraction/verification limitations. |
| `maintain-documentation` | Apply authorized documentation increments and maintain current product knowledge, known defects, applicability coverage, traceability, catalogs, cross-links, and the balanced tree. Use for request documentation tasks and authorized bootstrap/maintenance operations. | Current documentation, applied/verified increment records, known-defect updates, catalog/link changes, structural-change records, and documentation validation results. |
| `answer-product-questions` | Answer independent read-only questions from relevant current or explicitly identified historical evidence, including while change work is blocked. Preserve the separate question-lane permissions; do not alter implementation, request scope, product instructions, or durable product documentation. | Answer files under the question output area, question-owned records, source/content references, and explicit uncertainty or freshness limitations. |
| `git-workflow` | Optional extension for Git operations governed by configured rules and existing scoped authorization. Declare Git and repository dependencies; do not make them prerequisites of ordinary framework operation. | Results and evidence for authorized inspection, branch, diff, commit, push, or PR operations. Installation/enablement alone grants none of these actions and never grants integration, publication, deployment, or destructive authority. |

The skill roster does not introduce extra user-facing workflow stages or automatically runnable commands. Analysis owns planning, so do not add a separate planning skill or Plan command. Direct implementation must invoke the necessary analysis/planning capability internally and persist its plan before product changes; it must not require a separate Analyze invocation or fabricate human approval. Standalone `implement-plan` must include the analysis/planning guidance and helpers needed for this mode inside its own package; it must not depend on another installed AIH skill. Apply the same self-contained rule to other cross-skill capability reuse.

Test failure diagnosis does not authorize unrelated repairs. `test-and-verify` reports failures and their scope relationship; `implement-plan` performs authorized product fixes. Tests may be authored only within the authorized implementation scope. A deferred defect failing a required test continues to block successful completion; skills may not weaken or suppress tests to report success.

Reverse engineering owns baseline discovery and source-grounded interpretation; documentation maintenance owns applying and organizing that knowledge. Share contracts/helpers and reuse valid evidence rather than generating competing baselines or repeating source reads. An authorized bootstrap or maintenance operation may use both skills under the same operation identity. Ordinary read-only questions may inspect existing evidence but must not invoke documentation-writing effects.

Initialization, approvals, state changes, locks, snapshots, controlled execution, catalog generation, archival, and routine recovery bookkeeping remain deterministic Python engine operations, not separate agent skills. All skills use the required helpers. After interruption, the owning skill resumes its semantic work from reconstructed evidence and checked state; recovery never silently grants new authority. Keep shared routing in `run.md`; do not duplicate the whole orchestrator in each package.

### Catalog artifacts and metadata

Deliver `.aih/skills/catalog.yaml` as the compact machine-readable catalog and `.aih/skills/README.md` as its human-readable counterpart. The README explains when to use each skill, its outputs, important boundaries, and links to its package; do not duplicate full skill instructions in either catalog. The portal's Settings > Skills view and CLI listing use the same discovery contract.

Define the catalog schema and validation rules under `.aih/conventions/`. Skill package metadata is the authoritative source for the derived installed catalog; retain AIH-specific fields through the standard metadata extension mechanism. Every entry must identify:

- Stable ID, display name, package version, and concise purpose.
- Selection conditions/capabilities and the cases in which the skill must not be used.
- Input/output contract references and supported standalone parameters, including explicit input/output locations.
- Possible effects and write scope, prerequisites, and required authorization checks; declared effects are descriptions, never authority grants.
- Genuine tool/runtime dependencies and compatibility requirements.
- Package location, metadata/resource fingerprints, and referenced convention/helper bundle versions needed for integrity checks.

Generate and validate both catalogs through Python during core build, installation, upgrades, or explicit core maintenance. Derive them from the same metadata to prevent independently edited conflicting rosters. Include all eight initial packages. Ordinary discovery, listing, selection, and execution must not regenerate a catalog or write anything into `.aih/`.

Discovery reads and validates package metadata without passing skill bodies to the model or executing package code. It must identify newly installed skills without changes to `run.md`, compare the installed metadata against the generated catalog, and report missing/stale catalog entries or malformed, duplicate, and incompatible packages. Read-only discovery can report validated newly installed metadata in its effective in-memory inventory; catalog regeneration and installation integrity reconciliation remain explicit maintenance operations. An integrity/identity problem must not be silently bypassed to execute a package.

Keep installed metadata separate from dynamic state. Store supported enable/disable configuration by stable skill ID in `.aih_product/config.yaml`; compute effective enabled status, current dependency availability, and compatibility from that configuration and validated diagnostics. Do not write product-specific status into the core catalog. Display installed, enabled, available, and authorized as distinct concepts. Use the shared revision checks and safe execution boundaries for configuration changes, preserving effective skill/version references for active and historical run segments.

Load compact metadata first, select only the capabilities required by the current authorized action, and load each selected skill body/resources on demand. Do not routinely read the entire catalog's linked resources or every skill body. New extensions use the same discovery and portability contracts; the initial roster must cover the complete agreed workflow without depending on unspecified future skills.

Skill discovery must not execute code or install dependencies. Skill enablement is declarative, but adding executable adapters or changing trusted executable settings is explicit core/local administration. Metadata and product documents must never trigger arbitrary dynamic imports, installation, or command execution.

## 14. Agent profiles and CLI adapters

Provide a common Python adapter contract, a functional Codex CLI adapter, and manual handoff. Support multiple named profiles and installed adapters without coupling profile names to agents or changing `run.md`.

Profiles identify adapter, trusted executable reference, supported model/settings, timeouts, permissions, and credential environment-variable references, never credential values. Support a default profile, per-capability assignments, and explicit per-run selection. Document precedence and record the effective selection for every execution segment.

Validate settings against the selected adapter's schema. Reject arbitrary command templates, executable configuration, and unrestricted argument strings. Resolve privileged executable settings only through deliberate local administration; ordinary requests and agent-generated content cannot modify them.

Provide diagnostics that resolve the executable, detect its version, check adapter compatibility, inspect documented authentication status where available, and return actionable setup guidance. Distinguish credentials being present from verified service access. Do not install or upgrade CLIs automatically.

Verify invocation syntax against official documentation and installed help. For Codex, use its documented non-interactive execution and event interfaces. Support plain product directories using the documented non-Git option where compatible; never initialize Git to satisfy an adapter check. Verify resume syntax separately instead of assuming all start options also work for resume.

Each adapter declares and implements availability checks, start, available output/event streaming, run/session identifiers, exit status, timeout, cancellation, and supported resumption. If native resumption is unavailable, start a new session from persisted harness state and label it accurately. Never silently switch agents.

Invoke processes with argument arrays, no shell interpolation, explicit working directories, and an environment containing only required operational/authentication variables. Preserve host restrictions and user-approved permissions. Do not silently enable unrestricted execution, suppress inherited rules, or bypass approval controls.

Every agent receives instructions to follow `.aih/run.md`, use the deterministic helpers, and respect the identified action, request/question/system-operation ID, applicable submission, profile, and segment. Bootstrap/standalone maintenance use explicit operation parameters and source revisions instead of fictional request/submission records. Prevent recursive spawning of the same run through explicit parent/run ownership checks.

Portal execution uses documented non-interactive modes. If required approval cannot be handled, pause and offer manual handoff. Profile or capability changes apply to subsequent runs or explicit subsequent segments after a checkpoint, not to a live process. Do not assume conversation state transfers between different CLIs.

Persist resolved CLI versions and non-secret effective settings. Sanitize events before persistence or display; exclude credentials and private reasoning. A zero process exit does not prove task success.

## 15. Shared state, verification, and recovery

Define versioned schemas for configuration, state, skill catalogs and their metadata/integrity references, skill enablement, requests and their catalog, submissions, interpretation/analysis artifacts, sequential plans/tasks, questionnaires and their catalog, approvals, defect dispositions, documentation increments, system operations and bootstrap progress, inventory/extraction results, reusable summaries and their dependencies, available usage metrics, events, checkpoints, documentation nodes, evidence, implementation logs/summaries, and run records. Keep clarified requirements and implementation design/plan artifacts distinct, and bind each plan to its source requirements-definition revision. Portal, helpers, and agents must use the same contracts.

Global state includes the active request reference, phase and status, artifact references, analysis/submission/plan revision references, current sequential task, blockers, next action, checkpoint, run and segment IDs, selected profile, revision, verification status/content fingerprints, and pending documentation updates. Q&A and system-operation execution references must remain distinct from change-work state. Track initialization/documentation-generation status separately from product test and verification results.

Implement safe YAML parsing, validation, atomic replacement, optimistic revision checks, and appropriate file locking. Multi-file operations require a journal or equivalent recoverable file transaction protocol; atomic replacement of one file is insufficient. Report conflicts rather than silently overwriting human or agent changes.

Detect direct edits through content/revision checks. Provide documented stale-lock recovery, process identity checks, and interrupted-transaction reconciliation. Do not treat deletion of a lock as proof that its former process has stopped. Explain limitations when external agents bypass helpers.

Checkpoint before interruptions, profile switches, and operations with consequential partial outcomes. Record completed work, outstanding work, relevant content versions, and uncertain side effects.

On resumption, reconcile files, state, approvals, process status, and evidence. Inspect whether an interrupted action already succeeded before retrying. Use operation IDs and reconciliation to avoid duplicate external writes; if success cannot be established, report uncertainty instead of blindly retrying.

Verification must bind to the actual checked content, including uncommitted or non-Git files. Use defined content manifests and relevant dependency fingerprints. Record test selection, commands or invocation identifiers, results, environment, and checked versions. Source changes invalidate affected evidence.

Exclude volatile logs, answer timestamps, and bookkeeping revisions from product-content fingerprints so routine record updates do not invalidate their own evidence. Track documentation freshness and test evidence separately where their dependencies differ.

Stop child processes safely on supported platforms during cancellation/timeouts. Record partial results and whether termination is confirmed. Do not label work safely stopped or permit another writer when a child process may still be changing files.

Core immutability, read-only behavior, and human-owned instruction protection need helper validation plus supported host permissions. Checksums detect changes; they do not enforce a boundary against an actor with permission to rewrite everything. Describe actual enforcement and remaining limitations accurately.

## 16. Local web portal

Provide a Python command that starts the portal and opens the default browser. Bind to loopback by default, support a configurable port and no-browser operation, print the URL if browser opening fails, and handle port conflicts and shutdown cleanly. When `.aih_product/` is absent, automatically initialize it and start evidence-based documentation baselining through the configured agent; do not stop at showing setup guidance.

Target one local user. Do not require a shared server, cloud account, database, or Git. Keep the interface clear and focused on user actions rather than internal implementation details.

On first startup, use an exclusive recoverable bootstrap operation: run Python initialization/validation, collect a deterministic inventory, run semantic documentation generation through the configured compatible profile, and validate the resulting documentation. Starting the portal with missing product state authorizes this setup sequence; editing ordinary drafts still never triggers execution. Profile selection follows the existing configured precedence and trusted local settings, not opportunistic discovery of any installed executable.

Keep initialization and generation outside HTTP handlers. Open a responsive progress view showing phases, completed work, pending documentation, gaps, errors, and required input. Persist the operation identity before launching workers. Browser refreshes, repeated starts, and concurrent portal processes must reuse/reconcile that operation rather than duplicate work. Resume interrupted initialization from checkpoints while preserving user edits and already valid results.

Distinguish a missing folder, partially initialized state, and invalid existing state. Resume recoverable partial setup; report invalid existing files without overwriting them or treating them as a fresh installation. A completed setup must not regenerate its documentation on every portal launch. Use the explicit refresh workflow when appropriate.

If no usable configured profile/authentication is available, complete the safe deterministic setup, retain its evidence, and display semantic documentation generation as pending setup. Guide profile selection/authentication or manual handoff without automatic installation, silent fallback, or false completion. Authentication presence alone does not prove that generation succeeded. After prerequisites are resolved, resume the recorded operation through an explicit user action. Distinguish generated documentation, unresolved gaps, and verified product behavior in status.

Use the portal as the main working interface. Provide these eight navigation pages, each using the same underlying files and validated Python helpers as the CLI:

1. **Overview**: active request, phase, next action, blockers, current response, test status, documentation status, and selected agent profile. Offer Start request only when no request is open. Show initialization/maintenance progress and pending setup separately from change work; expose available token usage without inventing unavailable values.
2. **Current request**: the complete workspace for input, clarification, analysis, the generated plan, approval, sequential implementation, verification, documentation, and outcome. Use the six tabs specified below.
3. **Ask a question**: independent question editor, attachments, explicit Ask action, progress, answer-file links, source/content references, and question history. Remain available while change work is blocked and preserve the read-only Q&A contract.
4. **Product documentation**: progressive tree, breadcrumbs, search, applicability, provenance/source links, update dates, freshness, known defects, and unresolved reviews. Offer initial/incremental reverse engineering and refresh only when workflow ownership and permissions permit them. Explain when an active or blocked request prevents standalone maintenance.
5. **Runs and recovery**: current and previous runs, sanitized live events, task/segment progress, checkpoints, errors, implementation/results summaries, evidence, available usage, and permitted stop/resume/recovery actions. Include bootstrap and maintenance records with their system-operation identities; distinguish process outcome from product-task outcome and documentation generation from verified product behavior.
6. **History and decisions**: a closed-request catalog with short summaries, dates, and completed/cancelled/rejected outcomes, plus a separate tab for the changes/decisions ledger. Load full historical records only when selected. Preserve links to evidence; do not create a backlog or implicitly reopen a closed request.
7. **Settings**: agent profiles, defaults and capability assignments, compatibility/authentication diagnostics, the searchable Skills catalog, supported declarative product settings, and a human-editable custom-instructions area. Skills shows purpose, installed version, enabled state, dependencies, compatibility, availability diagnostics, and links to usage/input/output details. Enable/Disable changes supported product configuration only, with its effective execution boundary; it does not install packages, invoke a skill, approve a plan, or grant Git/deployment authority. Keep privileged executable/permission settings distinct from ordinary content. Only deliberate human edits may change custom instructions; agent suggestions belong in outputs. State when settings will take effect and preserve active-process boundaries.
8. **Help**: searchable detailed guide, getting-started walkthrough, workflow and authorization explanations, command reference, file locations, examples, troubleshooting, recovery, and limitations. Render the maintained `.aih/USER_GUIDE.md` and shared command metadata rather than maintaining a separate conflicting guide. Provide contextual links from relevant controls to stable help sections.

The Current request page has these six tabs:

- **Input and clarification**: current input and attachments, draft/submitted indicators, Save draft, Clarify, editable questionnaires, the canonical interpretation, and submitted revisions with reviewable differences. Show current responses and their request history here or through linked response panels.
- **Analysis**: the repeatable Analyze action, current analysis progress, architect assessment, question-and-answer catalog, optional impacts/risks/decisions, and unrelated issues with explicit include/defer/investigate controls. Apply selections through submitted revisions. Analyze generates/regenerates the plan; do not expose a separate Plan command.
- **Plan**: plan revision and source interpretation, ordered tasks and affected files/folders, mandatory test/documentation tasks, differences from the previous plan, approval status, and Approve plan. Approval alone must not start implementation. A combined Approve and implement action, if provided, must explicitly represent and record both actions.
- **Implementation**: Implement, Implement directly, Resume, and Stop execution, with sequential task states, available live events, file-change evidence, the implementation log, and the results summary. Explain that Implement directly generates the required plan internally while skipping a separate Analyze invocation and plan approval; it does not waive tests, documentation, evidence, or unrelated-defect scope selection.
- **Verification and documentation**: required test results and checked content versions, failed/unexecuted checks, repair attempts, documentation increment, applied amendments, remaining gaps, and linked evidence. Do not provide an accept-failure shortcut for required tests.
- **Outcome**: overall result, unmet completion conditions, unresolved defects, final summary, and distinct Close as cancelled/rejected actions. Successful completion is exposed only after every required gate passes. Stopping a process leaves the request open unless the user explicitly chooses a closure outcome.

Use a persistent header showing product, active request, phase, execution status, and selected profile, with explicit empty/initializing states. Make the relevant next action prominent and keep other allowed actions discoverable. Use ordinary language on human-facing pages; IDs, hashes, and detailed technical evidence remain available on demand.

Keep Save draft, submit/run actions, Stop execution, and Close request visibly distinct. Saving forms never runs the agent. Show pending same-request submissions separately from executing work. Explain unavailable actions with their specific cause, such as an open request, stale approval, unresolved blocker, missing profile, or failed required test. Do not silently queue a new request.

Present revision conflicts with the competing changes and explicit resolution instead of overwriting edits. Settings changes must show their execution boundary. Link contextual help to the relevant action and workflow state. Display sanitized execution events through streaming or polling and provide readable summaries without requiring users to inspect raw logs for routine progress.

Run agent work outside HTTP handlers through a controlled worker/subprocess. Keep the portal responsive. Deduplicate repeated clicks, refreshes, and retried requests; never launch duplicate writers. Support Q&A separately without using it to bypass change-work restrictions.

Manual handoff produces usable instructions and evidence expectations. Clearly show that execution takes place in an external agent; do not label it running or completed without evidence.

Protect against path traversal, symlink/junction escapes, arbitrary filesystem access, cross-origin writes, and unsafe content rendering. Validate origins and hosts and protect state-changing requests. Render Markdown safely; do not execute HTML, scripts, commands, hooks, or active attachments supplied through product files. Serve user outputs safely.

Do not expose a generic arbitrary-command endpoint. Privileged agent executable and permission configuration must be separated from ordinary content operations. Keep credentials outside persisted configuration, tracked files, outputs, and logs; store only references and redact sensitive values.

## 17. Installation, commands, and upgrades

### Windows/Linux menu launchers

Provide a shared interactive terminal menu as the Python CLI's `menu` operation. Supply optional `.aih/menu.cmd` for Windows and `.aih/menu.sh` for Linux; each only locates/invokes this Python menu with safely handled paths and arguments and reports minimal runtime/startup errors when Python cannot run. Keep all menu rendering, input validation, root resolution, settings, operation dispatch, lifecycle management, and framework/workflow error handling in Python. Do not interpret commands or hooks from product content in either launcher.

Support direct invocations such as `py .aih/engine/cli.py menu` on Windows and `python3 .aih/engine/cli.py menu` on Linux. Document supported Python selection and Linux executable permissions/terminal invocation. Do not claim universal desktop double-click behavior. Provide an actionable error if the required Python runtime is unavailable, without automatic installation.

The menu offers Open portal, Show current status, Configure/check agent profiles, Initialization/reverse engineering, Validate framework/product state, Inspect/resume interrupted operations, Open help, and Exit. These actions use the same typed Python APIs as the portal and CLI. Display current root/state and availability; preserve authorization, blockers, and recovery rules rather than introducing another workflow implementation.

Resolve the product root reliably from the installation or an explicitly selected valid root, independently of the launching shell's working directory. Handle installation paths containing spaces and special characters. Repeated launches must detect/reuse the appropriate portal or report its status and must not create duplicate workers. Simply opening the menu or help must not start product work; choosing Open portal retains the agreed automatic first-run initialization behavior. Exiting the menu must not silently cancel an existing run or close a request; explicit shutdown follows the controlled process-lifecycle rules.

### Quick start and shared help

The required `.aih/README.md` provides the initial knowledge needed to start: purpose, supported prerequisites, local-core installation, Windows/Linux launch commands and direct Python alternatives, first-run initialization/documentation behavior, agent/profile setup, folder purposes, the basic Clarify -> Analyze -> approve -> Implement workflow, direct implementation, the independent question lane, and short troubleshooting/help links. Keep it concise enough to use as a quick start.

The required `.aih/USER_GUIDE.md` supplies detailed operation: phase boundaries, iterative analysis, questionnaires, plan approval and direct implementation, sequential tasks, strict test completion, documentation increments, defect disposition, questions versus changes, profiles/skills/human instructions, reverse engineering, initialization and maintenance status, logs/results, cancellation versus closure, recovery, history/ledger, upgrades, and limitations. Include realistic walkthroughs and a command reference grounded in the shared command catalog. Define stable section anchors for contextual help.

The portal Help page and menu help use this same maintained guide and command metadata. Support navigation/search and local reading without an agent run; help remains accessible when product initialization or authentication is incomplete. Render safely, check links/anchors against the installed version, and update help through explicit core maintenance/upgrades. Do not duplicate user help into behavioral prompts or load the entire human guide into every agent run.

### CLI and maintenance operations

Provide one discoverable Python CLI, usable from the product root as `python .aih/engine/cli.py <command>`. Document the equivalent Python launcher usage on Windows and provide `--help` for every command, including the distinction between Clarify (what and why), repeatable Analyze (how, including plan generation), and Implement (execute the authorized plan). Implement the named operations below; select and document exact arguments consistently.

- Install a pinned core from a local directory, without requiring a release URL or Git.
- Initialize product information idempotently through Python helpers; portal first startup invokes initialization and documentation baselining automatically when product state is absent.
- Inventory the product and perform initial or incremental `reverse-engineer` operations, with status, cancellation, and checkpointed resumption.
- Expose the deterministic operation/help catalog and typed helper interfaces used by both agents and portal.
- Validate structure, schemas, state, documentation, skill bundles, and core integrity.
- Discover/list/validate skills from compact metadata and explicitly enable or disable supported skills by stable ID. Return machine-readable catalog/status results and readable summaries without loading instruction bodies into the response. Generate/reconcile the installed machine-readable and human-readable catalogs only through installation or explicit core maintenance.
- Diagnose profiles and CLI compatibility/authentication.
- Open the shared interactive Python menu, directly or through the optional Windows/Linux launchers.
- Start the portal with port and no-browser options.
- Display the shared local help and command reference without starting agent work.
- Clarify, analyze, approve, implement, implement directly, resume, stop execution, and close a request with an explicit outcome. Use `analyze` for every analysis iteration and automatic plan generation; do not require or expose a standalone `plan` command.
- Ask a read-only question.
- Prepare manual handoff and reconcile returned evidence.
- Upgrade the core and perform explicit required state migrations.

Installation and repeated initialization preserve existing files. Templates become product-owned after initialization. Do not silently merge incompatible schemas or overwrite human content.

Provide a short host-agent integration snippet pointing to `.aih/run.md`. Preserve existing agent instruction files; do not replace their content. Direct invocation must also work without adding an integration file.

Upgrades validate the incoming core and its version, detect unexpected installed-core modifications, preserve all product content, identify migrations, and support recoverable replacement. Update bundled skill resources only through explicit core maintenance. Do not invent a release URL or publish artifacts externally.

Document optional Git tracking and ignore guidance separately. Enabling Git support must not automatically authorize commit, push, PR creation, integration, deployment, or destructive operations.

## 18. Tests and acceptance evidence

Use meaningful automated tests for Python behavior and contracts. Use temporary plain product directories without Git as the baseline. Do not substitute mocked agent behavior for a claim that a real agent followed instructions.

Demonstrate:

1. Installation and repeat initialization preserve content; core upgrades preserve product state and report migrations/conflicts.
2. All framework behavior, helpers, adapters, workers, and backend code are Python. The only non-Python harness scripts are the two optional menu launch wrappers with no framework business logic; direct Python operation remains complete. No database or default Git dependency exists.
3. Root organization is valid, immediate directory names do not overlap, and no product skills directory or executable product-state content is accepted.
4. Ordinary runs leave the core and human-owned custom instructions unchanged.
5. Draft edits never trigger work; explicit actions snapshot revisions; submitted amendments apply safely and invalidate affected approvals/evidence.
6. Only one request can be open, no backlog is created, blockers stop change work, and repeated commands do not launch duplicate processes.
7. Plan approval alone does not implement; ordinary implementation requires current approval. Implement directly records its authorized exception to separate analysis invocation/approval while persisting the required plan before product changes.
8. Stopping execution differs from closing a request; cancelled/rejected closure preserves partial outcomes and permits a subsequent request.
9. Successful closure requires passing required tests, valid verification, documentation, and evidence. Zero exit status alone cannot close a request.
10. One current change response is maintained with history in request records.
11. Independent Q&A works with no request and during active/blocked work, writes answer files, preserves request state, and makes no product changes.
12. Markdown questionnaires round-trip through file and portal editing, including free text, contradictory selections, partial submissions, and revision conflicts.
13. Documentation traversal reaches relevant leaves without loading unrelated content; applicability and provenance remain visible.
14. Grow and reorganize documentation across multiple capacity boundaries; validate eight-child limits, depth difference at most one, stable IDs, unique parents, reachability, cross-links, and preserved content.
15. Interrupted documentation transactions recover safely; external edits conflict or serialize without data loss.
16. Documentation drift and verification invalidation detect relevant non-Git file changes without self-invalidating on bookkeeping.
17. Skill discovery exposes metadata without bodies and detects new, disabled, malformed, duplicate, and incompatible skills without changing `run.md`. Validate all eight required initial packages, the seven enabled defaults, the disabled optional Git default, matching YAML/README catalogs, schema validity, resource/version fingerprints, and actionable stale-catalog diagnostics. Ordinary discovery, portal listing, and enablement leave the core catalogs unchanged; explicit maintenance regenerates them deterministically. CLI and portal show consistent installed/enabled/available states, and enablement alone cannot authorize work.
18. Copy each of the eight delivered skill directories outside AIH and validate its declared input/output contract, usage example, resources, and helpers in clean fixtures without an installed AIH engine or fixed product-state path, supplying only declared dependencies. Use a separate repository fixture for `git-workflow`, including its declared operation-tool dependencies where needed. Detect altered bundled conventions. Claim behavioral portability only if an agent actually exercises the skill; distinguish package/helper checks from observed agent behavior.
19. Multiple profiles coexist; default, per-run, and capability assignments follow documented precedence and controlled checkpoints.
20. A controlled fake CLI tests streaming, Unicode and special-character arguments, spaces in paths, authentication/version errors, malformed events, nonzero exits, timeouts, cancellation, child processes, and resumption limitations.
21. Adapter selection supports a product directory without Git. Missing CLIs, invalid settings, unsupported versions, and unavailable authentication produce actionable errors without silent fallback.
22. Manual handoff is functional, accurately labeled, and cannot falsely mark work as executed or verified.
23. Atomic writes, revision conflicts, transaction recovery, stale-lock handling, and duplicate-action reconciliation work under simulated interruptions/concurrency.
24. Portal browser/no-browser startup, port conflicts, shutdown, primary workflow, separate Q&A, safe Markdown, origin protections, and file-boundary checks are exercised.
25. Product content cannot become arbitrary commands, dynamic imports, privileged configuration, or executable portal content. Seeded credentials are redacted from persisted records and displayed output.
26. Clarification artifacts and questionnaires capture what and why, scope, constraints, and observable acceptance criteria without selecting an implementation. Preserve explicit user technical constraints and distinguish them from observed existing technology. Exercise read-only investigation, Analysis-owned design choices, and a requirement gap discovered during Analysis that returns to clarification. Test structural/state contracts automatically; claim the semantic phase boundary was followed only when an actual agent exercised it.
27. Repeated Analyze invocations handle initial analysis, submitted answers, additional directions, unchanged inputs, and plan generation/regeneration without a separate Plan command or automatic implementation. Preserve valid completed-task history and invalidate affected approvals/evidence.
28. The interpretation remains the single current request definition, and the questions catalog points to authoritative submitted answers without creating another editable answer store. Validate required analysis records, optional supporting files, sequential task order, affected paths, and requirements-to-task/test traceability.
29. Normal and direct implementation both persist plans with mandatory test and documentation tasks and execute tasks sequentially. No shortcut omits logs, results, tests, documentation, or user selection of unrelated defects.
30. Run retained regression tests from earlier requests as part of the complete maintained suite. Repair authorized failures and rerun the suite; test suppression or unexecuted required tests cannot produce successful completion.
31. Unrelated defects require user scope disposition, unfixed established defects appear in current known-defect documentation, and a deferred defect failing a required test blocks completion without exception. Recording the blocker must not launch unauthorized repairs or another request.
32. Every request has a documentation increment with planned/applied/verified distinctions or a justified no-impact result. Reconcile it against actual changes, evidence, and current documentation before closure.
33. Every implementation attempt has durable incremental logs and a readable results summary. Simulate crashes between action intent and result, recover an explicitly reconstructed summary, retain uncertain outcomes, and prevent blind duplicate execution.
34. Closure moves records to separate historical folders, preserving IDs, links, outcomes, and summaries. Normal execution reads current documentation and the active request; historical evidence is fetched on demand through its catalog.
35. First portal startup without product state initializes files, inventories an existing product, and starts configured-agent documentation generation once. Refresh/restart/concurrent-start scenarios do not duplicate workers, operation IDs, or writes.
36. Interrupted bootstrap resumes without overwriting human content. Invalid existing state is reported rather than reset. Missing profile, incompatible CLI, unavailable authentication, or permission limitations leave semantic work visibly pending with actionable guidance and no silent fallback.
37. Initial and incremental reverse engineering preserve implementation/source/test/instruction fingerprints while writing evidence-based documentation. Extracted facts, inferred requirements, unknowns, generated content, and actually verified behavior remain distinguishable.
38. Bootstrap and standalone maintenance keep audit/checkpoint records without a synthetic request, extra product root, database, or Git. Maintenance respects open/blocked requests and single-writer ownership; active-request maintenance uses the request's authorization and documentation increment.
39. Inventory, parsing, validation, state updates, test execution/result capture, catalog maintenance, and archival route through tested deterministic helpers. Check equivalent bundled helpers for standalone skills. Test structural/helper behavior separately from actual agent compliance with the mandatory-use rule.
40. Unchanged input sets reuse valid extraction/summaries and avoid unnecessary semantic generation. Source, instruction, extractor, or schema/core changes invalidate affected reuse. Incremental runs select relevant documents without dropping required coverage or full regression tests.
41. Compact outputs retain evidence references and label omitted detail; full available sanitized evidence remains inspectable. Adapter-reported token usage is recorded accurately, and missing usage remains unavailable rather than fabricated as zero. Distinguish actual token measurements from proxy evidence.
42. Windows/Linux launch wrappers invoke the shared Python menu without duplicating logic; direct Python invocation also works. Exercise root resolution from another working directory, paths with spaces/special characters, missing runtime diagnostics, repeated launch deduplication, and menu exit/shutdown behavior. Report which OS launcher paths were actually exercised rather than inferring cross-platform success.
43. README quick-start commands, USER_GUIDE command references, menu help, portal help, and contextual section links match the implemented catalog and installed version. Help is accessible before initialization/authentication and does not invoke an agent or modify the core.
44. Exercise all eight portal pages and six Current request tabs with meaningful workflow states, inspecting the rendered interface. Verify explicit draft/submission differences, repeated Analyze and generated plan approval, direct-implementation explanation, defect scope selection, revision conflicts, profile effective boundaries, and distinct stop/closure actions.
45. Portal next-action/disabled-action explanations match validated state. Failed required tests cannot be accepted as a completion exception; historical browsing does not reopen/queue work, and independent Q&A remains available during blocked change work. Confirm log/result views distinguish process status from task outcomes and bootstrap documentation from product verification.

Perform a real Codex CLI smoke test if installed, authenticated, and permitted, using an isolated fixture. Otherwise report the integration as not live-tested and explain the missing prerequisite. Distinguish credential discovery from actual successful agent execution.

Exercise the rendered portal and inspect its primary screens. Distinguish automated tests, real agent execution, browser walkthroughs, and untested platform claims.

Create a small synthetic product fixture for an end-to-end demonstration: clarify a change, repeat Analyze through questions/answers and amendments until a plan is generated, approve it, execute its tasks sequentially, pass the full required suite, apply the documentation increment, and archive the completed request. Also demonstrate direct implementation with an internally generated plan, blocked-work Q&A, user triage of unrelated defects, a deferred defect blocking completion through a failed required test, incremental implementation records with interrupted recovery, historical catalog lookup, and cancelled closure. Include a separate existing-product fixture for automatic first-portal initialization, reverse engineering, profile-unavailable recovery, and incremental documentation refresh. Label these fixtures as test examples, not user product requirements.

## 19. Delivery

Deliver the working core, conventions/templates, all eight complete standalone skill packages, `.aih/skills/catalog.yaml`, `.aih/skills/README.md`, the portal Skills catalog, Python CLI and shared menu, optional Windows/Linux launchers, the complete portal, tests, demonstration fixtures, `.aih/README.md`, and `.aih/USER_GUIDE.md` with shared menu/portal help.

Document launcher/menu and direct-Python startup, the portal pages/tabs and contextual help, installation and automatic first-run baselining, initial/incremental reverse engineering and system-operation recovery, mandatory deterministic-helper use, runtime token-efficiency and available usage reporting, supported Python/dependency versions, Windows/Linux operation, agent authentication and profile configuration, file-based and portal workflows, requirements clarification versus iterative Analysis and automatic plan generation, analysis-file ownership, sequential implementation, questions versus change requests, plan approval and direct implementation, full regression testing and defect disposition, documentation increments, implementation logs/results, cancellation/closure and historical catalogs, resumption, the initial skill roster and responsibility boundaries, catalog generation/discovery and diagnostics, skill enablement versus authorization, standalone skill usage/portability, custom-instruction ownership, documentation maintenance/rebalancing, state conflicts/recovery, upgrades/migrations, optional Git, retention, and known limitations.

Provide a traceability summary connecting major requirements to implementation and actual validation evidence. Report failures and missing checks explicitly. Do not claim the framework is fully verified merely because its unit tests pass.

Finish with a concise report stating what was built, exact installation/startup and first-use commands, what was actually tested, whether a real Codex run occurred, tested platforms, and remaining limitations. Do not replace requested functionality with unspecified future work or silently reduce scope.
