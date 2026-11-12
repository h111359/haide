# HAI runtime

See [Windows and Linux execution](PORTABILITY.md) for path contracts, native
interpreter invocation, recording representation, exact-byte handling and the
workspace-contained regression runner. Startup includes observed
`execution_context`; this is separate from core validity and recording readiness.

Run `python -B .hai/tools/hai.py startup --workspace .` for core environment, Activity and separate read-only `recording_context` readiness. Required recording needs binding/synchronization before substantive recorded work, even when core `ok` is true. Common options may precede or follow the group. Commands emit JSON with `ok`, `status`, `operation`, `result`, `changed_files`, and `issues`. Exit codes are 0 for success or a valid plan, 1 for blocked, partial or unsupported work, and 2 for invalid invocation. Optional registration and model profile issues are reported separately from core environment validity.

Use `--request PATH` for a UTF-8 JSON object within the workspace. Duplicate keys and nonstandard numeric constants are rejected. Mutations are previews by default; add `--apply` to perform them. Mutation requests include `"provenance": {"source": "...", "reason": "..."}` with nonblank values. A pre-existing `.hai_env/.runtime.lock` blocks writes and requires inspection; do not remove an unexplained lock automatically. Partial results identify paths that were changed and must be inspected before another attempt.

- `environment initialize`: provenance only; creates absent state and missing instructions, preserving existing instructions.
- `environment migrate-layout`: provenance only; previews relocation of legacy `.hai_env/` state, profiles and instructions into `.hai_env/config/`. Add `--apply` only for explicitly authorized migration after stopping other writers. Preserves exact bytes and optional profile absence; retains recovery copies and a migration manifest. Mixed, conflicting or incomplete layouts require explicit reconciliation, never automatic overwrite or retry. See [migration procedure](../../procedures/migrate-environment-layout.md).
- `environment configure`: `changes` maps explicit dotted names to values. Supported names are `activities.location`, `features.chronicles.enabled`, and `features.chronicles.record_every_prompts`; changing a location does not move content.
- `environment migrate-specification`: provenance only; previews or executes the scoped format-2 migration using its existing backup and candidate safeguards.
- `profiles check` reads optional profiles. `profiles configure` takes `changes` naming `light`, `standard`, or `advanced`; all three model IDs must be present after the update. This does not establish host model availability.
- `configuration read` takes `agent`. `configuration update` takes `agent`, provenance and `changes` keyed by names declared in that installed agent's contract.

For example, save `{"provenance":{"source":"user request","reason":"adjust cadence"},"changes":{"features.chronicles.record_every_prompts":10}}` in a workspace JSON file, then run `python -B .hai/tools/hai.py environment configure --request change.json --workspace .` to preview. Add `--apply` to write.

Workflow modules provide Activity, package, recording and host operations. A host capability check reports availability; the runtime does not install dependencies or download packages implicitly.

## Workflow operations

Requests are JSON objects. All applied Activity and package mutations require valid current core state and readable mandatory instructions. For example, `python -B .hai/tools/hai.py activity discover --workspace .` reads the current Activity; add `--request request.json` where fields are listed below. Every mutation requires the provenance object described above.

