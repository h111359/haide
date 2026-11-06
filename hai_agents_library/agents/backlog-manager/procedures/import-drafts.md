# Import drafts

## Description

Convert selected draft sections into individual pending backlog items while preserving original source bytes and source precision.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| [input:workspace_root] | Explicit workspace and current Activity context. | Mandatory | Host coordinator. | Retrieve validated context before dependent writes. |
| [input:sources] | Explicit selected draft paths and section boundaries. | Mandatory | Caller or bounded inspection of caller-selected material. | Ask for the missing source; do not scan unrelated workspace files. |
| [input:authority] | Authorized draft conversion and source-preservation scope. | Mandatory | Caller. | Prepare an import plan without changing records. |
| [input:audit_context] | Current Activity identity, assigned safe audit directory and any relevant earlier import mapping. | Mandatory | Host coordinator. | Retrieve the assigned directory before preserving source material or writing items. |

## Prerequisites

A validated selected backlog root, original readable contained draft files, current Activity and import authority with sole mutation assignment.

## Rules

None.

## Steps

1. Inspect [input:sources] inside [input:workspace_root] without following unsafe links. Record source fingerprints and enumerate draft sections before writes; retain original headings and distinguish creation timestamps from unknown precision/timezones.

2. Compare each section with the relevant import mappings supplied in [input:audit_context] to detect repeated imports. Keep fingerprints, original paths and item-ID mappings in that Activity audit record, not in the backlog. Matching wording alone does not prove duplication. Resolve missing prior mappings or source-boundary conflicts rather than silently importing a second copy.

3. Prepare one pending item per independent supplied draft, using the item contract. Preserve the original What, Why and Acceptance Criteria wording; derive a short descriptive title only where one was absent and record that it was derived. Missing sections are explicitly unspecified. Historical requirements do not become current policy or evidence of implementation.

4. Validate the assigned audit directory from [input:audit_context] against the current Activity, containment and target types. Recheck original source bytes and preserve an exact copy at an unused audit path before changing the original layout. Allocate stable IDs against both live folders and record original fingerprints and item mappings only in the Activity audit record. If a source was already preserved, verify its exact identity instead of overwriting it.

5. Create the pending files and catalogue entries using Maintain items: pass [input:workspace_root] as workspace_root, the authorized conversion scope from [input:authority] as request, and the prepared self-contained sections with descriptive attribution as items. Verify every section maps to an item and every supplied section body remains intact; omit original-file and audit-copy paths from item metadata, history and catalogue prose.

6. After successful item/catalogue readback, remove an aggregate source from its former location only when the caller requested its transformation and the exact predecessor is safely preserved. Report preserved location/hash and all created item IDs. On partial work keep source evidence and report inconsistencies before any new attempt.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| [output:import_result] | Source inventory, preserved bytes/hash, created IDs and catalogue checks. | Every selected draft is attributable to one pending record; no historical completion or missing requirement is invented. |

## References

- [Role rules and references](../SKILL.md) — shared ownership, constraints and required reading.
- [Backlog format](../conventions/backlog_conv.md) — record, catalogue and history contracts; required for this procedure.
- [Audit helper](../scripts/README.md) — required before helper execution.
