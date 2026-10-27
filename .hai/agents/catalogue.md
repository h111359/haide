# Framework agent catalogue

All listed agents are selectable without environment initialization.
Each selection guide is copied verbatim from the decoded YAML description in the
agent's SKILL.md. Validate equality when authoring or updating either file.
Choose from these short guides before opening the selected definition;
ordinary selection uses these copies without opening every knowledge file.
Paths below are relative to this catalogue.

| Agent | Selection guide | Definition |
| --- | --- | --- |
| `leader` | Call to coordinate a user task, choose specialists, monitor their work, and report their results. Leader is the only role that delegates to other agents. | [SKILL.md](leader/SKILL.md) |
| `environment-manager` | Call to load or validate workspace environment, initialize safely absent core state while preserving existing resources, or configure optional features through chat. Returns validated context, setup choices, and unresolved issues. | [SKILL.md](environment-manager/SKILL.md) |
| `chronicles-manager` | Call to synchronize a session's exact Markdown transcript asynchronously by default or synchronously before a commit. Follows validated chronicles settings and workspace instructions; returns verified recording status, transcript location, source boundary, and unresolved synchronization issues. | [SKILL.md](chronicles-manager/SKILL.md) |
| `specification-manager` | Call to enter, update, organize, or validate durable product specification information. Returns changes, verification evidence, and unresolved decisions. | [SKILL.md](specification-manager/SKILL.md) |
| `request-manager` | Call on demand to create or manage a tracked request through clarification, analysis, planning, implementation, testing, and closure. Creation requires clear intent; selecting this role alone creates nothing. Uses HAI's enabled configured store, or standalone .hai_env/requests under the supplied workspace with an explicit folder override allowed. Returns request records, workspace changes, verification results, and unresolved dependencies. | [SKILL.md](request-manager/SKILL.md) |
| `agent-definition-manager` | Call to create, update, validate, audit, or register framework and workspace agent definitions and supporting resources. New agents default to workspace origin. Creation does not register an agent; registration must be requested separately or explicitly combined. Returns verified definition changes, findings, registration status, and unresolved decisions. | [SKILL.md](agent-definition-manager/SKILL.md) |
| `git-manager` | Call to inspect or operate Git repositories and GitHub commits, branches, merges, pushes, pull requests, issues, tags, releases, and checks using validated integration settings. Returns verified changes, repository and remote status, and unresolved dependencies. | [SKILL.md](git-manager/SKILL.md) |

Workspace agents and copies of their selection guides are listed exclusively
in `.hai_env/agents/catalogue.md`, not here. Read both catalogues together for selection. Availability, validation,
and explicit-call rules follow the [agent convention](../conventions/agent_conv.md).
