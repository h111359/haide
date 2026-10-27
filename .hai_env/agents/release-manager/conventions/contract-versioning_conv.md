# Specification-contract versioning policy

## Independent boundary

Track the specification contract with an independent, monotonically increasing
integer revision, rather than a SemVer release track. It covers the
structure and rules consumers rely on: tree organization and balance, node types,
node formats, folder structure, definitions, conventions, and governing
specification-manager `SKILL.md` instructions. The contract is broader than any
single file-format schema. Determine compatibility from guarantees and effects,
not from whether a changed file is executable.

Specification-manager owns the contract's definitions, governing specification
rules, compatibility assessments requiring domain decisions, and actual migrations.
Release-manager records release impact and checks the evidence; it does not revise
those rules or perform migrations. Return dependencies to leader with affected
sources, old and proposed guarantees, impacted consumers, and the needed outcome.
Only leader can route that work to another agent.

## Changes and version impact

Review relevant changes against the last published contract baseline. Establish
the initial integer revision explicitly; do not assume an initial number from
examples or the bundle's version. Advance an established revision when its contract
changes, classifying compatible and breaking effects separately and explaining
consumer impact. The integer is an identity for the contract revision, not a code
for the severity of its change.

Editorial edits and equivalent procedure rewrites that preserve the same contract
require no contract-revision change. Such edits can still appear in a bundle release.
Conversely, changing a governing instruction that changes required structure or
behavior can change the contract without changing JSON or Markdown syntax.
A contract revision does not dictate a bundle bump mechanically: assess the bundle's
public compatibility separately and document how the contract change affects it.

## Target and applied revisions

Keep these distinct:

- Target contract revision: the specification rules supplied by a particular HAI bundle.
- Applied contract revision: the revision an existing specification tree has actually
  been assessed or migrated to and verified against.

The discussed metadata design has three roles: the versioned bundle manifest's
`contracts` information identifies included targets; the owning framework agent's
`.hai/agents/specification-manager/contract.json` identifies its contract; and the
specification root's `__ncf__.md` records that tree's applied revision. These are
future adoption locations, not assertions that those files or fields already exist.
Before first writing them, establish the exact schemas, identifiers, field names,
and historical baselines explicitly with the owning role and caller. Preserve
existing unrelated node fields. Never infer a historical applied revision from the
current installed bundle or label a tree migrated merely by changing its marker.
Environment-state `compatible_version` is a separate format identifier.

The specification is living information, continuously updated by product requests
and by scoped reconciliation with its governing contract. A reconciliation must
preserve product meaning, stable identities, and history. Newly required product
information must be surfaced as a question or unresolved dependency, never invented
to make a tree pass validation. Migrating specification documentation does not
establish that the product has implemented or fulfilled what it describes.

For relevant specification changes, inspect the trustworthy applied revision and
compare it with the target before new specification mutations. If different,
unknown, or incompatible, require a scoped assessment and any necessary migration
through specification-manager before dependent specification mutations proceed.
An assessment may establish that no content migration is necessary; only record
an applied revision when the owning role has verified that outcome. Report
which trees and operations are affected, rather than blanket-migrating all trees.

## Release and upgrade dependencies

A bundle release can ship a new contract target without migrating every consumer's
workspace. Include verified compatibility and upgrade information, applicable
migration requirements, and known limitations in the candidate. Do not require a
local specification feature to be enabled or fabricate a specification tree just
to assess framework changes.

Missing baseline or schema decisions block dependent compatibility claims and
metadata writes; continue independent release preparation and return the exact
dependency. If an affected operation uses an existing local tree, its target/applied
gate remains relevant even when other release preparation can continue. Do not
claim migration tooling, automated upgrades, or specification fulfillment that has
not actually been implemented and verified.
