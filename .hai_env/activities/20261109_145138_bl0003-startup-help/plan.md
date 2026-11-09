# BL-0003 implementation plan

Give HAI users an accurate startup summary and a combined task/agent menu, with brief Help available again on request. Implement the interaction in host instructions using existing runtime observations.

| Phase | Goal | Depends on | Expected result |
| --- | --- | --- | --- |
| 1. Define the guide and selection contract | Specify one reusable interaction | None | Shared procedure covering startup, Help and selections |
| 2. Connect startup and document Help | Make the interaction discoverable and active | 1: startup must reference the shared behavior | Startup-only waits; explicit tasks proceed; Help refreshes |
| 3. Verify host behavior and compatibility | Check all acceptance scenarios | 2: exercise the integrated instructions | Attributable scenario results and startup regression results |
| 4. Reconcile delivery records | Report completion against requirements | 3: completion needs actual evidence | Outcome, remaining limits and accurate backlog state |

## Requirements and planning authority

- Agreed human decisions: Q001=A, Q002=C, Q003=A, preserved in [decisions.md](/home/hromar/Desktop/repos/haide/.hai_env/activities/00000000_000000_active/decisions.md).
- Requirements baseline: [requirements.md](/home/hromar/Desktop/repos/haide/.hai_env/activities/00000000_000000_active/requirements.md), with ten acceptance criteria, abbreviated AC1–AC10 below.
- Readiness: all 28 checks passed for the draft revision; [assessment](/home/hromar/Desktop/repos/haide/.hai_env/activities/00000000_000000_active/files/BL-0003-clarification/readiness-assessment.json) records evidence and the portable-text assumption.
- Current instruction, verbatim: “Make a plan for implementation”. Source: current human turn, saved root session position 1139, session `01a1b921-1f1b-7ae3-88a6-9dc7fbc32c63`.
- That instruction authorizes this planning work against the clarified baseline. It does not authorize implementation, installation, settings changes, publication, Activity closure or a commit.
- No business decision blocks this plan. Suggested labels and the design below remain delivery proposals, rather than additional human answers.

## Proposed design and rationale

Use one core procedure for presenting the overview, interpreting selections and responding to Help. Keep `.hai/start.md` short by linking that procedure and stating when the host must use it.

- Consume the primary runtime startup result, including `agents`, `activity_context`, scoped `issues` and `recording_context`.
- Keep the existing CLI, JSON schema, state format and read-only discovery unchanged. No new runtime dispatcher, renderer, persistent menu state or agent definition is needed.
- Let the host interpret whether the human requested startup alone, an explicit task, Help or a selection; the runtime does not receive conversation intent.
- Startup alone shows the summary and combined menu, then waits even if an Activity exists. An accompanying task gets the required summary and proceeds under current continuity rules.
- An internal startup check during unrelated ongoing work does not trigger another menu. An explicit Help/menu request refreshes observations and uses the same guide.
- Show the actual Activity ID, lifecycle, relevant step state and supplied goal when available. Label bounded/truncated input as an excerpt; never invent an agreed goal from unrelated text.
- Show each valid registered agent once as a selectable item, with a concise purpose and registration/availability distinction. Never substitute source packages for workspace registrations.
- Use stable choices such as `continue`, `new-task`, `agent-setup`, `help` and `agent:<registered-name>`. Equivalent clear prose is accepted; numbering is optional and tied to the last displayed menu.
- Recheck relevant current facts before dispatch. A missing prior menu, changed choice, ambiguous number or removed registration causes clarification or a refreshed menu, never reinterpretation as another action.
- Route selections through existing core operations or selected-role instructions. Selection does not waive task inputs, configuration, model/tool capability, authorization or recording prerequisites.
- Preserve independent valid observations when another startup component fails. Report unavailable/unverified fields and the actual issue; do not convert invalid state into absent state.
- Keep the introduction to two sentences and each option to one compact entry. Do not cap the agent count or repeat full role manuals.

### Task choices

