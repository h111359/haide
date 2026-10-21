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
`.hai/agents/catalogue.md`, then read `.hai/agents/leader/SKILL.md`
and act as {leader} in the root chat with the interface-selected model and effort.
Before spawning specialists, read `.hai/conventions/model-profiles_conv.md`.
Leader delegates startup context loading to environment-manager, including
automatic state-only initialization when
`.hai_env/` is absent; follow that role's own canonical procedures.
State is required; optional features remain disabled until chosen by the
human. Existing incomplete or incompatible environments are preserved and
reported, rather than reinitialized. Leader reports startup results with
a menu based on validated capabilities and recommends additional chat setup
after fresh initialization. Leader delegates transcript maintenance to
chronicles-manager when enabled or required by workspace instructions.

For subsequent role selection, use the framework catalogue and validated
workspace agent catalogue entries returned by environment-manager. Choose
from their catalogue selection guides before loading the selected definition
in full; do not open every role definition for selection.
Resolve specialist class and effort against local profiles and current runtime
capabilities before spawning; report unavailable settings without substitutions.
An absent profile uses only the explicitly reported environment-manager inherited
startup bootstrap. Missing profiles remain a setup choice, not invalid core state.
Framework agents remain selectable without environment. Registered workspace
definitions resolve through `.hai_env/agents/catalogue.md`, read together with
`.hai/agents/catalogue.md`; explicit
human calls may use unregistered definitions only at
`.hai_env/agents/<name>/SKILL.md`, with supplied paths identifying that
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
  `concepts/specification.md` for HAI integration and
  `agents/specification-manager/references/specification.md` for the
  authoritative format and type registry; navigate the relevant node files,
  and read that package's conventions for the leaf types being changed.

Follow a reference when its content is necessary to understand
or perform the current task. Do not read unrelated references.
Do not reread unchanged files already available in context.
