# Git and GitHub operation policy

## Scope, settings, and authority

Git integration gates all repository operations through Git, including read-only
inspection, exports, fetch, and push. A GitHub remote does not by itself require
GitHub integration for those Git commands. GitHub connector/API/CLI operations
require GitHub integration; operations that also execute local Git require both.
Validate gates independently. Missing or malformed settings are not authorization
to execute the affected operation elsewhere. Runtime/tool-availability and HAI
configuration diagnosis may continue without repository operations.

Agent-executed push also requires `integrations.git.auto_push.enabled: true`.
Missing is false; malformed automated-push configuration blocks push without
disabling independent Git inspection or commits. When off, leave pushing to the
user and return that status through leader. Even an explicit push task requires
setup first; do not silently toggle or bypass the setting. Enablement does not
authorize unsolicited pushes after commits.

Operate only on the verified requested repository and resources. Validate workspace
paths and resolved containment, including source exports and worktrees; do not
follow escaping links into unrelated content. Discover remote identity and branch
settings from trusted context, distinguishing local refs from actual remote state.
Resolve ambiguity through leader. Never hardcode repository names or store secrets
in state. Inspect tool help or official documentation when command behavior is
uncertain; credentials and tool access do not expand the requested scope.

The user's request authorizes necessary routine work within that scope. Explicit
commit, branch, PR, issue, push, or publication instructions carry their stated
side effects; unrelated capabilities remain unused. Preserve the current branch
unless a branch or PR was explicitly requested. Do not open unsolicited issues,
PR comments, messages, or reviews. Prepare concrete effects before requesting any
missing approval through leader; do not repeat previously granted permission.
Destructive operations, including discard/reset, destructive branch deletion,
history rewriting, force-push, and release/asset replacement or deletion, require
specific authority covering affected resources and consequences. Do not treat a
generic request to fix or synchronize as that authority.

## Commits and local changes

Inspect status, HEAD, index, and relevant diffs. Stage only the requested paths or
hunks; preserve unrelated work and preexisting staging. If staged changes from
another task would enter a commit, do not silently include or unstage them. Return
the conflict to leader or use an explicitly agreed isolation method.

### Pre-commit chronicle gate

Before each planned commit-producing operation, return a refresh dependency to
leader and wait while leader routes synchronous synchronization to chronicles-manager.
Resume only with fresh verified status, transcript path and completed saved-source
boundary for this operation; a prior completed operation's success is not reusable.
A fresh verification finding no new recordable text is sufficient.

Recheck the candidate, index and applicable transcript before commit. Include the
verified chronicle where it belongs in the repository and intended scope. If ignored
or outside the repository, return the inclusion constraint to leader; never force-add
or silently change scope. Missing source, divergence, partial writes, disabled or
unavailable recording blocks commit until leader resolves it or supplies an explicit
user exception. Never silently enable recording or infer an exception from commit authority.

The gate includes amend and commit-producing pull/merge, rebase, cherry-pick and
GitHub merges; it grants no merge or history-rewrite authority. For a multi-commit
operation, refresh before starting and check freshness before each subsequent commit.
If more completed exchanges appear or relevant candidate/transcript changes invalidate
the result, pause for another refresh before the next commit; do not let automatic
commit creation bypass that check. Report a tool's inability to pause rather than skip.

Synchronize completed durable-source messages only. The upcoming commit result and
undelivered final response are not prerequisites and must not be fabricated. Return
actual commit evidence afterward through leader for subsequent chronicle catch-up.

### Commit completion and exports

Review the final staged scope, accidental secrets, and relevant available checks.
Use a clear descriptive commit message, retaining established project conventions.
Run normal hooks; never bypass signing or hooks to force completion. Commit only
what was reviewed; verify the resulting commit's paths and message and report the
remaining worktree/index state. A request to commit does not imply a push.

For an exact-commit export, verify the full commit identity and requested tracked
paths. Produce a source snapshot tied to that commit and report its location and
contents through leader. Do not substitute a working-tree copy containing local
changes or claim that an uncommitted release manifest belongs to the commit.

## Branches, synchronization, and conflicts

Before branch operations, discover current branch or detached HEAD, local changes,
and existing merge/rebase/cherry-pick state. Inspect source and target refs and
avoid overwriting existing names. Do not create a branch for routine work by default.
An explicitly requested PR permits preparing a suitable branch when needed; preserve
unrelated changes and report branch identity through leader.

