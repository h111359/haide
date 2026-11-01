# Git extension configuration validator

Requires Python 3.11+ and only the standard library plus the adjacent installed
HAI framework's generic `safe_path`, `overlaps`, `readable_file` and duplicate-free
JSON utilities. It does not use core startup integration fields or policy. Verify a
working interpreter per the [tooling convention](../../../../.hai/conventions/tooling_conv.md).
From the workspace root:

```text
python -B .hai_env/agents/git-manager/scripts/validate_git_configuration.py --workspace /absolute/workspace
python -B .hai_env/agents/git-manager/scripts/test_validate_git_configuration.py
```

The validator reads only the fixed safely contained `.hai_env/state.json` in the
explicit existing workspace. It rejects unsafe/reserved aliases, unreadable files,
invalid JSON, duplicate keys and non-object envelopes. It never creates or changes
files, runs Git, uses credentials, performs network requests or assesses readiness.
The generic framework utility modules load from the framework installed beside this
extension, not executable files from a separately supplied target workspace.

JSON contains `ok`, independent `integrations.git`, `integrations.github` and
`integrations.git.auto_push` statuses, `issues`, and `scope` equal to
`saved_git_extension_configuration_only`. Settings are Boolean plus a status of
`enabled`, `disabled`, `unconfigured`, `invalid` or `unverified`; push readiness is
always `not_checked`. Unknown stored values are neither changed nor echoed.
Missing settings mean off/unconfigured; malformed GitHub does not disable valid
Git, and malformed auto-push does not disable valid Git inspection/commits.

Exit 0 means supported saved configuration checks passed; exit 1 reports invalid
extension configuration; exit 2 means the file/workspace could not safely be
interpreted, with statuses unverified. Argument errors use argparse output/exit 2.
The helper does not validate the complete core envelope, mandatory instructions,
Activity context, registration, live tools/authentication or operation authority.
Those independent prerequisites remain in the owning procedures. It implements no
configuration mutation or recovery. Core startup intentionally does not validate
these extension settings.

Fixtures run without Git, network, credentials, site packages or live workspace
writes. They cover independent failures, absent/malformed entries, Boolean type
strictness, unknown-data preservation, push dependency and readiness limits,
Unicode/CRLF, duplicate JSON, safe paths/symlinks and reserved aliases, and read-only
CLI behavior. Symlink checks may skip on unsupported systems; report actual OS,
interpreter and skipped checks. Run fixtures when changing this helper.
