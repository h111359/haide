# HAI monolithic runtime implementation plan

**Status:** Approved implementation direction; detailed technical contract returned by Solution-architect. Implementation has started at the recorded marker; the phases below guide the authorized work. No commit or release is included.

## Plan overview

| Phase | Work | Main result |
| --- | --- | --- |
| 1 | Build the runtime entry, role-independent storage/state contracts and startup/environment/CLI core. | `.hai/tools/hai.py` and modular runtime can validate and manage core environment data without built-in roles or model profiles. |
| 2 | Add Activity lifecycle, packages, recording and host capability operations. | Existing administrative behavior is available through explicit structured CLI commands with truthful limits. |
| 3 | Relocate role-owned docs/contracts and update compatibility consumers. | Framework, installed/source packages, docs and tests use the runtime APIs; built-in Leader/Environment-manager roles are retired. |
| 4 | Run parity and preservation checks, resolve failures, and document unsupported host behavior. | Reviewable evidence that supported existing behavior is retained. |

## Phase 1 — Runtime core

**Purpose:** Replace deterministic startup/environment coordination first, using existing validators as implementation references and preserving their APIs for compatibility.

| Step | Action | Files |
| --- | --- | --- |
| 1.1 | Add the `hai` CLI entry and strict structured request/response handling with provenance, status, issues and changed paths. Mutators preview by default; `--apply` performs writes. | Add `.hai/tools/hai.py` |
| 1.2 | Extract role-independent safe storage and state contracts/templates. | Add `.hai/tools/runtime/storage.py`; add `.hai/contracts/state.json`; add `.hai/templates/state.json` |
| 1.3 | Implement startup, environment initialization/configuration and scoped specification migration operations. | Add `.hai/tools/runtime/startup.py`, `environment.py` |
| 1.4 | Implement profile and configuration read/update commands without role-owned settings as a core prerequisite. | Extend `.hai/tools/runtime/environment.py` and runtime configuration handling |
| 1.5 | Keep existing helper entry points/API behavior as compatibility wrappers while callers migrate. | Existing `.hai/tools/startup/`, `.hai/tools/configuration/` helpers and READMEs |

**Checks:** Reuse existing read-only validators. Preserve absent/invalid/partial distinctions, empty/nonempty/missing instruction behavior, unknown properties, existing environment formats, exclusive writes, safe path checks and explicit partial results. Verify startup/core commands do not require built-in role registration or model-profile availability.

## Phase 2 — Lifecycle, packages, recording and host boundaries

**Purpose:** Add the stateful operations represented by the current role procedures while keeping unavailable host capabilities explicit.

| Step | Action | Files |
| --- | --- | --- |
| 2.1 | Implement Activity discovery/show/create/record/close/supplement and preserve IDs, input, history, revisions and original implementation markers. | Add `.hai/tools/runtime/activities.py` |
| 2.2 | Implement package validate/audit/install/register/resolve operations. | Add `.hai/tools/runtime/packages.py`; preserve optional external-agent support |
| 2.3 | Implement recording status/schedule/assess-closure and honor nonblocking closure when an authoritative source is unavailable, preserving available material and reporting limits. | Add `.hai/tools/runtime/recording.py` |
| 2.4 | Report host capabilities and route supported host operations through an adapter. | Add `.hai/tools/runtime/host.py` |

**Checks:** Exercise safe Activity writes, path containment, locks/collisions, revisions, unknown-property preservation, exact input retention, stale proof and unavailable-source outcomes. Optional source discovery, spawning and unsupported host hooks must return explicit unsupported/unavailable status; no transcript or background capability is assumed.

## Phase 3 — Compatibility and role retirement

**Purpose:** Move consumers only after runtime operations exist, retaining temporary wrappers until each dependency is updated.

| Step | Action | Affected locations |
| --- | --- | --- |
| 3.1 | Move core contracts/docs out of Leader/Environment-manager package ownership. | `.hai/agents/`, `.hai/contracts/`, `.hai/concepts/`, `.hai/conventions/`, `.hai/procedures/` |
| 3.2 | Update installed/source packages to call runtime APIs and remove built-in role/model prerequisites. | `.hai_env/agents/`, `hai_agents_library/agents/` |
| 3.3 | Update fixed-path imports and consumer documentation/tests before removing old paths. | Git-, Specification-, Chronicle-, Release-manager consumers; `.hai/tools/`, READMEs, installation docs and release manifests |
| 3.4 | Retire built-in Leader and Environment-manager role packages after reference and compatibility checks pass. | `.hai/agents/leader/`, `.hai/agents/environment-manager/`, associated catalogue/contract references |

**Checks:** Search for stale role/path/helper references. Ensure source and installed packages remain distinct and existing `.hai_env` configurations, Activities, and unrelated workspace changes are preserved. No commits or releases.

## Phase 4 — Parity, preservation and limits

Run relevant tests and generated work only under the current Activity at `files/test-work/<run-id>/phase-XX/`. Proposed checks include:

- Valid, absent, invalid and partial state; empty, nonempty and missing mandatory instructions.
- Unknown configuration property preservation and exclusive/no-overwrite creation.
- Sole-current consistency, Activity IDs, exact input/history, predecessor revisions and original implementation-start retention.
- Destination collisions, cooperating writer locks, changed bytes and interrupted multi-file writes with explicit partial status.
- Recording occurrences/intervals, stale proof, unavailable source and truthful nonblocking closure.
- Optional external agents without built-in role or model prerequisites.
- Release/export manifests include every runtime dependency.

Do not treat one-file atomic replacement as a multi-file transaction. Keep human/LLM judgments for intent, conflicts and substantive completion. A host adapter is required for spawning, model inventory, events and after-turn continuation. No complete transcript coverage, unavailable saved source, or background hooks may be claimed without actual support and evidence.

## Implementation boundaries

- `.hai/start.md` remains a small bootstrap; `.hai/tools/hai.py` is the single runtime entry.
- Internal modules replace built-in Leader/Environment-manager handoffs; optional external agents may remain behind adapters.
- Preserve existing `.hai_env` data formats and Activity history during migration.
- Use explicit structured requests with provenance. Mutators preview unless `--apply` is supplied.
- Proposed checks are not yet evidence of passing behavior; no tests are claimed by this plan.
