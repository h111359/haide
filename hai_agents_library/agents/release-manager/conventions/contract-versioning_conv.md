# Compatibility dependencies for releases

## Owning authorities

Environment-manager owns the independent state-format boundary. Its
[declaration](../../../../.hai/agents/environment-manager/contract.json) provides
`current_state_format_version` and `supported_state_format_versions`; the
[state convention](../../../../.hai/conventions/state_conv.md) governs compatibility
and authorized migration. Saved environment state uses `state_format_version`.
The former `compatible_version` is unsupported legacy metadata, not an alias or
a source for the current state-format version.

The [release policy](release_conv.md#manifest-schema-and-consistency) owns the exact
release-manifest schema and checks that its `contracts.environment_state` snapshot agrees with the
state declaration in the candidate. The state-format version is independent of HAI
SemVer. A release manifest records shipped targets, never proof that an installed
consumer's environment state was migrated.

Agent configuration contracts at each installed package's `configuration/contract.json`
are independent of state format and release SemVer. Release checks assess shipped
core declarations and compatibility without migrating consumer settings. External
configuration is excluded from bundles and preserved by upgrades. Optional agent
contracts remain part of their separate packages; they do not add a mandatory
optional-owner dependency to core startup.

## Release and upgrade scope

A bundle can ship a new state-format target without migrating every consumer workspace. Release assessment does not authorize changing a consumer environment; environment-manager owns any separately authorized state migration.

## References

- [Release procedures](../SKILL.md#procedures) — impact assessment, owner handoff and upgrade verification.
