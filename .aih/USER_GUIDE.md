# AIH user guide

Core version 1.0.0 · schema version 1.0 · Python 3.11+ · standard-library Python infrastructure.

AIH supports one logical product, one open change request and one active operational action. It uses ordinary files and a local portal. This guide is shared by the portal, menu and CLI; the live `operations` catalog provides installed operation metadata.

<a id="quick-start"></a>
## Start and first use

From the directory containing `.aih/`:

```sh
python -B .aih/engine/cli.py help
python -B .aih/engine/cli.py init
python -B .aih/engine/cli.py serve --port 8765 --no-browser
```

Open the printed local URL. `python -B .aih/engine/cli.py menu` opens the same Python menu used by `.aih/menu.sh` and `.aih\menu.cmd`. Windows may use `py -3 -B`; Linux may use `python3 -B`. The wrappers locate their own installation, including when launched from another directory. Quote paths with spaces. Python is required; missing-runtime diagnostics should direct you to install Python independently. Menu Exit and portal/server Stop are distinct from stopping product work; observe the menu's server ownership prompt.

Use `python -B /absolute/home/.aih/engine/cli.py --home /absolute/home status` from another working directory. The chosen home must contain the installed core; an arbitrary current directory never becomes a second state root.

Initialization is idempotent and preserves human files. The first portal start initializes absent state and attempts documentation bootstrap. Invalid or partial existing state is reported for recovery, not reset. Configure the workspace and an available profile, then explicitly continue `reverse-engineer`. Complete documentation for every configured product area is required before the first/new request opens. Inventory alone is insufficient. Setup remains pending when semantic interpretation, local coverage, permissions or profile prerequisites are missing. Setup/drafts/Q&A remain available while pending and idle; active setup has Stop-only controls.

<a id="portal"></a>
## Portal pages and request tabs

The eight primary pages are Overview, Current request, Ask a question, Product documentation, Runs and recovery, History and decisions, Settings and Help. Overview explains current status, owner, blockers and next permitted action. Current request owns input and lifecycle work. Product documentation follows canonical knowledge and notices. Ask a question is the independent read-only lane. History and decisions browses closed requests without reopening or queueing them. Runs and recovery exposes logs, evidence, process state and task outcomes. Settings contains Workspace, profiles, skills, supported declarative settings and deliberate human custom instructions. Help reads this guide without agent execution.

Current request has six tabs: Input and clarification, Analysis, Plan, Implementation, Verification and documentation, and Outcome. Input and clarification distinguishes saved drafts from submitted directions and contains explanations, authoritative answer drafts, requestor exports/import review and amendments. Analysis keeps interpretation, questions, architectural assessment and unrelated issues separate. Plan shows generated version, requirements/workspace bindings and explicit approval. Implementation shows sequential task progress and logs. Verification and documentation displays required checks and documentation increments. Outcome distinguishes incomplete evidence, Ready to close and closed outcomes.

Light and dark theme selections affect appearance only. Disabled controls explain state constraints. While busy, passive navigation, existing output/help and downloading an existing form remain available; Save, imports, diagnostics, settings, approvals, questions and closure are refused. A stale browser view receives a revision conflict and must refresh/reconcile instead of overwriting a newer edit.

<a id="appearance"></a>
### Appearance

Settings → Appearance offers Clear, Midnight, Warm, High contrast and System themes, plus a custom declarative preset. Base text size is 14–22 pixels. Custom presets select local font families and named semantic colors; arbitrary CSS, HTML and remote fonts are refused. The backend validates complete six-digit colors and text/focus contrast before saving. A rejected preset stays a draft for correction. Saving appearance is an explicit idle settings action and never invokes an agent.

<a id="workflow"></a>
## Change workflow and authority

Save draft records input without submitting it or invoking an agent. Clarify explicitly submits relevant saved input, answer revisions and pending saved amendments. It establishes what must change and why, with observed current behavior, scope, constraints and acceptance criteria. Clarify may inspect source and record evidence-backed defects/staleness, but cannot redesign/repair implementation or rewrite business meaning.

