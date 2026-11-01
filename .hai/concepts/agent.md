# Agent

## Definition

An agent is an AI role with defined responsibilities, instructions, and knowledge
for a particular kind of work.

## Purpose

An agent provides the knowledge needed for its assigned work. Loading only the
needed roles keeps unrelated instructions out of the active chat context.

## Explanation

### Identity

Each framework-provided agent role is identified by the name of its folder in `.hai/agents/`.
Workspace agents live in `.hai_env/agents/<name>/`. Names are distinct across
both origins; framework definitions take precedence when a conflict is found.
Conflicting workspace definitions are invalid rather than implicit overrides.

For example, `.hai/agents/leader` contains the leader's definition.

### Knowledge

Each agent has a `SKILL.md` with Agent Skills style YAML frontmatter and
Markdown instructions. The full selected file establishes the adopted role's instructions.
The format alone does not install a runtime skill or spawn an agent.

Required `name` matches the agent folder; the decoded `description` is canonical
short selection text and the catalogue guide is its exact copy. Specialist `metadata` declares generic
`hai-model-class` and `hai-reasoning-effort` strings. Local model profiles map
classes to model IDs; leader validates the exact pair against current runtime
capabilities. Leader stays in the root chat with interface-selected settings.
The role body separates purpose, ownership, exclusions, shared rules, procedure
selection, and references. The [agent convention](../conventions/agent_conv.md)
defines its exact representation. Shared rules have readable unique titles
without IDs, with optional subject groups that imply no priority. Concepts remain
in declared concept sources rather than embedded definitions.
References identify supporting resources and when they are needed.

Plain rules distinguish required actions, prohibited actions, and allowed choices.
Explicit MUST/MUST NOT/MAY wording makes those meanings visible, while an available
tool still says nothing about permission. Clear actors, concrete actions, and
stated conditions help a human review the rule; keywords alone cannot establish
clarity or preserve the meaning of an older rule. The Procedure concept explains
these meanings and the writing convention defines their representation.

### Availability

Selection for execution and delegation require a valid entry in the corresponding
catalogue for both origins: the [framework catalogue](../agents/catalogue.md) or
`.hai_env/agents/catalogue.md`. Together they describe registered availability. Registered framework roles
remain selectable without initialized environment. Creating a definition alone
does not register it; registration must be explicitly requested.
An explicit name or path does not bypass registration or authorize it.
Unregistered definitions in either origin can be inspected, maintained, validated,
or registered without executing them. Selection, validation, and collision handling
follow the agent convention. Discovery does not require loading every definition.

### Independence and ownership

Agents are independent roles. Each agent's SKILL.md defines the role and its
shared rules. It selects its execution procedures by explicit
triggers; linked procedure files contain their own description, inputs,
prerequisites, local rules, steps, outputs, and references. A single procedure may
remain inline. Shared rules always apply; local rules are only additional
procedure-specific obligations, never overrides or copies. Prerequisites are entry
conditions and steps are ordered actions/branches, not a list of ongoing rules.
The [Procedure concept](procedure.md) explains these distinctions and why literal
named input/output references are local rather than inherited parameters.
Executing a procedure stays in the same role; it is not another agent invocation
or registration.

Agent-definition-manager maintains definitions and their necessary resources in
both origins, owns explicitly requested registration, and synchronizes an existing
entry when its definition changes. Audits are read-only; updating an unregistered
definition does not register it. Environment-manager owns core environment and
model-profile configuration and lightweight startup-validation policy. Leader retains execution ownership and may
run the shared read-only startup helper directly for existing-state validation;
core initialization and core environment/profile configuration changes remain
environment-manager work. Optional extension owners retain their declared scope.

Substantive specialist work receives the current Activity ID/path and relevant
context through leader; Activity-manager owns records and lifecycle, not orchestration.
Bootstrap/setup and read-only diagnosis follow the shared bounded exceptions.

Only leader may select another agent, delegate work to it, monitor execution,
and use its results. Leader's handoffs identify the delegated role and work;
the delegated agent's own SKILL.md and procedure files define its responsibilities
and execution procedures rather than competing caller definitions.

Specialists are self-sufficient within their scope: they use their inputs,
shared references, and supporting tools, and do not delegate. Missing dependencies
are returned to leader, or discussed with the human when called directly.

### Optional workspace extensions

A workspace agent may extend one installation without becoming a core framework
dependency. Its definition is still subject to the same explicit registration and
leader-owned delegation boundaries. Installing a folder or retaining its data
does not activate a capability or authorize execution. Core initialization and
startup remain independent of optional workspace agents and their tooling; an
extension's own declared configuration and scoped state ownership belong to that
extension rather than changing the core environment contract.

### Supporting scripts

An agent may own supporting scripts inside its agent folder. Its
SKILL.md explains when to use them and links to their usage
instructions. Shared tools remain separate from individual agents.
Scripts follow the framework's [tooling convention](../conventions/tooling_conv.md).
Optional standard folders are `scripts/`, `procedures/`, `concepts/`, and `conventions/`; other justified
resources are permitted. Supporting folders serve actual resources rather than
unused scaffolding.

## Supporting Terms

- [term:agent-folder]: the single canonical folder for an agent under its framework or workspace origin.

## References

- [term:HAI] → [HAI concept](hai.md).
- `.hai/conventions/tooling_conv.md`: runtime and placement of supporting scripts
- `../conventions/agent_conv.md`: shared definition format and availability rules
- `../agents/catalogue.md`: framework agent identities and copied descriptions
- `../conventions/model-profiles_conv.md`: local models and runtime resolution
- [Procedure convention](../conventions/procedure_conv.md): procedure layout and local input/output scope.
- [Procedure concept](procedure.md): shared/local rules, prerequisites, ordered actions, and literal local contracts.
- [Reference notation](../conventions/reference-notation_conv.md): literal namespaced references.
- [Instruction writing](../conventions/instruction-writing_conv.md): plain wording and explicit rule strength, without changing existing permission or preferences.
