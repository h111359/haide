# Requirements clarification (draft)

Activity: `5f99ff6b-793b-475e-b184-8618582598ef`. Updated from user answers and read-only Business-analyst reviews on 2026-11-04. Acceptance criteria remain draft for architecture review; they do not approve implementation. The prior draft is preserved byte-for-byte at `files/revisions/requirements/20261104_020249_01.md`.

## Accepted requirements

- HAI remains the coordinator and initializes an absent `.hai_env` environment.
- `.hai` is a shared runtime/protocol location without built-in Leader or Environment-manager agent definitions. Local agent collections and configuration belong in `.hai_env`.
- HAI and external agents use a small integration contract; specialist behavior stays external.
- Fully support Codex first while designing the runtime to accommodate additional hosts.
- Each invocation gets its own Activity-local run notebook. Invocations start with fresh context; HAI may provide explicit references to other runs. A coordinator run has a notebook, and a new Activity gets fresh notebooks. Durable cross-Activity knowledge belongs in specification/product.
- Agents may directly update specification/product when the work fits their definition and assigned scope.
- Missing token telemetry never blocks work; record unavailable usage as unknown, not zero.
- Transcript content includes user/assistant messages, with tool activity in linked logs. Hosts with incomplete source access are supported; preserve available messages and report limitations. Activity closure must not wait for transcript sync.
- Existing `.hai_env` upgrades occur only when explicitly requested and preserve configuration, agents, Activity history, and transcript evidence.
- When the same Activity continues in another chat, create a new linked coordinator notebook and explicitly select carried-forward context.
- Preserve both contributions to conflicting shared edits, resolve conflicts before affected work is declared complete, and ask the user only for new business decisions.

## Draft acceptance criteria

1. The same `.hai` runtime supports different `.hai_env` agent collections through a small HAI integration contract, keeps specialist behavior external, has no built-in Leader/Environment-manager definitions, and keeps local configuration in the environment.
2. HAI initializes a missing environment while preserving existing content.
3. Every invocation has a separate Activity-local run notebook for assignment, actions, decisions, collected information, results, and observed token usage where available.
4. Each invocation starts with fresh context; prior run material is supplied only through explicit HAI references.
5. HAI has a coordinator notebook, each new Activity starts fresh run notebooks, and durable cross-Activity knowledge lives in specification/product.
6. An agent may edit product/specification directly when its definition and assignment permit the work.
7. Unavailable token telemetry does not block execution and is recorded as unavailable, not zero.
8. Transcripts preserve user/assistant messages where available, link tool logs separately, report host source limitations, and never delay Activity closure.
9. An existing `.hai_env` is upgraded only on explicit request, preserving configuration, agents, Activity history, and transcript evidence.
10. Continuing the same Activity in another chat creates a new linked coordinator notebook with carried-forward context explicitly selected.
11. Conflicting agent contributions are both preserved; affected work is not declared complete until conflict resolution. HAI handles routine choices and asks the user only for new business decisions.

## Business-analyst gap assessment

The Business-analyst found no fundamental business ambiguity requiring another clarification round; requirements are ready for architecture exploration. This is not implementation approval.

## Remaining design choices

Detailed run schemas, within-chat invocation boundaries, host adapters, transcript capture/recovery, upgrade mechanisms, and conflict detection remain design choices. They are not approved implementation mechanics.
