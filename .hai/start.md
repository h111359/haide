# Startup

## Required reading

Read these files once:
- `.hai/concepts/hai.md`
- `.hai/concepts/environment.md`
- `.hai/concepts/agent.md`

References in these files are navigation aids, not additional
required reading. Do not follow them recursively.

## Adopt the leader role

Read `.hai/conventions/agent_conv.md` and the leader entry in
`.hai/agents/catalogue.md`, then read `.hai/agents/leader/knowledge.md`
and act as {leader}. Leader delegates startup context loading to
environment-manager; follow that role's own canonical procedures.

For subsequent role selection, use the framework catalogue and validated
workspace agent catalogue entries returned by environment-manager. Choose
from their catalogue selection guides before loading the selected definition
in full; do not open every role definition for selection.
Framework agents remain selectable without environment. Registered workspace
definitions resolve through environment state's `agents` object; explicit
human calls may use unregistered definitions only at
`.hai_env/agents/<name>/knowledge.md`, with supplied paths identifying that
canonical folder or file, without registering them. Follow the agent convention
for conflicts and invalid references; never implicitly override framework roles.

## Load further knowledge when needed

Before performing a task, identify and read the concepts,
conventions, and role instructions that govern that task.

Examples:
- Managing a request: read `concepts/request.md`.
- Creating or editing a concept: read
  `conventions/concept_conv.md`.
- Working with specification content: read
  `concepts/specification.md`, navigate the relevant node files,
  and read the conventions for the leaf types being changed.

Follow a reference when its content is necessary to understand
or perform the current task. Do not read unrelated references.
Do not reread unchanged files already available in context.
