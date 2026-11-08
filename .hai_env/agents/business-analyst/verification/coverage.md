# BL-0011 coverage and verification

Implementation authority: human request, current chat, verbatim:
“Implement backlog item BL-0011”. Implementation/semantic mapping by host
coordinator, 2026-11-08, Activity `63c11143-eec4-487a-a7f1-57220a2d09e5`.
This is evidence about the reusable source package, not an invocation of it.

## Evidence keys

- C: [context contract](../conventions/context-registry.md) and [Acquire context](../procedures/acquire-context.md).
- D: [dialogue contract](../conventions/clarification-dialogue.md) and [Clarify intent](../procedures/clarify-intent.md).
- R: [readiness convention](../conventions/requirements-readiness.md).
- P: [Assess and propose](../procedures/assess-and-propose.md).
- F: [framework protection](../conventions/framework-protection.md).
- RC: [registry fixtures](../scripts/test_context_registry.py).
- DF: [dialogue/readiness/proposal/protection fixtures](../scripts/test_clarification.py).
- H: [helper APIs, operations and limits](../scripts/README.md).

Instruction/contract rows below are semantic inspection, not proof that a model
will follow every instruction in every host. Fixture rows exercise the named
behavior with isolated data and, for persistence/archival, actual core operations
in disposable workspaces. They do not substitute a checklist summary for the
individual requirements or the 28 readiness checks.

## Individual requirements

Numbering after AC labels identifies checkbox order in the captured story.

