# State

## File format

JSON

## Location

`.hai_env/state.json` and `.hai_env/agent_instructions.md` are mandatory in every
initialized environment. Neither can be disabled or relocated through state.

### Mandatory instructions

Always validate and load `.hai_env/agent_instructions.md` before dependent work,
independently of state validity or compatibility. An existing readable UTF-8 file
with empty content means no extra instructions. Missing, unreadable, wrong-type,
dangling, or escaping targets are failures, never an implicit empty file. Read-only
diagnosis and authorized initialization/migration/repair may resolve those failures;
do not proceed with other instruction-dependent work while instructions are unavailable.
Apply the shared agent convention's instruction precedence and handoff rules.

Validate containment and existing ancestors before reading and again before writing.
The fixed file must not alias `.hai/`, `.git/`, state, profiles, or the agent registry;
optional Activity/specification paths and profiles must not overlap it, including through aliases.
Only initialization, explicitly authorized migration, or scoped repair may create a
missing file. Startup validation never silently recreates a missing initialized file.

## Content

The root MUST be a JSON object with these required properties:

| Property | Type | Meaning and initial value |
| --- | --- | --- |
| `state_format_version` | positive integer | State schema version declared by the installed environment-manager contract; currently `2`. |
| `activities` | object | Mandatory Activity store configuration with a safe workspace-relative `location`; default `.hai_env/activities`, with no enable switch. |
| `features` | object | Required optional configuration entries for `specification` and `chronicles`. |

Each optional feature is an object with a required Boolean `enabled`. Specification also has a nonempty workspace-relative `location`, retained while disabled. Chronicles has no global location; its transcript directory is `chronicles/` inside each Activity. Both optional flags default to `false`. The mandatory `activities` object has a safe workspace-relative `location`, defaults to `.hai_env/activities`, and MUST NOT contain `enabled`. Additional properties are preserved and ignored.

| Feature | Default location | Target type |
| --- | --- | --- |
| `specification` | `.hai_env/specifications` | Specification root directory |
| `chronicles` | Derived under each Activity at `chronicles/` | Activity-local session transcripts; no global location |

The installed `.hai/agents/environment-manager/contract.json` is the single authority for the current and supported `state_format_version` values. Startup reads the contract from the installed framework package, never from a target workspace copy. A state version must be an integer listed in `supported_state_format_versions`; Booleans are invalid even though JSON decodes them as Python integers. The former `compatible_version` field is incompatible and must produce a clear error; never accept it as a fallback. Legacy `agents`, root `requests`, `current_request`, `current_activity`, `features.requests`, and `features.chronicles.location` properties are incompatible. Instructions have no state flag or configurable location. Preserve unrelated additional root and feature properties when updating state; duplicate JSON property names are invalid. Unknown properties do not implicitly enable a feature.

Optional `integrations` configuration is additive within state format 2 and has no
filesystem location or credential fields:

```json
"integrations": {
  "git": { "enabled": false, "auto_push": { "enabled": false } },
  "github": { "enabled": false }
}
```

The canonical template initializes both switches to `false`. In format-2
state, an absent `integrations` object or absent supported entry is valid and means
unconfigured/disabled. A present supported entry requires an object with Boolean
`enabled`; malformed configuration makes the affected integration unavailable and
is reported separately, without invalidating otherwise valid core state or
mandatory instructions. Unknown root and integration properties are preserved and
never enable an integration. Git and GitHub are independent switches.
`integrations.git.auto_push` is a separate subordinate Boolean policy, defaulting
to `false`. When its entry is absent in an existing state it is unconfigured and
disabled. A present entry must be an object with Boolean `enabled`; malformed
values make automatic push unavailable without invalidating the Git integration or
core state. Enabling auto-push while `integrations.git.enabled` is false or
unconfigured is invalid and unavailable.

The startup helper validates this saved policy only; it does not check current
tooling, authentication, repository identity, remote write access, or branch rules.
Environment-manager may enable it only after receiving fresh Git readiness evidence
from leader/git-manager for the actual repository and remote: Git is installed,
the selected HTTPS/SSH authentication is configured for noninteractive use, remote
write access is verified, and the requested target can be pushed without force.
Do not send a smoke push or change credentials/settings to establish readiness.
Runtime pushes must recheck current prerequisites because authentication and remote
permissions can change. State stores no credentials, remote identity, or branch
choice. Neither integration enablement nor auto-push setting grants authority for
destructive repository changes or publication.

### Paths and validation

All state paths use `/` separators and are relative to the workspace root. Reject absolute, drive-qualified, UNC, blank, and parent-traversal paths, dangling links, and nonportable Windows device names or trailing-dot/space aliases. Resolve existing ancestors, symlinks, and junctions before validation and again before writing; even an absent target must remain inside the workspace after resolution. Reject workspace-root targets and paths inside `.hai/` or `.git/`. The Activity store and specification paths must not overlap `.hai_env/state.json` or `.hai_env/agents/` (including its `catalogue.md`), contain those reserved locations, or collide with another configured path. The Activity store and specification directory locations must not equal, contain, or be contained by one another; an instructions file must not equal or fall inside a configured feature directory. Validate paths even for disabled entries so saved locations remain safe when enabled. Existing target types must match the table.

