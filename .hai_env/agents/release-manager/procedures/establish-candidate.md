# Establish the candidate

## Description

Assess release impact against published history and compatibility contracts, and return an evidence-based version recommendation or selection with outstanding dependencies.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit workspace root | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:release_objective] | Release objective, scope and authority | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:instructions] | Applicable workspace instructions and shared receiver context | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:repository_evidence] | Verified repository/source/published-baseline evidence supplied through leader | Mandatory | Caller or authorized context | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:version_choice] | Explicit version/bump or prior selection | Optional | Caller or authorized context | Apply the existing explicitly agreed initial/0.x policy; obtain a human version decision before version writes. |
| [input:candidate_options] | Change scope, source, notes, assessment, packaging additions, draft preference or automation request | Optional | Caller or authorized context | Use the single-bundle manifest/tag/archive conventions; infer no branch, remote, automation or publication authority. |

## Prerequisites

Explicit workspace/release objective, applicable instructions and established scope; trustworthy repository/source/published-baseline evidence through Leader before dependent claims.

## Rules

- **Impact evidence:** Release-manager MUST base version impact on reviewed public guarantees and actual changes rather than commit-message labels or edit counts.
- **Instruction changes:** Release-manager MUST include observable effects of changed public instructions in impact assessment even when code is unchanged.
- **Published-version identity:** Release-manager MUST reject published-version reuse or regression unless an explicitly agreed distinct channel makes the identity unambiguous.
- **No forced release:** Release-manager MUST NOT treat the existence of a diff alone as a requirement to release.
- **Missing version policy:** Release-manager MUST NOT infer missing initial, maturity, experimental or prerelease policy from a diff.

## Steps

1. Establish [input:workspace_root], [input:release_objective], [input:instructions], authority and supplied [input:version_choice]/[input:candidate_options]. Read the local release/contract/package authorities and owning declarations; inspect existing metadata, automation and available packaging/check tools.
2. Obtain/review [input:repository_evidence] through Leader: repository/destination, exact source, status, actual published history and baseline. Distinguish local tags from publication evidence and unrelated work from candidate scope; if history is missing, return the dependent baseline limit while continuing independent preparation.
3. Review actual changes since the published baseline across code, contracts, behavior, formats, conventions and governing instructions. List changed consumer guarantees, impact, relevant verification and uncertainty; if no releasable change or insufficient classification evidence, report that result rather than forcing a version.
4. For an established stable line, apply the release contract's highest applicable MAJOR/MINOR/PATCH impact and reset lower components under SemVer, explaining why lower increments fail. For initial/0.x/prerelease/build-metadata work, apply prior explicit decisions first; obtain only unresolved initial-version/maturity/breaking-policy/channel decisions before a numerical recommendation or version writes. Treat `0.1.0` as an example unless the existing agreed initial-release decision applies.
5. Present the recommendation for human selection/authorized acceptance, or retain the existing selected [input:version_choice]. If materially conflicting compatibility evidence appears, return the conflict rather than silently changing the version.
6. Assess bundle/specification/state-format impact independently against trustworthy history, declarations and the specification transition ledger. Return affected sources/consumers, old/proposed guarantees, evidence and required owner outcomes through Leader. If an actual tree is involved, request its owner's assessment/creation/migration gates and approval evidence rather than performing that work here.
7. Record verified compatibility/upgrade information, required migration scope and known limitations in the candidate assessment. Pass [output:candidate_assessment] as `candidate_assessment` to [Prepare and verify](prepare-and-verify.md), with `selected_version` only after human choice/recommendation authority exists; return the assessment and unresolved dependencies.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:candidate_assessment] | Version recommendation/selection, baseline, compatibility and release dependencies | Impact grounded in published evidence; owning decisions and unresolved consumer obligations explicit. |

## References

- [Release policy](../conventions/release_conv.md) — bundle versioning and readiness — required for every release.
- [Contract versioning](../conventions/contract-versioning_conv.md) — references to owning compatibility rules and release dependencies — required for every release.
- [Publishing policy](../conventions/publishing_conv.md) — packaging, authority, GitHub, and recovery — required for every release.
- [Agent convention](../../../../.hai/conventions/agent_conv.md) — receiver checks, role boundaries, and references — required for all operations.
- [Git-manager](../../git-manager/SKILL.md) — Git/GitHub execution boundary — conditional when specifying a repository/service dependency; leader performs routing, do not adopt or invoke that role.
- [Specification-manager](../../../../.hai/agents/specification-manager/SKILL.md) — ownership and relevant specification dependencies — conditional when assessing specification-rule changes or migration needs; do not adopt or execute that role.
- [State convention](../../../../.hai/conventions/state_conv.md) — state-format authority and configured context — required for release contract checks; conditional when interpreting environment state.
- [State contract](../../../../.hai/agents/environment-manager/contract.json) and [specification contract](../../../../.hai/agents/specification-manager/contract.json) — installed targets to snapshot and verify against the candidate's own declarations — required for every release.
- [Tooling convention](../../../../.hai/conventions/tooling_conv.md) — runtime and helper requirements — conditional when executing, creating, or changing supporting Python tools.
