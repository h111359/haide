Review complete. No framework, registry, configuration, or Activity files changed. This was a bounded architectural and semantic review of all five definitions and their procedures, relevant shared conventions, startup/profile code, and specification package boundaries. Structural audit commands and tests were not run; this report does not claim their success.

**Recommendation:** retain three mandatory *capabilities* in core—coordination, environment/bootstrap, and Activity continuity—but stop assuming they require three separately spawned agents. Make specification management and definition authoring optional reusable packages. Preserve generic registry/schema/runtime validation in core.

### Recommended disposition

| Current role | Core capability? | Recommended installation/runtime arrangement | Judgment |
|---|---|---|---|
| **Leader** | Yes: root orchestration and user boundary decisions | Keep root role in `.hai`. | The clearest core role. A framework whose purpose includes orchestration needs a coordinator. |
| **Environment-manager** | Yes: initialization, compatible configuration, instructions, profiles | Keep its contracts/tools/procedures as core environment module. Allow Leader to execute routine module operations; retain optional specialist execution for complex repair/migration. | Its responsibility deserves an explicit boundary; an always separate AI worker is unnecessary. |
| **Activity-manager** | Yes under current mandatory-Activity policy: record identity, continuity, lifecycle | Keep Activity contract and record service core. Retain a focused records worker where useful; remove generic task execution from this role. | Stronger separation case than Environment-manager because of continuity, sole-writer coordination, and history; current scope is too broad. |
| **Specification-manager** | No: product specification is explicitly optional | Optional reusable package, installable/registered under `.hai_env/agents` when needed. Preserve a canonical distributable package rather than independent workspace forks. | Strongest extraction candidate; already deliberately portable. |
| **Agent-definition-manager** | Authoring/audit intelligence: no. Minimal registry eligibility and validation: yes. | Optional reusable development/administration package; keep shared tools and a narrow trusted installation/registration path core. | Useful framework tooling, but most workspaces need to execute agents, not author their definitions. Removing the current sole registration owner requires redesign, not just relocation. |

These are recommendations, not existing permission. Today Leader explicitly MUST delegate substantive work, MUST NOT do specialist work except the read-only startup helper, and MUST route configuration to Environment-manager: `.hai/agents/leader/SKILL.md:26–31`. Existing ownership therefore cannot simply be ignored to obtain the target architecture.

### Why separate definitions do not imply separate processes

Four different decisions are currently entangled:

1. **Capability ownership:** who is accountable for environment configuration or record history?
2. **Logical module:** where are the authoritative contract and procedures?
3. **Runtime worker:** should a separate context/model execute this particular assignment?
4. **Installation location:** is the capability guaranteed by the framework or installed for one workspace?

The existing convention already states that a `SKILL.md` does not install a runtime skill or spawn a process (`.hai/conventions/agent_conv.md:50–53`), and direct root role use retains interface settings (`:173–179`). Therefore retaining a separate environment definition/module does not technically require a new worker for every environment operation. It is Leader's current routing prohibition that imposes that runtime arrangement.

Separate definitions provide real benefits: selective instruction loading, ownership clarity, domain-specific verification, and scope boundaries. Separate workers can provide context/model isolation and an additional review perspective. They do **not** establish a security boundary here: the reviewed definitions do not introduce distinct enforced filesystem privileges or distinct tool permission sets.

For routine work, the cost is repeated selection, settings resolution, explicit five-field handoffs, returned dependencies, result review, and record routing. The mandatory handoff is detailed in `.hai/conventions/agent_conv.md:198–219`. Those costs should buy something tangible; Environment-manager's normal startup validation already has a direct deterministic helper, so spawning another worker for the same observation has little value.

### Can specialists live without Leader?

**Yes as directly called roles; no as autonomous coordinators; only Specification-manager is explicitly a fully standalone package.**

The shared Agent concept says specialists use their own inputs/references/tools, never delegate, and discuss dependencies with the human when called directly (`.hai/concepts/agent.md:93–95`). The convention expressly supports direct root role use (`.hai/conventions/agent_conv.md:177`). Leader alone may select, delegate, monitor, and coordinate other agents (`:181–190`).

Consequently:

- A human can directly use a registered specialist in the root chat to execute its own procedure.
- The specialist cannot summon Environment-manager, Activity-manager, or another specialist to supply missing prerequisites. It returns the dependency to Leader, or discusses it with its human caller.
- Root direct use avoids *spawn-model* resolution; it does not waive registration, instructions, Activity, feature, path, authority, or lifecycle requirements.
- Direct-call ergonomics are incomplete in some procedures: Activity-manager's conflict handling and transcript assignments specifically name Leader (`.hai/agents/activity-manager/SKILL.md:39`, `:74–75`). It is therefore inaccurate to call the entire current Activity workflow Leader-independent just because ordinary direct role use is permitted.
- Specification-manager expressly permits standalone work without HAI, Leader, state, profiles, Activities, or recording (`.hai/agents/specification-manager/SKILL.md:40`). Its script README explains copying the entire package and invoking it independently (`scripts/README.md:3–9`). That is materially stronger independence.

### Environment-manager versus Activity-manager

