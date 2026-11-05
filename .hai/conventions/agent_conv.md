# Agent convention

## Identity and availability

Optional installed workspace definitions live at `.hai_env/agents/<name>/SKILL.md`. Names match `[a-z][a-z0-9]*(?:-[a-z0-9]+)*`, are at most 64 characters, match their parent directory and are unique case-insensitively. `.hai_env/agents/catalogue.md` contains explicit registrations and exact decoded description copies. Creation or installation does not register a package or grant permission to execute it. Unregistered packages may be inspected and validated as data. Selection requires an authorized task and the host's actual execution capability; a profile or catalogue row does not prove that capability. Core startup and administration do not depend on any optional package.

Source packages under `hai_agents_library/agents/` are data, not an execution origin. Source maintenance, installed replacement, registration and execution are separate scopes. Preserve external settings and records, review local differences or unknown baselines before replacing a package, and do not infer execution authority from installation.

Apply the safe fixed `.hai_env/agent_instructions.md` and higher-priority instructions before dependent work. Substantive work uses the current Activity; startup, necessary setup and read-only diagnosis can establish context first. Pass relevant task scope, authority, Activity identity and evidence to any selected extension.

## Required definition format

Use YAML frontmatter followed by Markdown. Required fields are `name` and
`description`; description is a nonblank string of at most 1024 characters,
expressed as one short paragraph with no line breaks after YAML decoding.
HAI names follow the stricter identity rule above. Preserve applicable Agent
Skills optional fields (`license`, `compatibility`, `metadata`, `allowed-tools`);
metadata maps string keys to string values. YAML duplicate keys are invalid.

Spawned specialists MUST declare both HAI extension keys under `metadata`:
`hai-model-class` is `light`, `standard`, or `advanced`, and
`hai-reasoning-effort` is a standard effort label (`low`, `medium`, `high`,
`xhigh`, `max`, or `ultra`). Quote metadata values as strings. Concrete model IDs belong only in local model profiles, never agent declarations.

There is no agent H1 title, Selection guide body section, embedded Definitions,
or agent-level Inputs/Outputs section. Include exactly these six H2 headings once
each and in order:

```markdown
---
name: example-specialist
description: "Call to perform a specific task and return its verified result."
metadata:
  hai-configuration-contract: "configuration/contract.json"
  hai-model-class: "standard"
  hai-reasoning-effort: "high"
---

## Purpose
<Why this role exists.>

## Scope
<Responsibilities and ownership.>

## Out of Scope
<Explicit exclusions and boundaries.>

## Rules
- **Agreed scope.** The example-specialist MUST keep its work within the user's agreed task scope.

## Procedures
| Procedure | Trigger | File |
| --- | --- | --- |
| Perform work | The caller requests the supported work. | [Perform work](procedures/perform-work.md) |

## References
[Owned configuration contract](configuration/contract.json) — required for configuration and dependent work.
<Path — purpose — reading condition; declared concept mappings when used.>
```

Shared Rules have readable bold titles unique within the agent's shared Rules section, without IDs or implied
numeric priority. Optional H3 groups organize related subjects; do not create
empty groups or require every agent to use the same taxonomy. Group order does not
establish precedence. State applicability and exceptions explicitly; steps and
execution dependencies belong in procedures. Shared rules apply to every procedure.
Only genuinely procedure-specific rules belong in that procedure's mandatory
Rules section, following [procedure_conv.md](procedure_conv.md). Local rules do not
override or duplicate shared rules. Resolve conflicts rather than treating a local
rule as overriding a shared rule; a shared rule's explicit applicability/exception remains
part of that shared rule. Procedure-local parameter names cannot appear in shared rules.

Rule wording follows [instruction-writing_conv.md](instruction-writing_conv.md):
explicit `MUST`, `MUST NOT`, or `MAY`, a clear actor/action/object and relevant
conditions, short readable titles, and preserved existing meaning. That convention
is the single source for writing style in shared and local Rules; it does not
change the existing six role sections or grant permission to act.

Procedures follow [procedure_conv.md](procedure_conv.md). Multiple procedures live
in separate agent-owned files, indexed with the exact Procedure/Trigger/File
columns. A single procedure may use the external form or the specified inline
form. Canonical triggers occur only in the index or beside the sole inline
procedure. Procedure execution stays within the same role; it is not delegation.

Every procedure declares one Inputs table and one Outputs table. Inputs use only
Mandatory/Optional requirements, with source and absence behavior. Rules and
prerequisites state operation-specific requirements without introducing another
input category. Outputs state observable results and completion criteria.

