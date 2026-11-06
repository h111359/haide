# BL-0001 — Activity agent chat

## Objective

Provide a persistent Activity-specific coordination chat that all assigned agents
can read and append to. Existing messages have no edit/delete runtime operation.
Messages do not replace exact user/assistant chronicles or canonical Activity artifacts.

## Design and implementation

1. Add activity chat-read and chat-post commands with stable Activity ID targeting.
   Store attributed UTF-8 JSONL messages in Activity-local chat.jsonl, using runtime
   generated UUID/sequence/time and supplied author/text/provenance.
2. Make chat-post preview by default and append only under the shared runtime lock.
   Strictly validate existing messages and identity, reject unsafe linked targets,
   use append-only descriptor writes without replacement/truncation, preserve and
   report partial writes, and expose no edit/delete/clear action.
3. Permit read-only history after Activity archival, reject posts to closed or stale
   Activities, and lazily initialize each chat on first post. New Activities start
   with empty independent history. Bound read output with sequence pagination.
4. Document format, commands and shared agent participation rules. Startup checks
   only optional chat file type, not full message history. No optional package or
   state migration is required. Direct filesystem access is not a distinct security
   principal; runtime append-only behavior does not establish OS immutability.
5. Test author sharing, exact append preservation, preview/pagination, malformed
   records, links, partial writes, lock contention and archive/new-Activity separation.
   Run existing runtime/startup regressions and demonstrate the live chat.

## Acceptance evidence

- Multiple assigned agent identities can post/read the same Activity chat.
- Runtime operations append without modifying existing message bytes and reject
  edit/delete requests; agent instructions prohibit direct rewriting/deletion.
- Archives retain readable history; a fresh Activity has no previous messages.

No commit, Activity closure or backlog terminal decision is inferred from this task.


Revision provenance: source: User: Now work on BL-0001; backlog item BL-0001; reason: Track authorized feature implementation; reason: Implement requested shared Activity chat and verify acceptance criteria; recorded 2026-11-06T05:38:40Z.
