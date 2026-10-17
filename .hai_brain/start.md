# Startup

## Required reading

Read these files once:
- `.hai_brain/concepts/hai.md`
- `.hai_brain/concepts/brain.md`
- `.hai_brain/concepts/memory.md`
- `.hai_brain/concepts/agent.md`

References in these files are navigation aids, not additional
required reading. Do not follow them recursively.

## Adopt the leader role

Read `.hai_brain/agents/leader/knowledge.md` and act as {leader}.

When instructed to become {name}, read
`.hai_brain/agents/{name}/knowledge.md`.

## Load workspace context

Read `.hai_memory/agent_instructions.md` if it exists.

Read `.hai_memory/state.json` if it exists.
Use it to locate the current request and specification.
Read only enough current-request context to understand its
status and next action.

If workspace memory is absent, report that fact.
Do not create it merely because startup was invoked.

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
