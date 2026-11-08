# BL-0011 — Business analyst clarification and requirements readiness

| Field | Value |
| --- | --- |
| ID | BL-0011 |
| Status | pending |
| Created | 2026-11-08T02:58:43Z |
| Updated | 2026-11-08T02:58:43Z |
| Closed | — |
| Activities | 35c72900-30fe-4e9b-b487-aba3ee4304b2 (story capture) |
| Source | User request and supplied clarification ideas, 2026-11-08; adapted to HAI |

## What

As a person submitting a backlog item or change request to HAI, I want the
`business-analyst` agent to turn incomplete intent into precise, reviewable
requirements through informed, durably recorded clarification, so that the host
coordinator and downstream delivery roles can proceed without inventing decisions
that belong to me.

Enrich the existing optional Business-analyst package with a complete clarification
workflow: acquire relevant context, identify consequential gaps, ask attributable
questions, preserve answers and revisions, assess requirements readiness, and
return a detailed proposed Activity input for human review. This extends the
existing role rather than creating a second analyst or reopening BL-0008.

The deliverables are the agent's shared rules and procedures, its owned dialogue
and readiness conventions, portable resource/configuration contracts where
needed, handoff instructions, and evidence that these parts work together.
Requirements below describe proposed future behavior; capturing this story does
not implement it or approve any particular technical design.

## Why

HAI already has a Business-analyst role, but its general instructions do not define
the detailed context selection, persistent dialogue, revision handling or
requirements-quality gate described here. Missing these contracts can lead to
repeated questions, lost answers, assumed approval and incomplete input for later
work. A consistent clarification process keeps human decisions attributable,
supports resumption, and gives users and reviewers the same evidence of readiness.
This is an enhancement to an existing capability; no release priority or deadline
has been assigned.

## Constraints and Assumptions

- Follow HAI instruction precedence, the six-section agent definition format,
  procedure contracts, reference notation and agent-owned configuration rules.
  Shared rules, ordered procedures and reusable conventions retain their separate
  responsibilities.
- Work under a validated, compatible active Activity and its stable UUID. The
  Business analyst returns proposed canonical record content to the host
  coordinator; runtime remains the writer of Activity records, state, chat,
  chronicles, checkpoints and archives. The analyst does not orchestrate agents.
- Keep durable specifications with Specification-manager, backlog edits with the
  authorized backlog owner, and technical design, implementation and QA with their
  existing roles. Clarification does not enable a disabled optional capability.
- Define resource locations, dialogue identity allocation, applicable conventions,
  file capabilities, diagnostics and lifecycle ownership in HAI terms. Use the
  agent-owned contract for genuine configurable values; preserve settings owned
  by others. Do not introduce retired request-store state or a second lifecycle.
- Treat product context as authorized sources supplied for the assignment,
  including enabled specifications when available. Do not require a monolithic
  product file, a `## Request` section, or an optional specification installation
  merely because an older workflow used one.
- Assume the host can persist clarification artifacts through an authorized
  supported operation. An absent capability is a reported dependency, never
  permission for direct analyst writes to runtime-owned resources. Identify any
  required core extension explicitly in the implementation plan and authority.
- Changes to golden source packages, installed copies and registrations are
  separate HAI operations. Updating source does not update an installed snapshot;
  report which copies and registrations were actually validated or changed.
- Preserve unrelated work. Use verified absolute Python 3.11+ with `-B` for any
  supplied Python helpers; avoid dependency installation and generated caches in
  protected framework/package locations.

## Out of Scope

Technical architecture, implementation plans, product code and product QA as
clarification outputs; automatic acceptance or execution of a proposed input;
automatic backlog rewriting; specification mutation; installing or registering
agents merely to clarify a request; changing central recording settings; replacing
core chronicles with a question ledger; and automatic Activity closure or archival.

## Acceptance Criteria

### AC1 — Acquire relevant context predictably

- [ ] Read the current human request or selected backlog item, validated Activity
  context, applicable workspace instructions and conventions, relevant product
  knowledge, and existing clarification records before identifying new questions.
  Reconcile those records with the live conversation, preserving settled decisions
  and recognizing already-recorded events after a restart.
