# Configure specification settings

## Description

Validate or update this agent's HAI enablement and specification-root reference while preserving existing product content and unrelated configuration.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical HAI workspace | Mandatory | Caller or authorized context | Retrieve context; report the dependency before dependent setup. |
| [input:instructions] | Safe fixed mandatory instructions and applicable session/workspace instructions | Mandatory | Caller and fixed instruction file | Empty readable content is valid; report unavailable instructions. |
| [input:authority] | Requested validation, chosen settings or scoped repair authority | Mandatory | Human or Leader relaying the human request | Read-only diagnosis only; do not infer chosen changes. |
| [input:activity_context] | Stable current Activity ID/path and work context, or bounded diagnosis exception | Mandatory | Caller or authorized context | Retrieve before substantive setup; report unresolved dependency. |
| [input:setting_choices] | Optional Boolean enabled and workspace-relative directory location | Optional | Human's explicit choices | Validate only and preserve saved values. |

## Prerequisites

Explicit workspace, instructions and task context. Writes additionally require compatible format-3 core assurance and chosen setting/repair scope. Configuration work does not require enabled specification, tree contents or a tree compatibility marker.

## Rules

- **Chosen enablement:** Specification-manager MUST NOT change enablement or location without the user's corresponding choice or explicitly authorized value-preserving extraction.
- **No content effects:** Specification-manager MUST NOT create, move, delete, rewrite or adopt a specification tree when changing its configuration.

## Steps

1. Establish the workspace, instructions, authority and Activity context. Read the installed configuration contract and run the owner helper in read-only mode; keep core assurance, owner settings and tree compatibility as separate evidence.
2. If [input:setting_choices] is absent, return actual configuration status/settings and issues. Missing files use declared defaults. Malformed, unreadable or unsupported files are dependencies; an existing invalid file is never treated as absent.
3. For chosen changes, validate core format 3 and prepare only the chosen `settings.enabled` and/or `settings.location`, preserving config version, unknown root/nested values and unchosen fields. Validate directory containment, reserved locations, Activity/profile/config collisions and existing type even when disabled. An absent root directory is valid and does not authorize creation. Verify an existing root before explicitly linking it.
4. Run the owner helper's dry-run and review effective old/new settings and source hash. Invalid affected data needs separately scoped repair rather than the ordinary helper's replacement. A format-2 source goes through Environment-manager's explicit transition adapter, not ordinary settings setup or a legacy runtime fallback.
5. Recheck inputs and paths; apply only the chosen candidate using the reviewed hash. Read back the owner file and independently verify unchanged core/chronicles, instructions and unrelated configuration. On changed inputs or partial failure stop and report actual stages without automatic retry or rollback.
6. Return [output:configuration_result] with attributable status, owner-file path, effective settings, changed fields, old/new location where relevant, preservation checks and unresolved issues. A location reference change does not imply a content move or a tree compatibility assertion.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:configuration_result] | Validated owner settings, chosen changes and dependency/preservation evidence | Read-only status or actual verified changes reported; unknown/unrelated values and product content preserved; no enablement, tree migration or readiness claim is inferred. |

## References

- [Role definition](../SKILL.md) — shared rules; required.
- [Configuration contract](../configuration/contract.json) and [configuration convention](../conventions/configuration_conv.md) — supported settings, defaults and ownership; required.
- [Helper instructions](../scripts/README.md#hai-settings) — read-only validation and guarded setup; required before helper use.
- [Shared configuration convention](../../../../.hai/conventions/agent-configuration_conv.md) — envelopes and safe paths; required for HAI settings.
- [State convention](../../../../.hai/conventions/state_conv.md) — core assurance and explicit format transition; required before HAI writes.
