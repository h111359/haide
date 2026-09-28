# Request documentation update flow

Document: D4. Type: processing-flow. Status: specified; no runtime execution is asserted.

## Input and baseline

The reusable prompt remains at `definitions/definitions_R20260925_2309/attachments/update_documentation.md`. It takes complete source files, a request ID, and a request name. Its selected workspace determines `.aih_product/documentation/` and `.aih_product/requests/`; it does not accept an arbitrary output destination.

Read the complete submitted sources. Read the product entry files and catalog, then all relevant extensions and dependencies needed to compare meaning, scope, conditions, and acceptance. Do not classify an uninspected area as unchanged. Missing expected baseline files or unreadable supplied sources block generation. An entirely absent product baseline must be established through setup before this prompt runs; it does not infer an empty product, and an absent file in an existing baseline is an error.

## Compute the change set

Determine source precedence from explicit corrections and authority. Compare each eligible finding with the product baseline. Emit supported additions, modifications, and removals in their applicable categories, plus genuinely unresolved change questions. Record unchanged findings by baseline references in coverage metadata; do not repeat their statements. Relevant unchanged context is linked, with only the minimal qualification needed to understand a changed finding retained in its wording.

Requirements state what/why; decisions state chosen technical how; context states qualified background. Do not invent implementation choices during clarification. The generated collection becomes the canonical request definition. Analysis/plan artifacts remain separate, and any interpretation.md points to this collection rather than duplicating it.

## Typed detail and references

Create only needed typed extensions under the request's `documentation/extensions/`. Existing unchanged product details are registered as reference-only documents with explicit product D identities and baseline versions. Changed details contain only changed logical units, with target locators and operations. New details may be complete documents. External material remains unchanged; a requested modification to it is described for later authorized implementation.

The request catalog uses its own stable D namespace. Read prior request catalog identity records only to preserve document identity, retirement, and allocation. Recompute semantic content from the current supplied sources and product baseline; do not inherit omitted prior findings. Preserve prior applied generations and source evidence in existing request history before any permitted regeneration; closed requests are not regenerated as new work.

## Prepare and verify

Stage the four entry files, catalog, and necessary extensions as one candidate subtree. Organize each entry file independently, assign hierarchical IDs, rebuild references, source lists, referenced-document lists, and linked contents. Record the complete baseline/input fingerprints and source-to-delta coverage.

Independent review first inventories the complete sources and baseline without candidate access. It then compares the whole candidate collection for completeness of changes, truthfulness, unchanged exclusions, exact targets, typed-detail consistency, permission boundaries, and valid links. Every correction returns for review. An accurately recorded unresolved source issue can remain in the generated request, but prevents a readiness-to-integrate claim.

## Commit and subsequent integration

Recheck inputs, baseline, and request state. Replace only the generated `documentation/` subtree after validation and review. Preserve sibling inputs, attachments, analysis, plans, execution records, metadata, and lifecycle state. A generation operation neither opens a second request nor bypasses normal admission/ownership gates. Store request identity with the collection; the owning workflow maintains its catalog and lifecycle records.

Stale baselines require renewed comparison and review before integration. Integration applies the explicit delta to current product documentation, retaining unaffected findings and authoritative detail. It translates request D identities into product D identities, preserves history and provenance, and repairs all references. Before publishing product references, it copies needed request evidence into product sources/ and changed defining detail into the appropriate product extensions/. Product source citations and document references must resolve to those copies or to product-owned files outside .aih_product/, never to request-folder files. Original attachments stay unchanged; origin request IDs, filenames, and digests retain provenance without request attachment links. It does not treat request generation or documentation integration as implementation, test, deployment, or external-file-write authority. Repeating an already applied generation has no duplicate effect. The retained legacy merge_context.md attachment still describes the older flat/global-ID contract; it is historical material, not a compatible implementation of this integration flow. Updating that integration prompt is separate from generating request documentation.

## Provenance

Based on “Migration and request-specific documentation”, “Clarified request storage”, and “Implementation conventions derived from the accepted design” in [documentation-evolution.md](../../sources/documentation-evolution.md).