Repeat Clarify after partial answers, changed wishes or corrections. Previously accepted wording and source revisions remain linked. An unchanged invocation reuses valid evidence and states unresolved questions. Once requirements are ready, choose Analyze separately. Analyze considers design, tradeoffs, dependencies, risks and verification, asking consequential design questions if needed. Repeat Analyze with answers until it automatically generates the sequential plan. There is no separate Plan command.

Approve the exact current plan, then choose Implement. Approval alone does not start execution. Every plan binds requirements, source/instruction and workspace revisions; each task names its intended result, specific root-qualified paths/action types, dependencies and completion evidence. Implementation runs tasks sequentially, including test authoring, full regression verification, authorized repairs/reruns, documentation application/verification and results. Material scope/approach changes require revised planning and applicable approval.

Implement directly is an explicit alternative that authorizes implementation of the submitted scope and internally generates/persists the same plan before changes. It does not fabricate approval or bypass missing requirements, unrelated-defect selection, test obligations, workspace reconciliation or documentation.

Ready to close is still an open request. Close successfully is a separate human action that rechecks all completion gates and archives the whole record. Failed/stale/unexecuted required tests cannot be accepted as exceptions. Cancelled or rejected closure preserves partial work and records a current-state notice; it is separate from Stop execution. Stop retains the request and acknowledges completed/incomplete task boundaries after safe termination. No next action runs automatically, and there is no pending-command queue.

<a id="clarification"></a>
## Questionnaires and requestor exchange

The request's editable Markdown questionnaire is the authoritative answer source. Every question has stable identity/revision, context, respondent, plain-language explanation, why it matters, how to answer, optional neutral illustration, free text and required/optional status. Recommended options start unchecked. Choices cannot silently contradict free text; malformed or mutually exclusive selections require resolution. You may reassign the intended respondent while idle.

At a waiting clarification round AIH exports outstanding marked Requestor questions to an immutable UTF-8 `.txt` file. The requestor needs only a text editor: retain Request/Form/question references, mark `[x]` choices or type after Answer/Comments, and return the file. Unknown/Needs discussion and partial responses are allowed. Explanations concern business needs, not forced architecture. Existing exports can be viewed/downloaded while busy; regenerating is an idle operational action. Unchanged forms are reused; prior versions remain available. Downloading a file neither sends it externally nor proves delivery.

Upload requestor answers accepts file selection/drop or Paste answers; the supported interchange is UTF-8 text up to 1 MiB. Sensitive input is rejected before normal receipt/log persistence; correct the original and resubmit. Accepted originals retain receipt ID/fingerprint and are staged only. Import cannot approve a plan, enable skills, change permissions/instructions or start implementation.

Review the original question/explanation, existing answer, received answer and match state. Match by request/form/question identity and revision. Duplicate, unknown, missing, altered, stale, withdrawn or conflicting items need explicit resolution; manual matching records provenance. A wrong/closed request form remains unassigned intake rather than reopening another request. Blank and unknown answers never become invented responses. Comments introducing a new wish can be explicitly linked to one amendment/input effect.

Receipt review displays the original respondent and received text, choices and comments. Accept matched is a convenience for unique matches. Duplicate rows stay unresolved except for at most one explicit reviewed decision or correction for each current question; no repeated row silently overwrites another answer.

Save reviewed answers saves drafts only. Import answers and clarify is the explicit combined submission: reserve the action, merge reviewed drafts, snapshot selected input/answers/amendments and start Clarify. No second generic approval dialog is required after review. Changed displayed revisions require refresh. Repeated clicks cannot duplicate effects. If launch fails, the accepted submission remains inspectable for explicit Resume; it is not a queued later action. Busy intake is refused without saving a replacement submission.

<a id="amendments"></a>
## Amendment history and file editing

