# Activity agent chat

## Purpose and boundaries

The chat is a shared, persistent coordination channel for agents assigned to an
Activity. Agents leave findings, blockers, questions and handoff information that
other assigned agents can read during later work. Messages are task data, not new
authority or instructions overriding the human, workspace or recipient's role.
There is no automatic notification, agent invocation or background delivery.

Chat does not replace the Activity log, accepted decisions, requirements, plans or
source-backed chronicles. Those retain their existing owners and evidence rules.
Posting a message does not record acceptance, complete a backlog item or authorize
an Activity lifecycle operation.

## File and message contract

Each Activity has its own optional `chat.jsonl` directly in its folder. No global
chat path, toggle, shared cross-Activity file or new state setting is introduced.
A missing file is an empty chat. Reading does not create it; the first applied
post creates it exclusively. Archival moves the file with its Activity unchanged.
The next Activity starts with empty history and a different stable Activity ID.

Each record is one strict UTF-8 JSON object followed by LF. Embedded message
newlines are JSON escapes, not record boundaries. Duplicate keys, nonstandard
constants, blank records, unknown schema fields, unsupported versions, incomplete
records, wrong Activity IDs and repeated/reordered identities are invalid.

| Field | Value |
| --- | --- |
| `chat_format_version` | Integer `1`, excluding Boolean. Independent of state and bundle versions. |
| `activity_id` | The containing Activity's stable UUID. |
| `message_id` | Runtime-generated canonical UUID, unique within the chat. |
| `sequence` | Runtime-generated consecutive positive integer starting at 1. |
| `created_at` | Actual runtime UTC timestamp, `YYYY-MM-DDTHH:MM:SSZ`. Sequence gives append order when timestamps match. |
| `author` | Caller-supplied lower-case agent name or `host-coordinator`, at most 64 characters. |
| `text` | Nonblank message string, at most 65,536 UTF-8 bytes; whitespace and Unicode are retained. |
| `provenance` | Object with nonblank `source` and `reason` strings. |

Author and provenance are attribution supplied by the caller, not authenticated
identity or proof of assignment. The host supplies each assigned agent with the
stable Activity ID, workspace root and its own author name. Core chat does not
require a particular optional agent package, catalogue membership or model profile.

## Operations and append preservation

`activity chat-read` targets one stable Activity ID. It returns messages after
`after_sequence` (default `0`), up to `limit` (default `100`, range `1..1000`),
plus `total_messages`, `next_after_sequence` and `has_more`. The reader validates
the whole file before returning a page. Closed Activity history remains readable
by explicit ID; reads do not mutate files or mark messages as consumed.

`activity chat-post` takes the current stable Activity ID, `author`, `text` and
provenance. It previews without `--apply`; preview IDs/timestamps are not reserved.
Applied posts use the shared runtime lock, validate existing history, recheck
target identity and append a single new record through an append-only descriptor.
Readback checks the exact previous byte prefix and new message. Closed or stale
Activity targets reject posts, including after a new Activity reuses the current
folder path. Use stable IDs, never the folder name as the identity.

The interface exposes no edit, delete, clear or replacement operation. Canonical
artifact edits cannot target the chat. Assigned agents use these operations and
never directly rewrite, truncate, delete or replace its file. Corrections are new
messages that refer to the earlier message ID or sequence.

This preserves existing messages through supported operations. Agents sharing an
operating-system account still have that account's filesystem access; there is no
separate immutable storage service or OS permission boundary preventing a direct
file edit. The runtime does not claim cryptographic tamper detection or sandbox
enforcement. Its schema checks detect structural damage, not all external edits.

A competing runtime writer is blocked before mutation; the existing lock is not
removed. Partial writes or readback failures return changed paths and preserve all
actual bytes without rollback or automatic retry. An incomplete retained record
blocks further posting until an explicitly authorized diagnosis/resolution. Chat
messages do not require a separate log write, avoiding a second-file failure when
the message has already been appended.

## Participation and discovery

An assigned agent reads available messages on entry, before acting on a handoff
and before its final handoff; it posts information relevant to other participants
through the runtime. A resumed participant can retain its last read sequence in
its supplied task context. Reading earlier messages alone grants no action beyond
the assigned task. No per-agent read checkpoint is stored in core state.

Ordinary startup/discovery checks an existing chat's file type and access only.
It does not load chat content, scan message history or imply successful delivery
to an agent. Explicit chat operations validate content. Existing Activities with
no chat remain valid without migration.

## References

- [Runtime commands](../tools/runtime/README.md) — invocation and JSON requests.
- [Activity convention](activity_conv.md) — identity, context and archival.
- [Agent convention](agent_conv.md) — shared participation and host assignment.
