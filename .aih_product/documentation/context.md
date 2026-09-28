# Contents

- [1. Product description and source status](#1-product-description-and-source-status)
- [2. Workspace terminology and environmental limits](#2-workspace-terminology-and-environmental-limits)
- [3. People, instructions, and request artifacts](#3-people-instructions-and-request-artifacts)
- [4. Lifecycle, execution, and capability states](#4-lifecycle-execution-and-capability-states)
- [5. Evidence, observation, and assurance limits](#5-evidence-observation-and-assurance-limits)
- [6. UX proposal and illustrative prototype](#6-ux-proposal-and-illustrative-prototype)
- [7. AIH documentation and request records](#7-aih-documentation-and-request-records)
- [Referenced documents](#referenced-documents)
- [Sources](#sources)

# 1. Product description and source status

- [A] 1.1. AIH is described as a portable product-development harness helping agents understand, clarify, plan, implement authorized changes, verify, document, and resume from files.
  {S1:L16}

- [A] 1.2. The build source reports that it supersedes AIH_Build_Prompt_v20260922_134714Z.md and originally allowed workspace changes while execution was idle, including during an open request. The accepted 2026-09-27 clarification supersedes that policy: workspace changes are allowed only between requests, with no active operation. Operations use the current validated configuration, and a separate configuration revision or folder-location history is not required.
  {S1:L5-6, S5:section "Accepted policy"}

- [A] 1.3. The build source authorizes building AIH and describes the approval workflow as governing subsequent product requests handled by AIH; it does not report that Git, a database, an installed agent CLI, or a published release is present.
  {S1:L12}

- [A] 1.4. The build source requests future live CLI, browser, platform, and storage validation but supplies no completed AIH implementation or live-validation evidence.
  {S1:L777-779}

# 2. Workspace terminology and environmental limits

- [A] 2.1. A product workspace is the collection of explicitly configured folders for one logical product; folders can be plain directories, separate repositories, or components.
  {S1:L18}

- [A] 2.2. The framework home is the canonical directory containing the sole installed `.aih/` and central `.aih_product/`, identified as the mandatory writable `home` root.
  {S1:L20}

- [A] 2.3. The specification notes that a process working directory or checksum does not itself enforce filesystem confinement against actors with broader access.
  {S1:L22, S1:L604}

- [A] 2.4. Host permissions remain external constraints on AIH, and independently operated tools may have enforcement limitations that the harness cannot universally control.
  {S1:L28, S1:L604}

- [A] 2.5. Registered roots may be on different drives/filesystems; whole-product atomic rename and recovery behavior on every network/synchronized filesystem are not established by workspace containment.
  {S1:L30, S1:L586}

- [A] 2.6. Workspace settings remain fixed throughout an open request, including while stopped or blocked. A request needing a workspace change must first be closed or cancelled under the existing lifecycle rules. After a permitted change, affected documentation, dependencies, and test coverage are reviewed before the next request starts. Historical request records remain available without a separate archive of workspace configurations.
  {S5:section "Accepted policy", S5:section "Consequences"}

# 3. People, instructions, and request artifacts

- [A] 3.1. The framework user operates AIH and submits work; the requestor provides business needs/answers and may be a different person. A returned form name is attribution rather than authentication.
  {S1:L231}

- [A] 3.2. Custom instructions are human-owned product material; agent suggestions are outputs rather than automatically applicable instruction edits.
  {S1:L150}

- [A] 3.3. Interpretation denotes the canonical request definition describing what changes and why.
  {S1:L265-270}

- [A] 3.4. Solution assessment and the implementation plan describe how to satisfy the request.
  {S1:L265-270}

- [A] 3.5. The question catalog points to authoritative answer records rather than owning another editable answer source.
  {S1:L265-270}

- [A] 3.6. The documentation increment audits planned and actual changes to current product knowledge.
  {S1:L265-270}

# 4. Lifecycle, execution, and capability states

- [A] 4.1. Request lifecycle, workflow phase, execution ownership, and task outcome are distinct concepts; a request may remain open while its execution is stopped or blocked.
  {S1:L45, S1:L215}

- [A] 4.2. An open or blocked request is idle when execution ownership is stopped and reconciled; startup, running, stopping, uncertain termination, and reserved manual handoff are busy states.
  {S1:L49, S1:L582}

- [A] 4.3. A deferred defect can remain outside approved repair scope while still preventing successful completion because it fails a required test.
  {S1:L288, S1:L300}

- [A] 4.4. Installed, enabled, dependency-available, compatible, and authorized skill states have different meanings; an enabled package can remain unavailable or unauthorized.
  {S1:L503-505, S1:L546}

- [A] 4.5. Credential presence does not establish verified service access.
  {S1:L560, S1:L572}

- [A] 4.6. A prepared manual handoff does not establish actual execution.
  {S1:L560, S1:L572}

- [A] 4.7. Returned external output alone does not establish termination or completed work.
  {S1:L560, S1:L572}

# 5. Evidence, observation, and assurance limits

- [A] 5.1. Intended requirements, observed implementation, test verification, deployment, and demonstrated reconstruction describe different evidential states; documentation alone does not establish runtime correctness or successful reconstruction.
  {S1:L361, S1:L379}

- [A] 5.2. The specification's reconstruction status remains specified but not demonstrated until evidence from an independent reconstruction exercise exists; that exercise is not an initial mandatory gate.
  {S1:L379}

- [A] 5.3. Source inventory is evidence collection rather than proof that inspected product behavior works at runtime.
  {S1:L385}

- [A] 5.4. The harness cannot claim to have captured intermediate external-editor saves it never observed; only observed accepted captures and explicit framework saves are evidenced.
  {S1:L243}

- [A] 5.5. A crash may prevent an agent-authored final summary, and some CLIs may not expose complete observable action histories; reconstructed summaries can therefore retain unknown outcomes.
  {S1:L477-479}

- [A] 5.6. Append-only records and content hashes provide auditability but are not tamper-proof against actors able to rewrite their underlying files.
  {S1:L457-459}

- [A] 5.7. Sensitive-input detection is explicitly best effort and does not establish that every secret will be detected.
  {S1:L461-463}

- [A] 5.8. External exports, provider records, and independent backups may lie outside AIH-owned historical-redaction control.
  {S1:L467-469}

# 6. UX proposal and illustrative prototype

- [A] 6.1. The UX document labels itself a proposal for review, not yet incorporated into its named build baseline AIH_Build_Prompt_v20260922_070309Z.md; its appearance defaults await confirmation.
  {S2:L3-9}

- [A] 6.2. The UX source describes the HTML as a bounded interactive visual example with simulated content/runs rather than implemented initialization, attachments, source inspection, agents, persistent product files, tests, or recovery.
  {S2:L9, S2:L282-288, S3:L19, S3:L40, S3:L81}
  Details: {D5}

- [A] 6.3. The HTML source uses fictional Northstar Analytics requests, Excel/CSV exports, finance users, defect D-0017, plans, tests, logs, and history; those examples are not observed facts about the target product or accepted export requirements.
  {S3:L19, S3:L40, S3:L58-71}
  Details: {D5}

- [A] 6.4. The supplied demo code defines Clear/Midnight/Warm/Contrast palettes, custom/system modes, local font stacks, base-size bounds 14–22 with default 16, selected contrast calculations, and browser local-storage preferences with a session fallback. This is static inspection of the prototype source, not verified rendering or accepted production appearance design.
  {S3:L32-44, S3:L74-79, S3:L110-113}
  Details: {D5}

- [A] 6.5. The UX author reports JavaScript syntax checks, template execution across 120 page/state combinations, action/label mappings, approval/closure safeguards, selected color checks, and no external dependencies; these are reported static/template checks, with rendered layout, focus, and cross-browser review unavailable and no complete accessibility claim.
  {S2:L288}

# 7. AIH documentation and request records

- [A] 7.1. This collection is the AIH repository's product documentation under .aih_product/documentation/, with requirements, technical decisions, and contextual entry points linked to typed detailed documents.
  {S4:section "Migration and request-specific documentation"}
  Details: {D1}

- [A] 7.2. The documentation catalog distinguishes stable document identities from file-local hierarchical entry numbers and local source aliases; document links and evidence citations serve different roles.
  {S4:section "Migration and request-specific documentation"}
  Details: {D2}

- [A] 7.3. The initial extension-type convention describes different information structures and suitable inert formats; its presence does not establish runtime support for every type.
  {S4:section "Migration and request-specific documentation"}
  Details: {D3}

- [A] 7.4. Request documentation describes changes relative to a recorded product baseline, while original attachments, analysis, implementation evidence, and lifecycle state remain separately owned request records.
  {S4:section "Migration and request-specific documentation"}
  Details: {D4}

- [A] 7.5. This migration preserves existing source-supported definitions and unresolved issues; reorganizing the collection does not itself provide evidence that the AIH runtime or future requested behavior is implemented.
  {S4:section "Migration and request-specific documentation"}
  Details: {D1:section "Product collection"}

# Referenced documents

- **D1:** [Documentation organization](extensions/architecture/documentation-organization.md) — architecture
- **D2:** [Documentation catalog contract](extensions/interface-contract/documentation-catalog.md) — interface-contract
- **D3:** [Documentation extension types](extensions/data-dictionary/document-types.yaml) — data-dictionary
- **D4:** [Request documentation update flow](extensions/processing-flow/request-documentation-update.md) — processing-flow
- **D5:** [Illustrative portal theme demo](../../.sandbox/ARCHVE/20260922/AIH_Portal_Theme_Demo_v20260922_073542Z.html) — ui-specification

# Sources

- **S1:** `sources/AIH_Build_Prompt_v20260922_173409Z.md`
- **S2:** `sources/AIH_Portal_UX_Proposal_v20260922_073542Z.md`
- **S3:** `../../.sandbox/ARCHVE/20260922/AIH_Portal_Theme_Demo_v20260922_073542Z.html`
- **S4:** `sources/documentation-evolution.md`

- **S5:** `sources/workspace-administration-20260927.md` — accepted clarification; supersedes conflicting earlier workspace policy.
