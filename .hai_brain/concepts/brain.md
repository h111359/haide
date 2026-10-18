# Brain

## Definition

[brain] is the collection of components of HAI framework, which are not specific for the workspace where the framework is isntalled. It contains the concepts, conventions, instructions, tools and define how the framework should work in general.

## Purpose

[brain] controls the behavior and defines the outcome of HAI. 
[brain] could be replaced with newer version, upgraded, without loosing the setup and context specific for the workspace where HAI is installed.

## Explanation

### Components

[brain] contains:

- agents
- concepts
- conventions
- prompts
- tools

### Agents

Agents are personalities with specific instructions and knowledge. Like different roles in a team. See definition of [agent]

### Concepts

Concepts are files containing common definitions, explanations, rules.

### Conventions

Conventions are files defining the formats, schemas, shapes, labels, names, enumerations.

### Prompts

Prompts are definition of behavior, actions that need to be performed.

### Tools

Tools are scripts, applications and other accelerators with their supporting data, media, documentation or other needed files.

HAI automation scripts are written in Python and support Windows, Linux,
and macOS. This applies to both shared tools and scripts owned by
individual agents. Runtime, dependency, placement, and testing details
are defined in the [Tooling convention](../conventions/tooling_conv.md).

## Supporting Terms

- [concept]: general explanation of element of [HAI] without details for behavior, structure or format 

## References

- `.aih_brain/concepts/hai.md` - definition of [HAI] 
- `.hai_brain\conventions\brain_conv.md` - folder structure of [brain]
- `.hai_brain\concepts\agent.md` - definition of [agent]
- `.hai_brain/conventions/tooling_conv.md` - automation tooling conventions
