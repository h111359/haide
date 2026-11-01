# HAI package contract

## Package contents and identity

The package identity is `dist/hai-<version>.zip`, tied to a verified full source commit. The package is an exact-commit source export, excluding working-tree changes. `dist/` is already ignored in this repository; output still requires current ignore assurance.

The explicit package allowlist is:

- The reusable `.hai/` tree, with exactly one agreed versioned release manifest.
- The repository license and required installation/use documentation from that same commit, with working relative references.

Required reusable `.hai/` content includes every core agent's configuration contract and the shared configuration reader; verify them in the exact export. Workspace settings at `.hai_env/config/agents/` are excluded and never become package defaults.

Excluded content is `.hai_env/` and workspace agents, state, profiles, Activities, specifications and chronicles; `.git/`, credentials, secrets, local configuration, caches, generated output and unrelated workspace material. Release-manager and Git-manager are optional workspace tooling under `.hai_env/` and are both excluded from the reusable `.hai/` bundle.

Archive entries and link behavior must stay within the verified source boundary. Source version, manifest filename/content, intended tag, release identity and asset name agree. A SHA-256 archive digest is external evidence, not a field authenticating the same archive from inside itself.

## References

- [Release policy](release_conv.md) — manifest schema, identity and readiness.
- [Release procedures](../SKILL.md#procedures) — source preparation, packaging, authority, publication and recovery.
