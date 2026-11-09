# Git-owned configuration helpers

Requires Python 3.11+ and the standard library. Verify and use an absolute working
interpreter per the [tooling convention](../../../../.hai/conventions/tooling_conv.md).
Shared helpers load from `.hai/tools` beside this installed package, never from a
separately supplied target workspace. No helper runs Git, uses credentials,
performs network requests or assesses live readiness.

```text
<absolute-python> -B .hai_env/agents/git-manager/scripts/validate_git_configuration.py --workspace /absolute/workspace
<absolute-python> -B -m unittest discover -s .hai_env/agents/git-manager/scripts -p 'test_*.py'
```

The validator reads the adjacent `configuration/contract.json` and only the fixed
`.hai_env/config/agents/git-manager.json` for saved settings, through shared safe
configuration-path and strict duplicate-free JSON tools. Path safety can inspect
core location metadata; legacy Git settings never supply effective values. Missing
files/leaves use false defaults. An invalid core state does not invalidate an
independent valid or defaulted owner configuration. Unsafe/reserved aliases,
unreadable/malformed envelopes and unsupported versions fail closed. Unknown
stored values are neither changed nor echoed. Git, GitHub and push failures stay
isolated where their supported parent structure permits.

JSON includes `ok`, `configuration_status`, `integrations.git`,
`integrations.github`, `integrations.git.auto_push`, `issues` and
`scope: saved_git_extension_configuration_only`. The `integrations` output grouping
is retained for callers; it is no longer a saved state path. Gate statuses are
`enabled`, `disabled`, `unconfigured`, `invalid` or `unverified`. Push readiness is
always `not_checked`. Exit 0 means supported local checks passed, 1 means isolated
setting failure, and 2 means the envelope/workspace/contract could not be safely
interpreted. No core assurance, instructions, Activity, registration or operation
authority is implied.

## Explicit legacy migration

Only run under explicit migration authority with separately verified supported core
state, instructions and Activity context. Source is fixed `.hai_env/config/state.json`;
destination is fixed `.hai_env/config/agents/git-manager.json`. No implicit scan,
startup migration, fallback or repair occurs.

Supported core versions and complete source-schema validation come from the
installed core contract and `state_context` helper. Extraction supports valid
format-2 legacy state and format-3 state without assuming specification settings
exist in current core state. It preserves the inspected state version and all
unrelated legacy data. Success means only Git settings were extracted; it never
claims that legacy state has been migrated to the current core version. Any core
migration-required result remains a separate environment-owner dependency.

```text
<absolute-python> -B .hai_env/agents/git-manager/scripts/migrate_git_configuration.py --workspace /absolute/workspace
<absolute-python> -B .hai_env/agents/git-manager/scripts/migrate_git_configuration.py --workspace /absolute/workspace --apply --expected-source-sha256 <reviewed-dry-run-hash>
```

Default is read-only dry-run. Review `source_sha256`, destination action and owned
keys before apply. Apply creates exclusive verified backups under
`.hai_env/config/migration-backups/<unique-operation>-*.json`, creates the absent
destination exclusively, verifies complete old/new data and unchanged source,
then replaces state with only owned legacy keys removed. Entire owned objects
including unknown nested values move; state version, unknown root values, sibling
integrations and all other settings remain unchanged. Empty `integrations` remains
an object. No readiness probe is needed for a value-preserving migration.

An existing destination always conflicts unless
`--accept-identical-destination` explicitly resolves it and its complete decoded
envelope equals the candidate. Divergent or extra values are never overwritten.
After any interruption, review actual source/destination/backups and partial
results before an explicitly authorized new attempt. No automatic retry, rollback,
cleanup or source removal occurs on failure. Symlinks in mutation paths are
rejected, even contained ones. Changed inputs stop dependent writes. State
replacement uses a prepared sibling file; a failed operation can leave that file
and reports its path. This is not a multi-file transaction or filesystem lock;
concurrent writers must be coordinated. Backups can contain unknown legacy data;
keep them within the workspace and do not echo their contents.

Migration JSON returns `ok`, mode, source hash, inspected source state version, destination action, migrated keys,
backup paths and completed stages, or an error with partial results when writes
started. Exit 0 means dry-run/apply completed; exit 1 is a validation or operation
failure; argparse usage errors use exit 2. A dry-run is not completed migration.
Independent startup and local configuration checks remain required after apply.

Fixtures use temporary workspaces and no Git/network/credentials/live writes.
They cover defaults, malformed values, independent gates, core independence,
unknown values, strict JSON, Unicode/CRLF, symlinks and reserved aliases,
read-only CLI, complete migration preservation, conflicts, exact destination
resolution, changed inputs, partial failure and retained old authority.
The complete extraction suite runs against both supported core schemas and rejects
unsupported core versions without writes. Report
actual interpreter, OS and skipped checks; portability intent is not cross-OS
verification.