| Proposed choice | Inclusion and next behavior |
| --- | --- |
| `continue` | Include for a valid current Activity; ask what to continue if its next work is unclear |
| `new-task` | Invite a task description; apply existing Activity continuity before any creation |
| `backlog` | Include only where an established backlog workflow is available; request an item if missing |
| `agent-setup` | Offer supported setup assistance; check the chosen operation before installation, registration or configuration |
| `help` | Refresh and present the same brief overview |
| `agent:<name>` | Include every valid registered agent; obtain a meaningful assignment before role work |

The current workspace has backlog files but no registered Backlog-manager. Its existence must not be claimed; a backlog request can still be described as a task and handled only within existing supported ownership.

### Alternatives considered

| Alternative | Tradeoff | Decision |
| --- | --- | --- |
| Shared host procedure | Matches conversation-driven routing and existing runtime facts | Recommended; smallest sufficient change |
| Python menu model and resolver | Adds schema/API, menu lifetime and stale-state responsibilities | Defer unless host validation demonstrates a concrete need |
| Workspace-only instructions | Would apply only to this installation | Reject as the sole implementation of reusable core startup behavior |
| Graphical menu or detailed manuals | Expands host integration and content scope | Outside the clarified iteration |

## File inventory

Existing links below point to actual files. Proposed paths identify planned additions; no product files have been changed by this plan.

| Path | Change | Purpose |
| --- | --- | --- |
| Existing [.hai/start.md](/home/hromar/Desktop/repos/haide/.hai/start.md) | Edit | Connect startup and subsequent explicit Help/selection handling to the shared procedure |
| Proposed `.hai/procedures/present-startup-guide.md` | Add | Own summary, conditional choices, refresh, selection, error and read-only behavior |
| Existing [README.md](/home/hromar/Desktop/repos/haide/README.md) | Edit | Explain startup-only waiting, explicit-task continuation and how to request Help |
| Proposed `.hai_env/activities/00000000_000000_active/files/BL-0003-verification/scenarios.md` | Add | Hold scenario inputs, expected results, actual outcomes and coverage limits |
| Existing [backlog/new/BL-0003.md](/home/hromar/Desktop/repos/haide/backlog/new/BL-0003.md) | Edit | Reconcile final scope, Activity reference and actual delivery evidence when authorized |
| Existing [backlog/catalogue.md](/home/hromar/Desktop/repos/haide/backlog/catalogue.md) | Edit | Keep item status/path consistent when authorized |
| Proposed move `backlog/new/BL-0003.md` → `backlog/closed/BL-0003.md` | Move | Archive only after accepted completion under backlog ownership |

Runtime modules, state/configuration, source and installed role packages, release manifests and existing ZIPs are unchanged in the proposed design. Verification material stays with this Activity rather than becoming framework product content.

## Phase 1 — Define the guide and selection contract

### Purpose

- Specify one compact, reusable startup/Help interaction and safe selection behavior.

### Why now

- Startup currently returns facts but has no contract for presenting or selecting them.

### Visible result

- Before: raw facts and discretionary chat. After: an inspectable core procedure with consistent behavior and examples.

### Scope

- Cover one agent and one current Activity first, then absent/partial states. Do not add a menu backend or execute a selected task while merely displaying choices.

### Actions

| Step | Action | Purpose or expected result |
| --- | --- | --- |
| 1.1 | Recheck the requirements, ledger and current protected-file baseline | Preserve settled A/C/A decisions and unrelated changes |
| 1.2 | Confirm covering implementation authority before product writes | Retain the actual human instruction verbatim; planning text supplies no authority |
| 1.3 | Add the proposed core procedure | Define triggers, inputs, summary, choices, selection and outputs in one owner location |
| 1.4 | Specify operation checks and partial-data behavior | Preserve independent capabilities and prevent invalid-state repair or false readiness |
| 1.5 | Include compact valid, empty and blocked examples | Make expected host behavior reviewable without hard-coding this workspace's agents |

### Affected files

- Proposed `.hai/procedures/present-startup-guide.md` from the inventory.

### Complete when

- A reader can identify the startup-only, explicit-task, Help and selection paths without guessing.
- The procedure covers AC1–AC10, uses actual registration/Activity facts, and separates display from work execution.
- No new settings, persistent menu file or blanket agent-configuration scan is introduced.

