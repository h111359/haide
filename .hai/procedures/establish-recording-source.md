# Establish recording source

## Description

Establish current-session source identity and an attributable Activity work range
before work that requires chronicles, without reconstructing any exchange.

## Inputs

Valid core context and readable instructions, the recording requirement, current
Activity UUID, authoritative host session ID, optional canonical source path,
observed saved first work-prompt position, enabled intervals and provenance.

## Steps

1. Inspect `recording_context` from primary runtime startup. Core validity remains
   independent. Optional disabled/no-obligation recording needs no lookup or
   binding. Independent mandatory recording supplies `mandatory: true` plus the
   applicable instruction's provenance to discovery/binding commands.
2. Run `recording discover` read-only for an unbound source. It uses
   `CODEX_THREAD_ID`, falling back to `CODEX_SESSION_ID` or an authoritative
   supplied `session_id`. A participant can inherit its parent's session ID;
   a supplied ID must match the selected current-thread identity. Missing current
   host identity cannot establish startup readiness from prior bindings alone.
   Prefer `source_path`; otherwise search exact-ID filenames only under
   `codex_home/sessions`, `CODEX_HOME/sessions` or `~/.codex/sessions`. Embedded
   identity/workspace, source schema, safe paths and a stable read are checked.
   The default representation is `event_msg`. When that representation has no
   saved user occurrence (as on some participant surfaces), explicitly select a
   supported representation such as `response_item`; never guess or merge them.
   Zero/multiple matches or invalid evidence stop binding; do not select by
   recency, broaden the search to unrelated sessions or reconstruct source text.
3. Identify the actual saved first user occurrence assigned to the Activity from
   its host turn/source. The result's `latest_user_occurrence` is diagnostic and
   does not infer an existing Activity's range. An empty scaffold created during
   earlier closure starts at its later first work prompt. Timestamps/text
   similarity cannot resolve an ambiguous occurrence. Attribute enabled intervals
   to actual settings/history and preserve off-period gaps.
   Some participant user records contain only environment context; they are not
   work assignments. Never bind such a record merely because its role is user.
   For delegation stored as native inter-agent metadata, the coordinator verifies
   the actual assignment record's identity/author/recipient and position, then uses
   existing `recording synchronize` with that explicit range. Keep the chosen
   representation's eligible final outcomes; do not turn inter-agent tool records
   into invented human prompts. Return an unknown boundary if not verifiable.
4. For an interactive saved work prompt, submit `recording bind` with Activity ID, explicit `start_position`, enabled
   intervals, source hints and provenance. Preview is read-only; `--apply` uses
   core synchronization. Inspect actual results/readback and return partial
   failures without cleanup or automatic retry. Pass returned `usage_source`
   separately to `activity usage-update` for attributable usage without invented
   counters/rates/charges. For native delegation, use the explicit synchronization
   path described in step 3 instead of interactive binding; register the same
   verified path/session/start separately for usage. No optional specialist is required.
5. Resume existing bindings rather than assigning a new range for each turn/chat.
   Additional participant sessions need explicit sources. Changed enablement
   requires explicit interval reconciliation. Retain malformed/partial history
   for diagnosis; never reset it or implicitly adopt legacy state.
6. Collect saved outcomes at the next active turn and honor prompt cadence. Use
   an after-delivery hook only when actually supplied by the host; no background
   task or unsaved future final response is assumed. Synchronize and verify
   synchronously before every commit and closure.

## Outputs

Actual resolver metadata, registered source/range and verification evidence, or
an actionable readiness blocker. No reconstructed text or blanket historical
import authority. Discovery, preview and startup are read-only.

## References

- [Chronicles](../conventions/chronicles_conv.md) — authority and integrity.
- [Source adapter](../conventions/codex-source_conv.md) — exact representations.
- [Runtime commands](../tools/runtime/README.md) — requests and operations.
