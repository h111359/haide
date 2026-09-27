---
schema_version: 1
id: merge_context
title: Merge request definitions into product definitions
summary: >
  Integrate a verified request definition folder into unified product
  definitions, preserving history and resolving conflicts before saving.
inputs:
  request_folder:
    type: string
    required: true
    minLength: 1
    label: Request definitions folder
    description: Path to the verified definitions_<request_id> folder containing all four extraction files.
    ui:
      widget: directory-path
  product_folder:
    type: string
    required: true
    minLength: 1
    label: Product definitions folder
    description: Destination folder for the three unified product definition files.
    ui:
      widget: directory-path
invocation:
  instruction: >
    Execute the instructions in the file named by prompt using the user-filled
    inputs below. If required inputs are missing or invalid, ask for corrections
    before proceeding.
  prompt: definitions/merge_context.md
  inputs:
    request_folder: ""  # Required.
    product_folder: ""  # Required.
output:
  channel: files-and-chat
  format: markdown
  description: Three unified product definition files and a merge result or blockers in chat.
effects:
  files: write
---

# Merge request definitions into unified product definitions

Integrate one verified request definition folder into the unified product
definitions. You MUST preserve product history and reconcile meaning, not merely
concatenate files. Request extraction and replacement belong to `extract_context.md`.

## Required inputs

The YAML header's `inputs` defines the authoritative field schema; the body defines execution and evidence checks. To invoke this prompt in chat, copy the entire `invocation:` block, including the `invocation:` line and all its nested fields, stopping before `output:`. Keep its indentation exactly as shown, fill in the values under `invocation.inputs`, and paste the block into chat. The included `instruction` explicitly asks the agent to execute the referenced prompt using those inputs. No additional sentence or reformatting is needed. The header itself is a reusable template; its presence in a file does not submit an invocation. Empty required template values are placeholders, not defaults or valid submissions. The `prompt` path selects the instructions to follow. Resolve relative invocation paths against the selected workspace root; if that root is ambiguous, ask for clarification. Source citations retain their separately defined path rules. If the header and body contradict each other, report the prompt-definition error and stop.

Both parameters MUST be explicitly provided:

- `request_folder`: the path of a generated `definitions_<request_id>` folder.
- `product_folder`: the destination folder for unified product definitions.

If either is missing, invalid, or ambiguous, you MUST ask for the needed values
and stop before writing. You MUST NOT choose defaults or infer paths from the
workspace. Example invocation; these values are illustrative, not defaults:

```yaml
invocation:
  instruction: >
    Execute the instructions in the file named by prompt using the user-filled
    inputs below. If required inputs are missing or invalid, ask for corrections
    before proceeding.
  prompt: definitions/merge_context.md
  inputs:
    request_folder: review/extracted/definitions_REQ-042
    product_folder: review/product_definitions
```

You MUST derive `request_id` from the request folder's `definitions_` name
component, retaining the complete identifier after that initial component.
The extracted identifier MUST match `[A-Za-z0-9][A-Za-z0-9_-]*`.
If the folder name does not unambiguously identify the request, you MUST ask
for correction rather than invent provenance.

The request folder MUST contain these four readable files:

- `requirements.md`
- `decisions.md`
- `context.md`
- `unresolved.md`

You MUST read all four completely. They MUST follow the extraction contract:
atomic entries, plain numeric IDs unique across the request snapshot, detailed
source evidence, and valid references. Empty category files are allowed.

If `unresolved.md` contains any unresolved issue, you MUST report the blockers
and leave the product folder unchanged. You MUST NOT merge only the convenient
alternatives or label the request fully merged. The requester must resolve
the issues and regenerate the request definitions before integration.

Resolve both paths and symlinks. The request and product folders MUST be distinct
and neither may contain the other. You MUST NOT overwrite inputs or either
prompt. The request folder is read-only throughout this operation.

## Product outputs and provenance

You MUST create or update exactly these files directly in `product_folder`:

- `requirements.md`
- `decisions.md`
- `context.md`

All three MUST exist after a successful merge; an empty category has an empty
file. You MUST NOT create `unresolved.md` in the product folder. Merge conflicts
MUST be reported in the response and resolved before saving product changes.
You MUST NOT modify the request's `unresolved.md`, source files, another request,
or unrelated product-folder files. This prompt does not implement the product.

