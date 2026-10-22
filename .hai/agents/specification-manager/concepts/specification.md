# Specification

## Definition

[specification] is a collection of files organized in a subfolders tree with a single folder root which combined represents fully the whole product from various aspects - business, technical, operational and so on and also add additional domain information needed for proper understanding of the product. This is the foundation for specification-driven product development.

## Purpose

[specification] organizes the full product documentation so an AI can discover and read only the parts relevant to its current task. Navigation must describe content clearly without prescribing required or optional reading.

## Explanation

### Physical representation

- The specification should reside in a folder structure which to be organized in a way similar to a balanced tree. The nodes of the tree will be folders. The inheritors of a node will be subfolders in the node folder. And vice versa - the node folder will be located in the folder of its ancestor.
- A folder can have subfolders in case it is not a leaf. In case of leaf the folder should have aditional file in it with the part of the specification.

- Represent every specification node as a folder.
- Represent parent-child relationships through physical folder nesting.
- Every node folder contains a configuration file named __ncf__.md.
- A branch contains __ncf__.md and child-node folders.
- A leaf contains __ncf__.md and a file in format specific to the lead type.
- A node is exclusively a branch or a leaf.
- The caller supplies the specification root explicitly. A path alone does not authorize creating a tree or changing its contents.

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
- Put each leaf-type convention in its own <type>_conv.md file in this package's `conventions/` folder.
- Convention files are outside the specification tree and do not require __ncf__.md.
- Each leaf has exactly one type.
- Allow multiple leaves of the same type.
- Use the convention filename without `_conv.md` as the registered `type` identifier. Identifiers use lowercase words separated by hyphens.
- Each convention defines the format and required content of the leaf's single content file. The content file is separate from __ncf__.md.
- In each type entry below, Specification links to the convention for that type, relative to this file.

### Classification rules

- Classify information by the question it answers and its intended audience, using the scopes below. Folder location and subject family do not determine type.
- Split material that answers different questions into separate leaves and connect them with relative links. Keep each fact or rule in one canonical leaf.
- Prefer a specialized type over a general type when its scope applies. For example, a security requirement belongs in Security; a performance requirement belongs in Quality requirements.
- Separate desired behavior, design, observed state, rationale, and procedures. They can concern the same feature while belonging to different types.
- Product-specific AI prompts, model behavior, retrieval, and evaluation belong to the same types as other product behavior, design, and tests. Instructions for AI working on the repository belong in Development guide.
- Domain terminology belongs in Glossary; domain policies and constraints belong in Business rules; domain entities and relationships belong in Data model. Supporting domain explanations stay with the rule, model, or behavior they explain.
- Request inputs, temporary analysis, implementation plans, execution logs, and conversations remain outside the specification in caller-managed work records. Promote only durable product knowledge into the specification and link to its supporting source when useful.
- If scope remains uncertain, record the ambiguity and request a classification decision rather than silently duplicating content or inventing a type. Add a type only when no existing scope reasonably covers the material.

### Leaf types

#### Product charter

##### Definition

The product's purpose, intended value, audience, boundaries, and measures of success.

##### Scope

Use for the problem being solved, stakeholders, user groups, business context, value proposition, product goals, scope exclusions, commercial assumptions, roadmap direction, and product-level success measures. Put specific capabilities in Functional requirements, domain policies in Business rules, and implementation choices in Architectural decision.

##### Specification

[Product charter convention](../conventions/product-charter_conv.md)

#### Functional requirements

##### Definition

The externally observable capabilities and behaviors the product must provide.

##### Scope

Use for actor goals, use cases, triggers, inputs, outcomes, error behavior, and acceptance criteria, including required AI behavior and human handoffs. Put reusable domain constraints in Business rules, measurable service qualities in Quality requirements, screen interaction in UI/UX specification, and internal implementation in Module specification or Algorithm specification.

##### Specification

[Functional requirements convention](../conventions/functional-requirements_conv.md)

#### Quality requirements

##### Definition

Measurable expectations and constraints on how well the product operates and can be maintained.

##### Scope

Use for performance, capacity, availability, reliability, scalability, compatibility, portability, maintainability, localization, cost budgets, and measurable usability or accessibility targets. Include AI accuracy, latency, and cost targets. Put security, privacy, and compliance obligations in Security; interface design in UI/UX specification; telemetry implementation in Observability; and verification procedures in Test specification.

