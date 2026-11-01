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
| `environment-manager` | Call to load or validate workspace environment, initialize safely absent core state while preserving existing resources, configure mandatory Activity location and chronicles, or perform explicitly scoped core migrations. Returns validated context, setup choices, and unresolved issues. | [SKILL.md](environment-manager/SKILL.md) |
| `activity-manager` | Call to discover, create, revise or close HAI Activities and perform scoped clarification, analysis, planning, implementation or verification. Also synchronizes optional exact-source Activity transcripts and verifies recording. Returns consistent records, lifecycle and step status, source coverage, actual evidence and unresolved dependencies; leader alone coordinates specialists. | [SKILL.md](activity-manager/SKILL.md) |

Workspace agents and copies of their selection guides are listed exclusively
in `.hai_env/agents/catalogue.md`, not here. Read both catalogues together for selection. Availability, validation,
and selection eligibility follow the [agent convention](../conventions/agent_conv.md).
