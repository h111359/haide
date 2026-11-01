# Migrating agent configuration

This change makes configuration declaration a characteristic of every agent. It
retains shared Activity location and chronicles, profiles, fixed instructions,
registration and task permissions. The Git-only stage kept format 2. The subsequent
specification extraction uses current state format 3 with format 2 as read-only
migration context; it does not extract chronicles.

1. Preserve recoverable prior core/optional packages, state and existing saved
   configuration. Inspect both catalogues and package differences. Stop for local
   changes not covered by the approved replacement decision; source edits alone
   never update an installed snapshot.
2. Stage the updated complete core and selected complete optional packages. Every
   agent must declare its package-local `configuration/contract.json`; no-settings
   agents explicitly declare an empty settings map. Run definition, configuration
   and startup checks in that disposable layout. Runtime must work with the source
   library absent. Preserve workspace config bytes outside package replacement.
3. Use Git-manager's explicit migration procedure/helper to extract complete
   `integrations.git` and `integrations.github` subtrees to the version-1 saved
   settings envelope at `.hai_env/config/agents/git-manager.json`. Preserve unknown
   nested values and unrelated state siblings. Verify all effective Booleans and
   the new file before removing only the old owned keys. A saved true switch is
   preserved configuration, not proof of fresh tools/authentication/readiness.
4. Refuse different pre-existing destination values, invalid source/destination
   data, unsafe aliases or changed inspected bytes. Resolve the actual conflict
   before a subsequent explicitly scoped attempt; do not silently merge, reset or
   choose precedence. There is one new authoritative configuration source after
   cutover, without a legacy runtime fallback.
5. Read back the configuration and unchanged core version/feature settings,
   instructions, profiles, registrations and Activity identity/content. Run the
   scoped tests and full authoring audit. Keep exact migration status and backup
   paths as evidence without copying secrets into outputs.

The multi-file operation is not atomic. A failure after destination creation but
before legacy-key removal leaves a reported partial migration, rather than a
successful cutover. Do not automatically retry, delete the destination or roll
back. Recovery needs a reviewed set of compatible prior package/state/config bytes
and a fresh check that restoring them would not overwrite subsequent valid work.
Settings extraction never moves or rewrites Activity/specification/transcript data.

For new environments, absent files use installed contract defaults. No-settings
agents need no saved file; a nonempty settings object for such an agent is invalid.
Invalid/unreadable/unsupported configuration does not silently become defaults.
Configuration errors affect dependent work; independent diagnosis remains possible.
Specification extraction is an explicitly authorized follow-up described below.
Chronicles remains central and has no extraction in this change.

## Specification: format 2 to 3

Use the installed `.hai/tools/startup/migrate_specification_configuration.py` for
read-only `--workspace .` review and explicitly authorized `--workspace . --apply`.
Verify its actual source/destination checks and required contract before apply.
The registered installed Specification-manager must ship configuration contract 2;
source-library presence is insufficient. That optional dependency is specific to
conversion, not fresh format-3 initialization or independent core startup.

The adapter moves complete `features.specification` into owner-file `settings`
under config format 1, including unknown nested values. It preserves false and the
saved root, verifies the destination, then removes only the old feature entry and
sets core version 3. Chronicles enabled/threshold, Activity location, Git config,
profiles, instructions, registries and content stay unchanged. Directory roots are
validated even while disabled, with no directory creation or tree-marker edits.

Conflicting existing destination values, unsafe aliases, invalid source values or
changed inspected inputs stop conversion. Preserve/report backups and partial writes
without claiming atomicity or silently retrying/rolling back. There is no legacy
runtime fallback. After conversion validate separate owner settings and core state;
ordinary setup uses Specification-manager's own configure procedure/helper.
