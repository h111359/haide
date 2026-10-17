# State

## File format

JSON

## Location

`.hai_memory/state.json`

## Content

The root MUST be a JSON object with these required properties:

| Property | Type | Meaning and initial value |
| --- | --- | --- |
| `specification_location` | string or null | Path to the existing [specification] root folder; `null` when none is linked. |
| `current_request` | string or null | Path to the current [request] folder under `.hai_memory/requests/`; `null` when none is selected. |
| `compatible_version` | positive integer | Memory format version, not the HAI framework or product version. Use the version supplied by the canonical template. |

Paths MUST be non-empty, relative to the workspace root, and use `/`
as the separator. Non-null references MUST resolve to existing folders.
Additional properties may hold workspace parameters; preserve them when
updating existing state. Duplicate JSON property names are invalid.

## Initialization template and compatibility

The canonical empty-state template is
[state.json](../agents/memory-manager/templates/state.json).
It is the authoritative source of the currently supported memory format
version. Read that version from the template; do not ask the human to
supply it or infer it from a framework release.

New memory uses this template unchanged by default, with no selected
request or linked specification. Set `specification_location` only when
linking an existing specification is explicitly requested.

When changing the memory format incompatibly, update this convention
and increment the template's version together. An existing state whose
version differs from the template's version requires a compatibility
decision or migration; do not silently rewrite or treat it as absent.
