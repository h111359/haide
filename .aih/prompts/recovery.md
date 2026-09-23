# Recover semantic work

Use [execution](../conventions/execution.md) and [workspace](../conventions/workspace.md) contracts. Read the owning checkpoint, actual content fingerprints, current workspace mapping/access, submitted revisions, plan authority, task outcomes and process termination evidence. Determine which effects already occurred before proposing retries.

Resume only within current authority. A former path mapping or old approval cannot restore a removed root, permit read-only writes, erase a failed test, or bypass documentation reconciliation. Preserve successful valid evidence, explicitly invalidate stale dependencies, and record incomplete/uncertain outcomes. Do not assume cross-filesystem atomicity. If the action can no longer complete safely, state the exact explicit resolution needed.
