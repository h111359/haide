# BL-0012 planning evidence and readiness

Assessor: host coordinator, directly following the installed Solution-architect instructions; no architect sub-agent was spawned. Date: 2026-11-09. Activity: `d44d0ee7-4250-494a-ba54-40b4729b94d2`.

## Sources and scope

- Assessed revision: `backlog/new/BL-0012.md`, Updated `2026-11-09T15:32:58Z`, plus the current human request to create a plan.
- Human requirement: move the three named files into `.hai_env/config/` and adapt dependencies, to clarify the folder arrangement.
- Human clarification: “yes, migrate existing env as well”. Persisted in `decisions.md` and the backlog item.
- Current authority: “Create a plan for realization of this backlog item.” The earlier backlog-only limit is expanded to planning, not implementation.
- The business analyst's prior limited assessment identified existing-environment migration as the consequential decision. That decision is now resolved; this assessment does not claim a new independent analyst review.
- Solution-architect configuration: defaulted, empty settings, no issues. Declared advanced profile resolves to the current host's `gpt-6.1-sol`; direct execution follows the shared role policy.

## Requirements readiness

Assessment scope is the bounded proposed implementation, for planning entry. No exemption is used. The following evidence covers all 28 mandatory checks from the installed requirements-readiness convention.

| Check | Result | Evidence and interpretation |
| --- | --- | --- |
| R1.1 | Pass | Backlog What names three moves, their destinations and dependent updates; plan objective restates them |
| R1.2 | Pass | All changes serve one environment-configuration layout |
| R1.3 | Pass | Maintainers find configuration in one directory; existing workspaces can migrate |
| R1.4 | Pass | User explicitly requests clearer `.hai_env/` arrangement |
| R2.1 | Pass | Workspace maintainers are the affected participant, inferred from workspace configuration ownership |
| R2.2 | Pass | Their configuration files are currently split between environment root and config directory |
| R2.3 | Pass | Runtime operators and optional-package consumers are also affected; inventoried core/package consumers provide evidence |
| R3.1 | Pass | Grouping configuration supplies the user's stated organization benefit |
| R3.2 | Pass | User requests planning now; implementation scheduling, urgency and release date remain unassigned |
| R3.3 | Pass | Startup and runtime currently hard-code all three root-level paths; the requested layout is not current capability |
| R4.1 | Pass | Three target moves, dependent resources and existing-environment migration are bounded deliverables |
| R4.2 | Pass | One coordinated path relocation with migration; schema redesign and independent feature work are excluded |
| R4.3 | Pass | New canonical paths and explicit legacy migration are compatible; no silent dual authority is required |
| R4.4 | Pass | Outcomes name locations and working behavior; internal module and command design are labeled proposals |
| R5.1 | Pass | Plan excludes implementation execution, publication and Activity closure from current work |
| R5.2 | Pass | Activity-local state filenames, agent-setting ownership and historical records are explicitly preserved |
| R6.1 | Pass | Existing Python 3.11+ requirement, strict JSON, path containment, optional profiles and empty-instructions semantics are retained |
| R6.2 | Pass | Runtime ownership, provenance, explicit migration, recording and package-update boundaries are recorded |
| R6.3 | Pass | Shared locks and ended writers are prerequisites; mixed/partial layouts block rather than imply safe continuation |
| R6.4 | Pass | Plan separates agreed requirements from proposed design and constraints |
| R7.1 | Pass | Backlog contains five acceptance conditions, including migration and preservation |
| R7.2 | Pass | Plan verification matrix names layout assertions, byte/hash comparisons and observable runtime operations |
| R7.3 | Pass | Disposable workspaces and existing test helpers can exercise each condition without live migration |
| R7.4 | Pass | Paths, byte preservation and pass/fail operation results replace the broad organization rationale as completion checks |
| R7.5 | Pass | Each of the five backlog acceptance conditions maps to planned evidence |
| R8.1 | Pass | Plan retains HAI environment, Activity, package and configuration ownership vocabulary |
| R8.2 | Pass | State/layout conventions and analyst findings inform explicit migration, preserved data and separate schema conversion |
| R8.3 | Pass | Existing fixed-path rules are the requested change target, not authority to move files now; new normal readers and a bounded legacy branch resolve the conflict in the proposed design |

Result: sufficient requirements for the requested plan. Implementation scheduling and release mechanics are deferred delivery choices; no priority, release version or migration design is represented as a human decision.

