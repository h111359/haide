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
| `environment-manager` | Call to load, initialize or configure the HAI environment, maintain Activity records and lifecycle, perform scoped core migrations, install selected optional agent packages, or register and synchronize runtime agent catalogues. Returns validated context, consistent records, package/registration evidence and unresolved issues. | [SKILL.md](environment-manager/SKILL.md) |

Workspace agents and copies of their selection guides are listed exclusively
in `.hai_env/agents/catalogue.md`, not here. Read both catalogues together for selection. Availability, validation,
and selection eligibility follow the [agent convention](../conventions/agent_conv.md).
