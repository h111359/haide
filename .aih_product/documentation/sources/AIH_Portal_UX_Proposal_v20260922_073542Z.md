# AIH portal: proposed UX and appearance specification

Version: `20260922_073542Z`  
Status: **Proposal for review; not yet incorporated into the build prompt.**  
Baseline: `AIH_Build_Prompt_v20260922_070309Z.md`

This document specifies what the portal displays, how users navigate it, and what its controls do. It preserves the agreed workflow: one open request, no backlog, separate Clarify and repeatable Analyze commands, an automatically generated plan, explicit implementation authorization, sequential tasks, mandatory passing tests, maintained documentation, and an independent read-only question lane.

The accompanying HTML theme demo is an interactive visual example. Its content and runs are simulated; it does not initialize a product, invoke agents, modify files, approve plans, or execute tests. Appearance values below are proposed defaults for confirmation.

## 1. Portal shell and navigation

Use eight permanent navigation entries in this order: **Overview**, **Current request**, **Ask a question**, **Product documentation**, **Runs and recovery**, **History and decisions**, **Settings**, **Help**. Keep Help and Settings accessible during initialization and failures.

The persistent header contains product display name; a compact current-request reference or “No open request”; phase; execution state; selected/effective agent profile; and a **Help for this page** link. Show initialization or maintenance as its own labeled operation, not as a change-request phase. Product root, installed version, internal IDs, and fingerprints belong in an expandable **Details** area.

The desktop sidebar remains visible. On narrow screens, **Open navigation** opens an accessible drawer; choosing a destination or pressing Escape closes it and restores predictable focus. The header and action bar must not conceal focused fields. Tables may scroll inside labeled regions; forms and ordinary text must reflow.

### Navigation contract

| Destination | Suggested route | Entry and return behavior |
|---|---|---|
| Overview | `/` | Product-level overview; its cards link directly to the relevant tab or operation. |
| Current request | `/request/{id}/{tab}` | Six tabs retain their selected tab, expanded details, and filters during the session. With no request, show the new-request draft surface. |
| Ask a question | `/questions` and `/questions/{id}` | Existing answer links open that answer, never resubmit the question. |
| Documentation | `/documentation/{node-id}` | Stable node IDs survive tree restructuring. Breadcrumbs identify structural ancestors. |
| Runs | `/runs/{run-id}` | Deep links preserve the run and segment; no side effect on opening. |
| History | `/history/requests/{id}` or `/history/ledger/{event-id}` | Closed records are read-only historical views. |
| Settings | `/settings/{section}` | Direct links select Profiles, Skills, Product, Instructions, or Appearance. |
| Help | `/help/{section-id}` | Stable anchors, searchable guide; a return link leads to the originating screen. |

Browser Back/Forward restores navigation and filters without repeating operations. Reload reconciles operation IDs and state instead of launching workers. Request, task, defect, question, run, document, and ledger links resolve by stable identity, not arbitrary filesystem paths. Unavailable targets show “This item is unavailable” with the recorded reference and a parent-page link; they must not silently show a different item.

Every editable surface shows **Unsaved changes**, **Saved draft**, or **Submitted revision …**. On navigation with unsaved edits, offer **Save draft and leave**, **Discard unsaved edits**, and **Keep editing**. Leaving or saving never submits or runs work. Switching read-only tabs does not show a needless confirmation. Form drafts must not be discarded by incoming live events.

## 2. Shared control and feedback contracts

Every action uses the same validated Python operation as the CLI. Availability comes from server state and is rechecked on invocation. A client-side disabled button is not enforcement. State-changing actions include revision and idempotency identifiers. An unavailable action has a visible explanation next to it, usable without hover.

