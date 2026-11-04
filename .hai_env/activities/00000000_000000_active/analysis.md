# Activity analysis: invocation runs and coordinator

## Revision provenance

Environment-manager revised this analysis on 2026-11-03T20:13:13Z using the user's follow-up and the actual focused read-only proposal from registered agent-definition-manager. The prior version is preserved byte-for-byte at `files/revisions/analysis/20261103_201313_01.md`. This revision records the user's clarification that HAI remains a leader/coordinator and bootstraps `.hai_env`; implementation remains unauthorized.

## Attributed specialist proposal

The specialist proposes that HAI coordinate bootstrap and invocation through shared procedures, schemas, templates, and tools, while agent definitions remain external and use a minimal invocation contract. Each dispatch, follow-up, or retry would receive a distinct linked run under its Activity; host sessions would retain separate identities. The coordinator itself could be recorded as a runtime run without a named Leader definition. New Activities start with fresh runs; prior runs are brought forward only as explicit context.

A candidate run notebook includes `run.json`, `assignment.md`, `notes.md`, `actions.jsonl`, `result.md`, `usage.json`, and `artifacts/`; `decisions.md` may be separate. Coordinator owns intake/run metadata, executor owns notes and results, and a host telemetry collector supplies usage. Record observed events, not hidden reasoning. Make usage source and coverage explicit; record input/output/cached tokens only when reported; avoid cumulative or child-run double counting. Preserve failed runs. Promote knowledge into specification/product only explicitly within task scope; do not accept notebook notes automatically.

## Questions and remaining choices

1. What defines a coordinator run: one chat, user turn, or Activity?
2. Should follow-ups and retries link to a previous run, and how should cross-host linkage work?
3. Which earlier notebooks may a new run see?
4. How should concurrent runs coordinate edits to shared product or specification files?
5. Is token usage available from every supported host, or must the field support unavailable/partial coverage?

This is a brainstorming proposal, not an approved design. No `agent_runs` structure or runtime behavior has been implemented. The Activity remains analysis-only with implementation unstarted.


## Transcript synchronization exploration — 2026-11-03T20:29:33Z

### Attributed read-only specialist proposal

Registered `agent-definition-manager` recommends a deterministic transcript service with host adapters: capture completed message events and reconcile them incrementally with the durable source; provide explicit export/import fallback, while keeping summaries distinct from exact transcripts. Treat the canonical record as an exact message-event stream, with readable Markdown derived from it, stable source/occurrence IDs, and committed checkpoints for idempotence. Attribute source ranges to Activities/runs and use explicit references instead of copying entire chats into each run. Keep action and usage logs separate.

Use after-delivery hooks where available; otherwise sync on the next invocation/startup or explicit flush. Do not promise unsupported background sync. Missing source should not block normal work.

### Unresolved choices and current limit

1. Should the transcript contain only user/assistant messages, with tool actions in linked logs? The specialist recommends this.
2. Should incomplete-transcript closure policy be configurable with a nonblocking default? This would change the current strict closure rules and is only a proposal; no policy was changed.

The current Chronicle adapter requires explicitly authorized Codex JSONL. No authoritative source was identified for this chat, so exact transcript synchronization remains pending. No synchronization or implementation was performed.


## Closure without transcript loss — 2026-11-03T20:37:22Z

### Attributed read-only specialist proposal

Registered `agent-definition-manager` proposes separating a durable capture journal/outbox from transcript rendering. Keep stable Activity, run, and source IDs; retain queued capture across closure, archive, and restart; retry idempotently; advance checkpoints only after a durable, verified write; and keep source material until the target is verified or retained. Closed Activities can receive assigned transcript catch-up without reopening. Capture the final reply after actual delivery.

Retry through supported delivery hooks, startup/next invocation, or explicit flush; do not promise unsupported background work. Missing transcript material should not block ordinary closure. Distinguish recoverable captured messages from gaps where the host never exposed or saved a source. Replay durable host history when available. HAI cannot guarantee zero loss across an unavailable capture boundary.

This is a proposal, not an approved mechanism or changed closure policy. Exact source synchronization for this chat remains pending.


## Business-analyst clarification review — 2026-11-03T20:44:38Z

Registered Business-analyst (`gpt-6.1-sol`, high reasoning) completed a read-only requirements review after the user asked for clarification. The compact draft accepted requirements and draft acceptance criteria are in `requirements.md`; specialist priority and deferred questions remain open. The review corrected the attribution of answer 4: it answered nonblocking missing token telemetry, not concurrent edits. An attributable correction is appended to `decisions.md`; the earlier mistaken entry remains visible as historical text. Requirements and mechanics beyond the user's settled constraints remain draft/proposals. No implementation or tests were performed.


## Human-readable plan format proposal — 2026-11-04T02:25:42Z

The user asked for clearer phase order, affected files, and concise human-readable formatting. Registered `agent-definition-manager` provided this read-only proposal; it is not adopted framework policy:

- Begin with an overview table showing each phase, dependencies, and result. Use the same goal/dependencies/actions/files/checks structure for every phase.
- Number phases and actions in execution order. Give each bullet one concrete action and verb.
- List exact repository-relative paths in concise `Path / Change / Purpose` tables. Label each file `Add`, `Edit`, `Move`, `Delete`, or `Proposed`; separate large inventories from phase descriptions.
- State observable completion checks. Keep prose to two or three sentences, prefer bullets/tables, explain unfamiliar terms at first use, and distinguish agreed items from proposals and open questions.

Leader may propose a tighter presentation guide: paragraphs up to two sentences and 40 words, with bullets usually one sentence. This is presentation guidance only; it makes no technical design change. The existing `plan.md` remains unchanged pending the user's response.


## Explain phases and steps before asking the user to review — 2026-11-04T03:08:47Z

The user asked for plan-generation rules that make each phase understandable without repeated explanation, after asking what Phase 2 aims to do. Registered `agent-definition-manager` provided this read-only proposal; it awaits user approval and does not alter the current plan or prior readability rules:

- Add an explain-before-actions requirement. For each phase, state in plain language what it does, why it happens at that point, and what visible result it produces. Explain dependency reasons, not only phase IDs.
- Tie each phase to a bounded concrete scenario, the minimum scope reused from earlier work, and later work it enables. For each step, use `Step / Action / Purpose or expected result`.
- Explain essential terms where they first appear. Give inspectable completion checks and a separate affected-file inventory. Use before/after examples where they clarify a change; keep wording concise.
- Example for Phase 2: use a temporary workspace to demonstrate one sample Activity, a coordinator and one fresh-context agent task, saved notebook/results/available usage, and closure with transcript sync still pending. This is an early integration check before broader runtime extraction or migration, not a technical redesign.

No readability rule has been adopted as framework policy. The current reformatted `plan.md` and Solution-architect definitions remain unchanged pending the user’s decision.