An absent configured Activity store is valid configuration; creation and migration are handled by the explicitly authorized Activity workflow. An absent specification folder is valid configuration and does not assert content exists. Chronicles are stored under individual Activities only when enabled. Disabled targets need not exist and their contents are preserved without loading them as active context. A location reference alone does not authorize moving, deleting, overwriting, or inventing content. Explicitly linking an existing specification requires verifying the supplied folder. Every feature path must also avoid the fixed mandatory instructions file; removing instructions from state does not remove that reservation.

Activity configuration is mandatory and supplies a safe workspace-relative store location, defaulting to `.hai_env/activities`. Environment validation checks its path and directory type without scanning Activity folders or discovering a current Activity. Startup returns this configuration for Activity-manager, which performs current-record discovery separately. No global current Activity pointer is stored.

### Feature configuration

Environment-manager owns environment state, feature configuration, and validation
policy. Leader may run the shared read-only
[startup helper](../tools/startup/README.md) directly for existing-state validation
and context loading. This exception changes no mutation ownership; unavailable
checks remain unverified and absent state still goes to environment-manager.
Activity lifecycle operations never change this state. A configuration toggle or
location change preserves existing records and does not close, move, or delete
them. Report the old and new location when a location changes; any record handling
is a separate authorized task, not an implicit part of configuration.

Environment-manager owns feature flags and locations. Minimal initialization creates state and mandatory instructions, with no optional resources. Subsequent chat setup records explicit choices for the two optional features, retaining unmentioned values. Instructions are always loaded from their fixed file and are never offered as an on/off or location choice. The mandatory Activity store is created by the authorized Activity/history migration workflow, not startup validation. Enabling specification does not fabricate specification contents. Chronicles-manager owns transcript contents within Activity-local `chronicles/` folders after the leader routes enabled recording. Disabling a feature preserves its files and does not override mandatory instructions. Moving existing contents requires separately scoped authorization.

Chronicles synchronization is asynchronous by default under chronicles-manager's
procedures, with mandatory workspace timing instructions taking precedence. This
workflow does not introduce a feature flag, change configured locations, or require
a state version migration. Only verified source-backed transcript writes may be
reported as completed; deferred catch-up does not disable recording.

## Local model profiles

Optional `.hai_env/model_profiles.json` is separate from state and catalogue.
Its absence is valid for core state; never add it to minimal initialization or
infer profile choices from feature flags. Environment-manager owns explicitly
requested profile setup under [model-profiles_conv.md](model-profiles_conv.md).
The leader reports exact runtime availability and bootstrap/override use there.
Preserve unrelated profiles during state and catalogue updates.

## Workspace agent catalogue

`.hai_env/agents/catalogue.md` is the fixed authoritative workspace agent catalogue and registry, separate from state. Read it together with the [framework catalogue](../agents/catalogue.md) for selection, after validating state. State has no `agents` property; a present legacy `agents` property is incompatible registration data, not a fallback. Report and preserve it pending explicitly scoped migration.

A missing catalogue means no registered workspace agents and is valid, including after minimal initialization. Do not create it during startup or scan agent definitions to reconstruct it. An existing catalogue must be a readable UTF-8 Markdown file resolving inside the workspace. Reject conflicting directories and escaping symlinks/junctions. Its format matches the framework catalogue:

```markdown
# Workspace agent catalogue

| Agent | Selection guide | Definition |
| --- | --- | --- |
| `release-reviewer` | Call to review a proposed release against its readiness criteria and report unresolved release issues. | [SKILL.md](release-reviewer/SKILL.md) |
```

Use exactly one table with these three columns. A header-only table is an empty catalogue; surrounding prose is allowed and preserved. Each row registers one unique name, enclosed in backticks, a nonblank short actionable guide, and one definition link. Names and collisions follow the [agent convention](agent_conv.md). Current-format definition destinations MUST be exactly `<name>/SKILL.md`, relative to `.hai_env/agents/catalogue.md`, and resolve to readable files inside the workspace; reject absolute paths, traversal, queries, fragments, and escaped separators. Reject case-insensitive duplicate names and framework-name collisions.

Author the canonical YAML `description` first and copy its decoded string value verbatim into the guide cell. Preserve its characters when encoding table syntax: encode `&`, `\`, and `|` as `&amp;`, `&#92;`, and `&#124;` respectively, in that order; decode those entities once when comparing with the canonical description. Literal Markdown punctuation is retained as source text, not rendered away. Guides must be a single paragraph without line breaks. Existing framework table copies follow the same encoding rule when needed. Validate exact decoded equality when creating or updating a definition or entry; ordinary startup validates table structure and references without loading every definition to compare guide copies. Report discovered stale copies without rewriting them.

