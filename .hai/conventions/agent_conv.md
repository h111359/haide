# Agent convention

## Identity and availability

Framework definitions live at `.hai/agents/<name>/knowledge.md` and are
always selectable, including without environment. The separate
[framework catalogue](../agents/catalogue.md) contains their names, short
actionable selection guides, and definition paths. Its guides are verbatim
copies of canonical Selection guide sections in knowledge definitions;
it does not duplicate their procedures.
Workspace definitions live at `.hai_env/agents/<name>/knowledge.md`.
Names use lowercase ASCII words separated by single hyphens, matching
`[a-z][a-z0-9]*(?:-[a-z0-9]+)*`. Names must be unique across both origins,
also when compared case-insensitively on supported platforms.

Only workspace agents registered in environment state's `agents` object
are normally selectable. An explicit human call may select an unregistered
workspace definition at `.hai_env/agents/<name>/knowledge.md`; a supplied
path must identify that canonical folder or its knowledge file and remain
inside the workspace after resolution. This neither registers it nor
authorizes registration. Do not search
unrelated locations. Ask for a path when the target is ambiguous.

Report conflicting workspace definitions or registrations as invalid.
The framework definition takes precedence for a conflicting name, including
after upgrades; explicit invocation cannot bypass this rule. Never silently
rename, override, unregister, or repair definitions. An invalid workspace
entry does not make framework agents unavailable.

## Selection and loading

Select from the guides in the framework catalogue and valid environment-state
catalogue entries. Each catalogue guide is a verbatim copy of the canonical
Selection guide section in its agent's knowledge.md. A guide briefly states when to call the role and what
it produces; it must agree with the definition's scope and ownership. Do not
read every knowledge file to choose a role or recover missing guides. Read the
full `knowledge.md` only for a selected role, or when a specific ownership
question requires its procedures, then follow conditional references.
Catalogue-only ordinary selection does not require opening definitions to
compare every guide copy. If a mismatch is discovered while loading or
reviewing a definition, report it; do not silently repair a catalogue or state.
An explicit call has already selected its target and needs no catalogue entry;
validate its identity and load its definition without registering it.
Load shared workspace instructions and this
convention before executing a role. References are not recursive read-all
instructions.

## Required knowledge format

Every definition has one title and exactly these level-two headings, once
each and in this order. Use subheadings for task-specific detail. Write
`None` when a section has no applicable content; do not omit headings.
This skeleton is the common knowledge template:

```markdown
# <Agent name>

## Selection guide
<Briefly say when to call this role and what it produces.>

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
<Constraints and any role-specific missing-input behavior.>

## Procedures
<Actions and conditional workflows.>

## Expected outcome
<Deliverables, validation evidence, and unresolved issues.>

## References
<Path — purpose — required, conditional with trigger, or optional.>
```

Definitions apply to the agent definition and its supporting files. Link
shared terminology instead of redefining it. Aliases must identify their
target and scope explicitly; they abbreviate references or names, not
grant authority or invent runtime values. Do not implicitly expand aliases
into commands or paths. Validate supplied paths before using them.

Inputs may be user decisions, task context, existing files, permissions,
or tool prerequisites. Unless a role specifies its own response, first
retrieve missing mandatory inputs from already available, authorized
context; then report or ask through the leader and pause dependent work.
Continue meaningful independent work. When called directly, ask the human
directly. Optional inputs use declared defaults; otherwise they remain
absent. Never fabricate values, decisions, or approval.

Rules state constraints; Procedures describe actions. References list
additional files or folders with purpose and reading conditions. A folder
reference must identify what relevant content to read; it does not require
loading every descendant. References may point to existing resources beyond
the standard folders.

## Independence and supporting resources

Only leader selects, delegates to, and coordinates other agents.
Specialists perform their own procedures using their inputs, shared
references, and tools; they do not invoke other agents. They return missing
dependencies to leader instead of coordinating specialists themselves.
Each role owns its procedures in its `knowledge.md`; callers describe the
delegated task without duplicating the receiving role's procedures.

Optional standard folders are `scripts/` for owned executable helpers and
usage documentation, and `conventions/` for role-specific formats and rules.
Create them only when needed. Other justified resources and folders are
permitted, including existing `templates/`; no empty scaffold is required.
Shared concepts and conventions retain their canonical framework location.
Scripts follow [tooling_conv.md](tooling_conv.md).

## Registration ownership and verification

The workspace-agent-creator owns creation-time workspace registrations;
environment-manager owns general environment state and validation. Neither
may silently repair the other's data. Preserve unrelated state properties.
Registration follows definition validation, never precedes it. Coordinate
definition and state writes without claiming filesystem transactionality:
on failure report completed changes and remaining inconsistencies, preserve
partial results, and do not retry, remove, or overwrite them silently.

Validate names, canonical paths, collisions, all required headings and their
order, local aliases, required inputs, output criteria, conditional
references, specialist independence, and consistency with shared rules.
Validate the canonical guide against scope, then validate its catalogue copy
for exact equality when creating or updating an agent or its entry. Author
the knowledge section first and copy its text verbatim into the framework
catalogue or workspace state's `selection_guide`; do not independently rewrite
the copy. Exclude the heading and surrounding separator blank lines from the
copied body, but preserve its text, punctuation, escaping, and internal whitespace.
Use a short single paragraph compatible with a Markdown table cell; JSON escapes
must decode to exactly that same text. Knowledge definitions have ten required
headings. Startup does not require scanning all definitions to verify copies.
Verify only meaningful supporting scripts with the tooling convention.
