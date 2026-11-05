# Inspect repository discovery boundaries

## Description

Return targeted effective-ignore and repository-aware discovery evidence within the caller's explicit product-source boundary, preserving exclusions and privacy limits.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:operation_context] | Verified target, enabled Git, authority and safe repository scope | Mandatory | Operation workflow `operation_context` output through caller | Complete the prerequisite before Git-aware discovery; ordinary filesystem discovery elsewhere remains independent. |
| [input:source_roots] | Explicit verified product source roots and requested discovery targets | Mandatory | Caller | Retrieve scope; never infer source root from a specification root. |
| [input:exclusions] | Reusable framework/agent, configuration/working-record, private/sensitive and library boundaries | Mandatory | Caller and governing workspace instructions | Resolve applicable exclusions before expansion; do not guess permission to inspect descendants. |

## Prerequisites

Verified `operation_context` output from [Operation workflow](operate.md), supplied as [input:operation_context]. Explicit verified product [input:source_roots], discovery targets and resolved [input:exclusions].

## Rules

- **Excluded product sources:** Git-manager MUST exclude reusable frameworks/agents, configuration/working records and their descendants from product registration and reverse-engineering, including this HAI workspace's `.hai/`, `.hai_env/` and `hai_agents_library/` roots.
- **Governing instructions:** Git-manager MAY read governing instructions despite product-source exclusions.
- **Ignored product sources:** Git-manager MUST exclude ignored folders and descendants from product registration and reverse-engineering.
- **Library root entry:** Git-manager MAY represent a verified third-party/dependency library by its top folder and brief purpose even when that folder is ignored.
- **Library descendants:** Git-manager MUST NOT enumerate, register, inspect or reverse-engineer a library's descendants.
- **Independent discovery:** Git-manager MUST NOT treat missing or disabled Git as blocking generic bounded filesystem discovery outside this optional repository-aware service.
- **Partial ignore evidence:** Git-manager MUST NOT present unavailable or partial evidence as complete repository-ignore coverage.
- **Ignored-content privacy:** Git-manager MUST NOT use partial evidence as permission to expose unrelated ignored names or content.

## Steps

1. Bound [input:source_roots] by [input:operation_context] and [input:exclusions]. Read governing instructions and identify permitted explicit targets without following escaping links or inventorying unrelated descendants.
2. Evaluate effective Git ignore rules for those targets, including nested `.gitignore`, precedence, negation and excluded-parent behavior. Collect only required classifications/rule provenance from actual Git-aware evidence, rather than fixed folder-name guesses.
3. Identify permitted library root/purpose evidence from manifests, lockfiles, configuration or reliable documentation outside excluded descendants. Distinguish verified dependencies from first-party folders merely named `lib`; mark uncertain classifications.
4. Verify the proposed evidence respects product/ignored/library/privacy boundaries, then return [output:discovery_evidence] through host coordinator with roots/targets, effective rule coverage, exclusions, uncertainty and unavailable checks.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:discovery_evidence] | Targeted repository/ignore classifications and scope/coverage limits | Verified roots, effective rules and exclusions supported by actual evidence; no unauthorized expansion or implied complete scan. |

## References

- [Role definition](../SKILL.md) — gates, authority, credentials and preservation; required.
- [Operation workflow](operate.md) — verified operation context; required prerequisite.
- Current installed Git help and official documentation — ignore behavior; conditional when uncertain.