If product definitions do not exist, initialize the three-file set from the
request after validation and independent review. If they exist, read all three
completely and retain an unchanged pre-merge snapshot for comparison and recovery.
A partially missing or incompatible existing set MUST be reported for clarification
rather than silently reconstructed or migrated.

In unified entries, `Source:` MUST contain only contributing request IDs, such
as `REQ-042` or `REQ-011, REQ-042`. It MUST NOT contain original filenames, line
numbers, page locators, temporary paths, or request-local entry numbers. Detailed
evidence remains in the request definition files.

When equivalent entries are contributed by several requests, you MUST keep one
entry per applicable category and add all supporting request IDs without duplicates.
When a decision is replaced, the historical entry MUST retain its existing
source IDs; the replacement MUST cite its actual contributing request IDs.
Preserved portions MUST cite both the original contributing requests and the
request establishing the changed scope. You MUST NOT attribute unaffected
product entries to the incoming request merely because they were read during merging.

## Categories and explicit wording

You MUST maintain the same classification as extraction:

- `requirements.md`: requester-facing what and why, business rules, observable
  capabilities, workflows, outcomes, acceptance criteria, and externally required
  qualities. Technical implementation details MUST NOT be introduced.
- `decisions.md`: selected technical how, including architecture, technologies,
  algorithms, internal interfaces and data structures, deployment, and technical
  verification approaches. Business objectives MUST NOT substitute for a
  technical choice.
- `context.md`: relevant descriptive domain facts, existing conditions, terminology,
  relationships, reported assumptions, and uncertainties that affect the work
  without prescribing a requirement or selecting a solution.

Every finding that genuinely belongs to multiple categories MUST appear in all
of them. You MUST preserve each category-appropriate representation, using distinct
IDs and `Related:` links where useful. Within a category, semantic duplicates
MUST be consolidated. Cross-category presence is not itself a duplicate to remove.
You MUST NOT invent an additional aspect to force a finding into more categories.

Normative entries MUST use the exact uppercase words `MUST`, `MUST NOT`, or
`OPTIONAL`, with the same force supported by the request: obligation, prohibition,
or deliberate permission respectively. You MUST NOT promote a suggestion to an
approved option or change its strength during merging. Descriptive context MUST
remain factual and preserve reported/assumed/uncertain qualifications; you MUST
NOT fabricate an imperative to make a fact resemble a requirement.

## Identity and references

Product entry IDs MUST be plain positive integers in one sequence across all
three product files. They MUST be unique across the set. Existing product IDs
MUST remain stable, including inactive IDs. New entries MUST receive the next
unused numbers after the highest existing product ID. A new product starts at `1`.

Request-local numbers MUST NOT be copied as product identities. During staging
you MUST construct a mapping from each incoming request entry to its resulting
product entry or entries, including equivalents already present and cross-listed
representations. You MUST use it to translate all `Supports:`, `Context:`, and
`Related:` references. A numeric match alone is not an identity match.

You MUST preserve product `Replaces:`, `Replaced by:`, and `Preserves:` history.
All references in final product files MUST point to real product entries, not
request-local IDs. `Supports:` MUST target requirements, and `Context:` MUST
target context. Cross-listing links MUST remain consistent after updates.

The staging map and detailed review evidence MUST NOT be added to product entries
or hidden comments. Product provenance is expressed through request IDs only.

## Merge semantics

An incoming request is evidence of a proposed integration, not automatic authority
to overwrite every conflicting product statement. You MUST compare meaning,
scope, conditions, modality, and evidence across all three categories.

1. **New independent finding:** append an `[A]` entry in every applicable category.
2. **Equivalent finding:** retain the existing product entry and its ID; add the
   incoming request ID to its sources only when it actually supports that finding.
3. **Explicit complete replacement:** when the request establishes supersession
   of the same scope, retain the old statement as `[I]`, append the replacement
   as `[A]`, and record reciprocal replacement links.
4. **Partial replacement:** mark the entire old entry `[I]`. Add atomic `[A]`
   entries for both the changed portion and every surviving portion. Preserved
   entries MUST carry `Preserves:` and `Replaces:` links and the correct source
   request IDs. You MUST NOT silently shorten the historical statement.
5. **Explicit withdrawal:** retain the old entry as `[I]` and record the supported
   withdrawal in the appropriate category, with its source request and links.
   You MUST NOT invent replacement behavior.
6. **Reinstatement:** create a new active product entry; you MUST NOT reactivate
   or renumber an old inactive entry.
