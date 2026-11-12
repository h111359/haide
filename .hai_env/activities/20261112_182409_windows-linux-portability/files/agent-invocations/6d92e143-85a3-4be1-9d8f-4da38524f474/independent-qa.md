# Independent additional portability QA

Environment: native Windows, Python 3.14.7. Assigned Activity 838322f7-62ca-48cf-a12a-7006f90a7709; invocation 6d92e143-85a3-4be1-9d8f-4da38524f474. This assessment tests additional risks beyond the three prior reviews, and does not claim native Linux or Python 3.11 execution.

## Finding: regression runner excludes valid assigned test areas

Severity: moderate (prevents compliant use of the new verification tool in delegated work and workspaces with a custom Activity location; does not demonstrate a product data failure).

The runner at `.hai/tools/run_tests.py:24` requires the fixed prefix `.hai_env/activities/<folder>/files/test-work`. Its documentation literally prescribes that default prefix, so rejection is an intentional restriction in the implementation and its example, not a contradiction of the example itself. However, the invocation convention and this assignment require the assigned agent's fixtures and temporary outputs to remain in its own `files/agent-invocations/<uuid>` folder. These two requirements cannot both be met by that runner. The same hardcoded prefix rejects a configured nondefault `activities.location` even though the Activity convention supports one.

Reproduction from the workspace root, with the specified Python executable:

```text
python -B .hai/tools/run_tests.py --workspace . --work-dir .hai_env/activities/00000000_000000_active/files/agent-invocations/6d92e143-85a3-4be1-9d8f-4da38524f474/test-work --suite chronicles
```

Expected: a safely validated, invocation-owned workspace-contained test directory can be used. Actual: exit 2, `work-dir must be inside an Activity files/test-work directory`, before any suite runs; the directory remains absent. This is independently reproduced by `edge_tests.py`.

`alternate_store_test.py` independently creates an isolated workspace with `activities.location` set to `records/activities`. Public CLI startup returns `valid`, and activity create succeeds at `records/activities/00000000_000000_active`. Running the regression runner with that Activity's `files/test-work` returns exit 2 with the same message, without creating the directory. Thus a valid nondefault store cannot use its actual Activity's test area; a fabricated default-path directory would be outside that Activity's owned area.

## Additional tests

`edge_tests.py`, executed with the absolute Windows Python 3.14.7 executable and `-B`, produced 13 passing assertions and exit 0. These check exact preservation and refusal to read a foreign absolute source path, valid COM0/LPT0/COM10 names, rejection of reserved Windows names and stream syntax, and the runner rejection and absence of fixture writes. `alternate_store_test.py` also passed its reproduction assertions. The runner's rejection is reported as a defect despite the reproducer assertions passing. This is a small targeted set, not a rerun of the existing aggregate or a substitute for the previously executed lifecycle suite. No additional behavior or data-integrity defect was established by these checks.

Prior aggregate and reviewer reports establish Windows-only behavior within their stated coverage; Linux, Python 3.11 and actual CI execution remain unverified. No product files were changed. The session source identity and assignment bounds for this subagent are not available from this handoff; the supplied Activity/invocation IDs do not establish a transcript source or range.
