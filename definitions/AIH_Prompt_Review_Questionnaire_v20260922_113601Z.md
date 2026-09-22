# AIH build-prompt review and decision questionnaire

Questionnaire version: `20260922_113601Z`  
Generated (UTC): 2026-09-22 11:36:01Z  
Reviewed file: `AIH_Build_Prompt_v20260922_095100Z.md`  
Status: **Review findings and proposed decisions. The build prompt has not been changed.**

## How to complete this questionnaire

Select **one option per question** by changing `[ ]` to `[x]`. Every question includes **C — Leave as is**, which retains the current specification, including the described ambiguity or tradeoff. Recommendations are suggestions; none is preselected.

Choose D if you prefer a different solution, then describe it in the comments field. Comments may also modify A, B, or C. Blank questions remain unanswered; they do not authorize the recommendation or imply acceptance of the current behavior. You can return the completed file or reply using selections such as `Q01=A, Q02=B`, with any modifications.

Each question explains the issue, its practical consequence, the relevant prompt sections, and the proposed alternatives. Section references are to the reviewed build prompt, not to this questionnaire.

## Review assessment

The prompt gives substantial coverage to the main workflow, the single active request, explicit submissions, mandatory passing tests, documentation, standalone skills, and requestor answer handling. The review identified **14 consequential findings**: operational decision gaps and one policy tension where exact preservation can conflict with redaction. These are specification findings; they are not claims that an implemented framework has already failed.

The recommendations build on the agreed requirements; alternatives that change an operational policy or add validation scope say so explicitly. This questionnaire does not propose adding Git or a database as defaults, abandoning standalone skills, weakening the all-required-tests-pass rule, introducing a backlog, or reopening the strict documentation-balancing choice. The separate detailed portal UX/theme proposal remains unapproved and its absence here is not counted as an issue.

Routine implementation choices have been excluded unless they materially affect visible behavior, authority, recovery, or an existing guarantee. Overlapping findings have been consolidated.

| Question | Decision |
|---|---|
| Q01 | Pending commands and the meaning of Stop |
| Q02 | What establishes a safe execution boundary? |
| Q03 | Current documentation after cancellation or rejection |
| Q04 | Who closes a successfully completed request? |
| Q05 | Starting work before initial documentation is complete |
| Q06 | Core repair and upgrades during an open request |
| Q07 | Execution ownership during manual handoff |
| Q08 | Repeated unsuccessful test repairs |
| Q09 | Required tests that affect external systems |
| Q10 | Documentation bookkeeping during Clarify |
| Q11 | Evidence for reconstruction from documentation |
| Q12 | Original records that contain sensitive values |
| Q13 | Authorization for skills used outside AIH |
| Q14 | Storage environments covered by recovery guarantees |

## Questions

### Q01 — Pending commands and the meaning of Stop

**Finding type:** Workflow decision gap  
**Source:** §5 Input submission; §7 Iterative Clarify; §15 recovery; §16 stop controls

**Relevant wording:** “keep the submission pending and show its status”; “Preserve the requested Clarify action at that checkpoint”.

**Issue and consequence:** The prompt permits new commands while an agent is running, but does not define how several pending commands replace or follow one another. It also leaves unclear whether Stop cancels waiting execution. For example, you submit Clarify during implementation and then press Stop; the worker might stop and immediately launch the waiting Clarify. A later Analyze could also start automatically after it, although you expected work to remain stopped.

**Your decision:** How should pending commands be handled, and what should Stop stop?

- [ ] **A — Recommended.** **One pending execution action per request; Stop suspends all dispatch.** A later command must explicitly replace or cancel the pending action. Preserve every submitted input revision. Stop halts the current process safely and cancels automatic dispatch of waiting actions; the saved content remains available for your next explicit command. This keeps the portal behavior easy to predict.

- [ ] **B — Alternative.** **Show an ordered list of pending actions for the same request.** Each entry names its action and input revision. Stop affects only the running action; add a distinct Stop all execution control that also prevents dispatch of waiting actions. This offers more automation but requires managing the list; it must never queue another change request.

- [ ] **C — Leave as is.** Keep the current general pending-submission and Stop rules. The implementer chooses replacement, ordering, and cancellation behavior.

- [ ] **D — My own approach.** Describe it below.

**Comments / modifications:**
When an action is running, no other actions are allowed. Only Stop button is enabled. When the current actions is completed or the user presses Stop and it completes safely, only then the user can choose other action. 
____________________________________________________________

