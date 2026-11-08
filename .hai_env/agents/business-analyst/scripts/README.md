# Business-analyst helpers

Python 3.11+ standard library only, on Windows, Linux and macOS. Verify a working
absolute interpreter and use `-B`; no implicit installations or generated caches.
Helpers prepare/validate data, never persist Activity records or invoke agents.
Source-package helpers are maintained and tested as data; execution selects only
registered installed packages. No new configurable values are introduced: the
existing empty format-1 contract and saved empty/default configuration remain
compatible. Core Activity location/recording and Specification-manager settings
remain with their owners.

## Registry diagnostic CLI

For the installed version, from the workspace root:

```text
<absolute-python-executable> -B .hai_env/agents/business-analyst/scripts/context_registry.py --workspace . --document product/context.md --activity-store .hai_env/activities
```

Pass the real supplied primary document and validated activities.location; the
store shown is an example. This read-only command reads only that primary
document, stats/checks resource availability independently and emits JSON with
ordered entries (`fields`, `resources`, `eligible`, `disposition`, `issues`) and
diagnostics. It never loads resource content, follows prompts, acts on Update,
accesses the network or writes files. Exit 0: supported registry, including no
entries/skipped entries/missing resources; 1: entry field/path errors; 2: primary
read/parse failure. No qualifying extensions is a normal result.

See the [registry contract](../conventions/context-registry.md) for the exact
Markdown subset, warnings, exclusions and semantic selection. Diagnose separately
from context acquisition. The host evaluates relevance, rechecks safe paths and
reads each selected Location/available Convention fully in order, with attribution.
Unreadable/changed sources report the actual dependency. The helper cannot prove
permission, sufficiency or relevance and offers no atomic filesystem snapshot.

## Pure dialogue API

`clarification.py` exposes `read_ledger`, `parse`, `next_ids`, `question_block`,
`display`, `prepare`, `validate`, and `verify_readback`. All return data or raise
`ValueError`/underlying read errors; none writes. See the complete
[dialogue contract](../conventions/clarification-dialogue.md) for event schemas.
`prepare(ledger, activity_id, event)` assigns sequence/Activity identity, validates
IDs and returns exact predecessor plus a canonical event. Supply stable event
IDs, actual author/source/UTC time, and all kind-specific fields. `next_ids`
returns the next batch and first question ID; assign consecutive IDs to every
question in one logical batch. Do not allocate again on retry; recover saved IDs.

The host writes a workspace-contained runtime request in its assigned working area:

```json
{
  "activity_id": "<validated active UUID>",
  "artifacts": [{"name": "decisions.md", "text": "<full prepared candidate>", "reason": "append exact clarification event"}],
  "log": "Saved question batch; display pending exact readback",
  "provenance": {"source": "<actual host/human source>", "reason": "clarification record"}
}
```

Use `activity record --apply` as documented in the dialogue contract. Serialize
the entire exchange, check the predecessor immediately before dispatch, read back
and call `verify_readback` before display/application. Runtime adds its provenance
line; retain it on subsequent appends. Helpers cannot authenticate human identity,
truth of supplied answers, source/session attribution or write serialization.
Malformed/unknown event markers, damaged canonical blocks, reused IDs, wrong
response numbers and invalid revisions fail rather than resetting the ledger.
Missing/empty files return no events without creating a file. `read_ledger`
requires an already host-validated regular canonical Activity path; it also rejects
symlinks. File errors retain their exact path/underlying error for the host report.

`validate` projects latest effective response IDs plus unanswered/unresolved IDs.
The analyst checks semantic mapping completeness and actual human provenance,
including multipart replies; structure alone does not prove an answer's meaning.

## Readiness, proposal and protection APIs

`readiness_items(convention_text)` returns all annotated check IDs while checking
stable initial order and compatible additions. `assess_readiness(items, checks,
blockers=..., exemption=...)` returns pass/fail/exempt. Every item needs
`satisfied: true` and nonblank `evidence`. Optional `basis` is `evidence`,
`assumption` or `deferral`. The latter two additionally require
`resolves_uncertainty: true`, `requires_human_decision: false` and nonblank
`consequences_if_false`. These flags are reviewer assertions, never inferred
approvals. Exemption data supplies `kind` and `reason`, plus
`user_visible_change: false` for `internal_framework_upkeep`, or `urgent`, `clear`
and `single_reversible_change` all true for `urgent_clear_defect`. Existing
blockers still fail an exempt assessment. See the readiness convention for
semantics and required source/revision evidence.

`validate_proposal` checks no unresolved dialogue/blockers, pass/exempt status,
deeper headings and required nonempty proposal sections. It returns a hash and
proposed target status; it never overwrites input or verifies semantic completeness.
`protection_check(before, after, authorized_prefixes)` compares complete path/hash
snapshots, reports sorted unauthorized paths and the exact mandated error, and
never reverts changes. Callers verify that supplied prefixes have actual explicit
human coverage. Supply canonical workspace-relative path keys, including all
untracked/generated/deleted paths and initial pre-existing modifications.

## Verification

From a maintenance workspace (testing source data), use:

```text
<absolute-python-executable> -B -m unittest discover -s hai_agents_library/agents/business-analyst/scripts -p 'test_*.py'
```

Tests use disposable temporary workspaces and real core runtime operations where
not explicitly fault-injected. No optional agents are executed. Package format
validation stages the whole source package in a disposable canonical installed
layout alongside the compatible `.hai/` core; use `packages validate` and selected
`configuration read` there. This does not update the real installed snapshot or
registration. Fixtures do not prove a real human/host exchange, actual product
Activity archival, cross-platform operation, billing or core chronicle coverage.
