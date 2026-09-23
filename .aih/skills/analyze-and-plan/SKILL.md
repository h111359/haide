---
{
  "name": "analyze-and-plan",
  "description": "Evaluate implementation choices and generate or revise the sequential plan from current submitted requirements.",
  "metadata": {
    "aih": "{\"id\":\"analyze-and-plan\",\"display_name\":\"Analyze and plan\",\"version\":\"1.0.0\",\"purpose\":\"Evaluate implementation choices and generate or revise the sequential plan from current submitted requirements.\",\"capabilities\":[\"analyze\",\"planning\",\"direct-planning\"],\"excludes\":[\"Product changes during Analysis\",\"Inventing user approval\"],\"input_contract\":\"references/standalone.md\",\"output_contract\":\"references/standalone.md#outputs\",\"standalone_parameters\":[\"contract\",\"data\",\"artifact\"],\"effects\":[\"scoped-output-records\"],\"write_scope\":\"Only explicit root-qualified invocation scope; no writes to read-only roots, human instructions, immutable core or outside folders.\",\"prerequisites\":[\"Explicit initiating instruction and applicable authority\",\"Validated root-qualified inputs/outputs and current workspace revision\"],\"authorization\":[\"analysis\"],\"dependencies\":[\"python>=3.11\"],\"compatibility\":\"AIH contract 1.0; Python 3.11+ standard library; secure POSIX writes. Other hosts require a compatible confinement backend.\",\"bundle_version\":\"1.0.0\",\"default_enabled\":true,\"output_summary\":\"Separate assessment/questions/issues records, scoped sequential plan and documentation increment.\"}"
  }
}
---

# Analyze and plan

Use deterministic helpers for inventory, parsing, validation, writes and evidence. Agent judgment supplies semantic interpretation and scoped patches; helper failure is an explicit capability gap, never permission to bypass validation. Read metadata first and only the relevant references; do not preload every package. Runtime execution must not modify this package or another immutable core. Disable Python bytecode. Human-owned instructions and workspace membership are read-only to the agent.

For installed AIH, the engine owns submission snapshots, global action reservation, current revisions, profile choice, state transitions and archival. Use its typed operation catalog and [semantic result shapes](references/semantic-results.md). For standalone use read [the compact contract](references/standalone.md), validate the explicit contract, and persist effective authority plus result references with the output. Do not recreate the AIH lifecycle. Declared effects are not permission grants.

Start from the one current submitted interpretation and current documentation. Apply submitted decisions/amendments while preserving their provenance; missing business requirements return to Clarify. Inspect only relevant source branches and metadata before full leaves. Distinguish evidence, assumptions and alternatives, covering feasibility, architecture, interfaces, data integrity, security, compatibility, deployment/migration/recovery, operations and consequential tradeoffs.

Keep interpretation, questions, solution assessment and unrelated issues separate. Record a concise evidence-scoped no-questions/no-unrelated-issues finding when applicable. Ask design choices as design choices; suggested solutions are not new approved requirements. An unresolved consequential choice pauses Analysis. Repeat Analyze after explicit answers; do not require a separate Plan command.

Once consequential questions are resolved, generate the sequential implementation plan automatically. Each task names stable identity/order, intended outcome, requirements/decisions, dependencies, exact existing/new root-qualified paths and create/modify/move/delete/inspect actions, completion criteria and evidence. Include bounded investigation if a future path is unknown; revise before dependent writes. Include changed-behavior tests, full regression suite, authorized repairs and reruns, documentation increment/application/verification and results tasks. Map every accepted criterion to tasks/checks.

Bind plan to interpretation/workspace/content/instruction revisions. Plan documentation by canonical topic and reason; a no-impact determination requires evidence. Record unrelated defects for include/defer/investigate selection without silently expanding scope. End at generated-plan awaiting explicit approval, or direct-mode internal plan persisted under existing direct authorization. Never self-issue human approval or start ordinary implementation.

Read [workspace boundaries](references/workspace.md) for path/access changes, [record ownership](references/records.md) for revisions, and the relevant [execution](references/execution.md), [questionnaire](references/questionnaires.md) or [documentation](references/documentation.md) contract when performing that work.
