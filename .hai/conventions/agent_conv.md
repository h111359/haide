# Agent convention

## Identity and availability

Framework definitions live at `.hai/agents/<name>/SKILL.md`; registered framework
roles are selectable without environment initialization. Workspace definitions live at
`.hai_env/agents/<name>/SKILL.md`. Names match
`[a-z][a-z0-9]*(?:-[a-z0-9]+)*`, are at most 64 characters, and match their
parent directory exactly. Names must be unique across both origins, including
case-insensitive comparison on supported platforms. Framework definitions take
precedence over conflicting workspace names; report conflicts without renaming,
overriding, unregistering, or repairing them.

The [framework catalogue](../agents/catalogue.md) and
`.hai_env/agents/catalogue.md` contain names, copied descriptions, and definition
links. Selection for execution and leader delegation require a valid registration
in the corresponding catalogue for both origins. Creation alone does not register
a definition. An explicit human call, name, or path does not bypass registration
or authorize it. Unregistered definitions in either origin may be inspected,
maintained, validated, or registered without executing them. Supplied paths must
identify the definition's canonical folder or `SKILL.md` and resolve inside the
workspace. Do not search unrelated locations. Ask for a
path when ambiguous. Before definition creation or registration, check both
catalogues and immediate folder names in both origins for case-insensitive
collisions, including unregistered folders; this does not authorize loading every
definition or discovering unregistered roles during ordinary selection.

## Reusable source packages and installed snapshots

`hai_agents_library/agents/<name>/` contains golden source packages, not a third
runtime origin or registry. Source and installed counterparts may share a name;
runtime uniqueness still covers both installed origins and unregistered runtime
folders. Source presence never grants execution eligibility. Runtime instructions,
helpers, contracts and peer references use installed copies or stable core paths,
never the library as a fallback. Ordinary startup and selection do not scan it.

Explicit source maintenance, installation, staging/tests and packaging may read
selected library files as data without adopting their roles. Shared source edits
leave installed snapshots unchanged. Human-approved updates copy complete packages;
local differences or an unknown baseline require review before replacement. No
automatic updater, agent-version scheme or new state dependency is introduced.

An installed registered Agent-definition-manager owns authorized source maintenance,
copy installation and catalogue work. If it is absent or unavailable, report the
optional-owner dependency; do not invoke its source definition or bypass registration.
A human may bootstrap by copying the complete package, validating its installed
canonical path with shared tools and explicitly adding its workspace catalogue row
under the state convention. This manual action does not grant Leader mutation
authority or change normal delegation. It needs compatible environment/instructions;
the human verifies startup and preserves existing data before installation.

## Selection and loading

Read the framework catalogue and valid workspace entries together. Catalogue
Selection guide cells are exact copies of the decoded YAML `description` value,
which is canonical selection text. Descriptions briefly state when to call a role
and what it produces, consistent with its scope and ownership. Select from copies
before loading the selected `SKILL.md`; do not open every definition to choose a
role or recover missing descriptions. An explicit call identifies the requested
target; its valid catalogue entry is still required before selection for execution.

Validate a selected definition's identity, format, references, and description
copy. Report discovered stale copies without repairing them. Ordinary startup
validates catalogue structure and references without loading all definitions.
Always load safe readable `.hai_env/agent_instructions.md` independently of state
validity before dependent work, as well as applicable higher-priority workspace
instructions and this convention. An existing empty file adds no instructions;
missing/unreadable content blocks dependent work, allowing diagnosis and authorized
initialization, migration, or repair under the state convention. Preserve this
instruction context in specialist handoffs. Then
follow supporting references only when needed. An invalid workspace entry does
not make framework roles unavailable.

