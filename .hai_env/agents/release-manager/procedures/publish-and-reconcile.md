# Publish and reconcile

## Description

Hand off the frozen candidate for authorized publication and review the returned execution evidence, reporting verified publication or preserved partial-state dependencies.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:ready_candidate] | Selected version, full source commit, manifest, notes, asset path/name/digest, checks and compatibility evidence | Mandatory | Prepare and verify result | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:publication_destination] | Verified destination and single intended publication path/state | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:publication_authority] | Established candidate-specific authority for the requested external effects | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:execution_evidence] | Git-manager results returned through host coordinator | Optional | Caller or authorized context | Return frozen handoff through host coordinator; publication remains unverified until actual execution evidence arrives. |

## Prerequisites

Verified `ready_candidate` output from [Prepare and verify](prepare-and-verify.md), supplied as [input:ready_candidate]. Established candidate-specific [input:publication_authority] and verified destination/path; returned execution evidence is required before publication completion claims.

## Rules

None.

## Steps

1. Freeze [input:ready_candidate], [input:publication_destination] and [input:publication_authority]: selected version, full source, manifest, notes, asset path/name/digest, checks, compatibility, desired draft/prerelease/public state and single automation/local path. If scope/authority is missing, return the concrete dependency after authorized preparation.
2. Pass candidate/artifacts, desired effects, checks and authority through host coordinator for the registered Git extension's [release execution](../../git-manager/procedures/release-and-recover.md). Receive actual stage evidence; if registration, access, readiness or remote refs are unavailable, keep those effects pending under the inherited dependency rule.
3. Review [input:execution_evidence] against product readiness: actual tag/full commit, version, release URL/state, notes, workflow/check results and downloadable ZIP name/bytes/digest/contents. Inspect supplied downloaded assets with filesystem tools where available; request missing service/download evidence through host coordinator.
4. If material candidate facts changed, return for renewed readiness and authority-scope review before dependent publication. If failure/partial results occurred, preserve package/check evidence and return product blockers plus actual remote state/recovery needs through host coordinator to the Git owner.
5. Return [output:publication_review] with verified URL/status on success, otherwise precise prepared/draft/published/failed/unverified stages, completed effects, preserved partial state, checks/limits and remaining dependencies.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:publication_review] | Actual publication URL/status and product review, or preserved partial state | Tag/full commit, release state, notes, checks and downloadable package identity reviewed; prepared/draft/published/failed/unverified states distinguished. |

## References

- [Release policy](../conventions/release_conv.md) — bundle versioning and readiness — required for every release.
- [Contract versioning](../conventions/contract-versioning_conv.md) — references to owning compatibility rules and release dependencies — required for every release.
- [Publishing policy](../conventions/publishing_conv.md) — packaging, authority, GitHub, and recovery — required for every release.
- [Agent convention](../../../../.hai/conventions/agent_conv.md) — receiver checks, role boundaries, and references — required for all operations.
- [Git-manager](../../git-manager/SKILL.md) — Git/GitHub execution boundary — conditional when specifying a repository/service dependency; host coordinator performs routing, do not adopt or invoke that role.
- [State convention](../../../../.hai/conventions/state_conv.md) — state-format authority and configured context — required for release contract checks; conditional when interpreting environment state.
- [State contract](../../../../.hai/contracts/state.json) — installed target to snapshot and verify against the candidate's own declaration — required for every release.
- [Tooling convention](../../../../.hai/conventions/tooling_conv.md) — runtime and helper requirements — conditional when executing, creating, or changing supporting Python tools.