Save an amendment with a stable ID to capture changed wishes or additional information. AIH preserves every accepted framework Save and submitted revision, original wording, attributed source, actual submitter, order, supersession/withdrawal and interpretation effect. Draft, saved-not-submitted, submitted, applied, superseded, withdrawn and needs-clarification states are distinct. A correction or withdrawal adds a revision rather than erasing history.

File-only users may edit permitted input/answer/amendment files directly. They remain unsubmitted drafts until an explicit idle Save/intake/submission observes and validates them. Intermediate external saves that AIH never observed are not claimed as recorded. Use `save-amendment` each time you need a revision captured. Repeated submission does not reapply an already adopted amendment. Contradictions with imported answers require interpretation reconciliation and may invalidate downstream plan/evidence. History survives all closure outcomes.

<a id="workspace"></a>
## Multiple folders and human administration

Settings → Workspace lists stable root IDs, display names, canonical paths, purposes and selected read-write/read-only modes. Home is the canonical parent of the sole `.aih/` and `.aih_product/`; it is mandatory writable and cannot be removed/relocated through an ordinary additional-folder edit. Additional folders may be noncontiguous or on other drives. Each is explicit; a common ancestor and unrelated siblings remain outside the workspace. Separate Git repositories are optional.

Use Add folder, Edit, Validate access and Remove from workspace only while globally idle. This includes an open/blocked/Ready-to-close request whose worker has stopped. Only deliberate human administration changes membership/access; an agent may suggest a needed folder in output but cannot register it. A saved registry change never starts an agent, moves files or grants implementation scope. It preserves old mappings/revisions and marks affected analysis, approval, docs, tests and reuse stale. Unknown impact remains unresolved; unaffected evidence needs recorded justification.

Engine product references use `frontend:src/view.js`, with workspace revision in the owning record. Portable standalone contracts use `{ "root": "frontend", "path": "src/view.js" }` and an explicit workspace revision. Historical references retain old mappings and never grant current access to removed roots. Registry changes require explicit reconciliation; newly added/relocated areas need documentation baselining before implementation relies on them. With an open request, invoke reverse engineering with `within_request: true` so evidence belongs to its documentation increment. Without a request, use setup/documentation maintenance.

Example: configure home plus writable frontend/backend and read-only reference folders. Complete their baseline, open a request, then safely stop its worker. Add a separate reports folder while idle. Approval/readiness for affected work becomes stale. Explicitly baseline reports and cross-folder dependencies, rerun applicable Clarify/Analyze, and approve the revised plan before implementation. If backend becomes unavailable, dependent work blocks. Removing it does not delete files, unresolved defects, failed tests or historical mappings; explicit disposition/reconciliation remains necessary.

All managed writes—including caches, temporary data, tests, cleanup and child processes—must stay inside current writable roots and action scope. Symlink/junction/reparse escapes, duplicate/nested/aliased roots and ambiguous hard links are refused. Read-only source roots require every test output/cache elsewhere in authorized writable scope. An incompatible tool is blocked; do not widen to a common parent, copy credentials into product files or silently omit required tests. External applications operated directly by a user are not controlled by AIH.

Cross-filesystem work records per-root progress. Recovery does not assume one atomic product commit. If a path is removed/restricted before recovery, prohibited writes stay blocked until explicit authorized resolution. Old journal permissions do not re-register it. Inert temporary data is operation-owned under `.aih_product/tmp/`, excluded from inventories/fingerprints and cleaned only after ownership is reconciled. Executable fixtures/runtime artifacts belong in ordinary authorized workspace locations outside product state. Durable evidence/checkpoints/authority never exist solely in tmp.

<a id="documentation"></a>
## Product knowledge and reverse engineering

Initial/incremental reverse engineering reads source/configuration/interfaces/tests/build/deployment docs safely, collects fingerprints and supported static facts without importing product code, then uses the selected agent for evidence-based semantic interpretation. It preserves implementation, executable tests, source config and human instructions. Static facts, inferred requirements, approved intent, observed behavior, verification and unknowns remain distinguishable.

