# Git-owned configuration

## Ownership and location

This optional agent owns `.hai_env/config/agents/git-manager.json`. Its adjacent
`configuration/contract.json` declares the three Boolean settings and false
defaults. It uses the shared [configuration convention](../../../../.hai/conventions/agent-configuration_conv.md)
and [configuration tools](../../../../.hai/tools/configuration/README.md).
Core startup neither loads nor returns these settings. Ordinary operations never
read legacy `integrations.git` or `integrations.github` as a settings fallback.
Core usability, instructions, Activity context and operation authority are
independent prerequisites. Other-agent dependencies go through host coordinator.

## Saved contract

```json
{
  "config_format_version": 1,
  "settings": {
    "git": { "enabled": false, "auto_push": { "enabled": false } },
    "github": { "enabled": false }
  }
}
```

An absent file or declared leaf uses the contract's false default. A present
malformed envelope, unsupported configuration version or nonobject `settings`
makes the file unavailable, without falling back to old state. Missing leaves
remain unconfigured/off; malformed present supported containers or Boolean
values are invalid. An invalid GitHub field leaves valid Git usable; malformed
`git.auto_push` blocks push while leaving valid Git inspection and commits usable.
Unknown values never enable capabilities and are preserved on chosen changes.

Git and GitHub switches are independent: Git commands against a GitHub remote
require Git; service connector/API/CLI operations require GitHub; combined
operations require both. A true push switch with Git disabled, unconfigured or
invalid is unavailable. Saved enablement never establishes live readiness.

## Validation evidence

The Git-owned validator reports `enabled`, `disabled`, `unconfigured`, `invalid`
or `unverified` for each gate. `configuration_status` reports `defaulted`,
`configured` or `invalid`. Automatic push readiness always remains `not_checked`.
For compatibility its output groups gates under `integrations`; that is an output
shape, not a saved state location. The shared loader can validate the complete
file separately; the Git validator isolates supported-field failures for the
operation-specific independent gates. No read-only validator mutates files or
assesses tooling, credentials, remote write access, branch readiness or authority.

## Mutation and migration boundary

Ordinary chosen changes affect only `settings.git.enabled`,
`settings.git.auto_push.enabled` and `settings.github.enabled`. Preserve owner-file
unknown root and nested properties, configuration version and all unchosen values.
Core state and sibling owner files remain untouched. Credential material and live
readiness evidence are never configuration values. Malformed data requires
explicit scoped repair before replacement.

An explicitly authorized legacy migration is the sole extraction path from
`.hai_env/state.json`: move complete `integrations.git` and `integrations.github`
objects into the owner's settings, preserving unknown nested values; preserve
every unrelated state value and sibling integration. Keep the state-format
version unchanged. Reject malformed legacy entries rather than repair them.

A dry-run produces the inspected source hash without writes. Apply requires that
hash, verified backups, unchanged source/path identities, safe destination creation
and complete old/new readback before removing the old authoritative keys. Existing
destinations are conflicts by default; explicit acceptance permits only a complete
exactly identical envelope. A partial cutover retains and reports completed writes
and backups. Both old and new data after interruption require reviewed resolution;
never claim migration complete or overwrite/retry automatically. These are guarded
individual writes, not a multi-file transaction. Preserving true Git/true GitHub/
false push needs no remote readiness probe. Newly effective push enablement still
requires its normal explicit choice and fresh readiness checks.

## References

- [Configure integrations](../procedures/configure-integrations.md) — setup, scoped repair and explicit migration.
- [Operation workflow](../procedures/operate.md) — runtime gates and authority.
- [Git helpers](../scripts/README.md) — commands, safety limits and exit codes.
- [Core state convention](../../../../.hai/conventions/state_conv.md) — independent core assurance and legacy-data preservation.
