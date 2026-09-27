- [A] 655. The build source reports that it supersedes AIH_Build_Prompt_v20260922_134714Z.md and incorporates confirmed multi-folder workspace support and option A: human workspace changes while execution is idle, including during an open request, with affected evidence reassessed.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:5-6`.

- [A] 656. The build source authorizes building AIH and describes the approval workflow as governing subsequent product requests handled by AIH; it does not report that Git, a database, an installed agent CLI, or a published release is present.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:12`.

- [A] 657. AIH is described as a portable product-development harness helping agents understand, clarify, plan, implement authorized changes, verify, document, and resume from files.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:16`.

- [A] 658. A product workspace is the collection of explicitly configured folders for one logical product; folders can be plain directories, separate repositories, or components.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:18`.

- [A] 659. The framework home is the canonical directory containing the sole installed `.aih/` and central `.aih_product/`, identified as the mandatory writable `home` root.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:20`.

- [A] 660. The specification notes that a process working directory or checksum does not itself enforce filesystem confinement against actors with broader access.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:22,604`.

- [A] 661. Host permissions remain external constraints on AIH, and independently operated tools may have enforcement limitations that the harness cannot universally control.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:28,604`.

- [A] 662. Registered roots may be on different drives/filesystems; whole-product atomic rename and recovery behavior on every network/synchronized filesystem are not established by workspace containment.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:30,586`.

- [A] 663. Request lifecycle, workflow phase, execution ownership, and task outcome are distinct concepts; a request may remain open while its execution is stopped or blocked.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:45,215`.

- [A] 664. An open or blocked request is idle when execution ownership is stopped and reconciled; startup, running, stopping, uncertain termination, and reserved manual handoff are busy states.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:49,582`.

- [A] 665. Custom instructions are human-owned product material; agent suggestions are outputs rather than automatically applicable instruction edits.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:150`.

- [A] 666. The framework user operates AIH and submits work; the requestor provides business needs/answers and may be a different person. A returned form name is attribution rather than authentication.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:231`.

- [A] 667. The harness cannot claim to have captured intermediate external-editor saves it never observed; only observed accepted captures and explicit framework saves are evidenced.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:243`.

- [A] 668. Interpretation denotes the canonical request definition describing what changes and why.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:265-270`.

- [A] 669. Solution assessment and the implementation plan describe how to satisfy the request.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:265-270`.

- [A] 670. The question catalog points to authoritative answer records rather than owning another editable answer source.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:265-270`.

- [A] 671. The documentation increment audits planned and actual changes to current product knowledge.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:265-270`.

- [A] 672. A deferred defect can remain outside approved repair scope while still preventing successful completion because it fails a required test.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:288,300`.

- [A] 673. Intended requirements, observed implementation, test verification, deployment, and demonstrated reconstruction describe different evidential states; documentation alone does not establish runtime correctness or successful reconstruction.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:361,379`.

- [A] 674. The specification's reconstruction status remains specified but not demonstrated until evidence from an independent reconstruction exercise exists; that exercise is not an initial mandatory gate.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:379`.

- [A] 675. Source inventory is evidence collection rather than proof that inspected product behavior works at runtime.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:385`.

- [A] 676. Append-only records and content hashes provide auditability but are not tamper-proof against actors able to rewrite their underlying files.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:457-459`.

- [A] 677. Sensitive-input detection is explicitly best effort and does not establish that every secret will be detected.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:461-463`.

- [A] 678. External exports, provider records, and independent backups may lie outside AIH-owned historical-redaction control.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:467-469`.

- [A] 679. A crash may prevent an agent-authored final summary, and some CLIs may not expose complete observable action histories; reconstructed summaries can therefore retain unknown outcomes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:477-479`.

- [A] 680. Installed, enabled, dependency-available, compatible, and authorized skill states have different meanings; an enabled package can remain unavailable or unauthorized.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:503-505,546`.

- [A] 681. Credential presence does not establish verified service access.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:560,572`.

- [A] 682. A prepared manual handoff does not establish actual execution.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:560,572`.

- [A] 683. Returned external output alone does not establish termination or completed work.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:560,572`.

- [A] 684. The build source requests future live CLI, browser, platform, and storage validation but supplies no completed AIH implementation or live-validation evidence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:777-779`.

- [A] 685. The UX document labels itself a proposal for review, not yet incorporated into its named build baseline AIH_Build_Prompt_v20260922_070309Z.md; its appearance defaults await confirmation.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:3-9`.

- [A] 686. The UX source describes the HTML as a bounded interactive visual example with simulated content/runs rather than implemented initialization, attachments, source inspection, agents, persistent product files, tests, or recovery.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:9,282-288`, `../AIH_Portal_Theme_Demo_v20260922_073542Z.html:19,40,81`.

- [A] 687. The UX author reports JavaScript syntax checks, template execution across 120 page/state combinations, action/label mappings, approval/closure safeguards, selected color checks, and no external dependencies; these are reported static/template checks, with rendered layout, focus, and cross-browser review unavailable and no complete accessibility claim.
  Source: `../AIH_Portal_UX_Proposal_v20260922_073542Z.md:288`.

- [A] 688. The HTML source uses fictional Northstar Analytics requests, Excel/CSV exports, finance users, defect D-0017, plans, tests, logs, and history; those examples are not observed facts about the target product or accepted export requirements.
  Source: `../AIH_Portal_Theme_Demo_v20260922_073542Z.html:19,40,58-71`.

- [A] 689. The supplied demo code defines Clear/Midnight/Warm/Contrast palettes, custom/system modes, local font stacks, base-size bounds 14–22 with default 16, selected contrast calculations, and browser local-storage preferences with a session fallback. This is static inspection of the prototype source, not verified rendering or accepted production appearance design.
  Source: `../AIH_Portal_Theme_Demo_v20260922_073542Z.html:32-44,74-79,110-113`.
