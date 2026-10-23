## Folder structure

.hai/ - contains the reusable [HAI] framework components
  agents/ - contains subfolders with agents
  concepts/ - contains the concepts definition files
  conventions/ - contains the convention definition files
  tools/ - contains programming code and other related files forming the application layer and stand alone scripts of [HAI]

## agents/ folder structure

agents/ folder contains one and only one subfolder per agent - the [agent-folder]

[agent-folder] MUST contain exactly one file named SKILL.md and other optional files and subfolders

`SKILL.md` follows the required template in [agent_conv.md](agent_conv.md).
The framework's separate [agent catalogue](../agents/catalogue.md) lives
directly in `agents/` and contains each name, verbatim description copy,
and definition link so selection does not require opening role files. It is
not an agent definition or a workspace registry.

Creating a framework or workspace definition does not create a catalogue entry.
Registration is a separate explicit operation; normal selection uses the
corresponding catalogue rather than discovering folders. Agent-definition-manager
owns definition maintenance and catalogue mutations for both origins.

Optional standard subfolders are `scripts/` for executable helpers and
their usage documentation, and `conventions/` for role-specific rules and
formats. Other justified files and folders are permitted; existing resources
such as environment-manager's `templates/` remain valid. Create only needed
resources. Framework-wide concepts and conventions remain at framework level;
role-owned domain knowledge may live in the owning package as the single public
authority. Other readers link to that authority rather than keeping shared copies.

## Workspace agent structure

Workspace agents use `.hai_env/agents/<name>/SKILL.md` with the same
definition template and optional resources. `.hai_env/agents/catalogue.md`
is their authoritative Markdown catalogue, following [state_conv.md](state_conv.md).
Do not initialize environment or create agent scaffolding merely to make
framework definitions available.
