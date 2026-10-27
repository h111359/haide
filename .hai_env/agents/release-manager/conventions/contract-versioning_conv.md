# Compatibility dependencies for releases

## Owning authorities

The specification owner's [contract-versioning convention](../../../../.hai/agents/specification-manager/conventions/contract-versioning_conv.md)
is the authority for the specification compatibility boundary, independent integer
version, target/applied distinction, transition ledger, assessment and migration
rules. Read it for every release, together with the owner's
[declaration](../../../../.hai/agents/specification-manager/contract.json).
Do not duplicate or override those semantics in release policy.

Environment-manager owns the independent state-format boundary. Its
[declaration](../../../../.hai/agents/environment-manager/contract.json) provides
`current_state_format_version` and `supported_state_format_versions`; the
[state convention](../../../../.hai/conventions/state_conv.md) governs compatibility
and authorized migration. Saved environment state uses `state_format_version`.
The former `compatible_version` is unsupported legacy metadata, not an alias or
a source for either current compatibility version.

The [release policy](release_conv.md#manifest-schema-and-consistency) owns the exact
release-manifest schema and checks that its `contracts` snapshot agrees with both
declarations in the candidate. These adopted declarations are independent of HAI
SemVer. A release manifest records shipped targets, never proof that an installed
consumer's state or specification tree was migrated.

## Assessment and handoff

Compare relevant changes with trustworthy published-baseline evidence and the
specification owner's transition ledger. Release-manager records release impact,
readiness, consumer-facing compatibility notes and verified upgrade requirements.
Specification-manager owns specification contract decisions and tree migrations;
environment-manager owns state-format decisions and state migrations. Return
dependencies to leader with the affected sources and consumers, old and proposed
guarantees, evidence, and needed outcome. Only leader routes specialist work.

When release work depends on an existing or new tree, apply the specification
owner's assessment, creation and migration gates by reference, returning required
decisions and approval dependencies through leader. A release assessment does not
grant tree-mutation authority or establish product implementation or fulfillment.

## Release and upgrade scope

A bundle can ship a new target without migrating every consumer workspace. Include
verified compatibility and upgrade information, required migration scope and known
limitations in the candidate. A disabled local specification feature does not block
framework release assessment and does not authorize creating or migrating a product
tree. General startup validates environment context without scanning specification
trees; specification compatibility checks occur through the owning role when the
operation requires them.

Missing history, invalid declarations or unresolved owner decisions block dependent
claims and writes; continue independent preparation. Report affected trees and
operations accurately. Do not claim automated upgrades, legacy migration tooling,
or product fulfillment without implemented and verified evidence.
