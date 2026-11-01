# Load existing environment

## Description

Validate existing environment configuration and load readable mandatory instructions, returning independent catalogue, profile and prerequisite findings.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit canonical workspace root. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions, including the fixed mandatory instructions file. | Mandatory | Caller and safe readable `.hai_env/agent_instructions.md` | An existing empty file is valid. Missing/unreadable instructions block dependent work; diagnose or perform only authorized setup/repair. |
| [input:authority] | The user's requested operation, agreed scope, constraints and permissions already given. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:operation] | Requested environment validation/load. | Mandatory | Caller and authorized workspace context | Retrieve authorized context first; if unresolved, return the dependency and pause dependent work. |
| [input:startup_context] | Previously verified unchanged files, runtime evidence or validation findings. | Optional | Caller and available authorized context | Perform applicable checks; report unavailable checks without inventing results. |

## Prerequisites

Read the shared Environment, state and model-profile references plus the installed [state contract](../contract.json) and [state template](../templates/state.json) as relevant. Read the startup-helper README before first use; do not reread unchanged knowledge already in context.

## Rules

- **Unavailable checks.** Environment-manager MUST report helper checks that cannot run as unverified.
- **Validation strength.** Environment-manager MUST NOT weaken duplicate-key or path checks during fallback validation.
- **Runtime installation.** Environment-manager MUST NOT install a runtime implicitly to complete fallback validation.
- **Read-only validation.** Environment-manager MUST NOT mutate the environment during validation.

## Steps

1. Establish [input:workspace_root] and [input:operation]/[input:authority]. Validate and load the fixed [input:instructions] independently of state compatibility, recording exact decoded text/status before dependent work.

2. Run the read-only startup helper using an explicit workspace and working interpreter. Compare [input:startup_context] with unchanged inspected inputs and use only still-valid results.

3. Inspect the helper's scoped results. Reuse completed checks and perform checks below only for missing applicable evidence; if the helper is unavailable, report its limit and perform the full applicable fallback with available tools. Mark unavailable checks unverified.

4. In fallback, validate the environment container and state path/target. Record safely absent state as an initialization dependency, or record exact invalid/unreadable/unsafe-target findings; keep state-dependent checks unavailable while continuing independent checks.

5. For a readable safe existing state, parse duplicate-free state and validate the installed supported version, mandatory Activity location, central chronicles settings and safe paths; recognize supported format 2 as read-only migration context with no specification fallback. Report malformed/incompatible core state before optional content loading.

6. Validate the independently available framework and workspace catalogue structure, identity and canonical references under the shared agent/state contracts. Return independent valid entries and excluded row/table findings; report any discovered stale description copy.

7. For usable core state, return validated Activity-store location/type and central chronicles enablement/effective threshold, default 5 when absent. Boundedly inspect only the valid registered installed Specification-manager configuration contract/file, without scripts or tree contents, and return its separate `agent_configurations` status/settings/path or isolated unavailable/invalid result. Core startup remains independent of this optional owner; format-2 context reports migration_required with no effective owner fallback. Inspect optional model profiles and report absent/valid/invalid mappings and supported-runtime evidence limits.

8. Assemble [output:environment_context] with core condition, instruction text/status, validated independent registrations, locations/flags, profile findings and isolated issues; identify checks that could not run.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:environment_context] | Environment condition, instructions exact decoded text/status, Activity location, central chronicles, separate owner-configuration and migration status, independent valid registrations, profile mappings/runtime limits and issues. | Complete every applicable startup check or identify it as unverified; separate invalid core state from isolated optional/registry problems. No configuration or record discovery is performed. |

## References

- [Role definition](../SKILL.md) — rules and shared references; required before this procedure.