##### Specification

[Quality requirements convention](../conventions/quality-requirements_conv.md)

#### Business rules

##### Definition

Domain policies, constraints, and derivations that determine valid business decisions and states.

##### Scope

Use for eligibility, pricing policy, entitlements, business calculations, domain invariants, and legally or contractually imposed business behavior. Include domain explanations and examples needed to interpret each rule. Put terminology in Glossary, feature behavior that applies the rule in Functional requirements, calculation implementation in Algorithm specification, and security or data-protection obligations in Security.

##### Specification

[Business rules convention](../conventions/business-rules_conv.md)

#### Glossary

##### Definition

The canonical meanings of terms used to understand the product and its domain.

##### Scope

Use for domain vocabulary, acronyms, synonyms, units, conceptual distinctions, and background explanations of terms, including AI terminology specific to the product. Put rules governing those concepts in Business rules, entity relationships in Data model, and field-level definitions in Data dictionary. Do not use as a miscellaneous knowledge store.

##### Specification

[Glossary convention](../conventions/glossary_conv.md)

#### Module specification

##### Definition

The internal responsibilities, structure, and behavior of one bounded product component.

##### Scope

Use for component boundaries, dependencies, internal state, configuration semantics, extension points, and implementation constraints. Include product AI agents, prompt composition, model selection configuration, and retrieval components. Put system-wide structure in Architecture overview, contracts between components in Interface contract, multi-step coordination in Processing flow, computational methods in Algorithm specification, and contributor instructions in Development guide.

##### Specification

[Module specification convention](../conventions/module-specification_conv.md)

#### Architecture overview

##### Definition

A system-wide view of the product's major components and their relationships.

##### Scope

Use for system context, boundaries, major components, dependency direction, trust zones, principal data paths, technology strategy, and logical deployment views. Put component internals in Module specification, concrete hosting resources in Infrastructure or Cloud, and reasons for choosing an approach in Architectural decision.

##### Specification

[Architecture overview convention](../conventions/architecture-overview_conv.md)

#### Architectural decision

##### Definition

A record of one significant technical choice, its context, alternatives, and consequences.

##### Scope

Use for durable decisions about architecture, technology, data, integration, security, and engineering tradeoffs. Record why a choice was made and what would justify reconsidering it. Put the current resulting design in its relevant specification type, product priorities in Product charter, and the decision index in ADR catalogue. Routine request questions remain in request records.

##### Specification

[Architectural decision convention](../conventions/architectural-decision_conv.md)

#### ADR catalogue

##### Definition

A navigable index of architectural decision records and their relationships.

##### Scope

Use only for decision identifiers, titles, decision states, dates, summaries, links, and supersession relationships. Put complete context, alternatives, and consequences in Architectural decision. This catalogue indexes decisions rather than replacing the specification's general navigation.

##### Specification

[ADR catalogue convention](../conventions/adr-catalogue_conv.md)

#### Data model

##### Definition

The structure of domain and persisted data, including entities, relationships, and structural invariants.

##### Scope

Use for conceptual and logical models, storage schemas, keys, cardinalities, ownership, state relationships, and structural consistency constraints. Include document, vector, feature, and training-data structures where applicable. Put detailed field meanings in Data dictionary, exchanged payloads in Interface contract, domain policies in Business rules, and privacy or retention obligations in Security.

##### Specification

[Data model convention](../conventions/data-model_conv.md)

#### Data dictionary

##### Definition

The precise meaning and representation of individual data fields and values.

##### Scope

Use for field names, types, units, formats, nullability, defaults, allowed values, semantic meaning, provenance, and data-quality constraints. Put entity relationships and storage structure in Data model, wire schemas in Interface contract, vocabulary shared beyond data fields in Glossary, and access or retention policy in Security.

##### Specification

[Data dictionary convention](../conventions/data-dictionary_conv.md)

#### Interface contract

##### Definition

An agreement on communication across a product or component boundary.

##### Scope

Use for APIs, events, messages, files exchanged between systems, command-line interfaces, extension protocols, and AI tool contracts. Define payloads, operations, errors, ordering, retries, versioning, and compatibility guarantees. Put interface internals in Module specification, orchestration across interfaces in Processing flow, human interaction design in UI/UX specification, and usage tutorials in User documentation.

