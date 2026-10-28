# HAI

## Definition

[HAI] is a framework for AI-assisted development.

## Purpose

[HAI] defines a routine for using AI in agentic mode to build or modify
a digital product in a [workspace].

## Explanation

### Framework and environment

Reusable framework components live in `.hai/`. They define how HAI works
across workspaces. The persistent, installation-specific [environment]
lives in `.hai_env/` and holds HAI's local state, instructions, and work
records. Every substantive HAI task belongs to an [Activity], including discussion
and analysis; leader coordinates agents while Activity-manager maintains records
and lifecycle. Product implementation remains in the workspace; a
[specification] may optionally reside in the environment or elsewhere.

The reusable framework can be upgraded without replacing the environment's
setup, customizations, or work records. Framework upgrades must respect
the environment format compatibility rules in the state convention.

### Components

The reusable framework contains:

- agents: roles with specific instructions and knowledge; see [agent].
- concepts: common definitions, explanations, and rules.
- conventions: formats, schemas, structures, labels, and naming rules.
- tools: scripts and applications with their supporting data,
  documentation, media, and other required files.

### Tools

HAI automation scripts are written in Python and support Windows, Linux,
and macOS. This applies to both shared tools and scripts owned by
individual agents. Runtime, dependency, placement, and testing details
are defined in the [Tooling convention](../conventions/tooling_conv.md).

## Supporting Terms

- [workspace]: one or several folders and their subfolder structures where the product is located.
- [concept]: a general explanation of an element of [HAI]; detailed behavior, structures, and formats belong in the relevant instructions and conventions.
- [Activity]: independent substantive work unit with persistent identity, lifecycle and outcome; see the Activity concept.
- [specification]: durable product documentation describing its intended behavior, structure, constraints, and relevant domain knowledge.

## References

- `environment.md`: definition of [environment].
- `../agents/activity-manager/concepts/activity.md`: mandatory Activity work context and continuity.
- `agent.md`: definition of [agent].
- `../conventions/framework-layout_conv.md`: reusable framework folder structure.
- `../conventions/state_conv.md`: environment state and compatibility rules.
- `../conventions/tooling_conv.md`: automation tooling conventions.
