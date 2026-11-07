# Workspace agent catalogue

This catalogue lists the installed optional workspace agents.
Entries follow the [state convention](../../.hai/conventions/state_conv.md).

| Agent | Selection guide | Definition |
| --- | --- | --- |
| `advisor` | Call to review this repository's HAI framework and recommend the top three logical next actions in chat without changing files. | [SKILL.md](advisor/SKILL.md) |
| `release-manager` | Call to prepare a HAI bundle release, recommend an evidence-based SemVer bump, and verify release readiness and publication evidence. Returns release assets, readiness findings, publication status, and unresolved dependencies. | [SKILL.md](release-manager/SKILL.md) |
| `git-manager` | Call to configure this workspace's optional Git/GitHub integrations or inspect and operate repositories, commits, branches, merges, pushes, pull requests, issues, tags, releases, and checks. Returns validated settings, verified changes, repository and remote status, and unresolved dependencies. | [SKILL.md](git-manager/SKILL.md) |
| `specification-manager` | Call to configure HAI specification enablement and location, or enter, update, organize, or validate durable product specification information. Returns validated settings, changes, verification evidence, and unresolved decisions. | [SKILL.md](specification-manager/SKILL.md) |
| `agent-definition-manager` | Call to create, maintain, validate or audit workspace agent definitions and reusable source packages against conventions. New agents default to workspace origin. Returns verified definition changes, findings and metadata for runtime; creation does not install or register a package. | [SKILL.md](agent-definition-manager/SKILL.md) |
| `business-analyst` | Call to clarify business intent, analyze requirements and define scope and acceptance criteria. Returns attributable requirements, decisions, ambiguities and evidence for host coordinator and the Activity record owner. | [SKILL.md](business-analyst/SKILL.md) |
| `solution-architect` | Call to analyze technical options, design a solution and plan implementation and verification against agreed requirements. Returns justified architecture, tradeoffs, dependencies, risks and an actionable plan. | [SKILL.md](solution-architect/SKILL.md) |
| `software-developer` | Call to implement authorized product changes and run appropriate developer checks against agreed requirements and technical decisions. Returns actual changes, verification evidence, failures and unresolved dependencies. | [SKILL.md](software-developer/SKILL.md) |
| `quality-assurance` | Call to verify product behavior against agreed requirements and acceptance criteria, assess regressions and report evidence-based defects and coverage limits. Returns actual test results and unresolved acceptance risks. | [SKILL.md](quality-assurance/SKILL.md) |
| `codex-chronicle-manager` | Call to synchronize exact saved Codex session exchanges into assigned Activity transcripts, inspect recording progress, verify source coverage or fulfill mandatory pre-delivery recording. Returns verified segments, checkpoints, operation-bound coverage and precise source or assignment blockers. | [SKILL.md](codex-chronicle-manager/SKILL.md) |
