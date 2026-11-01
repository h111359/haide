# HAI

## Definition

[term:HAI] is a framework for AI-assisted development.

## Purpose

[term:HAI] defines a routine for using AI in agentic mode to build or modify
a digital product in a [term:workspace].

## Explanation

### Framework and environment

Reusable framework components live in `.hai/`. They define how HAI works
across workspaces. The persistent, installation-specific [term:environment]
lives in `.hai_env/` and holds HAI's local state, instructions, and work
records. Every substantive HAI task belongs to an [term:Activity], including discussion
and analysis; leader coordinates agents while Activity-manager maintains records
and lifecycle. Product implementation remains in the workspace; a
[term:specification] may optionally reside in the environment or elsewhere.

The reusable framework can be upgraded without replacing the environment's
setup, customizations, or work records. Framework upgrades must respect
the environment format compatibility rules in the state convention.

### Components

The reusable framework contains:

- agents: roles with specific instructions and knowledge; see [term:agent].
- concepts: common meanings, explanations, and rationale.
- conventions: reusable formats, schemas, structures, labels, naming rules, and
  role-independent contracts.
- agent instructions: shared rules in each role's `SKILL.md`, with local
  rules and ordered actions/branches in its owned procedures.
- tools: scripts and applications with their supporting data,
  documentation, media, and other required files.

These components have distinct purposes: a concept explains what something means
and why it exists; a convention defines its reusable representation or contract;
agent rules constrain behavior, and procedure steps describe execution. Linked
sources give each meaning or rule one canonical home instead of copying it between
them. The [Procedure concept](procedure.md) explains prerequisites, shared/local
rules, actions, and local input/output contracts.

Plain wording supports human review of these boundaries. A rule's explicit
requirement, prohibition, or permission is different from an explanation of why
it exists or whether a tool can perform it. The
[instruction-writing convention](../conventions/instruction-writing_conv.md)
defines readable wording without turning an existing preference into a requirement.

### Tools

HAI automation scripts are written in Python and support Windows, Linux,
and macOS. This applies to both shared tools and scripts owned by
individual agents. Runtime, dependency, placement, and testing details
are defined in the [Tooling convention](../conventions/tooling_conv.md).

## Supporting Terms

- [term:workspace]: one or several folders and their subfolder structures where the product is located.
- [term:concept]: a general explanation of an element of [term:HAI]; detailed behavior, structures, and formats belong in the relevant instructions and conventions.
- [term:Activity]: independent substantive work unit with persistent identity, lifecycle and outcome; see the Activity concept.
- [term:specification]: durable product documentation describing its intended behavior, structure, constraints, and relevant domain knowledge.

## References

- [term:environment] → [Environment concept](environment.md).
- [term:Activity] → [Activity concept](../agents/activity-manager/concepts/activity.md): mandatory work context and continuity.
- [term:agent] → [Agent concept](agent.md).
- [Framework layout](../conventions/framework-layout_conv.md): reusable framework folder structure.
- Optional installed Specification-manager provides detailed specification formats; its absence does not affect the generic specification meaning above or core startup.
- `../conventions/state_conv.md`: environment state and compatibility rules.
- `../conventions/tooling_conv.md`: automation tooling conventions.
