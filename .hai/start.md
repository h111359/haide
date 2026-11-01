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
and act as leader in the root chat with the interface-selected model and effort.
Before spawning specialists, read `.hai/conventions/model-profiles_conv.md`.
Leader first runs the read-only [startup helper](tools/startup/README.md) for
existing-state validation and bounded context loading. This is a narrow root-role
execution exception; it does not authorize manual environment changes. Use its
independent results and report isolated issues without treating a nonzero exit as
absent state. Delegate safely absent state initialization, or validation when the
helper cannot run, to environment-manager under its canonical procedures. Only
that role initializes state, preserving existing containers and unrelated resources.
State and the fixed `.hai_env/agent_instructions.md` are mandatory. Always load the
safe instructions file independently of state validity; empty content is valid,
while missing/unreadable content blocks dependent work and must be reported.
Initialization or explicitly authorized migration may create the empty file;
startup validation never silently repairs an initialized environment.
Activities are mandatory; specification and chronicles remain disabled until chosen
by the human. With compatible validated context, leader routes current-record
discovery to Activity-manager, resuming the current Activity when present. A new
chat alone creates none. Meaningful new substantive work with no current record
creates one; conflicting current/new intent requires a boundary decision. Startup
validation, necessary bootstrap/setup and read-only diagnosis may precede a record.
All subsequent substantive work, including advice and analysis, belongs to an Activity. Existing invalid or incompatible state is preserved and
reported, rather than reinitialized. Leader reports startup results with
a menu based on validated capabilities and recommends additional chat setup
after fresh initialization. Leader assigns exact source exchanges to Activities
and routes enabled or required transcript segments to Activity-manager's separate
recording procedures. For ordinary enabled recording, keep a coordination count of
eligible user prompts and dispatch an asynchronous batch at the validated
`features.chronicles.record_every_prompts` threshold, default 5. Rebuild from exact
source identities and the returned Activity-local checkpoint after resumption;
dispatch progress is distinct from verified coverage. Do not invoke an agent or
write configuration merely to count each prompt. Serialize writers for one stable
Activity and retain source assignments across Activity switches. Ordinary Activity
edits do not force transcript synchronization. Segments live under their Activity,
never a global chronicles location. Enabling recording covers subsequent exchanges
without implicit off-period backfill. Ambiguous attribution is resolved by Leader
with the human. Ordinary delivery does not wait for a recording batch. Before an
authorized closure with recording enabled or independently mandatory, Activity-manager
freshly verifies required coverage through the closure request; missing source or
gaps block closure. Disabled/no-obligation closure has no transcript prerequisite.
Without supported after-turn continuation, retain pending replies for a later
active-turn batch or explicit flush rather than promise a background worker.
Mandatory workspace timing requirements take precedence.

For subsequent role selection, use the framework catalogue and validated
workspace agent catalogue entries returned by the helper or environment-manager. Choose
from their catalogue selection guides before loading the selected definition
in full; do not open every role definition for selection.
Resolve specialist class and effort against local profiles and current runtime
capabilities before spawning; report unavailable settings without substitutions.
The read-only helper needs no model profile or specialist invocation. An absent
profile uses the explicitly reported environment-manager inherited startup bootstrap
only when delegation is needed. Missing profiles remain a setup choice, not invalid core state.
Only agents with valid entries in their origin's catalogue may be selected for
execution or receive delegated work. Registered framework agents remain selectable
without environment. Registered workspace definitions resolve through
`.hai_env/agents/catalogue.md`, read together with `.hai/agents/catalogue.md`.
An explicit name or path does not bypass registration or authorize it. Unregistered
definitions in either origin may be inspected, maintained, validated, or registered
without executing them. Creation and registration remain separate operations.
Follow leader's registration handoff when registration is requested, and the agent
convention for eligibility, conflicts, and invalid references; never implicitly
override framework roles.

## Load further knowledge when needed

After selecting a role, read its shared rules and Procedures index. Follow the
applicable trigger to its procedure file, or the sole inline procedure, then read
that procedure's required references before executing it. Bind its local inputs
explicitly; matching names in other procedures do not supply values. Procedure
Rules add only procedure-specific obligations; shared role rules still apply and
are not overridden. `None.` means no additional local rules. Prerequisites are
entry conditions; Steps supply ordered actions and conditional branches. Procedure
execution stays in the selected role and is not another agent delegation. Read applicable shared authoring
conventions when creating or changing framework resources.
The shared [instruction-writing convention](conventions/instruction-writing_conv.md)
defines plain rule wording and MUST/MUST NOT/MAY. It changes neither task permission
nor input requirement labels; authoring behavior remains with agent-definition-manager.

Follow a reference when its content is necessary to understand
or perform the current task. Do not read unrelated references.
Do not reread unchanged files already available in context.
