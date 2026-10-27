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
optional feature paths and profiles must not overlap it, including through aliases.
Only initialization, explicitly authorized migration, or scoped repair may create a
missing file. Startup validation never silently recreates a missing initialized file.

## Content

The root MUST be a JSON object with these required properties:

| Property | Type | Meaning and initial value |
| --- | --- | --- |
| `compatible_version` | positive integer | Environment format version from the canonical template; currently `5`. |
| `features` | object | Required configuration entries for `requests`, `specification`, and `chronicles`. |

Each required feature is an object with required `enabled` (Boolean) and `location` (nonempty workspace-relative string) properties. Disabled features retain their location for later setup. All three flags are initially `false`:

| Feature | Default location | Target type |
| --- | --- | --- |
| `requests` | `.hai_env/requests` | Directory containing request folders |
| `specification` | `.hai_env/specifications` | Specification root directory |
| `chronicles` | `.hai_env/chronicles` | Directory containing session transcripts |

`specification_location` is the former version-1 field; versions 2 onward use `features.specification.location`. Do not use a legacy field as a fallback. Version 5 rejects legacy `agents` and `current_request` root properties and the retired `features.agent_instructions` entry. Instructions have no state flag or configurable location. Preserve unrelated additional root and feature properties when updating state; duplicate JSON property names are invalid. Unknown properties do not implicitly enable a feature.

Optional `integrations` configuration is additive within version 5 and has no
filesystem location or credential fields:

```json
"integrations": {
  "git": { "enabled": false },
  "github": { "enabled": false }
}
```

The canonical template initializes both switches to `false`. In existing version-5
state, an absent `integrations` object or absent supported entry is valid and means
unconfigured/disabled. A present supported entry requires an object with Boolean
`enabled`; malformed configuration makes the affected integration unavailable and
is reported separately, without invalidating otherwise valid core state or
mandatory instructions. Unknown root and integration properties are preserved and
never enable an integration. Git and GitHub are independent switches. State stores
no credentials, remote identity, or branch choice. Integration enablement does not
grant authority for destructive repository changes or publication.

### Paths and validation

All state paths use `/` separators and are relative to the workspace root. Reject absolute, drive-qualified, UNC, blank, and parent-traversal paths, dangling links, and nonportable Windows device names or trailing-dot/space aliases. Resolve existing ancestors, symlinks, and junctions before validation and again before writing; even an absent target must remain inside the workspace after resolution. Reject workspace-root targets and paths inside `.hai/` or `.git/`. A feature path must not overlap `.hai_env/state.json` or `.hai_env/agents/` (including its `catalogue.md`), contain those reserved locations, or collide with another feature path. Directory feature locations must not equal, contain, or be contained by another feature location; an instructions file must not equal or fall inside a configured feature directory. Validate paths even for disabled entries so saved locations remain safe when enabled. Existing target types must match the table.

An enabled feature whose target is missing needs feature-specific handling: absent configured requests or specification folders are valid configuration and do not assert records exist. Explicit requests enablement may create its empty directory; otherwise creation waits for an authorized operation. Chronicles-manager may create its directory on the first authorized transcript write. Disabled targets need not exist and their contents are preserved without loading them as active context. A location reference alone does not authorize moving, deleting, overwriting, or inventing content. Explicitly linking an existing specification requires verifying the supplied folder. Every feature path must also avoid the fixed mandatory instructions file; removing instructions from state does not remove that reservation.

Requests configuration supplies only `enabled` and `location`. Environment validation
checks the configured path and target type without scanning request folders, loading
request records, or interpreting lifecycle stages. Startup does not resume request
work. When request work is asked for, the caller supplies validated enabled-feature
and location context to the selected role; lifecycle knowledge belongs to that role's
package. There is no global active selection to load or clear.

### Feature configuration

Environment-manager owns environment state, feature configuration, and validation
policy. Leader may run the shared read-only
[startup helper](../tools/startup/README.md) directly for existing-state validation
and context loading. This exception changes no mutation ownership; unavailable
checks remain unverified and absent state still goes to environment-manager.
Request lifecycle operations never change this state. A configuration toggle or
location change preserves existing records and does not close, move, or delete
them. Report the old and new location when a location changes; any record handling
is a separate authorized task, not an implicit part of configuration.

Environment-manager owns feature flags and locations. Minimal initialization creates state and mandatory instructions, with no optional resources. Subsequent chat setup records explicit choices for the three optional features, retaining unmentioned values. Instructions are always loaded from their fixed file and are never offered as an on/off or location choice. Enabling requests may create its empty directory. Enabling specification does not fabricate specification contents. Chronicles-manager owns transcript contents after the leader routes enabled recording. Disabling a feature preserves its files and does not override mandatory instructions. Moving existing contents requires separately scoped authorization.

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

`.hai_env/agents/catalogue.md` is the fixed authoritative workspace agent catalogue and registry, separate from state. Read it together with the [framework catalogue](../agents/catalogue.md) for selection, after validating state. State has no `agents` property from version 3 onward; a present legacy `agents` property is incompatible registration data, not a fallback. Report and preserve it pending explicitly scoped migration.

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

The canonical [state template](../agents/environment-manager/templates/state.json) supplies the supported environment format version and initialization defaults. Read its version; do not ask the human to supply it or infer it from a framework release.