One central documentation tree covers every root. Read small navigation catalogs first and only relevant terminal leaves. Stable topic IDs survive physical reorganization; cross-links are separate from structural parentage. Defaults enforce at most eight catalog children, leaf depth difference at most one, and roughly 1,500 words per content leaf with justified indivisible exceptions. Reorganization preserves human content/IDs and commits with recoverable revision-checked operations. Supported readers lock/retry snapshots; unrelated external readers may observe intermediate filesystem state.

The applicability catalog covers 18 areas: purpose/domain; requirements; quality; architecture; workspace; data; analytics; interfaces; experience; security; dependencies; deployment; testing; recovery; observability; operations; support/known defects; additional product-specific knowledge. Each is applicable with substantive coverage, not-applicable with rationale, or unknown with explicit investigation limits. Missing required available local content blocks baseline completion. External unknowns and unverified runtime behavior may remain clearly labeled.

Source/instruction/extractor/schema/core/workspace changes invalidate affected reusable extraction/summaries. Incremental refresh inspects changed dependencies and retains valid content; unchanged documented input should not require another semantic generation call merely to repeat validation. Token efficiency never reduces required coverage or full regression tests. Compact outputs retain evidence references and label omitted detail. Actual adapter token telemetry is recorded when present; unavailable is not zero. Context bytes/model calls are proxies, not measured token savings.

Every request has `analysis/documentation_increment.yaml` linking planned topic/section changes, reasons, requirements/decisions and tasks, then application fingerprints/diffs and verification. Planned changes do not describe current implementation. A justified no-impact finding is explicit. Documentation failure blocks success. Initial bootstrap/no-request maintenance has its own audited system operation; documentation inside an open request belongs to that request.

The reconstruction gate reviews business rules, interfaces, expected results, dependencies, acceptance/tests and recovery prerequisites. Passing this gate means **specified but not demonstrated**. Only an independent explicitly authorized reconstruction exercise can add separate evidence; ordinary product tests do not establish rebuilt equivalence. That exercise is not silently required for initial completion. Production data recovery and bit-for-bit reproduction are not claimed from prose.

<a id="tests"></a>
## Tests, failures and unrelated defects

Each required suite has an environment/effects/authorization contract: suite ID, environment and runtime/prerequisites, root-qualified working/source/output/cache/temp locations, workspace revision, read/write needs, isolation/cleanup, timeout and any independently authorized external-service effects. Registering a suite does not execute it. A runner that cannot enforce all effects is blocked; missing infrastructure/authentication is an unexecuted required check, never a pass. Executable tests live in normal product source paths, including maintained applicable regressions from previous requests.

Implementation runs relevant task checks and the complete required suite against final relevant source, instructions and workspace configuration. Repairs rerun the full suite. Never remove/weaken/reclassify tests solely for passing. Test changes trace to approved behavior. Logs retain full available sanitized evidence plus compact result references. A process returning zero is distinct from a semantic task/acceptance outcome.

Default repair budget is three unsuccessful cycles per stable unresolved failure. Each cycle records diagnosis, authorized repair and rerun evidence. No-progress, elapsed-time or measured-token limits can stop earlier. Restarts/new segments do not reset counts. Explicit Extend repair budget records additional scope/reason and preserves prior history; it never waives required tests. Unknown token usage does not fabricate a zero measurement.

When unrelated defects are found, select include, defer or investigate. Include amends interpretation, plan, tests and documentation with applicable approval. Direct implementation still requires this selection. Deferred defects remain in current known-defects documentation. If one fails a required test, successful completion stays blocked; authorize repair or close cancelled/rejected. Acknowledging the defect is not a completion exception.

<a id="questions"></a>
## Independent product questions

Questions are read-only product investigations with their own output/evidence records. They do not open a request or change implementation, requirements, instructions, durable documentation or known-defect catalogs. They can disclose uncertainty/current-state notices and suggest a separately authorized action. They share the one global action slot and are available while blocked change work is safely stopped. Historical questions load relevant history on demand; ordinary runs do not reread all archived requests.

<a id="profiles"></a>
## Profiles, authentication and manual handoff

