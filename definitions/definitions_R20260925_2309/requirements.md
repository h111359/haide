- [A] 1. The AIH delivery MUST implement and verify the complete framework, including infrastructure, instructions, conventions, portable skills, portal, tests, and operating documentation; a proposal, scaffold, reduced first version, or unspecified future work does not satisfy delivery.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:8-10`.

- [A] 2. AIH implementation work MUST resolve routine engineering details without asking the requester to prioritize in-scope features, and ask only about consequential ambiguities unresolved by inspection or the specification.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:10`.

- [A] 3. AIH installation and build work MUST preserve existing product content and inspect applicable workspace and host instructions first.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:12`.

- [A] 4. AIH MUST support product understanding, requirements clarification, planning, authorized implementation, verification, maintained documentation, and file-based resumption after interruption.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:16`.

- [A] 5. Each AIH installation MUST support one logical product spanning one or more explicitly configured filesystem folders, including plain directories, separate repositories, and multiple components.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:18`.

- [A] 6. AIH MUST support Windows and Linux and distinguish intended platform support from platforms actually tested.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:18`.

- [A] 7. AIH MUST default to a single mandatory writable framework home and allow additional explicitly human-selected folders, including siblings or different drives, subject to host permission.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:20`.

- [A] 8. AIH inspection MUST stay within explicitly registered readable folders; their common ancestor and unregistered neighboring locations do not become workspace members.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:22`.

- [A] 9. All managed filesystem mutations MUST remain within registered writable folders and the action's authorized scope, including creates, writes, deletes, moves, permission changes, cleanup, tests, caches, subprocesses, agents, optional Git, and launched browser effects.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:22-24`.

- [A] 10. Writable workspace membership MUST NOT itself authorize implementation changes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:22`.

- [A] 11. Registered read-only folders MUST permit inspection without any managed direct or indirect writes, including outputs, caches, cleanup, and writable-alias bypasses.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:22-24`.

- [A] 12. AIH MUST reject registrations whose duplicate, overlapping, or aliased roots make ownership or access ambiguous.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:24`.

- [A] 13. AIH MUST reject mutations that could reach unregistered/read-only locations or whose containment cannot be established.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:24`.

- [A] 14. A discovered content link or dependency MUST NOT register its target or expand authority.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:24`.

- [A] 15. Explicit controlled import of supplied external material is OPTIONAL and MUST NOT authorize arbitrary neighboring-file access.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:24`.

- [A] 16. Plans, inventories, documentation, test contracts, checkpoints, and evidence MUST distinguish files by stable folder identity and relative path with the applicable workspace revision, preserving historical location mappings after relocation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:26`.

- [A] 17. Missing or inaccessible registered folders MUST remain visible and MUST NOT silently disappear from required coverage or tests.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:26`.

- [A] 18. Reading or invoking host-permitted external runtimes, libraries, agent executables, and authentication references is OPTIONAL; it MUST NOT grant filesystem-write authority outside registered writable roots.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:28`.

- [A] 19. AIH MUST block incompatible tools with actionable setup guidance without weakening confinement or moving credentials into tracked product files.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:28`.

- [A] 20. Separately authorized remote effects MUST NOT grant outside-workspace filesystem-write authority.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:28`.

- [A] 21. AIH MUST report actual storage and locking assumptions and tested limitations without claiming recovery guarantees for untested network or synchronized storage.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:30`.

- [A] 22. AIH MUST remain fully operable through direct Python invocation without Node, PowerShell, or optional menu wrappers.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:39`.

- [A] 23. Installation, history, diffs, revision checks, verification, and recovery MUST work without Git; Git MUST NOT be required or initialized by default.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:43`.

- [A] 24. All registered folders MUST share one product definition, documentation tree, required test inventory, and execution owner.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:45`.

- [A] 25. AIH MUST allow only one open change request and MUST NOT create a backlog, queued future request, or concurrent change-request execution, or silently replace/close/archive the active request to admit another.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:45,219`.

- [A] 26. Bootstrap and explicitly invoked documentation-only maintenance MUST remain scoped system operations without implementation authority.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:45`.

- [A] 27. AIH MUST allow only one operational action across change work, questions, setup, maintenance, tests, diagnostics, and manual handoffs; starting, running, stopping, uncertain termination, and reserved external execution all count as busy.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:47-49`.

- [A] 28. While busy, Stop MUST be the only operational control; saves, imports, submissions, approvals, settings changes, closure, questions, and replacement commands MUST be refused without queuing them.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:47-49,166`.

- [A] 29. Passive navigation, help, existing-artifact viewing/download, and status/log observation MUST remain available while busy.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:47`.

- [A] 30. The current action MUST be allowed to perform its own already-authorized internal substeps under its existing ownership.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:47`.

- [A] 31. A safely stopped or completed action MUST require a new explicit user action for subsequent work; no automatic dispatch follows Stop or completion.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:49`.

- [A] 32. An open blocked request with reconciled stopped ownership MUST be treated as idle for permitted drafts and questions without authorizing unrelated change work.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:49`.

- [A] 33. Externally edited inputs, instructions, or configuration MUST NOT silently change live execution authority; affected evidence and authority MUST be reconciled through the next applicable explicit idle action, with a safe pause when uncertain.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:49,130,154`.

- [A] 34. Ordinary operations MUST leave the installed framework core unchanged, including generated catalogs, bundled resources, logs, caches, and temporary files.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:66`.

- [A] 35. Core repair, catalog/resource regeneration, maintenance, and upgrades MUST require no open request and no other execution owner; blocked, paused, and Ready to close requests remain open.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:68`.

- [A] 36. A broken helper MUST NOT create an in-request core-repair exception; cancellation/rejection, if needed before repair, MUST preserve the incomplete request and current-state notice.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:68`.

- [A] 37. Missing or broken deterministic helpers MUST produce an actionable framework-gap diagnosis without silently bypassing validation or transactions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:80`.

- [A] 38. AIH MUST preserve direct human editing of permitted product files and detect/validate observed edits without claiming control over external filesystem actors.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:80`.

- [A] 39. AIH MUST minimize avoidable model-token use without reducing analysis, coverage, instructions, tests, documentation, evidence, or silently changing agents.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:84,90`.

- [A] 40. Compact outputs MUST retain evidence references and label omitted detail while preserving complete available sanitized evidence for targeted inspection.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:88`.

- [A] 41. Diagnostics and portal status MUST expose adapter-supplied actual token usage by operation/run/segment and useful totals, mark missing telemetry unavailable, and distinguish measured savings from proxies.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:92`.

- [A] 42. Product-state storage, including temporary data, MUST remain inert; accepted examples and attachments MUST NOT be executed or imported as code.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:110`.

- [A] 43. Workspace membership and access changes MUST be restricted to explicit human administration; agents MUST NOT register roots or expand their own permissions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:120`.

- [A] 44. Agent suggestions of a missing dependency or workspace folder are OPTIONAL and MUST NOT themselves register the folder or authorize its access.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:120`.

- [A] 45. The mandatory framework home MUST NOT be removed, made read-only, or relocated by an ordinary additional-folder edit.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:118`.

- [A] 46. Human workspace changes MUST be accepted while globally idle even with an open, blocked, or Ready to close request; this permission MUST NOT relax the separate core-maintenance gate.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:122`.

- [A] 47. Saving workspace changes MUST record their revision and mark affected analysis, approval, tests, documentation, baseline, and readiness for reassessment, preserving unaffected evidence only with recorded justification and treating unknown impact as unresolved.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:124`.

