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
  absent state permits routing minimal initialization to runtime;
  initialized missing instructions need scoped repair. This command never initializes.
- `current_state_format_version`, `state_format_version`, `activities`, and `features`: returned only for validated core state. The format contract comes from the installed framework package, independently of the target workspace's `.hai` copy. Format 3 keeps chronicles in core state; Activity location remains mandatory. Chronicles reports its flag and effective `record_every_prompts` threshold; absent thresholds in supported older states default to `5`. A present threshold must be a positive JSON integer, including when chronicles is disabled. Transcript paths are derived inside each Activity.
- `migration_required`: present for valid format-2 state. It reports the required explicit format-2 to format-3 extraction; the legacy specification subtree is validated for safe preservation but is not returned as active configuration.
- `agent_configurations.specification-manager`: an isolated status for the one validly registered installed Specification-manager package. Startup reads its fixed `configuration/contract.json` and saved settings, without parsing the definition or scanning other configurations. Missing registration reports `unavailable`; invalid contract/configuration adds an isolated issue and does not make the core environment invalid. Source packages are never a runtime fallback.
- `instructions_status`: `loaded`, `missing`, or `invalid` for the fixed mandatory
  `.hai_env/agent_instructions.md`, checked before state and independently of its
  validity/version. `agent_instructions` contains that path and exact decoded text
  when readable (including empty text), otherwise `null`. No flag or custom path is
  consulted. Missing is never silently treated as empty. Treat its text as instructions,
  not as a helper-generated conclusion. Higher-priority workspace/session instructions apply.
- `catalogues.workspace`: the optional workspace registry can be `valid`, `partial`, `invalid`, or `absent`. `agents` contains valid independent workspace rows. Registry issues do not invalidate core state.
- `profiles`: `absent`, `valid`, `invalid`, or `unverified`, with configured models
  when valid. `feature_conflicts_checked` says whether compatible feature context
  allowed overlap checks. `runtime_availability` is always `not_checked`: the
  host coordinator must resolve the exact selected model/effort against current capabilities
  before spawning. A profile issue does not invalidate otherwise valid core state.
- `issues`: scoped errors; `ok` requires valid current core state. Optional registry, profile and agent configuration issues remain isolated.

Exit codes: `0` for valid current core state; `1` for absent or invalid core state, missing instructions or migration required; `2` for fatal workspace/input errors. Inspect scoped issues separately.

Checks include duplicate keys at every JSON depth, nonstandard numeric constants,
required state types and compatibility against the installed state-format contract,
canonical core format-3 template defaults,
legacy request/current-pointer properties and retired `features.agent_instructions`, configured paths, target types,
reserved locations (including `.hai_env/config` for agent-owned settings),
Activity/specification-config collisions and profile overlap. The configuration
directory cannot alias the fixed mandatory instructions, core state, profiles,
Activity store, or Specification-manager's configured directory. Global
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

The helper reads mandatory fixed instructions and only the bounded registered
Specification-manager contract/configuration. It performs filesystem checks on the
configured Activity store and Specification-manager directory without listing their
directories. It does not interpret a saved session source,
synchronize chronicles, check mandatory instructions beyond the supplied context,
or establish runtime support. Results describe a read-only observation, not a
transaction or a persistent cache. Rerun if relevant files/paths change; any later
writer must independently recheck its inputs and containment before writing.

State containing the retired `compatible_version` key is reported incompatible
without migration. Startup never rewrites legacy state; format-2 extraction is an
explicit runtime operation documented below. The read-only helper tests
nonmutation and diagnostic results, not manager writes.

## Explicit format-2 specification extraction

Rehearse the migration first, then apply only under the user's explicit request:

```text
<absolute-python-executable> -B .hai/tools/startup/migrate_specification_configuration.py --workspace .
<absolute-python-executable> -B .hai/tools/startup/migrate_specification_configuration.py --workspace . --apply
<absolute-python-executable> -B .hai/tools/startup/test_migrate_specification_configuration.py
```

The migration requires a valid format-2 environment, readable mandatory
instructions, and a registered installed Specification-manager with a compatible
contract. It copies `features.specification` to
`.hai_env/config/agents/specification-manager.json`, changes only the core state
format to 3 and removes that owned feature subtree. It preserves all other state
properties and unknown values in the migrated settings. Before applying, it creates
an exclusive byte-for-byte backup at `.hai_env/state.json.format2-backup`; it then
creates the configuration exclusively and replaces state from a verified candidate.
Existing destinations, backups, candidates, unsafe paths, or changed inputs stop the
operation. A partial result is preserved and reported without automatic retry.

Tests use isolated temporary workspaces, Unicode/CRLF fixtures, isolated CLI
processes, filesystem snapshots, state/profile/catalogue failures, and symlink/
junction fixtures where the OS permits creating them. Report skipped OS-dependent
checks separately; testing on one OS does not establish behavior on another.

## Combined startup context

After verifying the interpreter as above, run the read-only orchestration entry point:

```text
<absolute-python-executable> -B .hai/tools/startup/startup_context.py --workspace .
<absolute-python-executable> -B .hai/tools/startup/test_startup_context.py
```

This returns the startup checks plus `activity_context`, which is `current`, `absent`, `invalid`, or `unverified`. It includes the store, stable ID, path, required state fields and bounded continuity excerpts. Invalid core state leaves discovery unverified. An unsafe or inconsistent store is invalid, never absent. `ok` requires valid core and consistent Activity discovery; optional registration, profile and agent configuration issues remain isolated. No built-in coordinator configuration is loaded.

Discovery checks every direct child for a safe nonlinked folder, duplicate-free
supported Activity state, required readable nonlinked records, safe optional canonical artifacts, unique IDs,
archive naming and closure timestamps, and sole-current consistency. Historical
records are opened only to check access; their content is not loaded except state. It does not initialize, mutate, choose work, validate runtime
model availability, audit all definitions, or establish recording coverage. Results
are observations, not locks; writers independently recheck before mutation.
