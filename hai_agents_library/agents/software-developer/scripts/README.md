# Execution validation

Python 3.11+, standard library only. Use a verified absolute interpreter and `-B`.
This helper validates explicitly supplied host evidence; it does not execute work,
authenticate a human, allocate identities, repair artifacts or change state.

```text
<absolute-python> -B .hai_env/agents/software-developer/scripts/execution_contract.py --workspace . --directive <current-directive-path> --context <host-context-json>
<absolute-python> -B .hai_env/agents/software-developer/scripts/execution_contract.py --workspace . --directive <current-directive-path> --context <host-context-json> --evidence <delivery-evidence-json>
<absolute-python> -B -m unittest discover -s .hai_env/agents/software-developer/scripts -p 'test_*.py'
```

Context and evidence use the exact fields in the [execution contract](../conventions/execution-evidence.md).
JSON must be duplicate-free UTF-8, without NaN/Infinity. Document and JSON inputs
are regular singly linked files inside the workspace, with no linked ancestors,
traversal or Git metadata. Directives are read completely without text normalization.

`preflight(root, directive, context, peer=None)` checks identity, exact directive
hash, submitted authority provenance, actual mode selection, readiness and runtime
start evidence, required dependency status, task/check/acceptance inventories,
planned writes and protected-maintenance evidence. Optional dependencies do not
block. The host checks their actual availability and reports warnings separately.

Existing hard-linked destinations are rejected; inferred protected writes must
appear in the declared maintenance inventory. Direct sections containing only
Markdown placeholder bullets are invalid. Every acceptance criterion requires
mandatory verification coverage and passed mandatory evidence for verified success.
Delivery paths/operations outside the validated inventory require refreshed preflight.

Plan mode loads only the validated installed sibling
`solution-architect/scripts/plan_contract.py`, with no bytecode writes or source
library fallback. The host first validates the selected peer/package and rechecks
its identity before invoking the helper. A missing peer blocks plan validation;
direct mode does not load it. Supplying `peer` is a pure test API, not production
permission to substitute an unvalidated implementation.

`validate_evidence(evidence, context)` checks current assignment identity, all
expected tasks/checks, immutable mandatory flags, required owners, check statuses,
change evidence fields and blocker state. Verified outcomes reject failed/skipped/
unavailable mandatory checks, incomplete tasks or required owner work. Blocked and
partial reports retain actual checks without claiming success.

Both APIs return `ok`, ordered `issues`, and `semantic_verification: not_performed`.
CLI exit 0 is structurally valid submitted evidence, 1 is validation findings,
2 is input/path/read/encoding/JSON/invocation failure. JSON stdout preserves Unicode.
An unavailable plan dependency is a preflight finding, not an input-loader failure.

The host must establish authority authenticity, maintenance scope, complete direct/
indirect path inventory, actual readiness, quality of checks and all task semantics.
A submitted `origin: human` or `passed` is not proof. Neither helper is a sandbox
or filesystem enforcement mechanism. Revalidate changed inputs and retain partial
evidence rather than silently repairing or retrying a failed persistence operation.

Tests require `TMPDIR` set to an existing workspace-local directory and `-B`.
Fixture directories labeled outside are outside only their disposable test root;
they still reside inside the actual workspace. Tests use no network, credentials,
package installation, global configuration or product lifecycle transitions.