- [A] 48. Saving workspace configuration MUST NOT start agents/tests, move product files, expand business scope, or automatically resume implementation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:124`.

- [A] 49. New or relocated areas MUST receive inventory and documentation baselining before implementation relies on them, with cross-folder dependencies and affected authorization reconciled.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:126`.

- [A] 50. Workspace reconciliation with an open request MUST be an explicitly authorized bounded documentation task within that request; without a request it MUST belong to setup or documentation maintenance.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:126,395-397`.

- [A] 51. Removing workspace membership MUST NOT delete files, request records, documentation history, evidence, required test obligations, or unresolved defects.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:128`.

- [A] 52. Access revocation MUST apply to subsequent recovery and cleanup; interrupted work MUST NOT revive removed registrations or write through stale paths.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:128`.

- [A] 53. Relocation MUST change the mapping without moving files and MUST require validation of the new location, content, and access rather than assuming identity from relative paths.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:128`.

- [A] 54. Each request MUST retain its own stable identity and complete input, clarification, amendments, analysis, plan, execution, verification, documentation-impact, and outcome record across affected folders.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:134`.

- [A] 55. Closed requests MUST preserve distinguishable completed, cancelled, and rejected outcomes, short metadata summaries, and stable links after archival.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:136`.

- [A] 56. Ordinary work MUST use current documentation, persistent current-state notices, and the active request; historical summaries/details MUST be loaded only for a relevant question.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:138`.

- [A] 57. Successful closure MUST preserve durable knowledge and applicable decisions in current documentation so historical request records are not hidden prerequisites for normal work.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:138`.

- [A] 58. Bootstrap and standalone documentation maintenance MUST retain resumable audit/checkpoint records without a synthetic change request or reliance on private memory/unavailable conversations.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:140-142`.

- [A] 59. AIH MUST respect host instruction hierarchy, restrictions, permissions, and existing authorization; explicit user directions and human product instructions govern behavior within those limits.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:146-148`.

- [A] 60. Behavioral overrides MUST be identifiable and MUST NOT bypass fixed formats, schemas, interfaces, or validation contracts.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:148`.

- [A] 61. Custom-instruction creation and editing MUST be restricted to humans; agents MUST NOT create or modify instruction content.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:150`.

- [A] 62. Agent suggestions of custom-instruction wording in output files are OPTIONAL and MUST NOT apply themselves as instruction edits.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:150`.

- [A] 63. Initialization is permitted to create the custom-instructions directory and explain how humans add instructions; creating instruction content is not permitted. This directory-and-guidance creation is OPTIONAL.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:150`.

- [A] 64. Historical requests, imports, logs, comments, attachments, memory, and agent proposals MUST NOT automatically become active instructions or authorize executable settings, skills, wider access, approval, or deployment.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:152`.

- [A] 65. Instruction changes MUST retain segment provenance and invalidate only affected assumptions/authorization; still-applicable authorization MUST persist.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:154`.

- [A] 66. Users MUST be able to operate entirely through files and explicit Python commands without chat or the portal.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:158`.

- [A] 67. Saving inputs, answers, and amendments MUST create drafts only; receiving accepted requestor responses MUST stage imports only, without execution or scope adoption.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:160`.

- [A] 68. Explicit idle Clarify, Analyze, Implement, Implement directly, or Resume MUST submit current relevant saved input, reviewed answer drafts, and saved pending amendments, excluding raw/unreviewed uploads.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:162`.

- [A] 69. Detected sensitive intake MUST be rejected before normal persistence with a corrected-resubmission request and only non-sensitive rejection metadata; rejected values MUST NOT appear in diagnostics, receipts, responses, or submissions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:164`.

- [A] 70. Submission capture MUST preserve preceding submitted versions and newer human edits, and MUST report partial or contradictory questionnaire edits needing correction.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:164`.

- [A] 71. Scope changes MUST invalidate affected plan approval, verification, and documentation freshness; cosmetic changes need not invalidate unrelated evidence, with the determination recorded.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:168`.

- [A] 72. AIH MUST maintain one current change-work response with preserved prior versions, request/submission/run references, outcome, blockers/questions, next action, and linked evidence/forms.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:170`.

- [A] 73. AIH MUST offer a separate read-only question lane when globally idle, including with no request, pending idle setup, or an open/blocked request whose owner stopped; existing questions and answers MUST remain readable at all times.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:174`.

- [A] 74. Questions MUST NOT open a request, occupy its slot, change approval, or resume blocked work.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:178`.

- [A] 75. Question execution MUST NOT change product source, durable documentation, configuration, custom instructions, or change-work state; only its permitted communication and execution records may be written.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:180`.

- [A] 76. Where read-only enforcement is unavailable, AIH MUST report the limitation and offer a constrained/manual route without claiming prompting alone provides protection.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:182`.

- [A] 77. Answers MUST cite stable folder-qualified sources, observed content/workspace versions, and uncertainty, and detect/report mixed observations caused by external edits or repeat affected inspection within the action.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:184`.

- [A] 78. Question intake MUST apply the same sensitive-input admission rules as other human intake.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:184`.

- [A] 79. Question execution MUST NOT modify the product to demonstrate an answer.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:184`.

- [A] 80. Questions asking for modifications MUST be directed to explicit change work and MUST NOT silently become requests, implementation authority, or submitted blocker answers.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:186`.

- [A] 81. A new request MUST open only by explicit submission after the complete current configured-product documentation baseline passes; idle setup, Q&A, and local drafts may precede this gate.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:192`.

- [A] 82. An already-open request with incomplete baseline after a workspace change MUST still permit explicit idle amendments and blocker clarification, while implementation remains gated on reconciliation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:192`.

- [A] 83. Clarify MUST establish what changes and why, recording problem/rationale, stakeholders/users, outcomes, current versus required behavior, in/out scope, functional/nonfunctional requirements, explicit constraints, observable acceptance criteria, assumptions, and unresolved questions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:201`.

- [A] 84. Read-only evidence inspection during Clarify is OPTIONAL for understanding behavior, dependencies, feasibility, and missing requirements; it MUST NOT choose architecture, algorithms, technologies, components, tasks, or test tooling, or implement changes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:203`.

- [A] 85. Clarify MUST be permitted to write clarification artifacts and narrowly factual evidence-backed known-defect/stale-documentation bookkeeping with source/request references, without repairs, redesign, substantive business-documentation rewriting, or inferred approved intent.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:203`.

- [A] 86. Clarification MUST retain explicitly supplied technical constraints and their provenance, while distinguishing existing implementation choices from required constraints.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:205`.

- [A] 87. Analyze MUST own implementation design and planning, with traceability to clarified requirements and a clear separation between design decisions and requirements.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:207`.

- [A] 88. Consequential requirement gaps discovered in Analysis MUST preserve the draft analysis/plan and return to clarification within the same request; implementation/design questions MUST remain identifiable as Analysis questions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:207,257`.

- [A] 89. Clarify MUST NOT implement, select a solution, generate an implementation plan, or automatically invoke Analyze; Analyze MUST NOT implement.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:209`.

