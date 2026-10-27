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
links. Normal selection requires registration in the corresponding catalogue for
both origins. Creation alone does not register a definition. An explicit
human call may select an unregistered workspace definition without registering it; supplied
paths must identify its canonical folder or `SKILL.md` and resolve inside the
workspace. Unregistered framework definitions may be maintained or inspected but
must be registered before execution. Do not search unrelated locations. Ask for a
path when ambiguous. Before definition creation or registration, check both
catalogues and immediate folder names in both origins for case-insensitive
collisions, including unregistered folders; this does not authorize loading every
definition or discovering unregistered roles during ordinary selection.

## Selection and loading

Read the framework catalogue and valid workspace entries together. Catalogue
Selection guide cells are exact copies of the decoded YAML `description` value,
which is canonical selection text. Descriptions briefly state when to call a role
and what it produces, consistent with its scope and ownership. Select from copies
before loading the selected `SKILL.md`; do not open every definition to choose a
role or recover missing descriptions. An explicit call already selects its target.

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

There is no agent H1 title or Selection guide body section. Include exactly these
nine level-two headings once each, in order; use subheadings for task detail and
write `None` for an inapplicable section:

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
<Responsibilities, ownership, and boundaries.>

## Definitions
<Local terms and aliases, or None.>

## Required inputs
<Inputs and prerequisites, or None.>

## Optional inputs
<Optional inputs and declared defaults, or None.>

## Rules
<Constraints and role-specific missing-input behavior.>

## Procedures
<Actions and conditional workflows.>

## Expected outcome
<Deliverables, validation evidence, and unresolved issues.>

## References
<Path — purpose — required, conditional with trigger, or optional.>
```

Definitions apply to the agent and its supporting files. Link shared terminology
instead of redefining it. Aliases identify their target and local scope; they do
not grant authority or supply runtime values. Validate paths before use. Retrieve
missing mandatory inputs from available authorized context first, then return the
dependency to leader or ask the human when called directly. Continue independent
work; optional inputs use declared defaults or remain absent. Never invent values,
decisions, permissions, or approval. References give reading conditions; a folder
reference identifies relevant content rather than requiring recursive loading.

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
owns its procedures in `SKILL.md`; callers describe the task without duplicating
those procedures. Runtime spawn interfaces may impose additional constraints:
when explicit model/effort overrides require an empty history fork (for example
`fork_turns="none"`), use that supported combination and pass the definition path,
workspace instructions, relevant task context, and expected outcome explicitly.
Do not assume inherited history, settings, or automatic skill discovery.

Git-manager owns Git and GitHub execution, including repository-state inspection.
Other roles return those needs to leader, who supplies validated integration context
and routes them to git-manager; specialists never call one another. Disabled or
invalid integrations are not bypassed through another role or tool. Ordinary
filesystem work and definition validation do not require Git. Integration enablement
permits scoped operations; it does not require approval for every routine check or
grant authority for unrelated, destructive, or otherwise unauthorized publication.
Agent-executed pushes additionally require valid enabled automated-push settings;
off means manual pushing, with no tool or role bypass. Leader obtains fresh
git-manager readiness evidence before environment-manager may enable that capability.

Every commit-producing operation requires a fresh pre-commit chronicle refresh
through leader before git-manager creates the commit. Follow git-manager's
[pre-commit gate](../agents/git-manager/conventions/git-github_conv.md#pre-commit-chronicle-gate);
ordinary asynchronous recording and a previous operation's refresh do not satisfy this
per-operation dependency. Unavailable recording requires resolution or an explicit
user exception, never an implicit bypass. This does not block independent
filesystem work or require recording future outcomes.

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
selected definition path, applicable workspace instructions and context, expected
output, and relevant verification requirements. Supply concise facts and precise
references the receiver can access; do not reproduce full conversation history
or duplicate the specialist's procedures. Inherited history does not replace this
handoff, and a follow-up must make retained context and changed requirements clear.

Before dependent work, the receiving specialist MUST load its definition and
applicable instructions, compare the handoff with its own **Required inputs**,
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

Optional standard folders are `scripts/` for owned helpers and usage documentation
and `conventions/` for role-specific formats. Other justified resources, including
existing `templates/`, remain permitted. Create no unused scaffold. Framework-wide
concepts and conventions retain their canonical framework location. A role's domain
knowledge may live in its package as the single public authority, with shared readers
linking to it rather than duplicating it. Scripts follow
[tooling_conv.md](tooling_conv.md).

## Registration ownership and verification

Agent-definition-manager owns framework and workspace definition creation, updates,
audits, and explicitly requested catalogue registrations. Creation and registration
are separate; an explicit combined operation may perform both. Updating a registered
definition synchronizes its existing catalogue description and canonical reference;
updating an unregistered definition never adds a row. Framework maintenance and
read-only definition inspection need no initialized environment; workspace mutations
retain the valid initialized environment prerequisite. Environment-manager owns
configuration, model profiles, and the lightweight startup-validation policy; leader
may execute the shared read-only startup helper directly under its bounded exception
and otherwise owns selection and execution. Initialization, configuration changes,
repairs, and migration remain environment-manager work. Audits do not repair, rename,
unregister, or delete.
Neither role silently repairs the other's data. Preserve unrelated state, rows,
and prose. Register only after validating the definition.
Coordinate writes without claiming multi-file transactionality: stop on changed
inputs, preserve partial results on failure, and report inconsistencies without
automatic retries, removal, or overwrite.

Validate names, canonical paths, collisions, YAML fields, string metadata,
model/effort declarations, all nine headings and their order, local aliases,
inputs/defaults, outcome criteria, conditional references, independence, and shared
rules. Author `description` first, then copy its decoded value into the catalogue
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
