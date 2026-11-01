# Install or update a source package

## Description

Copy a human-selected complete source package into a workspace installation and return validated installed bytes, actual registration status and unresolved local changes.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:inspection] | Verified scope, compatible environment, instructions, Activity, source identity and runtime collision findings | Mandatory | Establish scope and inspect result | Obtain the missing prerequisite before writes. |
| [input:source_package] | Explicit contained golden package folder selected as source data | Mandatory | Human request or authorized context | Return the missing source decision. |
| [input:install_authority] | Explicit install or update scope and selected installed name | Mandatory | Human request | Do not copy or update an installation. |
| [input:replacement_decision] | Reviewed baseline/differences and explicit human choice covering an existing installed package | Optional | Human decision and inspected evidence | Create only an absent destination; stop an existing-package update for review. |
| [input:registration_authority] | Explicit combined registration request | Optional | Human request | Leave a new copy unregistered; retain and synchronize an existing registration after an authorized update. |

## Prerequisites

Verified `inspection` output from [Establish scope and inspect](establish-scope-and-inspect.md), supplied as [input:inspection]. A compatible initialized environment, current Activity and human-directed source/installation scope. Existing-package replacement additionally requires review of complete installed-versus-candidate differences and an explicit human replacement decision. An unknown baseline or uncertain attribution stops replacement for that review; it does not prevent an informed human from choosing replacement after reviewing all differences.

## Rules

None.

## Steps

1. Resolve [input:source_package] and [input:install_authority] under [input:inspection]. Inspect the complete selected package as data, reject escaping or linked package files, check both runtime origins for collisions and establish `.hai_env/agents/<name>/` as the sole installed destination. Do not adopt the source role or register its library path.
2. For an existing destination, compare its complete file set and bytes with the requested candidate and any known prior source baseline. Stop for human review of local changes, missing baseline or uncertain attribution; do not invent whether differences are local or upstream. Continue only when [input:replacement_decision] explicitly covers the reviewed complete differences and selected replacement, including any unattributed differences. Do not infer update permission from a source edit.
3. Stage a complete ordinary file copy in a disposable workspace layout with the compatible `.hai/` core and necessary installed peers. Validate its canonical installed definition and supporting links, run relevant package checks and inspect compatibility assumptions. Read staged package resources for verification, without invoking unregistered definitions. No runtime link, import, symlink or hardlink may resolve to the golden source.
4. Recheck unchanged source, destination, catalogue, instructions and paths. Exclusively copy an absent destination. For approved replacement, preserve a recoverable prior copy in the agreed permitted location and replace the whole package with the reviewed staged bytes rather than overlaying stale files. Stop and report partial state on failure; do not automatically retry or roll back.
5. Read back and compare every installed file with the selected source candidate. Validate the installed canonical definition. Synchronize an existing catalogue row after an authorized update. For explicit [input:registration_authority], pass that authority, the installed definition and validation evidence plus [input:inspection] to [Register a validated definition](register-definition.md) as `registration_authority`, `target`, `validation_evidence` and `inspection`; otherwise leave a new copy unregistered.
6. Return [output:installation] with selected source, actual installed path/bytes, checks, registration and preserved local changes or partial results. Source maintenance, installation and registration do not enable features or integrations, change model profiles or authorize execution.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:installation] | Installed complete snapshot, validation, actual registration and unresolved differences | Source and installed bytes match the approved candidate; runtime resources use installed/core paths only; explicit registration verified or its absence stated; unrelated state and files preserved. |

## References

- [Role definition](../SKILL.md) — inherited ownership, preservation and source boundaries; required.
- [Agent tools](../../../../.hai/tools/agents/README.md) — staged and installed validation with two runtime origins; required before checks.
- [State convention](../../../../.hai/conventions/state_conv.md) — compatible context and catalogue format; required.
