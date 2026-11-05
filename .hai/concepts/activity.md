# Activity

## Definition

[term:Activity] is HAI's independent, persistent unit of substantive work. It connects
human intent, discussion and decisions, performed work, verification and an explicit
outcome, whether the result is understanding, a plan, or implemented changes.

## Purpose

Activities organize all substantive HAI work and preserve continuity across chats
without requiring every conversation to become an implementation project.

## Explanation

### Work continuity

Activity identity connects related work across chats. It is independent of the
conversation boundary, optional product features and the artifact locations of
product code/specification. The environment identifies one authoritative store;
its sole active record is current work. Stable identity survives archival paths,
material revisions and supplements. A new substantive continuation of a closed
subject is a separate linked work unit rather than a revision of past lifecycle.

### Lifecycle, work and outcome

Lifecycle (`active` or `closed`), performed steps and closure outcome answer
different questions: whether work is current, what was actually done, and how its
objective ended. Clarification, analysis, planning, implementation and verification
are independent performed steps, so discussion alone can achieve an objective.
Closure outcomes are `completed`, `cancelled` or `stopped`; closure does not imply
implementation success or automatically follow a final chat response.

### Revision and evidence

Definitions, analyses and plans can evolve after implementation starts. Prior
material versions and their provenance explain which decisions supported earlier
work; revised assumptions can make dependent evidence stale without erasing what
actually happened. The original implementation-start marker is historical fact,
not a freeze on later planning or proof of success.

### Record and product locations

State, preserved initial input and the action log form the minimum persistent
record. Decisions, analysis, plan, outcome and supporting artifacts add meaningful
context when needed; product code and durable specification retain their canonical
product locations. Exact-source chronicles are attributable optional segments,
not a replacement for decision or action records. Closed records can gain dated
attributable evidence and delayed old-source synchronization while remaining
closed to new substantive work.

## Supporting Terms

- [term:activity_id]: stable unique identity retained through revisions, archival and supplements.
- [term:current Activity]: the sole active work record at the fixed current folder.
- [term:supplement]: dated attributable additional evidence attached to a closed record without performing new substantive work under that identity.

## References

- [Activity convention](../conventions/activity_conv.md): canonical artifacts, state schema, revisions, storage and closure.
- [runtime](../tools/runtime/README.md): discovery, record and lifecycle procedures.
- [Environment](environment.md): mandatory configuration and optional features.
- The installed Codex Chronicle-manager owns exact-source recording evidence and pending gaps; missing optional recording support does not invalidate records.
