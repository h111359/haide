# Installing and upgrading HAI

The current source prepares the [0.4.0 release candidate](release-notes/0.4.0.md); exact source and package evidence are recorded separately. Actual publication status is tracked on [GitHub Releases](https://github.com/h111359/haide/releases). Published [0.1.0](release-notes/0.1.0.md), [0.2.0](release-notes/0.2.0.md), and [0.3.0](release-notes/0.3.0.md) retain their own compatibility targets.

HAI requires Python 3.11 or later and a host that can read workspace instructions and run commands. Optional agent invocation, models and integrations depend on the host; installing HAI does not establish those capabilities. Copy the complete reusable `.hai/` tree into the workspace, retaining the license and avoiding unrelated project files, and direct the host to [.hai/start.md](.hai/start.md). The runtime entry point and operation contracts are documented in [runtime commands](.hai/tools/runtime/README.md). It is not a background service or an automatically installed Python package.

Before replacing an existing framework, preserve the workspace's `.hai_env/`, configured Activity and specification data, and product files. A framework upgrade does not itself migrate state, records or transcripts. Current state format is 3; supported format 2 is read-only migration context. Preserve invalid, unsupported or conflicting state and use only an explicitly authorized migration after reviewing its inputs and backup/partial-result behavior. See the [state convention](.hai/conventions/state_conv.md) and [Activity migration notes](release-notes/activity-migration.md). Preserve Activity IDs, human inputs, revisions and transcript provenance through an upgrade.

Optional workspace extensions are separate complete packages under `.hai_env/agents/`, with explicit entries in its catalogue. Golden source packages in `hai_agents_library/agents/` are data; they do not execute from the source library. Installation, replacement, registration and execution are separate actions. Preserve local modifications and external settings at `.hai_env/config/agents/`, review replacement differences, and do not infer enabled capabilities or permission from a package being present. Core startup and administration require no optional extension or model profile. See [agent configuration](.hai/conventions/agent-configuration_conv.md).

## Upgrading the environment layout in 0.4.0

The canonical fixed files are `.hai_env/config/state.json`,
`.hai_env/config/agent_instructions.md`, and optional
`.hai_env/config/model_profiles.json`. Existing files directly under `.hai_env/`
are migration inputs, never fallback runtime authorities.

After preserving local changes and replacing the reusable core, follow the
[layout migration procedure](.hai/procedures/migrate-environment-layout.md).
Safely read and apply the legacy instructions first, stop other environment
writers, and prepare a workspace-contained JSON request with the actual migration
instruction identified in `provenance.source` and a meaningful `provenance.reason`.
Using a verified absolute Python 3.11+ executable, preview:

```text
<absolute-python> -B .hai/tools/hai.py environment migrate-layout --workspace . --request <workspace-contained-request.json>
```

Only after explicit authorization and review of hashes/moves, repeat with
`--apply`, inspect recovery copies and `config/layout-migration.json`, then run
startup and reload canonical instructions. The migration preserves exact bytes;
it does not convert state format or move Activities/specifications. Mixed layouts,
conflicts, unexplained locks and partial operations require reviewed resolution,
not automatic merging or retry. Format-2 specification extraction remains a
separate explicitly authorized operation after layout migration.

## Work and output boundaries

Apply the shared [workspace boundary](.hai/conventions/workspace-boundary_conv.md)
and [artifact placement contract](.hai/conventions/artifact-placement_conv.md).
Outside file writes require explicit user location/purpose permission, including
temporary files and tool effects. Requested outputs retain their canonical
destinations; task scratch, run results and review evidence stay with their owning
Activity/invocation unless a governing contract designates otherwise.

The core ZIP does not install optional agents. To obtain updated optional packages,
use a checkout of the exact release source and its `hai_agents_library/agents/`
packages, then follow runtime preview/apply installation and registration. Preserve
external settings and review existing local differences before replacement.