____________________________________________________________ 

Related: Q02 defines the safe handoff point; Q07 covers external manual execution.

### Q02 — What establishes a safe execution boundary?

**Finding type:** Operational contract gap  
**Source:** §5 controlled checkpoints; §7 iterative commands; §§14–15 adapter and worker recovery

**Relevant wording:** “only at a controlled checkpoint”; “Do not label work safely stopped or permit another writer when a child process may still be changing files.”

**Issue and consequence:** The prompt requires safe checkpoints but does not specify the minimum acknowledgement that proves the previous agent has yielded control. A saved progress message does not establish that the agent will refrain from starting another edit. Without a clear handoff, the portal and agent can disagree about which submitted revision is active.

**Your decision:** When and how should submitted changes become active?

- [ ] **A — Recommended.** **Use an explicit agent/worker handoff before consequential operations and at task boundaries.** Check for pending submissions at those points; confirm that current effects have settled, record a checkpoint, and yield write ownership before switching action or revision. An indivisible operation can finish first. If an adapter cannot cooperate, finish or stop its segment and confirm termination before adopting changes.

- [x] **B — Alternative.** **Adopt changes only between complete plan tasks or completed agent segments.** Use a recorded, acknowledged handoff at these boundaries. This is simpler but may leave an amendment waiting through a long task. Stop remains available under the existing safe-termination rules.

- [ ] **C — Leave as is.** Retain the general controlled-checkpoint rule and leave its timing and acknowledgement protocol to the implementation.

- [ ] **D — My own approach.** Describe it below.

**Comments / modifications:**

____________________________________________________________

____________________________________________________________

Q01 controls which pending action is adopted once this boundary is reached.

### Q03 — Current documentation after cancellation or rejection

**Finding type:** Lifecycle and documentation gap  
**Source:** §3 current documentation versus historical requests; §7 unsuccessful closure; §9 partial-change drift

**Relevant wording:** “Do not automatically roll back files.”; “record known drift and reconcile it on resumption”.

**Issue and consequence:** Cancelled or rejected requests retain partial product changes, while documentation reconciliation after an interruption is described as happening on resumption. A cancelled request never resumes. For example, a changed interface remains in the product after cancellation, but the current documentation still describes the earlier interface. Drift checks help expose this, yet no explicit next workflow owns reconciliation after archival.

**Your decision:** How should retained changes and stale documentation be carried forward when an unfinished request closes?

- [x] **A — Recommended.** **Allow closure with a persistent current-state notice.** Record retained changes, affected documentation, unresolved defects, verification uncertainty, and links to archived evidence as part of closure. Require the next authorized work to reconcile the affected knowledge before relying on it. Cancellation does not require passing tests or a full documentation rewrite, so it cannot trap the only active-request slot.

- [ ] **B — Alternative.** **Attempt documentation reconciliation before closure.** Describe the actual partial implementation and its uncertainties before archival. If reconciliation cannot finish, permit an explicit incomplete-closure outcome with a durable outstanding documentation obligation. This produces a clearer baseline when feasible but adds work to cancellation.

- [ ] **C — Leave as is.** Keep the existing drift markers and run-start checks, without specifying a reconciliation owner or carry-forward contract for unsuccessful closure.

- [ ] **D — My own approach.** Describe it below.

**Comments / modifications:**

____________________________________________________________

____________________________________________________________

Related: Q05 concerns which workflow can own incomplete setup work; Q10 concerns limited documentation writes during clarification.

### Q04 — Who closes a successfully completed request?

**Finding type:** User-visible behavior ambiguity  
**Source:** §7 lifecycle and completion gates; §16 Outcome; §17 close command

**Relevant wording:** “Close successfully when every completion condition is satisfied.”; “Successful completion is exposed only after every required gate passes.”

**Issue and consequence:** The completion conditions are clear, but the prompt does not explicitly say whether the agent automatically archives a successful request or waits for the user to close it. These lead to different experiences: the only active-request slot may become free immediately, or remain occupied until you review and click Close.

**Your decision:** Once every completion gate passes, should successful closure be automatic or explicitly requested?

- [ ] **A — Recommended.** **Automatically close successfully within the authorized execution workflow.** After validating all gates, finalize evidence, archive the request, and present its results. Cancelled/rejected closure remains user initiated. This avoids an extra step and releases the active-request slot when the work is done.