| Requirement | Contract and observed verification |
| --- | --- |
| AC1.1 Request, Activity, instructions, domain sources and prior dialogue reconciled | C steps 1–3; D event identity/restart; DF first-question/reuse and exact-answer/restart fixtures. |
| AC1.2 Absent/empty ledger, first real question creates it | D location/ownership; DF first-question test confirms absence, no proposal prerequisite, successful core persistence. |
| AC1.3 Additional authorized context, sufficient-files statement or named dependency | C steps 3–5; this Activity analysis explicitly records sufficient files; RC missing-context CLI fixture reports exact document path. |
| AC1.4 Ordered level-three registry entries, six independent fields | C supported format; RC order/independent resources and field/fence fixtures. |
| AC1.5 Case-insensitive flags, invalid diagnostics, exact real helper command | C diagnostic command; RC YES/No/invalid and CLI exit-code tests. No legacy command advertised. |
| AC1.6 Relevant order, workspace roots, excluded paths and historical authority | C safety/selection; RC ordered host reads, invalid/custom-store and link fixtures. |
| AC1.7 Independent availability and exact warning for each missing resource | C independent availability; RC independently missing location/convention/prompt fixture continues later entries. |
| AC1.8 Full attributed reads, primary authority, inert Prompt/Update, no effects | C final context steps; RC full last-line reads and inert-prompt test verifies primary-only diagnostic reads, no network/execution and unchanged files. |
| AC2.1 Intent, outcomes, people, motivation, metrics, terminology/workflows/rules | D procedure step 2 lists each diagnostic dimension; manually compared against the complete requirement. |
| AC2.2 Scope, priorities, acceptance, restrictions, dependencies, I/O and permissions | D procedure step 2 explicitly preserves every listed concern; no inventory item becomes an automatic deliverable. |
| AC2.3 Edge cases, qualities, recovery, compatibility and delivery concerns | D procedure step 2 preserves failure/recovery, scale, accessibility, region, migration, observability, rollback and verification. |
| AC2.4 Contradictions, prior requirements/design/conventions and human tradeoffs | D procedure step 3 and R8.3; unresolved critical conflict fails readiness in DF. |
| AC2.5 Material blockers only, no repeats or safe implementation questions, rationale | Shared consequential-questions rule; D local rationale rule/steps 1–4; unanswered reuse and no-question readiness paths are supported. |
| AC3.1 Canonical full blocks, IDs, options, recommendation, Other, status and sequences | D canonical format; DF first-question, invalid-ID/preselection, revisions and mapping tests. |
| AC3.2 One logical necessary batch, wait, interface partition without duplicates | D logical-batch rule and step 4; DF saves/displays a three-question logical batch with stable IDs. UI partitioning remains a host instruction, not an exercised UI integration. |
| AC3.3 Host persistence/readback before question display, initial unchecked content | D host handshake; DF first-question exact readback, failure/no-display and partial-persistence fixtures use real core writes. |
| AC3.4 Saved display, answer form and unanswered redisplay without new event | D canonical display; DF first-question test checks copyable IDs/choices and unchanged bytes on reuse. |
| AC4.1 Actual human answer and verified persistence before application | Shared actual-answers rule; D handshake; DF rejects blank responses/prechecked new choices and verifies saved fixture replies. Human identity is host-attributed, not authenticated by helpers. |
| AC4.2 Verbatim multipart choices/explanations, reception order, restart deduplication | D response fields; DF Unicode/multiline multipart/restart test retains raw utterance, exact parts and ordered response numbers. |
| AC4.3 Ambiguous raw response, explicit mapping and retained numbered revisions | D mapping/target-set contract; DF ambiguous-answer and multipart-revision completeness regression hold proposal until all human-confirmed targets are persisted. |
| AC4.4 Reassessment and exact errors; stop dependent work, retain partial evidence | D procedure steps 6–7 and handshake; DF unavailable/read/write/readback/partial-failure tests. |
| AC4.5 No reset/delete/archive; later work/core archive preserves ledger; separate chronicles | D lifecycle; DF later-work and authorized fixture archival preserve exact ledger bytes. No actual product Activity was archived. |
| AC5.1 Shared eight-category, 28-item annotated convention | R retains every initial identifier and evidence text; DF count/category checks and per-item failure test. |
| AC5.2 Gate timing, scope reassessment and only two narrow exemptions | Shared gate rule, R assessment and P steps 1–3; DF scope reassessment plus both allowed/rejected exemption cases. |
| AC5.3 All mandatory checks/critical gaps, bounded assumptions and consequences | R assessment; DF all-item pass/fail and assumption/deferral/human-decision-limit tests. |
| AC5.4 Mandatory failure holds downstream work and names failed IDs | Shared failed-readiness rule and P step 3; DF individually fails every item and prevents proposal on failed assessment. |
| AC6 R1.1 Self-contained objective | R1.1 retains its complete evidence annotation; DF individually fails R1.1 when unsatisfied. |
| AC6 R1.2 Coherent outcome | R1.2 retains its complete evidence annotation; DF individually fails R1.2. |
| AC6 R1.3 Observable change | R1.3 retains its complete evidence annotation; DF individually fails R1.3. |
| AC6 R1.4 Motivating need | R1.4 retains its complete evidence annotation; DF individually fails R1.4. |
| AC6 R2.1 Identified participant | R2.1 retains its complete evidence annotation; DF individually fails R2.1. |
| AC6 R2.2 Participant difficulty | R2.2 retains its complete evidence annotation; DF individually fails R2.2. |
| AC6 R2.3 Other affected parties | R2.3 retains its complete evidence annotation; DF individually fails R2.3. |
| AC6 R3.1 Concrete benefit | R3.1 retains its complete evidence annotation; DF individually fails R3.1. |
| AC6 R3.2 Priority rationale | R3.2 retains its complete evidence annotation; DF individually fails R3.2. No priority invented for this work. |
| AC6 R3.3 Existing capability considered | R3.3 retains its complete evidence annotation; DF individually fails R3.3. |
| AC6 R4.1 Named deliverables | R4.1 retains its complete evidence annotation; DF individually fails R4.1. |
| AC6 R4.2 Iteration-sized work | R4.2 retains its complete evidence annotation; DF individually fails R4.2. |
| AC6 R4.3 Compatible scope | R4.3 retains its complete evidence annotation; DF individually fails R4.3. |
| AC6 R4.4 Outcome-based scope | R4.4 retains its complete evidence annotation; DF individually fails R4.4. |
| AC6 R5.1 Explicit exclusion | R5.1 retains its complete evidence annotation; DF individually fails R5.1. |
| AC6 R5.2 Precise exclusions | R5.2 retains its complete evidence annotation; DF individually fails R5.2. |
| AC6 R6.1 Technical limits | R6.1 retains its complete evidence annotation; DF individually fails R6.1. |
| AC6 R6.2 Organizational limits | R6.2 retains its complete evidence annotation; DF individually fails R6.2. |
| AC6 R6.3 Consequential assumptions | R6.3 retains its complete evidence annotation; DF individually fails R6.3 and exercises assumption boundaries. |
| AC6 R6.4 Separate constraints | R6.4 retains its complete evidence annotation; DF individually fails R6.4. |
| AC6 R7.1 Completion test | R7.1 retains its complete evidence annotation; DF individually fails R7.1. |
| AC6 R7.2 Objective verification | R7.2 retains its complete evidence annotation; DF individually fails R7.2. |
| AC6 R7.3 Feasible acceptance | R7.3 retains its complete evidence annotation; DF individually fails R7.3. |
| AC6 R7.4 Specific language | R7.4 retains its complete evidence annotation; DF individually fails R7.4. |
| AC6 R7.5 Full scope coverage | R7.5 retains its complete evidence annotation; DF individually fails R7.5. |
| AC6 R8.1 Shared framing | R8.1 retains its complete evidence annotation; DF individually fails R8.1. |
| AC6 R8.2 Prior decisions | R8.2 retains its complete evidence annotation; DF individually fails R8.2. |
| AC6 R8.3 Resolved conflicts | R8.3 retains its complete evidence annotation; DF individually fails R8.3 and critical-blocker override. |
| AC7.1 Complete proposed request only after verified decisions/readiness | P step 4 names every required component; DF proposal validation and pending-mapping/failed-gate holds. Semantic completeness remains analyst/reviewer work. |
| AC7.2 Deeper headings and explicit proposed target | P local rule and target default; DF rejects level-two headings and returns proposed current Activity input. |
| AC7.3 Ledger separate, no direct overwrite, original input/provenance/revisions | P steps 4–6 and D ownership; pure proposal validator performs no writes, later-work fixture retains original input/ledger. |
| AC7.4 Actual results, locations, dependencies; completion distinct from acceptance/closure | P output and step 6; H verification limits and this coverage record distinguish fixture/source results from real host/product outcomes. |
| AC8.1 Explicit human framework-maintenance authority, no generated permission | Shared protected-resources rule and F authority; source maintenance authority quoted above; installed snapshot preserved. |
| AC8.2 Verbatim authority/source retained downstream | P step 5 and F handoff; this Activity analysis/plan and independent review assignment carry exact human request. |
| AC8.3 Assigned scratch, permanent tools canonical, no generated caches/install/gitignore substitute | Shared temporary-outputs rule, F and H; tests use temporary workspaces with `-B`; permanent helpers live in the owned package. |
| AC8.4 Baseline/touched-path inspection, exact error, sorted paths, no automatic revert | F inspection and P step 5; DF protection fixture retains pre-existing changes, emits exact error/sorted paths and leaves bytes intact. |
| AC9.1 Append annotated items/categories in stable positions using unused IDs | R compatible extension; DF adds R1.5 and R9.1 and rejects skipped numbers. |
| AC9.2 Preserve initial IDs/order/references and historical assessments | R compatible extension; DF detects removed/renumbered identifiers and retains the old assessment. |
| AC10.1 Integrated semantic mapping for all AC1–AC9 including 28 individual checks | This table plus shared rules/procedures/contracts reviewed together; independent QA reviews source behavior separately. |
| AC10.2 Context scenarios, flags, paths, independent resources, inert metadata/no effects | RC named fixtures cover these behaviors; relevance is explicitly a simulated host choice, not a helper claim. |
| AC10.3 Dialogue scenarios, all persistence failure modes and retained evidence | DF real-runtime handshake fixtures plus independent QA multipart-mapping regression and its corrective test. |
| AC10.4 Gate, assumptions/exemptions/reassessment/extensions, deeper proposal, preservation/protection | DF ReadinessProposalProtectionTests and later-work/archival fixtures; source R includes all exact annotations. |
| AC10.5 Package/config validators, actual capabilities/copies, exercised/unrun limits | DF disposable installed-layout validation and empty/default configuration read; H documents commands and limits. Source maintained; real installed BA bytes/catalogue/configuration remain unchanged. |

## Verification scope

Developer checks: the focused suite runs on Linux, Python 3.12.3 with verified
`/usr/bin/python3 -B`. All tests use only the standard library. Package format and
configuration checks run against a disposable installed layout copied from the
whole source package beside compatible core files. The unchanged format-1 empty
settings contract remains compatible; no new settings, migration or core extension.

An independently launched Quality-assurance invocation used its declared
standard/high profile resolved to host-advertised `gpt-6.1-terra`/`high`, after
selected configuration validation. Its original 22-test run passed but its own
extra regression identified incomplete multipart ambiguity resolution; the author
corrected it and added a permanent regression. Actual final results and reviewer
follow-up are retained in this Activity's records/invocation supporting files.

Unrun limits: real end-user clarification UI, real product Activity archival,
Windows/macOS execution and billing/usage attribution. Fixtures do not prove these.
Core chronicles are enabled, but the host has no explicit saved session source,
identity and attributed range available; no source discovery/backfill or transcript
coverage claim is made. The product Activity remains active; no closure authorized.
