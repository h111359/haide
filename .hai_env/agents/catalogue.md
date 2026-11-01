# Workspace agent catalogue

Read this catalogue together with `.hai/agents/catalogue.md` for role selection.
Entries follow the [state convention](../../.hai/conventions/state_conv.md).

| Agent | Selection guide | Definition |
| --- | --- | --- |
| `advisor` | Call to review this repository's HAI framework and recommend the top three logical next actions in chat without changing files. | [SKILL.md](advisor/SKILL.md) |
| `release-manager` | Call to prepare a HAI bundle release, recommend an evidence-based SemVer bump, and verify release readiness and publication evidence. Returns release assets, readiness findings, publication status, and unresolved dependencies. | [SKILL.md](release-manager/SKILL.md) |
| `git-manager` | Call to configure this workspace's optional Git/GitHub integrations or inspect and operate repositories, commits, branches, merges, pushes, pull requests, issues, tags, releases, and checks. Returns validated settings, verified changes, repository and remote status, and unresolved dependencies. | [SKILL.md](git-manager/SKILL.md) |
| `specification-manager` | Call to configure HAI specification enablement and location, or enter, update, organize, or validate durable product specification information. Returns validated settings, changes, verification evidence, and unresolved decisions. | [SKILL.md](specification-manager/SKILL.md) |
| `agent-definition-manager` | Call to create, maintain, validate or audit framework and workspace agent definitions and reusable source packages against conventions. New agents default to workspace origin. Returns verified definition changes, findings and metadata for Environment-manager; creation does not install or register a package. | [SKILL.md](agent-definition-manager/SKILL.md) |