- [A] 90. Approving a plan MUST NOT start implementation; a clearly labeled combined Approve and implement operation is OPTIONAL and MUST record both intentions if provided.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:209`.

- [A] 91. Implement directly MUST perform necessary internal analysis and persist the sequential implementation/test/documentation/evidence plan before product changes, recording scope-bound direct authorization rather than fictional human approval.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:211`.

- [A] 92. Direct implementation MUST NOT waive consequential clarification, unrelated-defect selection, tests, documentation, logs, evidence, host approval, or authorization for material expansion.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:211`.

- [A] 93. Implementation authority MUST remain bound to identified business scope across folders; workspace registration MUST NOT substitute for scope approval or repeatedly invalidate unrelated valid authorization.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:213`.

- [A] 94. Status MUST distinguish workflow phase, request lifecycle, worker state, and task outcome; process success or stoppage MUST NOT imply request completion.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:215`.

- [A] 95. A consequential blocker MUST stop the entire change workflow after preserving immediate evidence, relevant defect/documentation status, response, checkpoint, and any required requestor questionnaire; independent implementation tasks MUST NOT continue.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:217`.

- [A] 96. When blocked ownership safely releases, users MUST be able to submit blocker answers/amendments or clarification without implicitly authorizing repairs or resuming implementation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:217`.

- [A] 97. Documented defaults for optional unanswered questions are OPTIONAL; consequential unanswered questions MUST remain blockers.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:217,314`.

- [A] 98. Stop MUST leave the request resumable, preserve unfinished work, and require confirmed termination or reconciled external ownership without requiring task success or passing tests.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:221`.

- [A] 99. Explicit idle cancellation/rejection MUST preserve partial changes, evidence, and unresolved outcomes without automatic rollback or a requirement to pass tests or rewrite all documentation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:221`.

- [A] 100. Before unsuccessful closure releases the request slot, AIH MUST preserve a discoverable current-state notice covering retained changes, affected/stale documentation, defects, verification uncertainty, and archived evidence; subsequent authorized work MUST reconcile affected knowledge before reliance.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:221`.

- [A] 101. Successful completion MUST require implemented scope, passing required tests, acceptance/verification satisfaction, current affected documentation or justified no-impact, and recorded evidence; skipped, stale, failed, and unexecuted required tests MUST NOT count as passes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:223`.

- [A] 102. Passing gates MUST set Ready to close while the request remains open; explicit human Close successfully MUST recheck current gates and content before archival, withdrawing readiness if evidence changed.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:223`.

- [A] 103. Integration and deployment MUST remain separate milestones; Git, merging, and production deployment MUST NOT become completion gates unless explicitly included in request scope.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:225`.

- [A] 104. Product changes after request closure MUST use a new request.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:225`.

- [A] 105. One repeatable Clarify command MUST handle initial understanding, reviewed framework/requestor answers, amendments, changed human instructions, and later contradictions from persisted state.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:229`.

- [A] 106. AIH MUST record attributed requestor separately from actual framework submitter; a returned name MUST NOT establish authenticated identity or implementation authority.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:231`.

- [A] 107. Each Clarify round MUST reconcile submitted inputs and preserve one evolving interpretation, source-linked prior revisions, question catalog, conflicts, stale assumptions/answers, changed criteria, and downstream impacts.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:233`.

- [A] 108. Clarify MUST NOT resolve contradictions through arbitrary last-answer/file-wins; submitted explicit supersession may settle a statement, otherwise clarification is required.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:233`.

- [A] 109. Unchanged Clarify invocations MUST reuse valid results without duplicate questions, amendment application, gratuitous model calls, or semantic revision churn; meaningful new inputs may create another bounded question batch.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:235`.

- [A] 110. Each clarification round MUST report applied changes, open questions, blockers, next action, and whether it awaits framework-user answers, requestor answers, other resolution, or is ready for explicit Analysis; readiness MUST NOT imply approval.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:237`.

- [A] 111. Clarify resumption MUST reconcile the acknowledged complete task/segment boundary or incomplete Stop checkpoint, preserve scoped authority and progress, and avoid requiring the user to reconstruct a conversation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:239`.

- [A] 112. The request MUST expose an Amendments area with idle-only Add amendment, supporting changed wishes, additional detail, correction, and withdrawal without rewriting submitted history.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:241`.

- [A] 113. Each amendment MUST retain a stable ID, optional title/reason, original description, attribution, creation/save times, order, and known affected or superseded links.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:241`.

- [A] 114. Amendment history MUST preserve every accepted framework-saved/submitted revision and externally edited version next observed at a permitted capture action; unsaved keystrokes and unseen external saves need not be archived.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:243`.

- [A] 115. Amendments MUST show draft, saved-not-submitted, submitted, applied, superseded, withdrawn, and needs-clarification states as applicable; correction/withdrawal MUST append history subject only to authorized sensitive-value redaction.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:243`.

- [A] 116. Before execution, AIH MUST show the relevant saved input, reviewed answers, and pending amendments being submitted; selecting/saving alone MUST NOT apply them.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:245`.

- [A] 117. Direct input edits MUST retain revision differences and provenance, link explicitly identified amendments, and MUST NOT silently disappear or create duplicate amendments for the same change.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:245`.

- [A] 118. Amendment application MUST retain original wording and trace its effects on interpretation, questions, supersession, and unresolved state; conflicts with returned answers require explicit resolution unless a submitted supersession already resolves them.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:247`.

- [A] 119. Complete amendment histories MUST survive completed/cancelled/rejected archival; late imports MUST NOT amend closed requests. Historical sensitive-value redaction MUST remain a separate explicitly authorized operation, not a late-import exception.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:249`.

- [A] 120. The workflow MUST remove the standalone Plan action from CLI and portal; repeatable Analyze MUST own plan generation/regeneration and application of submitted answers, amendments, and updated human instructions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:253`.

- [A] 121. Analyze MUST update affected artifacts from saved state, preserve current valid results and previous revisions, stop for consequential unanswered questions, and generate the plan automatically when sufficiently resolved without implementation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:255-259`.

- [A] 122. Plan regeneration MUST retain completed-task history and identify still-valid tasks and required rework without needless resetting or rewriting on unchanged input.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:259`.

- [A] 123. Normal Analysis MUST keep interpretation, question catalog, assessment, and unrelated issues distinct, with a concise scoped none-found finding when appropriate rather than invented content.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:272`.

- [A] 124. Additional detailed impact, risk/decision, and verification records MUST be used when substantive detail warrants separate files; simple changes MUST retain concise equivalent coverage in the assessment or plan without empty boilerplate.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:274`.

- [A] 125. Plan tasks MUST identify stable ID, sequence, outcome, requirement/decision links, specific changes, folder-qualified existing/new paths, action types, dependencies, and completion evidence; unresolved paths MUST use bounded investigation before dependent changes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:278`.

- [A] 126. Implementation MUST execute tasks sequentially in plan order, record states/outcomes, preserve valid evidence, and MUST NOT silently skip, reorder, or concurrently execute tasks.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:280`.

- [A] 127. Material implementation scope/approach changes MUST revise the plan and obtain applicable authorization while explicitly invalidating affected work.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:280`.

- [A] 128. Every plan MUST include tasks for test creation/update, complete required-suite execution, authorized repair/reruns, documentation increment application and verification, and implementation-result evidence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:282`.

- [A] 129. Explicit Implement/resume MUST reconcile the plan, valid approval/direct authorization, current human instructions, documentation, source content, folder access/mappings, and baseline before starting; stale, missing, or inconsistent prerequisites MUST block it.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:284`.