##### Specification

[Interface contract convention](../conventions/interface-contract_conv.md)

#### Processing flow

##### Definition

The ordered coordination of actions, states, and participants in a product process.

##### Scope

Use for runtime workflows, state transitions, asynchronous processing, scheduled jobs, data pipelines, and AI orchestration with tool calls or human review. Specify branching, concurrency, retries, compensation, and failure paths. Put individual computations in Algorithm specification, communication details in Interface contract, build automation in CI/CD, and human operational procedures in the appropriate guide.

##### Specification

[Processing flow convention](../conventions/processing-flow_conv.md)

#### Algorithm specification

##### Definition

A precise computational method that transforms inputs into results.

##### Scope

Use for calculations, ranking, matching, optimization, parsing, inference methods, retrieval scoring, and prompt templates or output-selection logic when they define a computational method. Include assumptions, steps, numerical behavior, and complexity. Put the business policy being implemented in Business rules, component configuration in Module specification, process orchestration in Processing flow, and evaluation cases in Test specification.

##### Specification

[Algorithm specification convention](../conventions/algorithm-specification_conv.md)

#### UI/UX specification

##### Definition

The design of the product's human-facing presentation and interaction.

##### Scope

Use for information architecture, navigation, screens, interaction states, visual design, content design, accessibility behavior, localization presentation, and conversational interfaces. Include AI disclosures, uncertainty presentation, and review controls. Put product capabilities in Functional requirements, measurable experience targets in Quality requirements, and end-user instructions in User documentation.

##### Specification

[UI/UX specification convention](../conventions/ui-ux-specification_conv.md)

#### Test specification

##### Definition

The evidence and verification methods used to determine whether the product meets its requirements.

##### Scope

Use for test strategy, cases, fixtures, environments, coverage, acceptance checks, performance experiments, security checks, and AI evaluation datasets, metrics, and pass criteria. Put the target behavior or threshold in its originating requirement leaf and automation wiring in CI/CD. Keep individual execution logs and transient results in request or test-run artifacts; link durable evidence when needed.

##### Specification

[Test specification convention](../conventions/test-specification_conv.md)

#### Inventory

##### Definition

A dated factual register of product assets, dependencies, resources, and their ownership.

##### Scope

Use for repositories, services, packages, versions, licenses, datasets, models, external integrations, environments, resource instances, owners, and support or end-of-life dates. Record what is known to exist and where that fact came from. Put desired topology in Infrastructure or Cloud, required component behavior in Module specification, policies in Security, and change rationale in Architectural decision.

##### Specification

[Inventory convention](../conventions/inventory_conv.md)

#### Infrastructure

##### Definition

The provider-independent and non-cloud-specific runtime foundation required to host the product.

##### Scope

Use for hosting topology, compute, networks, storage, containers, orchestration, DNS, certificates, capacity allocation, and environment configuration that is portable across providers or hosted on premises. Put provider-specific services and account organization in Cloud, logical component views in Architecture overview, observed resource lists in Inventory, and rollout procedures in Deployment guide.

##### Specification

[Infrastructure convention](../conventions/infrastructure_conv.md)

#### Cloud

##### Definition

The product's provider-specific cloud organization, services, and resource configuration.

##### Scope

Use for cloud accounts, subscriptions, projects, regions, managed services, resource mappings, provider quotas, billing controls, and provider-specific infrastructure-as-code configuration. Put portable hosting design in Infrastructure, security policy in Security, observed instances and versions in Inventory, and operator steps in the appropriate guide. A provider-specific resource is described here and referenced from portable designs.

##### Specification

[Cloud convention](../conventions/cloud_conv.md)

#### Security

##### Definition

The requirements and design for protecting the product, its users, and its information.

##### Scope

Use for threats, abuse cases, identity, permissions, trust boundaries, secrets handling, encryption, privacy, consent, data classification, retention, audit obligations, software supply-chain controls, and security or data-protection compliance. Include prompt injection, unsafe tool use, and sensitive AI inputs or outputs. Put implementation configuration in the relevant module or hosting leaf, checks in Test specification, and incident response steps in Operations guide or Recovery guide.

##### Specification

[Security convention](../conventions/security_conv.md)

#### Observability

##### Definition

The telemetry and interpretation rules that make product behavior and health observable.

##### Scope

