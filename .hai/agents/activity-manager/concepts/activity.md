# Activity

## Definition

[Activity] is HAI's independent, persistent unit of substantive work. It connects
human intent, discussion and decisions, performed work, verification and an explicit
outcome, whether the result is understanding, a plan, or implemented changes.

## Purpose

Activities organize all substantive HAI work and preserve continuity across chats
without requiring every conversation to become an implementation project.

## Explanation

### Mandatory work context

Brainstorming, advice, analysis, planning, framework maintenance, implementation,
and verification belong to an Activity. There is no enable/disable flag. Startup
validation, bootstrap/setup needed to establish usable context, and read-only
diagnosis may proceed before a usable Activity context exists. They do not exempt
subsequent substantive work. Leader coordinates specialists; Activity-manager owns
records and lifecycle, and performs only assigned work within its scope.

The environment supplies `activities.location`, default `.hai_env/activities`.
Each Activity occupies one direct child folder. At most one is active, always at
`00000000_000000_active`. Its state identifies current work; there is no collection
state or external current pointer. A stable `activity_id` survives archive renames.
All previous Activities are closed under UTC closure timestamp folders.

Startup resumes a valid current Activity. A new chat alone creates none. Meaningful
new work with no current record creates one under that work's authority; existing
unrelated current work requires leader to resolve the boundary with the human.
No role silently closes or replaces current work. A new substantive continuation
of a closed subject uses a new Activity linked by stable ID and archive path.

### Lifecycle, work, and outcome

Lifecycle is `active` or `closed`. Clarification, analysis, planning,
implementation and verification are independently tracked performed steps, not a
mandatory waterfall or lifecycle states. An Activity may complete brainstorming,
comparison, advice, or analysis without implementing anything. A step is completed
only when its own evidence supports that result. Closure outcome is separately
`completed`, `cancelled`, or `stopped`; closure never implies implementation success.

Definitions, analyses and plans can change even after implementation begins.
Material prior versions and their provenance are preserved, with the reason and
impact of revisions recorded. Dependent work and checks are reassessed rather than
left falsely completed. Closure is an explicit authorized boundary, not the end
of a chat turn or the completion of one assigned specialist task.

### Artifacts and product locations

Mandatory artifacts are state, preserved input and action log. Meaningful decisions,
definition, analysis, plan and outcome artifacts are created when needed. Supporting
`files/`, `questionnaires/`, `results/` and `chronicles/` are likewise created only
when useful. Product code and durable specification stay in their canonical product
locations, linked from Activity records rather than relocated into the Activity.

Chronicles are optional exact-source transcript segments stored within the Activity.
One chat may span several Activities, and one Activity may span several chats or
segments of the same chat. Leader assigns exchanges to Activities and resolves
ambiguous boundaries; chronicles-manager applies and verifies them without creating
or closing Activities. Enabling recording covers subsequent exchanges, without
implicit backfill of periods when it was off. Missing durable source is reported,
never reconstructed from memory. Closed Activities allow attributable dated
supplements and delayed synchronization of completed source exchanges without
reopening substantive work.

## Supporting Terms

- [activity_id]: stable unique identity retained through revisions, archival and supplements.
- [current Activity]: the sole active work record at the fixed current folder.
- [supplement]: dated attributable additional evidence attached to a closed record without performing new substantive work under that identity.

## References

- [Activity convention](../conventions/activity_conv.md): canonical artifacts, state schema, revisions, storage and closure.
- [Activity-manager](../SKILL.md): discovery, record and assigned-work procedures.
- [Environment](../../../concepts/environment.md): mandatory configuration and optional features.
- [Chronicles-manager](../../chronicles-manager/SKILL.md): exact-source recording and segment verification.
