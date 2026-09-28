# Documentation evolution: accepted conversation record

This file preserves the user's instructions and accepted design choices from the documentation discussion. It is source evidence for this documentation revision, not evidence of implemented AIH runtime behavior. Quoted user text is retained as supplied; the accepted-design section records the proposals accepted in that discussion.

## Product knowledge and ownership

The user proposed these principles:

> The files requirements.md, decisions.md, context.md remain the entry points for the documentation, maintained in .aih_product
>
> There to be invented convention for extension of these files with additional files, each of which is in one of the predefined types primarely listed in 11.7
>
> These extension files are maintained automatically by AIH together with requirements.md, decisions.md, context.md.
>
> The product MAY have additional materials related to the context/documenation which are stored outside .aih_product. These MUST be able to be refered in the context documentation in .aih_product/ but MUST NOT be modified by default. Their modification MUST happen only via requests and these files should be treated in a way similar to the product code and their modification should be result of implementation of a request.

## Accepted document organization and references

The user selected: "I agree with option \"Extensions grouped by document type\"."

The subsequently accepted proposal uses `.aih_product/documentation/` with the three entry files, `catalog.yaml`, and `extensions/<document-type>/<subject>.<format>`. Product-area subdivisions may be used when needed. File names use descriptive lowercase words separated by hyphens, without request IDs, dates, or entry numbers. Only relevant documents are created, in formats suitable for their information.

The user asked for extensions to have IDs and references similar to sources and then instructed that this idea be applied. The accepted proposal assigns shared stable document IDs such as `D1`, `D2` within a documentation collection, maintained by `catalog.yaml`. IDs survive moves and renaming and are not reused after retirement. Each entry file lists only its referenced documents in a linked `Referenced documents` section. `Details: {D3:section "Field constraints"}` identifies detailed specification or explanation; `{S1:L40-45}` remains supporting source evidence. Named section, field, entity, or operation locators are preferred for maintained documents. A whole-document reference is allowed when the whole document applies. External materials may be registered with an explicit maintenance classification; referencing a material never authorizes modification.

The accepted organization separates concise entry files from typed detail, maintains one authoritative copy of a topic, and verifies both together. The entry layer is separate from the balanced extension-navigation tree. The type convention defines content, permitted formats, provenance, and validation without generating empty templates for every possible type.

## Migration and request-specific documentation

The user's implementation instruction was:

> Apply the idea in definitions/definitions_R20260925_2309/attachments/extract_context.md and the files requirements.md, decisions.md, context.md. Rename the durrent folder definitions/definitions_R20260925_2309 to .aih_product/documentation. The intention will be this folder to become the AIH framework prodict folder of AIH repo itself. Let definitions/definitions_R20260925_2309/attachments/extract_context.md remain located in definitions/definitions_R20260925_2309/attachments for now but rename it to definitions/definitions_R20260925_2309/attachments/update_documentation.md. It should continue receive source files describing the change request and it should generate a request specific documentation in a sub-folder of .aih_product/requests/ where each new request should have its own folder based on its ID and normalized name. The output should follow the new definition of the documentation and should generate the files requirements.md, decisions.md, context.md and unresolved.md + extensions if needed. The request documentation should contain only the changes and should not repeat the existing already documentation in .aih_product/documentation. Reflect these ideas in definitions/definitions_R20260925_2309/requirements.md and definitions/definitions_R20260925_2309/decisions.md.

## Clarified request storage

The user selected:

> Yes: use requests/<ID>_<normalized-name>/, with lifecycle status recorded without moving the folder (recommended).

The user also selected:

> In <request-folder>/documentation/, using a required request_name input normalized to a stable slug (recommended).

These choices replace the former `change_requests/active/` and `change_requests/history/` storage arrangement. Closing a request retains its location and historical evidence; lifecycle and archival status are recorded in metadata.

## Implementation conventions derived from the accepted design

The following are implementation choices documenting the accepted requirements, rather than additional verbatim user instructions: baseline fingerprints bind change targets to the compared product revision; request catalogs identify additions, modifications, removals, and unchanged findings; request-local document IDs map explicitly to product document IDs; unchanged product material is referenced rather than recopied; and the complete generated documentation subtree is verified before replacement, preserving request inputs, implementation records, and product documentation.

This revision specifies the documentation architecture. It does not establish that AIH runtime support, independent reconstruction, or all previously specified product behavior is implemented or verified.

## Attachment preservation clarification

The user's clarification was:

> In case the attachment should become part of the product documentation - copy them there. But originally the attachments will be saved in the request specific attachments folder and should stay there without change

Original request attachments remain unchanged in their original locations. Product documentation refers to them. Copying material into product documentation is permitted when that material is deliberately included there; a copy retains source provenance and does not authorize editing the original. For this migration the existing attachments remain under `definitions/definitions_R20260925_2309/attachments/`, with the explicitly requested prompt rename as the exception.

## Product reference boundary

The user's later clarification supersedes any earlier suggestion that product documentation may cite request attachments in place:

> The product documentation MUST NOT reference attachments in the requests folders. If file is referenced - it should be copied in the product documentation structure or should be outside .aih_product (hence part of the product itself)

Every file reference from product documentation, including source citations, Details links, extension references, catalog records, and evidence links, must resolve either within the product documentation collection or outside `.aih_product/` as product-owned material. Product integration retains required request evidence as immutable copies within the product documentation before creating references. Request originals remain unchanged. Provenance may retain request IDs, original filenames, and digests without linking to files in a request folder. References between a request change set and its product baseline are unaffected by this product-only boundary.
