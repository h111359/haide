# Mandatory pre-delivery recording

## Description

Host procedure for an independent mandatory instruction that explicitly requires recording the exact final response before delivery. This is an exception to saved-source recording, not an automatic source or a claim that delivery has occurred.

## Inputs

The applicable instruction and authority, validated Activity and assigned source context, sole mutation ownership, and the exact resolved final text are required. If they are unavailable, return the blocker without inventing content.

## Steps

1. Synchronize preceding eligible completed saved source and resolve gaps or unsafe placement before preparing an entry.
   The ordinary core CLI records saved exchanges only; it does not implement a
   prepared-text mutation or reconciliation operation. If no verified maintenance
   implementation is available, return this specific capability blocker before
   appending anything. Do not bypass core ledger/checkpoint integrity by hand.
2. Recheck Activity identity, assignment, segment contents and placement. Append the identical final text as explicitly prepared, then read it back and record pending reconciliation separately from verified saved-source coverage. Preserve gaps and partial results; never silently repair or retry.
3. Deliver only the identical verified text. Reconcile it against the later actual saved outcome without duplication. A missing, differing or reordered saved outcome remains pending or blocked for explicit resolution. This procedure does not cause an unsaved response to become a durable source or authorize a domain operation.

## Outputs

Identical verified prepared delivery text and actual recording status, or an explicit blocker/partial result. Do not claim that the prepared entry is an already saved or delivered outcome.

## References

- [Chronicles](../conventions/chronicles_conv.md) and [transcript segment convention](../conventions/transcript-segment_conv.md).
