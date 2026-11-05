# Git operations

## Definition

The role-local vocabulary for git operations, including the supporting terms below.

## Purpose

Provide the local vocabulary used by this role and its procedures without granting authority or supplying runtime values.

## Supporting Terms

- [term:Git integration]: `settings.git.enabled` in validated `.hai_env/config/agents/git-manager.json`; absent file or leaf uses the contract's false default.
- [term:GitHub integration]: `settings.github.enabled` in that owner file, independently gated from Git.
- [term:Automated push]: `settings.git.auto_push.enabled` in that owner file; missing means false. It gates agent-executed pushes separately from Git enablement and task authority. Saved enablement never supplies live readiness; legacy state supplies no runtime fallback.
- [term:Operation authority]: the user's request and established scope supplied through host coordinator, independently of whether an integration or tool is available.
- [term:Frozen release candidate]: version, exact source commit, destination, notes, asset identity and digest, readiness evidence, and publication authority supplied by host coordinator after release preparation.
- [term:Pre-commit chronicle verification]: a fresh completed-source synchronization result or verified disabled/no-obligation status obtained through host coordinator for this planned operation, not an earlier completed operation's result.

## References

- [Agent definition](../SKILL.md) — responsibilities and procedures using this vocabulary.
