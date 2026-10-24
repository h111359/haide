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

Each agent has a `SKILL.md` with Agent Skills style YAML frontmatter and
Markdown instructions. Read the full file when adopting the selected role.
The format alone does not install a runtime skill or spawn an agent.

Required `name` matches the agent folder; `description` is canonical short
selection text copied into the catalogue. Specialist `metadata` declares generic
`hai-model-class` and `hai-reasoning-effort` strings. Local model profiles map
classes to model IDs; leader validates the exact pair against current runtime
capabilities. Leader stays in the root chat with interface-selected settings.
The [agent convention](../conventions/agent_conv.md) defines the nine ordered
body sections beginning Purpose, without an agent H1 or Selection guide section.
Definitions holds local terms and aliases; References identifies supporting
resources and when to read them.

### Availability

Normal selection requires a valid entry in the corresponding catalogue for both
origins: the [framework catalogue](../agents/catalogue.md) or
`.hai_env/agents/catalogue.md`. Read both together. Registered framework roles
remain selectable without initialized environment. Creating a definition alone
does not register it; registration must be explicitly requested.
An explicit human call may select an unregistered workspace role without
registering it. Unregistered framework definitions can be inspected and maintained,
but require registration before execution. Selection, validation, and collision handling follow the
agent convention. Discovery does not require loading every definition.

### Independence and ownership

Agents are independent roles. Each agent's SKILL.md is the canonical
definition of its own responsibilities and procedures.

Agent-definition-manager maintains definitions and their necessary resources in
both origins, owns explicitly requested registration, and synchronizes an existing
entry when its definition changes. Audits are read-only; updating an unregistered
definition does not register it. Environment-manager owns configuration and
lightweight startup-validation policy. Leader retains execution ownership and may
run the shared read-only startup helper directly for existing-state validation;
initialization and configuration changes remain environment-manager work.

Only leader may select another agent, delegate work to it, monitor execution,
and use its results. Leader's instructions may identify the delegated role and
the work being delegated, but MUST NOT define or duplicate that other
agent's responsibilities or procedures. Those belong in the delegated
agent's own SKILL.md.

Specialists are self-sufficient within their scope: they use their inputs,
shared references, and supporting tools, and do not delegate. Missing dependencies
are returned to leader, or discussed with the human when called directly.

### Supporting scripts

An agent may own supporting scripts inside its agent folder. Its
SKILL.md explains when to use them and links to their usage
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
- `../agents/catalogue.md`: framework agent identities and copied descriptions
- `../conventions/model-profiles_conv.md`: local models and runtime resolution
