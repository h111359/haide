- 690. Adoption of the proposal-only shell/navigation details is unconfirmed: fixed desktop sidebar, accessible narrow-screen drawer with Escape/focus behavior, non-obscured fields, labeled scroll regions, reflow, header page-help/expandable details, session tab/filter/detail restoration, Back/Forward behavior, unavailable-target fallback, and unsaved-edit navigation choices. The build confirms eight pages and six tabs but does not adopt every proposed interaction.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,13-35`, `../AIH_Build_Prompt_v20260922_173409Z.md:620-646`.
  Resolution needed: Identify which additional shell, navigation, route, and draft-preservation details are approved.

- 691. The proposed conflict editor and accessibility details lack acceptance: a Your draft/Saved version labeled diff, Use saved version/Continue editing a merged draft/Download my draft choices with a fresh revision check and no force overwrite; persistent field labels and required/optional indicators, field-linked errors, keyboard/focus/semantic/live-announcement support, non-color state cues, reduced motion, and non-disruptive events.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,58-62`.
  Resolution needed: Confirm the proposed conflict-editing and accessibility behaviors.

- 692. The proposal describes pending-checkpoint submissions and safe adoption while a writer is active, and the HTML simulates pendingSubmission; the build explicitly rejects busy submissions and queues and adopts new revisions only through a subsequent idle action after a recorded boundary. The proposal is expressly unapproved, so its busy-intake behavior is not a settled alternative.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:51-55,107,120`, `../AIH_Build_Prompt_v20260922_173409Z.md:47-49,162-166,239`, `../AIH_Portal_Theme_Demo_v20260922_073542Z.html:59-60,66,85`.
  Resolution needed: Confirm whether to revise the proposal/demo to match the build before adopting their UX.

- 693. Adoption of proposal-only Overview/setup/input details is unconfirmed: exact card/introduction/empty/blocker text, task/last-update fields, count/freshness presentation, Start versus Continue navigation, step names/source counts/no invented percentages, selected recovery links, title/attachment metadata and draft-only removal, Preview/Edit controls, and comparison/response-history navigation.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:64-112`, `../AIH_Build_Prompt_v20260922_173409Z.md:612-624,639`.
  Resolution needed: Confirm the additional display/copy/control choices without replacing the build’s complete-baseline request gate.

- 694. Adoption of proposal-only Analysis/Plan review details is unconfirmed: precise display fields, draft defect rationale and save controls, task expansion, revision/required-test/documentation links, exact revision approval surface without a second confirmation, and omission of combined Approve-and-implement. The build permits a clearly labeled combined action but does not require one.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:116-143`, `../AIH_Build_Prompt_v20260922_173409Z.md:209,640-641`.
  Resolution needed: Confirm approved review interactions and whether to offer the combined action.

- 695. The proposal uses Complete request and the HTML uses Close as completed, whereas the build specifies explicit human Close successfully after Ready to close with fresh gate validation.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:172`, `../AIH_Portal_Theme_Demo_v20260922_073542Z.html:65,88`, `../AIH_Build_Prompt_v20260922_173409Z.md:223,644`.
  Resolution needed: Confirm whether the proposal/demo closure labels should be revised before adopting their UI.

- 696. Adoption of additional question-lane fields and interactions is unconfirmed: optional title/request reference/profile override, Save question draft, follow-up identities, New question navigation, and exact modification-request copy.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:176-186`, `../AIH_Build_Prompt_v20260922_173409Z.md:174-186,624`.
  Resolution needed: Confirm which proposal-only Q&A interactions supplement the build’s settled read-only lane.

- 697. Adoption of detailed documentation browsing/refresh design is unconfirmed: category/applicability/freshness/content-versus-metadata filters, snippets and clear filters, known-defect views, refresh form fields and deliberate full reinspection, and exact navigation/copy. Proposal wording that a blocked request cannot be bypassed must also account for the build’s explicitly permitted bounded workspace-reconciliation task within an open request.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:188-200`, `../AIH_Build_Prompt_v20260922_173409Z.md:395-397,625`.
  Resolution needed: Confirm additional UX and align its maintenance guidance with that exception.

- 698. Adoption of detailed Runs/history interaction design is unconfirmed: run type/owner/date filters, metadata pagination, event filtering/omitted counts, pause/follow log scrolling, exact handoff copy/download/evidence controls, historical filters/detail fields/labels, and ledger supersession navigation. Handoff evidence intake must remain within the build’s reserved Stop/release flow.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:201-221`, `../AIH_Build_Prompt_v20260922_173409Z.md:572,626-627,654`.
  Resolution needed: Confirm the additional interactions and reconcile standalone evidence-reconciliation wording with that flow.

- 699. Adoption of proposal-only Settings detail is unconfirmed: Profiles/Skills/Product/Instructions/Appearance sections, editor storage-target/revision/validation display, separate privileged editor, profile add/edit/default/assignment/delete restrictions, exact instruction editor controls, and immediate cosmetic application. The build additionally requires Workspace and disallows operational settings saves while busy.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:223-243`, `../AIH_Build_Prompt_v20260922_173409Z.md:628-635`.
  Resolution needed: Confirm these details and their idle/effective boundaries.

