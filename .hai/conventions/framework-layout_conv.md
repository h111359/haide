## Folder structure

.hai/ - contains the reusable [term:HAI] framework components
  agents/ - contains subfolders with agents
  concepts/ - contains the concepts definition files
  conventions/ - contains the convention definition files
  tools/ - contains programming code and other related files forming the application layer and stand alone scripts of [term:HAI]

## agents/ folder structure

agents/ folder contains one and only one subfolder per agent - the [term:agent-folder]

[term:agent-folder] MUST contain exactly one file named SKILL.md and other optional files and subfolders

`SKILL.md` follows the required template in [agent_conv.md](agent_conv.md).
The framework's separate [agent catalogue](../agents/catalogue.md) lives
directly in `agents/` and contains each name, verbatim description copy,
and definition link so selection does not require opening role files. It is
not an agent definition or a workspace registry.

Creating a framework or workspace definition does not create a catalogue entry.
Registration is a separate explicit operation; selection for execution and
delegation require a valid entry in the corresponding catalogue for both origins,
rather than discovering folders. Agent-definition-manager owns definition maintenance; Environment-manager owns
package installation and catalogue mutations for both origins.

Optional standard subfolders are `scripts/` for executable helpers and their usage
documentation, `concepts/` for role-owned definitions, `conventions/` for formats
and domain contracts, and `procedures/` for separate execution procedures.
`SKILL.md` retains the role entry point, scope, exclusions, shared rules, and
canonical procedure triggers under the
[agent convention](agent_conv.md#supporting-resources).
Other justified files and folders are permitted; existing resources
such as environment-manager's `templates/` remain valid. Create only needed
resources. Framework-wide concepts and conventions remain at framework level;
role-owned domain knowledge may live in the owning package as the single public
authority. Other readers link to that authority rather than keeping shared copies.

Procedures use their own Inputs and Outputs tables, entry prerequisites, local
Rules, and ordered Steps under the
[procedure convention](procedure_conv.md). A single procedure may instead remain
inline. Procedure files belong to their role and are not separately registered agents.
Shared role rules remain in `SKILL.md`; a procedure's local rules neither override
nor duplicate them. Meanings and rationale are explained by the
[Procedure concept](../concepts/procedure.md), separately from the format contract.

## Agent configuration resources

Every agent package includes `configuration/contract.json`, declared through its
SKILL string metadata. This required resource is separate from existing role
contracts such as Environment-manager's state `contract.json`. Mutable workspace
values live only at `.hai_env/config/agents/<agent-name>.json`, outside complete
source/installed package replacements. Empty contracts require no values file.
See [agent-configuration_conv.md](agent-configuration_conv.md) for the one format.

## Workspace agent structure

Workspace agents use `.hai_env/agents/<name>/SKILL.md` with the same
definition template and optional resources. `.hai_env/agents/catalogue.md`
is their authoritative Markdown catalogue, following [state_conv.md](state_conv.md).
Do not initialize environment or create agent scaffolding merely to make
framework definitions available.

## Activity resources

Activity-manager owns the canonical [Activity concept](../agents/activity-manager/concepts/activity.md)
and [Activity convention](../agents/activity-manager/conventions/activity_conv.md)
in its package. Core state format 3 retains a mandatory activities.location,
default `.hai_env/activities`, with one fixed current folder and closed archives.
Activity artifacts and optional transcript segments belong there; product code and
durable specification remain at canonical product locations. There is no reusable
framework store, Activity toggle or global chronicles location.

## References

- [term:HAI] → [HAI concept](../concepts/hai.md).
- [term:agent-folder] → [Agent concept](../concepts/agent.md).


## Optional source library

`hai_agents_library/agents/<name>/` contains complete reusable source packages;
`hai_agents_library/README.md` is an installation index, never a runtime registry.
Only `.hai/agents` and `.hai_env/agents` are executable origins. Matching source
and installed names are expected; only installed origins participate in runtime
collision checks. Core remains Leader, Environment-manager and Activity-manager.
The library is not included in the current HAI release package allowlist.
Environment-manager installs only selected complete packages into
`.hai_env/agents/<name>/`, validates them with shared core tools and performs
explicit registration. The library is a development/distribution resource, not a
required external-workspace download. Source updates never update installed snapshots.