- [ ] An absent or empty question ledger means no recorded questions. Do not create
  an empty ledger; arrange its first durable creation when the first actual
  question is ready, even if no refined Activity-input proposal exists yet.
- [ ] Read additional authorized local context when necessary, then reassess the
  request. When available files are sufficient, state that explicitly. When
  necessary context is unavailable, name the dependency rather than assuming it.
- [ ] When a supplied product-context document has a `## References` registry,
  support ordered level-three entries and parse `Location`, `Summary`,
  `Convention`, `Prompt`, `Read` and `Update` independently. This is an optional
  supplementary-context format, not a replacement for HAI specification storage.
- [ ] Interpret `Read` case-insensitively: `no` skips the entry; `yes` permits
  semantic relevance evaluation against the clarification objective. Report and
  skip every other value without guessing or rewriting it. Provide the exact
  diagnostic command documented by the implemented HAI registry contract; include
  a read-only diagnostic helper if no suitable one exists, and do not advertise a
  nonexistent legacy command as an available HAI tool.
- [ ] Load only eligible, relevant entries, in their listed order. Resolve
  `Location`, `Convention` and `Prompt` relative to the validated workspace root.
  Reject and report escaping paths and entries into closed Activity/archive
  stores, version-control metadata, virtual environments, dependency caches or
  generated caches. Historical material supplied explicitly for the assignment
  remains subject to its own authorization rather than registry discovery.
- [ ] Check each registered artifact's existence independently. A missing location
  prevents that extension's content from loading; a missing convention or prompt
  does not prevent loading an otherwise available location. For each missing
  artifact emit `WARNING: Context registry resource unavailable: <path>. Proceeding
  without that resource.` Continue to later entries, subject to any independently
  mandatory dependency.
- [ ] Read each qualifying location completely and attribute its entry title and
  path when using it. Keep the supplied primary product context authoritative.
  A prompt reference is catalogue information: check existence, never read or
  execute it. `Update` never triggers action. Context acquisition does not modify
  registry/resources, access the network, install dependencies or execute scripts;
  diagnostics are supplied for a separate authorized check.

### AC2 — Find consequential gaps without over-questioning

- [ ] Compare the request with relevant context, conventions and the latest
  effective decisions. Examine intent, expected outcomes, users, motivation,
  success measures, terminology, workflows, behavior and business rules.
- [ ] Examine scope, priorities, exclusions, acceptance and completion criteria,
  technical restrictions, dependencies, integrations and external resources;
  inputs, outputs, formats, origins, schemas and validation; stakeholder roles,
  permissions, security, privacy and applicable compliance obligations.
- [ ] Consider relevant edge cases, errors, failures, fallback and recovery;
  performance, scale, availability, accessibility, language/region and
  compatibility; migration, deployment, configuration, observability, rollback,
  testing and verification expectations.
- [ ] Detect contradictions within the request and conflicts with existing
  requirements, specifications, architecture and conventions. Surface unstated
  assumptions, constraints, tradeoffs and decisions requiring human judgment.
- [ ] Treat a gap as a decision blocker only if reliable context cannot resolve it
  and it materially affects scope, feasibility, correctness or acceptance. Do not
  ask questions already answered or about choices safely left to implementation.
  The diagnostic inventory does not make every possible feature or quality
  attribute a deliverable. Summarize each remaining blocker in one sentence
  immediately before its question; proceed toward readiness/proposal when none
  remains.

### AC3 — Ask identifiable questions with verified durable records

- [ ] Define one canonical question-block format with a unique stable ID, full
  question, implementation-impact explanation, every offered option, visibly
  marked recommendation when present, free-text alternative and status. Define
  monotonically increasing question IDs, per-question response numbering and
  revision links; never recycle an ID or attach it to another question. Specify
  the sequence scope and prefix/default, such as `Q001`, in the HAI contract.
