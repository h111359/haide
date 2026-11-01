# Definition management

## Definition

The role-local vocabulary for definition management, including the supporting terms below.

## Purpose

Provide the local vocabulary used by this role and its procedures without granting authority or supplying runtime values.

## Supporting Terms

- [term:Caller]: the human or coordinating leader supplying the task and authority.
- [term:Target]: the definition and supporting resources selected for this operation.
- [term:Origin]: runtime framework at `.hai/agents/<name>/` or workspace at `.hai_env/agents/<name>/`; each origin has its own `agents/catalogue.md`. Golden source packages at `hai_agents_library/agents/<name>/` are data, not a third runtime origin or registration. A source package and its installed snapshot may share the same name.
- [term:Registration]: a validated catalogue row making a definition eligible for selection and delegation. Creating files, updating them, validating them, and executing a registered role are separate from registration.

Configuration contracts are required package resources. Their settings/defaults
are definition knowledge; actual workspace values remain external owned data.
Definition management can identify an incompatible saved file without gaining
permission to repair it. Source and installed contracts follow the same complete
package and explicit-update boundaries as procedures and helpers.

## References

- [Agent definition](../SKILL.md) — responsibilities and procedures using this vocabulary.