- `activity discover` takes `{}`. `activity show` takes `activity_id`.
- `activity usage-update` takes `activity_id`, provenance and optional `sources`, `pricing` and `reported_spend`. It previews by default; `--apply` refreshes assigned source ranges into Activity-local `usage.json` and `usage.md`. `activity usage-read` takes only `activity_id` and reads a retained snapshot, including archives. Closure automatically refreshes usage before lifecycle writes; unknown data is unavailable/stale, never fabricated zero. See [source attribution, counters and estimates](../../conventions/activity-usage_conv.md).
- `activity invocation-allocate` takes `activity_id`, `agent` and provenance. Preview creates nothing (`allocated: false`); `--apply` exclusively creates `files/agent-invocations/<uuid>/invocation.json` below the current Activity and returns its existing folder (`allocated: true`), stable IDs, Activity-relative suffix and metadata. Closed/stale IDs, collisions and unsafe paths are rejected. Partial results retain and name changed paths. See [allocation and actual host handoff](../../conventions/agent-invocation_conv.md); the runtime does not spawn agents.
- `activity chat-read` takes `activity_id`, optional nonnegative integer `after_sequence` (default `0`) and optional integer `limit` (`1..1000`, default `100`). Returns a page with `messages`, `total_messages`, `next_after_sequence` and `has_more`; reads closed Activities too. Omit `--apply` for reads. `activity chat-post` takes `activity_id`, `author`, `text` and provenance. It previews by default; `--apply` appends to the current Activity's `chat.jsonl` under the runtime lock. No edit/delete action exists. See [chat format and participation](../../conventions/activity-chat_conv.md), including attribution and filesystem-access limits.
- `activity create` takes `initial_input` and provenance. `activity record` takes `activity_id`, optional `steps` mapping step names to statuses, optional `implementation_start` Boolean, optional `artifacts` array of `{name, text, reason}`, optional `input_append`, `log`, and provenance. `activity close` takes `activity_id`, `outcome`, `archive_label`, `outcome_text`, `recording` with `status` and `details`, and provenance. It also accepts `recording_requirement` with Boolean `enabled` and `mandatory`, and a `recording_proof` gate request. Verified closure additionally supplies `recording_paths` with `sources` mapping source IDs to workspace-relative files and `artifacts` mapping artifact IDs to files inside the Activity; their hashes must match the gate evidence. `activity supplement` takes `activity_id`, `text`, and provenance. When chronicles are enabled or independently mandatory, closure synchronizes assigned sources through completed saved exchanges and verifies the core transcript before archival; missing/failed recording blocks closure. Explicit compatible proof remains supported. Disabled/no-obligation closure requires no transcript. These operations preserve partial results on failure.
- `packages validate` takes `definition`; `packages resolve` takes `definition` and `runtime`, a capability snapshot shaped as `{"models":{"model-id":["high"]}}`. `packages audit` takes `{}`. `packages install` takes workspace-relative `source`, `name`, provenance, and optional Boolean `replace` and `register`. Replacement additionally requires the exact `reviewed_differences` list returned by a preview; the previous package is retained as a backup. Registration may require a separate reconciliation after replacement. `packages register` takes `name` and provenance. Remote acquisition is unsupported. Safe no-overwrite package and Activity moves require an available native atomic rename primitive. Implementations cover Linux, Windows and macOS; only Linux has been tested here.
- `recording status` takes `{}` and reports the configured flag, threshold, and available evidence. `recording schedule` takes `occurrence_ids`, optional `covered_ids`, optional positive integer `threshold`, and optional `last_dispatched_count` for the previously dispatched observed count. It reports gaps and whether dispatch is due; it does not persist a checkpoint or start a background task. `recording assess-closure` accepts the structured request defined by the recording gate helper. The recorder consumes explicit assignments; bounded current-session discovery/binding is documented below.
- `host check` takes `model`, `effort`, and caller-supplied `models` mapping each model ID to an array of supported efforts. It reports whether that evidence contains the pair. The runtime does not discover host capabilities or invoke a host agent.

## Activity chat example

Save a UTF-8 workspace request such as `chat-post.json`:

```json
{
  "activity_id": "<current stable Activity UUID>",
  "author": "software-developer",
  "text": "The implementation is ready for the assigned verification work.",
  "provenance": {"source": "assigned developer", "reason": "handoff"}
}
```

Preview with `python -B .hai/tools/hai.py activity chat-post --workspace . --request chat-post.json`;
append by adding `--apply`. To read, use a separate request containing only
`{"activity_id":"<same UUID>"}` with `activity chat-read`. For later pages, include
the returned `next_after_sequence` as `after_sequence`. These examples do not assign
an agent, authenticate an author or imply the described implementation is complete.

## Invocation allocation example

Save a workspace-contained JSON request, for example `invocation-request.json`:

```json
{
  "activity_id": "<current stable Activity UUID>",
  "agent": "software-developer",
  "provenance": {"source": "authorized host assignment", "reason": "allocate before a new spawn"}
}
```

Preview with `python -B .hai/tools/hai.py activity invocation-allocate --workspace . --request invocation-request.json`.
Add `--apply` to allocate. Dispatch only after successful applied readback, passing
the returned `path`, `activity_relative_path`, `activity_id` and `invocation_id` in
the first assignment. Record the actual returned host handle and observed launch
status through `activity record`; the manifest is not launch evidence.

