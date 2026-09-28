# Contents

- [1. Portal navigation and route adoption](#1-portal-navigation-and-route-adoption)
- [2. Editing, submission, and shared controls](#2-editing-submission-and-shared-controls)
  - [2.1. Draft preservation, conflicts, and submission boundaries](#21-draft-preservation-conflicts-and-submission-boundaries)
  - [2.2. Evidence viewing, feedback, and operational controls](#22-evidence-viewing-feedback-and-operational-controls)
- [3. Workflow screens and request outcomes](#3-workflow-screens-and-request-outcomes)
- [4. Documentation, history, and help interactions](#4-documentation-history-and-help-interactions)
- [5. Settings and appearance adoption](#5-settings-and-appearance-adoption)
- [6. Prototype deliverable and UX validation scope](#6-prototype-deliverable-and-ux-validation-scope)
- [7. External skill specification reference](#7-external-skill-specification-reference)
- [Sources](#sources)

# 1. Portal navigation and route adoption

- 1.1. Adoption of the proposal-only shell/navigation details is unconfirmed: fixed desktop sidebar, accessible narrow-screen drawer with Escape/focus behavior, non-obscured fields, labeled scroll regions, reflow, header page-help/expandable details, session tab/filter/detail restoration, Back/Forward behavior, unavailable-target fallback, and unsaved-edit navigation choices. The build confirms eight pages and six tabs but does not adopt every proposed interaction.
  {S1:L4-9, S1:L13-35, S2:L620-646}
  Resolution needed: Identify which additional shell, navigation, route, and draft-preservation details are approved.

- 1.2. The proposed Overview route pattern `/` has no supplied acceptance evidence.
  {S1:L4-9, S1:L23}
  Resolution needed: Confirm the Overview route pattern or provide the intended replacement.

- 1.3. The proposed Current request route pattern `/request/{id}/{tab}` has no supplied acceptance evidence.
  {S1:L4-9, S1:L24}
  Resolution needed: Confirm the Current request route pattern or provide the intended replacement.

- 1.4. The proposed Questions route pattern `/questions` and `/questions/{id}` has no supplied acceptance evidence.
  {S1:L4-9, S1:L25}
  Resolution needed: Confirm the Questions route pattern or provide the intended replacement.

- 1.5. The proposed Documentation route pattern `/documentation/{node-id}` has no supplied acceptance evidence.
  {S1:L4-9, S1:L26}
  Resolution needed: Confirm the Documentation route pattern or provide the intended replacement.

- 1.6. The proposed Runs route pattern `/runs/{run-id}` has no supplied acceptance evidence.
  {S1:L4-9, S1:L27}
  Resolution needed: Confirm the Runs route pattern or provide the intended replacement.

- 1.7. The proposed History route pattern `/history/requests/{id}` and `/history/ledger/{event-id}` has no supplied acceptance evidence.
  {S1:L4-9, S1:L28}
  Resolution needed: Confirm the History route pattern or provide the intended replacement.

- 1.8. The proposed Settings route pattern `/settings/{section}` has no supplied acceptance evidence.
  {S1:L4-9, S1:L29}
  Resolution needed: Confirm the Settings route pattern or provide the intended replacement.

- 1.9. The proposed Help route pattern `/help/{section-id}` has no supplied acceptance evidence.
  {S1:L4-9, S1:L30}
  Resolution needed: Confirm the Help route pattern or provide the intended replacement.

# 2. Editing, submission, and shared controls

## 2.1. Draft preservation, conflicts, and submission boundaries

- 2.1.1. The proposed conflict editor and accessibility details lack acceptance: a Your draft/Saved version labeled diff, Use saved version/Continue editing a merged draft/Download my draft choices with a fresh revision check and no force overwrite; persistent field labels and required/optional indicators, field-linked errors, keyboard/focus/semantic/live-announcement support, non-color state cues, reduced motion, and non-disruptive events.
  {S1:L4-9, S1:L58-62}
  Resolution needed: Confirm the proposed conflict-editing and accessibility behaviors.

- 2.1.2. The additional proposed Save draft interaction is not confirmed: valid local fields and a revision check persist editable content only; stay in place and show revision/time with “Draft saved. Nothing has been submitted or started.”.
  {S1:L4-9, S1:L42}
  Resolution needed: Confirm this Save draft interaction as an addition to the settled build workflow.

- 2.1.3. The additional proposed Discard unsaved edits interaction is not confirmed: restore the last saved local draft without changing submissions; name the discarded draft and stay unless this is a navigation departure.
  {S1:L4-9, S1:L43}
  Resolution needed: Confirm this Discard unsaved edits interaction as an addition to the settled build workflow.

- 2.1.4. The additional proposed Cancel interaction is not confirmed: close the pending dialog/editor without applying selections and return focus to its opener; cancellation is not stopping a run.
  {S1:L4-9, S1:L44}
  Resolution needed: Confirm this Cancel interaction as an addition to the settled build workflow.

- 2.1.5. The proposal specifies that incoming live events must not discard form drafts; acceptance of this additional draft-preservation interaction is unconfirmed.
  {S1:L4-9, S1:L34}
  Resolution needed: Confirm the proposed preservation of form drafts during incoming live events.

- 2.1.6. The proposal specifies unsaved-before-run feedback “Save these edits before submitting.” with saved valid input required and submitted revision identified; its exact interaction and copy remain unapproved.
  {S1:L4-9, S1:L52}
  Resolution needed: Confirm the proposed unsaved-before-run interaction and feedback.

- 2.1.7. The proposal describes pending-checkpoint submissions and safe adoption while a writer is active, and the HTML simulates pendingSubmission; the build explicitly rejects busy submissions and queues and adopts new revisions only through a subsequent idle action after a recorded boundary. The proposal is expressly unapproved, so its busy-intake behavior is not a settled alternative.
  {S1:L51-55, S1:L107, S1:L120, S2:L47-49, S2:L162-166, S2:L239, S3:L59-60, S3:L66, S3:L85}
  Resolution needed: Confirm whether to revise the proposal/demo to match the build before adopting their UX.

## 2.2. Evidence viewing, feedback, and operational controls

- 2.2.1. The additional proposed View details / View evidence interaction is not confirmed: open a permitted stable artifact reference inline or by detail route and retain a return link.
  {S1:L4-9, S1:L45}
  Resolution needed: Confirm this View details / View evidence interaction as an addition to the settled build workflow.

- 2.2.2. The additional proposed Download file interaction is not confirmed: download the exact identified permitted artifact revision with a safe filename and never execute attachments.
  {S1:L4-9, S1:L46}
  Resolution needed: Confirm this Download file interaction as an addition to the settled build workflow.

- 2.2.3. The additional proposed Compare revisions interaction is not confirmed: display a read-only old/new labeled diff without inferred approval or overwrite.
  {S1:L4-9, S1:L47}
  Resolution needed: Confirm this Compare revisions interaction as an addition to the settled build workflow.

- 2.2.4. The additional proposed Retry interaction is not confirmed: safely reuse or supersede an identified reconciled failed operation, offering inspection instead of retry when success is uncertain.
  {S1:L4-9, S1:L48}
  Resolution needed: Confirm this Retry interaction as an addition to the settled build workflow.

- 2.2.5. The additional proposed Refresh status interaction is not confirmed: read observable current status only, never documentation refresh, tests, or an agent run.
  {S1:L4-9, S1:L49}
  Resolution needed: Confirm this Refresh status interaction as an addition to the settled build workflow.

- 2.2.6. The proposal additionally requires unavailable-action explanations visible next to the control and usable without hover; this precise feedback presentation is not confirmed by the supplied build acceptance.
  {S1:L4-9, S1:L38}
  Resolution needed: Confirm the proposed visible non-hover unavailable-action explanations.

# 3. Workflow screens and request outcomes

- 3.1. Adoption of proposal-only Overview/setup/input details is unconfirmed: exact card/introduction/empty/blocker text, task/last-update fields, count/freshness presentation, Start versus Continue navigation, step names/source counts/no invented percentages, selected recovery links, title/attachment metadata and draft-only removal, Preview/Edit controls, and comparison/response-history navigation.
  {S1:L64-112, S2:L612-624, S2:L639}
  Resolution needed: Confirm the additional display/copy/control choices without replacing the build’s complete-baseline request gate.

- 3.2. Adoption of proposal-only Analysis/Plan review details is unconfirmed: precise display fields, draft defect rationale and save controls, task expansion, revision/required-test/documentation links, exact revision approval surface without a second confirmation, and omission of combined Approve-and-implement. The build permits a clearly labeled combined action but does not require one.
  {S1:L116-143, S2:L209, S2:L640-641}
  Resolution needed: Confirm approved review interactions and whether to offer the combined action.

- 3.3. The additional proposed implementation and verification UI lacks acceptance: pending/running/completed/blocked/failed/rework task states; compact timeline and full-log/results/file links; suite/check requirement/task mapping, required/inapplicable status, timestamp/version/freshness/failure/evidence fields; increment-item/target/reason/task/planned/applied/verified/gap fields; explicitly authorized Run required tests, deterministic Validate documentation with semantic gaps reported separately, and Continue authorized repairs navigation.
  {S1:L144-166}
  Resolution needed: Confirm the supplementary implementation and verification displays and actions.

- 3.4. The proposal uses Complete request and the HTML uses Close as completed, whereas the build specifies explicit human Close successfully after Ready to close with fresh gate validation.
  {S1:L172, S3:L65, S3:L88, S2:L223, S2:L644}
  Resolution needed: Confirm whether the proposal/demo closure labels should be revised before adopting their UI.

- 3.5. Cancelled/rejected closure forms are proposed with a reason, retained changes, uncertain operations and unresolved items; Confirm closure records that outcome and Keep request open cancels the form without rollback. The build settles unsuccessful closure behavior but does not specify all these form details.
  {S1:L174, S2:L221, S2:L644}
  Resolution needed: Confirm the proposed unsuccessful-closure form and reason field.

- 3.6. Adoption of additional question-lane fields and interactions is unconfirmed: optional title/request reference/profile override, Save question draft, follow-up identities, New question navigation, and exact modification-request copy.
  {S1:L176-186, S2:L174-186, S2:L624}
  Resolution needed: Confirm which proposal-only Q&A interactions supplement the build’s settled read-only lane.

# 4. Documentation, history, and help interactions

- 4.1. Adoption of detailed documentation browsing/refresh design is unconfirmed: category/applicability/freshness/content-versus-metadata filters, snippets and clear filters, known-defect views, refresh form fields and deliberate full reinspection, and exact navigation/copy. The former question about an open-request workspace-reconciliation exception is resolved: the accepted 2026-09-27 clarification permits workspace changes and their documentation review only between requests. The additional UI choices remain unresolved.
  {S1:L188-200, S2:L395-397, S2:L625, S4:section "Consequences"}
  Resolution needed: Confirm the additional documentation UI choices. No open-request workspace-reconciliation exception remains to be adopted.

- 4.2. Adoption of detailed Runs/history interaction design is unconfirmed: run type/owner/date filters, metadata pagination, event filtering/omitted counts, pause/follow log scrolling, exact handoff copy/download/evidence controls, historical filters/detail fields/labels, and ledger supersession navigation. Handoff evidence intake must remain within the build’s reserved Stop/release flow.
  {S1:L201-221, S2:L572, S2:L626-627, S2:L654}
  Resolution needed: Confirm the additional interactions and reconcile standalone evidence-reconciliation wording with that flow.

- 4.3. Additional Help UX is proposed but unapproved: guide contents/search/article/breadcrumbs/related topics/version, local platform-specific Copy command, Windows/Linux selector, quick-start view, return-to-origin, and broken-anchor fallback.
  {S1:L267-274, S2:L629, S2:L674-678}
  Resolution needed: Confirm which controls supplement the build’s settled shared-help requirement.

- 4.4. The additional proposed Help for this action interaction is not confirmed: open an installed relevant guide anchor and restore the prior view on return.
  {S1:L4-9, S1:L50}
  Resolution needed: Confirm this Help for this action interaction as an addition to the settled build workflow.

# 5. Settings and appearance adoption

- 5.1. Adoption of proposal-only Settings detail is unconfirmed: Profiles/Skills/Product/Instructions/Appearance sections, editor storage-target/revision/validation display, separate privileged editor, profile add/edit/default/assignment/delete restrictions, exact instruction editor controls, and immediate cosmetic application. Workspace is required. Its timing is now settled: workspace changes require no open request and no active operation. Other operational settings saves remain prohibited while busy; their proposal-only details remain unresolved.
  {S1:L223-243, S2:L628-635, S4:section "Accepted policy"}
  Resolution needed: Confirm the remaining proposed settings details and their effective boundaries; workspace-change timing is already settled.

- 5.2. Production appearance storage and theme selection are unapproved: the proposal suggests declarative appearance in .aih_product/config.yaml, immutable built-ins and named product-owned custom presets, Use system/Clear-or-Midnight selection, theme duplication, and allowed heading/body/code font presets; the demo stores only browser preferences and offers one Custom preset.
  {S1:L245-255, S3:L32-44, S3:L79, S3:L110-113}
  Resolution needed: Approve or revise production settings, preset multiplicity, system behavior, and font roles without treating demo persistence as a production decision.

- 5.3. The Clear, Midnight, Warm, and Contrast palettes/font pairings remain proposed defaults: light neutral blue/system sans, dark blue-gray/system sans, warm paper/Georgia headings with sans body, and near-black/white distinct accents with Arial, with system monospace code. HTML contains exact illustrative hex palettes.
  {S1:L247-253, S3:L32-37}
  Resolution needed: Confirm accepted theme names, colors, and font stacks or provide replacements.

- 5.4. The proposed semantic color customization remains unapproved: page/surface/raised/text/border/action/link/focus/status foreground/background tokens, derived hover/selected/disabled checks, validated colors/local stacks, and no arbitrary CSS/font URLs/HTML/scripts/styles.
  {S1:L257, S3:L9-15, S3:L75-79}
  Resolution needed: Confirm the customization contract and exact allowed values/token set.

- 5.5. Base text size 14–22 with default 16, slider plus numeric input, relative/rem scaling across text/controls/navigation/tables, readable code ratio, flexible heights, zoom compatibility, and persistence across navigation are proposed rather than accepted. The demo uses a slider and root pixel size.
  {S1:L259, S3:L38-44, S3:L79}
  Resolution needed: Confirm range/default, units, controls, and scaling behavior.

- 5.6. Theme Preview/Save/Discard/Reset/Delete behavior is proposed: preview unsaved values locally, save globally without workflow invalidation, restore saved values on discard, require explicit Save after reset, and select a replacement when deleting the active custom preset.
  {S1:L261, S2:L47, S2:L628, S3:L87, S3:L110-113}
  Resolution needed: Confirm these actions and busy-state availability under the build’s global settings gate.

- 5.7. Proposed appearance validation requires 4.5:1 ordinary text and 3:1 large text, distinguishable control/focus boundaries, failing-pair feedback with retained drafts, and a complete component preview; the demo checks selected pairs, including focus at 3:1.
  {S1:L263, S3:L73-79}
  Resolution needed: Approve the exact thresholds, checked states/pairs, and required validation without implying complete accessibility compliance.

# 6. Prototype deliverable and UX validation scope

- 6.1. The proposal specifies a self-contained offline HTML demo with embedded assets, local fonts, browser-only appearance storage, reset, and graceful session fallback. The supplied artifact exists, but its acceptance as a required deliverable or production implementation basis is unconfirmed.
  {S1:L265, S3:L8-15, S3:L32-44, S3:L110-113}
  Resolution needed: Confirm further demo work, if any, and its accepted relationship to the final portal.

- 6.2. Additional UX acceptance scope is unconfirmed: exhaustive route/control/empty/error/conflict coverage, keyboard/focus/zoom/reflow/large-font/reduced-motion/theme review, and a button-to-operation/input/prerequisite/effect/feedback/destination/help action catalog. The build requires rendered primary-page checks but does not explicitly adopt this complete proposal contract.
  {S1:L276-281, S2:L758-759, S2:L779, S1:L288}
  Resolution needed: Confirm these additional validation obligations; reported prototype checks do not establish their completion.

# 7. External skill specification reference

- 7.1. The build mandates the published Agent Skills specification and matching resource contracts but does not supply a pinned external specification or its complete contents.
  {S2:L481-483, S2:L489-495}
  Resolution needed: Identify the applicable Agent Skills version/reference if exact external metadata/compatibility obligations must be extracted; do not infer unsupplied rules.

# Sources

- **S1:** `sources/AIH_Portal_UX_Proposal_v20260922_073542Z.md`
- **S2:** `sources/AIH_Build_Prompt_v20260922_173409Z.md`
- **S3:** `../../.sandbox/ARCHVE/20260922/AIH_Portal_Theme_Demo_v20260922_073542Z.html`

- **S4:** `sources/workspace-administration-20260927.md` — accepted workspace-policy clarification.