## Phase 2 — Connect startup and document Help

### Purpose

- Apply the guide at the right user-facing moments and make repeat Help discoverable.

### Why now

- The shared contract exists after phase 1, so entry points can reference it without duplicating policy.

### Visible result

- Startup alone offers choices and waits; startup with a task proceeds; “show the menu” refreshes the overview later.

### Scope

- Edit core startup instructions and a short README explanation. Preserve recording readiness, fixed instructions and current Activity continuity.

### Actions

| Step | Action | Purpose or expected result |
| --- | --- | --- |
| 2.1 | Link the guide from `.hai/start.md` with explicit trigger rules | Distinguish a human startup/Help request from an internal diagnostic call |
| 2.2 | State subsequent Help and selection handling in the startup contract | Keep the interaction available after the first response |
| 2.3 | Document stable example choices and plain-language selection in README | Let users discover Help and choose work without role knowledge |
| 2.4 | Check links and instruction consistency | Avoid conflicting startup, Activity, agent or chronicle obligations |

### Affected files

- Existing `.hai/start.md` and `README.md` from the inventory.

### Complete when

- Startup-only and explicit-task instructions reflect Q001=A, combined choices reflect Q002=C, and repeat brief Help reflects Q003=A.
- The primary JSON CLI still accepts its existing arguments and emits its existing structure; internal status calls do not acquire conversation side effects.

## Phase 3 — Verify host behavior and compatibility

### Purpose

- Demonstrate the user interaction and verify unchanged startup behavior.

### Why now

- Only the integrated instructions from phase 2 can be evaluated against actual conversation outcomes.

### Visible result

- A scenario report ties observed responses and file comparisons to every acceptance criterion, with failures and unrun checks explicit.

### Scope

- Use isolated fixture workspaces and harmless tasks. Keep display-only mutation checks separate from the expected recording of actual exchanges.

### Actions

| Step | Action | Purpose or expected result |
| --- | --- | --- |
| 3.1 | Prepare the acceptance matrix below | Define observable expected results before evaluating the host |
| 3.2 | Exercise startup, selection and repeat Help scenarios in the host | Test actual instruction behavior rather than Markdown wording alone |
| 3.3 | Compare fixture files before and after display/Help | Prove no product settings, registrations or Activity lifecycle mutation |
| 3.4 | Run existing startup and runtime workflow regression suites | Check discovery, partial results, CLI compatibility and existing operations |
| 3.5 | Review evidence against all ten acceptance criteria | Identify any unmet behavior or host limitations before claiming completion |

### Affected files

- Proposed Activity-local `files/BL-0003-verification/scenarios.md` from the inventory.
- Existing tests listed below are run unchanged; add code tests only if the design actually acquires runtime code changes.

### Acceptance matrix

| Scenario | Expected observation | Criteria |
| --- | --- | --- |
| Startup alone, with and without a current Activity | Accurate summary, combined menu, invitation and no arbitrary work | AC1, AC4, AC10 |
| Startup with a concrete harmless task | Mandatory summary and task continuation without a menu gate | AC2 |
| Registered X/Y, no registrations, changed registrations | All and only valid registered choices; no static list or silent omissions | AC3 |
| Full and truncated Activity input, absent and invalid Activity | Real identity/state, honest goal excerpt/absence, invalid distinguished from absent | AC4, AC9 |
| Stable task/agent choice and equivalent prose | Intended existing operation, necessary inputs/prerequisites checked | AC5 |
| Bare agent choice without a task | Meaningful assignment requested; no empty invocation | AC5, AC8 |
| Invalid number, ambiguous prose, removed agent, missing prior menu | Clarification/refreshed menu; no wrong dispatch | AC6 |
| Help after facts change; ordinary task mentioning help | Refreshed brief guide for explicit Help; ordinary task interpreted by intent | AC7 |
| Agent operation with known unmet or unknown capability | Registration remains visible; no false readiness or silent enabling | AC8 |
| Partial registry/profile/recording/core failure | Independent valid facts retained; affected next steps accurately qualified | AC9 |
| Display and Help with many registered agents | Two-sentence introduction, one compact entry each, no hidden agents or product mutation | AC10 |