| Shared control | Preconditions and effect | Feedback and navigation |
|---|---|---|
| **Save draft** | Valid local fields; optimistic revision check. Persists editable content only. | “Draft saved. Nothing has been submitted or started.” Stay in place; show revision/time. |
| **Discard unsaved edits** | Local changes exist. Restore the last saved version; never alter a submitted record. | Name the discarded local draft; remain on the current page unless invoked while leaving. |
| **Cancel** | A dialog/editor is open. Close it without applying its pending selections. | Return focus to its opener. This never means stop a running operation. |
| **View details / View evidence** | Authorized stored reference exists. Read safe content or metadata. | Open an inline panel or the relevant stable detail route; retain a return link. |
| **Download file** | Stored artifact is permitted for download. | Download exact identified revision, with a safe filename. Never execute attachments. |
| **Compare revisions** | Two revisions are selected. Compute/show a read-only diff. | Label old/new versions; no inferred approval or overwrite. |
| **Retry** | Previous action failed and its outcome has been reconciled. | Reuse or supersede the identified operation safely; if success is uncertain, offer inspection instead of blind repetition. |
| **Refresh status** | Page has observable state. | Read current status only; never refresh documentation, rerun tests, or invoke an agent. |
| **Help for this action** | Applicable guide anchor is installed. | Open that guide section; returning restores the prior view. |

Run actions require saved valid inputs. If unsaved content exists, the action explains “Save these edits before submitting.” The explicit action snapshots the latest relevant saved content and identifies its submitted revision. Display **Submitted**, **Pending checkpoint**, **Running**, **Waiting for answers**, **Stopped**, **Failed**, or **Finished** according to evidence. A click alone does not justify “Running.”

For a pending amendment show: “Submission S… is waiting for a safe checkpoint. Run R… is still using submission S….” Do not create a future-request queue. Repeated clicks return the existing submission/run reference. Concurrent revision changes require reassessment before launch.

Success feedback is specific: “Plan revision 4 approved” rather than “Done.” Routine notices are unobtrusive; consequential blockers remain visible until resolved. Errors include the failed operation, whether anything was saved or started, a plain-language reason, and the applicable recovery action. Do not print credentials or unsanitized output.

### Conflicts and accessibility

A conflict panel shows **Your draft**, **Saved version**, and a readable diff, with revision labels. Offer **Use saved version**, **Continue editing a merged draft**, and **Download my draft**. Saving a merged result performs a fresh revision check; no generic force-overwrite control is provided.

All form fields have persistent labels, required/optional indicators, instructions, and field-linked errors. Provide keyboard access, visible focus, semantic headings, labeled dialogs/tabs/tables, and concise live announcements. Never rely only on color for state. Respect reduced-motion preferences. New live events must not steal focus or scroll a user away from inspected evidence.

## 3. Overview

**Page introduction:** “Your product, current work, and next action.”

Display a main **Current work** card with request title/ID, scope summary, phase, worker status, current task, last update, selected agent, and a single relevant next action. Separate cards show **Tests and verification**, **Documentation**, **Latest response**, and **Setup or maintenance** when applicable. Available token telemetry may appear in a compact usage panel; use “Unavailable” when no count is supplied.

Tests show passed/failed/unexecuted required counts and freshness, not just a green process exit. Documentation shows current/stale/unknown coverage and outstanding increments. The latest-response card includes its submission/run references and a link to response history.

| Control | Behavior |
|---|---|
| **Start request** | Available only without an open request and without incompatible initialization/maintenance ownership. Opens the request draft; it does not run the agent. The first explicit request action creates the open request record atomically. |
| **Continue request** | Opens the active request's relevant tab; does not resume execution. |
| **Answer questions** | Opens the blocking questionnaire in Input and clarification or Analysis. |
| **Review plan** | Opens the current Plan tab without approving it. |
| **View run** | Opens the exact operation in Runs and recovery. |
| **Read response** | Opens the current response panel; history remains accessible. |
| **Review failures / Review documentation** | Opens the corresponding Verification and documentation section. |

Use explicit empty copy: “No change request is open. Start a request to change the product, or ask a read-only question.” A blocked card states the reason and “Change work is paused. Read-only questions remain available.” Do not offer unrelated implementation work.

### First-start operation

When product state is absent, show automatic setup progress: **Initialize files → Inventory product → Generate documentation → Validate documentation**. Display completed steps, current step, source count where known, gaps, and operation identity. Do not invent percentages when total work is unknown.

Missing-profile copy: “Product files are initialized. Documentation generation is waiting for a configured, authenticated agent.” **Configure agent** opens Settings/Profiles; **Prepare manual handoff** opens the handoff flow; **Resume setup** explicitly resumes the existing operation after prerequisites pass. Invalid existing state shows its errors with **View diagnostics**, not a destructive “start fresh” button. Documentation generation is never labeled proof that the product works.

## 4. Current request