- [A] 130. The required suite MUST include current product tests and retained applicable earlier regressions across folders with one coverage/acceptance inventory.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:288`.

- [A] 131. Each required suite MUST run only in its declared authorized environment with satisfied infrastructure, permissions, isolation, cleanup, and compatible output locations; missing prerequisites MUST block execution and successful closure.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:288`.

- [A] 132. AIH MUST run relevant checks during tasks and the full maintained required suite before completion, repairing authorized in-scope defects and rerunning the full suite against final relevant content until passed or blocked/limited.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:290`.

- [A] 133. Automatic repairs MUST have configurable budgets and no-progress detection, defaulting to at most three unsuccessful cycles for the same unresolved failure across retries, segments, and restarts.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:292`.

- [A] 134. Repair budgets MUST support configured elapsed-time limits and reliable measured-token limits where telemetry exists; exhaustion or no progress MUST block safely with diagnosis, attempted repair, rerun evidence, and attempt history retained.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:292`.

- [A] 135. Explicit user continuation is OPTIONAL to extend a repair budget with recorded reason and scope; it MUST retain prior history and MUST NOT waive required passing tests.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:292`.

- [A] 136. AIH MUST NOT weaken, disable, remove, or reclassify tests merely to pass; expected-behavior changes MUST trace to authorized requirements, and obsolete incompatible historical versions MUST NOT run solely because archived evidence contains them.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:294`.

- [A] 137. Unrelated defects MUST be recorded for explicit human include/defer/investigate disposition; included defects MUST amend interpretation, plan, tests, documentation, and material-scope authorization, including in direct mode.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:296`.

- [A] 138. Established unfixed defects MUST remain in current known-defect documentation with stable identity, symptoms, evidence/reproduction, affected areas, impact, supported workarounds, disposition, and origin; suspected defects MUST remain unconfirmed until evidenced.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:298`.

- [A] 139. Verified repairs MUST update defect status without treating defect records as queued requests or authority for future work.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:298`.

- [A] 140. A deferred defect failing any required test MUST block successful completion without a waiver; the user may authorize repair or cancel/reject, while nonblocking deferred defects may remain documented.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:300`.

- [A] 141. Q&A findings MUST require an explicit authorized change/documentation action before durable documentation updates and MUST NOT start that action automatically.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:302`.

- [A] 142. File and portal questionnaire editing MUST share one authoritative answer source and revision checks; editing, saves, assignment, export generation, import, review persistence, and submission MUST be idle-only actions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:306`.

- [A] 143. Each question MUST include stable ID/revision, context, intended respondent, plain explanation, answer instructions, and an always-available free-text field.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:308`.

- [A] 144. Choice questions MUST state single/multiple selection rules with clear options and a meaningful reasoned recommendation where applicable; recommended choices MUST start unchecked and MUST NOT imply approval.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:308`.

- [A] 145. Questions needing facts or examples MUST use suitable free text rather than invented choices.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:308`.

- [A] 146. The framework user MUST be able to change an agent-suggested intended respondent assignment.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:308`.

- [A] 147. Clarification questions MUST address what/why and observable outcomes; implementation choices MUST be labeled as Analysis design, with missing-requirement questions returned to clarification.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:310`.

- [A] 148. Questions MUST be batched after reasonable investigation in an easy copy-paste form; later batches MUST be limited to new consequential uncertainty.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:312`.

- [A] 149. Questionnaires MUST distinguish consequential blockers from optional choices, preserve wording/revisions, and report malformed, exclusive, partial, or free-text-modified selections without guessing.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:314`.

- [A] 150. Submitted answers MUST remain linked to affected requirements, decisions, plan, and execution; agents MUST NOT issue human approval/authorization to themselves.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:316`.

- [A] 151. Each clarification round waiting for marked outstanding requestor answers MUST generate a separate UTF-8 text form with preview/download and explicit regeneration; unchanged current exports MUST be reused, superseded exports retained, and empty forms avoided.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:320`.

- [A] 152. Reopening an answered requestor topic MUST use a visible new question revision or explicit re-request with provenance.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:320`.

- [A] 153. Requestor forms MUST be completable in an ordinary text editor without AIH, account, portal, Markdown knowledge, or technical metadata editing, using compact stable references, check marks, answer/comments fields, and an I don't know / Needs discussion response.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:322`.

- [A] 154. Forms MUST include product/request title, short business summary, form identity/revision, UTC generation time, completion instructions, and usefully ordered questions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:322`.

- [A] 155. Each exported question MUST express one understandable request with an explanation of situation/terms/information needed, why it affects the change, suitable neutral illustrative examples, answer instructions, answer space, and comments/alternative space.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:324-332`.

- [A] 156. Form explanations MUST remain concise but sufficient for nontechnical readers, distinguish essential/optional answers and defaults, preserve attributed explicit technical constraints, and MUST NOT steer architecture or unapproved business decisions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:332`.

- [A] 157. Downloading/forwarding a form MUST NOT mark questions answered or prove receipt; the export MUST remain a snapshot rather than another live answer store.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:334`.

- [A] 158. The latest applicable form MUST be linked from the current response and clarification page, with prior forms/rounds retained; sharing MUST remain the user's chosen channel without implied email/message authority.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:336`.

- [A] 159. Requestor intake MUST support file selection, drag-and-drop text forms, and pasted responses, display supported types/size limits, and report actionable encoding/format errors.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:342`.

- [A] 160. Accepted intake MUST preserve original content with receipt identity and target request/form while only staging it; uploading MUST NOT invoke an agent or overwrite active answers.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:342`.

- [A] 161. Import review MUST display original question/explanation, existing answer, proposed answer, attributed respondent, and match status, including missing, unknown, duplicate, altered, contradictory, and stale items.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:343`.

- [A] 162. Review MUST offer accept-all nonconflicting matches plus per-answer accept, retain, user-correct, or leave-unresolved controls while preserving original wording and correction attribution.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:343`.

- [A] 163. Save reviewed answers MUST save authoritative answer drafts only; Import answers and clarify MUST explicitly merge reviewed answers and submit current relevant saved inputs/amendments to normal Clarify without a second generic approval dialog.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:344`.

- [A] 164. Import feedback MUST identify saved receipt/submission/round, progress, interpretation/questions/conflicts; deliberately partial submissions MUST retain consequential blockers and MUST NOT invent blank or unknown answers.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:345`.

- [A] 165. Combined import-and-Clarify MUST bind to the displayed form/question/draft/input/amendment revisions, require refresh/reconciliation of changed revisions, and protect intervening edits and unseen requirements.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:347`.

- [A] 166. The combined action MUST resolve unsaved edits before submission and be accepted as one recoverable idle operation; busy rejection MUST leave no merged drafts, submission, or queued work.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:347`.

- [A] 167. A launch failure MUST leave an inspectable saved submission, permit explicit resume only after reconciled ownership, and MUST NOT duplicate receipt/amendment effects or runs on retry.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:347`.

- [A] 168. Older-form intake MUST show original questions, propose unchanged-revision answers for review, require explicit resolution for changed/withdrawn questions, and protect newer answers.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:349`.

- [A] 169. Missing form/question references MUST offer explicit manual matching with provenance rather than positional guessing.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:349`.

- [A] 170. Wrong/closed-request forms MUST remain unassigned in current intake for correction without mutating/reopening the other request; no-request intake MUST offer read-only inspection and new-request guidance without implicit request creation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:349`.

