# State

## File format

JSON

## Location

`.hai_env/state.json`

## Content

The root MUST be a JSON object with these required properties:

| Property | Type | Meaning and initial value |
| --- | --- | --- |
| `specification_location` | string or null | Configured path to the [specification] root folder, which may not exist yet. Default: `.hai_env/specifications`. `null` means no location is configured. |
| `current_request` | string or null | Path to the current [request] folder under `.hai_env/requests/`; `null` when none is selected. |
| `compatible_version` | positive integer | HAI environment format version, not the HAI framework or product version. Use the version supplied by the canonical template. |

Paths MUST be non-empty, relative to the workspace root, and use `/`
as the separator. A non-null `current_request` MUST resolve to an existing
folder. A configured `specification_location` may be absent; if the path
exists, it MUST be a folder. Selecting a location does not create or
verify a specification. Explicitly linking an existing specification
requires verifying the supplied folder before recording its location.
Additional properties may hold workspace parameters; preserve them when
updating existing state. Duplicate JSON property names are invalid.

A selected current request MUST be nonclosed and use
`.hai_env/requests/00000000_000000_active`, following the
[request convention](request_conv.md). On closure, clear
`current_request` to `null` as part of the coordinated folder rename
and reference updates defined there. Naming or status inconsistencies
must be reported; they do not authorize automatic renaming or repair.

## Workspace agent catalogue

The optional `agents` property is the authoritative workspace agent catalogue
and registry. It is a JSON object mapping agent names to entry objects
with required string properties `path` and `selection_guide`, for example:

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

Names and collisions follow the [agent convention](agent_conv.md). Each
`path` MUST be exactly `.hai_env/agents/<name>/knowledge.md` for its key
and resolve to a readable file inside the workspace. Reject symlink/junction
resolution outside the workspace. It is a knowledge-file path, not a folder.
`selection_guide` MUST contain non-whitespace, short actionable text stating
when to call the role and its expected result, consistent with the definition's
scope and ownership. Its value MUST be a verbatim copy of the canonical
Selection guide body in `knowledge.md`, as defined by the agent convention.
Author that section first, then copy it into state and validate exact equality
when creating or updating the definition or entry. Do not store procedures here.
Ordinary selection uses the copy without scanning all definitions; startup
validates entry structure and references without verifying every copy's equality.
Report a discovered stale copy without silently repairing it.
The fixed path records explicit registration rather than allowing arbitrary
external agent locations. Preserve additional entry properties when updating.

Absent `agents` means an empty registry for existing version-1 environments;
`null`, arrays, invalid entry objects or field types, blank guides,
invalid names/paths, duplicate names,
missing definitions, and framework-name collisions are invalid. Report invalid
entries, exclude them from selection, and preserve them without repair. Valid
entries remain usable when their own references validate. Malformed registry
structure blocks registry writes; framework agents remain available. Other
environment operations must preserve invalid registry data and report it,
and must not claim complete environment validity.

The workspace-agent-creator owns creation-time registrations after definition
validation; environment-manager validates and reports them while owning general
state. Preserve unrelated properties during either kind of update. Explicitly
calling an unregistered agent never registers it. New environments include
`agents: {}`. This optional additive field retains format version 1 and requires
no rewriting or migration of existing states without it or with an empty object.

Earlier string-valued entries are legacy registrations without selection
guides. Preserve and report them, exclude them from normal selection, and
do not read their definitions to infer guides or silently convert them.
Explicit human invocation may still select a valid canonical definition
under the agent convention without modifying its registration. Report that
normal selection requires an explicitly authorized catalogue update supplying
a validated canonical definition path and agreed selection guide. Such an
existing-registration update is outside the creator's default new-agent
workflow and requires a separately scoped authorization. This transitional
read-only handling retains environment format version 1; it does not declare
legacy entries valid or migrate live state. Missing and empty registries
remain fully readable; framework agents remain available in every case.

## Initialization template and compatibility

The canonical initialization template is
[state.json](../agents/environment-manager/templates/state.json).
It is the authoritative source of the currently supported environment format
version. Read that version from the template; do not ask the human to
supply it or infer it from a framework release.

A new environment uses the template's default `specification_location` unless
the human chooses another location during initialization. The
environment-manager resolves that choice before writing state, following its
initialization procedure. No current request is selected. Recording the
chosen location does not create a specification or assert that one
already exists. Existing states with `specification_location: null`
remain valid; do not replace their value automatically.

When changing the environment format incompatibly, update this convention
and increment the template's version together. An existing state whose
version differs from the template's version requires a compatibility
decision or migration; do not silently rewrite or treat it as absent.
