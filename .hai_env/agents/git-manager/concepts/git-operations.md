# Git operations

## Definition

The role-local vocabulary for git operations, including the supporting terms below.

## Purpose

Provide the local vocabulary used by this role and its procedures without granting authority or supplying runtime values.

## Supporting Terms

- [term:Git integration]: `integrations.git.enabled` in validated `.hai_env/state.json`.
- [term:GitHub integration]: `integrations.github.enabled` in that state.
- [term:Automated push]: `integrations.git.auto_push.enabled`; missing means false. It gates agent-executed pushes separately from Git enablement and task authority.
- [term:Operation authority]: the user's request and established scope supplied through leader, independently of whether an integration or tool is available.
- [term:Frozen release candidate]: version, exact source commit, destination, notes, asset identity and digest, readiness evidence, and publication authority supplied by leader after release preparation.
- [term:Pre-commit chronicle verification]: a fresh completed-source synchronization result or verified disabled/no-obligation status obtained through leader for this planned operation, not an earlier completed operation's result.

## References

- [Agent definition](../SKILL.md) — responsibilities and procedures using this vocabulary.
