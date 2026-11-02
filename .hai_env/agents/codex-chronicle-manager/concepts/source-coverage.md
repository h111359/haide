# Source coverage

## Definition

[term:Source coverage] is the exact completed-source exchanges verified in a segment, including its assigned start/end boundary and last synchronized message.

## Purpose

State verified synchronization precisely without claiming future, unsaved or excluded messages.

## Explanation

Coverage records what exact saved source has been verified. A cadence cursor means
which prompt occurrences were observed at batch dispatch. It is scheduling progress,
not evidence that the batch succeeded. A newer successful range or timestamp does
not fill an earlier source gap. Pending outcomes and missing retained source remain
separate from the count of new prompts.

Enabled intervals distinguish eligible source from off-period messages. Disabling
preserves existing gaps and files; it does not itself authorize historical backfill.
The enabled-recording closure prerequisite applies when recording is currently
enabled or independently mandatory. Disabled/no-obligation closure has no transcript
prerequisite, while existing gaps remain part of the historical recording status.

A closure cutoff includes completed saved source through the user's closure
request. The final closure acknowledgement is not yet delivered, so it is outside
that pre-closure cutoff and can later belong to the original closed Activity.
Prepared pre-delivery text is a separate exception, not evidence of future saved
source. This distinction avoids requiring an operation to record its own future
acknowledgement before it can finish.

## Supporting Terms

None

## References

- [term:Transcript segment] → [Transcript segment](transcript-segment.md) — assigned range.
- [term:Durable session source] → [Durable session source](durable-session-source.md) — authoritative completed text.