- [x] **B — Alternative.** **Require an explicit Close successfully action.** Mark the request Ready to close and present the results for review. Only your close command archives it and releases the slot. This adds a final review opportunity without weakening any completion gate.

- [ ] **C — Leave as is.** Keep the existing completion conditions and leave the choice of automatic versus manual successful closure to the implementer.

- [ ] **D — My own approach.** Describe it below.

**Comments / modifications:**

____________________________________________________________

____________________________________________________________

### Q05 — Starting work before initial documentation is complete

**Finding type:** Bootstrap/request transition gap  
**Source:** §9 reverse engineering ownership; §16 first startup, pending setup, and Overview

**Relevant wording:** “exclusive recoverable bootstrap operation”; “Offer Start request only when no request is open.”

**Issue and consequence:** Initial documentation may remain pending because an agent is unavailable. The portal also offers a new request when none is open, while later documentation maintenance must belong to an open request. If you start a request before baselining finishes, the prompt does not specify whether the old setup operation can resume separately, transfers its remaining work, or prevents progress.

**Your decision:** When may the first request proceed if initial documentation is still incomplete?

- [ ] **A — Recommended.** **Allow drafting after valid initialization, then establish an affected-scope baseline before opening the request.** Through an explicit setup action, use the existing exclusive setup operation to document enough of the proposed request’s affected scope for analysis. Record a partial-setup handoff, its remaining gaps, and the end of its write ownership before opening the request. Analysis can then plan further required documentation tasks within that request; unrelated baseline gaps remain visible for later authorized maintenance. This permits earlier progress than a complete-product baseline and does not create an implicit documentation-writing exception during Clarify.

- [x] **B — Alternative.** **Finish the initial documentation baseline before opening a request.** Continue setup, Q&A, and local drafting while setup is pending. After a documented baseline-completion check, enable request creation. Unknown external facts may remain explicitly recorded; baseline completion must not mean that every real-world uncertainty is resolved.

- [ ] **C — Leave as is.** Retain separate setup and request rules without defining the readiness check or ownership transition between them.

- [ ] **D — My own approach.** Describe it below.

**Comments / modifications:**

____________________________________________________________

____________________________________________________________

This concerns initial setup, not permission to continue unrelated implementation while an active request is blocked.

### Q06 — Core repair and upgrades during an open request

**Finding type:** Maintenance ownership gap  
**Source:** §2 immutable core and missing helpers; §13 generated bundles; §17 upgrades and migrations

**Relevant wording:** “Core installation, explicit maintenance, and upgrades are separate operations.”; “Changes to helpers use the explicit core-maintenance workflow.”

**Issue and consequence:** Core maintenance is allowed, including fixing a helper that blocks work, but its timing relative to an open request is unspecified. A paused or external agent may still expect an older helper or schema. Replacing the core while that agent can continue would mix execution contracts and make its saved evidence harder to interpret.

**Your decision:** Under what conditions may the core be repaired or upgraded?

- [ ] **A — Recommended.** **Allow maintenance with an open request only after all execution owners are safely stopped.** Record a maintenance operation, check versions, migrate affected artifacts where supported, and reassess affected approval/evidence. Resume explicitly afterward. Resolve external handoff ownership first. This allows repairing a broken helper without forcing request cancellation.

- [x] **B — Alternative.** **Require no open request before core maintenance or upgrades.** Also require all setup, maintenance, and external writers to be stopped. This simplifies version boundaries, but an open request blocked by a broken helper may need to be cancelled before repair.

- [ ] **C — Leave as is.** Keep maintenance and upgrade requirements without an explicit gate for active workers, external handoffs, or open requests.

- [ ] **D — My own approach.** Describe it below.

**Comments / modifications:**

____________________________________________________________

____________________________________________________________

Q07 defines the external-handoff reservation that must be resolved before option A can proceed.

### Q07 — Execution ownership during manual handoff

**Finding type:** Manual recovery decision gap  
**Source:** §14 manual handoff; §15 writer exclusion; §16 handoff and evidence

**Relevant wording:** “execution takes place in an external agent”; “Do not label work safely stopped or permit another writer when a child process may still be changing files.”

**Issue and consequence:** The framework can inspect its own worker processes, but a manually started external agent may not be one of them. If you start that agent, close the portal, and later press Resume, AIH needs a clear rule for whether the external agent still owns write access. Otherwise two agents could work on the same request at once.

