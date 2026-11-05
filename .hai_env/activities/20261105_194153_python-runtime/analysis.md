# Read-only architecture analysis: Python runtime and monolithic core

## Attribution and method

This is an attributed synthesis of read-only reviews of the current `.hai/` working tree by the Solution-architect (`gpt-6.1-sol`, high) and Agent-definition-manager (`gpt-6.1-terra`, high). Their review covered the existing Python tools, agent/role procedures, contracts, and references in workspace packages and consumers. No files were changed as part of those reviews.

The Solution-architect's inventory counted **7 production Python modules, 7 test files, 45 Markdown files, and 5 JSON files** under `.hai/`. Existing Python is predominantly read-only. The only substantive writer identified is the scoped format-2 specification extraction operation. Validators are not complete administrative operations: they do not by themselves initialize, write records, install/register packages, acquire transcript sources, or prove host capabilities.

## Recommendation

A **single Python runtime with internal modules** can replace the built-in Leader and Environment-manager packaging without retaining those roles as agents. Keep `.hai_env/` as workspace data, and support optional external specialist agents through a host/runtime adapter where needed. Preserve observable behavior, data integrity, permission boundaries and safety properties; preserving every internal role handoff or procedure-format rule is not necessary.

This is a proposed direction, not an implementation decision or proof of parity. Deterministic workflows can move into Python. Intent interpretation, policy choices, substantive completion judgments and host-dependent behavior still need supplied decisions or supported model/host capabilities.

## Existing functions and replacement candidates

| Existing component | Current behavior | Candidate in one runtime | Boundary |
| --- | --- | --- | --- |
| `startup_check.py` (`check`, instruction/state/catalogue/configuration checks) and `startup_context.py` (`context`) | Loads exact mandatory instructions, validates state/configuration/catalogues/profiles, and returns bounded Activity continuity. | Reuse the checks behind a single startup command; remove the hard-coded Leader configuration dependency when that role is retired. | Preserve independent instruction loading, absent-versus-invalid distinctions, scoped errors and bounded fresh context. |
| `activities/discovery.py` (`discover`, state/file checks, excerpts) | Read-only sole-current Activity, identity, state, path and archive-name discovery. | Extend into explicit Activity creation, log/input updates, supplied-content updates, revisions, step transitions, original implementation-start recording, supplements, outcomes and guarded archival. | Those write operations do not exist merely because discovery or closure-proof comparison exists; each needs explicit input validation, ownership and safe write behavior. |
| `configuration/configuration_tools.py` | Reads typed configuration defaults and checks paths/directories. | Add explicit writers for core settings, preserving unknown properties and unrelated settings. | Core runtime settings need no fictional agent owner. |
| `startup/migrate_specification_configuration.py` | One scoped dry-run/apply format-2 specification extraction, with backups, exclusive targets, rechecks and explicit partial results. | Keep as a single explicit migration operation or factor its proven primitives into runtime internals. | It is not a general migration engine. |
| `agents/agent_tools.py` | Validates the documented definition subset, profile data, and exact catalogue/definition pairs. | Retain only the validation needed for optional external-agent compatibility. | It does not discover host capabilities, spawn agents, install packages or register agents. Built-in catalogue entries and empty Leader/Environment-manager contracts could be retired. |
| Environment-manager role procedures | Prose-led initialization, configuration, profile setup, package staging/install, and registry operations. | Implement explicit Python operations for initialization, configuration, package staging/install, registry updates and scoped migrations. | Source selection, semantic package review and covering authorization remain supplied decisions. |
| `activities/recording_gate.py` | Compares supplied closure proof and snapshot values. | Runtime can own proof acquisition and closure as one workflow, removing the agent handoff. | The gate itself does not acquire a trustworthy source, establish full coverage or prove that writers stopped. |
| Host/transcript integration | Outside core, `codex-chronicle-manager/scripts/read_codex_source.py` parses explicitly supplied supported JSONL. | Add explicit host and recording adapters; implement cadence, occurrence/overlap checks, rendering and freshness checks when real source/events exist. | Source discovery, assignment, coverage verification, scheduling and transcript/checkpoint writing are missing from core. Python cannot invent unavailable transcripts or unsupported background hooks. |

## Work that remains judgment- or host-dependent

