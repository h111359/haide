# HAI environment

## Definition

[environment] is the persistent, installation-specific collection of [HAI] state, optional work records, custom instructions, and references. Its mandatory state lives in `.hai_env/`, separately from the reusable framework in `.hai/`. Optional feature locations are configurable within the workspace.

## Purpose

[environment] preserves the setup and continuity of HAI's work in a [workspace]. It holds HAI's local working material; product implementation belongs in the workspace.

## Explanation

### Components

The only mandatory component is `.hai_env/state.json`. The state contains on/off flags and configurable locations for four optional features:

- Requests, defaulting to `.hai_env/requests`.
- Specification, defaulting to `.hai_env/specifications`.
- Agent instructions, defaulting to `.hai_env/agent_instructions.md`.
- Chronicles, defaulting to `.hai_env/chronicles`.

All optional features are off in a new environment. On leader startup, environment-manager automatically creates an absent `.hai_env/` containing state only. No requests directory, specification content, instructions file, chronicles directory, or agent scaffold is created. The leader then recommends additional setup through chat, where the human chooses which features to enable and which locations to retain or change. Setup may be deferred and all features may remain disabled.

The [state convention](../conventions/state_conv.md) defines configuration, safe workspace paths, compatibility, and validation. State is loaded before optional instructions or current-request context. Optional feature locations may be outside `.hai_env/` but must remain safe inside the workspace. Disabling a feature preserves its files and stops its use through environment configuration; changing its location does not move existing contents. Independent workspace and session instructions still apply. An active request must be resolved before requests can be disabled or relocated.

Enabling specification records a location without fabricating contents or asserting that a specification already exists. Linking an existing specification requires explicitly supplied intent and a verified folder. Chronicles-manager owns session transcripts when recording is enabled; environment-manager owns configuration. Chronicles are distinct from request-specific discussion and do not require requests to be enabled.

The environment may also hold local references and custom agent definitions under `.hai_env/agents/<name>/`. The separate `.hai_env/agents/catalogue.md` Markdown file is their authoritative catalogue and registry, containing definition links and verbatim copies of canonical YAML descriptions. Read it together with `.hai/agents/catalogue.md` for selection; its absence means no registered workspace agents. Normal selection reads catalogue copies. Unregistered agents are unavailable for normal selection, although an explicit human call may load one without registering it. The [agent convention](../conventions/agent_conv.md) defines identity, format, and selection. Workspace-agent-creator creates and registers specialists only in initialized environment; initialization creates no agent files or folders. Framework agents remain available independently of optional features.

Optional `.hai_env/model_profiles.json` maps specialist capability classes to
concrete model IDs. Environment-manager owns explicitly requested profile setup;
state-only initialization creates no profiles. Missing profiles do not invalidate
core state: startup uses the explicitly reported inherited-settings bootstrap in
the [model-profile convention](../conventions/model-profiles_conv.md), and normal
specialist spawning waits for valid runtime-supported resolution or an explicit
human override. Agent definitions and catalogue registration remain independent
of runtime skill discovery.

Existing incomplete or incompatible environment is preserved and reported, rather than silently reinitialized or migrated. Environment is persistent HAI material, not a Python virtual environment or collection of environment variables.

## Supporting Terms

- [state]: mandatory installation-specific HAI configuration, including optional-feature flags and locations and current-request reference.
- [agent_instructions]: optional custom workspace instructions file loaded from its configured location only when its environment feature is enabled, without overriding independent session instructions.
- [chronicles]: optional verbatim session transcripts owned by chronicles-manager, independent of request records.

## References

- `../conventions/model-profiles_conv.md`: optional local specialist model mapping.
- `hai.md`: definition of [HAI] and [workspace].
- `request.md`: definition and lifecycle of [request].
- `specification.md`: definition of [specification].
- `../conventions/state_conv.md`: required state and optional-feature configuration.
- `../agents/chronicles-manager/SKILL.md`: ownership and recording rules for chronicles.