**Activity-manager can operate without an Environment-manager invocation, but currently cannot operate without compatible environment evidence.**

Its procedures require *caller-validated compatible environment and activities.location*, then perform their own local safety checks; they do not require a live Environment-manager process or a fresh Environment-manager invocation (`.hai/agents/activity-manager/procedures/discover-and-create.md:15–23`; `SKILL.md:63`).

Leader can get that configuration evidence directly from the read-only helper (`.hai/agents/leader/procedures/startup.md:32`). Once supplied, Activity-manager discovers/maintains records independently. Environment-manager deliberately does not discover current records or manage their lifecycle (`.hai/agents/environment-manager/SKILL.md:24`).

The dependency is therefore:

> Activity record operation → compatible environment/store assurance → configuration contract/helper  
> **not** Activity record operation → always invoke Environment-manager.

If Environment-manager's *role* disappears but its core schema, helper, initialization, and configuration ownership are provided elsewhere, Activity-manager can still function. If its whole package disappears unchanged, startup currently breaks.

Conversely, environment validation/minimal initialization can run before any Activity exists. Ordinary substantive configuration needs Activity context (`.hai/agents/environment-manager/procedures/configure-features.md:20`). These bootstrap exceptions prevent a strict initialization cycle, but the current architecture still introduces significant orchestration coupling.

### Activity-manager has two different jobs

Its record/lifecycle ownership is coherent. Its ability to perform arbitrary assigned clarification, analysis, planning, implementation, and verification is a general task-executor remit (`.hai/agents/activity-manager/SKILL.md:17–20`), exercised by `procedures/work-and-revise.md:28–48`.

That has consequences:

- The default “advanced/high” worker (`SKILL.md:6–7`) is also used for routine record work.
- “Activity ownership” can become a catch-all execution destination, competing conceptually with domain specialists.
- Moving the whole role would move both mandatory continuity and general fallback execution out of core.
- Leader cannot compensate today, because it is forbidden to do substantive execution itself.

I recommend a focused core Activity records/lifecycle module or worker, with optional transcript procedures, and an explicit separate general executor/domain workers for actual task work. Record ownership should not imply subject-matter ownership.

### Invocation and operation matrix

“Selectable” and “able to perform the requested operation” must be distinguished. A role can remain selectable for diagnosis while its substantive procedure is blocked.

| Situation | Leader | Environment-manager | Activity-manager | Specification-manager | Agent-definition-manager |
|---|---|---|---|---|---|
| No initialized/compatible environment | Root startup/diagnosis works; substantive HAI work waits | Diagnosis and authorized setup/repair can work | Dependent discovery/record/substantive work blocked without validated usable context | HAI-managed product work blocked; genuine standalone package work is separately allowed | Independent format checks/prerequisite diagnosis work; substantive maintenance/audits need Activity |
| Missing/unreadable fixed instructions | Bounded diagnosis/setup only | Diagnose or authorized initialization/repair | Dependent work blocked | HAI-dependent work blocked; cannot relabel it standalone | Dependent work blocked except permitted diagnosis |
| Missing profiles | Root/helper works | Narrow inherited-settings startup bootstrap allowed | Normal spawned invocation blocked until resolved profile or explicit supported override | Same for spawned invocation | Same for spawned invocation |
| Present malformed profiles or unsupported model/effort | Root/helper works | No absent-profile bootstrap; explicit supported override may unblock | Affected spawn blocked | Affected spawn blocked | Affected spawn blocked |
| Specification disabled | No HAI product-specification delegation | May configure under scope | Activity work continues | HAI product-specification work blocked; framework/package maintenance is allowed | Definition review/maintenance continues within its prerequisites |
| Chronicles disabled, no independent obligation | Ordinary work continues | Configuration works | Record/lifecycle works; no transcript/checkpoint creation | No intrinsic effect | No intrinsic effect |
| Missing durable transcript source | Ordinary task delivery can continue unless mandatory timing applies | No intrinsic effect | Recording/verification blocked; enabled-recording closure blocked; ordinary Activity work is not generally disabled | No intrinsic effect unless its action separately requires evidence | Same |
| Closed Activity | New substantive work needs a new linked Activity | Ordinary new substantive work needs current context | Attributable supplements/old-source catch-up allowed; new substantive continuation blocked | New substantive work needs new Activity in HAI mode | Same |
| Role unregistered/invalid definition | Affected role cannot be selected | Same | Same | Same in HAI selection | Same; target definitions may still be inspected as data |
| Caller is a specialist | Cannot be spawned as replacement Leader | Cannot be summoned by that specialist | Cannot be summoned by that specialist | Cannot be summoned by that specialist | Cannot be summoned by that specialist |

Controlling evidence:

