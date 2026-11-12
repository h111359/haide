# Windows and Linux execution

HAI uses the running Python interpreter's native filesystem APIs. Startup reports
`execution_context` with the OS, `sys.platform`, `os.name`, Python version and
executable. These are observations, not proof of shell availability, filesystem
capabilities or recording readiness. WSL Python reports Linux; Windows Python
reports Windows even when launched from a different shell.

## Paths and safety

Workspace-relative configuration, Activity paths, package snapshot keys, artifact
references and `changed_files` use forward slashes on every OS. Internally derived
native Paths serialize with `.as_posix()`; canonical string parents use
`PurePosixPath`. Requests and saved strings are validated, never silently repaired.
Drive paths, UNC paths, backslashes, traversal, empty components, Windows device
names, control characters, alternate streams and nonportable punctuation cannot
be workspace-relative resource names. Existing incompatible names require explicit
review; startup does not rename them.

Absolute external recording/usage source paths remain native filesystem paths.
Foreign absolute paths retained in historical metadata are not reinterpreted as
paths under the current workspace. They remain unavailable for source reads on
the other OS; this change neither relocates sessions nor waives recording.

Runtime writes reject symbolic links and Windows reparse points, including
junctions on Python 3.11. Protected-path comparisons respect native case semantics.
The cooperative lock and optimistic checks do not constitute an OS security
sandbox or eliminate races against arbitrary external processes.

## Python and shell setup

Use Python 3.11 or newer. Verify a candidate in the actual execution environment
and use the resulting absolute executable. Windows PowerShell example:

```powershell
py -3 -B -c "import sys; print(sys.executable); print(sys.version)"
& 'C:\path\to\python.exe' -B .hai/tools/hai.py startup --workspace .
```

Linux shell example:

```sh
python3 -B -c 'import sys; print(sys.executable); print(sys.version)'
/absolute/path/to/python3 -B .hai/tools/hai.py startup --workspace .
```

An inaccessible application alias, sandbox rejection or failed launcher does not
mean Python is absent. Follow the tooling convention's permitted discovery and
permission mechanisms; never install a runtime implicitly or hardcode another
user's Python path. A canonical request filename passed through the CLI can use
the current shell's native syntax; paths inside its JSON follow their field's
contract.

## Recording and exact bytes

`event_msg` and `response_item` identify host source representations, not operating
systems. If default discovery reports no saved user occurrence, inspect the host
source and explicitly select the supported representation in a workspace request:

```json
{"representation":"response_item"}
```

Pass that request to `recording discover`, then bind the observed actual work
prompt and enabled interval under the existing recording procedure. Do not guess
or merge representations. Startup core validity and recording readiness remain
separate results.

New chronicle filenames use original source start in UTC, with seconds. No IANA
timezone database or third-party timezone package is required. Existing ledger
names remain unchanged. Chat appends and migration raw-byte writes use binary
descriptors so Windows cannot translate LF to CRLF behind exact-byte checks.

The repository's Git attributes disable newline conversion for hashed chronicle
and usage records. They do not repair history already transformed by a checkout.
Overlap inspection validates unrelated archived assignment metadata without
reading or verifying its transcript contents. Related session history and the
selected Activity retain full artifact/checkpoint/source verification. Missing,
changed or malformed required evidence remains a blocker; no automatic adoption,
hash rewriting or history repair occurs.

## Verification

From the workspace, use a verified absolute interpreter:

```text
<absolute-python> -B .hai/tools/run_tests.py --workspace . --work-dir .hai_env/activities/<activity-folder>/files/test-work
```

The runner keeps fixture current directories and temporary outputs under the
supplied workspace-contained test area. It runs all core suites and returns
failure if any suite fails. Symlink tests report unavailable privileges as skips;
native Windows junction tests exercise the separate reparse behavior.

Replace `.hai_env/activities` with the configured `activities.location` when using
another store. Delegated checks use `<store>/<activity>/files/agent-invocations/<id>/test-work`;
both layouts permit nested test directories. CI may use an Activity scaffold.

The repository CI matrix runs Windows and Linux with Python 3.11 and 3.14. A
workflow definition is not evidence of a completed run. Record actual native
platform/version, failures, skips and unrun platforms with each verification.
