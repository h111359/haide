# HAI environment

## Definition

[term:environment] is HAI's persistent installation-specific configuration, instructions,
Activities, optional records and local references. Mandatory configuration lives
in `.hai_env/`, separately from reusable framework material in `.hai/`.

## Purpose

The environment preserves setup and continuity across chats while product code
and durable specification remain in their canonical product locations.

## Explanation

### Mandatory context and Activities

Mandatory files are `.hai_env/state.json` and fixed `.hai_env/agent_instructions.md`.
Instruction availability is independent of state validity: empty readable content
adds no instructions, while missing or unreadable content leaves dependent work
without its required context. Instructions have no configurable location or
enabled flag. The state convention defines file, containment, and compatibility
contracts; the owning agents define loading, diagnosis, and repair workflows.

The configured Activity store supplies continuity for every substantive HAI task,
including advice, brainstorming, analysis, planning, maintenance, implementation,
and verification. Activities are mandatory rather than an optional feature. A new
chat is not a new work identity. One current Activity and closed history preserve
the distinction between continuity, a new objective, and a lifecycle decision.
Bounded startup/setup and read-only diagnosis exist to establish usable context,
not as an alternative to tracking later substantive work.

Environment-manager owns core configuration and availability checks; Activity-manager
owns record discovery, artifacts, and lifecycle. Leader alone coordinates agents
and boundary decisions. Configuration availability is distinct from discovery of
the current record, so startup does not infer current work by scanning the store.
Activity identity, lifecycle, performed steps, and closure outcome have different
meanings, explained in the Activity concept and its supporting sources.

### Optional features and transcripts

Chronicles is an optional core feature, initially disabled. Specification is an
optional installed-agent capability whose owned settings also default disabled.
Their settings express capability choices, not evidence that content exists.
Disabling preserves content; a changed location is a reference change rather than
an implicit move or deletion. Feature enablement, agent registration, and task
permission are separate: a registered role's availability does not enable a disabled
capability or establish permission to use it.

Chronicles are exact-source transcript segments assigned to Activities, with no
global transcript store. A chat may span Activities, and an Activity may contain
segments from several chats. Segment attribution and source coverage distinguish
the work record from the chat container. Enabling recording covers subsequent
exchanges; historical imports are distinct provenance-sensitive work rather than
implicit backfill. Late synchronization or attributable supplements to closed work
are different from new substantive continuation.

Asynchronous recording separates transcript catch-up from task delivery, while
mandatory timing and requested synchronous verification still determine when
recording evidence is required.
Pending synchronization is not completed coverage, and after-turn continuation
depends on actual runtime support. Leader owns attribution and prompt-batch
scheduling; Activity-manager owns source-backed synchronization and evidence in
separate recording procedures. The configurable prompt threshold defaults to five.
Ordinary Activity edits and transcript batches are separate operations. When
recording is enabled or independently mandatory, fresh recording coverage is a
closure prerequisite. Owner procedures define ordering, source failures, disabled
behavior and the mandatory pre-delivery exception.

### Startup, configuration and compatibility

Startup is a read-only observation of existing context; initialization creates
minimal core configuration, and migration transforms explicitly scoped existing
data. These operations are not interchangeable. Safely absent state differs from
invalid, incompatible, or unverified state. Minimal initialization preserves existing
resources and does not fabricate optional content, work records, profiles, or agents.
Optional chat setup is distinct from establishing the mandatory core environment.

The installed environment-manager contract defines supported state formats
independently of framework release numbering. A version marker alone cannot migrate
structure or history. Environment configuration migration and Activity/transcript
migration have separate owners and scopes. Leader's bounded read-only helper
exception does not transfer environment mutation ownership. The state convention
defines compatibility; owner procedures define initialization, validation, and migration.

### Agent-owned settings

Each agent declares its configuration contract in the installed package. Saved
values live at `.hai_env/config/agents/<agent-name>.json`; missing files use declared
defaults and invalid values affect dependent work. Package upgrades preserve these
external files. Git and Specification-manager settings use this location; chronicles and
Activity location retain central ownership in state format 3. Format 2 is read-only
migration context for explicit specification extraction.
Instructions, catalogues and model profiles keep their separate locations.
The [configuration concept](agent-configuration.md) explains the distinction.

### Agents, profiles and extensions

Workspace definitions and their catalogue live under `.hai_env/agents/`; an absent
catalogue means no registered workspace agents. Framework and workspace registration
are both eligibility contracts, separate from definition creation or maintenance.
An explicit name or path identifies an agent; it does not register it or permit execution.
An installed registered Agent-definition-manager owns definitions/catalogue mutations; its absence blocks that optional work, not startup. Leader owns selection
and delegation. The Agent concept explains this boundary. Compatible initialized
context underpins workspace mutations; independent read-only format inspection and
prerequisite diagnosis are distinct from substantive tracked maintenance.

Optional `.hai_env/model_profiles.json` maps specialist classes to concrete model
IDs. Profiles separate reusable role requirements from installation-specific model
choices; runtime evidence establishes whether a requested pair is actually supported.
Environment-manager owns profile configuration. Absent profiles do not invalidate
core state or imply permission to guess settings. Exact resolution, explicit human
overrides, and the bounded inherited startup bootstrap are distinct cases defined
by the model-profile convention and leader's procedures.

Selecting an optional workspace extension for execution requires valid registration
and the user's agreed task and permission. Core startup and minimal initialization require no extension
agent or extension tooling. An extension owns its declared agent configuration rather than general
environment configuration. Remaining legacy state subtrees stay opaque. Unknown
extension values are preserved but not interpreted by the core: preservation is
not validation or activation.

## Supporting Terms

- [term:state]: mandatory format-versioned HAI configuration, including Activity location and optional settings.
- [term:agent_instructions]: fixed mandatory instructions, independently loaded; empty adds no instructions.
- [term:chronicles]: optional exact-source Activity transcript segments owned by Activity-manager.

## References

- [term:Activity] → [Activity concept](../agents/activity-manager/concepts/activity.md): mandatory independent work unit and continuity.
- [State convention](../conventions/state_conv.md): configuration schema, safe paths and authorized migration.
- [Agent convention](../conventions/agent_conv.md): identities, catalogues, handoffs and registration.
- [Model profiles](../conventions/model-profiles_conv.md): local mappings, bootstrap and runtime resolution.
- [Environment-manager](../agents/environment-manager/SKILL.md): configuration, profile, initialization, validation, and migration procedures.
- [Leader](../agents/leader/SKILL.md): startup, boundary decisions, delegation, and recording coordination.
- [Activity-manager](../agents/activity-manager/SKILL.md): exact-source synchronization, synchronous verification, and timing exceptions.
- [HAI](hai.md): reusable framework and product workspace boundaries.