- [ ] Collect all currently necessary questions into one batch and wait for the
  user's response before deciding on another batch or advancing dependent work.
  Respect host interface limits without losing questions or issuing duplicate
  IDs; retain one recorded logical batch if display needs multiple parts.
- [ ] Before displaying new questions, have the host persist the exact question
  blocks in the Activity's clarification artifacts and read them back. Persist
  IDs, wording, impact, options, recommendation markers and free-text alternative;
  all new choices are unchecked, free-text placeholders are `___`, and status is
  unanswered. Allocation or a proposed write is not persistence evidence.
- [ ] Display the verified saved content with a compact copyable answer form
  preserving IDs and choices, for example `Q001: A [ ], B [ ], Other: ___`.
  Showing an existing unanswered question again reuses its ID/content without
  appending another question event. Preserve the ledger throughout clarification,
  resumption and later Activity work.

### AC4 — Preserve answers and decision changes accurately

- [ ] Wait for an actual human answer. A recommendation, preselected interface
  choice, silence or blank field is not an answer or approval. Before applying an
  answer or advancing dependent work, have the host append its response event,
  link it to the exact question ID, and verify it by reading the saved record.
- [ ] Preserve choices and free-text explanations verbatim, associating every
  multipart answer with the correct question part. Append in reception order with
  per-question response sequence numbers; resumption recognizes previously saved
  events rather than duplicating them.
- [ ] If mapping is ambiguous, preserve the raw response as unresolved, ask the
  user to establish its mapping, and do not apply an uncertain interpretation.
  Changed decisions append numbered revisions identifying the superseded response;
  retain all previous responses and make the latest effective decision explicit.
- [ ] After verified persistence, reassess blockers and repeat clarification only
  when necessary. On ledger read/write/readback failure, report the exact path and
  underlying error and stop the dependent question display, answer application or
  proposal. Report unavailable persistence capability in the same way; continue
  independent permitted work without claiming the failed operation succeeded.
- [ ] The analyst never clears, resets, deletes or archives dialogue records.
  Activity input preparation, analysis, revisions and retries preserve them.
  Only authorized core Activity archival moves them with the Activity log and
  supporting artifacts. The question ledger is an attributable decision record,
  separate from core source-backed chronicles and their coverage requirements.

### AC5 — Apply an explicit requirements-readiness gate

- [ ] Publish a readiness convention usable by both AI and human reviewers. Give
  its eight categories and 28 mandatory items stable identifiers and evaluable
  Markdown checkboxes, each explaining what evidence satisfies it, using AC6.
- [ ] Apply the gate before downstream technical analysis or implementation
  planning for a new request, and reapply it when scope, goals or acceptance
  conditions change. Exempt only internal framework upkeep with no user-visible
  behavior change, including pure refactoring, and urgent clear defects whose
  repair is one reversible change. Record the applicable exemption and reason;
  exemptions do not grant permissions or remove other clarification safeguards.
- [ ] Pass only when every mandatory item is satisfied and no undocumented
  critical gap remains. A reasonable documented assumption or explicit deferral
  within the iteration may resolve a gap only if it actually resolves the item's
  uncertainty; record the consequences if false. Never fabricate an answer or
  override a decision requiring explicit human judgment through an assumption.
- [ ] Fail if a mandatory item remains unsatisfied. Identify failed items and
  unresolved decisions for further clarification; the host does not advance that
  request to downstream technical analysis, planning or implementation under a
  failed gate. Record actual results rather than a plausible-sounding assessment.

### AC6 — Preserve all eight readiness dimensions and 28 checks

Each check below is mandatory for a non-exempt request; its text describes the
evidence needed. Preserve these initial identifiers when publishing the convention.

#### R1 — Intent

- [ ] **R1.1 Self-contained objective:** One or two sentences explain the goal to a
  new colleague without specialist background or further explanation.
- [ ] **R1.2 Coherent outcome:** One atomic intent is stated; multiple tasks serve
  that outcome rather than combining independent requests.
- [ ] **R1.3 Observable change:** The affected party's outcome or behavior is
  described, rather than only prescribing an internal solution.