- [A] 171. Accepted text outside recognized answer fields MUST be retained and reviewed; changed wishes may be explicitly linked as amendments or attributed input without duplicating the same change.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:351`.

- [A] 172. Requestor responses MUST NOT approve plans, enable skills, edit human instructions, expand permissions, or start implementation; reviewer/submitter and attributed source MUST remain distinct.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:351`.

- [A] 173. File-only users MUST have equivalent form export/intake/review/draft/amendment/Clarify operations and direct authoritative-file editing with the same capture/conflict rules and preserved accepted-source links.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:353`.

- [A] 174. Accepted drafts, exports, originals, reviews, submissions, and interpretations MUST remain linked in request history subject to explicit authorized redaction; unreviewed receipts MUST NOT become active answers/instructions on later runs.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:355`.

- [A] 175. Documentation MUST be maintained as normal authorized workflow work and consulted during clarification, before planning, and before implementation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:359`.

- [A] 176. Current documentation MUST cover all relevant registered folders, including read-only components, and distinguish intended requirements, observed implementation, verification, and deployment; future behavior MUST remain in its request, with approved unmet requirements explicitly statused if catalogued.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:361`.

- [A] 177. Disagreement among documentation, implementation, and intent MUST be recorded with observation separated from approved meaning; changing business meaning MUST require clarification rather than promoting inference.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:363`.

- [A] 178. Documentation updates MUST preserve human-authored content and use revision-checked reviewable changes to affected sections without requiring Git.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:365`.

- [A] 179. Documentation drift MUST be checked at run start and after relevant changes; externally managed/uninspectable components MUST retain provenance, last-known state, and explicit unknowns.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:367`.

- [A] 180. Relevant changes MUST refresh affected documentation and navigation with owning request/operation, sources, verification, and unresolved issues; partial implementation MUST expose drift rather than claim old documentation current.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:369`.

- [A] 181. Every request, including direct implementation, MUST retain a planned/applied/verified documentation increment reconciled with actual changes, or a justified no-impact finding; documentation failures MUST prevent successful completion.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:373-377`.

- [A] 182. Documentation MUST aim to specify a functionally equivalent rebuild defined by acceptance tests and undergo a recorded completeness/traceability review of business rules, interfaces, results, dependencies, acceptance, and recovery prerequisites.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:379`.

- [A] 183. Reconstruction MUST be reported as specified but not demonstrated until independent reconstruction evidence exists; ordinary tests or specification review MUST NOT imply rebuilt equivalence, bit identity, or production-data recovery.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:379`.

- [A] 184. An independent reconstruction exercise MUST NOT be a mandatory completion gate under this specification.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:379`.

- [A] 185. If an independent reconstruction exercise is explicitly authorized and performed, its scope, prerequisites, results, and remaining limitations MUST be recorded separately.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:379`.

- [A] 186. Rebuild documentation MUST inventory necessary external resources and gaps with content-versioned references to operational scripts/IaC and inert examples.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:379`.

- [A] 187. Users MUST have initial-baseline and incremental reverse-engineering modes across registered existing directories without Git, a database, or preexisting AIH documentation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:383`.

- [A] 188. Reverse-engineering inventory MUST cover authorized source, configuration, interfaces, tests, build/deployment definitions, and documentation without executing/importing inspected code/hooks/attachments or exposing credentials; unavailable folders and extraction limits MUST remain explicit.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:385`.

- [A] 189. Agent synthesis MUST document supported architecture, dependencies, domain, behavior, interfaces, flows, operations, and requirements while explicitly labeling inference, assumptions, contradictions, missing external facts, and unverified behavior.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:387`.

- [A] 190. Reverse engineering MUST write only authorized documentation and framework records, preserving implementation, source configuration, executable tests, deployment code, and human instructions; repairs/refactoring MUST require change work.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:389`.

- [A] 191. Incremental refresh MUST target changed/newly relevant material and dependencies, preserve unaffected content, and record scope, provenance, gaps, diffs, and validation without claiming structural validity alone proves documentation completeness.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:391`.

- [A] 192. Bootstrap MUST complete the authorized current workspace baseline before opening a first/new request, checking inventory, category applicability, evidence-backed coverage, provenance/unknowns, reconstruction review, catalogs, links, and tree structure.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:393`.

- [A] 193. Baseline completion MUST NOT require resolving every external uncertainty or verifying all runtime behavior; remaining unknown external facts, unverified behavior, and their limitations MUST be clearly identified and preserved.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:393`.

- [A] 194. AIH MUST NOT claim product tests passed merely because the documentation baseline is complete.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:393`.

- [A] 195. Pending idle setup MUST permit prerequisite configuration, Q&A, and drafts; after explicit successful continuation it MUST release ownership and enable request creation as a separate action.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:395`.

- [A] 196. Standalone documentation maintenance MUST require no open request; documentation inside an open request MUST use its explicit authorized task, increment, evidence, and blockers without creating another writer.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:395`.

- [A] 197. Workspace changes MUST retain prior baseline and mark affected coverage unresolved until explicit bounded reconciliation; saving the registry MUST NOT automatically reverse-engineer or waive phase boundaries, approval, or unrelated blockers.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:397`.

- [A] 198. Interrupted bootstrap/refresh MUST preserve valid progress and resume from evidence; missing profile, compatibility, authentication, or permission MUST leave semantic generation pending/partial with actionable setup or manual-handoff guidance without silent agent switching/installing.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:399`.

- [A] 199. Documentation navigation MUST let users/agents follow compact meaningful catalog summaries to relevant terminal content without loading unrelated leaves, with stable identities and one canonical topic copy.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:403-407`.

- [A] 200. Documentation catalogs MUST initially have at most eight direct children each.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:411-414`.

- [A] 201. The deepest and shallowest documentation content leaves MUST initially differ by at most one edge from the root.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:411-414`.

- [A] 202. Documentation content leaves MUST target at most 1,500 words, splitting at meaningful boundaries and recording justified exceptions for indivisible reference material.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:411-414`.

- [A] 203. Tree limits MUST be supported configuration parameters, with dynamic meaningful grouping and no unrestricted-hierarchy substitution, empty padding, or fabricated content.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:416`.

- [A] 204. Automatic tree reorganization MUST preserve human content and topic identities, assign identities to genuinely new split topics, repair links, and retain reference mappings and structural-change history.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:418`.

- [A] 205. Supported readers MUST avoid half-reorganized documentation, and consistency limitations for readers bypassing the protocol MUST be stated; search MUST supplement rather than replace tree navigation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:420`.

- [A] 206. The documentation applicability catalog MUST classify every required category as applicable, not applicable with rationale, or unknown needing investigation, generating substantive documents only where relevant.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424`.

- [A] 207. Relevant documentation MUST carry provenance, dates, source fingerprints, owning request/operation and decisions, verification status, and unresolved reviews without flattening all content into navigation catalogs.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:447-449`.

- [A] 208. Change/decision history MUST preserve stable source-linked events and historical workspace mappings with ordinary corrections appended as supersessions; essential decisions/outcomes/evidence MUST NOT be discarded as verbose logs.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:451-457`.