A profile selects a trusted installed adapter/executable, optional model/settings, timeout, permissions, credential environment references and compatible runtime location. Store references to credentials, never their values. Explicit per-action selection overrides capability assignment, which overrides default profile. Effective settings, CLI version, root registry and selected skills are recorded per segment. Settings changes are idle-only and apply to the next explicit segment, never a live process.

The portal header's **Next action profile** selector applies only to the next explicitly invoked semantic action, Resume or handoff. Leaving it empty preserves capability/default precedence. It is disabled while busy and does not save or change profile defaults.

Codex uses documented non-interactive execution/event interfaces and a non-Git mode. Diagnostics check executable/version/flags, authentication presence/status and actual host confinement; they do not install/update a CLI or prove service access. A real execution result is separate evidence. Native resume is not assumed: a new session reconstructed from durable harness records is labeled accurately. Agent output is typed proposal data validated by the engine, and no recursive owner launch is permitted.

If profile/authentication/permissions are unavailable, preserve setup/request evidence and fix the named prerequisite, then explicitly Resume. No silent agent fallback occurs. Privileged executable settings require human local administration; request text, source comments and imported forms cannot change them. Other agent identities can be represented by profiles/manual integration without pretending an uninstalled adapter is available.

Preparing a manual handoff persists a reservation before exposing the instructions. It binds action, scope, submission, plan/authority, profile, root modes/revision and handoff identity. Prepared does not mean started, and external execution may be unobservable. Stop/release requires confirmation that the process stopped or never started, returned evidence where needed, and actual file reconciliation. A closed browser, stale heartbeat or returned output is insufficient. Until termination is confirmed, retain the reservation and accept no competing operation or workspace edit. General evidence import cannot bypass this flow.

Return semantic proposals through Stop's `evidence` as `{"results":{"capability-or-task-ID":{"typed":"result"}}}`, with `confirm_external_stopped: true` after independently confirming termination. Match the capability or sequential task identity from the handoff; [the semantic-results contract](conventions/semantic-results.md) documents every result shape. Then explicitly Resume the original operation ID. The harness validates returned proposals against the captured scope and current evidence, runs authorized deterministic effects/tests itself, and records their actual results. Returning data or releasing a reservation never establishes execution, verification or successful closure by itself.

<a id="skills"></a>
## Skills, helper use and human instructions

The [generated skill catalog](skills/README.md) documents the eight complete packages: clarify-requirements, analyze-and-plan, implement-plan, test-and-verify, reverse-engineer-product, maintain-documentation, answer-product-questions and optional git-workflow. Seven core packages default enabled; Git is installed but disabled. Installed, enabled, available and authorized are separate. A required unavailable/disabled capability blocks with guidance; enabling it does not approve work.

Discovery reads compact metadata and integrity manifests without instruction bodies or executing package code. New validated metadata appears without editing run.md. Malformed/duplicate/incompatible/stale packages produce diagnostics, with integrity conflicts blocking execution. Catalog/resource regeneration is explicit core maintenance only, requiring no open request and no execution owner. Ordinary portal/CLI listing and enablement never change core catalogs.

Copy a package directory for standalone use. Its references, versioned schemas/helpers and example contract are already bundled; no exporter, installed AIH engine, portal, database or fixed `.aih_product/` path is needed. Supply explicit named roots/access, root-qualified inputs/outputs, initiating instruction, permitted scope/effects, host constraints and applicable authority. Implementation additionally binds exact approved plan/fingerprint or direct authority with internal persisted planning. Record effective contract and result/evidence references; do not claim independent identity verification. Run bundled helpers with `python -B`. Portable package/helper tests do not by themselves prove agent behavioral compliance. The implementation package has typed `apply-edits` and `reconcile` helpers using the same canonical product journals, explicit output-bound logs, exact plan/task effects and current root permissions; its `run-test` helper executes authorized verification without another installed package. See its standalone reference for inputs and sequential evidence requirements.

