# Request

## Location and active folder

Every [request] occupies one folder directly under `.hai_env/requests/`.
At most one request may be in a stage other than `Closed`. Its folder
MUST be named `00000000_000000_active`. This name sorts before closed
request folders in ascending name order.

Creating a request MUST fail if the active path already exists; never
overwrite or reuse its contents. When a current request is selected,
`current_request` in environment state points to
`.hai_env/requests/00000000_000000_active`.

## Closed folder name

When a request enters `Closed`, its folder MUST be renamed to
`YYYYMMDD_HHMMSS_short-label`.

- The timestamp is the actual UTC date and time of closure, to seconds.
  It is not the creation time. Use the same closure time for the folder
  name and any recorded closure timestamp.
- Closure includes cancellation or stopping from any stage; it does not
  establish successful implementation.
- The descriptive label contains one to five lowercase words separated
  by single hyphens. Each word uses ASCII letters `a` through `z` or
  digits `0` through `9`; spaces and other punctuation are not allowed.
- Preserve existing creation-time metadata. This naming convention does
  not introduce or change a request-state schema.

For example, closing a request at `2026-10-19T14:30:25Z` with the label
`request-folder-names` produces `20261019_143025_request-folder-names`.
Ascending name order groups closed requests by UTC closure time;
requests closed within the same second are then ordered by their names.

Before renaming, check that the destination does not exist. On a name
collision only, append the first available numeric suffix, starting at
`_02`, then `_03`, and so on, with at least two digits. For example,
`20261019_143025_request-folder-names_02`. The suffix is separate from
the label's word count. Never overwrite an existing file or folder;
the rename MUST also fail if its destination appears after the check.

## Closure and references

Treat closure as one coordinated operation:

1. Prepare the closure outcome, UTC timestamp, available destination,
   and affected persistent references before changing the request.
2. Rename the active folder, record the request's `Closed` stage and
   closure outcome, update affected references to its final folder, and
   clear environment state's `current_request` to `null`. Preserve
   unrelated state properties and request contents.
3. Verify the archived folder and request state agree, `current_request`
   is `null`, the active path is absent, and affected references resolve
   to the archived request before reporting successful closure or
   creating another request.

A folder rename and state-file updates are not a single atomic
transaction. If any step fails, stop, report exactly which changes
completed and which remain inconsistent, and preserve the existing
contents. Do not claim successful closure, create another request, or
silently repair a partial operation.

The fixed active path will be reused for subsequent requests. Historical
references MUST point to the final closed folder, not that reusable
path. Keep references within a request relative where possible, and
check references affected by its rename.

## References

- [Request concept](../concepts/request.md): components, stages, and lifecycle.
- [State convention](state_conv.md): environment state and current-request reference.
