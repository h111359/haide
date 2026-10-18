# State

## File format

JSON

## Location

`.hai_memory/state.json`

## Content

The root MUST be a JSON object with these required properties:

| Property | Type | Meaning and initial value |
| --- | --- | --- |
| `specification_location` | string or null | Configured path to the [specification] root folder, which may not exist yet. Default: `.hai_memory/specifications`. `null` means no location is configured. |
| `current_request` | string or null | Path to the current [request] folder under `.hai_memory/requests/`; `null` when none is selected. |
| `compatible_version` | positive integer | Memory format version, not the HAI framework or product version. Use the version supplied by the canonical template. |

Paths MUST be non-empty, relative to the workspace root, and use `/`
as the separator. A non-null `current_request` MUST resolve to an existing
folder. A configured `specification_location` may be absent; if the path
exists, it MUST be a folder. Selecting a location does not create or
verify a specification. Explicitly linking an existing specification
requires verifying the supplied folder before recording its location.
Additional properties may hold workspace parameters; preserve them when
updating existing state. Duplicate JSON property names are invalid.

## Initialization template and compatibility

The canonical initialization template is
[state.json](../agents/memory-manager/templates/state.json).
It is the authoritative source of the currently supported memory format
version. Read that version from the template; do not ask the human to
supply it or infer it from a framework release.

New memory uses the template's default `specification_location` unless
the human chooses another location during initialization. The
memory-manager resolves that choice before writing state, following its
initialization procedure. No current request is selected. Recording the
chosen location does not create a specification or assert that one
already exists. Existing states with `specification_location: null`
remain valid; do not replace their value automatically.

When changing the memory format incompatibly, update this convention
and increment the template's version together. An existing state whose
version differs from the template's version requires a compatibility
decision or migration; do not silently rewrite or treat it as absent.
