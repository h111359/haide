# Configure backlog

## Description

Establish a safe backlog location and its initial structure, or prepare an explicitly requested relocation with preserved records.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit existing workspace and validated core/Activity context. | Mandatory | Host coordinator. | Retrieve context before dependent writes. |
| [input:request] | Requested setup, setting change or separately scoped relocation. | Mandatory | Caller. | Retrieve intent; do not infer relocation from a new path. |
| [input:location] | Chosen workspace-relative folder. | Optional | Caller or valid installed settings. | Use the declared backlog default only when settings are absent. |

## Prerequisites

A valid initialized HAI environment, readable fixed instructions, current Activity and authority for the selected setup or setting change.

## Rules

None.

## Steps

1. Load the installed configuration contract and fixed external settings using the shared configuration helper. Resolve the effective root from [input:location] and [input:request] in [input:workspace_root]; distinguish absent settings from invalid or unreadable settings.

2. Validate the root with the shared workspace directory validator and current core protected paths. Separately validate the installed registered Specification-manager configuration when relevant and reserve its content directory even when disabled. An absent optional owner adds no content root; invalid or unverified owner paths block dependent writes. Reject linked ancestors and directory/file collisions.

3. Inspect only the selected root. If it contains an existing backlog, validate it and report its actual contents before changes. If it contains draft or unrelated material, preserve it and identify any conflicts; setup is not permission to import or overwrite it.

4. For authorized initialization, exclusively create missing new/ and closed/ folders and a catalogue with the empty table from the backlog format. Recheck the target and current bytes before each write. An absent custom root does not require it to be beneath .hai_env/.

5. For an explicitly requested location-setting change, use runtime configuration update for the installed backlog-manager location field with supplied provenance. Preview and inspect the result before apply; preserve unchosen and unknown settings. A missing installed contract is a setup dependency, not permission to read library defaults as a runtime fallback.

6. If relocation was explicitly requested, inventory both roots first and plan a no-overwrite move preserving item IDs and exact bytes, history and references. Original draft audit artifacts remain with their Activity and are not part of backlog relocation. Verify destination contents before changing the setting; do not silently merge roots or delete evidence. Stop and report partial writes on failure.

7. Run the read-only audit against the effective root; report root, settings status, created/moved paths, remaining conflicts and actual verification.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:backlog_context] | Effective root, settings evidence, structure and observed changes. | Root is safely inside the workspace, dependent paths checked and actual setup status distinguished from pending work. |

## References

- [Role rules and references](../SKILL.md) — shared ownership, constraints and required reading.
- [Backlog format](../conventions/backlog_conv.md) — record, catalogue and history contracts; required for this procedure.
- [Audit helper](../scripts/README.md) — required before helper execution.