### Planned regression commands

Run from the repository root using the verified Python executable. These commands have been identified, not executed as implementation validation during planning.

```text
/usr/bin/python3 -B .hai/tools/startup/test_startup_check.py
/usr/bin/python3 -B .hai/tools/startup/test_startup_context.py
/usr/bin/python3 -B -m unittest discover -s .hai/tools/runtime/tests -p 'test_workflows.py'
/usr/bin/python3 -B .hai/tools/hai.py startup --workspace .
```

### Complete when

- Every acceptance row has actual expected/observed evidence or an explicit unresolved limitation; no synthetic conversation is presented as a saved user exchange.
- Regression commands pass with skips and platform limits reported separately.
- If implementation expands into shared runtime behavior or multiple components, a separate reviewer performs the independent assessment required by `.hai/conventions/agent_conv.md`; the author still performs developer checks.
- Documentation-only review is proportionate; no tests merely assert that instruction sentences exist.

## Phase 4 — Reconcile delivery records

### Purpose

- Make the reported delivery and backlog status match the verified outcome.

### Why now

- Phase 3 provides the evidence needed to distinguish implemented behavior from a proposal or incomplete work.

### Visible result

- The user receives the final behavior, validation results and remaining limits; backlog records change only under covering ownership and authority.

### Scope

- Update Activity evidence through core runtime. Do not infer a request to commit, close the Activity, publish a release or reinstall packages.

### Actions

| Step | Action | Purpose or expected result |
| --- | --- | --- |
| 4.1 | Compare protected-file changes with the initial baseline and actual authority | Attribute exact paths and preserve unrelated work |
| 4.2 | Record actual implementation and verification results through runtime | Preserve original implementation start and evidence history |
| 4.3 | Reconcile the backlog item and catalogue under authorized backlog ownership | Keep requirements, stable Activity reference, status and path consistent |
| 4.4 | Report completion or remaining acceptance failures | Give a reviewable result without implying publication or closure |

### Affected files

- BL-0003 and catalogue entries from the inventory, conditionally on authorized completion.
- Canonical Activity records through runtime, retaining exact human input and prior revisions.

### Complete when

- Requirements, delivered files, actual checks and limitations are traceable to this Activity ID: `b5498652-adcc-4803-8843-b1893575ab97`.
- Any accepted-complete backlog move preserves history and keeps the catalogue link valid.
- Commit/closure remain separate operations requiring their own user instruction and current source-backed recording verification.

## Dependencies and risks

- Implementation waits for a covering human implementation instruction; this planning turn modifies only Activity records and supporting work files.
- Host instruction compliance needs actual interaction evaluation. Passing Python regressions alone does not prove the menu behaves correctly.
- Bare numeric selections need a known prior displayed menu; stable text identifiers reduce ambiguity but never bypass revalidation.
- Activity input is bounded in startup output. Read further authorized Activity context only when needed, and preserve the distinction between an excerpt and a confirmed goal.
- Optional workflow or agent availability varies by workspace. Derive choices from current evidence; no new package installation or configuration repair is implied.
- New core files will be included in a future release through the normal release process; do not edit historical release manifests or claim an existing ZIP contains this work.

## Planning evidence and limits

- Inspected core startup instructions, runtime startup/CLI modules, Activity discovery, startup tests, runtime workflow tests, README and BL-0003.
- Startup returned valid core/current Activity context; enabled recording was synchronized through the current human request at source position 1139.
- Solution-architect configuration is valid/defaulted at `.hai_env/config/agents/solution-architect.json`, settings `{}`, no configured fields or issues. Followed the installed role directly; no separate architect was spawned.
- No product implementation, interaction acceptance run, regression test run, backlog mutation, commit or closure was performed for this plan.


Revision provenance: source: Human request at root source position 1139: Make a plan for implementation; reason: Prepare actionable scoped implementation and verification plan; reason: Human-requested implementation plan; product implementation not started; recorded 2026-11-09T14:23:15Z.