The page header contains title, ID, open status, current phase, submitted revision, plan approval state, and a compact blocker summary. Tabs are **Input and clarification**, **Analysis**, **Plan**, **Implementation**, **Verification and documentation**, and **Outcome**. Tabs remain navigable even when their actions are unavailable; explain which prerequisite is missing.

### 4.1 Input and clarification

**Introduction:** “Describe what must change and why. Clarification establishes requirements; it does not select an implementation.”

Fields: request title; Markdown input editor; optional attachment picker; attachment names/types/sizes; saved/submitted state. Show a safe Markdown preview, canonical interpretation with provenance, current response, and submission history. File attachment limits and supported formats appear beside the picker. User-provided executable attachments are never run.

Questionnaires display ID, context, single/multiple-choice rule, unchecked recommended option with rationale, free-text answer/modification, whether consequential or optional, and draft/submitted status. The free-text alternative is always available. Invalid multiple selections receive a field error; do not guess.

| Control | Behavior |
|---|---|
| **Add attachments** | Adds selected allowed files to the draft using a validated upload; detects unsupported/oversized files. |
| **Remove from draft** | Removes only the draft reference. Submitted snapshots remain intact. |
| **Preview / Edit** | Switches presentation of the same draft; neither saves nor submits. |
| **Save draft** | Saves input and questionnaire edits with revision checks. |
| **Clarify** | Submits saved input/answers; creates or updates the sole request; starts or schedules safe adoption of requirements clarification. Show submission ID and progress. |
| **View interpretation** | Opens the canonical definition, accepted versus inferred requirements, and source references. |
| **Compare submissions / Response history** | Opens selected immutable revisions without reactivating them. |

If a blocking question arose in Analysis, explain that submitted answers may be applied by **Analyze**; do not force a redundant clarification run. Editing text in the interpretation is not an alternative untracked requirement source: amendments enter through explicit input/submission.

### 4.2 Analysis

**Introduction:** “Analyze applies submitted answers and amendments, assesses the solution, and creates or revises the implementation plan.”

Display analysis revision, its source interpretation/instructions/documentation versions, last result, and outstanding consequential questions. Provide separately labeled sections or file links for interpretation, questions, solution assessment, unrelated issues, plan, and documentation increment; optional impact, risks/decisions, and verification strategy appear when present.

**Analyze** is the sole analysis command. It snapshots saved answers/amendments and continues from persisted state. It may ask more questions, revise artifacts, or report an unchanged valid plan; it never implements. While a writer is active, show safe-checkpoint behavior instead of launching a second writer. There is no **Generate plan** or **Plan** command.

The unrelated-issues table shows defect ID, summary, confirmed/suspected status, affected components, evidence, impact on required tests, current disposition, and known-defect link. Each row has a draft choice: **Include in this request**, **Defer**, or **Investigate further**, plus optional rationale. **Save selections** saves drafts only; **Analyze** submits them and updates scope/plan as needed. Included material scope changes invalidate affected approval. Unknown issues do not become confirmed defects merely because an agent suspects them.

For a deferred failing defect, display: “Deferred defect D… still fails a required test. This request cannot complete until that failure is resolved.” Provide **Review disposition** and **View failing test**, never an accept-failure action.

**Review generated plan** navigates to Plan after a ready result. **View analysis changes** displays revisions. **Answer question** opens its authoritative questionnaire, not a duplicate editable answer field in the question catalog.

### 4.3 Plan

**Introduction:** “Review the proposed implementation. Approval records your agreement; it does not start work.”

Show plan revision, approval status, source scope/revisions, differences from the preceding plan, and concise design decisions. Each ordered task displays stable ID, sequence, outcome, requirement links, create/modify/move/delete operations, affected paths, dependencies, completion criteria, and evidence references. Required test creation/execution, documentation increment, and results-recording tasks must be visible.

**Expand task / Collapse task** changes only display. **Compare plan revisions** shows changes including retained completed tasks and rework. **Review required tests** and **Review documentation increment** navigate to their detailed records.

**Approve plan** requires a valid current plan, no unresolved consequential prerequisite, and reviewed current scope. The approval surface identifies the exact revision and states “Approve plan revision … for scope revision …. This does not start implementation.” The action records human approval and remains on Plan, offering **Go to implementation**. An outdated view returns a conflict rather than approving a replacement revision. Do not add a second generic confirmation after this explicit approval action.

