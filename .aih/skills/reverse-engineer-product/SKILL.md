---
{
  "name": "reverse-engineer-product",
  "description": "Build or refresh evidence-backed understanding from registered product roots without changing implementation.",
  "metadata": {
    "aih": "{\"id\":\"reverse-engineer-product\",\"display_name\":\"Reverse engineer a product\",\"version\":\"1.0.0\",\"purpose\":\"Build or refresh evidence-backed understanding from registered product roots without changing implementation.\",\"capabilities\":[\"reverse-engineer\",\"baseline\",\"incremental-extraction\"],\"excludes\":[\"Repairing implementation\",\"Claiming static extraction demonstrates runtime behavior\"],\"input_contract\":\"references/standalone.md\",\"output_contract\":\"references/standalone.md#outputs\",\"standalone_parameters\":[\"contract\",\"data\",\"artifact\"],\"effects\":[\"scoped-output-records\"],\"write_scope\":\"Only explicit root-qualified invocation scope; no writes to read-only roots, human instructions, immutable core or outside folders.\",\"prerequisites\":[\"Explicit initiating instruction and applicable authority\",\"Validated root-qualified inputs/outputs and current workspace revision\"],\"authorization\":[\"setup\"],\"dependencies\":[\"python>=3.11\"],\"compatibility\":\"AIH contract 1.0; Python 3.11+ standard library; secure POSIX writes. Other hosts require a compatible confinement backend.\",\"bundle_version\":\"1.0.0\",\"default_enabled\":true,\"output_summary\":\"Source fingerprints, observed facts, inferred knowledge, unknowns and baseline coverage evidence.\"}"
  }
}
---

# Reverse engineer a product

Use deterministic helpers for inventory, parsing, validation, writes and evidence. Agent judgment supplies semantic interpretation and scoped patches; helper failure is an explicit capability gap, never permission to bypass validation. Read metadata first and only the relevant references; do not preload every package. Runtime execution must not modify this package or another immutable core. Disable Python bytecode. Human-owned instructions and workspace membership are read-only to the agent.

For installed AIH, the engine owns submission snapshots, global action reservation, current revisions, profile choice, state transitions and archival. Use its typed operation catalog and [semantic result shapes](references/semantic-results.md). For standalone use read [the compact contract](references/standalone.md), validate the explicit contract, and persist effective authority plus result references with the output. Do not recreate the AIH lifecycle. Declared effects are not permission grants.

Resolve the explicit workspace contract first. Inventory every selected registered product root using helpers without following aliases, importing source, executing hooks, or exposing credentials. Include authorized configurations, interfaces, source/tests/build/deployment definitions and existing docs; record omissions/unavailable roots. Preserve source/test/instruction fingerprints. Static extraction is evidence collection, not verified runtime behavior.

Synthesize purpose, business behavior, architecture, components/dependencies, domain/data, interfaces/flows and operations only from cited evidence. Distinguish observed facts, inferred requirements, contradictions, unsupported claims, unknown external facts and unverified behavior. Preserve human-authored documentation and instructions. No implementation/config/test repairs belong to this action.

Initial mode covers all 18 applicability categories and every registered root, producing substantive relevant local documentation and a reconstruction completeness/traceability review. Missing local coverage blocks readiness; explicit unknown external facts need not. The review remains specified but not demonstrated until a separately authorized independent rebuild supplies evidence. Inventory alone never completes the baseline or means product tests passed.

Incremental mode compares source/instruction/extractor/schema/core/workspace fingerprints and dependencies, reuses valid extraction, selects changed topics and preserves unaffected content. Apply current knowledge through included documentation conventions, not a competing baseline. Validate tree/links/coverage. Record provenance, limitations and checkpoints before interruption. With no open request use the setup/documentation operation identity; inside a request use its authorized documentation increment. Saving a newly added root is not automatic authority to run this skill. Profile/permission blockers retain partial useful evidence with actionable guidance.

Read [workspace boundaries](references/workspace.md) for path/access changes, [record ownership](references/records.md) for revisions, and the relevant [execution](references/execution.md), [questionnaire](references/questionnaires.md) or [documentation](references/documentation.md) contract when performing that work.
