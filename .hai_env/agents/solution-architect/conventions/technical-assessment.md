# Technical assessment

## Representation

Use one initial H1 title and exactly these ordered H2 sections: Identity and input,
Interpretation, Scope and exclusions, Evidence and findings, Edge conditions,
Options, Knowledge effects, Decisions, Readiness. Every section is nonempty;
explicitly explain an applicable absence, including no consequential decisions.
Use ordinary Markdown prose, lists and pipe tables; no HTML structure.

Identity and input contains unique `- Activity:`, `- Input revision:` and
`- Decision revision:` fields. The runtime Activity UUID remains stable. Revisions
identify actual current input and decision evidence; verified absence can be
`none`. Preserve exact human contributions in current records and link them rather
than replacing them with the assessment interpretation.

## Content

Interpretation explains intent, motivation, domain terms and affected parties.
Scope distinguishes requested work, affected components/documents and exclusions.
Evidence and findings attributes reviewed resources, attachment inventory,
unreadable/nontext limits, research results, individual quality concerns and risks.
Concern entries distinguish requested fixes from discoveries outside scope.

Edge conditions addresses empty/boundary values, first use, revision, conflicting
state, missing prior artifacts, migrations and failure/recovery where relevant.
Options describes alternatives and their tradeoffs without treating recommendations
as decisions. Explain the proposed approach plainly, then decompose it into ordered
single-target actions with dependencies.

Knowledge effects identifies insertions, revisions or removals, target identity,
existing purpose, conflicts and required owner validation. Research missing facts
before asking consequential questions. Do not enable disabled knowledge features.

Decisions distinguishes actual human choices, governing instructions, delegated
choices and unresolved decisions. Preserve the exact supporting statement and
source; unresolved options remain neutral. Use the existing Business analyst
dialogue contract for questions, raw answers, ambiguity and revisions through host.

## Technical readiness

Readiness contains one `Check | Status | Evidence` table with exactly these IDs
in order. Status is `passed` or `blocked`; each row gives actual evidence or the
specific failed dependency and affected actions. A ready result requires all six
passed and no critical unresolved concern, independently of structural validity.

| Check | Meaning |
| --- | --- |
| T1 | Current requirements/business-readiness evidence or its applicable narrow exemption |
| T2 | Known affected components, interfaces and implementation evidence |
| T3 | Critical decisions resolved by actual authority; assumptions and delegated choices explicit |
| T4 | Compatibility, edge cases, migration and failure/recovery evaluated |
| T5 | Feasible acceptance and appropriate verification methods |
| T6 | Current conventions, permissions, knowledge owners and required dependencies identified |

Blocked assessments remain useful provisional review artifacts. Do not publish a
false ready result, invent missing sources or silently repair meaning. After a
changed input/answer, retain predecessors through host runtime revision history,
update affected conclusions and reassess current readiness.

## References

- [Assess solution](../procedures/assess-solution.md) — owning workflow.
- [Resolve decisions](../procedures/resolve-technical-decisions.md) — clarification and revisions.
- [Business readiness](../../business-analyst/conventions/requirements-readiness.md) — business gate; this technical table does not replace its 28 checks.
- [Helper contract](../scripts/README.md) — structural diagnostics and limitations.
