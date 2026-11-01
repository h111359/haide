# Git extension configuration

## Ownership and location

This optional workspace extension owns only `integrations.git` and
`integrations.github` in the existing `.hai_env/state.json` envelope. Core startup
preserves unknown data and neither validates nor returns these extension fields.
Their absence does not affect core startup or selection of other registered roles.
Git-manager owns requested setup and scoped repair directly; other-agent needs go
through Leader. State creation, core format migration, features, instructions,
profiles and unrelated extension configuration remain outside this subtree.

## Saved contract

The supported settings are independent Boolean switches, with no location,
credential, remote or branch fields:

```json
{
  "integrations": {
    "git": { "enabled": false, "auto_push": { "enabled": false } },
    "github": { "enabled": false }
  }
}
```

This is an extension example, not a core initialization default or instruction to
write settings. Missing `integrations` or missing entries are valid unconfigured,
disabled settings. A present container must be an object; a present supported
entry must be an object with Boolean `enabled`. An invalid supported entry makes
only that integration unavailable; an invalid shared container makes both
unavailable. Unknown root, container and nested properties remain preserved and
never enable a capability.

`integrations.git.auto_push` is a separate subordinate policy, default false.
A present value must be an object with Boolean `enabled`. Malformed policy blocks
push without disabling valid Git inspection or commits. A true stored push switch
with Git disabled, unconfigured or invalid is unavailable. Git and GitHub switches
remain independent: Git commands against a GitHub remote require Git; service
connector/API/CLI operations require GitHub; operations using both require both.

## Validation evidence

Saved statuses are `enabled`, `disabled`, `unconfigured` or `invalid`; a helper
that cannot safely read the configuration returns `unverified`. Automatic push
always reports live readiness `not_checked`. Saved enablement proves neither
installed tools, credentials, remote write access, branch readiness nor operation
authority. Invalid extension settings block only their dependent operations,
not core environment usability, independent integrations or general diagnosis.

## Ownership boundary

The extension's mutable fields are the three supported `enabled` Booleans under
`integrations.git` and `integrations.github`. The core state-format version, other
core values, unmentioned switches, unknown properties at every level and other
extensions are outside those chosen field changes. Credential material and live
readiness evidence are not configuration fields. Malformed data remains invalid
until an explicitly scoped repair produces a valid owned value.

## References

- [Configure integrations](../procedures/configure-integrations.md) — setup/readiness/write sequence.
- [Operation workflow](../procedures/operate.md) — independent runtime gates and authority.
- [Extension validator](../scripts/README.md) — read-only saved-setting statuses and limits.
- [Core state convention](../../../../.hai/conventions/state_conv.md) — generic envelope, containment and preservation.
