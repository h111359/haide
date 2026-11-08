# Clarification dialogue

## Location, identity and ownership

The canonical ledger is `decisions.md` directly inside the validated current
Activity path. Its identity is that Activity's stable UUID plus format version 1.
There is no separate request store, lifecycle or configurable global ledger root.
Existing unrelated decisions content is retained byte-for-byte as a prefix. An
absent or empty ledger means no recorded questions; create no empty scaffold.
The first real question batch creates meaningful ledger content, even before a
proposal. The analyst prepares content; the host serializes writes and core
`activity record` persists it. Analysts/helpers never write runtime-owned files.

Question IDs are Activity-scoped `Q001`, `Q002`, etc., with a minimum width of
three digits and no upper limit. Batches similarly use `B001`, etc. IDs increase
monotonically, are never recycled/reassigned, and remain stable across restarts,
revisions, redisplay and archival. Per-question response numbers start at 1 and
increase by 1. Event IDs are host-supplied stable occurrence identities, not
hashes of wording; equal human text from two actual occurrences remains two
events. No host/source event identity is fabricated when unavailable: retain a
host-assigned durable receipt ID explicitly attributed as such, not as a claimed
source-session position. The host checks saved IDs on resumption before assigning
another receipt. A repeated event ID with identical content is a no-op; different
content is an error. Unknown history is not treated as absence.

## Canonical format

Each append-only event is a `hai-clarification-event:v1` HTML marker, a JSON code
block, canonical human-readable display content, and its closing event marker.
`scripts/clarification.py:render` is the executable format definition; `parse`
verifies the entire display against the event and validates stream identity and
ordering. JSON stores exact strings, including Unicode and raw newline escapes.
The visible question block is exactly:

```markdown
### Q001 — Unanswered

<Full question; its immediately preceding blocker sentence is part of this text.>

Implementation impact: <How the decision affects implementation/acceptance.>

- [ ] A: <Offered option> (Recommended)
- [ ] B: <Offered option>
- Other: ___

Status: unanswered
```

Options use consecutive A–Z labels, every new choice is unchecked, and the
recommendation marker is present only for an explicitly recommended offered
option. Free-text questions can have zero offered choices but retain Other.
All questions carry the complete wording, impact, all offered choices, marked
recommendation when present, free-text placeholder and unanswered status in the
saved block. A batch display includes a compact copyable form:

```text
Q001: A [ ], B [ ], Other: ___
Q002: A [ ], B [ ], Other: ___
```

The saved initial question block remains immutable. Latest status is a projection
over events, not a rewrite of history: `unanswered`, `answered`, or revised
`answered` with the latest effective response ID/number. Redisplaying an existing
unanswered question reuses its verified block and appends no duplicate event.
If the host interface supports fewer questions than the logical batch, split
display into labelled sequential parts using the same saved IDs and wait for
all necessary responses before deciding on another batch.

Every event has `activity_id`, integer `sequence`, unique `event_id`, `kind`,
`author`, `source` and observed UTC `at` timestamp. Kinds and remaining fields:

| Kind | Fields |
| --- | --- |
| `questions` | `batch_id`, nonempty `questions`; each question has `id`, `question`, `impact`, `options` (label/text/checked=false), `recommended` (label or null), `other` (`___`) and `status` (`unanswered`). |
| `response` | `question_id`, `response_number`, exact `raw`, `parts` mapping exact question-part names to verbatim choices/explanations, `supersedes: null`. |
| `revision` | Response fields, but `supersedes` is the latest effective response event ID for this question. Retain all previous responses. |
| `unresolved` | Exact `raw`, `reason`, `candidate_question_ids`; no uncertain answer becomes effective. |

A mapped response additionally has `resolves_event_id` identifying an unresolved
event, exact actual human `mapping_text` and `mapped_question_ids`: the complete
target question set explicitly confirmed by that human mapping. It retains the
original raw answer and identifies the correct candidate question/parts. The
target set stays consistent for that unresolved event; it remains unresolved until
every confirmed target has a saved mapped response, even if those questions have
earlier effective answers. A one-question mapping can select one of several
candidates. The host never infers the target set from a partial answer.
Multipart answers preserve
each part separately plus the complete original raw utterance. If an unresolved
utterance covers multiple questions, the host includes all candidates, persists a
mapped response for each required part, and holds proposal until every mapping
is settled; the analyst checks semantic completeness, not just helper structure.
Do not infer a mapping from interface preselection or wording similarity.

## Host persistence and verification handshake

No new core operation is needed. The supported operation is existing
`activity record`, whose allowlist includes `decisions.md`. It retains exact
predecessors under `files/revisions/decisions/` and appends provenance to the
new artifact. This is host-coordinated append semantics over a versioned artifact,
not a new database or an OS-enforced append-only file.

The host is the sole ledger writer and serializes this whole read/prepare/write/
readback exchange with other Activity writers. It first reads exact current
ledger text, validates its identity/events and captures predecessor bytes/hash.
`prepare` returns only an append-only candidate; it does not write. Immediately
before dispatch, the host rechecks the same predecessor and active Activity UUID.
It persists the full candidate as an artifact with `name: decisions.md`, meaningful
`reason`, attributed `log` and request `provenance`, through:

```text
<absolute-python-executable> -B .hai/tools/hai.py activity record --workspace . --request <workspace-contained-host-request.json> --apply
```

After an actually successful operation, read `decisions.md` again and call
`verify_readback(before, candidate, actual, activity_id, event_id)`. Verify exact
prefix preservation, saved event contents and its complete question blocks/raw
answer. Runtime's appended revision-provenance line remains in the prefix for
the next append. Allocation, preview, staged files and a successful invocation
without content readback are not persistence evidence. The host displays only
verified saved question content, applies only verified actual human responses,
and checks latest effective decisions again before proposal/handoff.

The core operation does not accept an external expected-ledger hash. If the host
cannot serialize the full exchange or ensure predecessor/readback verification,
report unavailable safe persistence and hold dependent work. Do not silently
weaken this requirement or infer concurrency guarantees from the runtime lock.
On unavailable capability or read/write/readback failure report the exact ledger
path and underlying error, stop dependent question display, answer application
and proposal, retain partial writes, and do not automatically retry/repair.
Independent authorized diagnosis may continue. Raw answers awaiting persistence
remain pending and must not be applied.

## Lifecycle

The analyst never clears, resets, deletes or archives the ledger. Later analysis,
input preparation, revisions and retries retain it. Only authorized core Activity
closure/archival moves it, its revision history and supporting files together.
The host verifies ended writers and all applicable closure gates. Dialogue is an
attributable decision record, separate from core exact source-backed chronicles;
it establishes no transcript coverage or permission to close.
