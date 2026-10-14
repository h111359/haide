# Specification

## Definition

[specification] is a collection of files organized in a subfolders tree with a single folder root which combined represents fully the whole product from various aspects - business, technical, operational and so on and also add additional domain information needed for proper understanding of the product. This is the foundation for specification-driven product development.

## Purpose

The specification organizes the full product documentation so an AI can discover and read only the parts relevant to its current task. Navigation must describe content clearly without prescribing required or optional reading.

## Explanation

### 


  



Each leaf will be of a specific type. Different leaf types will be described by convention markdown files where the expected file purpose and format will be defined. 

The root folder of the specification should be stored as value in JSON file in folder .aih_memory/


### Physical tree

- The specification should reside in a folder structure which to be organized in a way similar to a balanced tree. The nodes of the tree will be folders. The inheritors of a node will be subfolders in the node folder. And vice versa - the node folder will be located in the folder of its ancestor.
- A folder can have subfolders in case it is not a leaf. In case of leaf the folder should have aditional file in it with the part of the specification. 

- Represent every specification node as a folder.
- Represent parent-child relationships through physical folder nesting.
- Every node folder contains a configuration file named __ncf__.md.
- A branch contains __ncf__.md and child-node folders.
- A leaf contains __ncf__.md and a file in format specific to the lead type.
- A node is exclusively a branch or a leaf.

### Organization and balance
- Organize upper levels by documentation subject families, such as product, architecture, engineering, operations, and user guidance.
- Organize deeper levels by meaningful subjects, domains, or modules.
- Treat subject families as navigation categories, distinct from leaf types.
- Allow no more than eight immediate children per branch.
- Count the specification root as depth zero.
- The depth difference between the shallowest and deepest leaves must not exceed one level across the entire tree.
- Maintain balance through meaningful regrouping when adding or splitting content.
- Permit single-child branches where necessary.
- Do not fabricate topics or content to satisfy structural limits.
- If meaningful organization cannot satisfy all limits, surface the conflict for a decision rather than silently relaxing a rule.

### Node configuration file format
__ncf__.md should have a standard format. It is in markdown as it should contact free text description of subfolders. 

__ncf__.md file should contain information for the type of the folder and explanation of all subfolders or in case of leaf - explanation of the information which the leaf file contains.  

__ncf__.md should have YAML front matter followed by Markdown.

Required metadata for every node:
- id: a unique, permanent UUID that survives moves and renaming.
- title: a human-readable title.
- kind: branch or leaf.

Additional required metadata for leaves:
- type: one registered leaf-type identifier.
- status: draft, approved, or deprecated.

### Branch Markdown:
- A Scope section describing the node’s subject.
- A Children table identifying every immediate child folder and explaining its purpose, scope, and distinguishing topics.
- Describe immediate children only; deeper detail belongs in their own node files.
- Keep descriptions useful for task-specific AI navigation without declaring required or optional reading.

### Leaf Markdown:
- Contains the type of the file in the leaf folder

Size limits
- Leaf __ncf__.md: target at most 8,000 characters; hard maximum 12,000.
- Branch __ncf__.md: hard maximum 4,000 characters.
- Count Unicode code points across the entire file, including YAML, whitespace, tables, and code, after normalizing line endings to LF.
- Split oversized content into meaningful leaves while preserving the tree’s balance.
- The 8,000-character target is advisory; the maximums are mandatory.

Leaf-type conventions
- Put each leaf-type convention in its own <type>.md file in `.hai_brain/conventions`.
- Convention files are outside the specification tree and do not require __ncf__.md.
- Each leaf has exactly one type.
- Allow multiple leaves of the same type.

### Leaf types
- Product charter.
- Functional requirements.
- Quality requirements.
- Business rules.
- Glossary.
- Module specification.
- Architecture overview.
- Architectural decision.
- ADR catalogue.
- Data model.
- Data dictionary.
- Interface contract.
- Processing flow.
- Algorithm specification.
- UI/UX specification.
- Test specification.
- Inventory.
- Infrastructure.
- Cloud.
- Security.
- Observability.
- CI/CD.
- Deployment guide.
- Operations guide.
- Recovery guide.
- User documentation.

### References and selective reading
- Use ordinary relative Markdown links with descriptive explanations of relationships.
- Repair links when nodes move or are renamed.
- Preserve stable node IDs across reorganizations.
- Keep each specification item in one canonical location and link to it rather than duplicating it.
- The AI decides what to read according to its task.

### Content lifecycle
- Create leaves only when meaningful content exists.
- Do not generate empty product-document templates merely to populate every type.
- Record unknowns explicitly within the relevant document rather than inventing answers.
- Document status does not imply implementation status.


## Supporting Terms

## References

- `.aih_brain/concepts/memory.md`: definition of [memory]
- `.hai_brain/conventions/state_conv.md`: state file where the location of the specification is stored


