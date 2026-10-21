## Folder structure

.hai/ - contains the reusable [HAI] framework components
  agents/ - contains subfolders with agents
  concepts/ - contains the concepts definition files
  conventions/ - contains the convention definition files
  tools/ - contains programming code and other related files forming the application layer and stand alone scripts of [HAI]

## agents/ folder structure

agents/ folder contains one and only one subfolder per agent - the [agent-folder]

[agent-folder] MUST contain exactly one file named knowledge.md and other optional files and subfolders 

`knowledge.md` follows the required template in [agent_conv.md](agent_conv.md).
The framework's separate [agent catalogue](../agents/catalogue.md) lives
directly in `agents/` and contains each name, verbatim selection-guide copy,
and definition link so selection does not require opening role files. It is
not an agent definition or a workspace registry.

Optional standard subfolders are `scripts/` for executable helpers and
their usage documentation, and `conventions/` for role-specific rules and
formats. Other justified files and folders are permitted; existing resources
such as environment-manager's `templates/` remain valid. Create only needed
resources. Shared concepts and conventions remain at framework level.

## Workspace agent structure

Workspace agents use `.hai_env/agents/<name>/knowledge.md` with the same
knowledge template and optional resources. Environment state's `agents`
object is their authoritative catalogue, following [state_conv.md](state_conv.md).
Do not initialize environment or create agent scaffolding merely to make
framework definitions available.