Legacy `<name>/knowledge.md` links must be identified as pending agent-format
migration, with their names and paths reported and rows preserved. They are not
executed or silently unregistered; other valid independent entries remain
selectable. Do not treat legacy links as current-format definitions or guess a
replacement. Coordinated authorized migration follows the agent convention.
The legacy version-2 migration described below preserves those links until that
separate or coordinated agent-format migration is authorized.

Malformed table structure, unreadable catalogue, or conflicting catalogue target blocks catalogue writes and excludes its entries. Isolated invalid rows are reported and excluded; valid independent rows remain selectable. Duplicate-name rows are all excluded. Preserve invalid material without repair, and keep framework agents available. Catalogue problems do not invalidate otherwise valid core state or prevent independent feature loading.

Agent-definition-manager owns explicitly requested registration and synchronization
of existing entries after definition updates. Creation alone does not register an
agent; updating an unregistered definition leaves it unregistered. Workspace
mutations require valid initialized environment context. Environment-manager owns
general state, model profiles, and lightweight startup catalogue validation, without
repairing definitions or registrations. Preserve unrelated rows, prose, and state
settings during updates. Explicitly calling an allowed unregistered workspace agent
does not register it. Framework roles require their framework catalogue entry for
selection but need neither workspace registration nor enabled optional features.

## Initialization template and compatibility

The [state contract](../agents/environment-manager/contract.json) is the authoritative machine-readable source for current and supported state versions. The canonical [state template](../agents/environment-manager/templates/state.json) supplies only initialization defaults. Validate both before initialization; do not ask the human to supply versions or infer them from a framework release.

Leader startup delegates minimal initialization when `.hai_env/state.json` is
absent and its location can be created safely. `.hai_env/` may already be a directory
containing independently managed resources; its existence alone does not establish
initialized core state. Preserve those resources without reading their contents to
decide whether initialization is allowed. Validate the container, state path, and
resolved containment; reject a conflicting file, escaping symlink/junction, dangling
state link, or unreadable path. Recheck absence and use exclusive file creation.
Validate and preserve an existing readable mandatory instructions file, loading its
content before dependent work. If it is safely absent, create the empty fixed file
exclusively. Prepare a state candidate in memory from the template defaults plus
`state_format_version` set to the contract's `current_state_format_version`; the
template itself remains unchanged and supplies no version. Validate the complete
candidate under this convention before any state-file write. Create the parent
directory only if absent. Recheck safe paths, state absence, inspected contract
and template contents, and candidate validity immediately before exclusive state
creation; stop on changed inputs and never replace an existing file or conflicting
target. Read back and verify the current supported version, all template defaults,
and disabled optional feature defaults with their default locations, then run the startup
helper. Create no catalogue or optional resources. Verify both mandatory resources
and that existing unrelated contents remain unchanged, rather
than requiring an empty container. No feature-location questions or additional
authorization precede this minimal startup action. The leader then recommends chat
setup; the human may defer it or keep all features off.

An existing malformed, unreadable, conflicting, or unsupported state is not absent;
preserve and report it without reinitialization or implicit repair. A known partial
initialization remains a reported failure, not permission for an automatic retry.
The prototype `compatible_version` field is rejected clearly and is never treated as
a `state_format_version`.

### Explicit format-1 to format-2 migration

Format-1 state is incompatible with the format-2 startup helper. Migrate only under
explicit leader authorization after inspecting the complete state and relevant
filesystem paths. Validate duplicate-free JSON, source shape, containment, directory
types, and the installed format-2 contract/template. Preserve integrations (including
nested settings), specification configuration, and every unknown property that
remains meaningful. Do not silently discard unrecognized properties; report
properties that cannot be carried forward and resolve them within the authorized
migration scope.

Construct format-2 state by changing `state_format_version` to `2`, adding the
mandatory `activities.location` using the selected safe store location (default to
`.hai_env/activities` when no existing store is selected), and removing
`features.requests` and the old global `features.chronicles.location`. Preserve the
chronicles `enabled` value. Record the old request-store and chronicles locations,
including any existing directory contents needed to map former request records to
Activities and transcripts to Activity-local `chronicles/` paths. This records
migration provenance; it does not itself move, delete, rewrite, classify, or
interpret records or transcripts. Do not create or migrate Activity records as
part of state conversion.

Validate that Activity and specification roots are safely contained, correctly
typed when present, and do not overlap reserved paths or each other. Record and
resolve any path mapping or collision before writing. Recheck the source state and
paths immediately before a guarded write, preserve a recoverable copy of the
inspected source under the authorized procedure, then read back and run the
startup helper. Verify preserved integrations, specification settings, chronicle
enablement, unrelated properties, and all new format-2 invariants. On conflict or
verification failure, preserve partial results and report them; do not retry or
claim migration success. Future format changes update the contract and convention
together; editing the template alone never changes the accepted format.
