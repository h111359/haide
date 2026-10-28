# HAI environment

## Definition

[environment] is HAI's persistent installation-specific configuration, instructions,
Activities, optional records and local references. Mandatory configuration lives
in `.hai_env/`, separately from reusable framework material in `.hai/`.

## Purpose

The environment preserves setup and continuity across chats while product code
and durable specification remain in their canonical product locations.

## Explanation

### Mandatory context and Activities

Mandatory files are `.hai_env/state.json` and fixed `.hai_env/agent_instructions.md`.
Load safe readable instructions before dependent work independently of state validity.
Empty content is valid; missing/unreadable instructions are a reported failure.
Instructions have no configurable location or enabled flag.

Current development uses state format 2. It requires root activities.location,
default `.hai_env/activities`, as a safe workspace-relative store. Activities are
mandatory for all substantive HAI work and have no switch. They include brainstorming,
advice, analysis, planning, framework maintenance, implementation and verification.
Only startup/bootstrap work needed to establish usable context and read-only diagnosis
may precede a record. A new chat alone creates none: after compatible validation,
leader routes current-record discovery to Activity-manager and resumes it, or creates
one when meaningful new substantive work begins with no current record. Conflicting
current/new intent requires an explicit boundary decision, never silent replacement.

At most one Activity is active at `00000000_000000_active`; previous records are
closed under UTC closure timestamp folders. Each keeps a stable activity_id.
Environment-manager validates configuration and directory availability without
loading Activity states. Activity-manager owns record discovery, artifacts and
lifecycle; leader alone orchestrates specialists. Store absence is valid before
meaningful work. There is no global current pointer or collection state file.

### Optional features and transcripts

State has two optional features, both off on initialization:

- features.specification has enabled and safe workspace-relative location, default
  `.hai_env/specifications`.
- features.chronicles has enabled only. There is no global transcript location.

Disabling preserves files. Changing Activity/specification location changes its
reference only; it does not move or delete content. Enabling specification does not
fabricate a tree; linking an existing tree requires verified intent and location.
HAI-managed work requires validated feature context, without a standalone bypass.
Registered framework roles remain available independently of optional enablement.

Chronicles live under their assigned Activity's `chronicles/`. A chat can span
Activities and an Activity can span chats or multiple segments of the same chat.
Leader assigns exact exchange boundaries and resolves ambiguity with the human;
chronicles-manager applies and verifies them, never opening/closing Activities.
Off means no new recording; enabling covers subsequent exchanges with no implicit
backfill of off periods. Explicit historical imports preserve provenance and source
limitations. Closed Activities allow attributable dated supplements and delayed
synchronization of completed old source exchanges without substantive reopening.

Synchronization is asynchronous from exact completed durable saved source by
default. Delivery does not wait for optional recording. If after-turn continuation
is unsupported, leader routes catch-up on the next active turn and reports deferred
status. Missing source/divergence is reported, never fabricated or repaired silently.
Mandatory workspace timing requirements take precedence. The synchronous pre-commit
gate verifies eligible segments or returns verified off/no-obligation status.

### Startup, configuration and compatibility

Leader runs the bounded read-only startup helper without a specialist profile.
Safely absent state permits environment-manager's minimal initialization, preserving
existing unrelated resources and readable instructions; create empty instructions
only when safely absent. Initialization creates configuration, not Activity records,
optional content, profiles or agent scaffolding. Leader then offers chat setup and
meaningful work; optional setup may be deferred.

The installed environment-manager contract defines supported state formats independently
of release numbering. Current development supports format 2 only; historical 0.1.0
bundles support format 1. Invalid/incompatible state is preserved and reported,
not reinitialized or silently migrated. Explicit format-1 migration maps configuration
under the state convention; record/transcript migration is separate scoped work
coordinated by leader and owned by Activity-manager/chronicles-manager. Marker-only
version changes do not migrate structure or history.

### Agents, profiles and integrations

Workspace definitions live under `.hai_env/agents/<name>/SKILL.md`; their catalogue
is `.hai_env/agents/catalogue.md`. Its absence means no registered workspace agents.
Read registered entries together with the framework catalogue for normal selection;
an explicit human call can select an unregistered canonical workspace definition
without registering it. Agent-definition-manager owns definitions and catalogue
mutations. Workspace mutations require compatible initialized context. Independent format tools and
read-only prerequisite diagnosis remain usable without it; substantive HAI framework
maintenance and audits follow Activity recording after bootstrap.

Optional `.hai_env/model_profiles.json` maps specialist classes to concrete model
IDs. Environment-manager owns explicit setup/repair; minimal initialization creates
none. Missing profiles do not invalidate core state. Normal spawning needs supported
exact model/effort resolution or an explicit human override; only the named startup
bootstrap may inherit settings under the model-profile convention.

Independent integrations.git.enabled and integrations.github.enabled default off;
missing settings are valid/unconfigured. They contain no credentials, repository
identity or branch choice and grant no unrelated destructive/publication authority.
Agent-executed push separately requires integrations.git.auto_push.enabled and fresh
Git-manager readiness evidence. Configuration alone does not prove live readiness.

## Supporting Terms

- [state]: mandatory format-versioned HAI configuration, including Activity location and optional settings.
- [agent_instructions]: fixed mandatory instructions, independently loaded; empty adds no instructions.
- [chronicles]: optional exact-source Activity transcript segments owned by chronicles-manager.

## References

- [Activity](../agents/activity-manager/concepts/activity.md): mandatory independent work unit and continuity.
- [State convention](../conventions/state_conv.md): configuration schema, safe paths and authorized migration.
- [Agent convention](../conventions/agent_conv.md): identities, catalogues, handoffs and registration.
- [Model profiles](../conventions/model-profiles_conv.md): local mappings, bootstrap and runtime resolution.
- [HAI](hai.md): reusable framework and product workspace boundaries.
