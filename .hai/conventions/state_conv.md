# State

## File format and mandatory resources

Strict UTF-8 JSON. `.hai_env/state.json` and `.hai_env/agent_instructions.md` are
mandatory in every initialized environment and cannot be disabled or relocated.
Load safe mandatory instructions before dependent work, independently of state
validity. Existing readable empty content adds no instructions. Missing, unreadable,
wrong-type, dangling or escaping instructions are failures; initialization or an
explicitly scoped repair/migration may resolve them, never silent startup repair.
Validate existing ancestors/containment before reading and again before writing.
Instructions cannot alias framework, Git, state, profiles, registries, configuration
or configured content directories. Apply shared instruction precedence/handoff rules.

## Current content: format 3

The root is an object with required properties:

| Property | Type | Meaning and initial value |
| --- | --- | --- |
| `state_format_version` | positive integer | Current installed Environment-manager contract version `3`; Booleans are invalid. |
| `activities` | object | Mandatory safe workspace-relative `location`, default `.hai_env/activities`; no `enabled` switch. |
| `features` | object | Required `chronicles` object; specification is no longer a core feature entry. |

`features.chronicles.enabled` is a required Boolean, default false.
`record_every_prompts` is an optional positive JSON integer, default 5; Booleans,
zero, negative/fractional/string/null values are invalid even while disabled.
Transcripts remain Activity-local under `chronicles/`; no global location exists.
Core state stores no current Activity pointer, prompt counter, transcript coverage
or in-flight-worker marker. Environment-manager owns record discovery policy and lifecycle; the shared startup context helper may perform read-only discovery for Leader. Optional installed Codex Chronicle-manager owns transcript/checkpoint formats and writes. Configuration changes never alter record lifecycle/content.

The installed `.hai/agents/environment-manager/contract.json` is the single
current/supported-version authority, independent of release SemVer or target copies.
Current is 3, supported versions are 2 and 3. Format 2 remains read-only migration
context with `migration_required`; it supplies no active specification fallback.
Ordinary core/path configuration targets format 3. Retired `compatible_version`,
legacy agents/requests/current pointers, request features and global chronicles
locations remain incompatible. Format-3 `features.specification` is a mixed-authority
error, not opaque configuration. Unknown unrelated root/feature values are preserved
and ignored; duplicate JSON keys/nonstandard constants anywhere are invalid.

### Agent configuration and preservation

Specification-manager owns enabled/location in
`.hai_env/config/agents/specification-manager.json`; Git-manager owns its settings
in its corresponding file. Neither is read from state as runtime settings.
Their installed configuration contracts define defaults/types/versions. Optional
owner absence or invalid configuration does not invalidate core startup. Startup
can boundedly report the registered installed Specification-manager's separate
`agent_configurations` result without loading scripts, product contents or the library.

Environment-manager owns central state, chronicles configuration, model profiles and startup
policy. It does not perform ordinary specification setup. The explicit format-2-to-3
extraction is its narrow transition exception, coordinated by Leader; it does not
grant tree-edit authority. Other extensions' unknown subtrees remain opaque:
core neither interprets/enables them nor repairs invalid domain data. Authorized
writers preserve unknown root/nested/sibling values and operate only on owned fields.
New agent settings use [agent-configuration_conv.md](agent-configuration_conv.md),
not new state subtrees. Initialization supplies only core defaults.

### Paths and dependent assurance

All configured paths use `/` separators and are relative to the workspace. Reject
absolute/drive/UNC/blank/traversal paths, dangling or escaping links, nonportable
Windows names and trailing-dot/space aliases. Resolve existing ancestors before
reads and immediately before writes. Reject workspace root, `.hai/`, `.git/`, state,
instructions, profiles, agent registries/packages and `.hai_env/config/` collisions.
Validate existing target directory types; missing directories are valid and do not
authorize creation. An Activity-store reference never moves/deletes records.

The owner's specification location follows the same safe-directory rules even
when disabled and cannot overlap the Activity store or another reserved/configured
location. Before a dependent Activity-location or profile mutation, obtain fresh
separate specification configuration/location assurance from the bounded reader.
Invalid/unverified owner settings stop affected path changes rather than supply a
guessed root. An unavailable optional owner remains an isolated dependency; setup
must resolve any potentially conflicting dormant configured root before a path
change. Core read-only startup and unrelated work remain independent.