Use for logs, metrics, traces, correlation, dashboards, alert conditions, service-indicator calculations, telemetry sampling, and telemetry retention configuration. Include AI quality, usage, token, and cost monitoring. Put required service targets in Quality requirements, privacy and audit policies in Security, and human alert response in Operations guide.

##### Specification

[Observability convention](../conventions/observability_conv.md)

#### CI/CD

##### Definition

The automated process that integrates changes and produces, verifies, and delivers release artifacts.

##### Scope

Use for pipeline triggers, jobs, dependencies, build environments, artifact provenance, automated checks, release gates, promotion, and automated deployment or rollback orchestration. Put test definitions in Test specification, hosting design in Infrastructure or Cloud, human rollout procedures in Deployment guide, and local contributor workflows in Development guide.

##### Specification

[CI/CD convention](../conventions/ci-cd_conv.md)

#### Deployment guide

##### Definition

An executable human procedure for installing, upgrading, releasing, or rolling back the product.

##### Scope

Use for deployment prerequisites, approved artifacts, environment preparation, migrations, rollout order, release checks, rollback criteria, and post-release verification. Put automated pipeline definitions in CI/CD, steady-state administration in Operations guide, and recovery from loss or disaster in Recovery guide.

##### Specification

[Deployment guide convention](../conventions/deployment-guide_conv.md)

#### Operations guide

##### Definition

Human procedures for running and administering the product during normal service and operational incidents.

##### Scope

Use for routine maintenance, service administration, support triage, alert response, capacity management, incident coordination, and safe mitigations while service remains recoverable in place. Put releases in Deployment guide, restoration or disaster failover in Recovery guide, telemetry definitions in Observability, and end-user tasks in User documentation.

##### Specification

[Operations guide convention](../conventions/operations-guide_conv.md)

#### Recovery guide

##### Definition

Human procedures for restoring service and data after loss, corruption, or disaster.

##### Scope

Use for backup execution and verification, restoration, disaster declaration, failover, failback, data reconciliation, recovery drills, and evidence of recovery. Put recovery-time and recovery-point targets in Quality requirements, backup infrastructure in Infrastructure or Cloud, routine incident triage in Operations guide, and ordinary release rollback in Deployment guide.

##### Specification

[Recovery guide convention](../conventions/recovery-guide_conv.md)

#### User documentation

##### Definition

Task-oriented explanations that help product consumers use the product successfully.

##### Scope

Use for onboarding, tutorials, user-facing configuration, feature explanations, integration examples, FAQs, troubleshooting, and release notes describing user-visible changes. Consumers may be end users, administrators using product features, or developers integrating with published interfaces. Put normative interface definitions in Interface contract, behavior requirements in Functional requirements, service operation in Operations guide, and work on the product's source repository in Development guide.

##### Specification

[User documentation convention](../conventions/user-documentation_conv.md)

#### Development guide

##### Definition

Workspace-specific instructions for humans and AI agents developing and maintaining the product.

##### Scope

Use for local setup, toolchain commands, coding conventions, contribution and review workflow, documentation maintenance, and durable AI working instructions or context-discovery procedures. Put the directory map and path-based discovery guidance in Workspace structure; product runtime AI behavior in Functional requirements, Module specification, or Algorithm specification; automated pipelines in CI/CD; technical rationale in Architectural decision; and temporary task records in caller-managed work records. Reusable framework instructions remain outside the product specification.

##### Specification

[Development guide convention](../conventions/development-guide_conv.md)

#### Workspace structure

##### Definition

A concise description of the workspace's folders and files that helps humans and AI agents locate relevant material and choose what to examine further.

##### Scope

Use for the meaning of top-level folders and files, important descendants, groups of same-purpose files, and task-oriented pointers into the workspace. Describe the observed layout with enough detail for discovery without an exhaustive file inventory. Put development procedures and working instructions in Development guide, logical components and their relationships in Architecture overview, and detailed asset, dependency, and version registers in Inventory; link these sources rather than duplicating them.

##### Specification

[Workspace structure convention](../conventions/workspace-structure_conv.md)

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

- [workspace]: the product root or roots established by the caller for product-source discovery; the specification root alone does not identify them.

## References

- `../SKILL.md`: specification management procedures and input contract.
- `../conventions/`: registered leaf content formats linked in the type entries above.