A direct-generated plan displays **Direct implementation authorized**, with its submitted scope and action evidence, rather than “Human-approved.” A stale plan says why approval is no longer valid and links to **Analyze**. This proposal omits a combined Approve-and-implement button to keep the two actions clear.

### 4.4 Implementation

**Introduction:** “Execute the authorized plan and inspect what happened.”

Show selected effective profile, scope/plan revision, applicable instructions, next task, sequence progress, run/segment IDs, current checkpoint, and file-change evidence. Task states include pending, running, completed, blocked, failed, and requiring rework; distinguish task evidence from worker exit status. Offer a compact live event timeline plus **View full log**, **View results summary**, and **View file changes**.

| Control | Preconditions, effect, and feedback |
|---|---|
| **Implement** | Current approved plan, valid submitted scope/instructions, no blocker or conflicting writer. Submits saved amendments, reconciles inputs, then starts only if authorization remains valid. Material changes return to Analysis/approval instead of starting stale work. |
| **Implement directly** | Explicit submitted scope and required prerequisites; no conflicting writer. Clearly state “Generate the required task plan, then implement without a separate analysis command or plan approval. Tests, documentation, evidence, and defect scope decisions remain required.” This explicit action grants the scoped shortcut, not unrestricted authority. |
| **Resume** | Existing interrupted/stopped/paused run; termination/ownership reconciled and blockers addressed. Snapshots relevant saved inputs, checks completed actions and evidence, then continues only what remains authorized. Show native resume versus a new segment accurately. |
| **Stop execution** | Live owned process exists. Request safe cancellation; immediately show “Stop requested. Waiting for process termination.” Change to stopped only after confirmation. Keep the request open. |
| **Prepare manual handoff** | Automated prerequisites unavailable or the user chooses external execution. Create identified instructions/evidence expectations and open the handoff view; do not mark work running. |

A crash shows last durable checkpoint, known completed actions, uncertain actions, and available partial summary. A reconstructed summary carries that label. An unconfirmed child process prevents another writer; link to recovery diagnostics. Live-log autoscroll can be paused without stopping execution.

### 4.5 Verification and documentation

**Introduction:** “Completion requires passing required tests, current evidence, and applied documentation changes.”

The verification table contains suite/check name, requirement/task mapping, required or explicitly inapplicable status, result, run timestamp, checked-content reference, freshness, failure summary, and evidence. Distinguish failed, not run, interrupted, passed-but-stale, and current passed results. Show complete maintained suite coverage and repair attempts.

The documentation table contains increment item ID, target document/section, reason and source task, planned change, applied revision, verification status, and unresolved gap. Include a justified no-impact finding where applicable; do not replace it with a silent empty table.

**View failure**, **View test evidence**, **Compare checked content**, **Open document**, and **View documentation change** are read-only linked detail actions. **Run required tests** invokes the registered complete suite through its controlled worker, only when authorized, no conflicting writer exists, and its supported environmental prerequisites hold. It creates evidence, not permission to repair unrelated defects. **Validate documentation** runs deterministic validation and reports semantic review gaps separately; it does not silently author missing content.

**Continue authorized repairs** routes to Implementation/Resume. A failure outside scope routes to Analysis defect disposition. Documentation requiring semantic changes follows the active request's authorized tasks. There is no ignore-failure, mark-passed, or accept-outdated-documents shortcut.

### 4.6 Outcome

Show implementation results summary, requirement fulfillment, full-suite status/freshness, documentation status, evidence completeness, unresolved defects, and separate integration/deployment milestones. Display every unmet completion gate with a link to its source. A process result such as “Exited successfully” must never substitute for these checks.

**Complete request** is available only after server-validated gates pass. It finalizes evidence, archives the complete record transactionally, updates the catalog/ledger, and navigates to the closed historical summary. If another change invalidates a gate, retain the open request and explain it.

**Close as cancelled** and **Close as rejected** open a labeled outcome form with a reason, current partial changes, uncertain operations, and unresolved items. Copy: “Close this request without successful completion. Existing product changes will remain; nothing is automatically rolled back.” Require no live/uncertain writer before final archival. **Confirm closure** records the chosen non-success outcome; **Keep request open** cancels the form. These actions do not bypass safe process termination.