**Your decision:** How should a manual handoff reserve and release execution ownership?

- [x] **A — Recommended.** **Create an explicit handoff reservation.** Bind it to the request, scope, submission, plan, and handoff ID. Prevent another change-work writer until you confirm external execution has stopped and AIH reconciles current files and returned evidence. Draft/intake operations and permitted read-only questions stay available; another Clarify, Analyze, or implementation execution must wait for the controlled handoff. Record uncertainty when external termination cannot be verified.

- [ ] **B — Alternative.** **Hand off one bounded task at a time.** Reserve the sole change-work writer for that task and reconcile/release ownership before handing off or resuming the next one. This reduces the amount of uncertain external work, at the cost of more manual exchanges.

- [ ] **C — Leave as is.** Keep the general handoff/evidence rules and let the implementer decide how external ownership is released.

- [ ] **D — My own approach.** Describe it below.

**Comments / modifications:**

____________________________________________________________

____________________________________________________________

Neither option claims that AIH can technically restrain an unrelated external process with unrestricted filesystem access.

### Q08 — Repeated unsuccessful test repairs

**Finding type:** Missing repair-loop stopping rule  
**Source:** §7 test repair loop; §2 token efficiency; §14 process timeouts

**Relevant wording:** “rerun the complete suite after repairs until it passes”; “An in-scope repairable failure starts this repair loop; it does not by itself require another authorization.”

**Issue and consequence:** The mandatory all-tests-pass requirement is intentional. The gap is what happens when several attempted fixes make no progress. A per-process timeout does not define how many repair cycles may continue across resumed segments. An intermittent or misunderstood failure could cause repeated changes and full-suite runs without a useful result.

**Your decision:** When should automatic repair pause for your direction?

- [x] **A — Recommended.** **Use a configurable repair budget and no-progress detection.** As an initial default, pause after three unsuccessful repair cycles for the same unresolved failure; support explicit time limits and measured token limits where telemetry exists. Preserve attempts and evidence, mark the request blocked, and offer a next decision. An explicit continuation can extend the budget without erasing history. Required failed or unexecuted tests still prevent successful completion.

- [ ] **B — Alternative.** **Pause after each unsuccessful repair cycle.** Show the attempted fix and test results, then wait for your explicit Resume command. This provides tighter control but adds frequent interaction.

- [ ] **C — Leave as is.** Keep repair-until-passing behavior, relying on agent judgment, existing process timeouts, and your Stop command instead of a defined repair-loop budget.

- [ ] **D — My own approach.** Describe it below.

**Comments / modifications:**

____________________________________________________________

____________________________________________________________

### Q09 — Required tests that affect external systems

**Finding type:** Test authorization/environment gap  
**Source:** §7 complete required suite and separate deployment authority; §15 recorded test environment; §2 registered test execution

**Relevant wording:** “The required test suite covers the current product tests and retained applicable regression tests from earlier change requests.”; “Record test selection, commands or invocation identifiers, results, environment, and checked versions.”

**Issue and consequence:** The full test suite may contain checks that write to shared databases, use paid services, or trigger external operations. The prompt requires complete execution and respects authorization, but does not define how such test effects are declared or what environment is acceptable. A routine verification command could therefore have effects beyond local testing.

**Your decision:** How should required tests with external or consequential effects be governed?

- [x] **A — Recommended.** **Require a test-run contract for each registered suite.** Declare its environment, prerequisites, expected effects, isolation/cleanup needs, and applicable authorization. Use configured test environments; execute only when those conditions hold. Missing permission or infrastructure blocks that required check and successful completion rather than silently skipping it. This preserves the full-suite requirement.

- [ ] **B — Alternative.** **Automatically run only local isolated checks.** Run other required checks through a separate explicit user action or controlled manual handoff, recording their evidence against the same checked content. The request remains incomplete until all required results are available.

- [ ] **C — Leave as is.** Retain the general authorization and full-suite rules while leaving test-effect classification and environment policy to implementation.

- [ ] **D — My own approach.** Describe it below.

**Comments / modifications:**

____________________________________________________________

____________________________________________________________

### Q10 — Documentation bookkeeping during Clarify

**Finding type:** Overlapping responsibility rules  
**Source:** §7 clarification write scope and unrelated defects; §9 authorized documentation work