- 700. Production appearance storage and theme selection are unapproved: the proposal suggests declarative appearance in .aih_product/config.yaml, immutable built-ins and named product-owned custom presets, Use system/Clear-or-Midnight selection, theme duplication, and allowed heading/body/code font presets; the demo stores only browser preferences and offers one Custom preset.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:245-255`, `../AIH_Portal_Theme_Demo_v20260922_073542Z.html:32-44,79,110-113`.
  Resolution needed: Approve or revise production settings, preset multiplicity, system behavior, and font roles without treating demo persistence as a production decision.

- 701. The Clear, Midnight, Warm, and Contrast palettes/font pairings remain proposed defaults: light neutral blue/system sans, dark blue-gray/system sans, warm paper/Georgia headings with sans body, and near-black/white distinct accents with Arial, with system monospace code. HTML contains exact illustrative hex palettes.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:247-253`, `../AIH_Portal_Theme_Demo_v20260922_073542Z.html:32-37`.
  Resolution needed: Confirm accepted theme names, colors, and font stacks or provide replacements.

- 702. The proposed semantic color customization remains unapproved: page/surface/raised/text/border/action/link/focus/status foreground/background tokens, derived hover/selected/disabled checks, validated colors/local stacks, and no arbitrary CSS/font URLs/HTML/scripts/styles.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:257`, `../AIH_Portal_Theme_Demo_v20260922_073542Z.html:9-15,75-79`.
  Resolution needed: Confirm the customization contract and exact allowed values/token set.

- 703. Base text size 14–22 with default 16, slider plus numeric input, relative/rem scaling across text/controls/navigation/tables, readable code ratio, flexible heights, zoom compatibility, and persistence across navigation are proposed rather than accepted. The demo uses a slider and root pixel size.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:259`, `../AIH_Portal_Theme_Demo_v20260922_073542Z.html:38-44,79`.
  Resolution needed: Confirm range/default, units, controls, and scaling behavior.

- 704. Theme Preview/Save/Discard/Reset/Delete behavior is proposed: preview unsaved values locally, save globally without workflow invalidation, restore saved values on discard, require explicit Save after reset, and select a replacement when deleting the active custom preset.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:261`, `../AIH_Build_Prompt_v20260922_173409Z.md:47,628`, `../AIH_Portal_Theme_Demo_v20260922_073542Z.html:87,110-113`.
  Resolution needed: Confirm these actions and busy-state availability under the build’s global settings gate.

- 705. Proposed appearance validation requires 4.5:1 ordinary text and 3:1 large text, distinguishable control/focus boundaries, failing-pair feedback with retained drafts, and a complete component preview; the demo checks selected pairs, including focus at 3:1.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:263`, `../AIH_Portal_Theme_Demo_v20260922_073542Z.html:73-79`.
  Resolution needed: Approve the exact thresholds, checked states/pairs, and required validation without implying complete accessibility compliance.

- 706. The proposal specifies a self-contained offline HTML demo with embedded assets, local fonts, browser-only appearance storage, reset, and graceful session fallback. The supplied artifact exists, but its acceptance as a required deliverable or production implementation basis is unconfirmed.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:265`, `../AIH_Portal_Theme_Demo_v20260922_073542Z.html:8-15,32-44,110-113`.
  Resolution needed: Confirm further demo work, if any, and its accepted relationship to the final portal.

- 707. Additional Help UX is proposed but unapproved: guide contents/search/article/breadcrumbs/related topics/version, local platform-specific Copy command, Windows/Linux selector, quick-start view, return-to-origin, and broken-anchor fallback.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:267-274`, `../AIH_Build_Prompt_v20260922_173409Z.md:629,674-678`.
  Resolution needed: Confirm which controls supplement the build’s settled shared-help requirement.

- 708. Additional UX acceptance scope is unconfirmed: exhaustive route/control/empty/error/conflict coverage, keyboard/focus/zoom/reflow/large-font/reduced-motion/theme review, and a button-to-operation/input/prerequisite/effect/feedback/destination/help action catalog. The build requires rendered primary-page checks but does not explicitly adopt this complete proposal contract.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:276-281`, `../AIH_Build_Prompt_v20260922_173409Z.md:758-759,779`, `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:288`.
  Resolution needed: Confirm these additional validation obligations; reported prototype checks do not establish their completion.

- 709. The build mandates the published Agent Skills specification and matching resource contracts but does not supply a pinned external specification or its complete contents.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:481-483,489-495`.
  Resolution needed: Identify the applicable Agent Skills version/reference if exact external metadata/compatibility obligations must be extracted; do not infer unsupplied rules.

- 710. The proposed Overview route pattern `/` has no supplied acceptance evidence.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,23`.
  Resolution needed: Confirm the Overview route pattern or provide the intended replacement.

- 711. The proposed Current request route pattern `/request/{id}/{tab}` has no supplied acceptance evidence.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,24`.
  Resolution needed: Confirm the Current request route pattern or provide the intended replacement.