- [A] 209. Verbose CLI-log retention MUST be configurable, documented, and non-silent while preserving essential request history and decision evidence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:455-457`.

- [A] 210. Evidence MUST record useful summaries and observable actions without private chain-of-thought or fabricated unavailable conversations, and MUST NOT claim hashes/append-only files are tamper-proof against filesystem owners.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:457-459`.

- [A] 211. Sensitive-input screening MUST precede durable intake and prevent detected rejected values appearing in previews, spooling, temporary records, logs, indexes, or telemetry; detection MUST be described as best effort.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:461-463`.

- [A] 212. Sensitive human-owned source drafts/files MUST NOT be silently rewritten/deleted; submission MUST be refused with non-echoing correction guidance while accepted originals preserve their exact content under the redaction exception.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:463-465`.

- [A] 213. AIH MUST support explicit human-authorized historical redaction scoped to identified sensitive material in AIH-owned originals, revisions, archives, logs, indexes, temporary/recovery copies, reconciling derived records and fingerprints to prevent restoration.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:465-467`.

- [A] 214. Historical redaction MUST be recoverable without new secret-bearing backups, preserve a non-sensitive authorization/record/reason/limits audit, label redacted originals, preserve unrelated history and request scope, and invalidate affected evidence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:465-469`.

- [A] 215. Historical redaction MUST NOT authorize agent edits to human instructions or claim erasure of external exports, providers, or independent backups, and MUST obey global idle ownership.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:467-469`.

- [A] 216. Every implementation attempt, including normal/direct, resumed, failed, and cancelled work, MUST create durable initial logs/results records before changes and update them throughout execution.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:471-473`.

- [A] 217. Implementation logs MUST retain timestamps, run/segment/task and input/plan/workspace revisions, available events, action intentions/results, observed changes, tests/content versions, documentation, errors, cancellation, and checkpoints, distinguishing attempted/confirmed/failed/uncertain outcomes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:473-475`.

- [A] 218. Results summaries MUST explain requested/attempted/completed/incomplete work, actual changes, verification, documentation increment, defect disposition, blockers, uncertainty, repair budget, recovery, and next action with evidence links.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:475-477`.

- [A] 219. Crash recovery MUST reconstruct and clearly label available summaries without inventing unavailable action history, inspect uncertain effects before retry, and preserve logs/results after archival.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:477-479`.

- [A] 220. Skill discovery MUST expose compact metadata, compatibility, availability, enabled status, and locations before bodies; new installed skills MUST be discoverable without editing the entry point, with actionable malformed/disabled/duplicate/incompatible diagnostics.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:481-485`.

- [A] 221. Every delivered skill MUST work by copying its directory outside installed AIH without an exporter, engine, portal, database, fixed state path, or ordinary Git requirement; intrinsic dependencies MUST be declared with explicit input/output locations.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:485-487`.

- [A] 222. Delivered skills MUST already contain matching versioned conventions, helpers, and behavioral guidance, and MUST NOT require ordinary runs to regenerate core resources or reconstruct the whole AIH lifecycle.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:491-497`.

- [A] 223. Standalone invocations MUST record input/output locations, allowed folder identities/access, scope/effects, initiating instruction, constraints, relevant approved/direct plan authority, and results/evidence; missing consequential authority MUST block effects without inventing stronger identity assurance.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:497-499`.

- [A] 224. Requirements-only, read-only, setup, and documentation-only standalone work MUST retain its applicable authority without acquiring an implementation-plan requirement merely for permitted record/documentation writes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:497-499`.

- [A] 225. Standalone portability MUST preserve the same per-folder and host boundaries without AIH global state; examples, metadata, and effects declarations MUST NOT grant permissions or widen roots.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:499-501`.

- [A] 226. The initial delivery MUST include eight complete standalone packages with seven core skills enabled by default and git-workflow installed but disabled; enabled, available, installed, and authorized MUST remain distinct.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:503-507`.

- [A] 227. A required disabled/unavailable skill MUST block with actionable guidance rather than silently skipping work or enabling a substitute.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:503-505`.

- [A] 228. Standalone clarify-requirements MUST support iterative rounds, explained text forms, import review, and amendments using explicit permitted local input/output locations without requiring a portal or another installed skill.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:519`.

- [A] 229. Direct-mode standalone implement-plan MUST include its own required analysis/planning guidance and helpers; cross-skill reuse MUST remain self-contained without adding a Plan workflow stage or fabricating approval.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:521`.

- [A] 230. Test diagnosis MUST NOT authorize unrelated repairs; implementation performs scoped fixes, and skill execution MUST preserve repair budgets, required-test gates, and attempt history.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:523`.

- [A] 231. Reverse engineering and documentation maintenance MUST share reusable evidence without competing baselines; read-only questions MUST NOT invoke documentation-writing effects.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:525`.

- [A] 232. The CLI and portal MUST expose consistent installed skill catalogs, purposes, outputs, boundaries, usage links, and diagnostics without duplicating full instructions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:531`.

- [A] 233. Discovery MUST report stale/missing catalog entries and integrity/identity conflicts; it MUST NOT bypass those problems to execute packages.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:544`.

- [A] 234. Skill configuration MUST change only while idle, record when it applies, and preserve historical skill/version references; it MUST NOT install or authorize skills or regenerate core catalogs.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:546`.

- [A] 235. Discovery/metadata MUST NOT execute package code, install dependencies, trigger dynamic imports, or change trusted executable settings.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:550`.

- [A] 236. AIH MUST provide functional Codex CLI integration, manual handoff, and multiple named profiles/adapters without coupling profile names to agents.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:554`.

- [A] 237. Profiles MUST support defaults, per-capability assignment, and explicit per-run selection with documented precedence and recorded effective segment selection.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:556`.

- [A] 238. Ordinary requests and generated content MUST NOT change privileged executable configuration; deliberate local administration MUST validate adapter-supported settings and reject arbitrary commands or unrestricted arguments.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:558`.

- [A] 239. Profile diagnostics MUST report executable/version, compatibility, confinement, and supported authentication status with actionable guidance, distinguishing credential presence from verified service access and never automatically installing/upgrading CLIs.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:560`.

- [A] 240. Adapters MUST support declared availability/start/events/identities/exit/timeout/cancellation/resumption capabilities; unavailable native resume MUST use a clearly labeled new segment from persisted state without silent agent switching.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:564`.

- [A] 241. Adapters unable to represent and enforce all required writable/read-only roots under host controls MUST block launch rather than widen to a common ancestor, omit roots, relocate content, or suppress inherited approvals/restrictions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:566`.

- [A] 242. Unavailable noninteractive approval handling MUST safely end/stop and offer manual handoff after reconciled ownership; profile/capability changes MUST apply only to the next explicit action/segment, not a live process.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:570`.

- [A] 243. Manual handoff MUST reserve the sole action slot before executable instructions are exposed, bind scope and authority to a unique identity, survive restarts, and MUST NOT label prepared work as actually running.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:572`.

- [A] 244. Returned output MUST NOT itself release handoff ownership or prove completion; Stop/release MUST request external termination, obtain human stopped/never-started confirmation, reconcile files/evidence, and retain uncertain attribution.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:572`.

- [A] 245. Uncertain external termination MUST retain the reservation and block competing operations; stale heartbeat, browser closure, and lock deletion MUST NOT imply termination.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:572`.

- [A] 246. Interrupted cross-filesystem work MUST preserve per-root progress and reconcile partial outcomes without claiming whole-product atomic commits or silently overwriting competing edits.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:586`.