- Mandatory Activity context includes advice, analysis, maintenance, implementation and verification; only bounded startup/setup and read-only prerequisite diagnosis bypass it: `.hai/conventions/agent_conv.md:55–77`.
- Registration is required even for an explicit human name/path: `:14–20`.
- Framework roles remain selectable without initialization; workspace roles depend on validated workspace catalogue use: `:5–7`; `.hai/tools/startup/startup_check.py:320–325`.
- Unsupported settings block the affected spawn, while root chat and independent work remain possible: `.hai/conventions/model-profiles_conv.md:49–69`.
- Absent-profile bootstrap covers Environment-manager validation/minimal initialization only; Activity-manager uses normal settings: `:78–98`.
- Specification's enabled/compatible gate, standalone-bypass prohibition, and framework-maintenance exception: `.hai/agents/specification-manager/SKILL.md:40–45`.
- Transcript source/coverage failures block enabled closure, not universal agent availability: `.hai/agents/activity-manager/SKILL.md:56–58`; `.hai/agents/leader/procedures/coordinate-recording.md:57`.

A new chat creates no new Activity by itself. Conflicting current work requires a boundary decision; inconsistent current-record discovery leaves downstream substantive work pending (`.hai/conventions/agent_conv.md:66–71`; `.hai/agents/leader/procedures/coordinate-activity.md:35–43`).

### Hidden core couplings and migration implications

**Environment package:** startup imports shared agent utilities (`.hai/tools/startup/startup_check.py:11–13`) and hardcodes the environment template and installed contract (`:19–20`). Existing-state validation loads that template from the target workspace path (`:306`), while the contract is installed-helper-relative (`:297`). Folder relocation alone therefore breaks required resources. Move shared contracts/defaults to a stable core module or explicitly update the helper and references.

**Activity package:** core agent conventions, Leader, framework-layout, state and HAI/environment concepts directly link to Activity-manager-owned concepts/conventions. Activity is mandatory by policy. Extraction requires retaining a core contract/service or explicitly changing the mandatory-Activity architecture; deleting the worker folder is not enough.

**Specification package:** its helper is package-relative and uses only standard-library imports (`.hai/agents/specification-manager/scripts/audit_specification.py:5–18`, `:32`). This is a good package boundary. Minimal extraction can retain standardized optional specification flag/location in core state while moving the executor and repairing registrations/links. A stronger extension architecture could transfer configuration to an opaque extension subtree, but that is **optional deeper redesign**, not required by folder relocation. Today required FEATURES and path validation still name specification (`.hai/tools/startup/startup_check.py:15`, `:165–178`).

**Definition authoring:** shared `agent_tools.py` belongs to `.hai/tools`, and startup imports it. Optionalizing the authoring role should leave generic JSON/catalogue/profile/definition validation core. Current registration routes require an already registered/invocable Agent-definition-manager (`.hai/agents/leader/procedures/register-agent.md:23`, `:35`). Moving it into a workspace catalogue makes bootstrap and damaged-catalogue recovery harder. A narrow trusted registration/installation path must exist before that owner becomes optional.

**All moves:** update origin catalogue rows, canonical paths, relative references, ownership statements, collision checks, and recovery/bootstrap procedures together. Moving a core role into `.hai_env` without removing its old registration creates a conflicting name; framework definitions take precedence and workspace collisions are invalid (`.hai/conventions/agent_conv.md:9–12`). Existing update policy preserves origin/path unless an explicit migration authorizes otherwise (`.hai/agents/agent-definition-manager/procedures/update-definition.md:24`).

**Minimal viable migration:** extract Specification-manager first, retaining standardized core configuration. Then separate core validation/registration services from optional definition authoring. Refactor Environment-manager into a callable core module before relaxing Leader's execution restriction. Narrow Activity-manager last, preserving mandatory continuity and history semantics.

None of the five roles is inherently specific to this repository. Specification and definition authoring are **optional but reusable**. Workspace-specific release, Git, product, team, and policy roles are a different category. `.hai_env` can be their installation location without implying that their reusable upstream definitions should be independently maintained for every workspace.


### Leader-reviewed supplementary recommendation — 2026-11-01T10:28:11Z

Provenance: Agent-definition-manager supplied the preceding report from `/tmp/hai-core-agent-analysis.md`; it is preserved verbatim above. Its opening statement about unchanged Activity files describes that specialist's review, before this report was saved. Leader supplied and reviewed this supplementary proposal for the final architectural recommendation.

After narrowing Activity-manager to records, prefer explicitly revised Leader permission for short ordinary task execution. Use optional domain or general workers when specialist expertise, context isolation, parallel execution, or independent review warrants the extra handoff. Do not introduce a compulsory generic worker that merely replaces forced Activity-manager execution. This clarifies and supersedes any reading of the report's “explicit separate general executor/domain workers” recommendation as requiring a separate general worker for every ordinary task.

The current Leader prohibition on substantive execution remains in force. Implementing this recommendation requires a future explicit design decision and authorized instruction changes; this analysis grants no new execution permission. Core coordination/environment/bootstrap/Activity capabilities remain the recommendation, with a callable environment module for routine Leader-executed operations, a focused Activity records worker where useful, optional reusable specification and definition-authoring packages, and generic validation/registration support retained in core.

Verification and limits: the supplied evidence is a bounded manual architectural and source review of the five roles and relevant procedures/tools, not an independently rerun audit. No structural test or audit-command success is claimed. Framework edits, moves, registration/configuration changes, implementation and closure remain unauthorized. Future design choices are for the user.
