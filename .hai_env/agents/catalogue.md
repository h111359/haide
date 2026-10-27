# Workspace agent catalogue

Read this catalogue together with `.hai/agents/catalogue.md` for role selection.
Entries follow the [state convention](../../.hai/conventions/state_conv.md).

| Agent | Selection guide | Definition |
| --- | --- | --- |
| `advisor` | Call to review this repository's HAI framework and recommend the top three logical next actions in chat without changing files. | [SKILL.md](advisor/SKILL.md) |
| `release-manager` | Call to prepare and publish a new HAI bundle release, recommend an evidence-based SemVer bump, assess specification-contract compatibility, and return verified release assets, publication status, and unresolved dependencies. | [SKILL.md](release-manager/SKILL.md) |
