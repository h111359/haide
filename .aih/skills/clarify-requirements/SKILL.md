---
{
  "name": "clarify-requirements",
  "description": "Establish what must change and why; apply reviewed submitted answers and amendments in iterative clarification.",
  "metadata": {
    "aih": "{\"id\":\"clarify-requirements\",\"display_name\":\"Clarify requirements\",\"version\":\"1.0.0\",\"purpose\":\"Establish what must change and why; apply reviewed submitted answers and amendments in iterative clarification.\",\"capabilities\":[\"clarify\",\"requirements\",\"requestor-exchange\"],\"excludes\":[\"Choosing implementation approaches\",\"Product implementation\"],\"input_contract\":\"references/standalone.md\",\"output_contract\":\"references/standalone.md#outputs\",\"standalone_parameters\":[\"contract\",\"data\",\"artifact\"],\"effects\":[\"scoped-output-records\"],\"write_scope\":\"Only explicit root-qualified invocation scope; no writes to read-only roots, human instructions, immutable core or outside folders.\",\"prerequisites\":[\"Explicit initiating instruction and applicable authority\",\"Validated root-qualified inputs/outputs and current workspace revision\"],\"authorization\":[\"requirements\"],\"dependencies\":[\"python>=3.11\"],\"compatibility\":\"AIH contract 1.0; Python 3.11+ standard library; secure POSIX writes. Other hosts require a compatible confinement backend.\",\"bundle_version\":\"1.0.0\",\"default_enabled\":true,\"output_summary\":\"Versioned interpretation, explained questions, exchange reviews, amendment dispositions and round results.\"}"
  }
}
---

# Clarify requirements

Use deterministic helpers for inventory, parsing, validation, writes and evidence. Agent judgment supplies semantic interpretation and scoped patches; helper failure is an explicit capability gap, never permission to bypass validation. Read metadata first and only the relevant references; do not preload every package. Runtime execution must not modify this package or another immutable core. Disable Python bytecode. Human-owned instructions and workspace membership are read-only to the agent.

For installed AIH, the engine owns submission snapshots, global action reservation, current revisions, profile choice, state transitions and archival. Use its typed operation catalog and [semantic result shapes](references/semantic-results.md). For standalone use read [the compact contract](references/standalone.md), validate the explicit contract, and persist effective authority plus result references with the output. Do not recreate the AIH lifecycle. Declared effects are not permission grants.

Read the current canonical interpretation, relevant documentation branches and submitted source revisions. Apply only submitted framework-user/requestor answers and amendments; a staged receipt, saved draft, unchecked recommendation or historical direction is not an accepted requirement. Preserve original wording and source links. Investigate available evidence before batching consequential questions.

Separate current behavior, intended outcomes, users, constraints, scope, acceptance criteria and proposed inferences. Resolve contradictions explicitly; never choose architecture to fill a missing requirement. Keep one interpretation and revision it, preserving previous rounds. An unchanged invocation should reuse valid interpretation/evidence and explain remaining blockers, not invent questions or rerun downstream phases.

For each question provide situation/terms, why the answer changes behavior/scope/acceptance, answer instructions, a neutral illustration when useful, respondent and required/optional distinction. Recommendations start unchecked. Use the bundled exchange helpers for Markdown parsing, export, intake/review and version checks. At a waiting round export outstanding marked Requestor questions automatically; retain earlier exports and avoid empty ones. A returned form is staged until reviewed. Respect partial, unknown, stale, altered, withdrawn, duplicate and wrong-request answers. Treat comments that change wishes as explicitly linked amendments instead of duplicating meaning. Save reviewed drafts and submit/clarify are distinct actions.

Use immutable amendment revisions for every observed framework Save/submission, corrections and withdrawals. Reassess stale answers and affected plan/test/doc evidence. Clarify permits read-only investigation plus evidence-backed known-defect/staleness bookkeeping only. Finish with ready-for-Analysis or explicit questions; do not call Analyze or implement automatically.

Read [workspace boundaries](references/workspace.md) for path/access changes, [record ownership](references/records.md) for revisions, and the relevant [execution](references/execution.md), [questionnaire](references/questionnaires.md) or [documentation](references/documentation.md) contract when performing that work.
