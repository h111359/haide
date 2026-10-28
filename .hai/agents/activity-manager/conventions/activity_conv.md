# Activity convention

## Artifacts and formats

Use UTF-8 Markdown for content and duplicate-free UTF-8 JSON for state. Canonical
artifacts live directly in one Activity folder:

| Artifact | Requirement and content |
| --- | --- |
| `state.json` | Mandatory identity, lifecycle and independent step metadata below. |
| `input.md` | Mandatory single initial input, preserved as supplied; may be empty until supplied. Never synthesize human input. Appended scope changes retain their source and date rather than replacing initial input. |
| `log.md` | Mandatory append-only UTC-dated meaningful actions, decisions, revisions, transitions, results, checks and failures. Related operations may share one entry; logging does not require recursive entries. |
| `decisions.md` | When useful: actual questions and answers, decisions, unresolved issues, author/source and date. Silence is not approval. |
| `definition.md` | When useful: agreed objective, scope, constraints and available acceptance criteria. |
| `analysis.md` | When useful: evidence, affected paths, comparisons, impact, risks, unknowns and conclusions. |
| `plan.md` | When useful: concrete proposed work and verification tied to the objective. |
| `outcome.md` | Required on closure: result against the objective, evidence, performed/skipped work, limitations, unresolved work and closure outcome. May be drafted earlier without implying closure. |

Initialize only state, input and log. Create no empty optional scaffold. `files/`
holds needed supporting files and revision history; `questionnaires/` holds useful
numbered saved question sets with stable question IDs; `results/` holds produced
Activity-specific outputs; `chronicles/` holds exact-source transcript segments.
Create these only when needed. Product code and durable specification remain in
canonical product locations. Link to them with source/identity as appropriate.
There is no mandatory duplicate `discussion.md`; a useful discussion summary is
clearly attributed analysis or decisions, never a substitute for exact chronicles.

## State schema

The state root is an object without duplicate property names. Required fields:

| Field | Type and meaning |
| --- | --- |
| `activity_id` | Nonblank unique UUID string assigned once at creation; never regenerated during renames, revisions, supplements or transcript segmentation. |
| `lifecycle` | `active` or `closed`, independent of work steps. |
| `created_at` | Actual initialization UTC timestamp, including for historical-import Activities. Imported source timestamps remain in their source records, not an invented earlier Activity creation time. |
| `closed_at` | `null` while active; actual UTC closure timestamp when closed. |
| `outcome` | `null` while active; `completed`, `cancelled` or `stopped` when closed. |
| `implementation_started_at` | `null` until a real first implementation attempt, then its UTC timestamp. Set before its changes/tests; never clear or replace on retries, revisions or closure. |
| `steps` | Object with required `clarification`, `analysis`, `planning`, `implementation`, `verification` keys. Each value is `not_started`, `in_progress`, `completed` or `skipped`. |

Use `YYYY-MM-DDTHH:MM:SSZ` timestamps. Initial state is active with null closure,
outcome and implementation-start fields, all steps `not_started`. Preserve unrelated
properties. Related Activities may be referenced with stable IDs plus final archive
paths when available; a path alone is not a stable identity. Imported historical
material must state its provenance and actual import date, without inventing prior
performed steps, continuity, completion, or missing source.

Lifecycle does not imply step completion. `completed` closure means the agreed
objective was met, which can be brainstorming or analysis alone. An implementation
objective requires its relevant checks and required external completion evidence.
Completed or in-progress implementation requires a real implementation-start marker.
Unperformed steps may stay `not_started` or be deliberately `skipped`, with the reason
in log/outcome. Record failed attempts and blocked/unrun verification honestly.
A closed Activity requires outcome.md, a closure timestamp and outcome; those fields
are null for an active Activity. Do not silently reinterpret unsupported records.

## Revisions and evidence

Material changes to definition, analysis or plan preserve the previous version
before publishing its replacement. Use unused dated files under
`files/revisions/<artifact>/`, such as `20261028_120000_01.md`, and record author/source,
UTC date, reason, predecessor and impact in the log or artifact revision entry.
Use exclusive creation, preserve exact prior content and keep relative references
valid. Do not overwrite a prior version or delete historical evidence merely because
it became stale. First-time creation of a previously absent artifact is allowed at
any appropriate point, including after implementation began; never pretend it
existed earlier or retroactively approved completed work.

