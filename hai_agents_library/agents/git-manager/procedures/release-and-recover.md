# Tags, releases, and recovery

## Description

Execute authorized tag, release, and asset operations against the frozen candidate, and return verified publication evidence or preserved partial-state recovery dependencies.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:operation_context] | Verified target, gates and established authority | Mandatory | Operation workflow result | Retrieve from authorized context; return the specific dependency and pause dependent work. |
| [input:candidate] | For product releases: frozen version, full source commit, tag, notes, asset identity/digest, readiness, destination and authority | Optional | Caller or authorized context | Product release execution blocks until a complete frozen candidate is supplied; independent recovery may proceed. |
| [input:partial_results] | Observed completed operations and partial state for recovery | Optional | Caller or authorized context | Inspect current state before recovery; do not infer completed operations or blindly retry. |

## Prerequisites

Verified `operation_context` output from [Operation workflow](operate.md), supplied as [input:operation_context]. Product publication needs complete frozen [input:candidate]; recovery needs established cause, actual partial state and applicable authority.

## Rules

- **Product owner:** Git-manager MUST leave version, policy, metadata, notes, packaging and readiness decisions with the selected product release owner.
- **Source before package:** Git-manager MUST provide the verified source commit and export before expecting package preparation from the release owner.
- **Frozen publication input:** Git-manager MUST use the release owner's frozen ready candidate for product publication.
- **Product review evidence:** Git-manager MUST return publication evidence through Leader for the release owner's final product review.
- **Exact tag target:** Git-manager MUST place a tag at the full intended commit rather than an unspecified default branch.
- **Existing remote target:** Git-manager MAY use an already verified remote target for an authorized release API operation.
- **Draft permission:** Git-manager MUST have permission for the remote write before creating a draft.
- **Publication permission:** Git-manager MUST have publication permission before publishing a draft.
- **Published assets:** Git-manager MUST NOT silently move published tags or replace published assets.
- **Recovery request limits:** Git-manager MUST NOT treat a request to recover as permission to delete resources, rewrite history or retry without checking current state.

## Steps

1. Establish [input:operation_context]. For product source preparation, receive exact metadata paths and existing authority through Leader; create the source commit under [Commits and local changes](commit-and-export.md) with `operation_context` and actual source scope as `commit_scope`, then supply the verified full commit/export for the release owner's package/check stage.
2. For product publication, receive the complete frozen [input:candidate] through Leader: selected version, full source commit/tag, notes, asset path/name/digest, readiness, destination and authority. If incomplete, return the missing candidate dependency before product-publication effects. For other authorized tag/service work, use the exact full commit/ref/content already established in [input:operation_context] without inventing product-release inputs.
3. Verify candidate source/asset identity, existing tags/releases/assets, relevant automation and authority. Choose one authorized publication path to avoid CI/local races. If required remote refs or push capability are absent, return the manual-push/ref dependency; otherwise execute the authorized exact-source tag/release/asset effects.
4. Verify the affected requested resources: applicable remote tag/peeled commit, release URL/state, notes, asset identity/digest and download where available. Pass source identity/artifacts/checks/authority and observed publication evidence through Leader for the release owner's final review.
5. For partial failure or recovery, inspect [input:partial_results] against actual current local/remote state, establish cause and authority, then propose/perform only scoped authorized recovery. If any dependency remains unresolved, stop dependent mutations and preserve completed resources/evidence.
6. Return [output:release_or_recovery] with actual completed effects, source/asset/publication evidence, preserved partial state and recovery dependencies.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:release_or_recovery] | Verified tag/release/asset evidence or preserved partial state | Remote tag/peeled commit, URL/status, notes and asset/download identity reported where possible; unresolved recovery dependencies explicit. |

## References

- [Role rules and references](../SKILL.md) — gates, authority, safety and applicable sources.
- [Agent convention](../../../../.hai/conventions/agent_conv.md) — receiver checks and leader-only routing — required for all tasks.
- [State convention](../../../../.hai/conventions/state_conv.md) — generic core-state envelope and preservation requirements — required before extension configuration writes.
- [Startup helper](../../../../.hai/tools/startup/README.md) — core environment assurance only; it does not validate extension settings — conditional when interpreting core helper output.
- [Tooling convention](../../../../.hai/conventions/tooling_conv.md) — Python runtime and helpers — conditional when executing or changing supporting Python tools.
- Current installed tool help and official Git/GitHub documentation — command behavior and service limits — conditional when needed for the selected operation.
- [Git configuration contract](../conventions/git-configuration_conv.md) — independent switches, unavailable states and scoped preservation — required before configured operations or setup.
- [Extension helper](../scripts/README.md) — read-only saved-setting validation and limits — required before first local helper use.