Deterministic helpers own inventory, extraction, parsing, screening, schema checks, snapshots, revision checks, edits, state/ownership, tests/results, catalogs and archival. Agents interpret evidence and propose semantic content/patches. Missing helpers are framework gaps, never permission to write ad hoc state or edit the core during product work.

Only humans edit product custom instructions. Initialization creates the directory and guidance without inventing preferences. Portal Save instructions records deliberate human edits with revision checks. Agents may suggest text in outputs. Host restrictions govern all work; product instructions supplement behavior and explicit overrides are identified, but fixed schemas/interfaces cannot be overridden. History, logs, source and attachments are context, not automatic active instructions.

<a id="activity"></a>
## Logs, history, Stop and recovery

Each implementation attempt, including direct, resumed, failed and cancelled segments, creates `implementation_log.jsonl` and `implementation_summary.md` before product changes. Records distinguish planned/attempted/applied/verified work, task sequence, file effects, required suite results, documentation status, repairs, blockers and safe next action. View complete sanitized evidence by reference. Bootstrap documentation and product verification are separate statuses.

Stop is idempotent. Managed process identity and children must be reconciled before releasing ownership; deleting a lock or observing a dead leader is not sufficient proof. Stop may interrupt an incomplete task and retains partial evidence without claiming completion. New submissions remain rejected until the owner is safely released; there is no queued successor. On Resume, compare actual source, human instructions, registry/access, plan/approval, process status and evidence before continuing.

Revision conflicts protect newer human changes. Refresh and reconcile; do not retry a stale overwrite blindly. Transaction recovery uses durable journals and idempotent effect checks, not private chat memory. Filesystem writes revalidate current scope/access. A relocated/revoked path can block recovery even when old history referenced it. Cross-root journals record partial outcomes without a fictional atomic cross-filesystem rollback.

Inspect interrupted information transactions or archival with `recover --wait`. After reviewing the result, explicitly apply permitted reconciliation with `recover --payload '{"apply":true}' --wait`. This can finish partial initialization without resetting existing content. If an interrupted successful archive no longer meets current completion gates, `recover --payload '{"apply":true,"restore_active":true}' --wait` explicitly restores its active blocked slot for reconciliation. Product-task continuation uses `resume --payload '{"operation_id":"OP-ID"}' --wait`; it observes retained proposals and effects and refuses conflicting human edits. These commands use the common `python -B .aih/engine/cli.py` prefix. Never remove lock files to force recovery.

Closed request catalogs preserve summaries/status/dates/stable links. History browsing does not reopen work. Successful closure first promotes durable knowledge to current docs. Cancelled/rejected closure records retained changes, affected canonical topics, unresolved defects, uncertainty and archived evidence in a current-state notice readable without reopening history. The next authorized work reconciles affected knowledge; Q&A can report it but cannot rewrite it.

<a id="security"></a>
## Sensitive input, retained evidence and local access

Input, answers, amendments, attachments and agent outputs are screened before normal persistence. Detected secrets are rejected with safe reason metadata; the original is not silently redacted and accepted. Correct the source and resubmit. Do not include credentials in product files, logs or reusable summaries. Execution evidence is sanitized. A detector is not a guarantee that every possible secret format is recognized, so review what you submit.

Historical sensitive removal is an explicit human-authorized redaction action on identified AIH-owned copies, preserving non-sensitive audit evidence and repairing fingerprints/references. Ordinary accepted source/history remains immutable except this exception. Retention settings must preserve required evidence, unresolved obligations, current knowledge and active/uncertain operation data. Automatic pruning is disabled by default; cleanup targets owned inert temporary material after reconciliation.

The local portal is a local administration interface; do not expose it publicly. Host permissions remain authoritative. Checksums detect changes; they do not prevent an external actor with equivalent filesystem access from rewriting files. Browser profiles/caches launched by framework tooling must be confined; ordinary user browser behavior is outside the framework's control.

<a id="maintenance"></a>
## Installation, upgrades and optional Git

Install a pinned local core without a published URL or Git:

