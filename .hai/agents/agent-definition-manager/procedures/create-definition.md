# Create a definition

## Description

Create and verify a scoped agent definition and necessary resources, keeping creation separate from registration and reporting the actual resulting status.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:inspection] | Verified scope, identity and prerequisite findings | Mandatory | Result of Establish scope and inspect | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:role_requirements] | Meaningful purpose, boundaries, knowledge, inputs, defaults, failures and outcomes | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:origin] | Requested origin; default workspace | Optional | Caller or authorized context | Default to workspace origin for new definitions; preserve origin for existing targets. |
| [input:name] | Proposed descriptive name | Optional | Caller or authorized context | Resolve a descriptive name with the caller before creating a definition. |
| [input:execution_metadata] | Proposed specialist class and effort | Optional | Caller or authorized context | Choose justified specialist class/effort and explain; preserve leader exceptions. |

## Prerequisites

Verified `inspection` output from [Establish scope and inspect](establish-scope-and-inspect.md), supplied as [input:inspection]. Meaningful role requirements and settled ownership before creation.

## Rules

- **Workspace default:** Agent-definition-manager MUST use workspace origin for a new agent unless framework creation is explicitly requested.
- **Missing name:** Agent-definition-manager MUST resolve an absent descriptive name with the caller before creation.
- **Unspecified execution settings:** Agent-definition-manager MUST choose and explain justified specialist class and effort values when none are supplied.
- **Model mapping boundary:** Agent-definition-manager MUST NOT put concrete model mappings in the new definition.
- **Exclusive creation:** Agent-definition-manager MUST create new definition files and directories exclusively without replacing existing parents or targets.

## Steps

1. Resolve purpose, trigger, boundaries, knowledge, inputs/defaults, failure behavior, procedures and observable outcomes from [input:role_requirements] and [input:inspection]. Resolve conflicting ownership and a missing [input:name]; establish [input:origin] and [input:execution_metadata] under the creation defaults.
2. Author the canonical description first. Prepare unchanged-format YAML identity/optional fields and the six ordered SKILL headings; set folder/name agreement and quoted string specialist metadata, applying leader's exception when relevant.
3. Classify each proposed statement by meaning and scope. Put shared constraints in SKILL Rules, unique operation-specific constraints in local Rules, actions/decisions in Steps, required starting conditions in Prerequisites and short purpose/result prose in Description. Keep concepts explanatory and conventions about representation/contracts.
4. Write each genuine rule with an explicit actor, action, object and applicable condition. Use uppercase `MUST` for an obligation, `MUST NOT` for a prohibition and `MAY` for a choice within existing permission. Split independent requirements into separate short bold titles without IDs; use exactly `None.` for no local rules. Reference inherited rules rather than repeat or override them.
5. Compare the drafted wording with [input:role_requirements] and settled decisions. Check that defaults, preferences, permitted alternatives, obligations, prohibitions and exceptions retain their meaning; a modal word alone proves neither clarity nor correct placement.
6. Prepare each procedure's Description, Inputs, Prerequisites, Rules, Steps, Outputs and References, including local namespaced tables and absence behavior. Use canonical index triggers and local file links, or the permitted single inline form. Map domain terms to purposeful concept Markdown; place schemas/contracts in conventions and actual execution behavior in the owning procedure. Add conditional references and only demonstrated supporting resources.
7. Recheck authority, collision facts, context, target absence and containment, then create the prepared resources exclusively. If inputs changed or creation partially fails, return actual partial results under the inherited failure rule.
8. Run [Validate or audit](validate-or-audit.md), passing the selected target as `target`, [input:inspection] as `inspection` and requested scope as `audit_scope` where relevant. If validation fails, return actual partial results and findings without registration.
9. If explicit combined registration was requested and verification succeeds, pass the canonical target, successful validation and explicit registration authority to [Register a validated definition](register-definition.md) as `target`, `validation_evidence` and `registration_authority`, with [input:inspection] as `inspection`. Receive its verified result before reporting registration.
10. Return [output:definition] with verification and actual registration status, unregistered when registration was not requested or did not succeed.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:definition] | Verified new definition and resources | Structural and semantic evidence reported; unregistered unless explicit combined registration succeeds. |

## References

- [Role rules and references](../SKILL.md) — applicable ownership, safety, context and authoring rules.
- [Agent convention](../../../conventions/agent_conv.md) — definition format, identity,
  selection, and ownership — required for all operations.
- [Agent concept](../../../concepts/agent.md) — role boundaries — required when creating
  or changing responsibilities.
- [State convention](../../../conventions/state_conv.md) — catalogue encoding and workspace
  prerequisites — required for catalogue writes and HAI context; independent format
  checks and prerequisite diagnosis remain available without initialized state.
- [Framework catalogue](../../catalogue.md) and the workspace catalogue when present —
  registration and identity checks — required before mutations; conditional on audit scope.
- [Model profiles](../../../conventions/model-profiles_conv.md) — model metadata and
  runtime evidence boundaries — conditional when choosing execution declarations.
- [Framework layout](../../../conventions/framework-layout_conv.md) — canonical resource
  placement — required for creation or explicitly authorized relocation.
- [Agent tools](../../../tools/agents/README.md) — validation commands and limits —
  required before first helper use.
- [Tooling convention](../../../conventions/tooling_conv.md) — implementation and testing —
  conditional when creating, changing, or executing supporting helpers.
- Caller-supplied sources — target-role knowledge and authority — read only what
  the selected operation needs.