## 5. Ask a question

**Introduction:** “Ask about the product without changing it. Answers are saved separately from change work.”

Fields: question text; optional title; optional reference to the current or a historical request; attachments; profile override if supported by the configured policy. Show saved/submitted state, observed-source version, answer status, available files, and the question history list. Expose sources and uncertainties alongside the answer.

**Save question draft** uses the shared save contract. **Ask** explicitly submits the saved question, creates its own ID, and starts a permitted read-only run; it never creates or resumes a change request. If read-only execution cannot be enforced, show the precise limitation and the supported constrained/manual option before execution. A blocked change request does not disable this lane.

**Stop question run** stops only that Q&A execution. **Open answer**, **Download answer**, and **View sources** read existing records. **New question** opens a fresh draft after handling unsaved edits, without deleting history. A follow-up can reference a prior answer but receives its own submitted identity.

If the ask requests product modification, answer: “This requires a change request. No product changes were made.” Provide **Open current request** or **Start request**, according to state, without silently copying/submitting scope. An answer discovered during concurrent writes warns when sources changed or represent a mixed observation. Q&A findings are not automatically written into durable product documentation.

## 6. Product documentation

**Introduction:** “Current product knowledge, evidence, and known gaps.”

Use a compact tree navigation panel and content pane. Catalog entries show title, scope, when to read, applicability, and child count. Leaf views show content, stable ID, source/provenance, updated date, observed/inferred/approved distinctions, content fingerprints on demand, verification status, and related requests/decisions. Cross-references are identified separately from structural parents.

Search fields: query; category; applicability; freshness; content versus metadata scope. Results show snippets and source nodes, not the full corpus. **Search** performs a local index/query operation; **Clear filters** resets filters only. **Expand catalog**, breadcrumbs, and **Open reference** navigate progressively.

Provide a **Known defects** view with confirmed/suspected distinction, symptoms, reproduction evidence, component, current status, workaround if evidenced, and origin. Filters never create a backlog or authorize repair. **Review in current request** opens the linked issue/disposition surface or the input area for explicit amendment; it must not include a defect silently.

**Refresh documentation** opens an operation form with initial/incremental mode as applicable, detected source changes, bounded source selection, owning system operation/request, effective profile, and expected documentation-only effects. **Start reverse engineering** commits the explicit operation; **Cancel** leaves it unstarted. Full reinspection is a deliberate choice, not the default for every refresh.

With no open request, use a standalone maintenance operation. With an open request, refresh must be an authorized task belonging to that request and must respect its blocker/one-writer rules. Unavailable copy: “Documentation maintenance must be part of the open request. Review its plan before starting.” A blocked request cannot be bypassed through this page. Setup-pending work links to **Resume setup**. Results link to provenance, changed documents, gaps, and the operation summary; generated prose is not verified behavior.

## 7. Runs and recovery

List runs with type (change work, question, setup, maintenance), owner, action, profile, start/end, process status, task outcome, and checkpoint. Filters include type, owner, status, and date. Default to active/interrupted operations; **Load older runs** pages metadata without loading all logs.

Run detail contains segment timeline, sanitized event list, completed/current tasks, artifact links, content/instruction references, exit status, timeout/cancellation reason, checkpoints, and results summary. Usage fields display actual supplied token counts by segment and available totals; absence says “Unavailable.” Do not combine unlike/missing measures into an invented total.

**Pause log scrolling / Follow latest** controls viewing only. **Filter events** changes severity/category visibility and shows omitted counts. **Download sanitized log** exports the identified record. **View checkpoint** opens recorded progress, not private reasoning.

**Stop execution** and **Resume** use the shared owning-operation contracts. **Inspect recovery** performs diagnostics and outcome reconciliation; show completed, incomplete, and uncertain actions separately. **Recover stale lock** is available only through the validated recovery operation after checking process identity/ownership; never treat a lock's age or deletion as proof of termination.

Manual handoff displays “Prepared for external execution; no execution confirmed.” **Copy instructions** copies the exact identified handoff. **Download handoff** saves instructions and expected artifacts. **Reconcile returned evidence** validates user-selected evidence references and inspected content; a textual success claim alone cannot satisfy completion. Unsupported files or inconsistent scope produce actionable errors. The portal never executes uploaded scripts.

