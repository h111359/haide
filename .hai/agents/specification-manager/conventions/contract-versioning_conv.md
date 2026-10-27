# Specification contract versioning

## Authority and scope

`../contract.json` is the machine-readable authority for this package's current
`specification_compatibility_version`. Its sole field is a positive JSON integer;
booleans, strings, zero, duplicate keys, extra fields, and missing values are
invalid. This version is independent of HAI core-state compatibility, agent
formats, package releases, Git tags, and the audit inventory `format`.

The specification contract includes this package's concept, all registered leaf
conventions, organization and balance rules, definitions, navigation, content
lifecycle, required behavior, and compatibility and catalogue rules. It is not
only the YAML schema. A contract-affecting change increments the integer, even
when no metadata fields change. Editorial clarifications that preserve every
obligation may retain it; record why no contract changed when that is uncertain.
The concept's Leaf types section alone registers leaf types. This convention is
contract knowledge, never a leaf type.

The root `__ncf__.md` has exactly this flat string metadata at baseline 1:

```yaml
specification_compatibility_version: "1"
```

Only the root carries it, whether the root is a branch or a leaf. It claims the
whole tree has been verified against that contract, not just its root schema.
Use canonical positive decimal strings without signs or leading zeroes. Do not
infer a marker from HAI state, another tree, inventory format, or file age.

## Baseline 1

Version 1 establishes the current package contract, including its 28 registered
leaf types, the concept's node UUIDs and metadata, exclusive branch/leaf layout,
node configuration sizes, maximum eight immediate children, global leaf-depth
difference at most one, canonical product facts and source/approval preservation,
explicit unknowns, task-scoped discovery, and the derived root catalogue.
The package's concept, conventions, and SKILL.md provide the complete normative
rules; this list is an orientation, not a replacement. No earlier prototype
contract versions or migration history are asserted.

## Check at the beginning of specification work

Read the package contract and inspect the supplied tree before dependent product
edits, including new sessions and resumed work whose inputs may have changed.
This is not a general HAI startup check. Read-only assessment and inventory remain
available for every compatibility state; incompatibility never authorizes edits.

- Current: marker equals the valid package target; ordinary authorized work may
  proceed, subject to discovered structural/content issues.
- Unmarked: assess the actual tree against all target rules and propose explicit
  adoption. Absence does not establish an older version or an automatic upgrade.
- Older: identify the exact source version and every applicable ledger transition
  through the target; missing transition knowledge blocks migration writes.
- Newer: stop dependent edits; obtain a package supporting that version or an
  explicitly designed and approved conversion. Never lower a marker as a shortcut.
- Invalid: malformed contract or marker (including duplicate/unsupported scalars)
  blocks dependent edits. Diagnose read-only and obtain a scoped repair/adoption
  plan and approval; do not silently normalize or infer the intended value.

New explicitly authorized specifications are created directly at the current
version using meaningful supplied content; they need no fictional migration.
Verify the complete new tree before reporting its marker as truthful.

## Plan, approval, execution, and verification

Every compatibility migration, adoption, or compatibility-marker repair requires
an explicit plan and the human user's approval before any migration write. A
coordinating caller may relay that approval with its scope and evidence, but
cannot substitute its own approval. This
includes a marker-only update. General permission to maintain content, an audit,
or a version mismatch alone is insufficient. Keep the plan and approval in the
caller's established work record or supplied context, outside product facts;
standalone use does not require HAI records. Do not invent an approval history.

The plan identifies the root and source evidence (including unmarked/invalid),
source and target versions, applicable transition IDs, exact changed rules,
affected nodes/files and scoped content transformations, identity and product
meaning preservation, approval history and unresolved unknowns, catalogue/link
updates, expected verification, recovery boundaries, and explicit approvals or
open decisions. An unmarked-tree plan includes the full target-rule assessment
and explains which requirements already hold and which need change. Marker-only
adoption still needs this evidence and explicit approval.

After approval, recheck paths, contents, authority and the plan's applicability.
Stop on changed inputs or new conflicts. Apply only the agreed transformations;
preserve UUIDs, meaning, source relationships, approval history, and unresolved
unknowns. Refresh the root catalogue for any resulting inventory changes. The
read-only renderer can prepare an adoption catalogue without a current marker;
its output is a candidate and does not approve adoption or validate compatibility.

Verify the complete target requirements, including manual content/behavior checks,
and compare saved identity/content/approval evidence. Use a staged candidate when
needed to check the target marker without prematurely asserting it in the live
tree. Write the live target marker only after the agreed transformations and
required target checks succeed, then rerun the final audit and manual checks.
Report a migration as applied only after final verification succeeds. A written
marker alone is never evidence of completed migration.

On partial failure, stop dependent writes, preserve completed work, and report
actual files, marker state, failed/unrun checks, and remaining changes. Never
claim atomicity, success, automatic rollback, or a completed migration. A retry
first reassesses the actual partial state against the approved plan; obtain
renewed approval if scope, source evidence, or transformations changed. Reuse a
still-applicable approval explicitly rather than inventing a fresh source state.

## Structured transition ledger

This convention owns the baseline and ledger. Add one structured record for each
future contract transition when its changed obligations are defined. Each record
must contain all fields below, with concrete rule changes and verification (not
only a version bump):

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
