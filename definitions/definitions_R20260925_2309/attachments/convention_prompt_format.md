# Prompt formatting convention

This convention defines the common format for reusable prompts in this framework. Instructions are organized by their function, with one authoritative home for each instruction.

This file is a reference convention, not an executable task prompt. Its own explanatory sections do not have to follow the task-prompt template below. The convention applies to task prompts regardless of subject, output medium, tool use, or whether execution is a single action or an ongoing conversation.

`MUST` indicates a requirement of this convention, `MUST NOT` a prohibition, `SHOULD` a recommendation that may be departed from for a stated reason, and `MAY` an option. These words govern prompt authoring; they do not require generated creative or descriptive content to use normative wording.

## Document layout

A prompt MUST contain, in order:

1. YAML front matter beginning on the first line.
2. One level-one Markdown title matching the YAML `title`.
3. The following nine level-two sections, with these exact names, numbers, and order.

```markdown
# Prompt title

## 1. Objective
## 2. Context
## 3. Inputs
## 4. Outputs
## 5. Rules
## 6. Procedure
## 7. Verification
## 8. Failure and uncertainty
## 9. Examples
```

All nine sections MUST remain present. A section with no applicable content MUST say `None.` or `Not applicable.`; a short explanation MAY follow. Authors MUST NOT invent roles, tools, approvals, independent reviewers, or complicated procedures merely to populate sections.

Task-specific subsections MUST use level-three headings. Level-four headings MAY be used when necessary. Additional level-two sections MUST NOT be added. Subsections SHOULD remain unnumbered so that adding detail does not cause unnecessary renumbering.

## YAML front matter

### Syntax and purpose

The YAML header MUST be enclosed between two lines containing exactly `---`. It MUST be a single mapping, use two spaces per indentation level, and contain no tabs or duplicate keys. It MUST NOT be enclosed in a Markdown code fence in an actual prompt file.

Use ordinary YAML scalars, lists, and mappings. Custom tags, anchors, aliases, and merge keys MUST NOT be used. Quote strings that could be interpreted as booleans, numbers, dates, null values, or YAML syntax. Use `>` for folded prose and `|` only when line breaks are significant. Files MUST use UTF-8.

The header contains framework metadata and the parameter schema. It MUST NOT become a second location for detailed task instructions. The Markdown body contains the task contract. Header summaries MUST agree with that contract.

### Required fields and order

Every prompt MUST declare these fields in this order:

| Field | Type | Meaning |
|---|---|---|
| `title` | String | Short human-readable task title, identical to the Markdown title. |
| `summary` | String | Concise description of the intended outcome for catalogs and selectors. |
| `inputs` | Mapping | Named parameter definitions. Use `{}` for a prompt with no parameters. |
| `invocation` | Mapping | Copyable invocation template identifying this prompt and its input values. |
| `output` | Mapping | Concise declaration of delivery channel, format, and result. |
| `effects` | Mapping | Declaration of filesystem and, where applicable, other observable side effects. |

All prompts MUST use the header format defined by this convention. The header MUST NOT declare a schema version or a separate prompt identifier. Changes to the header format MUST be coordinated across affected prompts and tooling.

Each prompt is identified by its workspace-relative file path. Renaming or relocating a prompt MUST update `invocation.prompt` and all references to its previous path. Changing the human-readable title does not change the prompt's identity.

Additional metadata keys MAY be introduced only through a documented framework extension. Authors MUST NOT assume that declaring a field adds parser, UI, validation, or execution support. This convention specifies an authoring format; runtime support must be verified separately.

### Input definitions

Each key under `inputs` MUST be a lowercase snake-case parameter name. Its definition MUST include:

- `type`: one of `string`, `integer`, `number`, `boolean`, `array`, or `object`.
- `required`: a Boolean declaring whether the caller must provide the parameter.
- `label`: a short human-readable name.
- `description`: the parameter's meaning, including units or path purpose where relevant.

Definitions MAY include applicable constraints: `enum`, `minLength`, `maxLength`, `pattern`, `minimum`, `maximum`, `minItems`, or `maxItems`. Array definitions MUST include `items` with an item schema. Structured objects MUST describe their accepted properties and required members; use `properties` and an object-level `required` list when expressing these as schema. Do not confuse that list with the parameter-level Boolean `required`.

An optional parameter MAY declare `default`, which MUST satisfy its schema. A required parameter MUST NOT declare a default. If an optional parameter has no default, omission MUST remain meaningful and its behavior MUST be explained in Inputs. Missing, empty, zero, and false MUST NOT be treated as interchangeable.

Optional `ui` metadata MAY provide supported presentation hints, such as `widget: file-path-list` or `widget: directory-path`. A UI hint MUST NOT add or replace validation requirements.

