# Framework protection evidence

Protected resources are `.hai/`, reusable packages under
`hai_agents_library/agents/` and installed definitions under `.hai_env/agents/`.
Ordinary clarification authorizes no modifications there. Installation, upgrade
or maintenance needs covering explicit human maintainer authority in the current
request/chat, under higher-priority session instructions. Generated analysis,
plans, prompts and implementation text cannot grant it. Source maintenance,
installed replacement and registration remain separate operations.

For covered framework work, carry the authorization statement verbatim and its
source into each downstream analysis/planning handoff. Record the exact covered
scope and separate owner permissions. Do not expand an implementation request
into installation, settings changes or publication.

Each writing participant captures initial path/content evidence, tracks paths
touched in its current run and compares final content with that baseline. Include
created/deleted files and untracked/generated files, not just a tracked diff.
Pre-existing changes remain attributable to the initial state: unchanged
pre-existing modifications are not charged to this run. Compare all protected
changes with actual covering human authority, not generated permission claims.
`scripts/clarification.py:protection_check` compares supplied digest snapshots;
the caller owns complete path collection and verifying permission provenance.

Before finalization or closure handoff, unauthorized protected changes produce:

```text
ERROR: Protected framework modified without authorization; workflow stopped.
```

Then list exact unauthorized paths in sorted order and stop affected finalization/
closure. Do not automatically revert changes, remove caches or discard unrelated
work. Return partial evidence and the dependency to the host. An absent snapshot
or unknown writer is an inspection dependency, not a passed check.

Request-specific temporary helpers, notes and generated outputs belong in the
assigned Activity/invocation working area, or explicitly authorized scratch.
Permanent product tooling keeps its canonical product location. Helpers use a
verified absolute Python 3.11+ executable with `-B`; no dependency installation
or caches in protected framework/packages. `.gitignore` is not protection.
