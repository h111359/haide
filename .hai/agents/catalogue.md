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
| `environment-manager` | Call to load or validate workspace environment, initialize safely absent core state while preserving existing resources, or configure mandatory Activity location and optional features through chat. Returns validated context, setup choices, and unresolved issues. | [SKILL.md](environment-manager/SKILL.md) |
| `chronicles-manager` | Call to synchronize exact source exchanges into leader-assigned Activity transcript segments asynchronously by default or synchronously before a commit. Follows validated recording settings and source boundaries; returns verified segment paths, source coverage, and unresolved synchronization issues without creating or closing Activities. | [SKILL.md](chronicles-manager/SKILL.md) |
| `specification-manager` | Call to enter, update, organize, or validate durable product specification information. Returns changes, verification evidence, and unresolved decisions. | [SKILL.md](specification-manager/SKILL.md) |
| `activity-manager` | Call to discover, create, resume, record, revise, or close HAI's current Activity and perform scoped clarification, analysis, planning, implementation, or verification. All substantive HAI work belongs to an Activity. Returns consistent records, lifecycle and step status, verification evidence, and unresolved dependencies; leader alone coordinates specialists. | [SKILL.md](activity-manager/SKILL.md) |
| `agent-definition-manager` | Call to create, update, validate, audit, or register framework and workspace agent definitions and supporting resources. New agents default to workspace origin. Creation does not register an agent; registration must be requested separately or explicitly combined. Returns verified definition changes, findings, registration status, and unresolved decisions. | [SKILL.md](agent-definition-manager/SKILL.md) |
| `git-manager` | Call to inspect or operate Git repositories and GitHub commits, branches, merges, pushes, pull requests, issues, tags, releases, and checks using validated integration settings. Returns verified changes, repository and remote status, and unresolved dependencies. | [SKILL.md](git-manager/SKILL.md) |

Workspace agents and copies of their selection guides are listed exclusively
in `.hai_env/agents/catalogue.md`, not here. Read both catalogues together for selection. Availability, validation,
and explicit-call rules follow the [agent convention](../conventions/agent_conv.md).
