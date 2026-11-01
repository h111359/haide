# Startup validation

`startup_check.py` is a read-only Python 3.11+ standard-library startup helper.
It shares strict JSON, model-profile schema, agent-name and catalogue-cell decoding
with `../agents/agent_tools.py`. It never installs a runtime, writes files,
initializes state, scans Activity stores, or parses every registered definition.

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
- `current_state_format_version`, `state_format_version`, `activities`, and optional `features`: returned only for validated core state. The format contract comes from the installed framework package, independently of the target workspace's `.hai` copy. `activities` reports the mandatory configured store location (default `.hai_env/activities`) and directory availability/type; startup does not enumerate records or discover the current Activity. Specification reports its flag, location, and availability. Chronicles reports its flag and effective `record_every_prompts` threshold; absent thresholds in older format-2 states default to `5`. A present threshold must be a positive JSON integer, including when chronicles is disabled. Transcript paths are derived inside each Activity.
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
required state types and compatibility against the installed state-format contract,
canonical core format-2 template defaults,
legacy request/current-pointer properties and retired `features.agent_instructions`, configured paths, target types,
reserved locations, Activity/specification collisions and profile overlap. Global
chronicles locations are rejected; Activity-local transcript paths are derived and
not scanned. Fixed mandatory instructions are reserved against feature/profile
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

Unknown extension properties are opaque JSON data: startup neither interprets nor
validates their policy and emits no extension capability/status object. Existing
values remain untouched, including values the extension owner may consider invalid.
Core initialization and validation require no optional extension agent or executable.
Extension owners handle their own requested setup, configuration, and tooling.

The helper reads mandatory fixed instructions and no optional feature contents.
It performs filesystem checks on the configured Activity store and specification path
without listing their directories. It does not interpret a saved session source,
synchronize chronicles, check mandatory instructions beyond the supplied context,
or establish runtime support. Results describe a read-only observation, not a
transaction or a persistent cache. Rerun if relevant files/paths change; any later
writer must independently recheck its inputs and containment before writing.

State containing the retired `compatible_version` key is reported incompatible
without migration. An explicitly authorized prototype reset belongs to
environment-manager under the state convention; startup never interprets or rewrites
legacy state. The read-only helper tests nonmutation and diagnostic results, not
manager writes.

Tests use isolated temporary workspaces, Unicode/CRLF fixtures, isolated CLI
processes, filesystem snapshots, state/profile/catalogue failures, and symlink/
junction fixtures where the OS permits creating them. Report skipped OS-dependent
checks separately; testing on one OS does not establish behavior on another.
