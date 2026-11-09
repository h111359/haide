# Synchronize chronicles

## Description

Synchronize explicitly assigned, completed Codex source exchanges into Activity-local chronicles under the [chronicles convention](../conventions/chronicles_conv.md).

## Inputs

A valid workspace and instructions, an existing stable Activity ID, actual authority, the recording requirement, and explicit source assignment and enablement provenance are required. For each initial source supply its canonical authorized path, session ID, inclusive start position, optional inclusive end position, explicit `event_msg` or `response_item` representation and enabled intervals with source occurrences and attributable provenance. A null interval end means enablement continues. Establish new current-session identity through [bounded discovery and binding](establish-recording-source.md); the synchronizer itself does no discovery. Resolve ambiguous/conflicting attribution before writes; never infer historical import authority or reconstruct text.

## Steps

1. Resolve the recording requirement. When disabled without an independent obligation, return disabled without recording writes. Otherwise validate the Activity, store, explicit sources, assignment, target types and sole mutation ownership.
2. Submit `recording synchronize --request` with a JSON request such as:

```json
{"activity_id":"ACTIVITY-UUID","sources":[{"path":"/explicit/session.jsonl","session_id":"SESSION-ID","start_position":0,"end_position":null,"representation":"event_msg","enabled_intervals":[{"start":{"source_session_id":"SESSION-ID","source_position":0},"end":null,"provenance":"attributable enablement boundary"}]}],"provenance":{"source":"source assignment authority","reason":"synchronize current Activity"}}
```

Initial synchronization requires explicit bindings. Later source-less synchronization can reuse registered bindings. A live source has no end position or a null end. Closure synchronization finalizes its assignment end at the completed eligible closure cutoff to prevent overlap with later Activity ranges. The host schedules this operation on the configured prompt cadence and synchronously before closure regardless of threshold.
For an independent mandatory workspace obligation while the setting is disabled,
also supply Boolean `mandatory: true` and identify that instruction in provenance.
This explicit obligation permits core synchronization without changing the setting.
3. Inspect actual results and readback coverage. Report missing or malformed source, pending outcomes, unsafe or divergent artifacts, unsupported legacy checkpoint/ledger state, conflicts and partial writes without automatic repair or retry. Never infer saved text from proposed output. Preserve prior contents and unresolved gaps.

## Outputs

Actual segment paths, source identities, verified occurrence boundaries, checkpoint and pending or blocked status; disabled status without writes when applicable. A successful dispatch or cursor is not coverage evidence.

## References

- [Chronicles](../conventions/chronicles_conv.md), [source](../conventions/codex-source_conv.md), and [segments](../conventions/transcript-segment_conv.md).
- [Runtime commands](../tools/runtime/README.md).
