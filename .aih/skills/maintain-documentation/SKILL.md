---
{
  "name": "maintain-documentation",
  "description": "Apply authorized documentation increments and organize current product knowledge into a balanced navigable tree.",
  "metadata": {
    "aih": "{\"id\":\"maintain-documentation\",\"display_name\":\"Maintain documentation\",\"version\":\"1.0.0\",\"purpose\":\"Apply authorized documentation increments and organize current product knowledge into a balanced navigable tree.\",\"capabilities\":[\"documentation\",\"rebalancing\",\"known-defects\"],\"excludes\":[\"Changing human business intent\",\"Rewriting product implementation\"],\"input_contract\":\"references/standalone.md\",\"output_contract\":\"references/standalone.md#outputs\",\"standalone_parameters\":[\"contract\",\"data\",\"artifact\"],\"effects\":[\"scoped-output-records\"],\"write_scope\":\"Only explicit root-qualified invocation scope; no writes to read-only roots, human instructions, immutable core or outside folders.\",\"prerequisites\":[\"Explicit initiating instruction and applicable authority\",\"Validated root-qualified inputs/outputs and current workspace revision\"],\"authorization\":[\"documentation\"],\"dependencies\":[\"python>=3.11\"],\"compatibility\":\"AIH contract 1.0; Python 3.11+ standard library; secure POSIX writes. Other hosts require a compatible confinement backend.\",\"bundle_version\":\"1.0.0\",\"default_enabled\":true,\"output_summary\":\"Current knowledge, verified increments, known defects, catalogs, provenance and structural changes.\"}"
  }
}
---

# Maintain documentation

Use deterministic helpers for inventory, parsing, validation, writes and evidence. Agent judgment supplies semantic interpretation and scoped patches; helper failure is an explicit capability gap, never permission to bypass validation. Read metadata first and only the relevant references; do not preload every package. Runtime execution must not modify this package or another immutable core. Disable Python bytecode. Human-owned instructions and workspace membership are read-only to the agent.

For installed AIH, the engine owns submission snapshots, global action reservation, current revisions, profile choice, state transitions and archival. Use its typed operation catalog and [semantic result shapes](references/semantic-results.md). For standalone use read [the compact contract](references/standalone.md), validate the explicit contract, and persist effective authority plus result references with the output. Do not recreate the AIH lifecycle. Declared effects are not permission grants.

Read the planned documentation increment and actual implementation/source evidence. Preserve the central current product knowledge and human-authored sections. Update affected topic sections, not the whole corpus. Keep intended requirements, observed implementation, verification and deployment distinct. Proposed future behavior remains in its request; inference cannot silently become business intent.

Use stable canonical topic IDs and root-qualified provenance bound to workspace revision. Maintain all applicability categories, required traceability and known defects. A known defect records evidence/symptoms/reproduction, components/impact, supported workaround, disposition and origin; suspected findings remain unconfirmed. Link verification of resolution. Do not turn a defect catalog into an active backlog.

Use bundled tree validators and revision-checked writes to preserve one structural parent, no cycles/missing/unreachable/duplicate nodes, maximum eight children, leaf depth difference at most one, meaningful topic grouping and approximately 1,500 words per leaf. Record justified indivisible exceptions. Rebalance via recoverable transactions with snapshot-aware readers, preserving IDs and old-reference mappings. Never pad with empty leaves.

Reconcile planned/applied/verified increment entries with actual before/after fingerprints and evidence. A no-impact finding needs rationale. Partial implementation marks affected topics stale. Cancelled/rejected work leaves a discoverable current-state notice of retained changes, affected topics, defects and uncertainty with archived references. Successful completion requires reconciled documentation and reconstruction specification review; it does not require or establish a demonstrated independent rebuild.

Read [workspace boundaries](references/workspace.md) for path/access changes, [record ownership](references/records.md) for revisions, and the relevant [execution](references/execution.md), [questionnaire](references/questionnaires.md) or [documentation](references/documentation.md) contract when performing that work.
