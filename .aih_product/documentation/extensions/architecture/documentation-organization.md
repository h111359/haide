# Documentation organization

Document: D1. Type: architecture. Maintenance: AIH-managed extension. Status: specified; runtime implementation not established by this document.

## Product collection

`.aih_product/documentation/requirements.md`, `decisions.md`, and `context.md` are the product's entry points. They contain atomic findings and links to fuller documentation. `unresolved.md` preserves known unresolved matters; its presence never implies a resolution or prevents inspecting the settled baseline. A request touching an unresolved matter must retain that uncertainty.

`catalog.yaml` registers documents, stable identities, types, provenance, relationships, and navigation. Typed detail lives under `extensions/<type>/<subject>.<format>`, optionally subdivided by product area. Names use lowercase hyphenated words. Request IDs, dates, and entry numbers are not current-document filenames. Original attachments stay unchanged in their request-specific `attachments/` folder. Product documentation MUST NOT link to request attachments or other files within request folders. Before product integration references request evidence or detail, retain the needed material as an immutable product-owned copy under sources/ or the applicable typed extension location. A product file reference must resolve within this documentation collection or outside .aih_product/ as product-owned material. Preserve source identity/version through request ID, original filename, and digest without a request-file link. The migration preserves existing attachments at their current paths.

Each extension has one primary predefined type and one canonical location. Several entry files may refer to it without owning competing copies. The type registry is described by D3. Markdown, tables, declarative YAML/JSON, and inert diagram formats may be selected according to type. Executable code, operational scripts, and runnable tests remain outside `.aih_product/`.

The three entry files remain independently structured. Their file-local hierarchical numbers support review; changes to these numbers require reference repair. Document IDs such as D1 are stable within the collection and do not encode file location. Retired document IDs are never reused.

## Entry layer and extension navigation

The entry files, their tables of contents, referenced-document lists, and source lists are the entry layer. Their existing small-section rules apply: aim for 5–12 findings per group, reassess groups above 15, and use at most three topic-heading levels.

The existing eight-child, depth-balance, and 1,500-word rules apply to the logical extension-navigation tree, not to entry-file length, catalog metadata records, or physical type-directory counts. Every managed extension has one structural parent in that tree. Cross-links do not create additional structural parents. Meaningful navigation groups may span physical type directories; grouping by type remains the storage convention. A small root index and catalog branches support progressive loading. No empty padding, fabricated topics, cycles, duplicate identities, or orphaned extensions are allowed. A format that cannot be measured in words needs a type-appropriate size check; indivisible reference exceptions must be justified.

## Source evidence and document references

Each finding retains its independent wording, conditions, certainty, and source citations. Sources use file-local S aliases and exact locators. Document references use the shared D catalog: `Details: {D3:section "Types"}` or `Details: {D3}` when the whole document applies. D references do not establish source support or acceptance. `Accepted:` evidence stays separately labeled.

Each entry file includes a generated `Referenced documents` list containing exactly the documents used by its Details references, with IDs, linked titles, and types. The table of contents links to that list. The catalog records reciprocal entry links using filename and complete entry ID. Reorganization must update both directions and preserve document identity.

## Product and request ownership

A request is stored at `.aih_product/requests/<request-id>_<normalized-name>/`. Its location remains stable across active, blocked, completed, cancelled, and rejected states. Lifecycle metadata and the request catalog replace moves between active/history directories. Existing authorization and single-open-request rules remain applicable.

The request's generated change definition lives only in its `documentation/` subtree. `requirements.md`, `decisions.md`, `context.md`, `unresolved.md`, `catalog.yaml`, and any needed typed extensions form that definition. `analysis/interpretation.md`, if retained, is navigation to this definition rather than another editable source of requirements. Analysis, plans, questionnaire records, inputs, attachments, and execution evidence retain their own roles outside the generated subtree.

Request documentation is a change set against a recorded product baseline. It does not duplicate unchanged product findings or entire unchanged extensions. Product integration is a separate authorized operation. Request generation neither edits the product baseline nor implements the requested changes. The change and baseline contracts are specified in D2 and D4.

## External materials

A document outside `.aih_product/` may be registered as external, request-controlled material. Record its permitted root-qualified location, authority role, observed fingerprint, freshness, provenance, and related findings. A link never registers a root or expands permissions. If current access is unavailable, retain its last-known location and explicit uncertainty; do not claim verification.

Documentation maintenance may refresh AIH's own descriptions and references from permitted inspection. It must not modify an external material to synchronize it. Such modification requires an implementation task in an authorized request, with scope, current access, review, and verification equivalent to product-code changes. Internal backreferences avoid editing external files simply to add links.

## Product reference boundary

The boundary applies to source citations, Details links, extension references, catalog paths, backlinks, and evidence links. Resolve symlinks and final targets when checking it. Product documentation must not depend on request-folder files for reading or verification. Request IDs may identify provenance without becoming attachment paths. Requests may still reference the product baseline. An unchanged product-owned file outside .aih_product/ may be cited directly under its access rules.

## Maintenance

Update related findings, typed documents, catalogs, source aliases, and references together as authorized workflow work. Preserve human content, record source dependencies and versions, detect drift, and use revision-checked recoverable replacement. Read-only questions do not authorize maintenance. Changed external content may invalidate derived knowledge but never automatically grants permission to change that external content.

## Provenance

This contract implements the accepted documentation discussion in [documentation-evolution.md](../../sources/documentation-evolution.md), especially “Product knowledge and ownership”, “Accepted document organization and references”, “Migration and request-specific documentation”, and “Clarified request storage”. Original coverage and maintenance obligations remain recorded in the entry files and their cited build source.
