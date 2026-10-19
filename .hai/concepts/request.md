# Request

## Definition

[request] is an iteration of [HAI] in which the user starts with rough idea what [HA] should do, uses [HAI] for clarification of the intent and agreement of the expected outcome and the implementation of the agreed actions. It consist of files for definition of the needed outcome, analysis of the impact, plan for action, log of the executed actions.

[request] is part of [environment]

## Purpose

[request] is the way [HAI] makes consequent chanes to the workspace in auditable from human way. 

## Explanation

### Location

Every request consist of a folder in .hai_env/requests/ with all of its components located directly or in subfolders of this request folder

The only nonclosed request uses the fixed folder name
`00000000_000000_active`. Whenever it enters `Closed`, including
cancellation or early closure, its folder is renamed using the UTC
closure timestamp and a short descriptive label. The
[request convention](../conventions/request_conv.md) defines naming,
collision handling, and coordinated state and reference updates.

### Request components

input: Human writes here the initial idea or change request. The request MUST have only one input. 

definition: AI written file containing the request definition after the initial idea from input.md is clarified in stage Clarification. The request MUST have only one definition.

analysis: AI written file containing the scope, the affected files of the workspace, edge cases. The request MUST have only one analysis.

decisions: Catalogue of questions from AI to human and the answers human has given during Clarification or Analysis stages. The request must have only one decisions catalogue file.

questionnaire: A file containing questions which AI asks to human to take decision or to explain further. A request CAN have multiple questionnaires.

plan: finalized set of steps to be executed during Implement stage. The request MUST have only one plan.

log: list of records for every action AI has taken during any of the stages. The request MUST have only one log file.

state: Specific for the request file holding the information about the current state of the request and additional service information - the request metadata. The request MUST have only one state file.

discussion: A file with human prompts and AI answers which is independent from the input -> definition -> analysis -> plan flow. Human simultaneously can ask questions and can ask for actions. A dialog between human and AI with questions, answers from AI, ideation and comparison of possible approaches or execution of prompts. 

### Request stages

Initial: The request is initialized with input, log, state, discussion and is ready for human input.

Clarified: Refine intent defined in the input, scope, constraints, and acceptance criteria. Result is creation of a definition.

Analysed: Inspect the workspace and assess impact, risks, and unknowns. Result is creation of analysis.

Planned: Define implementation and verification steps. Result is creation of a plan.

Implemented: Apply changes and record progress. Create new tests. Run tests and improves until all tests are passed. Compare results with acceptance criteria and update relevant specification.

Closed: Completion of the request and leaving it in final state

### Request lifecycle

Only one request could be in stage different from Closed at a given moment.

Initialization -> Clarification -> Analysis -> Planning -> Implement -> Closure

Transition to Closure can be made from any stage in any moment of request life

Implement can be invoked in any stage except when the request is closed. In case Implement is requested during Initialization and no input is defined - the execution stops and the human is notified.

Clarification can be invoked multiple times before Implementation. It replaces the previous definition if exist. After Implmentation - it should remain fixed forever. New clarification invalidates Analysis and Plan if exist.

Analysis can be invoked multiple times before Implementation. It replaces previous analysis if exists. After Implmentation - it should remain fixed forever. New analysis invalidates Plan if exists.

Analysis can be invoked multiple times before Implementation. It replaces previous plan if exists. After Implmentation - it should remain fixed forever. 

## Supporting Terms

N/A

## References

- `.hai/concepts/environment.md`: definition of [environment]
- `../conventions/request_conv.md`: request folder naming and closure rules
