# Codex durable source adapter

## Explicit source and identity

This package targets Codex saved JSONL sessions. Leader supplies one explicit
authorized canonical regular source file, original session ID/start time, chosen
representation and assigned source occurrences. The adapter never searches the
Codex home, unrelated sessions, conversation history or the source library.
Missing source or unsupported saved schemas remain explicit blockers; human or
assistant text is never reconstructed from memory, tool output or proposed work.

The read-only adapter accepts strict UTF-8 JSONL with a `session_meta` record
whose payload has nonblank `id` and original `timestamp` (or the recorded outer
timestamp if the payload field is absent). Duplicate keys and conflicting session
metadata are rejected. Each complete message has an actual outer UTC timestamp.
The normalized identity is `source_session_id` plus the physical zero-based
JSONL `source_position`; payload `id`, if present, is returned separately as
`message_id`. Stable physical source positions are usable only while the original
source has not been rewritten; changed/divergent history blocks synchronization.

## Supported representations

Leader explicitly chooses one representation for the source/segment and retains
it in source provenance. The reader never combines duplicate event and response
representations or deduplicates identical text.

| Representation | Eligible saved records |
| --- | --- |
| `event_msg` | `payload.type: user_message` with string `message`; `payload.type: agent_message` with string `message` and `phase: final_answer`. |
| `response_item` | `payload.type: message`, `role: user` with ordered `input_text`/`text` blocks; `role: assistant` with `phase: final_answer` and ordered `output_text`/`text` blocks. |

Text blocks concatenate without inserted separators; decoded text, Unicode,
whitespace and Markdown are preserved. Commentary/analysis assistant phases,
tool calls/results, reasoning, system/developer instructions, turn context and
environment metadata are excluded. Unknown/missing assistant phase is ambiguous
and blocks completed-coverage claims rather than treating progress as a final
outcome. Unsupported message content, malformed/truncated JSONL and changed source
during reading also produce explicit incomplete status. This conservative subset
does not claim to support every historical or future Codex schema.

## Boundaries and evidence

The adapter only extracts completed saved text and occurrence metadata. It does
not assign an Activity, authorize imports, advance coverage/checkpoints, write
transcripts, schedule work or decide operation success. Assignment, eligibility,
cross-Activity overlap and exact existing segment comparisons remain the owner's
procedure responsibilities. A prepared pre-delivery response remains the separate
mandatory-timing exception until reconciled with an actual saved delivery.

Output includes original session identity, normalized messages and source byte
SHA-256. It returns precise issues with `ok: false` if source interpretation is
incomplete; preceding readable messages do not erase the gap. Before writes and
closure proof, reread the explicit source and recheck identity, stable occurrences,
contents and boundaries. A fingerprint alone proves neither retained-source
completeness nor coverage. Existing generic transcript/checkpoint formats stay
unchanged; Codex-specific provenance belongs in source metadata.
