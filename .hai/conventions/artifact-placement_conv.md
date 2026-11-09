# Artifact ownership and placement

## Scope and principle

HAI separates the outputs it is asked to deliver or maintain from the material
used to perform and verify a task. This contract applies to all HAI work:
software, documents, research, configuration, flow execution, agent maintenance
and other operations, including artifacts stored through managed tools/services.

An artifact's purpose and ownership determine its destination. A filename,
extension, folder name, or usefulness during implementation does not establish
that it belongs in the delivered product or a reusable package.

## Rules

- **Classification before creation.** Before creating an artifact, the host or assigned agent MUST identify its purpose, owner, intended lifetime and canonical destination using the user's request and applicable project or operational contracts.
- **Deliverable placement.** The host and assigned agents MUST put requested deliverables and maintained reusable resources in their established product, project or operational locations; an Activity folder MUST NOT silently replace an explicitly designated deliverable destination.
- **Working material and evidence.** The host and assigned agents MUST keep task-specific scratch, intermediate drafts, assessments, implementation coverage records, run results, review notes and execution traces with the owning Activity or invocation unless the user or an applicable governing contract explicitly designates another destination.
- **Purpose-based exceptions.** The host and assigned agents MUST treat a report, log, dataset or other task-related artifact as a deliverable when the request or governing contract makes it one; its format or association with a particular task MUST NOT alone classify it as internal working material.
- **Prospective planning.** When planning artifact creation, the planner MUST establish each artifact's classification and destination before prescribing its creation; routine work MAY retain that classification in existing task context rather than generate a separate manifest or empty scaffold.
- **New artifacts during execution.** When execution discovers a need for an unplanned artifact, the executor MUST classify it before creation and return consequential scope or destination conflicts to the host rather than place it beside convenient product files by default.
- **Delivery review.** Before completion, installation, export or publication, the responsible host or agent MUST inspect the actual artifacts and inclusion scope, including generated and untracked material, and resolve misplaced working material or evidence before presenting that scope as ready.
- **Reusable resources.** A reusable resource's author MUST establish a continuing operational, maintenance, documentation or testing purpose beyond the current Activity before adding it to framework, product, flow or agent resources; relevance to the current implementation alone is insufficient.
- **Preservation and relocation.** The host and assigned agents MUST preserve evidence, provenance and existing ownership when correcting placement; a new convention alone MUST NOT authorize moving, deleting or rewriting existing artifacts or expanding cleanup beyond the requested scope.
- **Boundary and permission.** The host and assigned agents MUST apply existing workspace, owner, access and publication permissions to the selected destination; classification, a supplied path or a generated plan MUST NOT grant permission.

## Applying the distinction

| Work | Deliverable or reusable resource | Working material or execution evidence |
| --- | --- | --- |
| Software | Source code, reusable tests/fixtures, maintained documentation | Scratch helpers, test-run output, implementation assessment |
| Flows and operations | Maintained flow definition, explicitly requested operational report | A particular run's diagnostic trace or review notes |
| Research and documents | Requested report, final dataset, maintained template | Intermediate drafts, comparison notes, production checks |
| Framework or agent maintenance | Definitions, procedures, conventions, reusable tooling | Task-specific requirement mappings, reviewer history, recorded test results |

These examples are defaults, not filename rules. A user-requested test report or
an operational audit log with an established storage contract is an output in
its own right. A reusable test definition can belong to the product while the
results of one run remain Activity evidence.

## Ownership, retention and verification

Use validated current Activity context and its `files/` or `results/` locations
for supporting material, with assigned invocation folders for participant work.
Canonical Activity records and managed service records remain with their existing
owners; this convention creates no additional lifecycle or storage root.

Existing project and operational contracts retain their canonical locations and
retention requirements. If an authorized standalone operation has no Activity,
use its explicitly established working/evidence location; do not invent an Activity
or bypass an Activity prerequisite that otherwise applies.

Review each new artifact's intended audience and continued purpose. Ask whether
it belongs to the maintained output or records how the current task was performed.
This is a semantic content review, not a filename blacklist or an automatic
filesystem enforcement claim. Retain original evidence before an authorized move,
verify source/destination contents, and report partial moves without automatic rollback.

## References

- [Activity convention](activity_conv.md) — Activity record and supporting-material ownership.
- [Workspace write boundary](workspace-boundary_conv.md) — file destinations and outside-write permission.
- [Agent convention](agent_conv.md) — shared execution and reusable package review.
- [Tooling convention](tooling_conv.md) — reusable tools versus per-run outputs.
