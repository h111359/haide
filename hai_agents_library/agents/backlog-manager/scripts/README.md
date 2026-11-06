# Backlog audit helper

Requires Python 3.11+ and the standard library, plus the compatible `.hai/` core
beside the installed `.hai_env/` package. Verify an absolute working interpreter
under the core tooling convention. This helper does not install dependencies,
write backlog files/settings, repair catalogues, transition statuses or invoke agents.

From a workspace with the complete installed package:

```text
<absolute-python> -B .hai_env/agents/backlog-manager/scripts/audit_backlog.py --workspace /absolute/workspace
<absolute-python> -B .hai_env/agents/backlog-manager/scripts/audit_backlog.py --workspace /absolute/workspace --location planning/backlog
<absolute-python> -B -m unittest discover -s .hai_env/agents/backlog-manager/scripts -p 'test_*.py'
```

The optional `--location` selects a bounded read-only inspection root; it does not
save settings or override an invalid saved configuration. The helper loads its
adjacent package contract and the fixed `.hai_env/config/agents/backlog-manager.json`
using shared core configuration tools. Missing settings default to `backlog`.
Core reserved paths and the separately validated registered Specification-manager
location are excluded. No `.hai_env/` ancestor is required for the content root.

JSON reports `ok`, `scope`, configuration status, effective location, item summaries,
counts and issues. Exit 0 means supported structural checks passed; exit 1 means
configuration, path, content or consistency findings. Python/CLI setup errors are
not successful audits. The Python API is `audit(workspace, location=None)`.

Checks cover stable numeric identity, exact file/heading ID agreement, duplicate
metadata, required nonempty sections, status/folder/closure consistency, resolution
presence, current timestamps, nonlinked files/directories, unexpected item-folder
entries and exact catalogue rows/order. Unknown item metadata is listed rather
than removed. History is not live work and is not recursively scanned. Original
drafts are Activity audit artifacts, not backlog dependencies or audit inputs.
The audit checks representation, not truthful dates, real acceptance, authority,
complete provenance, material revision history, Activity validity or semantic
equivalence. The agent procedures own those reviews and mutation safety.

Source maintenance runs this complete package as data in a disposable installed
layout beside core, with the source library absent. Runtime instructions and
helpers never use the library as a fallback. Tests use disposable fixtures and
cover arbitrary nested/default roots, saved setting failures, terminal outcomes,
Unicode, read-only behavior, duplicate IDs/fields, stale catalogue, missing fields,
unsafe paths, symlinks and hardlinks. Report skipped OS-dependent checks; one OS
does not establish Windows or macOS verification.