Reassess dependent artifacts, assumptions, code and checks after a revision. Preserve
their prior evidence, mark affected step results `in_progress` or `not_started` as
appropriate, and state what must be repeated. Unaffected evidence remains usable.
Log meaningful deviations and decisions. The implementation-start marker records
history; it does not freeze artifacts or establish successful implementation.

## Location and sole current record

HAI provides mandatory caller-validated `activities.location`, default
`.hai_env/activities`. There is no Activity toggle, standalone fallback or global
chronicle location. Never guess another store or bypass invalid configuration.

Every Activity occupies one direct child folder of its store. At most one has
`lifecycle: active`, and it MUST use `00000000_000000_active`. All previous records
are closed. The fixed folder and its own state identify current work; no collection
state file or external current pointer is created or consulted. An absent store
or current folder is valid before meaningful new work, not an error to repair.

Startup asks Activity-manager to discover and resume current work after compatible
context is available. A new chat alone creates none. Meaningful new substantive
work with no current record authorizes creation; no separate tracking opt-in exists.
If unrelated current work exists, leader resolves continuation or authorized closure
before another Activity is created. Never silently overwrite, reuse or close it.

Before creating or mutating records, inspect direct child Activity-folder states
only to establish sole-current consistency. Validate each candidate folder as a
contained nonlinked directory before opening its contained regular state file;
never follow a symlink/junction to discover state. Reject multiple active records, an
active record under another name, a closed record at the current path, duplicate
IDs, or unreadable/missing states that prevent validation. Do not recursively load
history or infer repairs. A store-level `state.json` is unsupported, not a pointer.
Recheck inspected inputs and target absence before writes and use exclusive creation.
Partial operations are preserved and reported, never silently repaired or retried.

### Safe paths

Validate the explicit workspace as an existing directory. Resolve the store,
existing ancestors and selected record paths before reads and again before writes.
Reject blank/traversal paths, workspace-root stores, escaping symlinks/junctions,
version-control metadata, the reusable framework, and overlaps with protected
configuration or other configured content locations. Missing targets must have
safe resolved existing ancestors. Account for native case rules. Require directory
stores/record folders; reject symlinked/junction record folders and nonregular or
linked canonical artifacts. Caller validation of configuration does not replace
local containment/type checks. Supplied paths authorize neither relocation nor
overwriting. Configuration changes do not move, close or delete records.

## Closure, archival and references

Closure is an authorized decision from any performed-work state. Completing a
step or delivering a response does not close current work. Determine the actual
outcome and write outcome.md against the agreed objective before reporting closure.
Rename the current folder to `YYYYMMDD_HHMMSS_short-label` using the actual UTC
closure time, identical to `closed_at`. Labels use one to five lowercase ASCII
alphanumeric words separated by single hyphens. On a name collision append the
first unused suffix `_02`, `_03`, and so on with at least two digits, outside the
label word count. Never overwrite; the rename must fail if the destination appears
between check and write. For example: `20261028_140000_activity-records_02`.

Coordinate outcome, timestamp, available destination, archive rename, state changes
and affected persistent references. Preserve ID, creation time, implementation
start and all contents. Historical references use final archive paths and stable
IDs, not the reusable current path. Keep internal references relative where possible.
Verify archive/state agreement, absent current folder, sole-current consistency and
updated references before claiming success or creating another Activity. Rename
and file writes are not an atomic transaction: on failure stop dependent work,
preserve partial results and report exactly what remains inconsistent.

## Closed-record supplements and chronicles

Closed Activities are not reopened for substantive work. A new substantive task
uses a new linked Activity once the current boundary is resolved. Closed records
permit append-only dated supplements recording author/source, UTC date, reason,
evidence and what earlier assertion they supplement; preserve original assertions
and lifecycle. Delayed synchronization of already completed authoritative source
exchanges is permitted under the original Activity without reopening it.

Optional chronicles are Activity-local and may have multiple segments for the same
chat and Activity. Leader assigns exact source-exchange boundaries, with human
clarification when ambiguous; chronicles-manager applies and verifies those bounds
and never creates or closes Activities. Disabled periods receive no new transcripts
and no implicit later backfill. Only explicitly authorized historical import may
backfill such a period, retaining provenance and exact-source limitations. Missing
durable source is reported, never manufactured. Detailed source, naming, timing
and synchronization rules belong to chronicles-manager.

## References

- [Activity concept](../concepts/activity.md): work unit and lifecycle boundaries.
- [Activity-manager](../SKILL.md): discovery, work, revisions and closure procedures.
- [Chronicles-manager](../../chronicles-manager/SKILL.md): exact-source segment policy.
