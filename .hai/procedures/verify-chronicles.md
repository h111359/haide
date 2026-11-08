# Verify chronicles

## Description

Read-only fresh verification of assigned source coverage and recording status for an Activity.

## Inputs

A validated workspace, Activity ID, recording requirement, explicit registered bindings and authorized source access. Verification never invents missing source or assignment boundaries.

## Steps

1. Resolve the current recording requirement and ensure relevant writes have stopped. For enabled or independently mandatory recording, synchronize first through the completed operation cutoff; closure synchronizes registered sources itself.
2. Run `recording verify --request` with `{"activity_id":"ACTIVITY-UUID"}`. Verify relevant assigned source and segment coverage afresh, including earlier pending ranges and all enabled intervals, rather than trusting a cursor or earlier result.
3. Return exact coverage, fresh evidence, disabled/no-obligation status or precise gaps, conflicts, pending source, unsafe artifacts and partial status. Verification itself does not write. Required missing or pending evidence blocks closure; do not require the future undelivered closure acknowledgement.

## Outputs

Fresh source-backed verification or an explicit blocker, with no transcript or checkpoint writes by verification.

## References

- [Chronicles](../conventions/chronicles_conv.md) and [recording evidence](../conventions/recording-evidence_conv.md).
