# Workspace agent catalogue

Read this catalogue together with `.hai/agents/catalogue.md` for role selection.
Entries follow the [state convention](../../.hai/conventions/state_conv.md).

| Agent | Selection guide | Definition |
| --- | --- | --- |
| `advisor` | Call to review this repository's HAI framework and recommend the top three logical next actions in chat without changing files. | [SKILL.md](advisor/SKILL.md) |
| `release-manager` | Call to prepare a HAI bundle release, recommend an evidence-based SemVer bump, assess specification-contract compatibility, and verify release readiness and publication evidence. Returns release assets, readiness findings, publication status, and unresolved dependencies. | [SKILL.md](release-manager/SKILL.md) |