- [ ] **R1.4 Motivating need:** The goal connects to a stated business need, user
  problem or product objective, including reliable existing product context.

#### R2 — People

- [ ] **R2.1 Identified participant:** At least one user/stakeholder role directly
  using or affected by the change is named.
- [ ] **R2.2 Participant difficulty:** That participant's current problem or unmet
  objective is explained.
- [ ] **R2.3 Other affected parties:** Additional affected parties are identified,
  or their absence is explicitly established.

#### R3 — Value

- [ ] **R3.1 Concrete benefit:** At least one user, business or product benefit
  justifies the effort and opportunity cost.
- [ ] **R3.2 Priority rationale:** Priority, urgency, dependency or another reason
  for addressing the request now is recorded rather than invented.
- [ ] **R3.3 Existing capability considered:** A real gap is established, or the
  request explains why an available equivalent needs modification.

#### R4 — Delivery boundaries

- [ ] **R4.1 Named deliverables:** Bounded outputs or changes identify affected or
  new files, components or behaviors as appropriate.
- [ ] **R4.2 Iteration-sized work:** The request fits one reasonable implementation
  iteration; independent subrequests are identified for decomposition if needed.
- [ ] **R4.3 Compatible scope:** No deliverables demand mutually exclusive results.
- [ ] **R4.4 Outcome-based scope:** Scope says what must exist or happen, rather
  than dictating how internal code must implement it.

#### R5 — Exclusions

- [ ] **R5.1 Explicit exclusion:** At least one concern is expressly out of scope.
- [ ] **R5.2 Precise exclusions:** Exclusions identify concrete features, file
  types, workflows or components rather than undefined broad labels.

#### R6 — Limits and premises

- [ ] **R6.1 Technical limits:** Known restrictions, such as supported versions,
  allowed formats and available tools, are listed.
- [ ] **R6.2 Organizational limits:** Applicable policies, naming rules, process
  obligations and compliance constraints are recorded.
- [ ] **R6.3 Consequential assumptions:** Premises affecting scope, approach or
  acceptance are documented with consequences/risks if false.
- [ ] **R6.4 Separate constraints:** A dedicated section keeps constraints distinct
  from functional deliverables.

#### R7 — Evidence of success

- [ ] **R7.1 Completion test:** At least one acceptance condition is defined.
- [ ] **R7.2 Objective verification:** Each condition has a deterministic pass/fail
  check using a named artifact, behavior, count or observable state.
- [ ] **R7.3 Feasible acceptance:** Conditions are achievable within the stated
  scope and constraints.
- [ ] **R7.4 Specific language:** Undefined quality claims are replaced by
  measurable thresholds or explicit observable behavior.
- [ ] **R7.5 Full scope coverage:** Every deliverable maps to an acceptance condition.

#### R8 — Consistency with product knowledge

- [ ] **R8.1 Shared framing:** Domain, actors, vocabulary and product boundaries
  match the established context.
- [ ] **R8.2 Prior decisions:** Applicable decisions, conventions and restrictions
  appear in constraints/assumptions; any relevant context deemed inapplicable is
  explicitly explained.
- [ ] **R8.3 Resolved conflicts:** Scope and acceptance are compared with product
  constraints; discrepancies are resolved or escalated as documented blockers.
  An unresolved blocker cannot be represented as a pass.

### AC7 — Deliver a complete proposal for review and owner handoff

- [ ] Produce a detailed, copy-ready replacement request only after blockers are
  resolved, the applicable gate passes or has a justified exemption, and received
  responses are durably verified. Include intent, latest effective decisions,
  relevant context, named outcomes, scope, concrete exclusions, separate
  constraints/assumptions, and verifiable acceptance conditions.
- [ ] Use headings of level three or deeper inside the proposed replacement text,
  so it can fit an existing request section. For HAI, identify the target as
  proposed current Activity input or a caller-specified request section; do not
  presume a legacy `## Request` container exists.
