# Procedure format

## Ownership and selection

A procedure belongs to its agent. Executing it does not select, register, or
delegate to another agent. Shared role rules remain in `SKILL.md` and always apply.
The selected procedure supplies a short description, inputs, prerequisites,
procedure-specific rules, execution steps, outputs, and references. The
[Procedure concept](../concepts/procedure.md) explains these distinctions.

Multiple procedures use a single index in the agent's Procedures section:

```markdown
| Procedure | Trigger | File |
| --- | --- | --- |
| Inspect material | The caller requests an inspection. | [Inspect](procedures/inspect-material.md) |
```

Procedure names and resolved files are unique within the index. Every trigger is
nonblank and canonical in that index, not repeated in its external file. A trigger
identifies applicability, never permission, priority, or automatic execution.
File links are exactly `procedures/<lower-case-kebab-name>.md`, relative to
`SKILL.md`, and must resolve to readable regular files inside the same agent
package and workspace. Reject escaping links, traversal, queries, fragments,
alternate separators, and duplicate resolved files.

## External file

Use one initial H1 name and exactly these H2 sections in order:

```markdown
# Inspect material

## Description

Inspect the requested material and return evidence-grounded findings within the supplied scope.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:task] | Requested inspection. | Mandatory | Caller. | Retrieve context, then report unresolved intent. |

## Prerequisites

Conditions that must be satisfied before execution, or None.

## Rules

None.

## Steps

1. Inspect the material identified by [input:task].

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:result] | Inspection findings. | Findings supported by observed evidence. |

## References

Relevant sources and their reading conditions, or None.
```

Description is required immediately after the title, before Inputs. Use one or two
short sentences explaining this procedure's specific purpose and intended result;
do not repeat its trigger or add behavior. An empty description or `None` is invalid.
Prerequisites state entry conditions, not ongoing obligations or concept explanations.
Rules is mandatory between Prerequisites and Steps. Use literal `None.` alone when
there are no procedure-specific rules; shared rules still apply. Otherwise use
short '-' bullets beginning with bold readable titles unique within that Rules
section, without IDs. Optional H3 subject groups organize related rules; use no
empty groups. Inline procedures use H5 groups. State each rule's applicability and
exceptions explicitly. Local rules apply only within this procedure: they neither
override shared rules nor duplicate rules already owned by `SKILL.md` or a
referenced contract. Raise a conflict rather than infer an override from locality.
The [instruction-writing convention](instruction-writing_conv.md) defines the
shared `MUST`/`MUST NOT`/`MAY` vocabulary and plain wording. It applies to every
local rule, with `None.` alone exempt; existing inputs remain Mandatory/Optional.

Steps describe ordered actions and explicit conditional branches, with data supplied
before the action that consumes it. Do not number ongoing rules, prerequisites,
or concept explanations as execution steps. Steps may use subordinate headings.
Preconditions are distinct from the index's trigger and do not duplicate it.
Inputs and Outputs each contain one table with the exact shown columns;
header-only tables declare no parameters. All data cells are nonblank. Use
`Mandatory` or `Optional` only: no Conditional category. An operation-specific
prerequisite can require an otherwise optional value; its rule/prerequisite must
state that requirement explicitly. Optional values retain declared defaults or
remain absent. Nothing here grants new permission or implicit defaults.

Outputs describe observable results and completion evidence. Distinguish actual,
partial, unavailable, and pending results; do not declare future work completed.
Use [reference-notation_conv.md](reference-notation_conv.md) for local references,
term mappings, and explicit passing between procedures.

## Single inline procedure

An agent with one procedure may instead place it inline under Procedures. Use
`### <name>`, one nonblank `Trigger: ...` line, and the seven sections above as H4
headings. The inline trigger is canonical beside that procedure. Do not combine
an inline procedure with an external index or inline several procedures. A single
procedure may also use the external index/file form.
The required `#### Description` follows the trigger and precedes `#### Inputs`.

## Supported authoring subset

Tables use one physical line per row, leading/trailing pipes, exact column names,
and `---` alignment cells (optional edge colons). Encode literal cell pipes as
`&#124;`; multiline cells, escaped literal pipes, nested tables, reference-style
file links, and HTML table syntax are unsupported. Declaration tokens may be plain
or enclosed in one pair of backticks. Fenced examples are excluded from checks;
unclosed fences are invalid. Content meaning and execution order still require
human review; this is a Markdown contract, not an execution engine.
Rule bullets start at the left margin; indented prose may continue their obligation.
Arbitrary unlabelled rule prose, nested lists, numbered rule IDs, empty rule bodies,
and a `None.` marker combined with other Rules content are invalid. Structural
checks do not prove that local rules are specific, nonduplicative, or consistent.
Literal inline-code words and fenced examples are excluded from modal checks,
not from the human's responsibility to interpret their meaning correctly.
