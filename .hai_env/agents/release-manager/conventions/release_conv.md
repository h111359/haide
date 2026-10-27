# HAI bundle release policy

## Release unit and identity

Initially publish one HAI bundle with one `MAJOR.MINOR.PATCH` version. Do not
introduce independent package releases or a new version scheme without an explicit
product decision. An independent specification-contract version describes a
consumer boundary; it is not a second independently published bundle.

Use exactly one current `.hai/release-<version>.json` in the installed framework.
Its filename version and content `version` must match the selected bundle version,
`v<version>` tag, and `hai-<version>.zip` asset. Its `contracts` information records
included contract targets. Do not add a second fixed `release.json` authority.
The manifest is a release artifact created only for an authorized candidate with a
selected bundle version; adopting independent compatibility declarations does not
create a release. No first bundle version is implied by compatibility baseline 1.

An upgrade replaces the previously installed release manifest with the new one;
it must not accumulate stale manifests. Remove only positively identified prior
release metadata within an authorized upgrade, preserving unrelated files. Multiple,
malformed, or inconsistent current manifests block release identity verification.
A new source candidate must remove its superseded manifest from the released tree.
Published tags and release bytes are immutable; corrections use a new release.

## Manifest schema and consistency

The manifest is a UTF-8 JSON object with exactly `version` and `contracts`.
`version` is the selected nonempty SemVer string. `contracts` is an object with
exactly `environment_state` and `specification`, each an object with exactly the
fields shown below. This is a schema illustration, not a release record or a
selected bundle version:

```json
{
  "version": "<selected SemVer>",
  "contracts": {
    "environment_state": {
      "current_state_format_version": 1,
      "supported_state_format_versions": [1]
    },
    "specification": {
      "specification_compatibility_version": 1
    }
  }
}
```

| Manifest entry | Owning declaration within the candidate |
| --- | --- |
| `contracts.environment_state` | `.hai/agents/environment-manager/contract.json` in its entirety |
| `contracts.specification` | `.hai/agents/specification-manager/contract.json` in its entirety |

Reject duplicate JSON keys at any depth, nonstandard numeric constants, extra or
missing schema keys, and malformed values. All version numbers in `contracts`
are positive integers, excluding Booleans. `supported_state_format_versions` is
a nonempty array of unique positive integers including `current_state_format_version`.
The specification declaration contains exactly its positive integer
`specification_compatibility_version`. Baseline 1 is established in each owning
package, independently; future values must come from authorized owner changes,
never from the HAI SemVer number. Tree-root applied markers are strings governed
by specification-manager and are not copied into this manifest.

Release-manager MUST validate both declarations under their owning rules and
compare each manifest entry field for field, including the supported-version
array, against the declaration from the same candidate source. Check filename,
content version, planned tag and asset name together. Repeat these checks on the
verified exact-commit export before packaging and on the unpacked archive before
readiness. Record the checked paths, source commit, values and results. An installed
workspace copy cannot substitute for the candidate's declarations. Missing,
malformed, unsupported or inconsistent metadata blocks dependent compatibility
claims and publication readiness; return the owning dependency through leader,
without changing declarations to make a release pass. No release helper is implied
by this procedure; report which checks were actually performed.

## Version recommendation

Review the actual changes since the last published release, including code,
contracts, behavior, formats, conventions, and governing instructions. Use published
history and source evidence, not commit-message labels alone or the number of edits.
Obtain Git/GitHub evidence through leader's git-manager handoff; do not execute
repository or service operations from this role.
List changed consumer guarantees, impact, relevant verification, and uncertainty.

For an established stable line:

| Impact | Recommended increment |
| --- | --- |
| Existing supported consumers must change because a public guarantee breaks | MAJOR |
| Backward-compatible new capability or public addition | MINOR |
| Backward-compatible correction, including editorial or equivalent procedural clarification | PATCH |

Use the highest applicable impact across the bundle, reset lower components
according to SemVer, and explain why lower increments are insufficient. Public
agent instructions can change observable behavior even when no program code changes.
Do not force a new release merely because a diff exists; report when there is no
releasable change or insufficient evidence to classify it.

With no published baseline, ask for an explicit initial version and maturity
choice. `0.1.0` is an example, not a default. For `0.x`, establish the human's policy
for breaking changes before recommending a numerical result; do not silently apply
either stable-line rules or an arbitrary minor/patch rule. Establish prerelease or
build-metadata handling explicitly if requested, including its relationship to
existing published versions and channels. Reject reuse or regression of a published
version unless an explicitly agreed distinct channel makes the identity unambiguous.

The human selects the version or explicitly authorizes the agent's recommendation.
An existing explicit choice remains authority; report material compatibility
conflicts rather than silently substituting another version.

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

Use existing project checks where applicable, including HAI agent/catalogue,
startup, and specification-helper checks when their affected scope warrants them.
If a check executes Git/GitHub operations, return that execution need to leader;
ordinary filesystem/package checks remain release-manager work.
Read helper documentation and verify the interpreter before execution. Document
unavailable checks; do not call a required blocked check a pass. A local environment
with specification disabled is not itself a bundle-release blocker. Apply the
[contract policy](contract-versioning_conv.md) and [publishing policy](publishing_conv.md)
for the remaining readiness conditions.