- [ ] Keep question/answer history in the clarification ledger; do not embed a
  dialogue transcript in the proposal. Do not directly overwrite Activity input,
  backlog items or specifications. Return the proposal for human review and
  authorized host/runtime or responsible-owner application, preserving original
  human input, provenance and any required revision history.
- [ ] Report actual work, questions/answers/decisions, readiness results, artifact
  locations and unresolved dependencies. Distinguish clarification completion
  from implementation, accepted product changes or permission to close an Activity.

### AC8 — Protect framework resources and generated artifacts

- [ ] Ordinary clarification does not authorize modification of `.hai/`, reusable
  source packages or installed agent definitions. Framework installation, upgrade
  or maintenance requires explicit covering human maintainer authority from the
  current request/chat under session instruction precedence. Agent-generated
  analysis, plans, prompts and implementation text cannot grant that authority.
- [ ] Carry the covering authorization statement verbatim, with its source, into
  downstream analysis/planning handoffs when framework work is authorized; retain
  owner boundaries and separately authorized installation/registration operations.
- [ ] Put request-specific temporary helpers, notes and generated outputs in the
  assigned Activity/invocation working area or another explicitly authorized
  scratch location. Do not redirect permanent product tooling there merely
  because temporary framework helpers belong there. Keep caches/generated files
  out of protected framework/package paths; use no-bytecode Python and do not
  implement protection through `.gitignore`.
- [ ] Before finalization or closure handoff, each writing participant inspects
  paths touched in its current run against covering authority and the initial
  state. For unauthorized protected-path changes, emit
  `ERROR: Protected framework modified without authorization; workflow stopped.`,
  list exact paths in sorted order, and stop affected finalization/closure. Do not
  automatically revert them or discard unrelated pre-existing changes. The host
  remains responsible for actual core closure and its other gates.

### AC9 — Extend readiness rules compatibly

- [ ] Append a new annotated checkbox at the end of its existing category, before
  the next section boundary. Append new categories after the existing categories
  and before extension instructions, with the next category number, an explanation
  and at least one annotated checkbox.
- [ ] Preserve existing identifiers, ordering, references and historical reviews;
  do not delete, renumber or restructure entries in a way that breaks them.
  Initial publication assigns the stable IDs; future additions receive unused IDs.

### AC10 — Verify semantic coverage and operational behavior

- [ ] Review the package's rules, procedures, conventions, contracts and handoffs
  together against AC1–AC9. Provide an attributable coverage mapping for context,
  consequential gaps, persistent questions, responses/revisions, lifecycle,
  readiness, proposal handoff, resource protection and compatible evolution.
  Summary groups do not replace individual requirements or the 28 readiness checks.
- [ ] Demonstrate informed clarification with sufficient files and with missing
  context; ordered relevant registry reads; `YES`/`No` and invalid flags; invalid
  paths; independently missing location/convention/prompt artifacts; and no
  qualifying extensions. Verify prompts/update metadata remain inert and context
  loading has no unauthorized writes, network access or script execution.
- [ ] Demonstrate first-question persistence/readback, batch display, unanswered
  reuse, exact answers, multipart answers, ambiguous mapping, revisions and
  restart without duplicate events. Inject unavailable capability and read/write/
  verification failures to show dependent work stops and partial evidence remains.
- [ ] Demonstrate gate pass/fail, assumption limits, both narrow exemptions and
  reassessment after scope changes; verify all 28 checks and compatible extensions.
  Demonstrate a complete proposal with only deeper headings and no direct request
  overwrite, preserved ledger through later work and authorized Activity archival,
  and protection checks that preserve pre-existing changes.
- [ ] Use the appropriate HAI package/configuration validators and report actual
  host/tool capabilities, checked source versus installed copies, exercised
  scenarios and unrun checks. Fixture success alone does not prove a real host
  persisted or archived an Activity, or that chronicles have source coverage.

## History

- 2026-11-08T02:58:43Z — Created as the next pending backlog story from the user's request
  and supplied clarification ideas. Paraphrased into HAI's existing optional
  Business-analyst role, Activity/runtime ownership and package model. Requirements
  are proposed for future implementation; no implementation or acceptance claimed.
