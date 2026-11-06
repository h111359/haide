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

## Chat verification

Run `python -B -m unittest discover -s .hai/tools/runtime/tests -p 'test_chat.py'`
for isolated fixtures covering shared authorship, exact append preservation,
preview/read behavior, CLI requests, pagination, malformed history, unsafe links,
lock contention, partial writes and archive/new-Activity separation. Tests do not
invoke agents or establish OS-level immutability. Report actual platform and skips.
