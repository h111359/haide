# Reference notation

## Meaning and namespaces

HAI uses literal, human-readable references:

| Reference | Meaning | Resolution |
| --- | --- | --- |
| `[term:Activity]` | A concept or supporting term. | An explicitly declared concept reference. |
| `[input:task]` | A procedure input. | That procedure's Inputs table. |
| `[output:result]` | A procedure output. | That procedure's Outputs table. |

These markers are references, not automatic substitution, execution, or authority.
Plain or inline-code rendering has the same meaning. Ordinary Markdown links,
regex character classes, data fields, and fenced examples retain their own syntax.
Do not replace bracketed text indiscriminately.

Input/output names use lower-case `snake_case`: a letter followed by letters or
digits, with single underscores separating nonempty words. Names are unique
within their input or output table; an input and output may share a name because
their namespaces differ. There is no rule-ID namespace.

Term names preserve their declared spelling and case, including meaningful spaces
or underscores. Names must be nonblank and contain no brackets, colons, or line
breaks. A namespace does not rename the underlying concept.

## Declarations and scope

Each input or output table's first cell declares its reference, for example
`[input:task]`. Uses elsewhere in that procedure resolve only to its own tables.
An external procedure file is one scope; the single inline procedure is another.
Main agent rules and procedure indexes have no input/output scope.

A procedure call explicitly identifies the source value or evidence and the
destination procedure's input name. Use a plain code name such as `task` for a
foreign destination; writing `[input:task]` denotes the current procedure's input.
Matching names across files never imply passing or inheritance.

Declare each external term mapping on one References bullet with one concept
Markdown link, for example:

```markdown
- [term:Activity] → [Activity concept](concepts/activity.md).
```

The concept link must resolve to an actual readable `concepts/` Markdown file
inside the workspace. Fragments may identify a section. Declare a term once per
References section. Agent-level mappings apply to that agent's procedures;
procedure-local additions are allowed. A procedure must not remap an inherited
name to another source. Identical repeated mappings are permitted but unnecessary.

Concept files declare their own concept through their title and Definition section.
Supporting terms use the declaration format in [concept_conv.md](concept_conv.md).
External terms identify their canonical concept sources in References.

## Verification boundary

The shared agent tools check local parameter declarations/uses and explicit term
mapping paths in their documented Markdown subset. They do not prove that prose
uses a concept correctly, that a mapped source defines the intended meaning, or
that a value passed to a procedure satisfies its semantic requirements. Those
checks remain part of authoring and execution review.
