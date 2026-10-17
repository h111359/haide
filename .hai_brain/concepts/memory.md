# Memory

## Definition

[memory] is the collection of components of [HAI], which are specific for the [workspace]. 
[memory] contains the [state] for the specific workspace and zero or more [request].

## Purpose

[memory] serves to hold the specific for the workspace parameters, the current and completed requests files.

##  Explanation

### Components

[memory] contains:

- [state]
- [agent_instructions]
- requests folder
- optionnaly [specification] folder

Initialized [memory] is valid with an empty requests folder, no current
[request], and no linked [specification]. Initialization creates empty
memory by default; linking an existing [specification] is a separate,
explicitly requested choice.

## Supporting Terms

- [state]: a file with custom for the workspace parameters values. Important part of the [state] is [specification]

- [agent_instructions]: a file with specific for the workspace instructions to the AI agent, which should be taken in consideration always when AI agent works.

## References

- `.aih_brain/concepts/specification.md`: definition of [specification]
- `.aih_brain/conventions/state_conv.md`: convention of [state]