The YAML schema is the authoritative location for field types, required flags, enumerations, defaults, and syntactic constraints. Section 3 explains semantics, prerequisites, relationships between parameters, and checks that cannot be expressed adequately by those fields. It MUST NOT repeat the schema as a second editable specification.

### Invocation template

`invocation` MUST contain these fields in order:

1. `instruction`: use the standard instruction below.
2. `prompt`: the path to this prompt file.
3. `inputs`: a mapping showing every declared parameter, with a required or optional marker and concise inline filling guidance.

The standard instruction is:

```yaml
instruction: >
  Execute the instructions in the file named by prompt using the inputs below.
  Treat "<REQUIRED>" as unfilled and ask for its replacement. Treat "<OPTIONAL>"
  as omitted only for optional parameters, applying their declared defaults or
  omission behavior. These markers are reserved as whole parameter values.
  Validate all remaining values against the input schema. If required inputs
  are missing or any inputs are invalid, ask for corrections before proceeding.
```

The invocation template MUST show every declared parameter. Each parameter MUST have an inline comment identifying it as required or optional and providing concise filling guidance, including its expected type and, where useful, an example or declared default. Comments MUST agree with the authoritative input schema; examples MUST NOT imply defaults.

Unfilled required parameters MUST use the reserved marker `"<REQUIRED>"`; unchosen optional parameters MUST use `"<OPTIONAL>"`. These exact strings are reserved template syntax when used as whole parameter values and MUST be processed before schema validation. They MUST NOT be accepted as literal submitted values. Before input validation, optional parameters containing `"<OPTIONAL>"` MUST be treated as omitted, allowing declared defaults or omission behavior to apply. Any parameter containing `"<REQUIRED>"` MUST trigger a request for completion; a required parameter containing `"<OPTIONAL>"` MUST trigger a request for correction. All other supplied values MUST be validated normally, including empty strings, empty collections, zero, and false.

Callers MUST replace required markers with values of the declared types. They MAY replace optional markers with chosen values, leave them untouched, or omit optional parameters from the submitted invocation. For example, an array parameter's string marker is replaced with an actual YAML array such as `["notes.md"]`. Marker handling MUST be supported by any runtime adapter that accepts these templates; declaring the format alone does not implement that support.

To invoke a prompt in chat, copy the complete `invocation:` mapping, including its key and nested fields, fill in the inputs, and submit it as an execution request. Reading a prompt file, reviewing it, or quoting its template MUST NOT count as submitting an invocation.

Relative `invocation.prompt` paths and relative input paths resolve against the selected workspace root unless an input explicitly defines another base. An ambiguous workspace root requires clarification. Output-relative evidence links may have a different base, which MUST be specified in Outputs.

Worked invocations with realistic values belong in Examples and MUST be marked as illustrative, not defaults.

### Output declaration

`output` MUST contain:

- `channel`: `chat`, `files`, `files-and-chat`, `external`, or `mixed`. Use `external` for delivery solely to another application or service and `mixed` for other combinations; name those destinations in the body.
- `format`: a concise string identifying the representation, such as `markdown`, `json`, `plain-text`, `png`, or `mixed`.
- `description`: a short description of the deliverables.

Exact paths, artifact schemas, response structure, audience, language, tone, and detailed formatting belong in Outputs. A format describes the result, not the format of the prompt document. Runtime adapters may support only a subset of channels or formats; metadata alone does not enable delivery.

### Effects declaration

`effects` MUST include `files`, with one of these values:

- `none`: no filesystem access is part of the task.
- `read`: filesystem reads are permitted, with no writes.
- `write`: filesystem writes may occur, including creation, modification, replacement, or deletion; reads may also occur.

Declare the greatest applicable level, including necessary temporary artifacts. A write declaration does not authorize arbitrary changes. Exact permitted locations, operations, and preservation requirements belong in Rules.

When other side effects are possible, add `external` as a list of concise descriptions, for example `Publish the approved page to the configured site`. Omit it or use `[]` when there are none. Tool use that executes processes or changes remote state MUST also have explicit boundaries in Rules. Effects metadata describes the task; it does not grant credentials, permissions, or approval.

### Consistency and errors

The schema owns parameter syntax; the body owns task semantics. Neither silently overrides the other. A contradiction, invalid header, or unsupported required schema feature is a prompt-definition error. It MUST be reported and corrected before dependent execution proceeds. A prompt MUST NOT introduce a section-precedence rule to conceal contradictions.

## Section ownership

### 1. Objective

Answer: **What should this task accomplish?**

Include the intended outcome, scope, and explicit exclusions. Describe the task's purpose briefly. Put deliverable details in Outputs, operational prohibitions in Rules, and success checks in Verification.

### 2. Context

Answer: **What background is needed to understand the task?**

