# Request

## Definition

[request] is a tracked unit of work that carries human intent through clarification,
impact analysis, planning, implementation, verification, and an explicit recorded
outcome. Its files preserve initial input, decisions, work history, and lifecycle state.

## Purpose

A request makes workspace changes and their reasoning understandable and auditable
without requiring a particular coordinating agent or environment system.

## Explanation

### Location

Requests are managed on demand in an explicitly selected request store. Standalone
use defaults to `.hai_env/requests` under the supplied workspace, with an explicit
folder override allowed. HAI-managed use requires the caller's validated assurance
of enabled requests and the configured store; the manager does not read HAI state.
A disabled or conflicting HAI configuration cannot be bypassed using standalone mode.
Each request occupies one direct child folder of its store. Request-specific
discussion is independent from optional session transcripts.

The human must clearly intend to create a tracked request before its store or
records are initialized. Selecting the role, ordinary use of the word "request",
or asking for analysis does not authorize creation. Ambiguity requires clarification.
If existing active work is absent, report that condition rather than create a fallback.

The only nonclosed request uses the fixed folder name
`00000000_000000_active`. Whenever it enters `Closed`, including
cancellation or early closure, its folder is renamed using the UTC
closure timestamp and a short descriptive label. The
[request convention](../conventions/request_conv.md) defines naming,
collision handling, path safety, and coordinated record and reference updates.
The active folder and its own `state.json` identify active work. There is no
collection-level state file or external active-request pointer.

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

Implemented: Requested changes and relevant verification have succeeded. Implementation includes appropriate test changes and running relevant checks, comparing results with available acceptance criteria or meaningful input when earlier stages were skipped. Failed or blocked work retains the last completed stage and its actual progress in the log. Required specification or other external work is reported to the caller and must be resolved before this stage is recorded; the manager invokes no other agents.

Closed: Completion of the request and leaving it in final state

### Request lifecycle

At most one request in a supplied store may be in a stage other than Closed.
This invariant is local to that store; it does not require discovering other stores.

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
The caller supplies authority, applicable instructions, integration context, and
results of required external work. Request management does not change global
configuration, register agents, or maintain session transcripts. Creating or
selecting an agent does not create a live request.

## Supporting Terms

- [request store]: the selected directory holding request folders and defining the
  scope of the one-nonclosed-request invariant.

## References

- `../conventions/request_conv.md`: request folder naming and closure rules
- `../SKILL.md`: request-manager procedures and invocation contract