**Relevant wording:** “Clarification may write its requirements, questions, evidence references, responses, and workflow records.”; “Maintain all established unfixed defects in the current product documentation's known-defects area”.

**Issue and consequence:** Clarify is requirements-focused and lists its permitted records. Elsewhere, established unfixed defects must appear in current documentation, and documentation work inside a request must be authorized. When Clarify discovers a confirmed existing defect, it is unclear whether it may immediately update the known-defect entry or must stage the finding for a later documentation task.

**Your decision:** What limited documentation changes may clarification perform?

- [x] **A — Recommended.** **Explicitly allow factual defect and freshness bookkeeping.** Clarify may add an evidence-backed known-defect entry or mark an affected topic stale, with request/source links. It may not redesign behavior, repair the product, rewrite substantive business documentation, or silently approve inferred requirements. This keeps current knowledge honest while preserving the what-and-why boundary.

- [ ] **B — Alternative.** **Keep clarification findings entirely in request records until an authorized documentation task applies them.** Show their pending status prominently and require the later task before successful completion. If the request is cancelled, use the chosen Q03 carry-forward rule. This narrows Clarify writes but delays the canonical documentation update.

- [ ] **C — Leave as is.** Keep the present clarification, known-defect, and documentation rules without explicitly settling this overlap.

- [ ] **D — My own approach.** Describe it below.

**Comments / modifications:**

____________________________________________________________

____________________________________________________________

Q03 determines what happens to any deferred documentation obligation after unsuccessful closure.

### Q11 — Evidence for reconstruction from documentation

**Finding type:** Acceptance evidence gap  
**Source:** §9 rebuild target; §11 coverage; §18 acceptance tests and synthetic fixtures

**Relevant wording:** “recreate a functionally equivalent product and demonstrate equivalence through documented acceptance tests”.

**Issue and consequence:** The prompt promises documentation sufficient for functional reconstruction. Its acceptance exercises check structure, links, drift, and product changes, but do not require a separate product to be reconstructed from that documentation. All those checks could pass while an essential business rule exists only in the original source.

**Your decision:** What evidence should demonstrate the reconstruction target?

- [ ] **A — Recommended.** **Add an independent reconstruction exercise for the synthetic product fixture.** Give a separate build only the generated documentation, declared external prerequisites, and documented acceptance criteria; keep original implementation source unavailable. Verify the reconstructed product with an independently retained acceptance oracle derived from the specified behavior. This demonstrates the fixture only. For real products, separately report readiness, unresolved gaps, and whether reconstruction has actually been demonstrated.

- [x] **B — Alternative.** **Use a documented completeness and traceability review as the normal gate.** Check business rules, interfaces, expected results, dependencies, and recovery prerequisites. Clearly report reconstruction as specified but not demonstrated until an explicit independent exercise occurs. This provides weaker assurance with lower execution cost.

- [ ] **C — Leave as is.** Keep the functional reconstruction target without adding an acceptance method that specifically tests it.

- [ ] **D — My own approach.** Describe it below.

**Comments / modifications:**

____________________________________________________________

____________________________________________________________

### Q12 — Original records that contain sensitive values

**Finding type:** Policy tension requiring an explicit precedence rule  
**Source:** §7 amendment history; §8 original requestor responses; §12 sanitized records; §16 credential handling

**Relevant wording:** “Preserve the original received content before proposing changes”; “Keep credentials outside persisted configuration, tracked files, outputs, and logs”.

**Issue and consequence:** Exact original preservation can conflict with redaction when a requestor or framework user accidentally includes a credential in a form, amendment, attachment, or exported answer. Keeping the original preserves the sensitive value; removing it conflicts with immutable-history wording. The prompt needs a stated exception and a recovery procedure for already stored copies. Detection can only be best effort.

**Your decision:** Which rule takes precedence when incoming or archived content contains an accidentally supplied sensitive value?

- [ ] **A — Recommended.** **Sanitize detected values before normal persistence, with a controlled historical-redaction exception.** Show a local review for correction, retain a clearly marked sanitized original, and record that redaction occurred. If discovered later, an explicit human-authorized procedure removes the value from affected AIH-owned copies and appends a non-sensitive audit event with reason and scope. Preserve normal immutability for all other content and disclose any copies outside AIH that could not be changed.

