# Independent QA: BL-0003 startup guide

Authority: host assignment of human “Implement”, root source position 1203. Activity b5498652-adcc-4803-8843-b1893575ab97. Invocation manifest matches assigned ID, role, Activity and provenance. Startup reported valid environment and current Activity; fixed instructions are readable and empty. Recording readiness separately reported blocked for this participant; this review does not claim source coverage. Configuration supplied by host as valid/defaulted. This report is an independent instruction review with synthetic fixture exercises, not real human exchanges, actual interactive end-to-end execution, or evidence of host adherence. No regression suites run by this reviewer.

## Finding

README.md says “Startup resumes current work; a new chat alone does not create or close an Activity.” The new startup-only rule expressly requires displaying the menu and waiting even with a current Activity. The earlier README paragraph says this correctly, but the later unqualified statement can cause a reader or host to resume work automatically. Recommend changing it to say startup reports current work and continuity is preserved; resumption requires a selection or concrete compatible task. This is a documentation inconsistency with AC1, not a demonstrated runtime action.

## Synthetic exercise outputs

All names, Activity IDs, states, requests, selected mappings and dependencies in this section are hypothetical; outputs are candidate responses produced by applying the procedure, not actual exchanges. Each menu below presents one compact row per choice and waits where required. X and Y are registered unless noted, and availability is unknown unless otherwise noted.

**Startup alone, current Activity A** (AC1, 3, 4, 10): request “Start HAI”; A is active, goal “Ship report”, planning complete, implementation in progress; only X and Y registered, no established backlog owner.

> Registered agents: X, Y. Activity A: active; goal: Ship report; planning complete, implementation in progress.
> - continue — Continue the current Activity.
> - new-task — Describe a task.
> - agent-setup — Describe an agent setup need.
> - help — Refresh this overview.
> - agent:X — Analyze requirements (registered; availability checked when selected).
> - agent:Y — Implement changes (registered; availability checked when selected).
> Choose an option or describe your task.

**Startup alone, no Activity or agents** (AC1, 3, 4, 10): valid empty registry and validated absence.

> No agents are registered, and no Activity is active.
> - new-task — Describe a task.
> - agent-setup — Describe an agent setup need.
> - help — Refresh this overview.
> Choose an option or describe your task.

**Concrete task** (AC2, 4): request “Start HAI and fix the typo in the report”; same A and X/Y facts.

> Registered agents: X, Y. Activity A: active; goal: Ship report; planning complete, implementation in progress. I’ll check continuity and the prerequisites for fixing the typo and proceed if they are satisfied.

No menu selection required; actual execution remains conditional on real checks. The synthetic scenario does not establish that a typo was fixed.

**Fresh registry / Help** (AC3, 7): after an earlier X/Y menu, registry now validly contains Y/Z; request “show the menu”.

> Registered agents: Y, Z. Activity A: active; goal: Ship report; planning complete, implementation in progress.
> - continue — Continue the current Activity.
> - new-task — Describe a task.
> - agent-setup — Describe an agent setup need.
> - help — Refresh this overview.
> - agent:Y — Implement changes (registered; availability checked when selected).
> - agent:Z — Review changes (registered; availability checked when selected).
> Choose an option or describe your task.

X is not offered, and source package W is not labelled registered. An ordinary request “help me fix the report” is interpreted as a concrete task, not an automatic Help request; proceed after continuity and other gates.

**Selections** (AC5, 6, 8): in a current menu where 1=continue and 2=agent:X, synthetic “1” maps to continue after refreshed identity/prerequisites; if the next action is unclear: “What would you like to do next in Activity A?” A synthetic “agent:X” with no assignment receives “What would you like X to do?”; no role is invoked solely by selection. A known prior mapping 2=agent:X followed by removal of X receives “X is no longer registered. Please choose from a refreshed menu or describe your task.” An unknown number with no prior mapping receives “I don’t have a previous numbered menu to interpret that choice; please name an action or request the menu.” Ambiguous “do that” receives “Which action or agent do you mean?” An unknown stable ID receives clarification; it is not remapped. When X remains registered but a verified required model is unavailable, “X is registered, but its required model is unavailable in this host; that assignment is blocked until the requirement is met.” Independent supported operations remain available; no installation or settings change is implied.

**Partial/invalid observations** (AC4, 9): synthetic startup reports valid X, partial registry due to unreadable Y definition, invalid Activity discovery due to malformed state, and separate blocked recording readiness. Candidate:

> X is registered; agent discovery is incomplete because Y's definition could not be read. Activity state could not be verified because its state is malformed; recording readiness is blocked because the assigned source is unavailable.
> - new-task — Describe a task; Activity-dependent work requires the discovery issue to be resolved.
> - agent-setup — Describe an agent setup need; prerequisites will be checked.
> - help — Refresh this overview.
> - agent:X — Analyze requirements (registered; Activity-dependent work blocked).
> Choose an option or describe your task.

If registry itself is invalid, report that issue and do not claim no agents are registered. If Activity A's startup input is truncated, label the displayed text as an excerpt, not a confirmed goal; obtain an authorized full goal or say it is not supplied.

**Many agents** (AC3, 10): synthetic 30 registered agents R01–R30: produce one compact `agent:Rnn` row for each alongside supported task rows, with no length cap omitting agents. This is an instruction-level check of the rule, not a 30-agent live rendering test.

## Acceptance assessment

1. Conditional pass for shared procedure/startup entry: startup-only reports and waits, including current Activity. README conflict above remains open.
2. Instruction-level pass: concrete task summary and continuation without menu selection; no real task execution tested.
3. Instruction-level pass: dynamic registry and complete individual entries, including empty/changed fixtures; no runtime integration tested.
4. Instruction-level pass: identity, goal, lifecycle and steps, validated absence and truncated excerpt distinction; no actual display mutation test.
5. Instruction-level pass: selection mapping, rechecks and missing assignment; no real role dispatch tested.
6. Instruction-level pass: stale, absent numeric mapping, ambiguous and unknown identifiers clarify instead of dispatch.
7. Instruction-level pass: explicit Help refresh; ordinary task containing help remains a task.
8. Instruction-level pass: registered versus availability distinction, blocked dependency and independent capabilities.
9. Instruction-level pass: partial independently valid observations and explicit issues; no invalid fixture runtime run.
10. Conditional pass by procedure: compact format and read-only display rules; actual display/Help side effects not exercised. README wording inconsistency remains.

No automated host interpreter or interactive human acceptance run was performed. These synthetic candidates demonstrate one reasonable interpretation of textual instructions, not proof that every host will follow them or that all runtime issues produce these fixture values. Runtime regression suites are delegated to the host. No product or canonical Activity artifact changed by this reviewer.

## Follow-up recheck

Resolved: README.md lines 33–34 now state that startup reports current work and preserves continuity, and work resumes after a selection or accompanying concrete task. This agrees with the startup-only wait rule. AC1 and AC10's earlier README caveat is resolved; their instruction-level and live-interaction coverage limits remain unchanged. No regression rerun was necessary for this prose correction.
