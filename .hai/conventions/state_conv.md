# State

## File format

JSON

## Location

`.hai_env/state.json` is mandatory in every initialized environment and cannot be disabled or relocated through optional-feature settings.

## Content

The root MUST be a JSON object with these required properties:

| Property | Type | Meaning and initial value |
| --- | --- | --- |
| `compatible_version` | positive integer | Environment format version from the canonical template; currently `2`. |
| `current_request` | string or null | Workspace-relative path to the active request under the configured requests location; initially `null`. |
| `agents` | object | Workspace agent catalogue; initially `{}`. |
| `features` | object | Required configuration entries for `requests`, `specification`, `agent_instructions`, and `chronicles`. |

Each required feature is an object with required `enabled` (Boolean) and `location` (nonempty workspace-relative string) properties. Disabled features retain their location for later setup. All four flags are initially `false`:

| Feature | Default location | Target type |
| --- | --- | --- |
| `requests` | `.hai_env/requests` | Directory containing request folders |
| `specification` | `.hai_env/specifications` | Specification root directory |
| `agent_instructions` | `.hai_env/agent_instructions.md` | Custom workspace instructions file |
| `chronicles` | `.hai_env/chronicles` | Directory containing session transcripts |

`specification_location` is the former version-1 field; version 2 uses `features.specification.location`. Do not use a legacy field as a fallback. Preserve unrelated additional root, feature, and catalogue properties when updating state; duplicate JSON property names are invalid. Unknown properties do not implicitly enable a feature.

### Paths and validation

All state paths use `/` separators and are relative to the workspace root. Reject absolute, drive-qualified, UNC, blank, and parent-traversal paths. Resolve existing ancestors, symlinks, and junctions before validation and again before writing; even an absent target must remain inside the workspace after resolution. Reject workspace-root targets and paths inside `.hai/` or `.git/`. A feature path must not overlap `.hai_env/state.json` or `.hai_env/agents/`, contain those reserved locations, or collide with another feature path. Directory feature locations must not equal, contain, or be contained by another feature location; an instructions file must not equal or fall inside a configured feature directory. Validate paths even for disabled entries so saved locations remain safe when enabled. Existing target types must match the table.

An enabled feature whose target is missing needs feature-specific handling: requests and agent instructions require their directory or readable file before reporting setup complete; an absent configured specification folder is valid and does not assert a specification exists. Chronicles-manager may create its directory on the first authorized transcript write. Disabled targets need not exist and their contents are preserved without loading them as active context. A location reference alone does not authorize moving, deleting, overwriting, or inventing content. Explicitly linking an existing specification requires verifying the supplied folder.

A non-null `current_request` requires enabled requests and MUST resolve to the existing `<features.requests.location>/00000000_000000_active` directory. Its request state must be nonclosed under the [request convention](request_conv.md). Disabled requests require `current_request: null`. Close or explicitly resolve an active request before disabling or relocating requests; a configuration toggle never silently clears or moves it. On closure clear `current_request` to null with the coordinated rename and reference updates defined there. Report naming or status inconsistencies without automatic repair.

### Feature configuration

Environment-manager owns feature flags and locations. State-only initialization creates no optional resources. Subsequent chat setup records explicit human choices, retaining unmentioned values. Enabling requests may create its empty directory; enabling instructions may create its empty file, with supplied instructions only when explicitly provided. Enabling specification does not fabricate specification contents. Chronicles-manager owns transcript contents after the leader routes enabled recording. Disabling a feature stops using that feature through environment configuration and preserves all files; it does not override independent higher-priority workspace or session instructions. Moving existing contents requires separately scoped authorization. State remains present with all optional features disabled.

## Workspace agent catalogue

The `agents` property is the authoritative workspace agent catalogue and registry. It maps agent names to entry objects with required string properties `path` and `selection_guide`, for example:

```json
{
  "agents": {
    "release-reviewer": {
      "path": ".hai_env/agents/release-reviewer/knowledge.md",
      "selection_guide": "Call to review a proposed release against its readiness criteria and report unresolved release issues."
    }
  }
}
```

Names and collisions follow the [agent convention](agent_conv.md). Each `path` MUST be exactly `.hai_env/agents/<name>/knowledge.md` for its key and resolve to a readable file inside the workspace. Reject symlink or junction resolution outside the workspace. It is a knowledge-file path, not a folder. `selection_guide` MUST contain non-whitespace, short actionable text consistent with the definition's scope and ownership, copied verbatim from its canonical Selection guide body. Author that section first, then copy and validate exact equality when creating or updating the definition or entry. Normal selection uses the catalogue copy; ordinary startup validates structure and references without loading every definition to compare guide equality. Report discovered stale copies without silently repairing them. Preserve additional entry properties during updates.

Missing `agents`, null, arrays, invalid entries or field types, blank guides, invalid names or paths, duplicate names, missing definitions, and framework-name collisions are invalid in version 2. Report invalid entries, exclude them from selection, and preserve them without repair. Valid independent entries remain usable when their own references validate. Malformed registry structure blocks registry writes; framework agents remain available. Other environment operations preserve invalid registry data and report it without claiming complete environment validity.

Workspace-agent-creator owns creation-time registrations after definition validation; environment-manager validates and reports them while owning general state. Preserve unrelated properties during either kind of update. Explicitly calling an unregistered agent does not register it. Framework agents, including chronicles-manager, do not require workspace registrations or enabled optional features to be selectable.

Earlier string-valued entries are legacy registrations without guides. Preserve and report them, exclude them from normal selection, and do not infer guides or silently convert them. Explicit human invocation may still select a valid canonical definition under the agent convention without changing registration. An existing-registration update needs separately scoped authorization and validated canonical path and guide; it is outside the creator's default new-agent workflow.

## Initialization template and compatibility

The canonical [state template](../agents/environment-manager/templates/state.json) supplies the supported environment format version and initialization defaults. Read its version; do not ask the human to supply it or infer it from a framework release.

Leader startup delegates initialization when `.hai_env/` is absent. Environment-manager creates only `.hai_env/state.json` from the template, with no selected request, empty catalogue, and four disabled features. No feature-location questions or additional authorization precede this minimal startup action. The leader then recommends additional chat setup and offers available next actions. The human may defer setup or keep all features off.

Existing but incomplete environment is not absent. Missing, malformed, or unreadable state and conflicting `.hai_env` paths require reporting and scoped repair rather than reinitialization. Version 1 is incompatible with version 2: report the compatibility issue and preserve live state. Do not silently migrate, reinterpret legacy defaults as opted-in features, or create optional resources. An explicitly authorized migration must settle feature choices, locations, and active-request handling before writing. Future incompatible format changes update this convention and increment the template version together.
