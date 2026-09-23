---
{
  "name": "implement-plan",
  "description": "Execute an authorized current plan sequentially or plan internally for explicitly authorized direct implementation.",
  "metadata": {
    "aih": "{\"id\":\"implement-plan\",\"display_name\":\"Implement a plan\",\"version\":\"1.0.0\",\"purpose\":\"Execute an authorized current plan sequentially or plan internally for explicitly authorized direct implementation.\",\"capabilities\":[\"implement\",\"implement-directly\",\"repair\",\"resume\"],\"excludes\":[\"Unrelated unauthorized repairs\",\"Implicit deployment or publication\"],\"input_contract\":\"references/standalone.md\",\"output_contract\":\"references/standalone.md#outputs\",\"standalone_parameters\":[\"contract\",\"data\",\"artifact\"],\"effects\":[\"scoped-output-records\",\"implementation\",\"test-execution\"],\"write_scope\":\"Only explicit root-qualified invocation scope; no writes to read-only roots, human instructions, immutable core or outside folders.\",\"prerequisites\":[\"Explicit initiating instruction and applicable authority\",\"Validated root-qualified inputs/outputs and current workspace revision\"],\"authorization\":[\"approved-plan\",\"direct-implementation\"],\"dependencies\":[\"python>=3.11\",\"linux-landlock-abi>=3\",\"libseccomp\"],\"compatibility\":\"AIH contract 1.0; Python 3.11+ standard library; secure POSIX writes. Other hosts require a compatible confinement backend.\",\"bundle_version\":\"1.0.0\",\"default_enabled\":true,\"output_summary\":\"Scoped product changes, sequential task outcomes, incremental logs, checkpoints and verified results.\"}"
  }
}
---

# Implement a plan

Use deterministic helpers for inventory, parsing, validation, writes and evidence. Agent judgment supplies semantic interpretation and scoped patches; helper failure is an explicit capability gap, never permission to bypass validation. Read metadata first and only the relevant references; do not preload every package. Runtime execution must not modify this package or another immutable core. Disable Python bytecode. Human-owned instructions and workspace membership are read-only to the agent.

For installed AIH, the engine owns submission snapshots, global action reservation, current revisions, profile choice, state transitions and archival. Use its typed operation catalog and [semantic result shapes](references/semantic-results.md). For standalone use read [the compact contract](references/standalone.md), validate the explicit contract, and persist effective authority plus result references with the output. Do not recreate the AIH lifecycle. Declared effects are not permission grants.

Validate explicit plan approval bound to current revisions, or explicit direct implementation instruction. Before every start/resume reconcile product files, human instructions, requirements, workspace access and documentation freshness. New/relocated areas need explicit baseline reconciliation before reliance. If any consequential prerequisite is stale or authority unclear, stop before changes and report the exact blocker.

For direct implementation read the included [planning guidance](references/planning.md): generate and persist the same scoped sequential plan before first product change. This package includes that capability; no other installed skill is required. Do not create fictitious human approval. Direct mode still requires human selection of unrelated defects.

Create durable implementation log and readable summary before changes. Execute one plan task at a time in order, never concurrent implementation tasks. Use the bundled `apply-edits`/`reconcile` operations for standalone effects, and the bundled `run-test` for configured verification; use validated edits and current permissions; checkpoint per-root progress before safe boundaries and interruption. Record attempted/applied/verified distinctions. A task interrupted partway remains incomplete. Do not claim cross-filesystem atomicity or silently replay duplicate effects during recovery. Revalidate current access; revoked paths block recovery writes.

Author/update tests only for authorized behavior. Run relevant checks then the full maintained suite against final content through configured test contracts. Diagnose and repair authorized in-scope defects; rerun full suite after repairs. Preserve stable failure histories and honor three unsuccessful cycles by default, elapsed/token budgets and no-progress stops. Explicit extension requires a recorded reason; missing token usage stays unavailable. Do not weaken tests or treat a deferred failing defect as waived.

Apply and verify the documentation increment, known defects and results with source/evidence links. A failure or incomplete required check blocks successful completion. Stop at Ready to close once all gates pass; explicit human Close successfully owns archival. Cancellation preserves partial changes and a discoverable current-state notice. No Git publication/deployment follows implicitly.

Read [workspace boundaries](references/workspace.md) for path/access changes, [record ownership](references/records.md) for revisions, and the relevant [execution](references/execution.md), [questionnaire](references/questionnaires.md) or [documentation](references/documentation.md) contract when performing that work.
