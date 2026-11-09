### Intent

Give a person starting HAI a concise, accurate view of the registered agents and
current Activity, with selectable next actions so they can begin useful work
without already knowing HAI's roles or workflow.

### Effective decisions

- Q001=A: A startup-only request with no explicit task displays the menu and
  waits. If startup includes a concrete task, display the registered-agent and
  Activity summary and proceed with that task without an unnecessary selection.
- Q002=C: Include both task actions and individual registered agents in the same
  menu. They may be grouped for readability; agents are not hidden behind a
  separate submenu as the only way to select them.
- Q003=A: Provide a short startup overview, available again on an explicit Help
  or menu request. Detailed per-action/per-agent manuals are outside this iteration.

### Context

The source is BL-0003, Initial Menu and Help. Its stated need is to make available
next actions visible and selectable in the first startup response. Its original
acceptance requirements are to show registered agents and the current Activity
state. Those requirements remain mandatory.

Current startup already returns registration names/descriptions, Activity
lifecycle/steps/continuity and recording readiness. The missing outcome is a
consistent user-facing guide, menu and selection/Help interaction. Registered
agents are not automatically confirmed runnable: specific model, configuration,
tool and permission requirements still apply.

### Outcomes

The startup user can see what is registered, understand current work, and choose
a task or agent. The host coordinator can route that choice through existing
operations/roles. Registered-agent owners are affected only by accurate discovery
and routing, with their current scope and prerequisite rules preserved. No new
external stakeholder or service is introduced. The user selected this item as the
current work; no release priority, urgency or deadline has been specified.

### Scope

- D1: A startup summary with the registered-agent names and accurate current
  Activity information. When an Activity exists, identify it, its goal if supplied,
  lifecycle and relevant work-step state. Otherwise say no Activity is active.
- D2: A combined menu of existing task actions and individual registered agents.
  Proposed baseline task categories for review are Continue Activity, Start or
  describe a task, Work on a backlog item when supported, Agent setup, and Help.
  Labels/order can be refined without inventing new capabilities. Use current
  verified data; label unavailable or unverified capability truthfully.
- D3: Selection through a portable identifier/number or an unambiguous plain-text
  request. Resolve it to the displayed action or named agent; request only missing
  necessary task inputs. Ambiguous, invalid or stale choices receive clarification
  instead of being dispatched to a different action.
- D4: The same brief overview/menu format on an explicit Help/menu request, with
  current information refreshed. A task merely containing the word help is still
  interpreted according to its actual intent.
- D5: Useful, accurate responses with no active Activity, no registered agents,
  or blocked/partially available startup data. Preserve valid independent facts
  and name the relevant issue without inventing state or silently repairing it.

### Exclusions

A new graphical application or required native buttons; exhaustive command
reference or detailed role manuals; new agent implementations; new backend
capabilities merely to populate menu entries; automatic installation, registration,
configuration repair, Activity replacement/closure, publication or permission
changes triggered solely by displaying startup or Help.

### Constraints and assumptions

- Trigger the guide at the user-facing startup workflow response, not every
  internal status check during ongoing work. A startup-only request still reports
  existing Activity continuity; it does not erase it or manufacture a new task.
  An accompanying explicit task proceeds under existing continuity rules.
- Show actual workspace registrations, not all golden-source packages. Keep
  registration, operation-specific availability and authority distinct. Check
  affected prerequisites before selected work; do not disable independent valid
  capabilities because another sub-operation is unavailable.
- Displaying the guide/Help is read-only with respect to product settings and
  Activity lifecycle. Normal recording of actual exchanges and meaningful work
  retains the existing core/host ownership and chronicle requirements.
- P1: A portable text interaction is sufficient for this iteration, consistent
  with this HAI chat workflow and the human's actual labelled answers. If a future
  graphical-only surface is required, reassess its host integration and scope.
  No explicit graphical-interface decision is being overridden.
- Exact option labels/order and concise wording are delivery choices. The task
  categories above are a proposed baseline for review, not additional human
  answers. Unsupported operations must not be implemented or claimed just to make
  those categories available.
- Keep the opening explanation to at most two sentences, followed by one compact
  item per action/agent rather than reproducing full role instructions. Do not
  impose a total length cap that silently hides registered agents.
- Follow existing HAI ownership, safe-path, configuration, source-backed recording
  and tooling conventions (verified absolute Python 3.11+ with -B if helpers are
  used). Internal rendering/dispatch design remains for the delivery roles.
- Current authority is clarification only. This proposed input is for human review;
  implementation approval must supply covering human framework-maintenance
  authority verbatim with its source to downstream analysis/planning. This draft
  does not itself grant that authority.

### Acceptance criteria

1. Startup-only scenario: for a valid workspace with no explicit task, the first
   user-facing startup response contains the registered-agent/Activity summary,
   combined selectable menu and invitation to choose; it waits without starting
   an arbitrary task. This also applies when an existing Activity is reported.
2. Explicit-task scenario: with a concrete task accompanying startup, the response
   includes registered-agent/Activity information and proceeds with that task
   without requiring a menu selection first. D1's mandatory information is retained.
3. Registration fixtures: with agents X and Y registered, both names appear as
   individual selectable choices alongside task choices. No unregistered source
   package is labelled registered. With none registered, the response states that
   explicitly while retaining valid core task choices. Changes are reflected in
   the next requested overview rather than a hard-coded workspace list.
4. Activity fixtures: active Activity A is reported with its real identity,
   supplied goal and lifecycle/work-step state; no-Activity state is reported as
   absent. Rendering neither creates another Activity nor resets existing progress.
5. Valid-selection scenario: a clear displayed choice or equivalent plain request
   routes to that action/agent under existing prerequisites. Missing necessary
   task input is requested; the choice is not falsely reported as completed work.
6. Invalid/stale-selection scenario: an ambiguous, unknown or outdated selection
   causes clarification or a refreshed menu, without unrelated dispatch or mutation.
7. Help scenario: an explicit Help/menu request after startup produces the same
   brief type of guide and combined choices using refreshed facts. It does not
   require replaying startup setup or reproduce full agent manuals.
8. Availability scenario: a registered agent with an unmet requirement remains
   accurately identified as registered; unknown availability is not called ready.
   A selected blocked operation reports the actual dependency and respects existing
   independent gates, without silently enabling settings or installing anything.
9. Partial/invalid-startup scenario: valid independent information and the actual
   issue are visible; unverified agents/Activity state are not invented. Only
   supported, authorized next steps are offered or labelled with their dependency.
10. Presentation/read-only scenario: the opening explanation has at most two
    sentences and each choice has one compact entry. Both types of choices remain
    in the same menu. Display/Help alone changes no product configuration, agent
    registration or Activity lifecycle. D1–D5 map respectively to criteria
    1/2/4, 3/8, 5/6, 7, and 9/10.
