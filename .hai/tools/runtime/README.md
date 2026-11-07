# HAI runtime

Run `python -B .hai/tools/hai.py startup --workspace .` for core environment and Activity context. Common options may precede or follow the group. Commands emit JSON with `ok`, `status`, `operation`, `result`, `changed_files`, and `issues`. Exit codes are 0 for success or a valid plan, 1 for blocked, partial or unsupported work, and 2 for invalid invocation. Optional registration and model profile issues are reported separately from core environment validity.

Use `--request PATH` for a UTF-8 JSON object within the workspace. Duplicate keys and nonstandard numeric constants are rejected. Mutations are previews by default; add `--apply` to perform them. Mutation requests include `"provenance": {"source": "...", "reason": "..."}` with nonblank values. A pre-existing `.hai_env/.runtime.lock` blocks writes and requires inspection; do not remove an unexplained lock automatically. Partial results identify paths that were changed and must be inspected before another attempt.

- `environment initialize`: provenance only; creates absent state and missing instructions, preserving existing instructions.
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
- `activity create` takes `initial_input` and provenance. `activity record` takes `activity_id`, optional `steps` mapping step names to statuses, optional `implementation_start` Boolean, optional `artifacts` array of `{name, text, reason}`, optional `input_append`, `log`, and provenance. `activity close` takes `activity_id`, `outcome`, `archive_label`, `outcome_text`, `recording` with `status` and `details`, and provenance. It also accepts `recording_requirement` with Boolean `enabled` and `mandatory`, and a `recording_proof` gate request. Verified closure additionally supplies `recording_paths` with `sources` mapping source IDs to workspace-relative files and `artifacts` mapping artifact IDs to files inside the Activity; their hashes must match the gate evidence. `activity supplement` takes `activity_id`, `text`, and provenance. Closure requires valid proof when recording is mandatory; pending or unavailable optional recording is reported. These operations preserve partial results on failure.
- `packages validate` takes `definition`; `packages resolve` takes `definition` and `runtime`, a capability snapshot shaped as `{"models":{"model-id":["high"]}}`. `packages audit` takes `{}`. `packages install` takes workspace-relative `source`, `name`, provenance, and optional Boolean `replace` and `register`. Replacement additionally requires the exact `reviewed_differences` list returned by a preview; the previous package is retained as a backup. Registration may require a separate reconciliation after replacement. `packages register` takes `name` and provenance. Remote acquisition is unsupported. Safe no-overwrite package and Activity moves require an available native atomic rename primitive. Implementations cover Linux, Windows and macOS; only Linux has been tested here.
- `recording status` takes `{}` and reports the configured flag, threshold, and available evidence. `recording schedule` takes `occurrence_ids`, optional `covered_ids`, optional positive integer `threshold`, and optional `last_dispatched_count` for the previously dispatched observed count. It reports gaps and whether dispatch is due; it does not persist a checkpoint or start a background task. `recording assess-closure` accepts the structured request defined by the recording gate helper. Runtime does not infer saved transcript coverage.
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