- [A] 247. Direct source edits MUST invalidate affected evidence and require safe reconciliation; stale-lock recovery MUST check process identity rather than treating lock deletion as termination.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:592`.

- [A] 248. Stop MUST allow incomplete tasks/segments to terminate safely after an indivisible operation or controlled termination, preserving unfinished evidence instead of waiting for whole-task success.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:594`.

- [A] 249. Resume/recovery MUST recheck current files, approvals, processes, evidence, root identity/access, and authority, inspect prior success before retry, and preserve uncertain effects rather than blindly duplicating external writes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:596`.

- [A] 250. Verification MUST bind to actual checked relevant content including uncommitted/non-Git files and current root configuration; changes MUST invalidate affected evidence and Ready to close.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:598`.

- [A] 251. Stop, cancellation, and timeouts MUST safely terminate child processes on supported platforms, preserve partial results, and keep Stop/status available until termination or external release is confirmed.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:602`.

- [A] 252. The local portal MUST start from the single framework home, default to loopback, support port/no-browser options, report URL and browser/port/shutdown failures cleanly, and only auto-launch a browser with confined writes; otherwise it MUST provide a URL for independent opening.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:608`.

- [A] 253. The portal MUST serve one local user without requiring a shared server, cloud account, database, or Git, using clear action-oriented language.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:610`.

- [A] 254. First portal startup with absent product state MUST automatically initialize and begin configured-agent documentation baselining for the validated home and explicitly preconfigured roots, without enrolling neighbors or selecting opportunistically discovered agents.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:612`.

- [A] 255. Setup MUST show responsive phase/progress/gaps/errors/input status and retain an operation identity across refresh/concurrent starts; reopening MUST NOT restart a safely stopped operation without explicit continuation.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:614`.

- [A] 256. Setup MUST distinguish absent, recoverable partial, invalid, and complete state, preserve invalid/human files, and MUST NOT regenerate a completed baseline on every launch.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:616`.

- [A] 257. Missing usable profile/authentication MUST retain safe deterministic setup and visibly pending semantic generation with explicit setup/manual continuation and no false completion.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:618`.

- [A] 258. The portal MUST provide Overview, Current request, Ask a question, Product documentation, Runs and recovery, History and decisions, Settings, and Help pages over the same records and operations as the CLI.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:620-629`.

- [A] 259. Overview MUST show current request/phase, next action, blockers, response, test/documentation status, workspace availability, selected profile, distinct setup/reconciliation progress, and available token usage; Start request MUST require idle/no request/current complete baseline.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:622`.

- [A] 260. Ask a question MUST show editor, attachments, explicit Ask, progress, answer/source links, and history, with operational editing/intake disabled while busy and existing answers readable.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:624`.

- [A] 261. Product documentation MUST show progressive navigation, breadcrumbs/search, applicability, source provenance/dates/freshness, defects, reviews, current-state notices, per-area coverage, and explicit permitted refresh/reconciliation actions with truthful reconstruction status.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:625`.

- [A] 262. Runs and recovery MUST show current/prior runs, sanitized events, task/segment progress, checkpoints, errors, summaries/evidence, usage, and permitted Stop/resume/recovery with distinct system-operation and product/process outcomes.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:626`.

- [A] 263. History and decisions MUST expose closed-request summaries/dates/outcomes and a separate ledger tab, load full history only on selection, retain evidence links, and MUST NOT reopen or queue work.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:627`.

- [A] 264. Settings MUST expose Workspace, profiles/defaults/capability assignments, compatibility/authentication diagnostics, searchable Skills metadata/details, supported settings, and human-only custom instructions, with privileged settings distinct and busy controls disabled.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:628`.

- [A] 265. Help MUST offer searchable maintained guidance, walkthroughs, workflow/authorization, commands, locations, examples, troubleshooting/recovery/limits, and contextual stable links.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:629`.

- [A] 266. Workspace settings MUST list fixed home, registry revision, stable folder IDs/names, canonical paths, purposes, access modes, availability, baseline, and reassessment, explaining the one product/request/owner and central state.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:631`.

- [A] 267. Workspace settings MUST offer human Add folder, Edit, Validate access, Remove from workspace, Save changes, and Cancel, preserve stable IDs, validate only selected/configured roots, reject stale/invalid saves, and discard only unsaved forms on Cancel.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:633`.

- [A] 268. Workspace validation MUST NOT browse arbitrary ancestors/siblings or write probes to read-only/unregistered candidates; unproven access MUST be reported for later authorized checking.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:633`.

- [A] 269. Before saving workspace changes, the UI MUST explain affected coverage/dependencies and unknown impacts; afterward it MUST show pending reconciliation and affected withdrawn approval/readiness/evidence without launching work or hiding retained obligations.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:635`.

- [A] 270. Current request MUST have Input and clarification, Analysis, Plan, Implementation, Verification and documentation, and Outcome tabs.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:637-644`.

- [A] 271. Input and clarification MUST show inputs/attachments, draft/submitted differences, Save/Clarify, canonical interpretation, questionnaires and assignments, requestor preview/download/intake/review, amendments/history, round results, and the pending submission set with busy-state restrictions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:639`.

- [A] 272. Analysis MUST show repeatable Analyze, progress, assessment, question catalog, optional supporting analysis, and explicit include/defer/investigate selections without a separate Plan command.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:640`.

- [A] 273. Plan MUST show revision, interpretation/workspace sources, ordered folder-qualified tasks, tests/docs, differences, approval, and missing/read-only/unreconciled blockers; approval alone MUST NOT execute.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:641`.

- [A] 274. Implementation MUST expose Implement, Implement directly, Resume, Stop, sequential progress, events, file evidence, logs, and summaries with a clear explanation of direct-mode limits.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:642`.

- [A] 275. Verification and documentation MUST show required results/checked versions/root revision, failed/unexecuted checks, repair attempts, documentation increment/applied changes/gaps, reconciliation, and evidence without accept-failure shortcuts.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:643`.

- [A] 276. Outcome MUST show fulfillment, unmet gates, defects, and summary with distinct idle cancelled/rejected/successful closure, Ready to close retaining the open slot, and current-gate revalidation before archival.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:644`.

- [A] 277. The portal MUST retain a product/request/phase/execution/profile header with empty/setup states and prominent idle next actions, visible ownership/disabled reasons while busy, and clarification waiting/readiness distinctions without automatic stage advancement.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:646`.

- [A] 278. Human-facing pages MUST use ordinary language with IDs, hashes, and technical evidence available on demand.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:646`.

- [A] 279. Save, upload, submit/run, Stop, and closure MUST remain visibly distinct; combined Import answers and clarify MUST clearly disclose its execution effect and unavailable actions MUST explain the specific cause.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:648`.

- [A] 280. Revision conflicts MUST display competing changes and explicit resolution without overwrites; live events MUST be sanitized and routine progress understandable without raw-log inspection.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:650`.

- [A] 281. Handoff UI MUST distinguish prepared/reserved, evidenced external running, Stop requested, awaiting confirmation, reconciliation, and released states, exposing only the narrow Stop-release flow while reserved.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:654`.

- [A] 282. The portal MUST protect against traversal, link escapes, arbitrary filesystem access, cross-origin writes, and active untrusted rendering; product HTML/scripts/hooks/attachments MUST NOT execute.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:656`.

