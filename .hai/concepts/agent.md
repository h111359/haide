# Agent

## Definition

Agent is AI analogue of a team member with specific knowledge and instructions who is doing specific job in the team.

## Purpose

Specialized in specific work and holding the knowledge to do it. Called only when needed so the chat context is not overloaded with the agents which are not needed for the task.

## Explanation

### Identity

Each framework-provided agent role is identified by the name of its folder in `.hai/agents/`.
Workspace agents live in `.hai_env/agents/<name>/`. Names are distinct across
both origins; framework definitions take precedence when a conflict is found.
Conflicting workspace definitions are invalid and must be reported, not repaired.

For example the "leader" is identified by `.hai/agents/leader` and is defined in this folder

### Knowledge

Each agent has a file knowledge.md
When AI should read this knowledge.md file so to become fully onboarded to act in this role.

Every definition follows the common ten-heading template in the
[agent convention](../conventions/agent_conv.md). Its first section,
Selection guide, is canonical short actionable selection text. Copy that
section verbatim into the relevant catalogue, enabling ordinary role selection
without loading definitions. Knowledge files also retain Purpose and Scope;
Definitions includes local terminology and
explicit aliases; References identifies supporting resources and when to read them.

### Availability

Framework roles are always selectable through the separate
[framework catalogue](../agents/catalogue.md). Workspace roles are normally
selectable only when registered with a valid definition path and selection
guide in `.hai_env/agents/catalogue.md`, read together with the framework catalogue.
An explicit human call may select an unregistered workspace role without
registering it. Selection, validation, and collision handling follow the
agent convention. Discovery does not require loading every definition.

### Independence and ownership

Agents are independent roles. Each agent's knowledge.md is the canonical
definition of its own responsibilities and procedures.

Only leader may select another agent, delegate work to it, monitor execution,
and use its results. Leader's instructions may identify the delegated role and
the work being delegated, but MUST NOT define or duplicate that other
agent's responsibilities or procedures. Those belong in the delegated
agent's own knowledge.md.

Specialists are self-sufficient within their scope: they use their inputs,
shared references, and supporting tools, and do not delegate. Missing dependencies
are returned to leader, or discussed with the human when called directly.

### Supporting scripts

An agent may own supporting scripts inside its agent folder. Its
knowledge.md explains when to use them and links to their usage
instructions. Shared tools remain separate from individual agents.
Scripts follow the framework's [tooling convention](../conventions/tooling_conv.md).
Optional standard folders are `scripts/` and `conventions/`; other justified
resources are permitted. Do not create unused supporting folders.

## Supporting Terms

N/A

## References

- `.hai/concepts/hai.md`: definition of [HAI]
- `.hai/conventions/tooling_conv.md`: runtime and placement of supporting scripts
- `../conventions/agent_conv.md`: shared definition format and availability rules
- `../agents/catalogue.md`: framework agent identities and canonical selection guides