Stakeholder identification and the single-iteration boundary are planning interpretations, not additional accepted business requirements. If dependency discovery reveals a separate product change or external integration, reassess scope before implementing it.

## Observed technical findings

- `.hai/tools/startup/startup_check.py` defines the old instruction path and separately reads old state/profile paths.
- Its `instruction_path()` rejects overlap with all of `.hai_env/config/`; direct string replacement would reject the requested instruction location.
- `.hai/tools/runtime/environment.py` requires valid startup before most mutation branches; a new migration operation needs a narrow legacy-aware prerequisite path.
- State reads are duplicated in Activity, recording, chronicles and source-discovery code. Activity-local `state.json` files are separate and remain in place.
- `.hai/tools/configuration/configuration_tools.py` reads state to reserve configured content locations; relocation must preserve that protection and isolated owner-settings diagnosis.
- Git-manager and Specification-manager helpers contain direct environment paths. Their reusable source and installed copies require separate updates.
- Current schema contract supports formats 2 and 3, with ordinary mutation targeting format 3. Layout relocation need not mutate schema contents or fabricate an environment version bump.

## Checks actually performed

- Runtime startup: valid environment and current Activity; readable mandatory instructions are empty.
- Solution-architect settings: defaulted and valid.
- Read-only searches: current runtime/startup/configuration consumers, source packages, installed packages and conventions.
- Read-only review: current migration, path protection, lock and dispatcher implementations.
- No implementation tests or migration trials performed. Planned checks are enumerated in `plan.md`.
- Initial Git status already contained backlog and active-Activity changes from prior turns. This planning turn adds only Activity planning/evidence/recording artifacts and temporary scratch files.

## Recording limits

Current host recording is synchronized through saved exchanges; the final delivery remains collectable on a later active turn. Prior business-analyst participant discovery did not establish a verified native-assignment boundary; this plan does not claim full participant transcript coverage or closure readiness.

Assessed backlog SHA-256: `dbe1e765ecaf8c49b1de4ed6fc8b8159ea6db8325ae50e340d245b3f7e5eb3d9`.


Revision provenance: source: Human request: Create a plan for realization of this backlog item.; reason: Save reviewable plan and evidence; implementation is not authorized by this operation.; reason: User-requested BL-0012 implementation plan and attributable planning evidence.; recorded 2026-11-09T16:42:08Z.


## Implementation and verification — 2026-11-09

The human instruction “Implement.” authorized realization of the saved plan.
Core operational paths, source-package dependencies, affected installed helper
scripts and current documentation now use `.hai_env/config/`. Installed script
adaptation was direct scoped maintenance; no whole-package replacement or
registration membership change was performed. Changed source/installed helper
files match by byte comparison.

The explicit `environment migrate-layout` command migrated this workspace and
retained recovery copies. All three destination hashes and backup hashes match
the inspected legacy bytes. Old root-level files are absent; startup validates
the same current Activity identity and readable empty mandatory instructions.

Developer verification: 410 tests run across 10 suites, 407 passed and 3 skipped.
The 18 migration tests cover optional profiles, empty/BOM instructions, unknown
state preservation, layout conflicts, invalid input, links, locks, partial writes,
removal failures, changed inputs, schema-2 relocation followed by conversion,
initialization guards and legacy-path reservations.

Independent QA `/root/qa_bl0012`, invocation
`44a49212-e711-4870-b181-d137dcfe90c6`, found two defects (initialization with an
incomplete marker and instruction aliases to recovery metadata). Both were fixed
and independently retested. The final migration and configuration changes passed
independent retesting; no remaining concrete severe defect was reported.
All review writes have ended. Windows/macOS execution remains unverified.

[Verification evidence](files/verification/test-results.json) records each suite
and its output. Package audit, live startup, profile read, completed-backlog audit
and Git whitespace checks passed. No product implementation test result is being
inferred from transcript verification.

[BL-0012](../../../backlog/closed/BL-0012.md) is completed with acceptance mapping
and preserved predecessor. The Activity remains active. No commit, publication
or Activity closure was requested or performed. Host recording is synchronized
separately; participant assignment boundaries remain unavailable, so full
participant transcript or billing coverage is not claimed.


Revision provenance: source: User: Implement.; actual developer results and independent QA handoffs; reason: Record completed implementation and verification without closing the Activity.; reason: Append actual implementation, independent QA and verification results.; recorded 2026-11-09T16:56:02Z.
