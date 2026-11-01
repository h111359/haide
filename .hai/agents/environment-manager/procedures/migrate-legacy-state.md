# Migrate explicitly authorized legacy state

## Description

Migrate explicitly authorized legacy configuration while preserving source provenance and unrelated properties, and return compatibility evidence or precise partial results.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:activity_context] | Stable current Activity ID, path and relevant record context for substantive work; applicable bootstrap/diagnosis exception when no record is needed. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:migration_authority] | The user's explicit migration permission, source format, approved mapping and scope. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:legacy_source] | Duplicate-free complete legacy state, relevant paths and configuration provenance. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |

## Prerequisites

Read the shared Environment, state and model-profile references plus the installed [state contract](../contract.json) and [state template](../templates/state.json) as relevant. Read the startup-helper README before first use; do not reread unchanged knowledge already in context. Explicit migration permission supplies a source format and approved mapping; validation failure alone is insufficient.

## Rules

- **Approved conversion.** Environment-manager MUST limit state conversion to the approved configuration mapping.
- **Separate record work.** Environment-manager MUST return record/history or exact-transcript migration work to Leader for the responsible specialist.
- **Prototype mapping.** Environment-manager MUST require a mapping specific to an earlier prototype before migrating that prototype.
- **Version marker.** Environment-manager MUST NOT replace a version marker alone while leaving incompatible structure unchanged.

## Steps

1. Establish [input:workspace_root], load [input:instructions], and compare [input:migration_authority] with [input:authority]/[input:activity_context]. Identify [input:legacy_source] and the approved source-format mapping.

2. Read duplicate-free complete source state, validate relevant safe paths, and record old store/destination provenance needed for separately scoped history handling.

3. Prepare the format-2 candidate under the approved mapping: mandatory Activity location, preserved specification configuration and chronicles enablement, with obsolete request settings/global chronicles location removed. Preserve unrelated and opaque extension-owned properties; return uncarryable properties or path conflicts for resolution.

4. Validate the complete candidate and preserve a recoverable inspected source under the authorized state-convention procedure. Recheck unchanged source/paths immediately before the guarded write.

5. Read back and run the startup helper; compare preserved properties and all format-2 invariants. Return partial results on conflict/verification failure.

6. Return [output:migration_result] with verified configuration, provenance and separate record/transcript dependencies for leader routing.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:migration_result] | Verified compatible candidate, preserved properties and source provenance, or precise partial failure. | Helper verifies complete mapping instead of marker-only reset; return separate record/transcript migration dependencies, never silently discard history. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
