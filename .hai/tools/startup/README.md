# Startup validation

`startup_check.py` is a read-only Python 3.11+ standard-library startup helper.
It shares strict JSON, model-profile schema, agent-name and catalogue-cell decoding
with `../agents/agent_tools.py`. It never installs a runtime, writes files,
initializes state, scans request stores, or parses every registered definition.

Use a working interpreter as described in
[the tooling convention](../../conventions/tooling_conv.md). From the workspace root:

```text
python -B .hai/tools/startup/startup_check.py --workspace .
python -B .hai/tools/startup/test_startup_check.py
```

Use an explicit workspace when running elsewhere. The helper disables bytecode
cache writes before importing shared tools, including when `-B` is omitted. It emits UTF-8
compatible JSON with escaped Unicode and these fields:

- `environment`: `valid`, `absent`, or `invalid`; only `absent` permits routing
  minimal initialization to environment-manager. This command never initializes.
- `compatible_version` and `features`: returned only for validated core state;
  each feature has its validated flag, location, target type, and availability.
- `agent_instructions`: the configured path and exact decoded text only when
  enabled and readable, otherwise `null`. Treat its text as instructions, not as
  a helper-generated conclusion. Independent workspace/session instructions apply.
- `catalogues`: each origin is `valid`, `partial`, `invalid`, `absent` (workspace
  only), or `unverified`. `agents` contains valid independent registration rows
  with decoded selection guides and canonical definition paths. Invalid core state
  prevents workspace registry use; an unreadable framework catalogue prevents safe
  cross-origin collision checks and leaves workspace registrations unverified.
- `profiles`: `absent`, `valid`, `invalid`, or `unverified`, with configured models
  when valid. `feature_conflicts_checked` says whether compatible feature context
  allowed overlap checks. `runtime_availability` is always `not_checked`: the
  leader must resolve the exact selected model/effort against current capabilities
  before spawning. A profile issue does not invalidate otherwise valid core state.
- `issues`: scoped errors; `ok` is true only for valid core state with no issues.

Exit codes: `0` for all applicable checks passing; `1` for absent/invalid state or
isolated catalogue/profile/instruction issues; `2` for fatal workspace/input errors.
Argument-parser errors use argparse usage text and exit `2`. Callers must inspect
`environment`, `issues`, and the independent results rather than treating a nonzero
exit as permission to initialize or repair. Missing Python means the check did not
run, and is never validation success.

Checks include duplicate keys at every JSON depth, nonstandard numeric constants,
required state types and compatibility against the canonical template, legacy
properties, configured paths even for disabled features, target types, reserved
locations, feature collisions and profile overlap. Existing prefixes are resolved
to detect escaping or dangling symlinks/junctions, including absent descendants.
Windows device names and trailing-dot/space aliases are rejected on all systems.
Paths are workspace-relative with `/` separators; Windows comparison follows
native `Path` case handling. References must be readable regular files; startup
opens references only to check access, without reading definition content. Legacy
links, duplicate/conflicting registrations, and isolated malformed rows are reported
and excluded without changing anything. A malformed overall table excludes its
whole origin. Selected-definition format and exact description equality remain
selection/authoring checks in `agent_tools.py`; do not run its full audit at startup.

The helper reads no optional feature contents except enabled configured instructions.
It performs filesystem checks on configured request/specification/chronicles paths
without listing their directories. It does not interpret a saved session source,
synchronize chronicles, check mandatory instructions beyond the supplied context,
or establish runtime support. Results describe a read-only observation, not a
transaction or a persistent cache. Rerun if relevant files/paths change; any later
writer must independently recheck its inputs and containment before writing.

Tests use isolated temporary workspaces, Unicode/CRLF fixtures, isolated CLI
processes, filesystem snapshots, state/profile/catalogue failures, and symlink/
junction fixtures where the OS permits creating them. Report skipped OS-dependent
checks separately; testing on one OS does not establish behavior on another.
