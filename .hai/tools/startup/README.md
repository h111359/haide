# Startup validation

`startup_check.py` is a read-only Python 3.11+ standard-library startup helper.
It shares strict JSON, model-profile schema, agent-name and catalogue-cell decoding
with `../agents/agent_tools.py`. It never installs a runtime, writes files,
initializes state, scans request stores, or parses every registered definition.

Find and verify a Python 3.11+ interpreter as described in
[the tooling convention](../../conventions/tooling_conv.md). Run the helper with
the verified absolute executable path, from the workspace root:

```text
<absolute-python-executable> -B .hai/tools/startup/startup_check.py --workspace .
<absolute-python-executable> -B .hai/tools/startup/test_startup_check.py
```

On Windows, invoke the absolute path with the shell's normal path quoting (for
example, PowerShell's call operator); on POSIX, quote the executable path as
needed. A failing `python`, `python3`, or `py` command may be an inaccessible
alias or launcher even when Python is installed. Resolve and probe other runtime
candidates, including paths reported by an installed Python launcher or runtime
manager. Run the helper using a verified executable path; do not report Python
absent solely because a command alias or launcher failed. If discovery or launch
is blocked by sandbox policy, use the environment's normal permission or trusted
execution mechanism for a harmless version and `sys.executable` probe, if
available; do not elevate automatically. Recheck the discovered absolute path in
the original execution context before running the helper. If probing and direct
path execution are both blocked there, report a sandbox blocker and that the
helper did not run. Use an explicit workspace when running elsewhere. The helper
disables bytecode cache writes before importing shared tools, including when `-B`
is omitted. It emits UTF-8 compatible JSON with escaped Unicode and these fields:

- `environment`: `valid`, `absent`, or `invalid`; `valid` requires compatible state
  and readable mandatory instructions. `state_status` separately reports core-state
  validity so missing instructions are not mistaken for absent state. Only safely
  absent state permits routing minimal initialization to environment-manager;
  initialized missing instructions need scoped repair. This command never initializes.
- `compatible_version` and the three optional `features`: returned only for validated core state;
  each feature has its validated flag, location, target type, and availability.
- `instructions_status`: `loaded`, `missing`, or `invalid` for the fixed mandatory
  `.hai_env/agent_instructions.md`, checked before state and independently of its
  validity/version. `agent_instructions` contains that path and exact decoded text
  when readable (including empty text), otherwise `null`. No flag or custom path is
  consulted. Missing is never silently treated as empty. Treat its text as instructions,
  not as a helper-generated conclusion. Higher-priority workspace/session instructions apply.
- `catalogues`: each origin is `valid`, `partial`, `invalid`, `absent` (workspace
  only), or `unverified`. `agents` contains valid independent registration rows
  with decoded selection guides and canonical definition paths. Invalid core state
  prevents workspace registry use; an unreadable framework catalogue prevents safe
  cross-origin collision checks and leaves workspace registrations unverified.
  Valid registration results do not bypass unavailable mandatory instructions.
- `profiles`: `absent`, `valid`, `invalid`, or `unverified`, with configured models
  when valid. `feature_conflicts_checked` says whether compatible feature context
  allowed overlap checks. `runtime_availability` is always `not_checked`: the
  leader must resolve the exact selected model/effort against current capabilities
  before spawning. A profile issue does not invalidate otherwise valid core state.
- `issues`: scoped errors; `ok` is true only for valid core state with no issues.

Exit codes: `0` for all applicable checks passing; `1` for absent/invalid state,
unavailable mandatory instructions, or
isolated catalogue/profile/instruction issues; `2` for fatal workspace/input errors.
Argument-parser errors use argparse usage text and exit `2`. Callers must inspect
`environment`, `state_status`, `instructions_status`, `issues`, and independent results rather than treating a nonzero
exit as permission to initialize or repair. Missing Python means the check did not
run, and is never validation success.

Checks include duplicate keys at every JSON depth, nonstandard numeric constants,
required state types and compatibility against the canonical template (version 5),
legacy properties and the retired `features.agent_instructions` setting, configured
paths even for disabled features, target types, reserved locations, feature collisions
and profile overlap. Fixed mandatory instructions are reserved against feature/profile
aliases; actual aliases to state, profiles, framework, or registry are rejected.
Unrelated invalid profile/state paths do not prevent safe canonical instructions
from loading. Existing prefixes are resolved
to detect escaping or dangling symlinks/junctions, including absent descendants.
Windows device names and trailing-dot/space aliases are rejected on all systems.
Paths are workspace-relative with `/` separators; Windows comparison follows
native `Path` case handling. References must be readable regular files; startup
opens references only to check access, without reading definition content. Legacy
links, duplicate/conflicting registrations, and isolated malformed rows are reported
and excluded without changing anything. A malformed overall table excludes its
whole origin. Selected-definition format and exact description equality remain
selection/authoring checks in `agent_tools.py`; do not run its full audit at startup.

The helper reads mandatory fixed instructions and no optional feature contents.
It performs filesystem checks on configured request/specification/chronicles paths
without listing their directories. It does not interpret a saved session source,
synchronize chronicles, check mandatory instructions beyond the supplied context,
or establish runtime support. Results describe a read-only observation, not a
transaction or a persistent cache. Rerun if relevant files/paths change; any later
writer must independently recheck its inputs and containment before writing.

Version-4 state is reported incompatible without migration. Initialization and
explicit version-4 to version-5 migration belong to environment-manager under the
state convention: ensure the mandatory file first, preserve existing/legacy content,
and remove only the retired setting while retaining the three optional features.
The read-only helper tests nonmutation and diagnostic results, not manager writes.

Tests use isolated temporary workspaces, Unicode/CRLF fixtures, isolated CLI
processes, filesystem snapshots, state/profile/catalogue failures, and symlink/
junction fixtures where the OS permits creating them. Report skipped OS-dependent
checks separately; testing on one OS does not establish behavior on another.
