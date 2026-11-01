# Compatibility dependencies for releases

## Owning authorities

The specification owner's [contract-versioning convention](../../../../.hai/agents/specification-manager/conventions/contract-versioning_conv.md)
is the authority for the specification compatibility boundary, independent integer
version, target/applied distinction, transition ledger, assessment and migration
rules. Its [declaration](../../../../.hai/agents/specification-manager/contract.json) supplies the target.
Those semantics are not duplicated or overridden by release policy.

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

## Release and upgrade scope

A bundle can ship a new target without migrating every consumer workspace. A disabled local specification feature does not block framework release assessment and does not authorize creating or migrating a product tree. General startup validates environment context without scanning specification trees; specification compatibility checks belong to the owning role when required.

## References

- [Release procedures](../SKILL.md#procedures) — impact assessment, owner handoff and upgrade verification.
