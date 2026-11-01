# Specification contract versioning

## Authority and scope

`../contract.json` is the machine-readable authority for this package's current
`specification_compatibility_version`. Its sole field is a positive JSON integer;
booleans, strings, zero, duplicate keys, extra fields, and missing values are
invalid. This version is independent of HAI core-state compatibility, agent
formats, package releases, source-control tags, and the audit inventory `format`.

The specification contract includes this package's concept, all registered leaf
conventions, organization and balance rules, definitions, navigation, content
lifecycle, required behavior, and compatibility and catalogue rules. It is not
only the YAML schema. A contract-affecting change increments the integer, even
when no metadata fields change. Editorial clarifications preserving every obligation may retain it. An uncertain
classification needs an explanation that no contract obligation changed.
The concept's Leaf types section alone registers leaf types. This convention is
contract knowledge, never a leaf type.

The root `__ncf__.md` has exactly this flat string metadata at baseline 1:

```yaml
specification_compatibility_version: "1"
```

Only the root carries it, whether the root is a branch or a leaf. It claims the
whole tree has been verified against that contract, not just its root schema.
Markers are canonical positive decimal strings without signs or leading zeroes.
HAI state, another tree, inventory format and file age do not establish a marker.

## Baseline 1

Version 1 establishes the current package contract, including its 28 registered
leaf types, the concept's node UUIDs and metadata, exclusive branch/leaf layout,
node configuration sizes, maximum eight immediate children, global leaf-depth
difference at most one, canonical product facts and source/approval preservation,
explicit unknowns, task-scoped discovery, and the derived root catalogue.
The package's concept, conventions, and SKILL.md provide the complete normative
rules; this list is an orientation, not a replacement. No earlier prototype
contract versions or migration history are asserted.

## Compatibility states

Current means the root marker equals the valid package target. Unmarked establishes
no prior version; older requires a known ordered transition path; newer requires a
supporting package or explicitly designed conversion. Invalid contract/marker values
are not normalized or inferred. Read-only assessment/inventory remains available in
all states; incompatible states grant no product-edit authority. New authorized trees
start at the current target with meaningful content and complete target verification.

## Plan and approval contract

Every compatibility migration, adoption or marker repair, including marker-only work,
requires an explicit scoped plan and the human user's approval before migration writes.
A coordinator may relay scope/evidence but cannot substitute its own approval. General
content-maintenance permission, an audit or mismatch is not migration approval. Plans
and approval evidence belong in caller records/supplied context outside product facts;
standalone invocation does not require HAI records.

The plan identifies the root and source evidence (including unmarked/invalid),
source and target versions, applicable transition IDs, exact changed rules,
affected nodes/files and scoped content transformations, identity and product
meaning preservation, approval history and unresolved unknowns, catalogue/link
updates, expected verification, recovery boundaries, and explicit approvals or
open decisions. An unmarked-tree plan includes the full target-rule assessment
and explains which requirements already hold and which need change. Marker-only
adoption still needs this evidence and explicit approval.

## Execution ownership

[Adopt or migrate specification](../procedures/adopt-or-migrate.md) owns assessment,
plan/approval handling, transformation ordering, live-marker finalization, verification
and partial-state/retry handling. The role's Rules apply to every operation. General
HAI startup performs no specification compatibility assessment.

## Structured transition ledger

This convention owns the baseline and ledger. Each future contract transition is
represented by one structured record when its changed obligations are defined.
Each record contains all fields below, with concrete rule changes and verification
rather than only a version bump:

```yaml
transition_id: "<stable transition identifier>"
source_version: "<positive integer>"
target_version: "<next positive integer>"
changed_rules: ["<old obligation -> new obligation; authoritative references>"]
applicability: ["<which source trees/nodes/content are affected and exclusions>"]
scoped_migration: ["<specific transformations; what is preserved>"]
verification: ["<mechanical and manual acceptance checks, failure criteria>"]
```

These are documentation records, not node metadata or executable migrations.
The distributed/applied baseline is immutable under the same rule as entries.
Transitions must cover the precise ordered source-to-target path; never guess
that skipping an intermediate contract preserves semantics. Once applied to any
tree or distributed, an entry and its meaning are immutable. Correct obligations
through a new version/transition; do not rewrite history to make an old claim
appear compliant. A proposed, undistributed, unapplied entry may be revised
before adoption, with the associated plan reassessed. Per-tree approval and
applied outcomes belong to caller records, never fabricated in this package.

Ledger entries: none. Baseline 1 introduces no invented earlier source version.