## 8. History and decisions

Tabs: **Closed requests** and **Changes and decisions**. Closed-request columns are ID, title, concise scope/result, outcome, opened/closed dates, and significant document/decision links. Filters include outcome, date, and search. **Open record** loads that record on demand; display a persistent “Historical record — read only” label.

Historical detail shows interpretation, final plan, response history, summaries, tests as they were checked, documentation increment, defects, runs, and closure evidence. Clearly distinguish historical passing evidence from current product verification. **Compare revisions**, **Open evidence**, and **Download artifact** are read-only controls. There is no Reopen, Queue, or Implement button on history.

The ledger lists event type, time, concise description, actor/source, request/operation, affected artifacts, and supersession links. **Open event** shows immutable detail. **View superseding event** follows a correction; the original remains readable. Search/filter actions do not rewrite the generated catalog. A discrepancy directs the user to a current explicit workflow, not direct historical editing.

## 9. Settings

Use sections **Agent profiles**, **Skills**, **Product**, **Custom instructions**, and **Appearance**. Each editor states its storage target, effective boundary, revision, and validation status. Workflow-related changes affect subsequent runs or controlled segments; cosmetic changes apply immediately after saving without changing approvals or verification.

### Agent profiles

List name/ID, adapter, configured executable reference, detected CLI version, compatibility, authentication diagnostic result, and last check. The editor contains only adapter-schema fields: model/settings, timeout, supported permission settings, and credential environment-variable references. Never request or show actual credential values.

**Add profile** opens a blank validated editor. **Edit profile** opens the chosen version. **Save profile** persists validated settings, without diagnosing or launching work implicitly. **Run diagnostics** checks the selected profile without product work; reports authentication presence separately from verified access. **Set as default** records the selected valid profile; **Save capability assignments** updates explicit capability mappings. Show resulting selection precedence.

Keep executable paths and permission settings in a visually separate **Privileged local settings** form. Only deliberate local human administration may change them. **Save local executable settings** validates and records that action; product content must not populate or submit it. Do not offer automatic install/upgrade or fallback to another agent. Profile deletion, if offered, is blocked while referenced unless assignments are explicitly reassigned; historical run records retain their effective settings.

### Skills and product settings

Skills list metadata, source/version, compatibility, enabled state, and diagnostics. **Enable / Disable** changes the declarative setting for subsequent execution boundaries, without installing anything or loading/executing a skill body. **Validate skills** runs deterministic checks. Unsupported or duplicate skills show why they cannot be selected.

Product settings expose only supported fields: documentation tree limits, retention, supported runtime/portal preferences, and other schema-defined options. **Save settings** validates and revision-checks the group; dependency-changing settings explain what will require revalidation. No arbitrary command template or unrestricted arguments field exists.

### Custom instructions

List human-owned instruction files with revision/date. The editor has filename, Markdown content, safe preview, and explicit behavioral-supplement/override guidance. **Save my edits** records a deliberate human edit with conflict checking and its future execution boundary. **View agent suggestion** shows an output separately; it cannot apply itself. Agent operations never invoke this human editor or silently translate a suggestion into instructions.

## 10. Appearance and font sizes

Appearance settings are proposed as declarative `appearance` values in `.aih_product/config.yaml`. They do not affect scope, plan authorization, evidence freshness, or agent behavior. Save with normal conflict checks. Built-in themes remain immutable core assets; customization creates a product-owned named preset containing validated values only.

| Preset | Palette direction | Predefined font roles |
|---|---|---|
| **Clear** | Light neutral surfaces, dark text, blue action accent | Segoe UI/system sans for headings and body; system monospace for code |
| **Midnight** | Dark blue-gray surfaces, light text, brighter blue accent | Same sans and monospace families as Clear |
| **Warm** | Warm off-white surfaces, brown-gray text, restrained earthy accent | Georgia/serif headings; system sans body; system monospace code |
| **Contrast** | Near-black surfaces, white text, strong distinct accents/borders | Arial/sans for headings and body; system monospace code |

Fields: appearance mode (**Use system**, **Choose theme**); selected theme; custom preset name; heading/body/code font presets; base text size; and editable semantic colors. System mode chooses Clear or Midnight from browser light/dark preference. Selecting a named theme selects explicit mode. **Customize theme** duplicates the current effective preset, then opens its editor; it does not rewrite the built-in.

