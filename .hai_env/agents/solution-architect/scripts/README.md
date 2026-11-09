# Assessment and plan validation

Python 3.11+, standard library only. Verify the absolute interpreter and use `-B`.
The helper performs read-only structural checks on explicit current documents;
it does not run a role, change state, repair text, install dependencies or write
files/caches. Source maintenance tests run in a disposable installed layout.

From the validated workspace root, using a verified interpreter:

```text
<absolute-python> -B .hai_env/agents/solution-architect/scripts/plan_contract.py --workspace . --document <current-plan-path> --kind plan --expected <current-identity-json>
<absolute-python> -B .hai_env/agents/solution-architect/scripts/plan_contract.py --workspace . --document <current-assessment-path> --kind assessment
<absolute-python> -B -m unittest discover -s .hai_env/agents/solution-architect/scripts -p 'test_*.py'
```

`--expected` is optional for draft generation but host execution preflight checks
current identity. It is a duplicate-free JSON object with exact `Activity`,
`Input revision`, `Decision revision` strings; supplied empty/missing values fail.
No latest-file inference, source discovery or automatic revision is performed.

`validate(text, kind='plan', expected=None)` returns `ok`, ordered `issues`, `kind`,
`semantic_verification: not_performed`, and parsed identity/task/acceptance IDs
when available. `safe_file` rejects traversal, outside input, linked ancestors,
nonregular/multiply linked files and Git metadata. File operations never broaden
source-read authority; only pass user-authorized resources.

Supported Markdown is the exact convention form: initial H1, ordered/unique H2
sections, seven ordered H3 phase sections, unique `- Key: value` fields, and
single-line pipe tables with exact headers. Fenced examples are ignored; unclosed
fences/HTML structure, missing rows/fields and unsupported forms produce diagnostics.
Literal pipes in cells use `&#124;`. Plan targets are workspace-relative; outside
operations require a separately authorized host handoff.

Checks include UUID shape, current identity comparison, ready/business gate
fields, phase overview/order, unique task/acceptance IDs, action/detail agreement,
earlier task dependencies, inventory membership and full acceptance mapping.
Assessment checks include section shape and all T1–T6 passed evidence rows.

Exit 0 means structural checks passed, 1 means validation findings (including a
correctly labeled blocked draft), 2 means input/path/read/encoding/JSON/invocation
failure. UTF-8 JSON stdout preserves international text. No tool success proves
truth, permission authenticity, semantic completeness or agent compliance.

Tests require `TMPDIR` explicitly set to an existing directory inside the actual
workspace, so temporary fixture roots and subprocess outputs remain local. Run
tests with `-B`; configure caller-managed output/cache destinations before use.

Contracts: [assessment](../conventions/technical-assessment.md),
[plan](../conventions/implementation-plan_conv.md). Existing plans are not rewritten
automatically to satisfy a new convention.
