## Formats

### Concept file

```
# <concept name>

## Definition

<definition explanation in free text>

## Purpose

<purpose explanation in free text>

## Supporting Terms

<purpose explanation in bulet list of supporting term elements>

## References

<reference explanation in bulet list of reference elements>

```

### Supporting term list element

```
- [term:<name>]: explanation in free text in single line
```

### Reference list element

```
- <relative path to another file>: explanation in free text
```

### Term format

Use `[term:name]` for a concept or supporting-term reference, following
[reference-notation_conv.md](reference-notation_conv.md). Preserve the concept's
identity and spelling; adding the namespace does not rename it. A Supporting
Terms list element declares that supporting term in its owning concept file.
External term references identify their canonical concept sources in References.
Ordinary Markdown links, code fields, and regex brackets retain their syntax.
The concept template remains unchanged; existing Explanation sections and useful
subsections are permitted. Concepts explain meaning and rationale, not executable
workflows. Shared behavioral obligations belong to the owning agent's `SKILL.md`;
procedure-specific obligations and ordered steps belong to its procedure files.
Data formats/contracts belong to conventions. See the
[Procedure concept](../concepts/procedure.md) for the distinction between
prerequisites, rules, and steps.
Plain explanatory prose follows [instruction-writing_conv.md](instruction-writing_conv.md).
Concept explanations are not forced into MUST/MUST NOT/MAY rules; necessary
technical terms retain their precise meaning and supporting references.