Leader startup delegates minimal initialization when `.hai_env/state.json` is
absent and its location can be created safely. `.hai_env/` may already be a directory
containing independently managed resources; its existence alone does not establish
initialized core state. Preserve those resources without reading their contents to
decide whether initialization is allowed. Validate the container, state path, and
resolved containment; reject a conflicting file, escaping symlink/junction, dangling
state link, or unreadable path. Recheck absence and use exclusive file creation.
Validate and preserve an existing readable mandatory instructions file, loading its
content before dependent work. If it is safely absent, create the empty fixed file
exclusively, then create state from the template with three disabled features using
exclusive creation. Create the parent directory only if absent. Recheck paths and
absence immediately before writes; never replace an existing file or conflicting
target. Create no catalogue or optional resources. Verify both mandatory resources
and that existing unrelated contents remain unchanged, rather
than requiring an empty container. No feature-location questions or additional
authorization precede this minimal startup action. The leader then recommends chat
setup; the human may defer it or keep all features off.

An existing malformed, unreadable, conflicting, or incompatible state is not absent;
preserve and report it without reinitialization or implicit repair. A known partial
initialization remains a reported failure, not permission for an automatic retry.
Versions 1, 2, 3, and 4 are incompatible with version 5. Do not silently migrate,
reinterpret legacy defaults as opted-in features, or create optional resources.
Future incompatible format changes update this convention and the template version
together. Migration requires explicit authority and verified preservation of data.

### Authorized version-4 to version-5 migration

1. Require explicit migration authority. Validate duplicate-free version-4 state
   against its four-feature schema, required types, safe paths, and existing target
   types, not against the version-5 template. Load an existing safe canonical
   instructions file independently of the old flag. Preserve all three retained
   features, their unknown properties, unrelated root/feature properties, profiles,
   catalogues, records, and transcripts. Malformed source or unsafe/conflicting
   paths require resolution before writes.
2. Resolve legacy instruction content without deleting or changing its source.
   Preserve an existing canonical file. If the old instructions were enabled at a
   custom location, verify that source is readable. A missing canonical file may be
   created exclusively with an exact byte copy of that active source. If canonical
   and active custom contents differ, obtain an explicit content resolution; never
   overwrite or merge either file automatically. A disabled custom file is preserved
   as inactive legacy material, not silently copied into the new instructions.
   Where there is no active custom source and the canonical file is safely absent,
   create it empty exclusively. An existing canonical file becomes active regardless
   of its old flag; instructions have no opt-out after this migration.
3. Prepare version-5 state by removing only `features.agent_instructions` and
   setting `compatible_version` to `5`. Validate the three retained features,
   profiles, and canonical instructions against all new reservations, including
   resolved aliases. Recheck state bytes, any source/canonical instruction bytes,
   containment, target types, and absence immediately before writes. Stop if changed.
4. Ensure the canonical instructions file is verified before replacing only the
   unchanged inspected state. Read back both resources and run the startup helper;
   verify version 5, absent retired entry, readable instructions with the intended
   exact content, preserved settings/files, and reported independent issues. The
   file and state changes are not a transaction: preserve and report partial results
   without automatic deletion, rollback, overwrite, or retry. Missing instructions
   in an already initialized version-5 environment require scoped repair, not this
   migration or startup initialization.

### Authorized version-3 to version-4 migration

1. Validate duplicate-free version-3 state, all feature values, safe configured paths,
   and the legacy `current_request` value without changing records. Preserve every
   feature setting, including a custom requests location, and all unrelated properties.
2. This migration is an exception to ordinary configuration-only validation: obtain
   read-only validation of the configured store under the package's
   [request convention](../agents/request-manager/conventions/request_conv.md).
   Inspect direct request-folder states, not their unrelated historical contents.
   A null pointer does not establish that the store is empty. If the store is absent,
   require a null pointer; do not create it. If a non-null pointer exists, requests
   must be enabled and it must identify the store's sole valid nonclosed fixed active
   folder. A null pointer with active records, another nonclosed folder, invalid
   record, or partial closure requires separately resolved migration handling; do
   not silently drop an inconsistent pointer or repair, rename, or close records.
3. Prepare state by removing only `current_request` and changing
   `compatible_version` to `4`. Recheck state bytes, affected path facts, and any
   inspected records immediately before writing. Stop if they changed. Preserve
   files, custom store locations, other feature values, and unknown properties.
4. Read back and verify version 4, absent pointer, exact preservation of all other
   state values, and unchanged request records and unrelated resources. Report the
   retained store location and that future request work is on demand; create no
   collection state or replacement pointer. Preserve and report partial failures
   without silent retries or rollback over concurrent changes.

Version 4 is an intermediate format. Reaching current version 5 additionally
requires the explicitly authorized version-4 to version-5 migration above.

### Earlier migration history

The version-2 to version-3 migration validates legacy registrations, writes their names, verbatim guides, and relative definition links into `.hai_env/agents/catalogue.md`, then removes only `agents` from state and sets `compatible_version` to `3`. Verify the catalogue before replacing state, preserve feature settings, the legacy current-request field, and unrelated properties, and stop on changed inputs or an existing conflicting catalogue. Do not invent missing guides or silently drop invalid entries or extra registration metadata; resolve such cases within the migration scope. These writes are not one transaction: preserve partial results and report any inconsistency rather than retrying automatically. Versions 3 and 4 are intermediate legacy formats, not the current success target; reaching version 5 requires both later authorized stages above. Authorization for a historical migration alone does not authorize extra stages.
