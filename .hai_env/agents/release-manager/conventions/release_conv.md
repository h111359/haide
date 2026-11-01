# HAI bundle release policy

## Release unit and identity

The initial release unit is one HAI bundle with one `MAJOR.MINOR.PATCH` version.
Changing this core bundle version scheme requires an explicit product decision.

An identified installed release has exactly one current `.hai/release-<version>.json`.
Its filename version and content `version` must match the selected bundle version,
`v<version>` tag, and `hai-<version>.zip` asset. Its `contracts` information records
included contract targets; no second fixed `release.json` authority exists.
The manifest is a release artifact created only for an authorized candidate with a
selected bundle version; adopting a state-format declaration does not
create a release. No first bundle version is implied by a state-format version.

Published tags and release bytes are immutable; corrections use a new release. A selected release candidate and a released installation require exactly one current manifest matching their own declarations. Multiple, malformed or inconsistent current manifests block identity verification. Historical manifests outside `.hai/` are historical evidence, excluded from the reusable package.

## Manifest schema and consistency

This schema governs newly prepared candidate manifests. It does not authorize
rewriting existing candidate manifests or historical release evidence.

The manifest is a UTF-8 JSON object with exactly `version` and `contracts`.
`version` is the selected nonempty SemVer string. `contracts` is an object with
exactly `environment_state`, an object with exactly the
fields shown below. This is a schema illustration, not a release record or a
selected bundle version:

```json
{
  "version": "<selected SemVer>",
  "contracts": {
    "environment_state": {
      "current_state_format_version": 1,
      "supported_state_format_versions": [1]
    }
  }
}
```

| Manifest entry | Owning declaration within the candidate |
| --- | --- |
| `contracts.environment_state` | `.hai/agents/environment-manager/contract.json` in its entirety |

Duplicate JSON keys at any depth, nonstandard numeric constants, extra/missing
schema keys and malformed values are invalid. All version numbers in `contracts`
are positive integers, excluding Booleans. `supported_state_format_versions` is
a nonempty array of unique positive integers including `current_state_format_version`.
State-format values must come from authorized owner changes, never from the HAI
SemVer number.

## Version impact

For an established stable line:

| Impact | Recommended increment |
| --- | --- |
| Existing supported consumers must change because a public guarantee breaks | MAJOR |
| Backward-compatible new capability or public addition | MINOR |
| Backward-compatible correction, including editorial or equivalent procedural clarification | PATCH |

## Agreed initial release and experimental policy

The human selected `0.1.0` as HAI's first bundle release. During `0.x`, new
capabilities and breaking changes increment MINOR; compatible fixes increment
PATCH. Notes explicitly describe breaking effects. Moving to `1.0.0` requires
an explicit stability decision. These choices do not change independent state-format
numbering and do not authorize publication by themselves.

## Readiness and evidence

A candidate is ready for publication only when:

- Source and published comparison baseline are identified, or the first-release
  decision is explicit; repository and publication destination are verified.
- Version, manifest, planned tag, and archive name agree; relevant contract targets,
  assessment, compatibility notes, and migration dependencies are resolved.
- Release notes describe changes, breaking behavior, upgrade requirements, and
  known limitations without claiming unverified fulfillment.
- Applicable validation and tests pass, the archive has been inspected, and the
  exact candidate commit and asset digest are recorded.
- Required decisions and publication authority cover the concrete candidate.

## References

- [Release procedures](../SKILL.md#procedures) — execution, checks, source sequence, authority and recovery.
- [Compatibility dependencies](contract-versioning_conv.md) and [package contract](publishing_conv.md) — owning contract boundaries and package requirements.