7. **Unclear conflict:** stop before changing product files, report the competing
   product and request entries, and ask for resolution. You MUST NOT select a
   winner based on merge order, request-name sorting, timestamps, or file order.

You MUST preserve compatible findings for different scopes, time periods, or
environments. A more recent contextual observation supersedes an older one only
when the evidence establishes a correction or change of the same applicable
fact. Context changes MUST NOT silently authorize new technical designs or
new business requirements.

Cross-listed representations and dependencies MUST be reviewed together. If a
change affects a requirement, solution, or context entry in another category,
you MUST reconcile the affected aspect when supported. You MUST NOT invent a
redesign, automatically invalidate a need because its implementation changed,
or leave contradictory active representations. Unsettled consequences MUST be
reported as merge blockers.

`[A]` means applicable to the current product definition; `[I]` means superseded
by supported integration history. These markers do not establish implementation
or test completion. Completion alone MUST NOT invalidate a definition entry.

## Regenerated requests and repeat merges

Request extraction replaces its folder and may renumber local entries. You MUST
match contributions by meaning, category, evidence, and relationships, not just
the incoming numeric IDs. A repeated merge of identical content MUST leave the
product files unchanged, without duplicate entries, source IDs, or events.

If the same request ID already contributed to the product, changed incoming
content MUST NOT silently erase or rewrite its earlier contributions. You MUST
require clear evidence of a correction, removal, or scope change before replacing
a product entry. Omitting an entry from a regenerated request is not evidence
that the product requirement was withdrawn. If the revision's intent cannot be
established, ask and leave the product files unchanged.

Product entries absent from the incoming request MUST be preserved unless that
request explicitly supersedes them. Existing source request IDs MUST NOT be
discarded from unaffected or historical entries.

## Exact unified format

Files MUST contain only atomic entries and concise metadata, with no titles,
headings, summaries, diagnostics, review notes, timestamps, or hidden comments.
For example:

```markdown
- [I] 17. Users MUST retain reports for 30 days.
  Source: REQ-011. Replaced by: 24.

- [A] 24. Users MUST retain reports for 90 days.
  Source: REQ-042. Replaces: 17.
```

`Source:` MUST list request IDs only. Other allowed metadata is `Replaces:`,
`Replaced by:`, `Preserves:`, `Supports:`, `Context:`, and `Related:`. These
relationships MUST use product IDs. Acceptance locators and detailed source
evidence MUST remain in the original request files, not unified entries.

## Independent verification and save

You MUST stage the complete candidate product set without modifying the existing
product files. You MUST arrange an independent reviewer in a separate agent
or fresh session. In the first phase, the reviewer MUST receive only the complete
incoming request folder, the unmodified product baseline, and this contract.
They MUST independently inventory incoming findings and baseline obligations
before inspecting the candidate outputs. Only then may the candidates be supplied
for comparison. The reviewer MUST NOT receive the merging agent's reasoning or
assertions of correctness. They MUST verify source-to-output completeness and
output-to-source truthfulness: every incoming settled finding is represented in every applicable
category, every product addition or modification is supported by the request,
and every retained or replaced baseline obligation is correctly accounted for.

The reviewer MUST check normative strength, factual certainty, unresolved issues,
cross-category consistency, correct equivalence and precedence, partial-replacement
survivors, history, ID stability, translated references, and request-ID-only
provenance. Sources for this verification are the complete request definitions
and the pre-merge product baseline. Detailed locators in the request preserve
traceability to the original material; the reviewer MUST NOT infer missing evidence.

All mistakes and omissions MUST be fixed before completion. Corrections MUST
return to the independent reviewer for checking against the affected sources
and confirmation of overall consistency and completeness. A self-review by
the merging agent MUST NOT be presented as independent verification.
If an independent reviewer is unavailable, or a substantive conflict remains,
you MUST report the blocker and leave the product files unchanged.

Product integration MUST be serialized. Before saving, you MUST verify that
neither the request nor the baseline changed during staging and review. If
either changed, reread and repeat the affected merge and independent verification;
you MUST NOT overwrite concurrent work. Only a verified complete set may be
saved. A failed save MUST restore the previous product set; it MUST NOT
leave partially updated cross-file references.

In the response only, report the request ID, three output paths, independent
verification outcome, and changes or blockers. You MUST NOT create a product
`unresolved.md`, edit the request folder, or claim success for a blocked merge.
