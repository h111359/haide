# Workspace backlog format

## Location and ownership

One backlog root is configured by `location` in the installed Backlog-manager's
external `.hai_env/config/agents/backlog-manager.json`. Missing configuration uses
`backlog`. There is no enable switch. Examples of other locations are
`planning/backlog`, `product/work-queue` and `.hai_env/backlog`.

The root is any safe directory inside the workspace, excluding the workspace root
itself, `.git/`, reusable framework/package paths, configuration, profiles,
instructions and configured Activity/specification stores. Neither ancestors nor
descendants of protected directories are eligible. Core path validation is shared;
the owner additionally reserves the registered Specification-manager's separately
validated content directory. Invalid or unavailable dependent path assurance is a
reported blocker for writes, never permission to assume no collision. Existing
links in the selected root's ancestor chain, `new/`, `closed/`, catalogue or item
paths are rejected; multiply linked item files are also rejected.

The folder layout is:

```text
<location>/
  catalogue.md
  new/
    BL-0001.md
  closed/
    BL-0002.md
  history/                 # predecessors of materially revised items, when needed
```

`new/` contains pending work, including work being investigated or implemented.
`closed/` contains terminal outcomes. `.gitkeep` is an optional empty-folder marker,
not an item. Revision snapshots are historical evidence, not additional live items
and not catalogue entries. Original draft files are audit artifacts in the current
Activity's assigned `files/` directory, outside the backlog; there is no backlog
imports folder. Item and catalogue content does not reference original filenames,
paths or audit copies. Existing foreign files are reported and preserved, not
silently classified or removed.

## Item identity and Markdown

Each live item is a regular UTF-8 Markdown file named `<ID>.md`. IDs have form
`BL-0001`, using at least four digits; allocate the next integer above the largest
ID in both folders. IDs stay fixed when titles, status, requirements or location
change. Duplicate numeric identities with different zero padding are invalid.

An item starts with `# <ID> — <short title>` and exactly one metadata table:

```markdown
# BL-0001 — Short title

| Field | Value |
| --- | --- |
| ID | BL-0001 |
| Status | pending |
| Created | 2026-11-06T05:00:00Z |
| Updated | 2026-11-06T05:00:00Z |
| Closed | — |
| Activities | — |
| Source | User request, 2026-11-06 |

## What

Requested behavior and scope.

## Why

Reason for the requested change.

## Acceptance Criteria

Observable acceptance criteria, or an explicit statement that none were supplied.

## History

- 2026-11-06T05:00:00Z — Created from the attributed user request.
```

Table fields shown above are required and unique; unknown metadata is preserved
and reported separately rather than discarded. Literal pipes inside titles or
table values use `&#124;`. Each required section occurs once and has nonblank
content. Missing source details are represented by an explicit unspecified marker,
not guessed requirements or a claim of approval. Imported historical wording can
refer to retired roles; it stays attributable and does not become current policy.

`Created` is a UTC timestamp for a new item. For imports, an original label such
as `20261029_0554` is retained with its unknown timezone stated; date-only sources
retain date-only precision. `Updated` and terminal `Closed` use actual UTC
`YYYY-MM-DDTHH:MM:SSZ` timestamps. Import time is recorded in History and never
pretends to be the original creation time. Activities contains stable UUIDs and
current known paths when supplied, or `—` before assignment. Paths alone do not
replace identity. Source describes the original request, draft heading or other
attributable evidence without linking to the original file or its audit copy.
Each item contains its complete requirements; reading or auditing it never needs
the original draft. Original-file fingerprints, preservation paths and import-to-ID
mapping belong only in the assigned Activity's audit records.

## Status and transitions

| Status | Folder | Closure information |
| --- | --- | --- |
| `pending` | `new/` | Closed is `—`; implementation is not acceptance. |
| `completed` | `closed/` | Actual closure time and acceptance evidence. |
| `cancelled` | `closed/` | Actual closure time, authorized cancellation and reason. |
| `rejected` | `closed/` | Actual closure time, authorized rejection and reason. |

Terminal items include `## Resolution` with the decision source, reason and
evidence, plus linked Activity IDs when available. Completion records the outcome
against each supplied acceptance criterion and leaves unverified claims explicit.
Absent acceptance criteria require an explicit completion decision; the agent does
not create criteria after the fact to justify completion.

Reopening is an explicitly requested move back to `new/` with the same ID, status
`pending` and Closed `—`. The earlier Resolution and history remain, labelled as
the earlier outcome; reopening adds the new decision and reason. Ordinary edits
do not erase prior closure or reopen an item. Merely implementing a related new
request, closing an Activity or finding similar existing work does not authorize
automatically closing imported proposals.

Material requirement revisions retain exact previous bytes at an unused
`history/<ID>/<UTC-stamp>-<sequence>.md` before change. History records actual
author/source, old/new status, reason, relevant Activity and predecessor path.
Simple metadata edits and moves retain history without making duplicate live items.
Moves use a no-overwrite destination check and a native atomic no-overwrite move
when available; unavailable safe primitives are reported before a dependent move.

## Catalogue

The root `catalogue.md` contains one table, in ascending numeric ID order:

```markdown
| ID | Title | Status | File |
| --- | --- | --- | --- |
| BL-0001 | Short title | pending | [BL-0001](new/BL-0001.md) |
```

Every live item has exactly one row and every row refers to an existing live item
under this root. Title and status agree with the item. Links are relative, direct
children of the correct status folder, never escaping paths or historical copies.
Catalogue prose can explain import provenance; item bodies remain authoritative.
An inconsistent catalogue is reported before dependent mutations. An explicitly
requested catalogue repair rebuilds only its item table from inspected records,
preserving unrelated prose and reporting records that cannot be validated.

Changing a setting does not move content. Relocation is separately scoped: inspect
both roots, preserve bytes/IDs/history, stop on collisions, verify content and
relative references at the destination, then update the owned location setting.
Neither setting changes nor imports overwrite an existing backlog.
