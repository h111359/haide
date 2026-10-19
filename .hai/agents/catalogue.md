# Framework agent catalogue

All listed agents are selectable without environment initialization.
Each selection guide is copied verbatim from its canonical section in the
agent's knowledge.md. Validate equality when authoring or updating either file.
Choose from these short guides before opening the selected definition;
ordinary selection uses these copies without opening every knowledge file.
Paths below are relative to this catalogue.

| Agent | Selection guide | Definition |
| --- | --- | --- |
| `leader` | Call to coordinate a user task, choose specialists, monitor their work, and report their results. Leader is the only role that delegates to other agents. | [knowledge.md](leader/knowledge.md) |
| `environment-manager` | Call to inspect or load workspace environment, validate state and registered-agent availability, or initialize an absent environment when authorized. Returns context and unresolved issues. | [knowledge.md](environment-manager/knowledge.md) |
| `specification-manager` | Call to enter, update, organize, or validate durable product specification information. Returns changes, verification evidence, and unresolved decisions. | [knowledge.md](specification-manager/knowledge.md) |
| `workspace-agent-creator` | Call to clarify a new workspace specialist role, create its definition, and register it in an initialized environment. Returns validated files and registration evidence, or the decisions or prerequisites still needed. | [knowledge.md](workspace-agent-creator/knowledge.md) |

Workspace agents and copies of their selection guides are listed exclusively
in environment state's `agents` catalogue, not here. Availability, validation,
and explicit-call rules follow the [agent convention](../conventions/agent_conv.md).
