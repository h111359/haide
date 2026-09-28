# Workspace administration clarification — 2026-09-27

## Authority and supersession

During the requirements review, the user explained that workspace configuration is expected to change rarely after initial setup and that changes should happen between requests. The user accepted the proposed simplification and instructed: “Yes. Make the needed changes in the requirements. Review the decisions.md and context.md files as well and check if this resolves some of the unresolved.md issues”.

This clarification supersedes the earlier build source's option A allowing workspace changes during an idle but open request, and its requirements for workspace configuration revisions and historical location mappings. Other requirements remain applicable.

## Accepted policy

- Human workspace changes are allowed only when no request is open and no operation is active. Blocked, stopped, and Ready to close requests remain open.
- Operations use the current validated workspace configuration. Agents cannot change workspace membership or expand their own access.
- Direct human configuration edits follow the same timing and validation rules. An external edit does not silently change execution authority or bypass the gate.
- After workspace changes, affected documentation, dependencies, and required test coverage are reviewed before starting the next request. Saving settings does not automatically launch that work.
- Historical request records, documentation history, test obligations, and unresolved defects are retained. A separate history of workspace configurations, revision identifiers, and historical folder-location mappings is not required.
- Stable folder IDs and relative paths remain useful for file references. Historical records do not grant access to removed locations or prove that content at a new location is unchanged.
- Stale-save detection, recoverable configuration updates, current access checks, and source/content version checks remain required; these do not require a permanent configuration-version archive.

## Consequences

A request that needs a workspace change must first be closed or cancelled under the existing lifecycle rules. Merely stopping execution is insufficient. Historical records can retain their original information, but AIH need not reconstruct every past filesystem location.

The open-request workspace-reconciliation exception discussed in unresolved issue 4.1 is superseded. That issue's additional documentation UI choices remain unapproved. Issue 5.1's workspace timing is settled by this clarification, while its other proposed settings details remain unresolved.
