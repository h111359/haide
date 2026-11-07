# Agent invocation working folders

## Allocation and identity

Every new sub-agent spawn attempt receives a distinct folder inside its assigned
Activity. A fresh invocation UUID identifies the folder, independently of the
agent's name, model or host handle. Repeated and concurrent same-agent spawns
therefore receive separate folders.

`activity invocation-allocate` takes the stable current `activity_id`, an `agent`
name and provenance. It does not select or authorize a package, invoke agents,
launch processes or discover host capabilities. The caller cannot set the UUID
or destination; the runtime derives:

```text
<Activity>/files/agent-invocations/<invocation-uuid>/
  invocation.json
  <agent-created supporting material>
```

The manifest is strict JSON with exactly these fields:

| Field | Meaning |
| --- | --- |
| `invocation_format_version` | Integer `1`; independent of state, settings and bundle versions. |
| `activity_id` | The containing Activity's stable UUID. |
| `invocation_id` | Fresh canonical UUID for the allocation. |
| `agent` | Caller-supplied lower-case agent name, up to 64 characters. |
| `created_at` | Actual runtime UTC timestamp, `YYYY-MM-DDTHH:MM:SSZ`. |
| `provenance` | Nonblank `source` and `reason` strings. |

The result supplies `allocated`, both IDs, `agent`, workspace-relative `path`,
`activity_relative_path`, `metadata_path` and `metadata`. Preview has `allocated:
false` and creates nothing; its UUID/path is not reserved. Only an applied success
with `allocated: true` supplies a dispatchable folder.

Allocation uses the existing runtime lock and current-Activity checks. Parent
paths reject links, escaping paths and wrong types; directories and the manifest
are created exclusively. Collisions and changed inputs preserve existing material.
Partial failures report retained changed paths, without rollback, reuse or retry.
The manifest proves allocation, never successful launch or authenticated identity.

## Host handoff

The host follows this sequence for every new spawn:

1. Establish task authority, current Activity, installed package settings and
   actual host model/effort capability.
2. Apply allocation for that Activity and agent. Do not dispatch from preview,
   failed or partial results.
3. Supply the existing folder, Activity ID, invocation ID and Activity-relative
   suffix in the initial assignment alongside ordinary task inputs.
4. Associate the actual returned host handle with that allocation in host context
   and an attributable Activity log entry. Record actual launch status.
5. Verify the agent received and used its folder; retain returned work and
   completion/writer-status evidence.

The handoff also returns available usage-source identity and attribution bounds
for the host's [usage update](activity-usage_conv.md), or an explicit unavailable
result. A host handle, model profile or folder alone is not token/billing evidence.

Failed, not-dispatched and uncertain launches retain their allocated folders.
The host resolves uncertain launch status before risking a duplicate worker.
A deliberately new spawn attempt always receives a new allocation. A follow-up
to the same live invocation retains that invocation's folder and IDs; the host
resupplies the same context when needed. Role name alone never identifies an
existing invocation. A new host instance is a new spawn, even for resumed work.

Actual handles and status evidence remain in host context and Activity records;
there is no global invocation registry. `host check` remains read-only capability
validation; core does not provide a host-specific spawning API.

## Agent working material

The agent verifies that its supplied folder exists under the assigned Activity
and that the manifest matches its Activity ID, invocation ID and agent name. A
missing, unsafe or mismatched folder is returned to the host, not silently replaced.
The runtime-owned manifest is not edited by the agent.

Temporary files, logs and concise supporting notes go in this folder. Product
changes still use canonical product paths. Canonical Activity artifacts, lifecycle,
chronicles and shared chat retain their existing owners and operations. No
unnecessary logs or explanations are required.

These are separate folders under existing account permissions, not security
sandboxes. Core does not recursively inspect agent-created work or prevent direct
same-account filesystem edits. Startup/discovery does not eagerly scan invocation
manifests or work files. No new core state setting or migration is required.

## Closure and retention

The runtime lock serializes allocation and archival, not agents' later writes.
Before dispatching closure, the host verifies all relevant invocations have ended
their writes. Running, uncertain or unresolved writers block host closure; a
timeout or allocation manifest alone is not proof that writing stopped.

The host records actual evidence and withholds closure while that condition is
unresolved. Runtime cannot discover or stop host workers itself; direct closure
commands do not enforce external process lifetime.

Archival retains invocation folders and bytes with the Activity. Durable references
use the stable Activity ID plus `activity_relative_path`, resolving the current or
final Activity path. New allocations reject closed/stale Activity IDs. New
Activities inherit no earlier folders or handle bindings.

No cleanup/delete operation is introduced. Material stays with its Activity;
later cleanup needs separate scope.

## References

- [Runtime commands](../tools/runtime/README.md) — invocation and checks.
- [Agent convention](agent_conv.md) — host selection and handoff obligations.
- [Activity convention](activity_conv.md) — record boundaries and archival.