Same-live-instance follow-ups keep the allocation; every new spawn attempt uses a
new one. Failed or uncertain launches retain material. Host closure waits for
verified ended writers; allocation locks do not stop later filesystem writes.
There is no new global registry, cleanup command or security sandbox.

Run `python -B -m unittest discover -s .hai/tools/runtime/tests -p 'test_invocations.py'`
for allocation, CLI, concurrency, unsafe-path, partial-failure and archive fixtures.
Separately observe real host launches receiving usable distinct folders and writing
independent files; fixture success alone does not prove host handoff. Controlled
verification Activities may be used so product work is not closed for a test.

## Chat verification

Run `python -B -m unittest discover -s .hai/tools/runtime/tests -p 'test_chat.py'`
for isolated fixtures covering shared authorship, exact append preservation,
preview/read behavior, CLI requests, pagination, malformed history, unsafe links,
lock contention, partial writes and archive/new-Activity separation. Tests do not
invoke agents or establish OS-level immutability. Report actual platform and skips.

## Activity usage example

Save a workspace-contained JSON request with an explicitly authorized source:

```json
{
  "activity_id": "<current stable Activity UUID>",
  "sources": [
    {"path": "/explicit/saved-session.jsonl", "session_id": "<original source session ID>", "start_position": 42}
  ],
  "provenance": {"source": "host Activity assignment", "reason": "refresh requested usage"}
}
```

Run `python -B .hai/tools/hai.py activity usage-update --workspace . --request usage-request.json`
to preview and add `--apply` to persist. Later requests need only `activity_id` and
provenance to refresh the same bindings. Position 42 is an example, not a default;
the host supplies actual Activity attribution and does not scan unrelated sessions.
`end_position` is optional for a fixed inclusive cutoff; otherwise the source is
read through its latest complete saved record.

Optional pricing is a rate snapshot, not a framework default:

```json
{
  "rates": {
    "example-model": {
      "input_credits_per_million": "10",
      "cached_input_credits_per_million": "1",
      "output_credits_per_million": "20"
    }
  },
  "source": "Explicit example rate card; these are not current prices",
  "captured_at": "2026-11-06T00:00:00Z"
}
```

Pass that object as `pricing` only when actual selected rates and provenance are
available. Reports and configuration cover tokens and credits only.
No API keys, account credentials, billing calls or network access are used.

Run `python -B -m unittest discover -s .hai/tools/runtime/tests -p 'test_usage.py'`
for cumulative/interval accounting, model rates, reported-spend freshness, malformed
sources, idempotent totals, unavailable data, optimistic/partial persistence, CLI,
archive reads and automatic pre-closure refresh. These checks do not authenticate
host billing evidence or prove completeness of all related sessions.

## Current-session source discovery and early binding

Enabled recording authorizes read-only lookup of the current host-identified
session. `recording discover` accepts optional `session_id`, `source_path`,
`codex_home`, `representation` (default `event_msg`), `mandatory` and `provenance`.
Prefer host `CODEX_THREAD_ID`, then `CODEX_SESSION_ID`; a supplied ID must agree
with that selected identity. An inherited parent session ID can differ from a
participant's current thread. Prefer a canonical supplied path;
otherwise inspect filenames under the Codex home's `sessions/` tree for exactly
one `rollout-*-<session UUID>.jsonl`, then validate only that candidate's embedded
identity, workspace, schema and canonical nonlinked/singly-linked file. No other
conversation content is read. Zero/multiple candidates fail; there is no newest-file
heuristic. Results contain metadata and `latest_user_occurrence`, never source text.
No saved user occurrence in the chosen representation blocks discovery with an
actionable diagnostic. Some participant surfaces require explicit `response_item`
instead of default `event_msg`; representations are never guessed or merged.

`recording bind` additionally requires `activity_id`, observed `start_position`,
`enabled_intervals` and provenance. The start is a saved user occurrence in the
selected representation; the host attributes it to the first actual Activity work
prompt. Latest occurrence does not select an existing Activity's range. Intervals
follow the existing synchronization schema. Preview is read-only; `--apply` persists
through the synchronizer and returns `usage_source` for separate `activity usage-update`.
Existing ranges cannot silently move. Disabled/no-independent-obligation commands
perform no discovery/writes. Independent mandatory recording supplies `mandatory:
true` plus applicable instruction provenance.

