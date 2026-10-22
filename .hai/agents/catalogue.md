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
| `chronicles-manager` | Call to maintain a session's exact Markdown transcript when chronicles are enabled or required by workspace instructions. Returns the verified transcript location and any synchronization issues. | [SKILL.md](chronicles-manager/SKILL.md) |
| `specification-manager` | Call to enter, update, organize, or validate durable product specification information. Returns changes, verification evidence, and unresolved decisions. | [SKILL.md](specification-manager/SKILL.md) |
| `request-manager` | Call on demand to create or manage a tracked request through clarification, analysis, planning, implementation, testing, and closure. Creation requires clear intent; selecting this role alone creates nothing. Uses HAI's enabled configured store, or standalone .hai_env/requests under the supplied workspace with an explicit folder override allowed. Returns request records, workspace changes, verification results, and unresolved dependencies. | [SKILL.md](request-manager/SKILL.md) |
| `workspace-agent-creator` | Call to clarify a new workspace specialist role, create its definition, and register it in an initialized environment. Returns validated files and registration evidence, or the decisions or prerequisites still needed. | [SKILL.md](workspace-agent-creator/SKILL.md) |

Workspace agents and copies of their selection guides are listed exclusively
in `.hai_env/agents/catalogue.md`, not here. Read both catalogues together for selection. Availability, validation,
and explicit-call rules follow the [agent convention](../conventions/agent_conv.md).
