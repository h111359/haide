# Validate or audit

## Description

Review selected agent definitions and resources without changing them, and return structural and semantic findings with verification limits.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:inspection] | Verified operation and scope findings | Mandatory | Result of Establish scope and inspect | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:target] | Canonical definition or requested registered collection | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:audit_scope] | Optional audit baseline or scope details | Optional | Caller or authorized context | Use the requested canonical target or registered collection; infer no broader audit. |

## Prerequisites

Verified `inspection` output from [Establish scope and inspect](establish-scope-and-inspect.md), supplied as [input:inspection]. A canonical target or bounded registered collection.

## Rules

- **Independent format checks:** Agent-definition-manager MAY validate a definition's format without a catalogue, model profiles or environment state.
- **Tool results:** Agent-definition-manager MUST limit claims based on a successful format tool to the checks documented for that tool.
- **Separate checks:** Agent-definition-manager MUST NOT treat format success as proof that instructions preserve their meaning, a model can run, a catalogue registers the agent or its name is unique within the workspace origin.

## Steps

1. Bound [input:target] and [input:audit_scope] using [input:inspection]. Read the tool README before first use. Select `validate --definition` for a canonical installed target (registered or not), or `audit` for the registered collection/profiles. For a source package, copy the complete package into a disposable `.hai_env/agents/<name>/` layout beside the compatible core and required installed peers, then validate that staged installed path; do not add a third runtime origin or invoke the source definition. Record checks outside the command's coverage for scoped manual review.
2. Check required configuration metadata, canonical package-contained contract, matching identity, supported versions, supported typed defaults and safe directory declarations, explicit empty settings when applicable, runtime absence/error behavior and compatibility boundaries. Do not require an override file or initialize settings for definition validation. Separately review saved-setting dependencies where in scope. Check YAML, optional metadata, identity, six SKILL headings, unique titled rules, index/single-inline form, seven procedure sections, local input/output tables, resolved term mappings, paths/references and catalogue equality where applicable. Inspect requested membership/collision/supporting-link facts separately from parser results.
3. Review every relevant statement semantically: Description explains purpose/result; Prerequisites state required conditions; Rules contain constraints; Steps contain ordered actions and explicit branches; concepts explain meaning and conventions define data/formats. Reject numbered workflows or superficial imperative prefixes in Rules. Confirm cross-procedure rules live in SKILL and apply automatically, local Rules contain only unique narrower constraints without overrides/duplicates, and no local rules is written exactly `None.`.
4. Review every rule's meaning and plain wording beyond parser checks. Identify its actor, action, object and applicable condition; split unrelated requirements and check unique readable titles. Confirm `MUST` means obligation, `MUST NOT` prohibition and `MAY` an existing permitted choice. Compare before/after duties, defaults, preferences, alternatives and exceptions with the authorized source; reject a rule whose meaning is unclear even if its modal spelling passes.
5. Review trigger/description agreement, ownership, inputs/defaults/absence behavior, parameter scope, explicit source-to-target handoffs, outcomes, reading conditions, independent execution and host coordinator's special rules. Review relevant helpers under the tooling convention. Compare changed semantics with the authorized source baseline and map every obligation to its retained destination.
6. Return [output:findings] with paths, operation/origin, scope, decisions, severity/effect, structural and semantic evidence, actual registration status, limits and unresolved dependencies. Identify unrun checks and pre-existing issues. Distinguish creation without registration, audits with findings and any required inconsistent coordinated update.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:findings] | Structural and semantic verification findings | Paths, scope, severity/effect, evidence, limits and actual registration status reported; unavailable checks explicitly unrun. |

## References

- [Role rules and references](../SKILL.md) — applicable ownership, safety, context and authoring rules.
- [Agent convention](../../../../.hai/conventions/agent_conv.md) — definition format, identity,
  selection, and ownership — required for all operations.
- [Agent concept](../../../../.hai/concepts/agent.md) — role boundaries — required when creating
  or changing responsibilities.
- [State convention](../../../../.hai/conventions/state_conv.md) — catalogue encoding and workspace
  prerequisites — required for interpreting catalogue identity and HAI context; independent format
  checks and prerequisite diagnosis remain available without initialized state.
- [Workspace catalogue](../../../../.hai_env/agents/catalogue.md) when present —
  registration and identity checks — required before mutations; conditional on audit scope.
- [Model profiles](../../../../.hai/conventions/model-profiles_conv.md) — model metadata and
  runtime evidence boundaries — conditional when choosing execution declarations.
- [Framework layout](../../../../.hai/conventions/framework-layout_conv.md) — canonical resource
  placement — required for creation or explicitly authorized relocation.
- [Agent tools](../../../../.hai/tools/agents/README.md) — validation commands and limits —
  required before first helper use.
- [Tooling convention](../../../../.hai/conventions/tooling_conv.md) — implementation and testing —
  conditional when creating, changing, or executing supporting helpers.
- Caller-supplied sources — target-role knowledge and authority — read only what
  the selected operation needs.