```sh
python -B /path/to/source/.aih/engine/cli.py install --source /path/to/source/.aih --destination /path/to/product
```

The source is explicitly read-only intake; neighboring source files are not permission grants. The destination becomes the fixed home. Installation preserves product content and refuses unsafe aliases or an incompatible existing installation. State templates become product-owned after initialization. Do not overwrite `.aih/` manually during ordinary runs.

Upgrade with `upgrade --source /path/to/reviewed/.aih` only while no request is open and every managed/external owner is confirmed stopped. Blocked, paused and Ready-to-close requests still count as open. A broken helper does not create an exception; explicitly cancel/reject the request first if necessary, preserving its notice/evidence. Validate incoming version/integrity and schema compatibility, retain recoverable replacement records, and preserve product content/root identities/history. Unimplemented incompatible migrations are rejected rather than silently merging schemas. Executable staging lives in an authorized ordinary writable root, never `.aih_product/`.

Git is optional per root. Enabling git-workflow never authorizes commit, push, PR creation, integration, deployment or destructive actions. The bundled standalone helper supports typed status/diff/log/branch/commit and explicit HTTPS push. Mutations require exact declared Git effects and scoped repository metadata writes; push requires network/publication authorization and a matching reviewed remote URL. Credentials stay in named environment references or explicitly readable TLS files. Local validation exercises branch/commit and preservation of unrelated staged work; no remote push is performed. PR creation and SSH/custom transport remain independently operated, explicitly authorized tool boundaries. Git worktrees/gitdirs, hooks/filters, signing, configuration and credential/SSH helpers must honor current root/access/scope rules. A remote-service permission is not permission to write outside the workspace. Preserve unrelated changes and review exact intended effects. If tracking files, exclude runtime caches, inert temporary data, credentials and local session material according to your retention needs; do not automatically discard durable request/evidence history.

<a id="commands"></a>
## Command reference

`python -B .aih/engine/cli.py --help` lists the installed parser. `operations` returns IDs, inputs, effects, required permissions and result contracts; `help [query]` reads/searches this guide without initialization/authentication. The shared menu uses these same implementations.

| Command | Purpose |
|---|---|
| `init` | Idempotent product initialization; does not claim baseline completion |
| `serve --port 8765 --no-browser` | Local portal; reuse/reconcile existing launch ownership |
| `menu` | Shared interactive menu |
| `status` | Passive state, owner, blockers and next-action information |
| `operations` | Installed typed operation catalog |
| `skills` | Metadata-only discovered skills and diagnostics |
| `help [query]` | Local guide/help search |
| `install --source CORE --destination HOME` | Pinned local installation |
| `upgrade --source CORE` | Gated local core upgrade |
| `test` | Run framework validation suite |
| `demo` | Run labeled synthetic demonstrations |
| `run OPERATION` | Invoke a typed operational action |

Operational commands are also direct aliases. They accept `--payload JSON` or `--payload-file PATH`, `--expected-revision N`, `--idempotency-key KEY`, and `--wait` where appropriate. Reuse an idempotency key only for the identical action and payload: a retry returns the acknowledged receipt without launching another action, even while the existing worker saves a checkpoint. Obtain current revision from status, and reread after every accepted action. For multiline or quoted material prefer a UTF-8 JSON payload file. Filesystem permission and operation authority remain enforced. Example:

```sh
python -B .aih/engine/cli.py save-draft --payload '{"lane":"change","text":"Add a customer-visible status label."}' --expected-revision 1
python -B .aih/engine/cli.py clarify --expected-revision 2 --wait
python -B .aih/engine/cli.py status
```

The shown revisions are illustrative, not fixed: use the actual returned state. On Windows, use a payload file to avoid shell-specific JSON quoting.

