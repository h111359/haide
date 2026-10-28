# Activity migration — 0.2.0 candidate

This document describes the [0.2.0 candidate](0.2.0.md) compatibility boundaries.
The human selected this version for release preparation; these notes do not
identify a published release or certify every consumer migration. The published
[0.1.0 notes](0.1.0.md) and [historical manifest](0.1.0-manifest.json) retain their
original state-format and specification targets.

## Breaking changes

- Activity replaces Request as the mandatory unit of work. The framework role is
  `activity-manager`; callers and current framework links must use that role.
- Activity storage is mandatory, with a safely configurable workspace-relative
  `activities.location` defaulting to `.hai_env/activities`. It has no enable
  switch. Existing Request records are not silently reinterpreted as Activity
  records.
- Environment state moves from format `1` to format `2`. The owning declaration
  accepts only `[2]`; format-1 workspaces need an explicitly authorized migration
  before dependent work with the new framework.
- Chronicles remain optional, with transcripts stored under individual
  Activities. The former global chronicles location is not a format-2 setting.
- Durable product specifications remain independent of Activity records. A
  specification task can finish when its requested specification work and
  verification finish; product implementation is not a prerequisite. Activity
  completion must be judged against that Activity's agreed scope and evidence.

## Independent compatibility targets

| Boundary | Published 0.1.0 | 0.2.0 candidate target |
| --- | --- | --- |
| Current environment state format | `1` | `2` |
| Supported environment state formats | `[1]` | `[2]` |
| Specification compatibility | `1` | `1` |

The state declaration is owned by
[environment-manager](../.hai/agents/environment-manager/contract.json); the
specification declaration is owned by
[specification-manager](../.hai/agents/specification-manager/contract.json).
These versions are independent of bundle SemVer. Replacing temporary source
terminology preserves the existing specification obligations, including standalone
use and the distinction between document completion and product implementation;
the compatibility target remains `1`. Any actual change
to its normative obligations requires the owner's separate contract assessment
and transition, even if the specification metadata schema is unchanged.

## Upgrade boundaries

Preserve the existing state, Request records, transcripts, profiles, mandatory
instructions, and unrelated workspace files before preparing a migration. Inspect
their actual paths and contents; neither a framework update nor a version number
authorizes overwriting or relocating them.

An authorized state migration replaces `features.requests` with mandatory
`activities.location`, using the default `.hai_env/activities` or an explicitly
chosen safe workspace-relative mapping. Changing this setting alone does not
move existing records. The migration changes the state version to `2`, retains
the specification configuration, and preserves the chronicles enablement while
removing its global `location`. Retain unrelated state properties and integration
choices, subject to the new schema's validation. Legacy
`compatible_version` metadata remains unsupported and is not another spelling of
either format version.

Record and history migration is separate from schema conversion. For this
workspace the human authorized initializing the first current Activity with all
existing chronicle history and leaving it open. That authorization does not
establish a general automatic migration for other workspaces, nor imply that old
Request lifecycle stages satisfy the new Activity contract. Preserve original
transcript content and ordering, check every migrated file and affected reference,
and report partial operations honestly before dependent work resumes.

Specification enablement, location, tree metadata, and product meaning are not
implicitly changed by an Activity or state migration. Unmarked or incompatible
specifications still require the specification owner's scoped assessment and
explicit migration/adoption approval; do not rewrite their compatibility markers
merely to match a framework update.

## Verification and release status

Local validation of the candidate source completed with 141 tests passed and
3 Windows-only tests skipped: startup/environment checks had 44 passes and
2 skips, agent tools had 57 passes, and specification checks had 40 passes and
1 skip. The registered-agent audit checked 9 agents with no issues, and local
model profiles validated. A local documentation scan checked 189 links across
59 documents with no missing targets; this establishes target existence, not
network reachability or anchor validity. Independent semantic review found no
additional issues.

This workspace's authorized format-2 migration preserved specification disablement
and its configured location, enabled chronicles, enabled Git/GitHub integrations,
and disabled automated push. Its first current Activity was initialized and left
open at migration verification. All 37 historical transcript files, totaling 436,467 bytes, were relocated
to Activity-local storage; file hashes matched both pre-migration evidence and
the recorded source revision. Recording checks also verified completed source
segments; future replies remain outside completed synchronization coverage.
These checks verify this scoped migration, not a general automatic upgrade path.

Windows-specific tests were not executed, and no macOS execution is established.
The skipped tests do not establish cross-platform verification. These source and
workspace checks are separate from exact-release-source and package validation;
the published 0.1.0 test counts describe that historical release only.

The [current 0.2.0 manifest](../.hai/release-0.2.0.json) records the selected
candidate's targets. The historical 0.1.0 manifest remains outside `.hai/` without
changing its bytes. Exact committed-source and package verification remain
separate release-preparation steps, with results recorded outside these source
notes. Commit preparation is authorized; no tag, push, remote draft or publication
is authorized or claimed by these notes.

Under the established experimental `0.x` policy, this breaking state/workflow
change warrants a MINOR increment. The human selected `0.2.0`; that choice does
not authorize public publication.
