# Documentation catalog contract

Document: D2. Type: interface-contract. Status: specified; this contract does not claim an implemented validator.

## Collection identity

`catalog.yaml` is validated inert data. `format_version: 1` identifies this catalog contract, not the reusable prompt header format. `collection` identifies `kind: product` or `kind: request`, product identity, and collection status. A request collection also records its exact request ID, supplied display name, normalized slug, stable request-folder path, and generation identity. Directory names alone do not supply missing identity or authorization.

For a new request, trim the request ID and preserve its case. IDs must match `[A-Za-z0-9][A-Za-z0-9_-]*`, be safe folder components, and be unique without relying on case differences. Normalize the required name using Unicode NFKD, remove combining marks, convert to lowercase, replace each run outside ASCII letters/digits with one hyphen, and trim leading/trailing hyphens. Reject an empty result and unsafe or platform-invalid resulting components. Do not silently invent a name. Example: `REQ-042` and `Customer API Update` yield `REQ-042_customer-api-update`.

On regeneration, find the existing request by its stored exact ID before creating directories. Reject case-only IDs, collisions, competing folders for one ID, and a different normalized name for an existing request unless an explicit metadata migration has been authorized. Preserve its folder across lifecycle changes; a name edit never silently creates a second request.

## Document registry

`documents` contains one record per registered D identity, including retired identities. Each active record contains:

| Field | Meaning |
|---|---|
| `id` | Stable `D` plus positive integer, unique within this collection |
| `title`, `type`, `format` | Human title, predefined primary type, actual format |
| `maintenance` | `aih-managed`, `external-request-controlled`, or `product-reference` in a request |
| `path` | Relative to this catalog for local material; absent for unresolved locations |
| `workspace_ref` | Root ID and root-relative path for external material |
| `authority` | `defining-detail`, `supporting-reference`, or `illustrative` |
| `status`, `freshness` | Specified/observed/uncertain/retired and inspection freshness, separately from implementation or acceptance |
| `fingerprint` | Observed content hash, or explicit unavailable status |
| `provenance` | Source path and exact locator records, with source role |
| `related_entries` | Filename and complete hierarchical ID for every reciprocal entry relationship |
| `product_document_id` | For request references/changes to existing product detail, the product D identity |
| `baseline_locator` | Precise existing section, field, operation, entity, or document being changed |
| `representation` | `complete-document`, `changed-fragment`, or `reference-only` |

Catalog paths resolve from the final catalog location. In product collections, every referenced file must resolve within product documentation or outside .aih_product/; request-folder targets are prohibited, including evidence links and symlink aliases. Promote required request evidence into immutable product sources/ copies before integration. Record origin request IDs, filenames, and digests without retaining a resolvable request-file dependency. Fingerprints describe observed bytes; they do not establish semantic truth. Renaming preserves D identity. Retiring records preserves history and prevents ID reuse. `next_document_id` allocates above every previously assigned number. Request D identities are local to the request catalog, not implicitly equal to the same D number in the product catalog. `product_document_id` explicitly maps them. Reading an older request catalog to preserve D identities must never carry forward unsupported old findings.

## Citation and backlink contract

Entry evidence remains an indented brace block such as `{S1:L10, S1:L25, S2:L3-6}`. Source aliases are defined per entry file. Extensions carry equivalent source identity, locators, and evidential status in the catalog or format-native metadata; no custom fields are forced into a standard artifact format.

`Details: {D3:field "customer_id", D8:operation "createCustomer"}` references typed detail. Repeat the D ID for each locator. Prefer semantic locators; preserve quoted text intact. `{D3}` means the entire document applies. Generate each entry file's `Referenced documents` list from its actual Details usage. Entries and the catalog must agree in both directions; non-entry extension dependencies use separate `related_documents` links.

## Baseline and change operations

A request catalog records `baseline.path`, whether the baseline was explicitly empty, and fingerprints for all compared entry files, catalogs, and relevant extension/reference material. It also records the relevant product revision or workspace mapping when available. A missing expected baseline is an error, not an empty product. Numeric entry targets are meaningful only with their filename and recorded baseline fingerprint.

Each settled request finding has `Change: add`, `Change: modify`, or `Change: remove`. Modification and removal also carry `Target: product:requirements.md, entry 2.1.1` (with the appropriate file); additions have no fictitious old target. Multiple affected targets are explicit. A cross-category change remains represented in each affected category. Removal requires source-supported withdrawal; omission from a request is never deletion authority.

`changes` records each finding reference, operation, baseline targets, and related document changes. Extension changes identify local D ID, product D ID if any, action, affected locator, representation, and any expected prior fingerprint. Store only new/changed content; use changed fragments for partial structured changes and retain format/scope metadata sufficient for validation and integration. Unchanged scaffolding necessary for format parsing is not a copy of unchanged product knowledge and must be minimal and identified. Do not reproduce a whole existing artifact merely to change one field.

`coverage` accounts for every eligible source finding as `add`, `modify`, `remove`, `unchanged`, `unresolved`, or `excluded`, with source locator and output/target references or a concise exclusion reason. Unchanged coverage records contain references, not duplicate statements. This makes delta completeness reviewable without inflating the entry files. `unresolved` records point to unresolved.md entries and affected baseline targets without selecting an alternative.

## Navigation and applicability

`type_registry` references the governing type convention. `navigation` is a logical tree with a small root and managed-extension leaves; catalog records are not themselves content leaves. Each managed extension has one parent. External references are cross-links, not copied leaf documents. Large registries may use validated catalog branches that retain the same collection namespace. `applicability` records applicable, not-applicable-with-reason, or unknown classifications without generating empty documents.

## Validation and update integrity

Validate identities, required fields, type/format compatibility, all paths and locators, evidence, reciprocal links, baseline fingerprints, and change coverage. Reject dangling D IDs, duplicate canonical material, executable content in product state, and references that imply expanded authority. Stale or missing evidence remains explicit. Verify the complete collection before a revision-checked recoverable replacement; never expose a partially updated catalog and entry set to supported readers.

## Provenance

Derived from the accepted design and request-storage choices in [documentation-evolution.md](../../sources/documentation-evolution.md). Detailed catalog fields and normalization are implementation conventions for those choices.
