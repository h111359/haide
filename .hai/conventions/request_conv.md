# Request

## Artifacts and formats

Use UTF-8 Markdown for request content and UTF-8 JSON for request state. Canonical
files live directly in the request folder:

| File | Contents and availability |
| --- | --- |
| `input.md` | One human-supplied initial input, preserved as supplied; initially empty if not yet provided. Never synthesize human input. |
| `definition.md` | Intent, scope, constraints, and acceptance criteria; present only after clarification and while valid. |
| `analysis.md` | Affected workspace paths, impact, risks, edge cases, and unresolved questions; present only after analysis and while valid. |
| `plan.md` | Implementation and verification steps; present only after planning and while valid. |
| `decisions.md` | Questions and actual human answers, with stage and source; unresolved answers remain explicitly unanswered. Initially empty. |
| `log.md` | Append-only UTC-dated actions, transitions, invalidations, implementation progress, checks and outcomes, deviations, and failures. |
| `discussion.md` | Append-only request-related human prompts and AI replies in order, with speaker labels. Independent of derived artifacts and optional session chronicles. |
| `state.json` | The request metadata below. |

Optional saved questionnaires use `questionnaire-01.md`, `questionnaire-02.md`,
and increasing unused numbers. Give questions stable local identifiers; copy actual
answers and their source into decisions rather than treating a questionnaire as
approval. Do not create empty questionnaires. Content may use subfolders for needed
supporting material, but never multiple canonical files of the same component.

Initialization creates input, decisions, log, discussion, and state only. Derived
artifacts are created when their stages finish. Before implementation, invalidation
removes only the affected derived artifacts and records the reason in log; decisions,
discussion, and action history remain. At implementation start, existing definition,
analysis, and plan become immutable and skipped ones remain absent forever.

Record actions and their results throughout every stage, including inspections and
failed operations. One log entry may describe a related batch of actions; recording
the entry itself does not require a recursive entry. Discussion is retained even
when a prompt does not change the definition, analysis, or plan.

### Request state

The root is a JSON object without duplicate property names. Required fields are:

| Field | Type and meaning |
| --- | --- |
| `stage` | One of `Initial`, `Clarified`, `Analysed`, `Planned`, `Implemented`, `Closed`; the last completed stage, not an assertion that work in progress succeeded. |
| `created_at` | UTC ISO 8601 timestamp for initialization. |
| `implementation_started_at` | UTC ISO 8601 timestamp for the first implementation attempt, or `null`. Never clear or replace it on retries or closure. |
| `closed_at` | UTC ISO 8601 closure timestamp, or `null` before closure. |
| `outcome` | `null` before closure; at closure, `completed`, `cancelled`, or `stopped`. The log explains the outcome and any incomplete work. |

Use timestamps in `YYYY-MM-DDTHH:MM:SSZ` form. Initial state uses `Initial`
and null implementation-start, closure, and outcome fields. Preserve unrelated
additional properties. Nonclosed records have null closure and outcome fields;
closed records require both. `Implemented` requires an implementation-start timestamp.
`completed` closure requires verified implementation; cancellation or early closure
does not establish it. Do not silently convert existing unsupported records.

Repeated pre-implementation clarification records `Clarified` and invalidates analysis
and plan; repeated analysis records `Analysed` and invalidates plan; repeated planning
records `Planned`. An explicit early Implement skips missing stages. Write the first
implementation-start timestamp before implementation changes or tests; frozen artifacts
stay unchanged even on failure. Record `Implemented` only after successful requested
work and relevant verification, including required enabled specification handoffs.
Further implementation attempts retain the start timestamp; failed attempts retain
the preceding completed stage and log the failure. Before new work invalidates an
existing `Implemented` result, restore the last completed preparatory stage supported
by its artifacts, or `Initial` when none exist; retain the original start timestamp.
Closure records `Closed` regardless of the preceding stage.

## Location and active folder

Requests must be enabled in environment state before creating or loading
them through environment configuration. Every [request] occupies one folder
directly under `features.requests.location` (default `.hai_env/requests`).
Resolve and validate this workspace-relative location using the state
convention; do not assume the default or scan for another location.
At most one request may be in a stage other than `Closed`. Its folder
MUST be named `00000000_000000_active`. This name sorts before closed
request folders in ascending name order.

Creating a request MUST fail if the active path already exists; never
overwrite or reuse its contents. When a current request is selected,
`current_request` in environment state points to
`<features.requests.location>/00000000_000000_active`.

Request-manager owns request artifacts and lifecycle changes to `current_request`:
set it during successful initialization and clear it during closure. Environment-manager
owns general environment state, feature flags, and locations. Initialization requires
no selected request and no other nonclosed request in the configured directory.
Create files without overwriting, reread environment state before updating its
reference, preserve unrelated properties, and stop on concurrent changes. Verify
records and reference together. Partial creation or reference updates must be reported
and preserved, not silently reused or repaired.

Disabled requests require `current_request: null` and do not authorize
creating request files. Before disabling or relocating requests with an
active request, resolve its lifecycle and references explicitly. A flag or
location change does not close, move, delete, or clear an active request.
Disabling preserves request history. Enabling creates no request by itself.

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
