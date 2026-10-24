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

All optional features are off in a newly initialized core state. On leader startup,
leader uses the shared read-only startup helper for existing-state validation and
bounded context loading without an environment-manager round trip. When state is
safely absent, environment-manager creates `.hai_env/state.json` only, creating its
container if needed. An existing `.hai_env/` may hold independent resources; preserve
them without treating the container alone as initialized core state. Initialization
creates no optional resources or agent scaffold. The leader then recommends chat
setup, where the human chooses features and locations. Setup may be deferred.

The [state convention](../conventions/state_conv.md) defines configuration, safe workspace paths, compatibility, and validation. State is loaded before configured optional context. Optional feature locations may be outside `.hai_env/` but must remain safe inside the workspace. Disabling a feature preserves its files and stops its use through environment configuration; changing its location does not move existing contents. Independent workspace and session instructions still apply.

Request configuration contains only enablement and the store location, with no
global active-request pointer. Environment validation checks its path and type,
not request records or stages; an absent store is valid configuration. Startup
does not discover or resume requests. Explicit enablement may create an empty
store; it never creates request records. Record handling is a separate task.

Enabling specification records a location without fabricating contents or asserting that a specification already exists. Linking an existing specification requires explicitly supplied intent and a verified folder. Chronicles-manager owns session transcripts when recording is enabled; environment-manager owns configuration. Chronicles are distinct from request-specific discussion and do not require requests to be enabled.

Chronicles synchronize asynchronously from completed messages in the durable saved
session source by default, without a new state flag or schema migration. Response
delivery does not wait for optional recording. If the runtime cannot continue after
delivery, leader routes catch-up at the next active turn and reports recording as
deferred. Missing sources and existing divergence remain unresolved issues, not
permission to reconstruct or repair records. Mandatory workspace timing requirements
take precedence; chronicles-manager defines synchronization and verification.

HAI-managed feature work requires validated enablement and location context.
Standalone capabilities do not bypass that configuration. Detailed content rules
and procedures belong to the selected role; leader owns handoff and setup routing.

The environment may also hold local references and custom agent definitions under
`.hai_env/agents/<name>/`. The separate `.hai_env/agents/catalogue.md` is their
authoritative catalogue and registry, containing definition links and verbatim
copies of canonical YAML descriptions. Read it together with the framework catalogue
for selection; its absence means no registered workspace agents. Both origins use
catalogue entries for normal selection. An explicit human call may load an
unregistered workspace definition without registering it. The
[agent convention](../conventions/agent_conv.md) defines identity, format, and selection.
Agent-definition-manager owns definitions and catalogue mutations; workspace mutations
require valid initialized environment context. Framework maintenance and read-only
definition inspection do not require environment initialization. Creating a definition
does not register it, and environment initialization creates no agent resources.
Registered framework agents remain available independently of optional features.

Optional `.hai_env/model_profiles.json` maps specialist capability classes to
concrete model IDs. Environment-manager owns explicitly requested profile setup;
state-only initialization creates no profiles. Missing profiles do not invalidate
core state: the read-only helper requires no specialist profile. Delegated startup
uses the explicitly reported inherited-settings bootstrap when applicable under
the [model-profile convention](../conventions/model-profiles_conv.md), and normal
specialist spawning waits for valid runtime-supported resolution or an explicit
human override. Agent definitions and catalogue registration remain independent
of runtime skill discovery.

Existing malformed, unreadable, conflicting, or incompatible core state is preserved
and reported rather than silently reinitialized or migrated. A known partial
initialization is not automatically retried. Environment is persistent HAI material,
not a Python virtual environment or collection of environment variables.

## Supporting Terms

- [state]: mandatory installation-specific HAI configuration, including optional-feature flags and locations.
- [agent_instructions]: optional custom workspace instructions file loaded from its configured location only when its environment feature is enabled, without overriding independent session instructions.
- [chronicles]: optional verbatim session transcripts owned by chronicles-manager, independent of request records.

## References

- `../conventions/model-profiles_conv.md`: optional local specialist model mapping.
- `hai.md`: definition of [HAI] and [workspace].
- `../conventions/state_conv.md`: required state and optional-feature configuration.
- `../conventions/agent_conv.md`: agent identity, catalogue selection, and registration contract.
