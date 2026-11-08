# Commits and local changes

## Description

Create scoped commits or exact-commit source exports under the applicable gates, and return verified source identity, contents, and remaining repository state.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:operation_context] | Verified operation target, gates and authority | Mandatory | Operation workflow result | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:commit_scope] | Requested paths/hunks and reviewed candidate; or exact export source and paths | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:recording_verification] | Fresh `recording_verification` from the recording owner for this planned operation, relayed through host coordinator | Optional | Caller or authorized context | Obtain fresh verified status before commit-producing work; export-only work needs none. |
| [input:commit_message] | Supplied commit message or established project conventions | Optional | Caller or authorized context | Use a clear descriptive message following established project conventions. |

## Prerequisites

Verified `operation_context` output from [Operation workflow](operate.md), supplied as [input:operation_context]. Explicit reviewed commit/export scope; commit-producing work additionally requires fresh operation-specific [input:recording_verification].

## Rules

- **Reviewed staging:** Git-manager MUST limit a commit to reviewed task paths and hunks.
- **Unrelated staged changes:** Git-manager MUST NOT silently commit or unstage unrelated pre-existing staged changes.
- **Inclusion decision:** Git-manager MUST resolve an inclusion conflict through an agreed isolation method or caller decision before committing.
- **Per-operation recording:** Git-manager MUST obtain fresh recording verification for every planned commit-producing operation, including amend, pull/merge, rebase, cherry-pick and GitHub merge.
- **No reused verification:** Git-manager MUST NOT reuse an earlier completed operation's recording verification for a new operation.
- **Multiple commits:** Git-manager MUST recheck recording freshness before each subsequent commit in a multi-commit operation.
- **Invalidated coverage:** Git-manager MUST obtain fresh verification when new completed exchanges or relevant candidate/transcript changes invalidate previous coverage.
- **Automatic commits:** Git-manager MUST NOT let automatic commit creation bypass a required verification pause.
- **Accepted verification:** Before a commit, Git-manager MUST have fresh verification that the required completed saved source is recorded, or fresh confirmation that optional recording is off and no recording obligation applies.
- **Mandatory recording:** Git-manager MUST follow any mandatory recording requirement that applies even when optional recording is off.
- **Future source exclusion:** Git-manager MUST NOT require future commit results or undelivered final messages to verify already completed source.
- **Actual operation evidence:** Git-manager MUST NOT present proposed details as completed `operation_evidence`.
- **Transcript placement:** Git-manager MUST include the verified transcript segments that belong in the repository and planned commit.
- **Recording or inclusion blocker:** Git-manager MUST block a commit for ignored/outside-repository inclusion, missing required source, divergence, partial recording or unavailable required verification until resolved or covered by an explicit operation-specific human exception.
- **No forced inclusion:** Git-manager MUST NOT force-add excluded transcript segments to satisfy inclusion.
- **Unchanged commit files:** Git-manager MUST NOT silently change the agreed commit files to resolve a recording problem.
- **No silent recording setup:** Git-manager MUST NOT silently enable recording to resolve a recording problem.
- **No inferred exception:** Git-manager MUST NOT infer an exception to recording requirements from permission to commit.
- **Export identity:** Git-manager MUST tie export bytes to the full verified commit and requested tracked paths.
- **No source substitution:** Git-manager MUST NOT substitute working-tree bytes or an uncommitted manifest for the declared committed export source.
- **Separate push request:** Git-manager MUST NOT infer a push request from a commit request.

## Steps

1. Inspect HEAD/status/index and relevant diffs under [input:operation_context] and [input:commit_scope]. If the request is export-only, continue at step6 and skip commit steps2–5. Otherwise stage only reviewed paths/hunks; if unrelated staging would enter, return an isolation/inclusion decision before proceeding. Select the supplied [input:commit_message] or a descriptive project-convention message.
2. For each planned commit-producing operation, resolve the current recording requirement. With verified disabled/no-independent-obligation recording, retain that result without requiring a source. Otherwise return the explicit Activity/source assignment and completed-source boundary to host coordinator for core `recording synchronize`, then request fresh synchronous [chronicle verification](../../../../.hai/procedures/verify-chronicles.md). Missing source or failed verification blocks this dependent operation. Core recording needs no optional agent registration, package or model profile. Supply actual completed operation evidence only when available; do not record a proposed commit or message as completed.

3. Receive the recording owner's `recording_verification` as [input:recording_verification] through host coordinator. Check operation identity, freshness, Activity IDs, segment paths, source identity and completed-source boundary or verified disabled/no-obligation status. A fresh finding of no new eligible text is sufficient. If coverage/inclusion is unresolved, return the exact blocker or explicit-exception dependency.
4. Recheck candidate/index and applicable transcript bytes; include verified segments only within the intended repository scope. Review accidental secrets and relevant checks; run normal hooks/signing and create only the reviewed commit. If the operation has multiple commits, repeat the freshness check and return for another synchronous verification whenever invalidated; if the tool cannot pause, stop dependent commit creation and report it.
5. Verify resulting commit identity, paths/message and remaining index/worktree state. Return actual commit identity/message/paths/checks/state through host coordinator as target `operation_evidence` for later source-backed recording catch-up; no future response or result is fabricated.
6. For export-only work, verify the full commit and requested tracked paths, create its exact source snapshot, inspect contents and report location/identity. No recording obligation is invented for export-only work.
7. Return [output:commit_or_export] with observed source/state/check evidence and unresolved inclusion/recording/export limits.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:commit_or_export] | Verified commit identity and remaining state, or exact-commit export identity/location/contents | Only reviewed scope committed with normal hooks; export matches exact full commit. Gate, checks and any blocked inclusion reported. |

## References

- [Role rules and references](../SKILL.md) — gates, authority, safety and applicable sources.
- [Agent convention](../../../../.hai/conventions/agent_conv.md) — receiver checks and host coordinator-only routing — required for all tasks.
- [State convention](../../../../.hai/conventions/state_conv.md) — generic core-state envelope and preservation requirements — required before extension configuration writes.
- [Startup helper](../../../../.hai/tools/startup/README.md) — core environment assurance only; it does not validate extension settings — conditional when interpreting core helper output.
- [Tooling convention](../../../../.hai/conventions/tooling_conv.md) — Python runtime and helpers — conditional when executing or changing supporting Python tools.
- Current installed tool help and official Git/GitHub documentation — command behavior and service limits — conditional when needed for the selected operation.
- [Git configuration contract](../conventions/git-configuration_conv.md) — independent switches, unavailable states and scoped preservation — required before configured operations or setup.
- [Extension helper](../scripts/README.md) — read-only saved-setting validation and limits — required before first local helper use.
