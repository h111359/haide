# HAI environment

## Definition

[environment] is the persistent, installation-specific collection of
[HAI] state, work records, custom instructions, and references. It lives
in `.hai_env/`, separately from the reusable framework in `.hai/`.

## Purpose

[environment] preserves the setup and continuity of HAI's work in a
[workspace], including current and completed [request] records. It
contains HAI's local working material; product implementation belongs
in the workspace.

## Explanation

### Components

[environment] contains:

- [state].
- [agent_instructions].
- a requests folder containing zero or more [request] records.
- optionally, a [specification] folder; its location is configurable.

The environment may also hold local references and custom agent definitions
under `.hai_env/agents/<name>/`. Environment state's optional `agents` object
is their authoritative catalogue and registration list, with each entry
holding a canonical definition path and short actionable selection guide.
The guide is a verbatim copy of the canonical Selection guide section in
the definition; normal selection reads the catalogue copy.
Unregistered agents
are unavailable for normal selection, although an explicit human call may
load one without registering it. The [agent convention](../conventions/agent_conv.md)
defines identity, common knowledge structure, and selection rules. The
workspace-agent-creator creates and registers workspace specialists only in
an already initialized environment. These possibilities do not require
creating agent files or folders during initialization.

Initialized [environment] is valid with an empty requests folder, no
current [request], and a configured [specification] location whose folder
may not exist yet. The default location is `.hai_env/specifications`.
During initialization, the environment-manager asks whether to keep that
default or use another workspace-relative location. A specification may
therefore live outside `.hai_env/`. Recording a location does not create
specification folders or content; linking an existing specification is
a separate, explicitly requested choice.

The environment is persistent HAI material, including active state and
historical work records. It is not a Python virtual environment or a
collection of environment variables.

## Supporting Terms

- [state]: a file holding installation-specific HAI parameters, including the specification location and current-request reference.
- [agent_instructions]: a file holding custom instructions that apply whenever an AI agent works in this workspace.

## References

- `hai.md`: definition of [HAI] and [workspace].
- `request.md`: definition and lifecycle of [request].
- `specification.md`: definition of [specification].
- `../conventions/state_conv.md`: convention of [state].