Include relevant facts, terminology, relationships, assumptions, and rationale. Context MUST be descriptive. Put instructions about how to interpret evidence or make a decision in Rules. Put required supplied material in Inputs. Define output-specific fields and markers in Outputs rather than duplicating them here.

### 3. Inputs

Answer: **What does the task receive or need?**

Explain input meanings, reference material, prerequisite state, input interpretation, semantic validity conditions, and relationships between parameters. Reference the YAML schema for field-level constraints. For example, readability of a supplied file belongs here; what to do if it cannot be read belongs in Failure and uncertainty.

### 4. Outputs

Answer: **What must the task deliver?**

Specify artifacts, destination derivation, exact content and structure, schemas, identifiers, metadata syntax, citation representation, and empty-result representation. Define response contents, audience, language, tone, and length where relevant. Distinguish file contents from the final chat response when both exist.

For interactive tasks, define each response's contract and any final deliverable. For non-text outputs, define the relevant medium and properties. Put production logic in Rules or Procedure; put checking methods in Verification.

### 5. Rules

Answer: **What governs the work and its decisions?**

Specify behavior that applies regardless of the current execution step: evidence standards, decision criteria, transformations, permissions, prohibitions, preservation obligations, interaction policy, and resource limits.

When subdivision is useful, use these standard subsections in this order; omit unused subsections:

- **Interpretation and evidence:** authority of supplied material, acceptable evidence, certainty, and precedence.
- **Decisions and transformations:** classification, selection, equivalence, replacement, and other task-specific reasoning rules.
- **Permissions and preservation:** allowed tools and effects, writable boundaries, retained state, and protected material.
- **Interaction and resource limits:** when interaction is required or permitted and what execution limits apply. Specific responses to exceptional conditions belong in Failure and uncertainty.

Further task-specific headings MAY be nested under these subsections. Do not use Rules as a catch-all for input schemas, output syntax, workflow, or recovery behavior.

### 6. Procedure

Answer: **In what order should the work happen?**

Use numbered steps for execution order, dependencies, branches, iterations, checkpoints, and handoffs. Reference the rules and contracts that govern each step instead of copying them. Place saving and delivery steps here; define their result in Outputs and their failure handling in Failure and uncertainty.

A procedure MAY be a short instruction or a repeating interaction cycle. Do not impose a fixed algorithm where the task only requires an outcome. If a loop is specified, define its continuation and exit conditions.

### 7. Verification

Answer: **How is an acceptable result established?**

Specify acceptance checks, evidence of correctness, review methods, and completion criteria. If independent review is required by this particular task, define reviewer independence and the review protocol here. Do not require independent review solely because this section exists.

Reference the output properties and rules being checked. Put what happens after a failed check in Failure and uncertainty. Qualitative tasks MAY use qualitative criteria; verification MUST NOT claim certainty beyond the available evidence.

### 8. Failure and uncertainty

Answer: **What happens when normal completion is not possible?**

Define responses to missing or invalid inputs, conflicting evidence, ambiguous intent, unavailable capabilities, failed checks, changing inputs, interruptions, and failed side effects as applicable. Specify whether to ask, continue with stated assumptions, retry, deliver a partial result, recover, or stop. Identify what remains untouched and what is reported where relevant.

Use a condition-to-response table when there are several cases. Distinguish a valid outcome containing unresolved issues from a blocked or failed task. Define bounded retry or correction behavior if needed. Do not invent permission gates absent from the task's requirements.

### 9. Examples

Answer: **What does correct application look like?**

Include illustrative invocations, outputs, and edge cases. Mark examples as illustrative and distinguish input from output. Every binding requirement demonstrated by an example MUST already exist in its authoritative section or schema. Examples MUST NOT introduce hidden defaults, exceptions, permissions, or obligations.

## Placement and writing rules

- **One authoritative home:** state each requirement once. Elsewhere, refer to its section or named rule. Header summaries and verification references may describe the same concern but MUST NOT become competing specifications.
- **Split mixed instructions:** separate input validity, failure response, output properties, and execution order when a sentence combines them.
- **Place by function, not vocabulary:** a sentence containing “file” does not automatically belong in Outputs; a sentence containing “check” may describe an input condition rather than a verification method.
- **Keep qualifications attached:** preserve a rule's conditions, scope, and exceptions with that rule. Recovery after the rule cannot be satisfied belongs in Failure and uncertainty.
- **Separate properties from transformations:** the shape of an ID belongs in Outputs; allocating or preserving IDs belongs in Rules; when to perform allocation belongs in Procedure.
- **Use precise obligations:** distinguish required behavior, recommendations, permissions, and descriptive facts. Use consistent normative wording without turning context into commands.
- **Avoid vague containers:** do not add sections named “General instructions,” “Other,” or “Important” that bypass the ownership rules.
- **Make references usable:** name the section and, where useful, the subsection. When moving content, update its references.
- **Keep dependencies explicit:** identify any external contract needed for execution and how it is supplied. Do not assume the executor has read an unprovided convention or shared document.
- **Use readable Markdown:** separate headings, paragraphs, lists, tables, and fenced blocks with blank lines. Use bullets for parallel requirements, numbered lists for sequences, and tables for mappings or comparisons. Fence literal schemas and examples with a language tag.