These definitions reuse the [Agent Skills format](https://agentskills.io/specification).
The filename alone does not install a skill, add it to a runtime's discovery
paths, select a model, create a subprocess, or spawn an agent. HAI catalogue
selection and leader orchestration remain explicit.

## Mandatory Activity context

All substantive HAI work belongs to a [term:Activity],
including advice, brainstorming, analysis, planning, framework maintenance,
implementation and verification. Activities have no enabled flag. A compatible
validated environment supplies activities.location; Activity-manager discovers
and maintains the sole current record, while leader alone coordinates specialists.
Startup validation, bootstrap/setup required to establish usable context, and
read-only prerequisite diagnosis may proceed before a record exists. These bounded
exceptions do not authorize later untracked substantive work.

Startup resumes valid current work. A new chat alone creates none; meaningful new
work with no current record creates an Activity within the user's agreed task and permission.
Conflicting current/new intent needs leader's boundary resolution, not silent
closure or replacement. Substantive specialist handoffs include stable Activity ID,
path and relevant context; return actual results for recording. The Activity-manager
is a records/lifecycle owner and scoped executor, never a second orchestrator.

Lifecycle active/closed, performed steps and completed/cancelled/stopped outcomes
are separate. Analysis alone may complete its objective. Material definition,
analysis and plan revisions preserve history even after implementation begins.
Closed Activities accept dated attributable supplements and delayed exact old-source
transcript synchronization; new substantive work needs a new linked Activity.

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
`xhigh`, `max`, or `ultra`). Quote metadata values as strings. The leader omits
both keys: it remains the root chat using the interface-selected model and effort.
Concrete model IDs belong only in local model profiles, never agent declarations.

There is no agent H1 title, Selection guide body section, embedded Definitions,
or agent-level Inputs/Outputs section. Include exactly these six H2 headings once
each and in order:

