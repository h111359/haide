---
{
  "name": "answer-product-questions",
  "description": "Answer an independent read-only question from current or explicitly requested historical product evidence.",
  "metadata": {
    "aih": "{\"id\":\"answer-product-questions\",\"display_name\":\"Answer product questions\",\"version\":\"1.0.0\",\"purpose\":\"Answer an independent read-only question from current or explicitly requested historical product evidence.\",\"capabilities\":[\"ask\",\"read-only-question\"],\"excludes\":[\"Changing request scope or implementation\",\"Writing durable product documentation\"],\"input_contract\":\"references/standalone.md\",\"output_contract\":\"references/standalone.md#outputs\",\"standalone_parameters\":[\"contract\",\"data\",\"artifact\"],\"effects\":[\"scoped-output-records\"],\"write_scope\":\"Only explicit root-qualified invocation scope; no writes to read-only roots, human instructions, immutable core or outside folders.\",\"prerequisites\":[\"Explicit initiating instruction and applicable authority\",\"Validated root-qualified inputs/outputs and current workspace revision\"],\"authorization\":[\"read-only\"],\"dependencies\":[\"python>=3.11\"],\"compatibility\":\"AIH contract 1.0; Python 3.11+ standard library; secure POSIX writes. Other hosts require a compatible confinement backend.\",\"bundle_version\":\"1.0.0\",\"default_enabled\":true,\"output_summary\":\"Question-owned answer, evidence links and explicit uncertainty/freshness limitations.\"}"
  }
}
---

# Answer product questions

Use deterministic helpers for inventory, parsing, validation, writes and evidence. Agent judgment supplies semantic interpretation and scoped patches; helper failure is an explicit capability gap, never permission to bypass validation. Read metadata first and only the relevant references; do not preload every package. Runtime execution must not modify this package or another immutable core. Disable Python bytecode. Human-owned instructions and workspace membership are read-only to the agent.

For installed AIH, the engine owns submission snapshots, global action reservation, current revisions, profile choice, state transitions and archival. Use its typed operation catalog and [semantic result shapes](references/semantic-results.md). For standalone use read [the compact contract](references/standalone.md), validate the explicit contract, and persist effective authority plus result references with the output. Do not recreate the AIH lifecycle. Declared effects are not permission grants.

Read the initiating question, current documentation navigation, relevant leaves and current-state notices. Use historical metadata/records only when concretely relevant or explicitly requested. Inspect authorized product content read-only where freshness or missing evidence requires it; cite root-qualified references and observed fingerprints.

Answer the actual question and distinguish established facts, inference, intended behavior, observed implementation, verification and uncertainty. Explain stale/incomplete knowledge and scope limits; do not present bootstrap documentation as tested product behavior. Reuse valid summaries and label any omitted detail while retaining evidence references.

Write only question-owned answer/evidence output within the invocation's declared scope. Do not modify implementation, request requirements/status, instructions, known-defect catalogs or durable product documentation. You may report a discovered issue in the answer and describe the separately authorized action needed to maintain product knowledge. A request blocked with its owner stopped permits Q&A, but starting/running/stopping/uncertain/external-reserved ownership blocks a competing question action. Never queue work or resume implementation after answering.

Read [workspace boundaries](references/workspace.md) for path/access changes, [record ownership](references/records.md) for revisions, and the relevant [execution](references/execution.md), [questionnaire](references/questionnaires.md) or [documentation](references/documentation.md) contract when performing that work.
