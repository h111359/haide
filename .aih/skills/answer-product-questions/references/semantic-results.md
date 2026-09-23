# Typed semantic results

Version 1.0. Agents supply semantic content and proposed effects. Python owns state, revisions, authorization, file mutation, actual test execution, catalogs and archival. A zero process exit or an agent's assertion is never sufficient completion evidence.

Each automated segment receives its exact result contract and current scoped context. Return a UTF-8 JSON object, without executable code wrappers. Preserve source attribution, unknowns and observed content hashes. For a manual handoff return `{"results": {"capability-or-task-ID": {"typed": "result"}}}` through Stop's `evidence`, explicitly confirm external termination, then invoke `resume` with the original operation ID. This is a data proposal, not permission to exceed the captured scope. The engine rejects stale handoffs and validates the same gates as automated execution.

## Clarification (`clarify-requirements`)

Required fields: `interpretation` (canonical Markdown), `questions` (array in the questionnaire contract), `ready` (boolean), `acceptance_criteria` (complete stable `{id,description,source}` inventory when ready), `blockers` (strings), `amendment_effects` (one `{id,effect,explanation}` per submitted amendment, with effect applied/superseded/withdrawn/needs-clarification). Optional `workspace_scope_reconciled` is true only when actual scope/dependency impact has been assessed; it cannot bypass missing documentation coverage. `defects` must carry evidence and remain unconfirmed when uncertain; `stale_topics` may mark factual drift. Clarify never supplies implementation edits or design decisions.

The interpretation covers problem and rationale, users, current/required behavior, desired outcomes, in/out-of-scope work, functional/nonfunctional requirements, explicit constraints, observable acceptance criteria, assumptions, open questions and source revisions. Technical constraints explicitly supplied by the requestor remain attributed requirements.

Question shape:

```json
{"id":"Q-AUDIENCE","revision":1,"question":"Who receives the greeting?","explanation":"We need to know which people use the greeting.","why":"This determines whose names the product must support.","instructions":"Describe the intended users in your own words.","example":"For example, new members of a club (illustration only).","respondent":"Requestor","kind":"text","blocker":true,"category":"requirement","options":[],"answer":"","comments":""}
```

## Analysis (`analyze-and-plan`)

Uses the clarification fields and supplies separate `solution_assessment` and `unrelated_issues` Markdown, `plan: {tasks:[...]}`, and `documentation_increment: {topics,proposed_changes,reason}`. Requirements gaps return to Clarify; design questions stay in Analysis. If ready, the engine generates the identified versioned plan and stops before implementation. When blocked, the draft plan and questions are retained.

Tasks have unique stable `id`, contiguous `sequence`, `kind` (investigate/implement/tests/verify/documentation/evidence), `outcome`, nonempty `requirements`, `changes`, prior-task `dependencies`, and nonempty `completion_criteria`. Every plan includes explicit tests, verification/repair, documentation and evidence tasks. A change is `{path:"backend:src/api.py",action:"modify"}`; move additionally names `destination`. All mutation locations must be writable and within approved scope. A plan is bound to submitted requirements, instructions, source content, documentation and workspace revision, and its full content hash is bound to authorization.

## Implementation and test creation (`T1`, `T2`, …)

Return `summary`, `edits`, `requirements_trace`, optional `test_contracts`, `observations`, `blockers` and `defects`. Each edit includes exact root-qualified `path`, `action`, `expected_hash` (null only for create), and UTF-8 `content` for create/modify. Move also names the approved destination. The engine checks each action against the current sequential task, journals effects separately across roots, and never assumes an atomic cross-filesystem product commit. An investigation task returns observations with no implementation edits.

Registered tests use the test-run contract in the runtime schema. Python orchestration can run a registered `python-unittest` suite or a reviewed normal-workspace `python-script` driver. A Python driver may invoke the product's installed toolchain under the same inherited confinement; declared prerequisites and filesystem effects still apply. No generic command template is accepted. Tests never run from `.aih_product/`.

```json
{"id":"unit","workspace_revision":1,"runner":"python-unittest","environment":"python3","working_directory":"home:","source_paths":["home:tests"],"start_directory":"home:tests","write_paths":[],"prerequisites":[],"isolation":"landlock","cleanup":"operation-runtime","authorization":"request-implementation","required":true}
```

## Repair (`repair-1`, `repair-2`, …)

Return `scope` (in-scope/unrelated/infrastructure), `diagnosis`, approved-path `edits`, and `requirements_trace`. Unrelated failures additionally provide a defect with stable ID, symptoms, evidence, disposition and confirmation status; the user selects its scope. The engine retains stable failure identities and every attempt, enforces budgets and no-progress blocking, and reruns the full suite. No result may disable or weaken tests merely to obtain a pass.

## Documentation (`reverse-engineer-product` or documentation task ID)

Return `topics`, `coverage`, `source_dispositions` and `reconstruction_review`. Each topic has a stable `id`, `title`, meaningful `summary`, substantive Markdown `content`, `sources` (root-qualified references), and `when_to_read`; an existing changed topic may include `expected_hash`. Preserve human content. Unchanged valid topics may be retained; affected topics cannot be omitted. Every inventory source must occur in a topic or a reasoned source disposition. Every ID in `coverage.json` needs applicable/not-applicable/unknown with rationale; applicable categories reference substantive topic IDs. The reconstruction review covers `business_rules`, `interfaces`, `expected_results`, `dependencies`, `acceptance_tests`, and `recovery`, with traceability and explicit gaps. Its status remains **specified but not demonstrated**.

## Acceptance/evidence task

Return `summary`, `acceptance` and `unmet`. Each acceptance entry has `criterion` (exact canonical criterion ID), nonempty `suite_ids` and an evidence explanation. The engine requires exact complete coverage of canonical criteria and checks actual current passing-suite evidence, content, workspace and authorization bindings; an assertion cannot manufacture a test pass. Unmet outcomes remain blockers.

## Read-only answer (`answer-product-questions`)

Return `answer` Markdown, root-qualified `sources`, and `uncertainty`. Explain that modification requests need an explicit change action. The worker writes only question communication records, validates source stability, and leaves request scope, product documentation, source and configuration unchanged.

## Synthetic examples

`engine/demo_fixtures.py` and `engine/demo.py` contain complete fixture-authored results. They exercise contracts and actual confined test processes; they are clearly labeled test examples and are never selected as a fallback for a missing agent.
