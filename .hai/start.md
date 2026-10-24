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
Leader first runs the read-only [startup helper](tools/startup/README.md) for
existing-state validation and bounded context loading. This is a narrow root-role
execution exception; it does not authorize manual environment changes. Use its
independent results and report isolated issues without treating a nonzero exit as
absent state. Delegate safely absent state initialization, or validation when the
helper cannot run, to environment-manager under its canonical procedures. Only
that role initializes state, preserving existing containers and unrelated resources.
State is required; optional features remain disabled until chosen by the
human. Existing invalid or incompatible state is preserved and
reported, rather than reinitialized. Leader reports startup results with
a menu based on validated capabilities and recommends additional chat setup
after fresh initialization. Leader routes enabled or required transcript maintenance
to chronicles-manager asynchronously, using completed messages from the durable
saved session source. Delivery does not wait for optional recording. If the runtime
cannot continue after delivery, catch up on the next active turn and report deferred
recording accurately; mandatory workspace timing requirements take precedence.

For subsequent role selection, use the framework catalogue and validated
workspace agent catalogue entries returned by the helper or environment-manager. Choose
from their catalogue selection guides before loading the selected definition
in full; do not open every role definition for selection.
Resolve specialist class and effort against local profiles and current runtime
capabilities before spawning; report unavailable settings without substitutions.
The read-only helper needs no model profile or specialist invocation. An absent
profile uses the explicitly reported environment-manager inherited startup bootstrap
only when delegation is needed. Missing profiles remain a setup choice, not invalid core state.
Registered framework agents remain selectable without environment. Registered workspace
definitions resolve through `.hai_env/agents/catalogue.md`, read together with
`.hai/agents/catalogue.md`; explicit
human calls may use unregistered definitions only at
`.hai_env/agents/<name>/SKILL.md`, with supplied paths identifying that
canonical folder or file, without registering them. Unregistered framework definitions
may be inspected or maintained, but require registration before execution. Follow the agent convention
for conflicts and invalid references; never implicitly override framework roles.

## Load further knowledge when needed

After selecting a role, follow its required knowledge and task-specific
references before performing the task. Read applicable shared authoring
conventions when creating or changing framework resources.

Follow a reference when its content is necessary to understand
or perform the current task. Do not read unrelated references.
Do not reread unchanged files already available in context.
