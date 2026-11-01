# Instruction writing

## Purpose and scope

This convention defines plain wording for HAI definitions and the vocabulary for
shared and procedure-local Rules. It does not grant permission, select an agent,
or define an author's execution workflow. Concepts explain meaning and rationale;
agent instructions own behavior. The [Procedure concept](../concepts/procedure.md)
explains the difference between rules, entry conditions, and steps.

## Rule vocabulary

| Wording | Meaning |
| --- | --- |
| `MUST` | A required action or condition within the rule's stated scope. |
| `MUST NOT` | A prohibited action within that scope. |
| `MAY` | An allowed choice within the user's existing permission and agreed task scope. It grants no new permission and says nothing about tool availability. |

These are the only words used to express requirement, prohibition, or permission
in Rules. They are uppercase and occur in the rule body, not merely its title.
`None.` alone means no additional local rules and requires no such word.
Inputs retain `Mandatory`/`Optional`; neither those labels nor explanatory concept
text is subject to this Rules vocabulary requirement.

`SHOULD`, `SHOULD NOT`, `SHALL`, `ought to`, and contractions such as `mustn't`
are not alternative obligation words. `MAY NOT` is ambiguous: prohibition uses
`MUST NOT`; permission to omit something uses a positive phrase such as
`MAY omit the optional appendix`. `Can` describes ability, not permission.
Literal words, code, and examples retain their exact content; inline code or
fenced examples distinguish them from the rule's own wording. Quotation marks
alone do not establish a machine-checked exception.

`IF`, `WHEN`, and `ONLY IF` state conditions, not strength or permission. `IF`
describes the applicable branch; `WHEN` can describe timing; `ONLY IF` states a
necessary condition and does not promise that it is sufficient. Positive explicit
conditions are clearer than `unless` or double negatives. An exception names the
condition and permitted alternative rather than implying an override.

## Plain rule structure

A rule has a short readable title and names the actor, action, object, and any
condition needed to understand its scope. One independent instruction per rule is
the default. A related exception or default can remain beside it when separating
them would obscure their relationship. No word-count limit justifies compressed
phrases, unexplained abbreviations, or deleting a condition.

```markdown
- **Authorized scope.** The leader MUST NOT perform or delegate work outside the user's agreed task scope, even when an agent, feature, or tool is available.
- **Missing source.** IF the required source is unreadable, the agent MUST report that problem before dependent work.
```

Familiar words and concrete verbs make an instruction easier to review. Necessary
technical terms and exact identifiers remain valid when precise and explained in
a linked concept or contract. Words such as "gates" or "authority" are not a
substitute for naming the required checks, permission, or agreed scope. A rule
states behavior; background explanation belongs in a concept, an entry condition
in Prerequisites, and ordered actions or branches in Steps.

## Preserving meaning in revisions

An existing requirement remains required, a prohibition remains prohibited, and
an allowed choice remains allowed. A preference is not automatically upgraded to
`MUST`: it can be represented as the existing default with its permitted
alternatives stated explicitly. For example, a connector preference is distinct
from a ban on all command-line tools. Existing defaults, exceptions, trigger
conditions, failure handling, and user permission remain part of the meaning.
If an old preference does not establish when alternatives are allowed, that is an
unresolved policy question rather than permission to invent a stricter rule.

## Verification limits

Shared tools check the documented Markdown structure and selected word forms.
They do not prove that an actor is clear, a condition is complete, a permission is
valid, or a revision preserves meaning. Keyword presence alone proves none of
these. Authoring and review procedures belong to agent-definition-manager.

## References

- [Agent convention](agent_conv.md): role structure and shared rule scope.
- [Procedure convention](procedure_conv.md): procedure-local Rules structure.
- [Procedure concept](../concepts/procedure.md): meaning, scope, and rationale.
- [Agent tools](../tools/agents/README.md): exact supported checks and their limits.