- [A] 283. The portal MUST NOT expose generic arbitrary-command execution or retain credential values in configuration, tracked files, outputs, or logs.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:658`.

- [A] 284. Users MUST have a shared terminal menu with Open portal, status, profile checks, Workspace settings, initialization/reverse engineering, validation, inspect/resume, help, Exit, and Stop-only operational choices while busy.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:664-668`.

- [A] 285. Startup MUST support direct Windows/Linux Python commands and actionable missing-runtime guidance without automatic installation or universal double-click claims.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:666`.

- [A] 286. Startup MUST resolve home independently of current directory, handle spaces/special characters, deduplicate portal/worker launches, and MUST NOT start product work merely by opening menu/help or silently cancel/close on menu Exit.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:670`.

- [A] 287. The quick start MUST document purpose, prerequisites, local installation, platform/direct startup, first-run baseline, profiles, workspace/home/access, basic and direct workflows, Q&A, troubleshooting, and help.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:674`.

- [A] 288. The detailed guide MUST cover all delivered lifecycle, requestor exchange, amendments, authorization, tests/defects/budgets, documentation, profiles/skills/instructions, recovery/history, workspace scope/reconciliation, confinement, redaction, standalone use, maintenance, retention, and limitations, with realistic multi-folder recovery examples.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:676,787-789`.

- [A] 289. Shared help MUST support local navigation/search before initialization/authentication without an agent run, use stable valid installed-version anchors, and MUST NOT modify the core during ordinary reading.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:678`.

- [A] 290. The CLI MUST make installation, workspace administration, initialization, inventory/reverse engineering, helper discovery, validation, skills, profiles, menu, portal, help, lifecycle, form/import/amendment exchange, Q&A, handoff/release, and upgrade/migration operations discoverable with consistent arguments and per-command help.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:682-699`.

- [A] 291. Installation and repeated initialization MUST preserve existing files and human content, make initialized templates product-owned, and MUST NOT silently merge incompatible schemas.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:701`.

- [A] 292. Host integration MUST offer a short entry-point snippet without replacing existing agent instructions; direct operation MUST work without adding integration files.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:703`.

- [A] 293. Upgrades MUST validate incoming version/core and installed modifications, preserve product content and workspace history, identify migrations, and support recoverable replacement without moving home or installing duplicate cores in added roots.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:705`.

- [A] 294. Installation, upgrade, migration, rollback, and cleanup MUST stay in currently authorized writable roots including indirect effects; former membership MUST NOT authorize recovery writes, and artifacts MUST NOT be externally published or assigned invented release URLs.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:705`.

- [A] 295. Optional Git enablement MUST NOT require a common repository or automatically authorize commits, pushes, PRs, integration, deployment, destructive actions, or outside-root side effects.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:707`.

- [A] 296. A real Codex CLI smoke test MUST run when installed, authenticated, and permitted in a compatible isolated confined fixture; absent prerequisites MUST be reported as not live-tested, and multi-root live support MUST NOT be inferred from single-root execution.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:777`.

- [A] 297. Delivery validation MUST include a rendered portal walkthrough of primary screens and Workspace settings and distinguish automated checks, real agent execution, browser review, tested platforms, and actual storage assumptions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:779`.

- [A] 298. Delivery MUST demonstrate the full baseline-to-explicit-successful-closure workflow with iterative clarification/requestor exchange/amendments/Analysis, sequential implementation, full tests, and applied documentation, plus the specified alternate/recovery and multi-root cases as labeled synthetic fixtures.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:781`.

- [A] 299. Delivery MUST include the working core, conventions/templates, all eight complete standalone skills and catalogs, CLI/menu/optional launchers, complete portal, tests/fixtures including requestor exchanges and amendment history, quick start, and detailed shared help.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:785`.

- [A] 300. The final delivery report MUST trace major requirements to implementation and actual evidence, state exact installation/startup/first-use commands, tested platforms/real Codex execution/failures/missing checks/limits, and MUST NOT equate unit-test success with full verification or silently reduce scope.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:791-793`.

- [A] 301. The documentation applicability catalog MUST cover product purpose, scope, capabilities, stakeholders, users, terminology, domain knowledge, and definitions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,428`.

- [A] 302. The documentation applicability catalog MUST cover business requirements, rules, processes, acceptance criteria, and requirement-to-implementation-to-test traceability.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,429`.

- [A] 303. The documentation applicability catalog MUST cover nonfunctional requirements, service objectives, performance, capacity, availability, accessibility, localization, and supported platforms.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,430`.

- [A] 304. The documentation applicability catalog MUST cover architecture, component responsibilities, solution design, architectural decisions, alternatives, and tradeoffs.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,431`.

- [A] 305. The documentation applicability catalog MUST cover product/workspace structure, registered folder IDs, purposes, access modes, component ownership, cross-folder dependencies, important paths and entry points, without assuming repositories exist.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,432`.

- [A] 306. The documentation applicability catalog MUST cover data structures, logical and physical models, storage, data ownership, lineage, quality, retention, privacy, and migrations.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,433`.

- [A] 307. The documentation applicability catalog MUST cover ETL and transformations, pipelines, orchestration, schedules, semantic models, reports, dashboards, and analytics definitions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,434`.

- [A] 308. The documentation applicability catalog MUST cover algorithms, functional logic, APIs, interface contracts, integrations, events, queues, and external services.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,435`.

- [A] 309. The documentation applicability catalog MUST cover UI definitions, visual and interaction design, web interfaces, navigation, user flows, error behavior, and user help.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,436`.

- [A] 310. The documentation applicability catalog MUST cover networking, authentication, authorization, roles, secrets references, threat models, security controls, and relevant compliance constraints.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,437`.

- [A] 311. The documentation applicability catalog MUST cover dependencies, versions, licenses, build requirements, configuration, feature flags, and environment differences.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,438`.

- [A] 312. The documentation applicability catalog MUST cover deployment procedures and script references, releases, infrastructure, cloud services, resource inventories, and relevant cost assumptions.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,439`.

- [A] 313. The documentation applicability catalog MUST cover unit, integration, system, acceptance, performance, and security testing; test data, fixtures, expected results, and evidence.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,440`.

- [A] 314. The documentation applicability catalog MUST cover backup, recovery, disaster recovery, restore validation, operational continuity, and rebuild prerequisites.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,441`.

- [A] 315. The documentation applicability catalog MUST cover logging, monitoring, alerting, incident response, troubleshooting, administration tools, and support interfaces.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,442`.

- [A] 316. The documentation applicability catalog MUST cover operational processes, schedules, maintenance, data operations, escalation, and handover.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,443`.

- [A] 317. The documentation applicability catalog MUST cover user guides, onboarding, administration guides, support materials, known limitations, a dedicated known-defects catalog, deprecation, and retirement.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,444`.

- [A] 318. The documentation applicability catalog MUST cover any additional product-specific knowledge needed to preserve its definition and support functional reconstruction.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:424,445`.

- [A] 319. Genuinely inapplicable checks MUST be defined explicitly rather than inventing passing test results.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:223`.

- [A] 320. Human file-based workspace configuration edits MUST pass the same explicit administrative contract; file contents or claimed identity alone MUST NOT establish authorization.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:120`.

- [A] 321. The framework Save operation MUST be documented for file-only users who need every amendment revision captured.
  Source: `../AIH_Build_Prompt_v20260922_173409Z.md:243`.