### Chronicles configuration

Environment-manager applies explicit chosen Activity-location/chronicles changes,
preserving unmentioned values and all optional owner files. Initialization creates
state and mandatory instructions only; no catalogue, profiles, Activity records,
specification/config file or transcript contents are fabricated. Environment-manager creates the Activity store under its authorized record workflow. Optional installed Codex Chronicle-manager owns exact-source transcripts/checkpoints after Leader assigns recording; missing owner or source is an isolated recording dependency.

Enabling/disabling chronicles preserves existing content and does not override
mandatory instructions. Return attributable enablement-change boundaries separately;
threshold changes do not reset coverage or dispatch progress. Leader owns counting,
batch dispatch and continuation limits; Chronicle verifies source coverage and Environment-manager consumes Leader-returned fresh operation-bound evidence before required-recording closure. Core startup and independent record operations need no Chronicle tree; disabled/no-obligation closure needs no transcript source.

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

Environment-manager owns explicitly requested registration and synchronization of
existing rows after authorized definition/package updates in both runtime catalogues.
Agent-definition-manager owns authoring/verification and returns exact decoded
metadata through Leader; it never copies packages into installation or mutates
catalogues. Creation alone does not register an agent. Environment-manager can
install and validate the first selected optional package using shared core tools,
without the optional authoring agent or a whole library. Workspace mutations retain
compatible initialized context, instructions and Activity prerequisites. Preserve
unrelated rows/prose/settings; selection/execution still requires valid registration
for either origin and remains Leader's responsibility.

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
and disabled chronicles/default threshold, then run the startup
helper. Create no catalogue or optional resources. Verify both mandatory resources
and that existing unrelated contents remain unchanged, rather
than requiring an empty container. No optional-setting questions or additional
authorization precede this minimal startup action. The leader then recommends chat
setup; the human may defer it or keep all features off.

An existing malformed, unreadable, conflicting, or unsupported state is not absent;
preserve and report it without reinitialization or implicit repair. A known partial
initialization remains a reported failure, not permission for an automatic retry.
The prototype `compatible_version` field is rejected clearly and is never treated as
a `state_format_version`.

### Historical format-1 to format-2 mapping

This historical intermediate mapping is not the current runtime target. Current
format-3 upgrades need an explicit ordered mapping through the specification
extraction below; do not mark an intermediate state fully upgraded. Format-1 state
is incompatible with current startup. Migrate only under
explicit leader authorization after inspecting the complete state and relevant
filesystem paths. Validate duplicate-free JSON, source shape, containment, directory
types, and the installed format-2 contract/template. Preserve extension-owned data (including
nested values), specification configuration, and every unknown property that
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
startup helper. Verify preserved extension data, specification settings, chronicle
enablement, unrelated properties, and all new format-2 invariants. On conflict or
verification failure, preserve partial results and report them; do not retry or
claim migration success. Future format changes update the contract and convention
together; editing the template alone never changes the accepted format.

### Explicit format-2 to format-3 specification extraction

Environment-manager's installed
[extraction helper](../tools/startup/migrate_specification_configuration.py) provides
read-only dry-run and explicitly authorized guarded apply. Validate complete strict
source state, safe paths and the registered installed Specification-manager contract;
never load a source-library fallback or invoke that optional role merely to parse data.
An absent optional owner does not block fresh format-3 core initialization/startup,
but missing migration dependencies must be resolved before this conversion.

Preserve recoverable source/destination bytes. Extract the complete prior
`features.specification` object into config-format-1 `settings` under the owner file,
including unknown nested values. Preserve enabled/location exactly, including false
and missing directories; validate the directory even while disabled. Verify the
new envelope and source stability before removing only `features.specification`
and setting core version 3. Preserve chronicles, Activity location, unknown siblings,
instructions, profiles, registries and content. Existing different destination values
are conflicts, never silent merges or precedence. Retain/describe partial writes,
stop on changed inputs, and do not retry/rollback automatically. Re-run core and
owner checks before claiming completion. This is not a multi-file transaction,
a new enablement choice, a content move or a specification-tree migration.
