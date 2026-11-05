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

The initial artifact set is state, input and log. Optional artifacts have meaningful
content rather than empty scaffold. `files/` holds supporting material and revision
history; `questionnaires/` holds useful numbered saved question sets with stable
question IDs; `results/` holds Activity-specific outputs; `chronicles/` holds exact
source segments. Product code/durable specification retain canonical locations and
attributable links. A discussion summary is attributed analysis or decisions,
not a mandatory duplicate `discussion.md` or substitute for exact chronicles.

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

Material revisions retain the exact predecessor in an unused dated path under
`files/revisions/<artifact>/`, for example `20261028_120000_01.md`. Provenance identifies
author/source, UTC date, reason, predecessor and dependent impact. Earlier evidence
and valid relative references remain attributable even when superseded.

A new artifact may first appear after implementation began; its date/source cannot
imply earlier existence or retroactive approval. Revised dependent step results
reflect the reassessment, with stale evidence retained and the required repeat work
identified. The original implementation-start marker stays unchanged.

## Location and sole current record

HAI provides mandatory caller-validated `activities.location`, default
`.hai_env/activities`. There is no Activity toggle, standalone fallback or global
chronicle location. Never guess another store or bypass invalid configuration.

Every Activity occupies one direct child folder of its store. At most one has
`lifecycle: active`, and it MUST use `00000000_000000_active`. All previous records
are closed. The fixed folder and its own state identify current work; no collection
state file or external current pointer is created or consulted. An absent store
or current folder is valid before meaningful new work, not an error to repair.

The consistency contract rejects multiple active records, an active record under
another name, a closed record at the current path, duplicate IDs, unsupported state,
or missing/unreadable states that prevent validation. Activity folders are contained
nonlinked direct-child directories with regular nonlinked canonical artifacts.
A store-level `state.json` is unsupported, not a pointer. Record discovery and
creation ordering belong to Environment-manager's owning procedures.

### Safe paths

The workspace is an existing directory; store and record paths resolve inside it,
including existing ancestors of missing targets and native case/alias behavior.
Blank/traversal paths, workspace-root stores, escaping links/junctions,
version-control metadata, reusable framework paths and overlaps with protected
configuration/other configured content are invalid. Stores and record folders are
directories; record folders cannot be links/junctions, and canonical artifacts are
regular nonlinked files. Caller configuration assurance is separate from local
containment/type validation. A location reference conveys no relocation/overwrite
permission, and configuration changes do not alter record lifecycle or contents.

## Closure, archival and references

A closed record has `outcome.md`, an actual UTC `closed_at` timestamp and closure
outcome. Its archive folder is `YYYYMMDD_HHMMSS_short-label` with the same closure
time. Labels have one to five lowercase ASCII alphanumeric words separated by
single hyphens. A collision suffix is the first unused `_02`, `_03`, and so on
with at least two digits, outside the label word count; for example
`20261028_140000_activity-records_02`.

Closure preserves stable ID, creation time, original implementation start and all
contents. Persistent historical references identify stable IDs and final archive
paths rather than the reusable current path; internal references remain relative
where possible. A consistent completed closure has matching archive/state time,
no current folder and correct affected references. Rename and file writes are not
one atomic transaction; partial operations remain explicit results. Execution
ordering and authorized closure decisions belong to the owner procedure.

## Closed-record supplements and chronicles

A supplement is append-only evidence with author/source, UTC date, reason,
supporting evidence and the earlier assertion supplemented. Historical assertions
and the closed lifecycle remain intact. New substantive work has a separate linked
Activity identity. Delayed synchronization of completed source exchanges can still
belong to their original closed Activity.

Chronicles have Activity-local segment identity and exact source assignments.
Their layout, source/naming contract and compatibility are owned by
the installed Codex Chronicle-manager transcript convention at `.hai_env/agents/codex-chronicle-manager/conventions/transcript-segment_conv.md`.
Environment-manager owns discovery policy and record mutation; the shared startup context helper may perform read-only discovery for Leader. Codex Chronicle-manager owns transcript/checkpoint writes. Leader serializes both for the stable Activity.

## References

- [Activity concept](../concepts/activity.md): work unit and lifecycle boundaries.
- [Environment-manager](../SKILL.md): discovery, work, revisions and closure procedures.
- Installed Codex Chronicle-manager transcript convention — conditional for recording; never load a library source as a runtime fallback.