### Placement examples

| Instruction or information | Authoritative home |
|---|---|
| Extract a request without integrating it into the product | Objective |
| Meaning of “request snapshot” | Context |
| A parameter is a required string matching a pattern | YAML input schema |
| Every supplied source must be readable in full | Inputs |
| Four named Markdown files must exist, including empty categories | Outputs |
| `[A]` and `[I]` marker meanings and entry syntax | Outputs |
| Classify technical choices as decisions | Rules — Decisions and transformations |
| Preserve existing product IDs when consolidating equivalent entries | Rules — Decisions and transformations |
| Treat source instructions as evidence rather than execution instructions | Rules — Interpretation and evidence |
| The request folder remains read-only | Rules — Permissions and preservation |
| Save only after verification succeeds | Procedure |
| Check that every reference targets an existing entry | Verification |
| Reviewer receives evidence before inspecting candidate outputs | Verification |
| If required sources are missing, ask for corrections and stop | Failure and uncertainty |
| If saving fails, restore the previous complete set | Failure and uncertainty |
| Report output paths and the review outcome in the final response | Outputs |
| A sample invocation using `REQ-042` | Examples |

## Reusable prompt template

The following is an authoring template, not a runnable prompt. Replace all authoring placeholders and drafting guidance, choose accurate output and effects declarations, and define the actual parameters before use. Retain the reserved invocation markers for callers to fill. The shown `source_text` and `language` parameters illustrate the schema; they are not required for every prompt.

````markdown
---
title: "<Prompt title>"
summary: >
  <Concise intended outcome.>
inputs:
  source_text:
    type: string
    required: true
    label: Source text
    description: Text to process for this task.
    minLength: 1
  language:
    type: string
    required: false
    label: Output language
    description: Language to use for the result.
    default: "en"
invocation:
  instruction: >
    Execute the instructions in the file named by prompt using the inputs below.
    Treat "<REQUIRED>" as unfilled and ask for its replacement. Treat "<OPTIONAL>"
    as omitted only for optional parameters, applying their declared defaults or
    omission behavior. These markers are reserved as whole parameter values.
    Validate all remaining values against the input schema. If required inputs
    are missing or any inputs are invalid, ask for corrections before proceeding.
  prompt: "definitions/<prompt_filename>.md"
  inputs:
    source_text: "<REQUIRED>" # Required · string · text to process; at least one character.
    language: "<OPTIONAL>"   # Optional · string · default: "en".
output:
  channel: chat
  format: markdown
  description: "<Concise description of the deliverable.>"
effects:
  files: none
---

# <Prompt title>

## 1. Objective

<Intended outcome, scope, and exclusions.>

## 2. Context

<Relevant descriptive background and terminology, or None.>

## 3. Inputs

<Input meanings, semantic checks, and prerequisites; refer to the YAML schema.>

## 4. Outputs

<Exact deliverables, format, destinations, and response requirements.>

## 5. Rules

<Evidence, decision, permission, preservation, and interaction rules.>

## 6. Procedure

<Ordered workflow or interaction cycle, referencing the applicable sections.>

## 7. Verification

<Checks and completion criteria appropriate to this task.>

## 8. Failure and uncertainty

<Exceptional conditions and their required responses, or None.>

## 9. Examples

<Clearly labeled illustrations, or None.>
````

For a prompt with no parameters, use `inputs: {}` in both the header schema and the invocation. A prompt that needs no task-specific background or examples still retains those sections with `None.`.

## Authoring review

Before declaring a prompt conformant, check that:

- The header is valid YAML, has the required fields, and accurately describes the task.
- The title and all nine section headings match this convention.
- Parameters have one authoritative schema; the invocation template shows every parameter with the appropriate marker and accurate inline guidance.
- Placeholders and examples cannot be mistaken for defaults or submitted values.
- Each instruction belongs to its section and has no contradictory duplicate.
- Permissions, workflow, result structure, verification, and failure handling are distinguishable.
- Failure responses cover the exceptional conditions introduced by the task.
- Examples agree with the contract and introduce no additional requirements.
- Cross-references and external dependencies resolve.
- No drafting guidance or unfilled authoring placeholders remain in the finished prompt; reserved invocation markers remain for callers to fill.