The host verifies that a user occurrence is the actual work prompt, not an
environment-only context record. Native delegated assignments can use the
existing explicit `recording synchronize` path at their verified assignment
position; do not feed an environment record to interactive `recording bind`.
The adapter still excludes inter-agent/tool metadata from transcript text.

Example workspace-contained request (values are placeholders):

```json
{"activity_id":"<current UUID>","start_position":42,"enabled_intervals":[{"start":{"source_session_id":"<host session UUID>","source_position":42},"end":null,"provenance":"recording enabled before this observed work prompt"}],"provenance":{"source":"authorized host assignment","reason":"register before recorded work"}}
```

Run `<absolute-python> -B .hai/tools/hai.py recording bind --workspace . --request <request.json>`;
add `--apply` for persistence. Position 42 is illustrative, never a default. Startup
never mutates a binding. `recording_context` reports disabled, needs_activity,
needs_binding, verified, needs_synchronization, blocked or unverified independently
of core validity. Missing current host identity remains unverified even with a
previously registered source. Source failures become visible here immediately. See the owning
[procedure](../../procedures/establish-recording-source.md).

Run `<absolute-python> -B -m unittest discover -s .hai/tools/runtime/tests -p 'test_source_discovery.py'`
for discovery/readiness/binding integration; existing `test_chronicles.py` checks
range separation, off-periods, exact text, closure and persistence safeguards.
Fixtures do not replace observed actual host/source integration.

## Core chronicles

Chronicles are core framework functionality, independent of optional agents or model
profiles. Supply explicit Activity-attributed sources in a workspace JSON request:

```json
{
  "activity_id": "<current Activity UUID>",
  "sources": [{
    "path": "/explicit/saved/session.jsonl",
    "session_id": "<original session UUID>",
    "start_position": 42,
    "representation": "event_msg",
    "enabled_intervals": [{
      "start": {"source_session_id": "<original session UUID>", "source_position": 42},
      "end": null,
      "provenance": "Recording was enabled before this assigned Activity range"
    }]
  }],
  "provenance": {"source": "host assignment", "reason": "record current Activity exchanges"}
}
```

`recording synchronize` previews; `--apply` writes exact eligible saved exchanges
to Activity-local `chronicles/` with a format-1 checkpoint and a core binding/hash
ledger. Position 42 is illustrative. Later requests need only Activity ID and
provenance; source assignments remain fixed. `recording verify` takes only
Activity ID and is read-only, including archived Activities. It freshly checks current eligible source and
recorded artifacts. Preview/verify never creates files. Synchronization with
recording disabled and no independent obligation writes nothing.

Closure synchronizes regardless of prompt cadence and finalizes live assignment
ends at the completed eligible cutoff. The final undelivered acknowledgement is
excluded. New eligible input during closure invalidates freshness. Missing,
rewritten or ambiguous source, edited artifacts and persistence failures preserve
actual partial results and block enabled closure. Exact prior checkpoint/segments
without a core binding ledger remain preserved but require explicit adoption;
there is no implicit legacy migration. Never delete a ledger to retry partial work.

See the [core chronicle contract](../../conventions/chronicles_conv.md),
[transcript format](../../conventions/transcript-segment_conv.md) and
[source adapter](../chronicles/README.md). The source reader extracts text; only
core synchronization writes transcript/checkpoint/ledger files. Host assignment
and cadence remain necessary; no background daemon or after-turn continuation
is assumed.

Independent mandatory recording while the setting is disabled supplies Boolean
`mandatory: true` to synchronize, with the applicable instruction identified in
provenance. The setting itself is preserved. Enablement toggles increment an
internal revision; subsequent synchronization needs explicit reconciled enabled
intervals for every registered source, retaining all previously recorded exchanges.
Cadence-only changes do not reset recording or require interval reconciliation.
Ordinary synchronization does not implement legacy adoption, closed-record
catch-up or prepared-text mutations; those remain explicit maintenance dependencies.
Pending checkpoint work blocks normal refresh rather than being overwritten.