Proposed semantic colors include page background, surface, raised surface, primary/secondary text, border, primary action and action text, link, focus ring, success, warning, and error foreground/background pairs. Derived hover/selected/disabled states must also be checked. Accept validated color values and allowed installed-font stacks, not CSS, font URLs, HTML, scripts, or unrestricted styles.

Proposed base-size control: nominal **14–22**, default **16**, with a slider and numeric input. Express resulting sizes relatively so browser zoom and user settings still work. Headings, labels, controls, navigation, and table text scale together with `rem`/relative units; code uses a readable relative ratio. Do not make controls inaccessible by fixing their height. User resizing must survive page navigation.

**Preview changes** applies the unsaved theme locally to the preview area. **Save appearance** persists the valid preset/selection and applies it throughout the real portal; show “Appearance saved. Workflow state is unchanged.” **Discard preview** restores the saved appearance. **Reset draft to preset** resets unsaved values; the user still chooses Save. **Delete custom theme** is available only for custom presets and requires selection of a replacement if active.

Display readable controls, links, badges, input errors, tables, disabled actions, code, and focus states in the live preview. Reject a saved theme that fails the proposed minimum text contrast checks (4.5:1 ordinary text; 3:1 large text), and require distinguishable control/focus boundaries. Show which token pair fails and preserve the draft for correction. This is automated validation of selected properties, not a blanket accessibility claim.

The standalone HTML demo stores appearance choices only in that browser when storage is available, with a visible reset option and graceful in-memory fallback. It must state that these demo preferences do not update `.aih_product/config.yaml`. Embed CSS/JavaScript and use local font stacks so the demo opens without external requests, a server, or third-party assets.

## 11. Help

**Introduction:** “Learn the workflow and find instructions for your current step.”

Use the maintained `.aih/USER_GUIDE.md` and shared command metadata. Show a guide contents panel, search, current article, breadcrumbs, related topics, and installed guide/core version. Sections cover quick start, initialization, Clarify versus Analyze, approvals, direct implementation, tests/defects, documentation, questions, profiles/skills, human instructions, logs, recovery, history, appearance, and limitations.

**Search help** searches locally without an agent. **Open topic** follows stable anchors. **Copy command** copies the exact platform-specific example, never runs it; allow **Windows / Linux** example selection. **Open quick start** displays `.aih/README.md`; **Back to …** returns to the context that opened help. Broken anchors show a fallback topic and explicit missing-link notice. Help is available before authentication or product initialization and never modifies the immutable core.

## 12. Required UX validation and demo boundaries

Exercise every route, tab, control, disabled reason, conflict, and critical empty/error state against its contract. Verify keyboard navigation, focus restoration, zoom/reflow, large configured fonts, reduced motion, readable theme states, and safe rendering. Check first-start progress, no-profile setup, direct implementation, approval staleness, blocked-work Q&A, failing deferred defects, termination uncertainty, manual handoff, and historical read-only views.

The implementation must maintain an action catalog mapping each user-facing button to its Python operation, inputs, prerequisites, effects, feedback, destination, and help anchor. Recurring controls may reference the shared contracts rather than duplicating logic. Test transitions and meaningful user journeys; screenshots alone do not establish behavior.

The review HTML is a theme/component and navigation demonstration, not an implementation of these backend contracts. Simulated actions must be labeled as such and must never announce actual saved product files, successful tests, approved plans, or completed work. The final portal must implement and verify the real contracts separately.


## 13. Accompanying review artifact

The companion file is `AIH_Portal_Theme_Demo_v20260922_073542Z.html`. Open it in a browser to explore the eight page areas, six request tabs, example workflow states, four theme presets, a custom palette, and font scaling. This is a deliberately bounded demonstration of the proposed design; attachments, source inspection, real persistence, agent execution, and recovery operations remain specified here rather than implemented in the demo.

Validation performed for this draft: embedded JavaScript syntax; template execution across 120 page/state combinations; action and label mappings; approval/closure safeguards; selected preset color-pair checks; and absence of external resource dependencies. These were static and template-level checks. A rendered browser review was unavailable in the authoring environment, so layout, actual focus behavior, and cross-browser rendering remain to be checked. No claim of complete accessibility conformance is made.
