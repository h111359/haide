---
{
  "name": "test-and-verify",
  "description": "Design scoped tests, run the maintained required suites in authorized environments, and diagnose actual failures.",
  "metadata": {
    "aih": "{\"id\":\"test-and-verify\",\"display_name\":\"Test and verify\",\"version\":\"1.0.0\",\"purpose\":\"Design scoped tests, run the maintained required suites in authorized environments, and diagnose actual failures.\",\"capabilities\":[\"test\",\"verification\",\"failure-diagnosis\"],\"excludes\":[\"Waiving failed required tests\",\"Unrelated product repairs\"],\"input_contract\":\"references/standalone.md\",\"output_contract\":\"references/standalone.md#outputs\",\"standalone_parameters\":[\"contract\",\"data\",\"artifact\"],\"effects\":[\"scoped-output-records\",\"test-execution\"],\"write_scope\":\"Only explicit root-qualified invocation scope; no writes to read-only roots, human instructions, immutable core or outside folders.\",\"prerequisites\":[\"Explicit initiating instruction and applicable authority\",\"Validated root-qualified inputs/outputs and current workspace revision\"],\"authorization\":[\"approved-plan\"],\"dependencies\":[\"python>=3.11\",\"linux-landlock-abi>=3\",\"libseccomp\"],\"compatibility\":\"AIH contract 1.0; Python 3.11+ standard library; secure POSIX writes. Other hosts require a compatible confinement backend.\",\"bundle_version\":\"1.0.0\",\"default_enabled\":true,\"output_summary\":\"Test inventory and mappings, sanitized run evidence, failures, stale and unexecuted checks.\"}"
  }
}
---

# Test and verify

Use deterministic helpers for inventory, parsing, validation, writes and evidence. Agent judgment supplies semantic interpretation and scoped patches; helper failure is an explicit capability gap, never permission to bypass validation. Read metadata first and only the relevant references; do not preload every package. Runtime execution must not modify this package or another immutable core. Disable Python bytecode. Human-owned instructions and workspace membership are read-only to the agent.

For installed AIH, the engine owns submission snapshots, global action reservation, current revisions, profile choice, state transitions and archival. Use its typed operation catalog and [semantic result shapes](references/semantic-results.md). For standalone use read [the compact contract](references/standalone.md), validate the explicit contract, and persist effective authority plus result references with the output. Do not recreate the AIH lifecycle. Declared effects are not permission grants.

Read accepted criteria, approved tasks, current required suite inventory and final relevant content. During authorized implementation design/update tests that expose actual behavior and regressions; Analysis may propose a strategy without editing executable tests. Preserve maintained relevant regressions across earlier requests and all registered roots.

Require each suite's explicit environment, prerequisites, root-qualified source/working/output/cache/temp effects, workspace revision, access needs, isolation, cleanup and authorization. Validate the runner can enforce these effects, including read-only source folders and external-service effects. Missing credentials/infrastructure/confinement blocks required execution. Do not run in a substitute environment or claim that setting a working directory confines a process. Use the configured tested runner; the portable helper intentionally does not launch an unconfined arbitrary command.

Run the complete required suite and preserve sanitized full evidence, process exit, check outcomes, actual content/instruction/workspace fingerprints and measured usage availability. Clearly distinguish static inspection, process success and acceptance evidence. Investigate stable failure identity, reproduction and scope relationship. In-scope repair belongs to authorized implementation; unrelated diagnosis does not authorize repair. Record include/defer/investigate disposition and known defects. A deferred failing required test continues blocking.

After a repair rerun the full suite. Preserve attempts across restarts, stop at budget/no-progress boundaries, and require explicit scoped extension. Never erase failed/skipped/stale/unexecuted checks or weaken tests solely to pass. Summarize every required suite with evidence and unresolved limitations.

Read [workspace boundaries](references/workspace.md) for path/access changes, [record ownership](references/records.md) for revisions, and the relevant [execution](references/execution.md), [questionnaire](references/questionnaires.md) or [documentation](references/documentation.md) contract when performing that work.