| Operation | Required payload / boundary |
|---|---|
| `save-draft` | `lane`, `text`; saves only |
| `clarify`, `analyze` | Explicit submission; repeatable, phase-separated |
| `approve` | `plan_revision`; human approval only |
| `implement`, `implement-directly`, `resume` | Current scoped authority and prerequisite gates |
| `stop` | Idempotent Stop; external confirmation/evidence belongs to its release flow |
| `close` | `outcome`: `completed`, `cancelled`, or `rejected` |
| `reverse-engineer` | Initial/incremental documentation; `within_request:true` for open-request reconciliation |
| `ask` | Submit the saved independent question |
| `workspace-save`, `workspace-validate` | `roots` entries; human idle administration |
| `profile-save` | `profile_id`, `profile`; trusted supported settings |
| `settings-save` | Supported appearance/skills/repair configuration |
| `instructions-save` | `text`; deliberate human content only |
| `save-questionnaire` | `text`; authoritative Markdown drafts |
| `export-questions` | Generate/reuse explained outstanding Requestor forms |
| `receive-answers` | `text`; staged accepted original only |
| `review-answers`, `import-and-clarify` | `receipt_id`, `decisions`, `review_revision`; draft versus explicit Clarify submission |
| `save-amendment` | `text`; include stable amendment identity when revising |
| `defect-disposition` | `id`, `disposition`, `reason` |
| `extend-repair-budget` | `failure_id`, `additional`, `reason` |
| `register-test` | `contract`; registration is not execution |
| `verify` | Run complete maintained required suites |
| `handoff` | `action`, `instruction`; acquires external reservation |
| `doctor`, `validate` | Operational diagnostics; idle required |
| `recover`, `cleanup` | Current-permission recovery / owned inert temporary cleanup |
| `redact` | `value`, `reason`, `paths`; explicit human historical exception |
| `inventory` | Deterministic source facts, no inspected code execution |

The live operation catalog and command `--help` list operation IDs, required payload fields and common invocation flags. Semantic actions accept an optional `profile` ID for the next segment. Resume accepts the selected `operation_id`; recovery's `apply` and `restore_active` options are described above. Adapter-specific settings and manual evidence follow the profile and semantic-result contracts. Errors return structured reasons/conflict details and preserve accepted evidence; a refused busy command does not queue work.

Framework `test` and `demo` are synchronous maintenance commands. They require globally idle execution and no open request, including blocked or Ready-to-close requests, before creating isolated fixtures. They leave an uninitialized main product uninitialized and refuse competing initialization/actions. Run `test` through the selected home's installed CLI so its generated fixtures stay inside that home. Tests need local loopback sockets for HTTP checks; unsupported confinement or host permissions are reported as failed/blocked prerequisites, never replaced with fabricated passes.

<a id="limitations"></a>
## Validation evidence and current limitations

Consult the delivered `logs/` action and validation records for this build's actual commands, outcomes, platform, browser walkthrough, synthetic fixtures and real-agent smoke result. Unit/helper tests, fixture adapter scenarios, rendered browser inspection and live Codex execution are different evidence classes. Authentication discovery alone does not count as live execution. A synthetic model fixture does not establish semantic agent compliance. Standalone copies are package/helper portability evidence unless independently exercised by a real agent.

The current enforceable managed subprocess backend is Linux x86_64/aarch64 with Landlock ABI 3+ and libseccomp. POSIX descriptor operations guard helper mutations; native Windows mutation/confinement is unavailable and fails closed. Windows users can operate within a compatible WSL2 distribution, but untested Windows launchers/native behavior must not be inferred from Linux tests. Local filesystem assumptions are advisory file locking, same-directory rename and fsync. Shared, synchronized and network storage are unverified; no stronger durability guarantee is claimed.

Not every source format has a semantic extractor; unsupported/binary/large content retains fingerprints and explicit limitations for investigation. Sensitive detection is heuristic. Agent-authored interpretations, explanations, plans and patches need substantive evidence review in addition to structural validation. Reconstruction remains specified but not demonstrated until a separate exercise. Any unavailable required capability or test environment blocks its action/completion rather than silently reducing coverage.

Historical sensitive-data correction includes encoded interrupted recovery copies. Corrected product-edit proposals require fresh explicit authorization before replay. Keep audit reasons non-sensitive.
