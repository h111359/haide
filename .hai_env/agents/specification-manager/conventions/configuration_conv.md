# HAI specification configuration

## Ownership and saved contract

Specification-manager owns `.hai_env/config/agents/specification-manager.json`.
Its package-local `configuration/contract.json` uses configuration contract format
2, independently of the unchanged specification-tree contract at `../contract.json`.
The saved file uses config format 1:

```json
{
  "config_format_version": 1,
  "settings": {
    "enabled": false,
    "location": ".hai_env/specifications"
  }
}
```

Missing files/leaves use these declared defaults. Invalid present data never falls
back to defaults or `state.features.specification`. A location is a nonblank safe
workspace-relative directory; absent directories are valid and existing nonfolders
are invalid. Validate the directory even when disabled. It cannot overlap the
Activity store, `.hai/`, `.git/`, state, instructions, profiles, installed agents,
configuration storage or another declared content root, including aliases.

Core state format 3 owns mandatory Activity location and chronicles only.
Specification-manager's absence, disabled setting or invalid file is an isolated
optional dependency, not invalid core state. Startup can read the one registered
installed contract/config to report that separate status, without loading this
package's scripts or product tree. Core path writers require usable specification
location assurance before changing a potentially conflicting path.

## Validation and setup

The shared loader validates the complete owner settings. The owner helper reports
only known effective settings/provenance and directory availability; unknown values
are preserved and never echoed as settings. Ordinary setup changes only chosen
`enabled`/`location`, retains unchosen values and creates no product directory.
Invalid data needs explicit scoped repair. Read-only diagnosis and configuration
setup do not require enabled product work or an adopted tree.

Tree operations additionally require validated core/Activity context, an enabled
owner setting and a supplied root matching the owner location. Source/version/path
changes invalidate stale assurance. Portable standalone work keeps its explicit
root and requires neither this file nor HAI helpers. HAI work cannot be relabeled
standalone to bypass missing, invalid or disabled settings.

## Compatibility and migration

Environment-manager's explicitly authorized format-2-to-3 adapter extracts the
complete prior `features.specification` object into this file's `settings`, verifies
the destination before removing the old field, and preserves chronicles and every
unrelated setting. This narrow extraction exception grants no ordinary setup or
specification-tree authority. Conflicting pre-existing files, unsafe paths and
changed source bytes stop conversion. Partial results are reported without an
automatic retry or rollback. There is no indefinite old/new precedence or fallback.

Moving configuration does not change specification content rules, compatibility
version 1 or existing root markers. Enabled false remains false; changing storage
is neither enablement nor permission to create/move/adopt a tree.

## References

- [Configure specification](../procedures/configure-specification.md): owner validation/setup workflow.
- [Invocation](../concepts/invocation.md): HAI assurance versus standalone use.
- [Shared configuration](../../../../.hai/conventions/agent-configuration_conv.md): typed contracts, preservation and paths.