```markdown
---
name: example-specialist
description: "Call to perform a specific task and return its verified result."
metadata:
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
dependency to leader or asking the human when called directly. Continue independent
work; optional values use declared defaults or remain absent. Never invent values,
decisions, permission, or approval. References specify reading conditions; a folder
reference does not require recursive loading. Preserve paths and resolved containment
before reads and writes.

## Model resolution and orchestration

Follow [model-profiles_conv.md](model-profiles_conv.md) before spawning. Resolve
the selected specialist's class through `.hai_env/model_profiles.json` and check
the exact model/effort pair against the current runtime's advertised capabilities.
Report missing or unavailable settings; do not silently substitute a model, class,
or effort. Direct role use in the root chat does not change its interface settings.
Startup bootstrap and explicit human overrides follow the named exceptions in the
model-profile convention. They must be reported and never rewrite declarations.

Only leader selects, delegates to, monitors, and coordinates other agents.
Specialists execute their own procedures using inputs, references, and tools;
they return missing dependencies to leader and do not invoke agents. Each role
owns its shared rules in `SKILL.md` and its execution procedures, including any
genuinely local rules, in linked
`procedures/` files (or the sole inline procedure); callers do not duplicate them. Runtime spawn interfaces may impose additional constraints:
when explicit model/effort overrides require an empty history fork (for example
`fork_turns="none"`), use that supported combination and pass the definition path,
workspace instructions, relevant task context, and expected outcome explicitly.
Do not assume inherited history, settings, or automatic skill discovery.

Available agents/tools and enabled features do not expand the user's permission
or the role's responsibilities. Do not bypass
disabled or invalid capabilities through another role or tool.

## Context handoff and input checks

For every specialist handoff, including startup and follow-up assignments, leader
MUST explicitly cover this checklist in the task message:

1. **Objective and acceptance criteria:** the user's objective and the agreed
   criteria for completing the delegated work.
2. **Constraints and decisions:** applicable constraints and explicit decisions,
   distinguishing settled decisions from assumptions.
3. **Relevant context:** relevant files, verified findings, and completed work
   the specialist needs to use or preserve.
4. **Open dependencies:** unresolved questions, conflicts, and dependencies.
5. **Scope and authorization:** allowed changes, task boundaries, and established
   authorization, including any actions that still require a decision.

Identify missing information or not-applicable items explicitly; never silently
omit a checklist field or fabricate context, decisions, or approval. Include the
selected definition path, applicable workspace instructions, stable current Activity
ID/path and context for substantive work (or the applicable bootstrap/diagnosis
exception), expected
output, and relevant verification requirements. Supply concise facts and precise
references the receiver can access; do not reproduce full conversation history
or duplicate the specialist's procedures. Inherited history does not replace this
handoff, and a follow-up must make retained context and changed requirements clear.

Before dependent work, the receiving specialist MUST load its definition and
applicable instructions, compare the handoff with the selected procedure's **Inputs** and prerequisites,
and check for missing or conflicting inputs. First retrieve needed context from
available, authorized sources within scope. If a required input remains missing
or conflicting, report the specific issue and dependent work to leader, pause that
work, and continue meaningful independent work. When called directly, report or
ask the human instead. Do not treat an assumption as a settled decision or infer
authorization from missing context. Shared checks supplement each role's own
input requirements and failure behavior; they do not replace them.

Leader monitors requests for context or decisions, resolves them from authorized
evidence or the human, and sends the resulting clarification to the receiver.
Before reporting completion, review the returned output and verification against
the objective, agreed acceptance criteria, and authorized scope; route remaining
gaps rather than claim dependent work is complete.

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

## Registration ownership and verification

When installed and registered, Agent-definition-manager owns framework and workspace definition creation, updates,
audits, selected golden source maintenance and explicitly requested catalogue registrations.
A missing optional owner blocks its dependent work, not core startup; manual human
bootstrap follows the source-package section above. Creation and registration
are separate; an explicit combined operation may perform both. Updating a registered
definition synchronizes its existing catalogue description and canonical reference;
updating an unregistered definition never adds a row. Independent format tools and
read-only prerequisite diagnosis need no initialized environment. Substantive HAI
maintenance/audits follow mandatory Activity context; workspace mutations additionally
retain their valid initialized environment prerequisite. Environment-manager owns
core environment configuration, model profiles, and the lightweight startup-validation policy; leader
may execute the shared read-only startup helper directly under its bounded exception
and otherwise owns selection and execution. Core initialization/configuration,
profile changes, and their repairs/migrations remain environment-manager work;
extension owners retain their declared scoped configuration. Audits do not repair, rename,
unregister, or delete.
Neither role silently repairs the other's data. Preserve unrelated state, rows,
and prose. Register only after validating the definition.
Coordinate writes without claiming multi-file transactionality: stop on changed
inputs, preserve partial results on failure, and report inconsistencies without
automatic retries, removal, or overwrite.

Validate names, canonical paths, collisions, YAML fields, string metadata,
model/effort declarations, six role headings, procedure layout and containment,
local input/output declarations, Mandatory/Optional requirements, outcome criteria,
term mappings, reference conditions, independence, and shared rules. Author `description` first, then copy its decoded value into the catalogue
using the state convention's table encoding. Compare decoded strings exactly,
including punctuation and whitespace; do not copy YAML quotes or scalar syntax.

For authoring or migration verification, use the shared
[agent tools](../tools/agents/README.md), then review semantic ownership and
procedures manually. Their full audit is not a startup requirement.

## Legacy definitions and authorized migration

A previous `knowledge.md` definition or catalogue link is legacy agent-format
material even when core state has the supported version. Report its registered name
and path and preserve the registration as a pending migration; exclude it from
execution without silently unregistering or reinterpreting it. Do not scan folders
to reconstruct registrations or prefer one file when both old and new files exist.
Core-state compatibility remains governed separately by the state convention.

An explicitly authorized agent-format migration validates every affected existing
registration and definition, retains each name and exact Selection guide text as
the new YAML description, agrees or assigns justified specialist class/effort
settings within scope, renames the definition to `SKILL.md`, and updates its
catalogue link and owned references together. Preserve other sections, supporting
resources, optional-feature settings, existing work records, and unrelated work. Do not
silently drop invalid registrations, extra metadata, missing descriptions, or
conflicting old/new files: resolve them within the authorized scope before writing.
Verify all affected links and decoded catalogue equality after writes; report any
partial failure. Historical transcripts are records and are not rewritten.

## References

- [term:Activity] → [Activity concept](../agents/activity-manager/concepts/activity.md) — mandatory work context.
