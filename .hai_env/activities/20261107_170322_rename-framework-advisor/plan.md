# BL-0007 rename plan

1. Validate old definition, catalogue, selected settings and new-name collision absence. Preserve exact old package/catalogue bytes and the original backlog item before material revision.
2. Use the existing runtime lock, checked-path/fingerprint writes and native no-overwrite rename helpers for the explicitly authorized workspace-local identity migration. There is no generic CLI rename command; this is a bounded migration, not a new runtime feature. Stop and retain/report partial results if any step fails.
3. Update only the name in the role definition, role actor labels and contract identity; preserve all behavior and unrelated metadata. Synchronize exactly the old registration row to the new path/name, with the same description; run runtime registration for canonical readback.
4. Validate the definition/configuration, audit catalogue, verify startup discovers the new name only and compare exact normalized old/new behavior plus package file inventory. Check active references, preserve historical references and unrelated BL-0003 changes. Record evidence and update pending backlog implementation status; do not commit or close the Activity.


Revision provenance: source: User accepted proposed BL-0007 name and scope: yes, proceed; reason: Begin authorized rename with preserved behavior; reason: Plan scoped workspace-only identity migration and verification; recorded 2026-11-07T16:59:13Z.
