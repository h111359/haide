# State

## File format

JSON

## Location

`.hai_env/state.json` is mandatory in every initialized environment and cannot be disabled or relocated through optional-feature settings.

## Content

The root MUST be a JSON object with these required properties:

| Property | Type | Meaning and initial value |
| --- | --- | --- |
| `compatible_version` | positive integer | Environment format version from the canonical template; currently `3`. |
| `current_request` | string or null | Workspace-relative path to the active request under the configured requests location; initially `null`. |
| `features` | object | Required configuration entries for `requests`, `specification`, `agent_instructions`, and `chronicles`. |

Each required feature is an object with required `enabled` (Boolean) and `location` (nonempty workspace-relative string) properties. Disabled features retain their location for later setup. All four flags are initially `false`:

| Feature | Default location | Target type |
| --- | --- | --- |
| `requests` | `.hai_env/requests` | Directory containing request folders |
| `specification` | `.hai_env/specifications` | Specification root directory |
| `agent_instructions` | `.hai_env/agent_instructions.md` | Custom workspace instructions file |
| `chronicles` | `.hai_env/chronicles` | Directory containing session transcripts |

`specification_location` is the former version-1 field; versions 2 and 3 use `features.specification.location`. Do not use a legacy field as a fallback. Preserve unrelated additional root and feature properties when updating state; duplicate JSON property names are invalid. Unknown properties do not implicitly enable a feature.

### Paths and validation

All state paths use `/` separators and are relative to the workspace root. Reject absolute, drive-qualified, UNC, blank, and parent-traversal paths. Resolve existing ancestors, symlinks, and junctions before validation and again before writing; even an absent target must remain inside the workspace after resolution. Reject workspace-root targets and paths inside `.hai/` or `.git/`. A feature path must not overlap `.hai_env/state.json` or `.hai_env/agents/` (including its `catalogue.md`), contain those reserved locations, or collide with another feature path. Directory feature locations must not equal, contain, or be contained by another feature location; an instructions file must not equal or fall inside a configured feature directory. Validate paths even for disabled entries so saved locations remain safe when enabled. Existing target types must match the table.

An enabled feature whose target is missing needs feature-specific handling: requests and agent instructions require their directory or readable file before reporting setup complete; an absent configured specification folder is valid and does not assert a specification exists. Chronicles-manager may create its directory on the first authorized transcript write. Disabled targets need not exist and their contents are preserved without loading them as active context. A location reference alone does not authorize moving, deleting, overwriting, or inventing content. Explicitly linking an existing specification requires verifying the supplied folder.

A non-null `current_request` requires enabled requests and MUST resolve to the existing `<features.requests.location>/00000000_000000_active` directory. Its request state must be nonclosed under the [request convention](request_conv.md). Disabled requests require `current_request: null`. Close or explicitly resolve an active request before disabling or relocating requests; a configuration toggle never silently clears or moves it. On closure clear `current_request` to null with the coordinated rename and reference updates defined there. Report naming or status inconsistencies without automatic repair.

### Feature configuration

Request-manager owns setting `current_request` during request initialization and
clearing it during closure, under the request convention. This narrow lifecycle
ownership does not authorize feature configuration or unrelated state changes.
Environment-manager retains general environment state and validation ownership.

Environment-manager owns feature flags and locations. State-only initialization creates no optional resources. Subsequent chat setup records explicit human choices, retaining unmentioned values. Enabling requests may create its empty directory; enabling instructions may create its empty file, with supplied instructions only when explicitly provided. Enabling specification does not fabricate specification contents. Chronicles-manager owns transcript contents after the leader routes enabled recording. Disabling a feature stops using that feature through environment configuration and preserves all files; it does not override independent higher-priority workspace or session instructions. Moving existing contents requires separately scoped authorization. State remains present with all optional features disabled.

## Local model profiles

Optional `.hai_env/model_profiles.json` is separate from state and catalogue.
Its absence is valid for core state; never add it to state-only initialization or
infer profile choices from feature flags. Environment-manager owns explicitly
requested profile setup under [model-profiles_conv.md](model-profiles_conv.md).
The leader reports exact runtime availability and bootstrap/override use there.
Preserve unrelated profiles during state and catalogue updates.

## Workspace agent catalogue

`.hai_env/agents/catalogue.md` is the fixed authoritative workspace agent catalogue and registry, separate from state. Read it together with the [framework catalogue](../agents/catalogue.md) for selection, after validating state. State has no `agents` property in version 3; a present legacy `agents` property is incompatible registration data, not a fallback. Report and preserve it pending explicitly scoped migration.

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

Workspace-agent-creator owns creation-time registrations after definition validation; environment-manager validates the catalogue while owning general state. Preserve unrelated rows, prose, and state settings during updates. Explicitly calling an unregistered agent does not register it. Framework agents need neither workspace registrations nor enabled optional features.

## Initialization template and compatibility

The canonical [state template](../agents/environment-manager/templates/state.json) supplies the supported environment format version and initialization defaults. Read its version; do not ask the human to supply it or infer it from a framework release.

Leader startup delegates initialization when `.hai_env/` is absent. Environment-manager creates only `.hai_env/state.json` from the template, with no selected request and four disabled features; no catalogue is created. No feature-location questions or additional authorization precede this minimal startup action. The leader then recommends additional chat setup and offers available next actions. The human may defer setup or keep all features off.

Existing but incomplete environment is not absent. Missing, malformed, or unreadable state and conflicting `.hai_env` paths require reporting and scoped repair rather than reinitialization. Versions 1 and 2 are incompatible with version 3: report the compatibility issue and preserve live state. Do not silently migrate, reinterpret legacy defaults as opted-in features, or create optional resources. An explicitly authorized migration must settle feature choices, locations, and active-request handling before writing. Future incompatible format changes update this convention and increment the template version together.

An explicitly authorized version-2 migration validates legacy registrations, writes their names, verbatim guides, and relative definition links into `.hai_env/agents/catalogue.md`, then removes only `agents` from state and sets `compatible_version` to `3`. Verify the catalogue before replacing state, preserve feature settings, current request, and unrelated properties, and stop on changed inputs or an existing conflicting catalogue. Do not invent missing guides or silently drop invalid entries or extra registration metadata; resolve such cases within the migration scope. These writes are not one transaction: preserve partial results and report any inconsistency rather than retrying automatically.
