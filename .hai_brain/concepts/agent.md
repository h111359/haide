# Agent

## Definition

Agent is AI analogue of a team member with specific knowledge and instructions who is doing specific job in the team.

## Purpose

Specialized in specific work and holding the knowledge to do it. Called only when needed so the chat context is not overloaded with the agents which are not needed for the task.

## Explanation

### Identity

Each agent role is identified by the name of its folder in .hai_brain/agents/

For example the "leader" is identified by `,hai_brain/agents/leader` and is defined in this folder

### Knowledge

Each agent has a file knowledge.md
When AI should read this knowledge.md file so to become fully onboarded to act in this role.

### Independence and ownership

Agents are independent roles. Each agent's knowledge.md is the canonical
definition of its own responsibilities and procedures.

An agent may select another agent, delegate work to it, monitor execution,
and use its results. Its instructions may identify the delegated role and
the work being delegated, but MUST NOT define or duplicate that other
agent's responsibilities or procedures. Those belong in the delegated
agent's own knowledge.md.

### Supporting scripts

An agent may own supporting scripts inside its agent folder. Its
knowledge.md explains when to use them and links to their usage
instructions. Shared tools remain separate from individual agents.
Scripts follow the framework's [tooling convention](../conventions/tooling_conv.md).

## Supporting Terms

N/A

## References

- `.hai_brain\concepts\brain.md`: definition of [brain]
- `.hai_brain/conventions/tooling_conv.md`: runtime and placement of supporting scripts