Leader intent interpretation, objective conflicts, task decomposition, substantive completion judgments, arbitrary natural-language instruction handling and evaluation of actual evidence remain human/LLM work. The runtime can receive structured commands, decisions and provenance, then enforce transitions. A short host-coordinator contract could replace long built-in role prompts.

Spawning, model inventory, event delivery and after-turn continuation require a supported host adapter. These are not guaranteed by Python code alone and were not validated against host APIs in this review.

## Proposed shape and role retirement

A candidate layout, **not present in the working tree**, is:

- `.hai/hai.py`
- `.hai/runtime/{startup,storage,environment,configuration,activities,packages,recording,host}.py`
- `.hai/contracts/`
- `.hai/templates/`
- `.hai/host-instructions.md`

This keeps one runtime entry point and internal modules without built-in agent roles. Preserve current `.hai_env/` data formats initially, and deliberately move state, Activity and closure contracts out of role-owned folders.

Likely discardable internal mechanisms are the mandatory framework-agent catalogue, internal specialist model lookup for deterministic administration, repeated Leader-to-Environment-manager handoffs, empty role configuration contracts, and role `SKILL.md`/procedure-layout constraints for the core runtime. Keep definition linting and model profiles only where external-agent compatibility needs them. Markdown concepts can remain concise developer/user documentation; they need not be loaded on every turn.

## Preservation requirements and recording policy

A replacement should preserve:

- Exact readable workspace instructions, and absent-versus-invalid state distinctions.
- Isolated errors, unknown configuration properties, strict UTF-8/JSON handling and configured path/alias/reserved-root safety.
- Stable Activity UUIDs, full history, original timestamps, exact user input and predecessor revisions.
- Explicit intent, authority and provenance; no fabricated completion or verification.
- Exclusive creation, no-overwrite behavior, serialized writers, changed-input checks and explicit partial-failure reporting. A one-file atomic replacement does not make a multi-file operation transactional. Locks must coordinate cooperating processes; independent edits still require rechecks.

Recording settings and the user's nonblocking-closure preference are separate. Existing code/prose often requires proof when recording is enabled, but the user explicitly chose closure without blocking on unavailable transcript sources, with available material preserved and limitations reported. That preference is recorded in the closed related Activity `5f99ff6b-793b-475e-b184-8618582598ef` (`.hai_env/activities/20261105_185515_hai-runtime-exploration`); this Activity is separate and does not continue it. A proposed runtime should represent required/optional recording and unavailable-source outcomes explicitly. Missing source cannot be solved by architecture alone, and no complete-coverage claim is warranted without evidence.

## Compatibility and migration impact

Workspace consumers reference Leader/Environment-manager and their Activity paths, including packages under `.hai_env/agents/` and source counterparts under `hai_agents_library/agents/`. The reviews also identified dependencies from:

- Software-developer procedures on the pre-implementation marker.
- Chronicle tools on source, Activity and closure conventions.
- Git-manager commit workflows on verification records and scripts importing fixed `.hai/tools` paths.
- Specification-manager scripts on helper imports and tests on the state template.
- Release-manager on `environment-manager/contract.json` and package contract allowlists.
- README, installation docs, tests and release artifacts on the current layout.

Migrate source and installed packages within their respective authorized scopes; do not delete old paths first. Temporary compatibility wrappers may ease transition. Preserve historical releases as history.

## Suggested sequence and parity checks

1. Put a single CLI over the read-only helpers and relocate contracts, with compatibility wrappers.
2. Implement environment and Activity writes.
3. Implement package and registry operations.
4. Add explicit host and recording adapters.
5. Migrate consumers, then retire built-in roles.

Proposed parity checks, **not run**, cover valid/absent/invalid/partial state; empty/nonempty/missing instructions; unknown-setting preservation; sole-current consistency; input/history/original-marker retention; destination collisions, concurrent creation, changed bytes and interrupted writes; source occurrences, recording intervals, stale proof and truthful unavailable-source status; optional agents without built-in role/model prerequisites; and release exports containing every runtime dependency. No reliable percentage of prompt or quota savings was estimated.

## Limits and status

This was source inspection and architecture review only. No tests, prototype, host API validation, implementation or framework edits were performed. Functionality preservation is a feasible design direction, not demonstrated parity; implementation and the proposed parity checks would be required to establish it. The broader runtime plan from the prior closed Activity is not adopted implicitly.