- 712. The proposed Questions route pattern `/questions` and `/questions/{id}` has no supplied acceptance evidence.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,25`.
  Resolution needed: Confirm the Questions route pattern or provide the intended replacement.

- 713. The proposed Documentation route pattern `/documentation/{node-id}` has no supplied acceptance evidence.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,26`.
  Resolution needed: Confirm the Documentation route pattern or provide the intended replacement.

- 714. The proposed Runs route pattern `/runs/{run-id}` has no supplied acceptance evidence.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,27`.
  Resolution needed: Confirm the Runs route pattern or provide the intended replacement.

- 715. The proposed History route pattern `/history/requests/{id}` and `/history/ledger/{event-id}` has no supplied acceptance evidence.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,28`.
  Resolution needed: Confirm the History route pattern or provide the intended replacement.

- 716. The proposed Settings route pattern `/settings/{section}` has no supplied acceptance evidence.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,29`.
  Resolution needed: Confirm the Settings route pattern or provide the intended replacement.

- 717. The proposed Help route pattern `/help/{section-id}` has no supplied acceptance evidence.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,30`.
  Resolution needed: Confirm the Help route pattern or provide the intended replacement.

- 718. The additional proposed Save draft interaction is not confirmed: valid local fields and a revision check persist editable content only; stay in place and show revision/time with “Draft saved. Nothing has been submitted or started.”.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,42`.
  Resolution needed: Confirm this Save draft interaction as an addition to the settled build workflow.

- 719. The additional proposed Discard unsaved edits interaction is not confirmed: restore the last saved local draft without changing submissions; name the discarded draft and stay unless this is a navigation departure.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,43`.
  Resolution needed: Confirm this Discard unsaved edits interaction as an addition to the settled build workflow.

- 720. The additional proposed Cancel interaction is not confirmed: close the pending dialog/editor without applying selections and return focus to its opener; cancellation is not stopping a run.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,44`.
  Resolution needed: Confirm this Cancel interaction as an addition to the settled build workflow.

- 721. The additional proposed View details / View evidence interaction is not confirmed: open a permitted stable artifact reference inline or by detail route and retain a return link.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,45`.
  Resolution needed: Confirm this View details / View evidence interaction as an addition to the settled build workflow.

- 722. The additional proposed Download file interaction is not confirmed: download the exact identified permitted artifact revision with a safe filename and never execute attachments.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,46`.
  Resolution needed: Confirm this Download file interaction as an addition to the settled build workflow.

- 723. The additional proposed Compare revisions interaction is not confirmed: display a read-only old/new labeled diff without inferred approval or overwrite.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,47`.
  Resolution needed: Confirm this Compare revisions interaction as an addition to the settled build workflow.

- 724. The additional proposed Retry interaction is not confirmed: safely reuse or supersede an identified reconciled failed operation, offering inspection instead of retry when success is uncertain.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,48`.
  Resolution needed: Confirm this Retry interaction as an addition to the settled build workflow.

- 725. The additional proposed Refresh status interaction is not confirmed: read observable current status only, never documentation refresh, tests, or an agent run.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,49`.
  Resolution needed: Confirm this Refresh status interaction as an addition to the settled build workflow.

- 726. The additional proposed Help for this action interaction is not confirmed: open an installed relevant guide anchor and restore the prior view on return.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,50`.
  Resolution needed: Confirm this Help for this action interaction as an addition to the settled build workflow.

- 727. The additional proposed implementation and verification UI lacks acceptance: pending/running/completed/blocked/failed/rework task states; compact timeline and full-log/results/file links; suite/check requirement/task mapping, required/inapplicable status, timestamp/version/freshness/failure/evidence fields; increment-item/target/reason/task/planned/applied/verified/gap fields; explicitly authorized Run required tests, deterministic Validate documentation with semantic gaps reported separately, and Continue authorized repairs navigation.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:144-166`.
  Resolution needed: Confirm the supplementary implementation and verification displays and actions.

- 728. Cancelled/rejected closure forms are proposed with a reason, retained changes, uncertain operations and unresolved items; Confirm closure records that outcome and Keep request open cancels the form without rollback. The build settles unsuccessful closure behavior but does not specify all these form details.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:174`, `../AIH_Build_Prompt_v20260922_173409Z.md:221,644`.
  Resolution needed: Confirm the proposed unsuccessful-closure form and reason field.

- 729. The proposal additionally requires unavailable-action explanations visible next to the control and usable without hover; this precise feedback presentation is not confirmed by the supplied build acceptance.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,38`.
  Resolution needed: Confirm the proposed visible non-hover unavailable-action explanations.

- 730. The proposal specifies unsaved-before-run feedback “Save these edits before submitting.” with saved valid input required and submitted revision identified; its exact interaction and copy remain unapproved.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,52`.
  Resolution needed: Confirm the proposed unsaved-before-run interaction and feedback.

- 731. The proposal specifies that incoming live events must not discard form drafts; acceptance of this additional draft-preservation interaction is unconfirmed.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:4-9,34`.
  Resolution needed: Confirm the proposed preservation of form drafts during incoming live events.
