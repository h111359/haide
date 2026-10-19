# Request

## Definition

[request] is an iteration of [HAI] in which the user starts with rough idea what [HA] should do, uses [HAI] for clarification of the intent and agreement of the expected outcome and the implementation of the agreed actions. It consist of files for definition of the needed outcome, analysis of the impact, plan for action, log of the executed actions.

[request] is part of [environment]

## Purpose

[request] is the way [HAI] makes consequent chanes to the workspace in auditable from human way. 

## Explanation

### Location

Requests are optional. Creation and loading through environment configuration
require `features.requests.enabled: true` in `.hai_env/state.json`. Every
request occupies a folder directly under `features.requests.location`
(default `.hai_env/requests`), with its components directly inside that
folder or its subfolders. Do not create request records when requests are
disabled; the leader can offer chat setup or continue work without them.
Request-specific discussion is independent from optional session chronicles.

The only nonclosed request uses the fixed folder name
`00000000_000000_active`. Whenever it enters `Closed`, including
cancellation or early closure, its folder is renamed using the UTC
closure timestamp and a short descriptive label. The
[request convention](../conventions/request_conv.md) defines naming,
collision handling, and coordinated state and reference updates.

### Request components

input: Human writes here the initial idea or change request. The request MUST have only one input. 

definition: AI written file containing the request definition after the initial idea from input.md is clarified in stage Clarification. A request has one definition when clarification has been completed and not invalidated; otherwise it may be absent.

analysis: AI written file containing the scope, the affected files of the workspace, edge cases. A request has one analysis when analysis has been completed and not invalidated; otherwise it may be absent.

decisions: Catalogue of questions from AI to human and the answers human has given, with their stage and source. The request has one decisions catalogue, initially empty.

questionnaire: A file containing questions which AI asks to human to take decision or to explain further. A request CAN have multiple questionnaires.

plan: finalized set of steps to be executed during Implement stage. A request has one plan when planning has been completed and not invalidated; otherwise it may be absent.

log: list of records for every action AI has taken during any of the stages. The request MUST have only one log file.

state: Specific for the request file holding the information about the current state of the request and additional service information - the request metadata. The request MUST have only one state file.

discussion: A file with human prompts and AI answers which is independent from the input -> definition -> analysis -> plan flow. Human simultaneously can ask questions and can ask for actions. A dialog between human and AI with questions, answers from AI, ideation and comparison of possible approaches or execution of prompts. 

### Request stages

Initial: The request is initialized with input, decisions, log, state, discussion and is ready for human input.

Clarified: Refine intent defined in the input, scope, constraints, and acceptance criteria. Result is creation of a definition.

Analysed: Inspect the workspace and assess impact, risks, and unknowns. Result is creation of analysis.

Planned: Define implementation and verification steps. Result is creation of a plan.

Implemented: Requested changes and relevant verification have succeeded. Implementation includes appropriate test changes and running relevant checks, comparing results with available acceptance criteria or meaningful input when earlier stages were skipped. Failed or blocked work retains the last completed stage and its actual progress in the log. Relevant specification updates go through leader to specification-manager when that feature is enabled; disabled specification is recorded as unavailable and does not implicitly enable it.

Closed: Completion of the request and leaving it in final state

### Request lifecycle

Only one request could be in stage different from Closed at a given moment.

Initialization -> Clarification -> Analysis -> Planning -> Implement -> Closure

Transition to Closure can be made from any stage in any moment of request life

Implement can be invoked in any stage except when the request is closed. It skips missing Clarification, Analysis, and Planning stages without creating their artifacts. Meaningful human input is required regardless of the current stage; if absent, execution stops and the human is notified. Ask only for missing information necessary to execute the requested work.

Clarification can be invoked multiple times before implementation starts. It replaces the previous definition if present. New clarification invalidates Analysis and Plan if present.

Analysis can be invoked multiple times before implementation starts. It replaces previous analysis if present. New analysis invalidates Plan if present.

Planning can be invoked multiple times before implementation starts. It replaces the previous plan if present.

The first implementation attempt permanently freezes the existing definition,
analysis, and plan, even if implementation fails or is interrupted. Skipped
artifacts remain absent; they are not backfilled on retries. Subsequent decisions
and deviations are recorded in decisions and log. Normal analysis requires a
definition and normal planning requires definition and analysis; explicit Implement
is the path that skips missing stages.

Request-manager owns the request records, lifecycle, implementation, and testing.
It sets or clears the environment's current-request reference only as part of
initialization or closure. Leader coordinates other specialists; environment-manager
retains ownership of general environment configuration, and specification-manager
retains ownership of durable specification edits. Creating an agent does not enable
requests or create a live request.

## Supporting Terms

N/A

## References

- `.hai/concepts/environment.md`: definition of [environment]
- `../conventions/request_conv.md`: request folder naming and closure rules
