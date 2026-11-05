# Activity closure recording gate

`recording_gate.py` uses Python 3.11+ and only the standard library. It performs a
read-only comparison of the core [recording-evidence contract](../../conventions/recording-evidence_conv.md).
It neither invokes an optional owner nor reads session sources, mutates records,
initializes state or authorizes closure. Core startup does not run this tool.

Verify a working absolute interpreter under the tooling convention, then run:

```text
<absolute-python-executable> -B .hai/tools/activities/recording_gate.py /explicit/gate-request.json
<absolute-python-executable> -B .hai/tools/activities/test_recording_gate.py
<absolute-python-executable> -B .hai/tools/activities/test_role_migration.py
```

The request object has `recording_requirement`, `operation`, `evidence`,
`current_sources`, `current_artifacts` and `writers_stopped`. The convention defines
the operation and evidence fields. Current snapshot maps contain actual fresh
SHA-256 hashes independently reread immediately before mutation. The owner validates
the explicit source paths and contained Activity-relative artifact paths first.
For disabled/no-independent-obligation recording only validated requirement flags
are needed; the result is `disabled_no_obligation` without optional dependencies.

Required recording returns `verified` only for exact operation/Activity/cutoff,
enabled intervals, current requirement, complete source, empty gaps/conflicts,
stopped writers and unchanged source/artifact fingerprints. Unknown or changed
inputs return `blocked`. Output contains `ok`, `status`, `issues`; CLI exit codes
are 0 for a passing comparison, 1 for blockers, 2 for unreadable/invalid JSON input.
The Python API is `assess_closure(request)` with the same result shape.

A passing comparison proves neither source coverage, trustworthy supplied input,
actual stopped workers nor permission. host coordinator and the responsible owners must
perform those checks and supply actual fresh evidence. No timestamp alone proves
freshness. Tests exercise changed sources/artifacts, stale operation binding,
missing/partial/uncertain evidence and independent disabled closure.

## Read-only discovery

`discovery.py` provides the internal `discover(workspace, location)` API used by
`../startup/startup_context.py`. The supplied location must come from compatible
validated core state. It checks all direct-child records and returns independent
consistency issues plus bounded, attributed current-record excerpts; see the startup
README for status, limits, invocation and operational boundaries. It performs no
Activity mutation or lifecycle operation.