Use [reference-notation_conv.md](reference-notation_conv.md): `[input:name]` and
`[output:name]` are local to one procedure, not agent-global placeholders. Calls
explicitly identify source values and destination input names; matching names do
not imply inheritance or substitution. Concept definitions remain in their owning
concept files, with `[term:name]` mappings declared in References. Agent-level term
mappings apply to its procedures; procedure-local additions are allowed.

Retrieve missing mandatory inputs from authorized context before returning the
dependency to host coordinator or asking the human when called directly. Continue independent
work; optional values use declared defaults or remain absent. Never invent values,
decisions, permission, or approval. References specify reading conditions; a folder
reference does not require recursive loading. Preserve paths and resolved containment
before reads and writes.

## Agent-owned configuration

Every optional agent declares string metadata
`hai-configuration-contract: "configuration/contract.json"` and ships the matching
package-local contract under [agent-configuration_conv.md](agent-configuration_conv.md).
Agents with no customizable settings declare an empty settings map. Keep all six
SKILL headings; do not add a configuration body section or concrete model mappings.
Creation, update, validation, registration and installation check this characteristic.

Before dependent execution, validate the selected installed contract and read that
agent's fixed workspace configuration with the shared read-only
[configuration helper](../tools/configuration/README.md). Retain its path, status,
known effective values, configured fields and issues in the handoff. Missing files
use declared defaults; invalid/unverified files do not silently become defaults.
The receiving role checks that evidence and rereads when inputs changed. Scope
failures to dependent work; owner-specific validators may preserve independent
valid capabilities where the generic aggregate result is invalid. Read-only
configuration diagnosis and explicitly authorized scoped repair remain possible.
Do not scan every agent's configuration during ordinary startup.

Definition validation checks contract data without loading workspace settings or
requiring initialized state. Saved settings do not affect registration identity,
replace model-profile resolution, or override task permission. Package installation
preserves external config bytes and reports format incompatibility; it never
performs an implicit config migration. Activity location and chronicles remain runtime-owned in state
format 3; Specification-manager owns enablement/root and validates it independently
from core/Activity context. Format 2 is migration context, never an owner-settings fallback.

## Model resolution and coordination

For an optional extension, use its declared model and effort only if supported by the actual host; report unavailable combinations without silently substituting. Profiles are optional and do not establish host support. Core runtime commands do not require profiles or agent invocation. The host decides whether to invoke an optional extension, supplies relevant context and authority, and reports actual results and unresolved dependencies.

## Supporting resources

An agent's `SKILL.md` is its canonical role entry point: identity, purpose, scope,
exclusions, shared rules, procedure selection, and references. Its linked
`procedures/` files own their execution steps, procedure-specific rules, and local input/output contracts;
a single procedure may remain inline. This deliberately separates procedure files
from shared role rules without moving execution behavior into conventions. Concepts
explain meaning and rationale; prerequisites state entry conditions, rules state
obligations, and steps state ordered actions/branches. The
[Procedure concept](../concepts/procedure.md) explains their relationship.

Agent-local `concepts/` contain purposeful concept definitions and `conventions/`
contain reusable formats and domain contracts. Neither is a substitute for the
agent's execution procedures. Shared agent conventions define role-independent
identity, structure, selection, handoff, and ownership contracts; reference those
contracts rather than copying them into each role. Each participant owns its own
handoff procedures even when several roles participate in a workflow.

Optional supporting folders are `procedures/`, `concepts/`, `conventions/`, and
`scripts/` for owned helpers and usage documentation. Other justified resources,
including existing `templates/`, remain permitted. Create no unused scaffold.
Framework-wide concepts and conventions retain their canonical framework location.
Role-owned domain knowledge remains in its package as a single authority, with
shared readers linking to it. Scripts follow [tooling_conv.md](tooling_conv.md).

## Registration and verification

Explicit registration is separate from package installation, authoring and execution. Validate the installed definition and its configuration contract, identity, path containment and the exact catalogue description; preserve unrelated entries and stop on conflicts. Synchronizing an existing row does not add membership. The shared agent auditor checks format, not semantic equivalence, authorization or runtime availability. See [agent tools](../tools/agents/README.md) and [state convention](state_conv.md).

## References

- [Activity](../concepts/activity.md) and [Activity convention](activity_conv.md).
- [Agent configuration](agent-configuration_conv.md), [procedure convention](procedure_conv.md), and [reference notation](reference-notation_conv.md).
- [Runtime commands](../tools/runtime/README.md).
