# State

## File format

JSON

## Location

`.hai_env/state.json` is mandatory in every initialized environment and cannot be disabled or relocated through optional-feature settings.

## Content

The root MUST be a JSON object with these required properties:

| Property | Type | Meaning and initial value |
| --- | --- | --- |
| `compatible_version` | positive integer | Environment format version from the canonical template; currently `4`. |
| `features` | object | Required configuration entries for `requests`, `specification`, `agent_instructions`, and `chronicles`. |

Each required feature is an object with required `enabled` (Boolean) and `location` (nonempty workspace-relative string) properties. Disabled features retain their location for later setup. All four flags are initially `false`:

| Feature | Default location | Target type |
| --- | --- | --- |
| `requests` | `.hai_env/requests` | Directory containing request folders |
| `specification` | `.hai_env/specifications` | Specification root directory |
| `agent_instructions` | `.hai_env/agent_instructions.md` | Custom workspace instructions file |
| `chronicles` | `.hai_env/chronicles` | Directory containing session transcripts |

`specification_location` is the former version-1 field; versions 2 onward use `features.specification.location`. Do not use a legacy field as a fallback. Version 4 has no `current_request` property; its presence is incompatible legacy data, not an optional pointer or a fallback. Preserve unrelated additional root and feature properties when updating state; duplicate JSON property names are invalid. Unknown properties do not implicitly enable a feature.

### Paths and validation

All state paths use `/` separators and are relative to the workspace root. Reject absolute, drive-qualified, UNC, blank, and parent-traversal paths. Resolve existing ancestors, symlinks, and junctions before validation and again before writing; even an absent target must remain inside the workspace after resolution. Reject workspace-root targets and paths inside `.hai/` or `.git/`. A feature path must not overlap `.hai_env/state.json` or `.hai_env/agents/` (including its `catalogue.md`), contain those reserved locations, or collide with another feature path. Directory feature locations must not equal, contain, or be contained by another feature location; an instructions file must not equal or fall inside a configured feature directory. Validate paths even for disabled entries so saved locations remain safe when enabled. Existing target types must match the table.

An enabled feature whose target is missing needs feature-specific handling: agent instructions require their readable file before reporting setup complete; absent configured requests or specification folders are valid configuration and do not assert records exist. Explicit requests enablement may create its empty directory; otherwise creation waits for an authorized operation. Chronicles-manager may create its directory on the first authorized transcript write. Disabled targets need not exist and their contents are preserved without loading them as active context. A location reference alone does not authorize moving, deleting, overwriting, or inventing content. Explicitly linking an existing specification requires verifying the supplied folder.

Requests configuration supplies only `enabled` and `location`. Environment validation
checks the configured path and target type without scanning request folders, loading
request records, or interpreting lifecycle stages. Startup does not resume request
work. When request work is asked for, the caller supplies validated enabled-feature
and location context to the selected role; lifecycle knowledge belongs to that role's
package. There is no global active selection to load or clear.

### Feature configuration

Environment-manager owns environment state, feature configuration, and validation.
Request lifecycle operations never change this state. A configuration toggle or
location change preserves existing records and does not close, move, or delete
them. Report the old and new location when a location changes; any record handling
is a separate authorized task, not an implicit part of configuration.

Environment-manager owns feature flags and locations. State-only initialization creates no optional resources. Subsequent chat setup records explicit human choices, retaining unmentioned values. Enabling requests may create its empty directory; enabling instructions may create its empty file, with supplied instructions only when explicitly provided. Enabling specification does not fabricate specification contents. Chronicles-manager owns transcript contents after the leader routes enabled recording. Disabling a feature stops using that feature through environment configuration and preserves all files; it does not override independent higher-priority workspace or session instructions. Moving existing contents requires separately scoped authorization. State remains present with all optional features disabled.

## Local model profiles

Optional `.hai_env/model_profiles.json` is separate from state and catalogue.
Its absence is valid for core state; never add it to state-only initialization or
infer profile choices from feature flags. Environment-manager owns explicitly
requested profile setup under [model-profiles_conv.md](model-profiles_conv.md).
The leader reports exact runtime availability and bootstrap/override use there.
Preserve unrelated profiles during state and catalogue updates.

## Workspace agent catalogue

`.hai_env/agents/catalogue.md` is the fixed authoritative workspace agent catalogue and registry, separate from state. Read it together with the [framework catalogue](../agents/catalogue.md) for selection, after validating state. State has no `agents` property from version 3 onward; a present legacy `agents` property is incompatible registration data, not a fallback. Report and preserve it pending explicitly scoped migration.

A missing catalogue means no registered workspace agents and is valid, including after state-only initialization. Do not create it during startup or scan agent definitions to reconstruct it. An existing catalogue must be a readable UTF-8 Markdown file resolving inside the workspace. Reject conflicting directories and escaping symlinks/junctions. Its format matches the framework catalogue:

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

Leader startup delegates state-only initialization when `.hai_env/state.json` is
absent and its location can be created safely. `.hai_env/` may already be a directory
containing independently managed resources; its existence alone does not establish
initialized core state. Preserve those resources without reading their contents to
decide whether initialization is allowed. Validate the container, state path, and
resolved containment; reject a conflicting file, escaping symlink/junction, dangling
state link, or unreadable path. Recheck absence and use exclusive file creation.
Create only the state file from the template, with four disabled features, and its
parent directory if absent. Do not create or replace a catalogue or other resources.
Verify the new state and that existing unrelated contents remain unchanged, rather
than requiring an empty container. No feature-location questions or additional
authorization precede this minimal startup action. The leader then recommends chat
setup; the human may defer it or keep all features off.

An existing malformed, unreadable, conflicting, or incompatible state is not absent;
preserve and report it without reinitialization or implicit repair. A known partial
initialization remains a reported failure, not permission for an automatic retry.
Versions 1, 2, and 3 are incompatible with version 4. Do not silently migrate,
reinterpret legacy defaults as opted-in features, or create optional resources.
Future incompatible format changes update this convention and the template version
together. Migration requires explicit authority and verified preservation of data.

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

### Earlier migration history

The version-2 to version-3 migration validates legacy registrations, writes their names, verbatim guides, and relative definition links into `.hai_env/agents/catalogue.md`, then removes only `agents` from state and sets `compatible_version` to `3`. Verify the catalogue before replacing state, preserve feature settings, the legacy current-request field, and unrelated properties, and stop on changed inputs or an existing conflicting catalogue. Do not invent missing guides or silently drop invalid entries or extra registration metadata; resolve such cases within the migration scope. These writes are not one transaction: preserve partial results and report any inconsistency rather than retrying automatically. Version 3 is an intermediate legacy format, not the current success target; reaching version 4 additionally requires the authorized migration above. Authorization for a historical migration alone does not authorize extra stages.
