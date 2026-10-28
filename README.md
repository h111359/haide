# HAI

HAI is a framework for AI-assisted development. Start with [the startup
instructions](.hai/start.md).

This source tree is the **HAI 0.2.0 candidate**, using environment
state format **2**. All substantive HAI work belongs to an Activity, including
brainstorming and analysis. Startup resumes current work; a new chat alone does
not create or close an Activity. Leader coordinates specialists and Activity-manager
maintains records, lifecycle and assigned work.

The first immutable packaged prototype is **0.1.0**, which uses state format **1**.
Its [release notes](release-notes/0.1.0.md) and [preserved manifest](release-notes/0.1.0-manifest.json)
describe that historical bundle. The [0.2.0 candidate notes](release-notes/0.2.0.md)
and [current manifest](.hai/release-0.2.0.json) identify the selected candidate;
publication remains pending. See [installation and upgrade instructions](INSTALL.md) and
[Activity migration notes](release-notes/activity-migration.md).

- `.hai/` contains reusable agents, concepts, conventions and tools.
- `.hai_env/` holds local state, mandatory fixed instructions, Activity records and
  optional local context. State configures mandatory `activities.location` (default
  `.hai_env/activities`), optional specification enabled/location, and optional
  chronicles enabled. Transcripts live under assigned Activities; there is no
  Activity toggle or global chronicles location.
- One current Activity uses `00000000_000000_active`; closed Activities retain stable
  IDs under UTC closure timestamp folders. Material definition/analysis/plan revisions
  preserve history after implementation starts. Completion may be analysis alone.
- Optional chronicles record exact durable-source exchanges in Activity segments.
  Recording starts with subsequent exchanges when enabled, without implicit backfill
  of off periods. Closed records allow attributable supplements and delayed old-source
  synchronization; new substantive work uses a new linked Activity.
- Workspace agent registrations use `.hai_env/agents/catalogue.md` alongside the
  framework catalogue; a missing workspace catalogue means none are registered.
  Specialist definitions declare generic model class and effort; optional local
  profiles resolve supported models. Leader remains the root chat.
- Product code and durable specifications remain in their canonical product locations.
  Activity records link to them rather than becoming product storage.

HAI is distributed under the [MIT license](LICENSE). See the [HAI concept](.hai/concepts/hai.md)
and [environment concept](.hai/concepts/environment.md) for detailed boundaries.
