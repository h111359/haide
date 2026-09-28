# Contents

- [1. Delivery scope and operating environment](#1-delivery-scope-and-operating-environment)
- [2. Product workspace and access](#2-product-workspace-and-access)
  - [2.1. Membership and filesystem boundaries](#21-membership-and-filesystem-boundaries)
  - [2.2. External tools and permitted effects](#22-external-tools-and-permitted-effects)
  - [2.3. Human administration and folder changes](#23-human-administration-and-folder-changes)
  - [2.4. Reviewing prior work and documentation after workspace changes](#24-reviewing-prior-work-and-documentation-after-workspace-changes)
  - [2.5. Workspace settings and validation](#25-workspace-settings-and-validation)
- [3. Human instructions and framework maintenance](#3-human-instructions-and-framework-maintenance)
  - [3.1. Instruction ownership and authority](#31-instruction-ownership-and-authority)
  - [3.2. Core protection and maintenance gates](#32-core-protection-and-maintenance-gates)
- [4. Request ownership and submission](#4-request-ownership-and-submission)
  - [4.1. Single request and operational availability](#41-single-request-and-operational-availability)
  - [4.2. Drafts, submissions, and changed input](#42-drafts-submissions-and-changed-input)
  - [4.3. Request records and historical access](#43-request-records-and-historical-access)
- [5. Clarification and amendments](#5-clarification-and-amendments)
  - [5.1. Clarification scope and phase boundaries](#51-clarification-scope-and-phase-boundaries)
  - [5.2. Iterative clarification and reconciliation](#52-iterative-clarification-and-reconciliation)
  - [5.3. Amendment editing, capture, and history](#53-amendment-editing-capture-and-history)
- [6. Questionnaires and requestor exchanges](#6-questionnaires-and-requestor-exchanges)
  - [6.1. Questions, respondents, and authoritative answers](#61-questions-respondents-and-authoritative-answers)
  - [6.2. Plain-text form export and explanation](#62-plain-text-form-export-and-explanation)
  - [6.3. Intake, matching, and answer review](#63-intake-matching-and-answer-review)
  - [6.4. Reviewed submission and recoverable launch](#64-reviewed-submission-and-recoverable-launch)
  - [6.5. Attribution, authority, and file-only access](#65-attribution-authority-and-file-only-access)
- [7. Analysis and implementation](#7-analysis-and-implementation)
  - [7.1. Design assessment and plan regeneration](#71-design-assessment-and-plan-regeneration)
  - [7.2. Plan tasks and sequential execution](#72-plan-tasks-and-sequential-execution)
  - [7.3. Approval, direct implementation, and scope](#73-approval-direct-implementation-and-scope)
  - [7.4. Blockers, Stop, and resumption](#74-blockers-stop-and-resumption)
  - [7.5. Recovery and evidence freshness](#75-recovery-and-evidence-freshness)
- [8. Testing and defect disposition](#8-testing-and-defect-disposition)
  - [8.1. Required suites and execution conditions](#81-required-suites-and-execution-conditions)
  - [8.2. Repair limits and authorized continuation](#82-repair-limits-and-authorized-continuation)
  - [8.3. Unrelated defects and retained obligations](#83-unrelated-defects-and-retained-obligations)
- [9. Request outcomes](#9-request-outcomes)
  - [9.1. Successful completion and explicit closure](#91-successful-completion-and-explicit-closure)
  - [9.2. Cancellation, rejection, and retained state](#92-cancellation-rejection-and-retained-state)
- [10. Independent product questions](#10-independent-product-questions)
- [11. Product documentation](#11-product-documentation)
  - [11.1. Current knowledge, provenance, and change tracking](#111-current-knowledge-provenance-and-change-tracking)
  - [11.2. Reconstruction coverage and evidential limits](#112-reconstruction-coverage-and-evidential-limits)
  - [11.3. Initial and incremental reverse engineering](#113-initial-and-incremental-reverse-engineering)
  - [11.4. Baseline gates and maintenance ownership](#114-baseline-gates-and-maintenance-ownership)
  - [11.5. Navigation, document size, and reorganization](#115-navigation-document-size-and-reorganization)
  - [11.6. Applicability and business knowledge](#116-applicability-and-business-knowledge)
  - [11.7. Architecture, data, interfaces, and dependencies](#117-architecture-data-interfaces-and-dependencies)
  - [11.8. Operations, verification, and support knowledge](#118-operations-verification-and-support-knowledge)
  - [11.9. Typed detail and document traceability](#119-typed-detail-and-document-traceability)
  - [11.10. External materials and original attachments](#1110-external-materials-and-original-attachments)
  - [11.11. Request changes against product knowledge](#1111-request-changes-against-product-knowledge)
  - [11.12. Coordinated documentation maintenance](#1112-coordinated-documentation-maintenance)
- [12. Evidence, efficiency, and sensitive information](#12-evidence-efficiency-and-sensitive-information)
  - [12.1. History, compact evidence, and token usage](#121-history-compact-evidence-and-token-usage)
  - [12.2. Intake screening and historical redaction](#122-intake-screening-and-historical-redaction)
  - [12.3. Implementation logs and results](#123-implementation-logs-and-results)
- [13. Standalone skills](#13-standalone-skills)
  - [13.1. Package portability and invocation authority](#131-package-portability-and-invocation-authority)
  - [13.2. Delivered capabilities and their boundaries](#132-delivered-capabilities-and-their-boundaries)
  - [13.3. Discovery, availability, and configuration](#133-discovery-availability-and-configuration)
- [14. Agent profiles and external execution](#14-agent-profiles-and-external-execution)
  - [14.1. Profile selection, diagnostics, and launch boundaries](#141-profile-selection-diagnostics-and-launch-boundaries)
  - [14.2. Manual handoff and release](#142-manual-handoff-and-release)
- [15. Portal experience](#15-portal-experience)
  - [15.1. Local startup and first-use setup](#151-local-startup-and-first-use-setup)
  - [15.2. Pages and product navigation](#152-pages-and-product-navigation)
  - [15.3. Current request tabs](#153-current-request-tabs)
  - [15.4. Action clarity, conflicts, and execution status](#154-action-clarity-conflicts-and-execution-status)
  - [15.5. Browser and content protection](#155-browser-and-content-protection)
- [16. Installation, commands, and user guidance](#16-installation-commands-and-user-guidance)
  - [16.1. Installation, upgrades, and preservation](#161-installation-upgrades-and-preservation)
  - [16.2. Menu, startup, and command discovery](#162-menu-startup-and-command-discovery)
  - [16.3. Quick start and shared help](#163-quick-start-and-shared-help)
- [17. Delivery validation and reporting](#17-delivery-validation-and-reporting)
- [Referenced documents](#referenced-documents)
- [Sources](#sources)

# 1. Delivery scope and operating environment

- [A] 1.1. The AIH delivery MUST implement and verify the complete framework, including infrastructure, instructions, conventions, portable skills, portal, tests, and operating documentation; a proposal, scaffold, reduced first version, or unspecified future work does not satisfy delivery.
  {S1:L8-10}

- [A] 1.2. AIH implementation work MUST resolve routine engineering details without asking the requester to prioritize in-scope features, and ask only about consequential ambiguities unresolved by inspection or the specification.
  {S1:L10}

- [A] 1.3. AIH MUST support product understanding, requirements clarification, planning, authorized implementation, verification, maintained documentation, and file-based resumption after interruption.
  {S1:L16}

- [A] 1.4. AIH MUST support Windows and Linux and distinguish intended platform support from platforms actually tested.
  {S1:L18}

- [A] 1.5. AIH MUST remain fully operable through direct Python invocation without Node, PowerShell, or optional menu wrappers.
  {S1:L39}

- [A] 1.6. Installation, history, diffs, revision checks, verification, and recovery MUST work without Git; Git MUST NOT be required or initialized by default.
  {S1:L43}

- [A] 1.7. Users MUST be able to operate entirely through files and explicit Python commands without chat or the portal.
  {S1:L158}

# 2. Product workspace and access

## 2.1. Membership and filesystem boundaries

- [A] 2.1.1. Each AIH installation MUST support one logical product spanning one or more explicitly configured filesystem folders, including plain directories, separate repositories, and multiple components.
  {S1:L18}

- [A] 2.1.2. AIH MUST default to a single mandatory writable framework home and allow additional explicitly human-selected folders, including siblings or different drives, subject to host permission.
  {S1:L20}

- [A] 2.1.3. All registered folders MUST share one product definition, documentation tree, required test inventory, and execution owner.
  {S1:L45}

- [A] 2.1.4. AIH inspection MUST stay within explicitly registered readable folders; their common ancestor and unregistered neighboring locations do not become workspace members.
  {S1:L22}

- [A] 2.1.5. All managed filesystem mutations MUST remain within registered writable folders and the action's authorized scope, including creates, writes, deletes, moves, permission changes, cleanup, tests, caches, subprocesses, agents, optional Git, and launched browser effects.
  {S1:L22-24}

- [A] 2.1.6. Writable workspace membership MUST NOT itself authorize implementation changes.
  {S1:L22}

- [A] 2.1.7. Registered read-only folders MUST permit inspection without any managed direct or indirect writes, including outputs, caches, cleanup, and writable-alias bypasses.
  {S1:L22-24}

- [A] 2.1.8. AIH MUST reject registrations whose duplicate, overlapping, or aliased roots make ownership or access ambiguous.
  {S1:L24}

- [A] 2.1.9. AIH MUST reject mutations that could reach unregistered/read-only locations or whose containment cannot be established.
  {S1:L24}

- [A] 2.1.10. A discovered content link or dependency MUST NOT register its target or expand authority.
  {S1:L24}

- [A] 2.1.11. Explicit controlled import of supplied external material is OPTIONAL and MUST NOT authorize arbitrary neighboring-file access.
  {S1:L24}

- [A] 2.1.12. Missing or inaccessible registered folders MUST remain visible and MUST NOT silently disappear from required coverage or tests.
  {S1:L26}

## 2.2. External tools and permitted effects

- [A] 2.2.1. AIH MAY use runtimes, libraries, agent executables, and authentication references located outside the registered workspace folders, if the host environment permits access. This permission covers reading or using those resources only. AIH and any tools it invokes MUST NOT write outside the registered writable folders, including when creating caches, logs, or temporary files.
  {S1:L28}

- [A] 2.2.2. If a tool cannot operate within AIH’s required access boundaries, AIH MUST block its use and explain what setup changes are needed. AIH MUST NOT relax those boundaries or copy credentials into tracked product files to make the tool work.
  {S1:L28}

- [A] 2.2.3. An explicitly authorized action on a remote service MUST NOT expand local filesystem-write permissions. Any local writes caused by that action MUST remain within registered writable folders.
  {S1:L28}

- [A] 2.2.4. AIH MUST document its assumptions about file storage and locking, what storage environments have been tested, and any known limitations. It MUST NOT promise reliable recovery on network drives or synchronized folders unless that behavior has been tested.
  {S1:L30}

- [A] 2.2.5. AIH MUST treat stored product state, including temporary data, as data only. It MUST NOT execute that content or import it as code, including any accepted examples or attachments.
  {S1:L110}

- [A] 2.2.6. Enabling optional Git support MUST NOT require all registered workspace folders to belong to the same Git repository. Enabling Git MUST NOT itself grant permission to create commits, push changes, open pull requests, integrate changes, deploy, perform destructive actions, or cause filesystem changes outside registered writable folders.
  {S1:L707}

## 2.3. Human administration and folder changes

- [A] 2.3.1. Only an explicit human administrative action MAY change which folders belong to the workspace or what access is allowed. Agents MUST NOT register folders or expand their own permissions.
  {S1:L120}

- [A] 2.3.2. Agents MAY suggest adding a missing dependency or workspace folder. A suggestion MUST NOT itself add the folder to the workspace or grant permission to access it.
  {S1:L120}

- [A] 2.3.3. Editing the settings for additional workspace folders MUST NOT remove the required framework home, make it read-only, or change its location.
  {S1:L118}

- [A] 2.3.4. AIH MUST allow human workspace changes only when no request is open and no operation is active. Blocked, stopped, and Ready to close requests still count as open. These changes MUST NOT bypass the separate conditions required for framework core maintenance.
  {S1:L122, S3:section "Accepted policy"}

- [A] 2.3.5. Humans MAY change workspace settings by directly editing the configuration file. Agents MUST NOT modify workspace membership or access settings. AIH MUST validate changes before applying them and MUST apply them only when no request is open and no operation is active. External file edits MUST NOT bypass these conditions or silently change execution authority.
  {S1:L120, S3:section "Accepted policy"}

- [A] 2.3.6. Saving workspace configuration MUST NOT start agents or tests, move product files, expand the business scope of the work, or automatically resume implementation.
  {S1:L124}

- [A] 2.3.7. Removing a folder from the workspace MUST NOT delete its files or erase request records, documentation history, evidence, required test obligations, or records of unresolved defects.
  {S1:L128}

- [A] 2.3.8. Once access to a folder is revoked, all later recovery and cleanup MUST respect that revocation. Resuming interrupted work MUST NOT restore removed folder registrations or use outdated paths to write to locations that are no longer authorized.
  {S1:L128}

- [A] 2.3.9. Changing a registered folder's location MUST update the workspace mapping without moving any files. AIH MUST validate the new location, its contents, and the permitted access; matching relative file paths alone MUST NOT be treated as proof that it is the same folder.
  {S1:L128}

## 2.4. Reviewing prior work and documentation after workspace changes

- [A] 2.4.1. AIH MUST use the current validated workspace configuration. Plans, inventories, documentation, test contracts, checkpoints, and evidence MUST identify files by stable folder identity and relative path. Historical request records MUST be preserved, but a separate history of workspace configurations, configuration revision identifiers, and previous folder locations is not required.
  {S1:L26, S3:section "Accepted policy"}

- [A] 2.4.2. When workspace changes are saved, AIH MUST mark affected documentation, documentation baselines, dependencies, and required test coverage for review before the next request can start. AIH MUST record why any evidence it continues to rely on is unaffected. If the impact of a change is unknown, AIH MUST mark that impact as unresolved.
  {S1:L124, S3:section "Accepted policy"}

- [A] 2.4.3. Before the next request starts, AIH MUST inventory new or relocated workspace areas, establish or update their documentation baselines, and review affected dependencies between folders and required test coverage. This review MUST use the current validated folder locations and access permissions.
  {S1:L126, S3:section "Accepted policy"}

- [A] 2.4.4. Work to bring documentation and test coverage into agreement with workspace changes MUST be an explicitly authorized task with a defined scope within setup or documentation maintenance. This work MUST take place when no request is open.
  {S1:L126, S1:L395-397, S3:section "Accepted policy"}

- [A] 2.4.5. Workspace changes MUST preserve existing documentation history. Affected documentation and test coverage MUST remain marked as unresolved until the required review is complete. Saving workspace settings MUST NOT automatically start reverse engineering or other review work, bypass approval requirements, or disregard unrelated blockers.
  {S1:L397, S3:section "Accepted policy"}

## 2.5. Workspace settings and validation

- [A] 2.5.1. Workspace settings MUST show the fixed framework home folder. For each registered folder, they MUST show its stable identifier and name, resolved filesystem path, purpose, read-only or writable access, availability, documentation baseline status, and pending review status. They MUST explain that all registered folders belong to one product and share one request, one execution owner, and centrally stored product state.
  {S1:L631, S3:section "Accepted policy"}

- [A] 2.5.2. Workspace settings MUST offer human Add folder, Edit, Validate access, Remove from workspace, Save changes, and Cancel, preserve stable IDs, validate only selected/configured roots, reject stale/invalid saves, and discard only unsaved forms on Cancel.
  {S1:L633}

- [A] 2.5.3. Workspace validation MUST NOT browse arbitrary ancestors/siblings or write probes to read-only/unregistered candidates; unproven access MUST be reported for later authorized checking.
  {S1:L633}

- [A] 2.5.4. Before saving workspace changes, the UI MUST explain affected documentation and test coverage, dependencies, and unknown impacts. After saving, it MUST show the reviews required before the next request can start, without launching work or hiding retained obligations. Workspace changes MUST be unavailable while a request is open or an operation is active.
  {S1:L635, S3:section "Accepted policy"}

# 3. Human instructions and framework maintenance

## 3.1. Instruction ownership and authority

- [A] 3.1.1. AIH MUST respect host instruction hierarchy, restrictions, permissions, and existing authorization; explicit user directions and human product instructions govern behavior within those limits.
  {S1:L146-148}

- [A] 3.1.2. Behavioral overrides MUST be identifiable and MUST NOT bypass fixed formats, schemas, interfaces, or validation contracts.
  {S1:L148}

- [A] 3.1.3. Custom-instruction creation and editing MUST be restricted to humans; agents MUST NOT create or modify instruction content.
  {S1:L150}

- [A] 3.1.4. Agent suggestions of custom-instruction wording in output files are OPTIONAL and MUST NOT apply themselves as instruction edits.
  {S1:L150}

- [A] 3.1.5. Initialization is permitted to create the custom-instructions directory and explain how humans add instructions; creating instruction content is not permitted. This directory-and-guidance creation is OPTIONAL.
  {S1:L150}

- [A] 3.1.6. Historical requests, imports, logs, comments, attachments, memory, and agent proposals MUST NOT automatically become active instructions or authorize executable settings, skills, wider access, approval, or deployment.
  {S1:L152}

- [A] 3.1.7. Instruction changes MUST retain segment provenance and invalidate only affected assumptions/authorization; still-applicable authorization MUST persist.
  {S1:L154}

## 3.2. Core protection and maintenance gates

- [A] 3.2.1. Ordinary operations MUST leave the installed framework core unchanged, including generated catalogs, bundled resources, logs, caches, and temporary files.
  {S1:L66}

- [A] 3.2.2. Core repair, catalog/resource regeneration, maintenance, and upgrades MUST require no open request and no other execution owner; blocked, paused, and Ready to close requests remain open.
  {S1:L68}

- [A] 3.2.3. A broken helper MUST NOT create an in-request core-repair exception; cancellation/rejection, if needed before repair, MUST preserve the incomplete request and current-state notice.
  {S1:L68}

- [A] 3.2.4. Missing or broken deterministic helpers MUST produce an actionable framework-gap diagnosis without silently bypassing validation or transactions.
  {S1:L80}

- [A] 3.2.5. AIH MUST preserve direct human editing of permitted product files and detect/validate observed edits without claiming control over external filesystem actors.
  {S1:L80}

# 4. Request ownership and submission

## 4.1. Single request and operational availability

- [A] 4.1.1. AIH MUST allow only one open change request and MUST NOT create a backlog, queued future request, or concurrent change-request execution, or silently replace/close/archive the active request to admit another.
  {S1:L45, S1:L219}

- [A] 4.1.2. AIH MUST allow only one operational action across change work, questions, setup, maintenance, tests, diagnostics, and manual handoffs; starting, running, stopping, uncertain termination, and reserved external execution all count as busy.
  {S1:L47-49}

- [A] 4.1.3. While busy, Stop MUST be the only operational control; saves, imports, submissions, approvals, settings changes, closure, questions, and replacement commands MUST be refused without queuing them.
  {S1:L47-49, S1:L166}

- [A] 4.1.4. Passive navigation, help, existing-artifact viewing/download, and status/log observation MUST remain available while busy.
  {S1:L47}

- [A] 4.1.5. The current action MUST be allowed to perform its own already-authorized internal substeps under its existing ownership.
  {S1:L47}

- [A] 4.1.6. A safely stopped or completed action MUST require a new explicit user action for subsequent work; no automatic dispatch follows Stop or completion.
  {S1:L49}

- [A] 4.1.7. An open blocked request with reconciled stopped ownership MUST be treated as idle for permitted drafts and questions without authorizing unrelated change work.
  {S1:L49}

- [A] 4.1.8. Status MUST distinguish workflow phase, request lifecycle, worker state, and task outcome; process success or stoppage MUST NOT imply request completion.
  {S1:L215}

## 4.2. Drafts, submissions, and changed input

- [A] 4.2.1. Externally edited inputs, instructions, or configuration MUST NOT silently change live execution authority; affected evidence and authority MUST be reconciled through the next applicable explicit idle action, with a safe pause when uncertain. Workspace configuration changes MUST additionally wait until no request is open.
  {S1:L49, S1:L130, S1:L154, S3:section "Accepted policy"}

- [A] 4.2.2. Saving inputs, answers, and amendments MUST create drafts only; receiving accepted requestor responses MUST stage imports only, without execution or scope adoption.
  {S1:L160}

- [A] 4.2.3. Explicit idle Clarify, Analyze, Implement, Implement directly, or Resume MUST submit current relevant saved input, reviewed answer drafts, and saved pending amendments, excluding raw/unreviewed uploads.
  {S1:L162}

- [A] 4.2.4. Submission capture MUST preserve preceding submitted versions and newer human edits, and MUST report partial or contradictory questionnaire edits needing correction.
  {S1:L164}

- [A] 4.2.5. Scope changes MUST invalidate affected plan approval, verification, and documentation freshness; cosmetic changes need not invalidate unrelated evidence, with the determination recorded.
  {S1:L168}

- [A] 4.2.6. Before execution, AIH MUST show the relevant saved input, reviewed answers, and pending amendments being submitted; selecting/saving alone MUST NOT apply them.
  {S1:L245}

- [A] 4.2.7. A new request MUST open only by explicit submission after the complete current configured-product documentation baseline passes; idle setup, Q&A, and local drafts may precede this gate.
  {S1:L192}

- [A] 4.2.8. An open request MUST keep its validated workspace configuration. A workspace change MUST require closing or cancelling the request under the existing lifecycle rules first; stopping or blocking execution is not sufficient. AIH MUST NOT apply or queue a workspace change during an open request.
  {S1:L192, S3:section "Accepted policy"}

## 4.3. Request records and historical access

- [A] 4.3.1. Each request MUST retain its own stable identity and complete input, clarification, amendments, analysis, plan, execution, verification, documentation-impact, and outcome record across affected folders.
  {S1:L134}

- [A] 4.3.2. Closed requests MUST preserve distinguishable completed, cancelled, and rejected outcomes, short metadata summaries, stable folder-qualified references, and stable links. Lifecycle and archival status MUST be recorded without moving the request between active/history folders. Preserving these records does not require a separate history of workspace configurations or folder locations.
  {S1:L136, S2:section "Clarified request storage", S3:section "Accepted policy"}
  Details: {D1:section "Product and request ownership"}

- [A] 4.3.3. Ordinary work MUST use current documentation, persistent current-state notices, and the active request; historical summaries/details MUST be loaded only for a relevant question.
  {S1:L138}

- [A] 4.3.4. Successful closure MUST preserve durable knowledge and applicable decisions in current documentation so historical request records are not hidden prerequisites for normal work.
  {S1:L138}

- [A] 4.3.5. AIH MUST maintain one current change-work response with preserved prior versions, request/submission/run references, outcome, blockers/questions, next action, and linked evidence/forms.
  {S1:L170}

# 5. Clarification and amendments

## 5.1. Clarification scope and phase boundaries

- [A] 5.1.1. Clarify MUST establish what changes and why, recording problem/rationale, stakeholders/users, outcomes, current versus required behavior, in/out scope, functional/nonfunctional requirements, explicit constraints, observable acceptance criteria, assumptions, and unresolved questions.
  {S1:L201}

- [A] 5.1.2. Read-only evidence inspection during Clarify is OPTIONAL for understanding behavior, dependencies, feasibility, and missing requirements; it MUST NOT choose architecture, algorithms, technologies, components, tasks, or test tooling, or implement changes.
  {S1:L203}

- [A] 5.1.3. Clarify MUST be permitted to write clarification artifacts and narrowly factual evidence-backed known-defect/stale-documentation bookkeeping with source/request references, without repairs, redesign, substantive business-documentation rewriting, or inferred approved intent.
  {S1:L203}

- [A] 5.1.4. Clarification MUST retain explicitly supplied technical constraints and their provenance, while distinguishing existing implementation choices from required constraints.
  {S1:L205}

- [A] 5.1.5. Clarify MUST NOT implement, select a solution, generate an implementation plan, or automatically invoke Analyze; Analyze MUST NOT implement.
  {S1:L209}

- [A] 5.1.6. Documented defaults for optional unanswered questions are OPTIONAL; consequential unanswered questions MUST remain blockers.
  {S1:L217, S1:L314}

- [A] 5.1.7. AIH MUST record attributed requestor separately from actual framework submitter; a returned name MUST NOT establish authenticated identity or implementation authority.
  {S1:L231}

## 5.2. Iterative clarification and reconciliation

- [A] 5.2.1. One repeatable Clarify command MUST handle initial understanding, reviewed framework/requestor answers, amendments, changed human instructions, and later contradictions from persisted state.
  {S1:L229}

- [A] 5.2.2. Each Clarify round MUST reconcile submitted inputs and preserve one evolving interpretation, source-linked prior revisions, question catalog, conflicts, stale assumptions/answers, changed criteria, and downstream impacts.
  {S1:L233}

- [A] 5.2.3. Clarify MUST NOT resolve contradictions through arbitrary last-answer/file-wins; submitted explicit supersession may settle a statement, otherwise clarification is required.
  {S1:L233}

- [A] 5.2.4. Unchanged Clarify invocations MUST reuse valid results without duplicate questions, amendment application, gratuitous model calls, or semantic revision churn; meaningful new inputs may create another bounded question batch.
  {S1:L235}

- [A] 5.2.5. Each clarification round MUST report applied changes, open questions, blockers, next action, and whether it awaits framework-user answers, requestor answers, other resolution, or is ready for explicit Analysis; readiness MUST NOT imply approval.
  {S1:L237}

- [A] 5.2.6. Clarify resumption MUST reconcile the acknowledged complete task/segment boundary or incomplete Stop checkpoint, preserve scoped authority and progress, and avoid requiring the user to reconstruct a conversation.
  {S1:L239}

## 5.3. Amendment editing, capture, and history

- [A] 5.3.1. The request MUST expose an Amendments area with idle-only Add amendment, supporting changed wishes, additional detail, correction, and withdrawal without rewriting submitted history.
  {S1:L241}

- [A] 5.3.2. Each amendment MUST retain a stable ID, optional title/reason, original description, attribution, creation/save times, order, and known affected or superseded links.
  {S1:L241}

- [A] 5.3.3. Amendment history MUST preserve every accepted framework-saved/submitted revision and externally edited version next observed at a permitted capture action; unsaved keystrokes and unseen external saves need not be archived.
  {S1:L243}

- [A] 5.3.4. Amendments MUST show draft, saved-not-submitted, submitted, applied, superseded, withdrawn, and needs-clarification states as applicable; correction/withdrawal MUST append history subject only to authorized sensitive-value redaction.
  {S1:L243}

- [A] 5.3.5. Direct input edits MUST retain revision differences and provenance, link explicitly identified amendments, and MUST NOT silently disappear or create duplicate amendments for the same change.
  {S1:L245}

- [A] 5.3.6. Amendment application MUST retain original wording and trace its effects on interpretation, questions, supersession, and unresolved state; conflicts with returned answers require explicit resolution unless a submitted supersession already resolves them.
  {S1:L247}

- [A] 5.3.7. Complete amendment histories MUST survive completed/cancelled/rejected archival; late imports MUST NOT amend closed requests. Historical sensitive-value redaction MUST remain a separate explicitly authorized operation, not a late-import exception.
  {S1:L249}

- [A] 5.3.8. The framework Save operation MUST be documented for file-only users who need every amendment revision captured.
  {S1:L243}

# 6. Questionnaires and requestor exchanges

## 6.1. Questions, respondents, and authoritative answers

- [A] 6.1.1. File and portal questionnaire editing MUST share one authoritative answer source and revision checks; editing, saves, assignment, export generation, import, review persistence, and submission MUST be idle-only actions.
  {S1:L306}

- [A] 6.1.2. Each question MUST include stable ID/revision, context, intended respondent, plain explanation, answer instructions, and an always-available free-text field.
  {S1:L308}

- [A] 6.1.3. Choice questions MUST state single/multiple selection rules with clear options and a meaningful reasoned recommendation where applicable; recommended choices MUST start unchecked and MUST NOT imply approval.
  {S1:L308}

- [A] 6.1.4. Questions needing facts or examples MUST use suitable free text rather than invented choices.
  {S1:L308}

- [A] 6.1.5. The framework user MUST be able to change an agent-suggested intended respondent assignment.
  {S1:L308}

- [A] 6.1.6. Clarification questions MUST address what/why and observable outcomes; implementation choices MUST be labeled as Analysis design, with missing-requirement questions returned to clarification.
  {S1:L310}

- [A] 6.1.7. Questions MUST be batched after reasonable investigation in an easy copy-paste form; later batches MUST be limited to new consequential uncertainty.
  {S1:L312}

- [A] 6.1.8. Questionnaires MUST distinguish consequential blockers from optional choices, preserve wording/revisions, and report malformed, exclusive, partial, or free-text-modified selections without guessing.
  {S1:L314}

- [A] 6.1.9. Submitted answers MUST remain linked to affected requirements, decisions, plan, and execution; agents MUST NOT issue human approval/authorization to themselves.
  {S1:L316}

## 6.2. Plain-text form export and explanation

- [A] 6.2.1. Each clarification round waiting for marked outstanding requestor answers MUST generate a separate UTF-8 text form with preview/download and explicit regeneration; unchanged current exports MUST be reused, superseded exports retained, and empty forms avoided.
  {S1:L320}

- [A] 6.2.2. Reopening an answered requestor topic MUST use a visible new question revision or explicit re-request with provenance.
  {S1:L320}

- [A] 6.2.3. Requestor forms MUST be completable in an ordinary text editor without AIH, account, portal, Markdown knowledge, or technical metadata editing, using compact stable references, check marks, answer/comments fields, and an I don't know / Needs discussion response.
  {S1:L322}

- [A] 6.2.4. Forms MUST include product/request title, short business summary, form identity/revision, UTC generation time, completion instructions, and usefully ordered questions.
  {S1:L322}

- [A] 6.2.5. Each exported question MUST express one understandable request with an explanation of situation/terms/information needed, why it affects the change, suitable neutral illustrative examples, answer instructions, answer space, and comments/alternative space.
  {S1:L324-332}

- [A] 6.2.6. Form explanations MUST remain concise but sufficient for nontechnical readers, distinguish essential/optional answers and defaults, preserve attributed explicit technical constraints, and MUST NOT steer architecture or unapproved business decisions.
  {S1:L332}

- [A] 6.2.7. Downloading/forwarding a form MUST NOT mark questions answered or prove receipt; the export MUST remain a snapshot rather than another live answer store.
  {S1:L334}

- [A] 6.2.8. The latest applicable form MUST be linked from the current response and clarification page, with prior forms/rounds retained; sharing MUST remain the user's chosen channel without implied email/message authority.
  {S1:L336}

## 6.3. Intake, matching, and answer review

- [A] 6.3.1. Requestor intake MUST support file selection, drag-and-drop text forms, and pasted responses, display supported types/size limits, and report actionable encoding/format errors.
  {S1:L342}

- [A] 6.3.2. Accepted intake MUST preserve original content with receipt identity and target request/form while only staging it; uploading MUST NOT invoke an agent or overwrite active answers.
  {S1:L342}

- [A] 6.3.3. Import review MUST display original question/explanation, existing answer, proposed answer, attributed respondent, and match status, including missing, unknown, duplicate, altered, contradictory, and stale items.
  {S1:L343}

- [A] 6.3.4. Review MUST offer accept-all nonconflicting matches plus per-answer accept, retain, user-correct, or leave-unresolved controls while preserving original wording and correction attribution.
  {S1:L343}

- [A] 6.3.5. Older-form intake MUST show original questions, propose unchanged-revision answers for review, require explicit resolution for changed/withdrawn questions, and protect newer answers.
  {S1:L349}

- [A] 6.3.6. Missing form/question references MUST offer explicit manual matching with provenance rather than positional guessing.
  {S1:L349}

- [A] 6.3.7. Wrong/closed-request forms MUST remain unassigned in current intake for correction without mutating/reopening the other request; no-request intake MUST offer read-only inspection and new-request guidance without implicit request creation.
  {S1:L349}

- [A] 6.3.8. Accepted text outside recognized answer fields MUST be retained and reviewed; changed wishes may be explicitly linked as amendments or attributed input without duplicating the same change.
  {S1:L351}

## 6.4. Reviewed submission and recoverable launch

- [A] 6.4.1. Save reviewed answers MUST save authoritative answer drafts only; Import answers and clarify MUST explicitly merge reviewed answers and submit current relevant saved inputs/amendments to normal Clarify without a second generic approval dialog.
  {S1:L344}

- [A] 6.4.2. Import feedback MUST identify saved receipt/submission/round, progress, interpretation/questions/conflicts; deliberately partial submissions MUST retain consequential blockers and MUST NOT invent blank or unknown answers.
  {S1:L345}

- [A] 6.4.3. Combined import-and-Clarify MUST bind to the displayed form/question/draft/input/amendment revisions, require refresh/reconciliation of changed revisions, and protect intervening edits and unseen requirements.
  {S1:L347}

- [A] 6.4.4. The combined action MUST resolve unsaved edits before submission and be accepted as one recoverable idle operation; busy rejection MUST leave no merged drafts, submission, or queued work.
  {S1:L347}

- [A] 6.4.5. A launch failure MUST leave an inspectable saved submission, permit explicit resume only after reconciled ownership, and MUST NOT duplicate receipt/amendment effects or runs on retry.
  {S1:L347}

## 6.5. Attribution, authority, and file-only access

- [A] 6.5.1. Requestor responses MUST NOT approve plans, enable skills, edit human instructions, expand permissions, or start implementation; reviewer/submitter and attributed source MUST remain distinct.
  {S1:L351}

- [A] 6.5.2. File-only users MUST have equivalent form export/intake/review/draft/amendment/Clarify operations and direct authoritative-file editing with the same capture/conflict rules and preserved accepted-source links.
  {S1:L353}

- [A] 6.5.3. Accepted drafts, exports, originals, reviews, submissions, and interpretations MUST remain linked in request history subject to explicit authorized redaction; unreviewed receipts MUST NOT become active answers/instructions on later runs.
  {S1:L355}

# 7. Analysis and implementation

## 7.1. Design assessment and plan regeneration

- [A] 7.1.1. Analyze MUST own implementation design and planning, with traceability to clarified requirements and a clear separation between design decisions and requirements.
  {S1:L207}

- [A] 7.1.2. Consequential requirement gaps discovered in Analysis MUST preserve the draft analysis/plan and return to clarification within the same request; implementation/design questions MUST remain identifiable as Analysis questions.
  {S1:L207, S1:L257}

- [A] 7.1.3. The workflow MUST remove the standalone Plan action from CLI and portal; repeatable Analyze MUST own plan generation/regeneration and application of submitted answers, amendments, and updated human instructions.
  {S1:L253}

- [A] 7.1.4. Analyze MUST update affected artifacts from saved state, preserve current valid results and previous revisions, stop for consequential unanswered questions, and generate the plan automatically when sufficiently resolved without implementation.
  {S1:L255-259}

- [A] 7.1.5. Plan regeneration MUST retain completed-task history and identify still-valid tasks and required rework without needless resetting or rewriting on unchanged input.
  {S1:L259}

- [A] 7.1.6. Normal Analysis MUST keep interpretation, question catalog, assessment, and unrelated issues distinct, with a concise scoped none-found finding when appropriate rather than invented content.
  {S1:L272}

- [A] 7.1.7. Additional detailed impact, risk/decision, and verification records MUST be used when substantive detail warrants separate files; simple changes MUST retain concise equivalent coverage in the assessment or plan without empty boilerplate.
  {S1:L274}

## 7.2. Plan tasks and sequential execution

- [A] 7.2.1. Plan tasks MUST identify stable ID, sequence, outcome, requirement/decision links, specific changes, folder-qualified existing/new paths, action types, dependencies, and completion evidence; unresolved paths MUST use bounded investigation before dependent changes.
  {S1:L278}

- [A] 7.2.2. Implementation MUST execute tasks sequentially in plan order, record states/outcomes, preserve valid evidence, and MUST NOT silently skip, reorder, or concurrently execute tasks.
  {S1:L280}

- [A] 7.2.3. Material implementation scope/approach changes MUST revise the plan and obtain applicable authorization while explicitly invalidating affected work.
  {S1:L280}

- [A] 7.2.4. Every plan MUST include tasks for test creation/update, complete required-suite execution, authorized repair/reruns, documentation increment application and verification, and implementation-result evidence.
  {S1:L282}

- [A] 7.2.5. Explicit Implement/resume MUST reconcile the plan, valid approval/direct authorization, current human instructions, documentation, source content, folder access/mappings, and baseline before starting; stale, missing, or inconsistent prerequisites MUST block it.
  {S1:L284}

## 7.3. Approval, direct implementation, and scope

- [A] 7.3.1. Approving a plan MUST NOT start implementation; a clearly labeled combined Approve and implement operation is OPTIONAL and MUST record both intentions if provided.
  {S1:L209}

- [A] 7.3.2. Implement directly MUST perform necessary internal analysis and persist the sequential implementation/test/documentation/evidence plan before product changes, recording scope-bound direct authorization rather than fictional human approval.
  {S1:L211}

- [A] 7.3.3. Direct implementation MUST NOT waive consequential clarification, unrelated-defect selection, tests, documentation, logs, evidence, host approval, or authorization for material expansion.
  {S1:L211}

- [A] 7.3.4. Implementation authority MUST remain bound to identified business scope across folders; workspace registration MUST NOT substitute for scope approval or repeatedly invalidate unrelated valid authorization.
  {S1:L213}

## 7.4. Blockers, Stop, and resumption

- [A] 7.4.1. A consequential blocker MUST stop the entire change workflow after preserving immediate evidence, relevant defect/documentation status, response, checkpoint, and any required requestor questionnaire; independent implementation tasks MUST NOT continue.
  {S1:L217}

- [A] 7.4.2. When blocked ownership safely releases, users MUST be able to submit blocker answers/amendments or clarification without implicitly authorizing repairs or resuming implementation.
  {S1:L217}

- [A] 7.4.3. Stop MUST leave the request resumable, preserve unfinished work, and require confirmed termination or reconciled external ownership without requiring task success or passing tests.
  {S1:L221}

- [A] 7.4.4. Stop MUST allow incomplete tasks/segments to terminate safely after an indivisible operation or controlled termination, preserving unfinished evidence instead of waiting for whole-task success.
  {S1:L594}

- [A] 7.4.5. Resume/recovery MUST recheck current files, approvals, processes, evidence, root identity/access, and authority, inspect prior success before retry, and preserve uncertain effects rather than blindly duplicating external writes.
  {S1:L596}

- [A] 7.4.6. Stop, cancellation, and timeouts MUST safely terminate child processes on supported platforms, preserve partial results, and keep Stop/status available until termination or external release is confirmed.
  {S1:L602}

## 7.5. Recovery and evidence freshness

- [A] 7.5.1. Interrupted cross-filesystem work MUST preserve per-root progress and reconcile partial outcomes without claiming whole-product atomic commits or silently overwriting competing edits.
  {S1:L586}

- [A] 7.5.2. Direct source edits MUST invalidate affected evidence and require safe reconciliation; stale-lock recovery MUST check process identity rather than treating lock deletion as termination.
  {S1:L592}

- [A] 7.5.3. Verification MUST bind to actual checked relevant content including uncommitted/non-Git files and current root configuration; changes MUST invalidate affected evidence and Ready to close.
  {S1:L598}

# 8. Testing and defect disposition

## 8.1. Required suites and execution conditions

- [A] 8.1.1. The required suite MUST include current product tests and retained applicable earlier regressions across folders with one coverage/acceptance inventory.
  {S1:L288}

- [A] 8.1.2. Each required suite MUST run only in its declared authorized environment with satisfied infrastructure, permissions, isolation, cleanup, and compatible output locations; missing prerequisites MUST block execution and successful closure.
  {S1:L288}

- [A] 8.1.3. AIH MUST run relevant checks during tasks and the full maintained required suite before completion, repairing authorized in-scope defects and rerunning the full suite against final relevant content until passed or blocked/limited.
  {S1:L290}

- [A] 8.1.4. AIH MUST NOT weaken, disable, remove, or reclassify tests merely to pass; expected-behavior changes MUST trace to authorized requirements, and obsolete incompatible historical versions MUST NOT run solely because archived evidence contains them.
  {S1:L294}

- [A] 8.1.5. Genuinely inapplicable checks MUST be defined explicitly rather than inventing passing test results.
  {S1:L223}

## 8.2. Repair limits and authorized continuation

- [A] 8.2.1. Automatic repairs MUST have configurable budgets and no-progress detection, defaulting to at most three unsuccessful cycles for the same unresolved failure across retries, segments, and restarts.
  {S1:L292}

- [A] 8.2.2. Repair budgets MUST support configured elapsed-time limits and reliable measured-token limits where telemetry exists; exhaustion or no progress MUST block safely with diagnosis, attempted repair, rerun evidence, and attempt history retained.
  {S1:L292}

- [A] 8.2.3. Explicit user continuation is OPTIONAL to extend a repair budget with recorded reason and scope; it MUST retain prior history and MUST NOT waive required passing tests.
  {S1:L292}

## 8.3. Unrelated defects and retained obligations

- [A] 8.3.1. Unrelated defects MUST be recorded for explicit human include/defer/investigate disposition; included defects MUST amend interpretation, plan, tests, documentation, and material-scope authorization, including in direct mode.
  {S1:L296}

- [A] 8.3.2. Established unfixed defects MUST remain in current known-defect documentation with stable identity, symptoms, evidence/reproduction, affected areas, impact, supported workarounds, disposition, and origin; suspected defects MUST remain unconfirmed until evidenced.
  {S1:L298}

- [A] 8.3.3. Verified repairs MUST update defect status without treating defect records as queued requests or authority for future work.
  {S1:L298}

- [A] 8.3.4. A deferred defect failing any required test MUST block successful completion without a waiver; the user may authorize repair or cancel/reject, while nonblocking deferred defects may remain documented.
  {S1:L300}

# 9. Request outcomes

## 9.1. Successful completion and explicit closure

- [A] 9.1.1. Successful completion MUST require implemented scope, passing required tests, acceptance/verification satisfaction, current affected documentation or justified no-impact, and recorded evidence; skipped, stale, failed, and unexecuted required tests MUST NOT count as passes.
  {S1:L223}

- [A] 9.1.2. Passing gates MUST set Ready to close while the request remains open; explicit human Close successfully MUST recheck current gates and content before archival, withdrawing readiness if evidence changed.
  {S1:L223}

- [A] 9.1.3. Integration and deployment MUST remain separate milestones; Git, merging, and production deployment MUST NOT become completion gates unless explicitly included in request scope.
  {S1:L225}

- [A] 9.1.4. Product changes after request closure MUST use a new request.
  {S1:L225}

## 9.2. Cancellation, rejection, and retained state

- [A] 9.2.1. Explicit idle cancellation/rejection MUST preserve partial changes, evidence, and unresolved outcomes without automatic rollback or a requirement to pass tests or rewrite all documentation.
  {S1:L221}

- [A] 9.2.2. Before unsuccessful closure releases the request slot, AIH MUST preserve a discoverable current-state notice covering retained changes, affected/stale documentation, defects, verification uncertainty, and archived evidence; subsequent authorized work MUST reconcile affected knowledge before reliance.
  {S1:L221}

# 10. Independent product questions

- [A] 10.1. AIH MUST offer a separate read-only question lane when globally idle, including with no request, pending idle setup, or an open/blocked request whose owner stopped; existing questions and answers MUST remain readable at all times.
  {S1:L174}

- [A] 10.2. Questions MUST NOT open a request, occupy its slot, change approval, or resume blocked work.
  {S1:L178}

- [A] 10.3. Question execution MUST NOT change product source, durable documentation, configuration, custom instructions, or change-work state; only its permitted communication and execution records may be written.
  {S1:L180}

- [A] 10.4. Where read-only enforcement is unavailable, AIH MUST report the limitation and offer a constrained/manual route without claiming prompting alone provides protection.
  {S1:L182}

- [A] 10.5. Answers MUST cite stable folder-qualified sources, observed content versions, and uncertainty. They MUST use the current validated workspace configuration and detect/report mixed observations caused by external edits or repeat affected inspection within the action.
  {S1:L184, S3:section "Accepted policy"}

- [A] 10.6. Question intake MUST apply the same sensitive-input admission rules as other human intake.
  {S1:L184}

- [A] 10.7. Question execution MUST NOT modify the product to demonstrate an answer.
  {S1:L184}

- [A] 10.8. Questions asking for modifications MUST be directed to explicit change work and MUST NOT silently become requests, implementation authority, or submitted blocker answers.
  {S1:L186}

- [A] 10.9. Q&A findings MUST require an explicit authorized change/documentation action before durable documentation updates and MUST NOT start that action automatically.
  {S1:L302}

# 11. Product documentation

## 11.1. Current knowledge, provenance, and change tracking

- [A] 11.1.1. Documentation MUST be maintained as normal authorized workflow work and consulted during clarification, before planning, and before implementation.
  {S1:L359}

- [A] 11.1.2. Current documentation MUST cover all relevant registered folders, including read-only components, and distinguish intended requirements, observed implementation, verification, and deployment; future behavior MUST remain in its request, with approved unmet requirements explicitly statused if catalogued.
  {S1:L361}

- [A] 11.1.3. Disagreement among documentation, implementation, and intent MUST be recorded with observation separated from approved meaning; changing business meaning MUST require clarification rather than promoting inference.
  {S1:L363}

- [A] 11.1.4. Documentation updates MUST preserve human-authored content and use revision-checked reviewable changes to affected sections without requiring Git.
  {S1:L365}

- [A] 11.1.5. Documentation drift MUST be checked at run start and after relevant changes; externally managed/uninspectable components MUST retain provenance, last-known state, and explicit unknowns.
  {S1:L367}

- [A] 11.1.6. Relevant changes MUST refresh affected documentation and navigation with owning request/operation, sources, verification, and unresolved issues; partial implementation MUST expose drift rather than claim old documentation current.
  {S1:L369}

- [A] 11.1.7. Every request, including direct implementation, MUST retain a planned/applied/verified documentation increment reconciled with actual changes, or a justified no-impact finding; documentation failures MUST prevent successful completion.
  {S1:L373-377}

- [A] 11.1.8. Relevant documentation MUST carry provenance, dates, source fingerprints, owning request/operation and decisions, verification status, and unresolved reviews without flattening all content into navigation catalogs.
  {S1:L447-449}

## 11.2. Reconstruction coverage and evidential limits

- [A] 11.2.1. Documentation MUST aim to specify a functionally equivalent rebuild defined by acceptance tests and undergo a recorded completeness/traceability review of business rules, interfaces, results, dependencies, acceptance, and recovery prerequisites.
  {S1:L379}

- [A] 11.2.2. Reconstruction MUST be reported as specified but not demonstrated until independent reconstruction evidence exists; ordinary tests or specification review MUST NOT imply rebuilt equivalence, bit identity, or production-data recovery.
  {S1:L379}

- [A] 11.2.3. An independent reconstruction exercise MUST NOT be a mandatory completion gate under this specification.
  {S1:L379}

- [A] 11.2.4. If an independent reconstruction exercise is explicitly authorized and performed, its scope, prerequisites, results, and remaining limitations MUST be recorded separately.
  {S1:L379}

- [A] 11.2.5. Rebuild documentation MUST inventory necessary external resources and gaps with content-versioned references to operational scripts/IaC and inert examples.
  {S1:L379}

## 11.3. Initial and incremental reverse engineering

- [A] 11.3.1. Users MUST have initial-baseline and incremental reverse-engineering modes across registered existing directories without Git, a database, or preexisting AIH documentation.
  {S1:L383}

- [A] 11.3.2. Reverse-engineering inventory MUST cover authorized source, configuration, interfaces, tests, build/deployment definitions, and documentation without executing/importing inspected code/hooks/attachments or exposing credentials; unavailable folders and extraction limits MUST remain explicit.
  {S1:L385}

- [A] 11.3.3. Agent synthesis MUST document supported architecture, dependencies, domain, behavior, interfaces, flows, operations, and requirements while explicitly labeling inference, assumptions, contradictions, missing external facts, and unverified behavior.
  {S1:L387}

- [A] 11.3.4. Reverse engineering MUST write only authorized documentation and framework records, preserving implementation, source configuration, executable tests, deployment code, and human instructions; repairs/refactoring MUST require change work.
  {S1:L389}

- [A] 11.3.5. Incremental refresh MUST target changed/newly relevant material and dependencies, preserve unaffected content, and record scope, provenance, gaps, diffs, and validation without claiming structural validity alone proves documentation completeness.
  {S1:L391}

- [A] 11.3.6. Interrupted bootstrap/refresh MUST preserve valid progress and resume from evidence; missing profile, compatibility, authentication, or permission MUST leave semantic generation pending/partial with actionable setup or manual-handoff guidance without silent agent switching/installing.
  {S1:L399}

## 11.4. Baseline gates and maintenance ownership

- [A] 11.4.1. Bootstrap and explicitly invoked documentation-only maintenance MUST remain scoped system operations without implementation authority.
  {S1:L45}

- [A] 11.4.2. Bootstrap and standalone documentation maintenance MUST retain resumable audit/checkpoint records without a synthetic change request or reliance on private memory/unavailable conversations.
  {S1:L140-142}

- [A] 11.4.3. Bootstrap MUST complete the authorized current workspace baseline before opening a first/new request, checking inventory, category applicability, evidence-backed coverage, provenance/unknowns, reconstruction review, catalogs, links, and tree structure.
  {S1:L393}

- [A] 11.4.4. Baseline completion MUST NOT require resolving every external uncertainty or verifying all runtime behavior; remaining unknown external facts, unverified behavior, and their limitations MUST be clearly identified and preserved.
  {S1:L393}

- [A] 11.4.5. AIH MUST NOT claim product tests passed merely because the documentation baseline is complete.
  {S1:L393}

- [A] 11.4.6. Pending idle setup MUST permit prerequisite configuration, Q&A, and drafts; after explicit successful continuation it MUST release ownership and enable request creation as a separate action.
  {S1:L395}

- [A] 11.4.7. Standalone documentation maintenance MUST require no open request; documentation inside an open request MUST use its explicit authorized task, increment, evidence, and blockers without creating another writer.
  {S1:L395}

## 11.5. Navigation, document size, and reorganization

- [A] 11.5.1. Documentation navigation MUST provide the requirements, decisions, and context entry points with links to canonical typed detail; progressive extension catalogs MUST reach relevant terminal content without loading unrelated leaves, with stable document identities and one canonical topic copy.
  {S1:L403-407, S2:section "Accepted document organization and references"}
  Details: {D1:section "Entry layer and extension navigation"}

- [A] 11.5.2. Each logical extension-navigation catalog MUST initially have at most eight direct children; entry files, metadata registry records, and physical type-directory counts are outside this limit.
  {S1:L411-414, S2:section "Accepted document organization and references"}
  Details: {D1:section "Entry layer and extension navigation"}

- [A] 11.5.3. The deepest and shallowest extension content leaves MUST initially differ by at most one edge from the extension-navigation root; the requirements, decisions, and context entry layer is outside this depth-balance calculation.
  {S1:L411-414, S2:section "Accepted document organization and references"}
  Details: {D1:section "Entry layer and extension navigation"}

- [A] 11.5.4. Extension content leaves MUST target at most 1,500 words, splitting at meaningful boundaries and recording justified exceptions for indivisible reference material; non-prose formats MUST use appropriate size checks, while entry files retain their section readability rules.
  {S1:L411-414, S2:section "Accepted document organization and references"}
  Details: {D1:section "Entry layer and extension navigation"}

- [A] 11.5.5. Tree limits MUST be supported configuration parameters, with dynamic meaningful grouping and no unrestricted-hierarchy substitution, empty padding, or fabricated content.
  {S1:L416}

- [A] 11.5.6. Automatic tree reorganization MUST preserve human content and topic identities, assign identities to genuinely new split topics, repair links, and retain reference mappings and structural-change history.
  {S1:L418}

- [A] 11.5.7. Supported readers MUST avoid half-reorganized documentation, and consistency limitations for readers bypassing the protocol MUST be stated; search MUST supplement rather than replace tree navigation.
  {S1:L420}

## 11.6. Applicability and business knowledge

- [A] 11.6.1. The documentation applicability catalog MUST classify every required category as applicable, not applicable with rationale, or unknown needing investigation, generating substantive documents only where relevant.
  {S1:L424}

- [A] 11.6.2. The documentation applicability catalog MUST cover product purpose, scope, capabilities, stakeholders, users, terminology, domain knowledge, and definitions.
  {S1:L424, S1:L428}

- [A] 11.6.3. The documentation applicability catalog MUST cover business requirements, rules, processes, acceptance criteria, and requirement-to-implementation-to-test traceability.
  {S1:L424, S1:L429}

- [A] 11.6.4. The documentation applicability catalog MUST cover nonfunctional requirements, service objectives, performance, capacity, availability, accessibility, localization, and supported platforms.
  {S1:L424, S1:L430}

- [A] 11.6.5. The documentation applicability catalog MUST cover UI definitions, visual and interaction design, web interfaces, navigation, user flows, error behavior, and user help.
  {S1:L424, S1:L436}

- [A] 11.6.6. The documentation applicability catalog MUST cover any additional product-specific knowledge needed to preserve its definition and support functional reconstruction.
  {S1:L424, S1:L445}

## 11.7. Architecture, data, interfaces, and dependencies

- [A] 11.7.1. The documentation applicability catalog MUST cover architecture, component responsibilities, solution design, architectural decisions, alternatives, and tradeoffs.
  {S1:L424, S1:L431}

- [A] 11.7.2. The documentation applicability catalog MUST cover product/workspace structure, registered folder IDs, purposes, access modes, component ownership, cross-folder dependencies, important paths and entry points, without assuming repositories exist.
  {S1:L424, S1:L432}

- [A] 11.7.3. The documentation applicability catalog MUST cover data structures, logical and physical models, storage, data ownership, lineage, quality, retention, privacy, and migrations.
  {S1:L424, S1:L433}

- [A] 11.7.4. The documentation applicability catalog MUST cover ETL and transformations, pipelines, orchestration, schedules, semantic models, reports, dashboards, and analytics definitions.
  {S1:L424, S1:L434}

- [A] 11.7.5. The documentation applicability catalog MUST cover algorithms, functional logic, APIs, interface contracts, integrations, events, queues, and external services.
  {S1:L424, S1:L435}

- [A] 11.7.6. The documentation applicability catalog MUST cover networking, authentication, authorization, roles, secrets references, threat models, security controls, and relevant compliance constraints.
  {S1:L424, S1:L437}

- [A] 11.7.7. The documentation applicability catalog MUST cover dependencies, versions, licenses, build requirements, configuration, feature flags, and environment differences.
  {S1:L424, S1:L438}

## 11.8. Operations, verification, and support knowledge

- [A] 11.8.1. The documentation applicability catalog MUST cover deployment procedures and script references, releases, infrastructure, cloud services, resource inventories, and relevant cost assumptions.
  {S1:L424, S1:L439}

- [A] 11.8.2. The documentation applicability catalog MUST cover unit, integration, system, acceptance, performance, and security testing; test data, fixtures, expected results, and evidence.
  {S1:L424, S1:L440}

- [A] 11.8.3. The documentation applicability catalog MUST cover backup, recovery, disaster recovery, restore validation, operational continuity, and rebuild prerequisites.
  {S1:L424, S1:L441}

- [A] 11.8.4. The documentation applicability catalog MUST cover logging, monitoring, alerting, incident response, troubleshooting, administration tools, and support interfaces.
  {S1:L424, S1:L442}

- [A] 11.8.5. The documentation applicability catalog MUST cover operational processes, schedules, maintenance, data operations, escalation, and handover.
  {S1:L424, S1:L443}

- [A] 11.8.6. The documentation applicability catalog MUST cover user guides, onboarding, administration guides, support materials, known limitations, a dedicated known-defects catalog, deprecation, and retirement.
  {S1:L424, S1:L444}

## 11.9. Typed detail and document traceability

- [A] 11.9.1. Product documentation MUST retain requirements.md, decisions.md, and context.md as independently structured entry points to detailed product knowledge.
  {S2:section "Accepted document organization and references"}
  Details: {D1:section "Product collection"}

- [A] 11.9.2. Knowledge needing extensive explanation or specialized structure MUST be represented in applicable typed extension documents, preserving its complete meaning and evidential status.
  {S2:section "Accepted document organization and references"}
  Details: {D3}

- [A] 11.9.3. A subject MUST have one authoritative detailed representation that may be referenced from multiple entry files without competing copies.
  {S2:section "Accepted document organization and references"}
  Details: {D1:section "Source evidence and document references"}

- [A] 11.9.4. Every finding MUST remain independently understandable in its core meaning, scope, conditions, and certainty while identifying any defining detail precisely.
  {S2:section "Accepted document organization and references"}
  Details: {D1:section "Source evidence and document references"}

- [A] 11.9.5. Users MUST be able to navigate from findings to detailed documents and back to the related findings through maintained references.
  {S2:section "Accepted document organization and references"}
  Details: {D2:section "Citation and backlink contract"}

- [A] 11.9.6. Document references MUST remain distinguishable from supporting source evidence and acceptance; a detailed document MUST NOT imply approval or verified implementation merely because it is linked.
  {S2:section "Accepted document organization and references"}
  Details: {D2:section "Citation and backlink contract"}

- [A] 11.9.7. Documentation MUST create only applicable substantive extensions and MUST NOT manufacture empty documents or unsupported knowledge to fill a predefined type list.
  {S2:section "Accepted document organization and references"}
  Details: {D3}

- [A] 11.9.8. Document identities MUST survive relocation and renaming, and retired identities MUST NOT be reused for unrelated content.
  {S2:section "Accepted document organization and references"}
  Details: {D2:section "Document registry"}

## 11.10. External materials and original attachments

- [A] 11.10.1. Product documentation MUST be able to reference relevant materials outside .aih_product/ with their authority role, observed revision, freshness, and provenance explicit.
  {S2:section "Attachment preservation clarification"}
  Details: {D1:section "External materials"}

- [A] 11.10.2. Routine documentation maintenance MUST NOT modify external materials; their modification MUST be implementation work in an authorized request with scope and verification equivalent to product-code changes.
  {S2:section "Attachment preservation clarification"}
  Details: {D1:section "External materials"}

- [A] 11.10.3. A material reference MUST NOT expand workspace membership, reading rights, or write authority.
  {S2:section "Attachment preservation clarification"}
  Details: {D1:section "External materials"}

- [A] 11.10.4. Original attachments MUST remain unchanged in their request-specific attachment locations, including during request documentation regeneration and product integration.
  {S2:section "Attachment preservation clarification"}
  Details: {D1:section "Product collection"}

- [A] 11.10.5. Copying otherwise unreferenced attachment material into product documentation is OPTIONAL; material referenced by product documentation MUST be retained as a product-owned copy when its original is in a request folder, preserving provenance and the unchanged original.
  {S2:section "Attachment preservation clarification", S2:section "Product reference boundary"}
  Details: {D1:section "Product collection"}

- [A] 11.10.6. Unavailable or changed external evidence MUST remain visible as unknown or stale, rather than silently disappearing or being presented as verified current knowledge.
  {S2:section "Attachment preservation clarification"}
  Details: {D1:section "External materials"}

- [A] 11.10.7. Product documentation MUST NOT reference files in request folders, including original attachments; every referenced file MUST be retained within product documentation or reside outside .aih_product/ as product-owned material.
  {S2:section "Product reference boundary"}
  Details: {D1:section "Product reference boundary"}

## 11.11. Request changes against product knowledge

- [A] 11.11.1. Request documentation MUST contain source-supported additions, modifications, explicit removals, and unresolved change questions against an identified current product baseline.
  {S2:section "Migration and request-specific documentation"}
  Details: {D4:section "Compute the change set"}

- [A] 11.11.2. Already documented unchanged product knowledge MUST be referenced rather than repeated in request findings or copied extension documents.
  {S2:section "Migration and request-specific documentation"}
  Details: {D4:section "Typed detail and references"}

- [A] 11.11.3. Changed findings MUST retain source-supported reasons, conditions, scope, and exact targets, including every affected category, without carrying forward unrelated baseline content.
  {S2:section "Migration and request-specific documentation"}
  Details: {D2:section "Baseline and change operations"}

- [A] 11.11.4. Omission from a request MUST NOT imply deletion or withdrawal of an existing product finding or detailed document.
  {S2:section "Migration and request-specific documentation"}
  Details: {D2:section "Baseline and change operations"}

- [A] 11.11.5. Request generation MUST expose ambiguous change intent and conflicting authority as unresolved instead of choosing an unsupported replacement.
  {S2:section "Migration and request-specific documentation"}
  Details: {D4:section "Compute the change set"}

- [A] 11.11.6. Users MUST be able to verify which source findings produced changes and which were already covered by the product baseline without duplicating unchanged statements.
  {S2:section "Migration and request-specific documentation"}
  Details: {D2:section "Baseline and change operations"}

- [A] 11.11.7. Changed baseline evidence MUST trigger renewed comparison and verification before integration; stale request targets MUST NOT silently overwrite current product knowledge.
  {S2:section "Migration and request-specific documentation"}
  Details: {D4:section "Commit and subsequent integration"}

- [A] 11.11.8. Producing request documentation MUST NOT modify current product documentation, execute implementation, grant external-file-write authority, or perform unrequested lifecycle transitions.
  {S2:section "Migration and request-specific documentation"}
  Details: {D4:section "Commit and subsequent integration"}

## 11.12. Coordinated documentation maintenance

- [A] 11.12.1. AIH MUST maintain affected entry files, typed detail, catalogs, and references together during authorized workflow work, preserving human content and unaffected knowledge.
  {S2:section "Migration and request-specific documentation"}
  Details: {D1:section "Maintenance"}

- [A] 11.12.2. Request documentation regeneration MUST preserve original sources and sibling request inputs, metadata, analysis, plans, implementation evidence, and historical records.
  {S2:section "Migration and request-specific documentation"}
  Details: {D4:section "Commit and subsequent integration"}

- [A] 11.12.3. Verification MUST cover source-to-change completeness and change-to-source truthfulness across the entire linked documentation collection.
  {S2:section "Migration and request-specific documentation"}
  Details: {D4:section "Prepare and verify"}

- [A] 11.12.4. Request documentation MUST distinguish settled change definitions from unresolved matters and planned behavior from implemented, tested, or deployed product behavior.
  {S2:section "Migration and request-specific documentation"}
  Details: {D4:section "Compute the change set"}

- [A] 11.12.5. Supported readers MUST receive a consistent verified documentation collection after updates; failures or concurrent edits MUST leave the previous collection intact or recoverable.
  {S2:section "Migration and request-specific documentation"}
  Details: {D2:section "Validation and update integrity"}

# 12. Evidence, efficiency, and sensitive information

## 12.1. History, compact evidence, and token usage

- [A] 12.1.1. Change/decision history MUST preserve stable source-linked events, with ordinary corrections appended as supersessions. Essential decisions, outcomes, and evidence MUST NOT be discarded as verbose logs. A separate history of workspace configurations and folder-location mappings is not required.
  {S1:L451-457, S3:section "Accepted policy"}

- [A] 12.1.2. Verbose CLI-log retention MUST be configurable, documented, and non-silent while preserving essential request history and decision evidence.
  {S1:L455-457}

- [A] 12.1.3. Evidence MUST record useful summaries and observable actions without private chain-of-thought or fabricated unavailable conversations, and MUST NOT claim hashes/append-only files are tamper-proof against filesystem owners.
  {S1:L457-459}

- [A] 12.1.4. AIH MUST minimize avoidable model-token use without reducing analysis, coverage, instructions, tests, documentation, evidence, or silently changing agents.
  {S1:L84, S1:L90}

- [A] 12.1.5. Compact outputs MUST retain evidence references and label omitted detail while preserving complete available sanitized evidence for targeted inspection.
  {S1:L88}

- [A] 12.1.6. Diagnostics and portal status MUST expose adapter-supplied actual token usage by operation/run/segment and useful totals, mark missing telemetry unavailable, and distinguish measured savings from proxies.
  {S1:L92}

## 12.2. Intake screening and historical redaction

- [A] 12.2.1. Detected sensitive intake MUST be rejected before normal persistence with a corrected-resubmission request and only non-sensitive rejection metadata; rejected values MUST NOT appear in diagnostics, receipts, responses, or submissions.
  {S1:L164}

- [A] 12.2.2. Sensitive-input screening MUST precede durable intake and prevent detected rejected values appearing in previews, spooling, temporary records, logs, indexes, or telemetry; detection MUST be described as best effort.
  {S1:L461-463}

- [A] 12.2.3. Sensitive human-owned source drafts/files MUST NOT be silently rewritten/deleted; submission MUST be refused with non-echoing correction guidance while accepted originals preserve their exact content under the redaction exception.
  {S1:L463-465}

- [A] 12.2.4. AIH MUST support explicit human-authorized historical redaction scoped to identified sensitive material in AIH-owned originals, revisions, archives, logs, indexes, temporary/recovery copies, reconciling derived records and fingerprints to prevent restoration.
  {S1:L465-467}

- [A] 12.2.5. Historical redaction MUST be recoverable without new secret-bearing backups, preserve a non-sensitive authorization/record/reason/limits audit, label redacted originals, preserve unrelated history and request scope, and invalidate affected evidence.
  {S1:L465-469}

- [A] 12.2.6. Historical redaction MUST NOT authorize agent edits to human instructions or claim erasure of external exports, providers, or independent backups, and MUST obey global idle ownership.
  {S1:L467-469}

## 12.3. Implementation logs and results

- [A] 12.3.1. Every implementation attempt, including normal/direct, resumed, failed, and cancelled work, MUST create durable initial logs/results records before changes and update them throughout execution.
  {S1:L471-473}

- [A] 12.3.2. Implementation logs MUST retain timestamps, run/segment/task and input/plan revisions, stable folder-qualified file references, available events, action intentions/results, observed changes, tests/content versions, documentation, errors, cancellation, and checkpoints, distinguishing attempted/confirmed/failed/uncertain outcomes.
  {S1:L473-475, S3:section "Accepted policy"}

- [A] 12.3.3. Results summaries MUST explain requested/attempted/completed/incomplete work, actual changes, verification, documentation increment, defect disposition, blockers, uncertainty, repair budget, recovery, and next action with evidence links.
  {S1:L475-477}

- [A] 12.3.4. Crash recovery MUST reconstruct and clearly label available summaries without inventing unavailable action history, inspect uncertain effects before retry, and preserve logs/results after archival.
  {S1:L477-479}

# 13. Standalone skills

## 13.1. Package portability and invocation authority

- [A] 13.1.1. Every delivered skill MUST work by copying its directory outside installed AIH without an exporter, engine, portal, database, fixed state path, or ordinary Git requirement; intrinsic dependencies MUST be declared with explicit input/output locations.
  {S1:L485-487}

- [A] 13.1.2. Delivered skills MUST already contain matching versioned conventions, helpers, and behavioral guidance, and MUST NOT require ordinary runs to regenerate core resources or reconstruct the whole AIH lifecycle.
  {S1:L491-497}

- [A] 13.1.3. Standalone invocations MUST record input/output locations, allowed folder identities/access, scope/effects, initiating instruction, constraints, relevant approved/direct plan authority, and results/evidence; missing consequential authority MUST block effects without inventing stronger identity assurance.
  {S1:L497-499}

- [A] 13.1.4. Requirements-only, read-only, setup, and documentation-only standalone work MUST retain its applicable authority without acquiring an implementation-plan requirement merely for permitted record/documentation writes.
  {S1:L497-499}

- [A] 13.1.5. Standalone portability MUST preserve the same per-folder and host boundaries without AIH global state; examples, metadata, and effects declarations MUST NOT grant permissions or widen roots.
  {S1:L499-501}

## 13.2. Delivered capabilities and their boundaries

- [A] 13.2.1. The initial delivery MUST include eight complete standalone packages with seven core skills enabled by default and git-workflow installed but disabled; enabled, available, installed, and authorized MUST remain distinct.
  {S1:L503-507}

- [A] 13.2.2. Standalone clarify-requirements MUST support iterative rounds, explained text forms, import review, and amendments using explicit permitted local input/output locations without requiring a portal or another installed skill.
  {S1:L519}

- [A] 13.2.3. Direct-mode standalone implement-plan MUST include its own required analysis/planning guidance and helpers; cross-skill reuse MUST remain self-contained without adding a Plan workflow stage or fabricating approval.
  {S1:L521}

- [A] 13.2.4. Test diagnosis MUST NOT authorize unrelated repairs; implementation performs scoped fixes, and skill execution MUST preserve repair budgets, required-test gates, and attempt history.
  {S1:L523}

- [A] 13.2.5. Reverse engineering and documentation maintenance MUST share reusable evidence without competing baselines; read-only questions MUST NOT invoke documentation-writing effects.
  {S1:L525}

## 13.3. Discovery, availability, and configuration

- [A] 13.3.1. Skill discovery MUST expose compact metadata, compatibility, availability, enabled status, and locations before bodies; new installed skills MUST be discoverable without editing the entry point, with actionable malformed/disabled/duplicate/incompatible diagnostics.
  {S1:L481-485}

- [A] 13.3.2. A required disabled/unavailable skill MUST block with actionable guidance rather than silently skipping work or enabling a substitute.
  {S1:L503-505}

- [A] 13.3.3. The CLI and portal MUST expose consistent installed skill catalogs, purposes, outputs, boundaries, usage links, and diagnostics without duplicating full instructions.
  {S1:L531}

- [A] 13.3.4. Discovery MUST report stale/missing catalog entries and integrity/identity conflicts; it MUST NOT bypass those problems to execute packages.
  {S1:L544}

- [A] 13.3.5. Skill configuration MUST change only while idle, record when it applies, and preserve historical skill/version references; it MUST NOT install or authorize skills or regenerate core catalogs.
  {S1:L546}

- [A] 13.3.6. Discovery/metadata MUST NOT execute package code, install dependencies, trigger dynamic imports, or change trusted executable settings.
  {S1:L550}

# 14. Agent profiles and external execution

## 14.1. Profile selection, diagnostics, and launch boundaries

- [A] 14.1.1. AIH MUST provide functional Codex CLI integration, manual handoff, and multiple named profiles/adapters without coupling profile names to agents.
  {S1:L554}

- [A] 14.1.2. Profiles MUST support defaults, per-capability assignment, and explicit per-run selection with documented precedence and recorded effective segment selection.
  {S1:L556}

- [A] 14.1.3. Ordinary requests and generated content MUST NOT change privileged executable configuration; deliberate local administration MUST validate adapter-supported settings and reject arbitrary commands or unrestricted arguments.
  {S1:L558}

- [A] 14.1.4. Profile diagnostics MUST report executable/version, compatibility, confinement, and supported authentication status with actionable guidance, distinguishing credential presence from verified service access and never automatically installing/upgrading CLIs.
  {S1:L560}

- [A] 14.1.5. Adapters MUST support declared availability/start/events/identities/exit/timeout/cancellation/resumption capabilities; unavailable native resume MUST use a clearly labeled new segment from persisted state without silent agent switching.
  {S1:L564}

- [A] 14.1.6. Adapters unable to represent and enforce all required writable/read-only roots under host controls MUST block launch rather than widen to a common ancestor, omit roots, relocate content, or suppress inherited approvals/restrictions.
  {S1:L566}

- [A] 14.1.7. Unavailable noninteractive approval handling MUST safely end/stop and offer manual handoff after reconciled ownership; profile/capability changes MUST apply only to the next explicit action/segment, not a live process.
  {S1:L570}

## 14.2. Manual handoff and release

- [A] 14.2.1. Manual handoff MUST reserve the sole action slot before executable instructions are exposed, bind scope and authority to a unique identity, survive restarts, and MUST NOT label prepared work as actually running.
  {S1:L572}

- [A] 14.2.2. Returned output MUST NOT itself release handoff ownership or prove completion; Stop/release MUST request external termination, obtain human stopped/never-started confirmation, reconcile files/evidence, and retain uncertain attribution.
  {S1:L572}

- [A] 14.2.3. Uncertain external termination MUST retain the reservation and block competing operations; stale heartbeat, browser closure, and lock deletion MUST NOT imply termination.
  {S1:L572}

# 15. Portal experience

## 15.1. Local startup and first-use setup

- [A] 15.1.1. The local portal MUST start from the single framework home, default to loopback, support port/no-browser options, report URL and browser/port/shutdown failures cleanly, and only auto-launch a browser with confined writes; otherwise it MUST provide a URL for independent opening.
  {S1:L608}

- [A] 15.1.2. The portal MUST serve one local user without requiring a shared server, cloud account, database, or Git, using clear action-oriented language.
  {S1:L610}

- [A] 15.1.3. First portal startup with absent product state MUST automatically initialize and begin configured-agent documentation baselining for the validated home and explicitly preconfigured roots, without enrolling neighbors or selecting opportunistically discovered agents.
  {S1:L612}

- [A] 15.1.4. Setup MUST show responsive phase/progress/gaps/errors/input status and retain an operation identity across refresh/concurrent starts; reopening MUST NOT restart a safely stopped operation without explicit continuation.
  {S1:L614}

- [A] 15.1.5. Setup MUST distinguish absent, recoverable partial, invalid, and complete state, preserve invalid/human files, and MUST NOT regenerate a completed baseline on every launch.
  {S1:L616}

- [A] 15.1.6. Missing usable profile/authentication MUST retain safe deterministic setup and visibly pending semantic generation with explicit setup/manual continuation and no false completion.
  {S1:L618}

## 15.2. Pages and product navigation

- [A] 15.2.1. The portal MUST provide Overview, Current request, Ask a question, Product documentation, Runs and recovery, History and decisions, Settings, and Help pages over the same records and operations as the CLI.
  {S1:L620-629}

- [A] 15.2.2. Overview MUST show current request/phase, next action, blockers, response, test/documentation status, workspace availability, selected profile, distinct setup/reconciliation progress, and available token usage; Start request MUST require idle/no request/current complete baseline.
  {S1:L622}

- [A] 15.2.3. Ask a question MUST show editor, attachments, explicit Ask, progress, answer/source links, and history, with operational editing/intake disabled while busy and existing answers readable.
  {S1:L624}

- [A] 15.2.4. Product documentation MUST show progressive navigation, breadcrumbs/search, applicability, source provenance/dates/freshness, defects, reviews, current-state notices, per-area coverage, and explicit permitted refresh/reconciliation actions with truthful reconstruction status.
  {S1:L625}

- [A] 15.2.5. Runs and recovery MUST show current/prior runs, sanitized events, task/segment progress, checkpoints, errors, summaries/evidence, usage, and permitted Stop/resume/recovery with distinct system-operation and product/process outcomes.
  {S1:L626}

- [A] 15.2.6. History and decisions MUST expose closed-request summaries/dates/outcomes and a separate ledger tab, load full history only on selection, retain evidence links, and MUST NOT reopen or queue work.
  {S1:L627}

- [A] 15.2.7. Settings MUST expose Workspace, profiles/defaults/capability assignments, compatibility/authentication diagnostics, searchable Skills metadata/details, supported settings, and human-only custom instructions, with privileged settings distinct and busy controls disabled.
  {S1:L628}

- [A] 15.2.8. Help MUST offer searchable maintained guidance, walkthroughs, workflow/authorization, commands, locations, examples, troubleshooting/recovery/limits, and contextual stable links.
  {S1:L629}

## 15.3. Current request tabs

- [A] 15.3.1. Current request MUST have Input and clarification, Analysis, Plan, Implementation, Verification and documentation, and Outcome tabs.
  {S1:L637-644}

- [A] 15.3.2. Input and clarification MUST show inputs/attachments, draft/submitted differences, Save/Clarify, canonical interpretation, questionnaires and assignments, requestor preview/download/intake/review, amendments/history, round results, and the pending submission set with busy-state restrictions.
  {S1:L639}

- [A] 15.3.3. Analysis MUST show repeatable Analyze, progress, assessment, question catalog, optional supporting analysis, and explicit include/defer/investigate selections without a separate Plan command.
  {S1:L640}

- [A] 15.3.4. Plan MUST show revision, interpretation/workspace sources, ordered folder-qualified tasks, tests/docs, differences, approval, and missing/read-only/unreconciled blockers; approval alone MUST NOT execute.
  {S1:L641}

- [A] 15.3.5. Implementation MUST expose Implement, Implement directly, Resume, Stop, sequential progress, events, file evidence, logs, and summaries with a clear explanation of direct-mode limits.
  {S1:L642}

- [A] 15.3.6. Verification and documentation MUST show required results, checked content versions and folder identities, failed/unexecuted checks, repair attempts, documentation increment/applied changes/gaps, reconciliation, and evidence without accept-failure shortcuts.
  {S1:L643, S3:section "Accepted policy"}

- [A] 15.3.7. Outcome MUST show fulfillment, unmet gates, defects, and summary with distinct idle cancelled/rejected/successful closure, Ready to close retaining the open slot, and current-gate revalidation before archival.
  {S1:L644}

## 15.4. Action clarity, conflicts, and execution status

- [A] 15.4.1. The portal MUST retain a product/request/phase/execution/profile header with empty/setup states and prominent idle next actions, visible ownership/disabled reasons while busy, and clarification waiting/readiness distinctions without automatic stage advancement.
  {S1:L646}

- [A] 15.4.2. Human-facing pages MUST use ordinary language with IDs, hashes, and technical evidence available on demand.
  {S1:L646}

- [A] 15.4.3. Save, upload, submit/run, Stop, and closure MUST remain visibly distinct; combined Import answers and clarify MUST clearly disclose its execution effect and unavailable actions MUST explain the specific cause.
  {S1:L648}

- [A] 15.4.4. Revision conflicts MUST display competing changes and explicit resolution without overwrites; live events MUST be sanitized and routine progress understandable without raw-log inspection.
  {S1:L650}

- [A] 15.4.5. Handoff UI MUST distinguish prepared/reserved, evidenced external running, Stop requested, awaiting confirmation, reconciliation, and released states, exposing only the narrow Stop-release flow while reserved.
  {S1:L654}

## 15.5. Browser and content protection

- [A] 15.5.1. The portal MUST protect against traversal, link escapes, arbitrary filesystem access, cross-origin writes, and active untrusted rendering; product HTML/scripts/hooks/attachments MUST NOT execute.
  {S1:L656}

- [A] 15.5.2. The portal MUST NOT expose generic arbitrary-command execution or retain credential values in configuration, tracked files, outputs, or logs.
  {S1:L658}

# 16. Installation, commands, and user guidance

## 16.1. Installation, upgrades, and preservation

- [A] 16.1.1. AIH installation and build work MUST preserve existing product content and inspect applicable workspace and host instructions first.
  {S1:L12}

- [A] 16.1.2. Installation and repeated initialization MUST preserve existing files and human content, make initialized templates product-owned, and MUST NOT silently merge incompatible schemas.
  {S1:L701}

- [A] 16.1.3. Host integration MUST offer a short entry-point snippet without replacing existing agent instructions; direct operation MUST work without adding integration files.
  {S1:L703}

- [A] 16.1.4. Upgrades MUST validate incoming version/core and installed modifications, preserve product content, current workspace configuration, and historical request records, identify migrations, and support recoverable replacement without moving home or installing duplicate cores in added roots.
  {S1:L705, S3:section "Accepted policy"}

- [A] 16.1.5. Installation, upgrade, migration, rollback, and cleanup MUST stay in currently authorized writable roots including indirect effects; former membership MUST NOT authorize recovery writes, and artifacts MUST NOT be externally published or assigned invented release URLs.
  {S1:L705}

## 16.2. Menu, startup, and command discovery

- [A] 16.2.1. Users MUST have a shared terminal menu with Open portal, status, profile checks, Workspace settings, initialization/reverse engineering, validation, inspect/resume, help, Exit, and Stop-only operational choices while busy.
  {S1:L664-668}

- [A] 16.2.2. Startup MUST support direct Windows/Linux Python commands and actionable missing-runtime guidance without automatic installation or universal double-click claims.
  {S1:L666}

- [A] 16.2.3. Startup MUST resolve home independently of current directory, handle spaces/special characters, deduplicate portal/worker launches, and MUST NOT start product work merely by opening menu/help or silently cancel/close on menu Exit.
  {S1:L670}

- [A] 16.2.4. The CLI MUST make installation, workspace administration, initialization, inventory/reverse engineering, helper discovery, validation, skills, profiles, menu, portal, help, lifecycle, form/import/amendment exchange, Q&A, handoff/release, and upgrade/migration operations discoverable with consistent arguments and per-command help.
  {S1:L682-699}

## 16.3. Quick start and shared help

- [A] 16.3.1. The quick start MUST document purpose, prerequisites, local installation, platform/direct startup, first-run baseline, profiles, workspace/home/access, basic and direct workflows, Q&A, troubleshooting, and help.
  {S1:L674}

- [A] 16.3.2. The detailed guide MUST cover all delivered lifecycle, requestor exchange, amendments, authorization, tests/defects/budgets, documentation, profiles/skills/instructions, recovery/history, workspace scope/reconciliation, confinement, redaction, standalone use, maintenance, retention, and limitations, with realistic multi-folder recovery examples.
  {S1:L676, S1:L787-789}

- [A] 16.3.3. Shared help MUST support local navigation/search before initialization/authentication without an agent run, use stable valid installed-version anchors, and MUST NOT modify the core during ordinary reading.
  {S1:L678}

# 17. Delivery validation and reporting

- [A] 17.1. A real Codex CLI smoke test MUST run when installed, authenticated, and permitted in a compatible isolated confined fixture; absent prerequisites MUST be reported as not live-tested, and multi-root live support MUST NOT be inferred from single-root execution.
  {S1:L777}

- [A] 17.2. Delivery validation MUST include a rendered portal walkthrough of primary screens and Workspace settings and distinguish automated checks, real agent execution, browser review, tested platforms, and actual storage assumptions.
  {S1:L779}

- [A] 17.3. Delivery MUST demonstrate the full baseline-to-explicit-successful-closure workflow with iterative clarification/requestor exchange/amendments/Analysis, sequential implementation, full tests, and applied documentation, plus the specified alternate/recovery and multi-root cases as labeled synthetic fixtures.
  {S1:L781}

- [A] 17.4. Delivery MUST include the working core, conventions/templates, all eight complete standalone skills and catalogs, CLI/menu/optional launchers, complete portal, tests/fixtures including requestor exchanges and amendment history, quick start, and detailed shared help.
  {S1:L785}

- [A] 17.5. The final delivery report MUST trace major requirements to implementation and actual evidence, state exact installation/startup/first-use commands, tested platforms/real Codex execution/failures/missing checks/limits, and MUST NOT equate unit-test success with full verification or silently reduce scope.
  {S1:L791-793}

# Referenced documents

- **D1:** [Documentation organization](extensions/architecture/documentation-organization.md) — architecture
- **D2:** [Documentation catalog contract](extensions/interface-contract/documentation-catalog.md) — interface-contract
- **D3:** [Documentation extension types](extensions/data-dictionary/document-types.yaml) — data-dictionary
- **D4:** [Request documentation update flow](extensions/processing-flow/request-documentation-update.md) — processing-flow

# Sources

- **S1:** `sources/AIH_Build_Prompt_v20260922_173409Z.md`
- **S2:** `sources/documentation-evolution.md`

- **S3:** `sources/workspace-administration-20260927.md` — accepted clarification; supersedes conflicting earlier workspace policy.