- [x] **B — Alternative.** **Reject detected sensitive input and ask for a corrected resubmission.** Do not persist the rejected content in normal AIH records. Keep a non-sensitive rejection record, and define the same explicit historical-redaction exception for content discovered only after it was saved. This preserves accepted originals exactly, but makes correction less convenient.

- [ ] **C — Leave as is.** Keep both original-preservation and redaction requirements without specifying their precedence or an exception for accidental sensitive input.

- [ ] **D — My own approach.** Describe it below.

**Comments / modifications:**

____________________________________________________________

____________________________________________________________

This is a defined exception to normal history preservation, not a general permission to rewrite decisions or evidence. No option guarantees removal from third-party tools or copies already shared externally.

### Q13 — Authorization for skills used outside AIH

**Finding type:** Standalone execution contract gap  
**Source:** §13 independent portability, implementation authority, and bundled helpers

**Relevant wording:** “Standalone skill execution must not require recreating the entire AIH lifecycle.”; “Declare genuine runtime/tool dependencies and accept explicit input/output locations.”

**Issue and consequence:** A copied skill must work without the AIH engine and request records, yet implementation skills must follow authorized plans and scope. The prompt does not define what an approved plan or direct-implementation authorization looks like in that standalone setting. Different skill authors could invent incompatible approval requirements or accidentally require the full AIH lifecycle.

**Your decision:** How should a standalone skill establish its permitted scope and authorization mode?

- [x] **A — Recommended.** **Define a compact standalone invocation contract.** Supply input/output locations, permitted scope/effects, and the plan plus approved-plan or explicitly requested direct mode where relevant. Record the initiating user instruction and effective boundaries with the results, without claiming stronger identity verification than the host provides. Bundle validation and required guidance; keep actual permissions governed by the hosting agent.

- [ ] **B — Alternative.** **Let the hosting agent own authorization entirely.** Each skill documents prerequisites, receives the host-provided scope and plan, and records those inputs. Its helpers validate artifacts but do not attempt to reproduce or certify AIH-style approvals. This is lighter, with more variation between hosts.

- [ ] **C — Leave as is.** Retain the portability and authorization requirements while leaving each standalone skill to interpret their connection independently.

- [ ] **D — My own approach.** Describe it below.

**Comments / modifications:**

____________________________________________________________

____________________________________________________________

### Q14 — Storage environments covered by recovery guarantees

**Finding type:** Support-boundary gap  
**Source:** §1 Windows/Linux plain directories; §15 locks and recoverable file transactions; §10 consistent readers

**Relevant wording:** “appropriate file locking”; “Multi-file operations require a journal or equivalent recoverable file transaction protocol”.

**Issue and consequence:** The prompt specifies Windows and Linux support but does not distinguish a local disk from a network share or an actively synchronized folder. Recovery and writer-exclusion behavior depend on the storage environment and on whether another device can modify the same files. An implementation tested only on local storage should not imply that every directory arrangement has the same guarantees.

**Your decision:** Which storage environments must the first complete framework support?

- [ ] **A — Recommended.** **Guarantee supported operation on validated local disks.** Document network/shared storage and folders actively synchronized by another process as unsupported unless specifically validated. Detect and explain known problematic cases where practical, without claiming universal detection. Windows and Linux remain required target platforms with honest reports of actual tests.

- [ ] **B — Alternative.** **Also support explicitly designated network/shared storage environments.** Name the supported environments during implementation, validate locking/recovery there, and document cross-device and synchronization limitations. This broadens support and adds meaningful test and engineering scope; it does not promise every remote filesystem.

- [ ] **C — Leave as is.** Keep the broad Windows/Linux-directory wording and let implementation choose and document its underlying storage assumptions.

- [x] **D — My own approach.** Describe it below.

**Comments / modifications:**

____________________________________________________________
The agent should be limited to work only in the folder, where the folder .aih/ is located. This is its workspace. Nothing outside this folder should be changed. Add in .aih_product/ a special subfolder for temporary files needed the framework to run.
____________________________________________________________

## After your answers

The selected options will be used to revise the complete prompt in a new timestamped file through the agreed refinement cycle. A Leave as is answer preserves the current wording for that issue. Conflicting custom choices will be brought back for clarification rather than silently resolved.

Source integrity reference: SHA-256 `946ffb5cc40825f1c92ce439b9e292e26a9196510b9a558e6e64b175c5711f04`. The reviewed file was preserved unchanged during this review.