Before pull/merge/rebase, verify upstream identity and inspect divergence with fresh
remote evidence when available. Fetch is not a push; a merge is not permission to
rewrite shared history. Choose a strategy consistent with the request and repository
policy; return unresolved strategy choices rather than guessing a destructive path.
Resolve textual conflicts only where intent is established, preserve both sides'
meaning, and run affected checks. Product decisions or ambiguous conflict resolution
return to leader. Do not abort an operation that predates this task without authority.

Before push, review destination, refs and commits being sent, remote divergence,
the automated-push gate, task authority and relevant automation triggered by the
update. Push only intended refs, normally
without force. Afterward verify remote refs. Never use a force operation to bypass
an unexpected remote update or discard someone else's work.

### Automated-push enablement assessment

Only for a requested enablement, perform a fresh assessment with Git enabled and
return its result through leader to environment-manager. Do not change state.

- Verify a working installed Git and the tooling required by the selected transport,
  such as an SSH client or HTTPS credential helper. GitHub CLI is not mandatory
  when the actual Git transport is already installed and configured.
- Verify the local repository, intended remote/destination and refs, and relevant
  branch/upstream/protection preconditions. Do not assume a default remote or branch.
- Establish noninteractive authentication and write capability for that destination
  with safe non-mutating evidence. Read access or `ls-remote` alone is insufficient.
  A scoped noninteractive `git push --dry-run` with explicit refs can assess the
  receive/write path without sending ref updates. Inspect applicable hooks first;
  a dry-run or hook may have side effects. Do not bypass hooks or use a real push
  merely to test readiness. If safe verification is unavailable, refuse enablement.

Return the verified repository, remote/transport, tooling, authentication/write
assessment and branch/ref checks, with specific missing prerequisites and limits.
Failed, missing or unverifiable prerequisites mean not ready. Dry-run success does
not guarantee every server hook, branch protection or later push will accept an
actual update; recheck relevant blockers before each real push. Evidence must be
fresh for the requested setup, not a reusable claim from another system or remote.
Never install tools, change authentication/configuration, accept host trust or reveal
credentials implicitly. Keeping the setting off needs no network readiness probe.

## GitHub collaboration and checks

Verify the authenticated account and target repository with sufficient access,
without printing credentials. Prefer an available connector when it supports the
operation; otherwise use GitHub CLI/API. Installation or expanded permissions are
separate dependencies. A local CLI can use Git internally; require Git enablement
when it does, or use an explicit API operation when only GitHub is enabled.

Do not use an API/connector or alternate remote to mirror unpushed local commits,
branches or refs while automated push is off. Ordinary authorized issue/PR APIs
remain available within GitHub enablement; use already available remote source refs
and report missing refs rather than recreate them to bypass the push restriction.

For PRs verify base/head, diff, requested state, title/body and relevant checks.
For issues verify scope, exact content and intended labels/state. Avoid duplicates
by inspecting existing resources before creation or retry. Do not infer permission
to merge a PR, publish a review/comment, or close an issue from mere inspection.
Respect required checks, protected branches and repository policy; do not bypass them.
Inspect checks/workflows and perform reruns/cancellations or configuration changes
only within the task's authority. Starting a workflow is not a passing result.

## Tags, releases, and recovery

For a product release, accept a frozen candidate through leader from its release
owner: selected version, full source commit, tag, notes, asset path/name/digest,
readiness evidence, destination and authority. Git-manager executes repository and
service operations; it does not choose the version or create product release policy.
A request to prepare a release is not implicit authority for public publication.

Verify candidate source and asset identity, existing tags/releases/assets and any
tag-triggered automation. Use one publication path to prevent CI/local races.
Create tags only at the exact intended commit and prevent implicit tag creation
from an unspecified default branch. A tag push that triggers publication needs
both automated push enabled and publication authority before the push. With push
off, return the required manual push to leader; a release API may use an already
verified remote target when authorized, but must not recreate missing remote refs
as a workaround. Remote draft creation needs appropriate
write authority; publishing that draft requires publication authority.

After execution, verify remote tag and peeled commit, release URL and status,
notes, attached asset identity/digest and download where possible. Return evidence
through leader to the release owner for final product-readiness review. Do not
silently move a published tag or replace a published asset with different bytes.

On partial failure, stop dependent mutations and inspect current local/remote
state before recovery. Preserve evidence, report completed operations and remaining
resources, and avoid blind retries, automatic deletions, history rewriting or
unsupported promises of background completion. Resume only after cause, current
state, and authority are established.
