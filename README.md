# HAI

HAI is a framework for AI-assisted development. Start with [the startup
instructions](.hai/start.md).

This source tree contains **unreleased development beyond the recorded 0.2.0 candidate**,
using current environment state format **3**, with format **2** retained as read-only
specification-migration context. All substantive HAI work belongs to an Activity, including
brainstorming and analysis. Startup resumes current work; a new chat alone does
not create or close an Activity. The host coordinates work and uses the Python runtime for supported environment and Activity operations. Optional extensions provide domain instructions and source-backed recording.

The first immutable packaged prototype is **0.1.0**, which uses state format **1**.
Its [release notes](release-notes/0.1.0.md) and [preserved manifest](release-notes/0.1.0-manifest.json)
describe that historical bundle. The [0.2.0 candidate notes](release-notes/0.2.0.md)
and [preserved candidate manifest](.hai/release-0.2.0.json) identify that recorded
candidate; they do not claim that this later development has been packaged or published. See [installation and upgrade instructions](INSTALL.md) and
[Activity migration notes](release-notes/activity-migration.md).

- `.hai/` contains the Python runtime, shared concepts, conventions and tools.
- `hai_agents_library/agents/` contains optional golden source packages; see the library index at `hai_agents_library/README.md`. Only complete copies installed and registered in `.hai_env/agents/` execute. Source updates do not update installed snapshots; the library is excluded from the current release bundle. External workspaces start with `.hai` only; core runtime later installs selected individual optional packages and owns runtime catalogues, while Agent-definition-manager authors and verifies definitions.
- `.hai_env/` holds local state, mandatory fixed instructions, Activity records and
  optional local context. State configures mandatory `activities.location` (default
  `.hai_env/activities`) and central chronicles enabled/prompt threshold (default five).
  Specification-manager owns its separate enabled/location configuration. Transcripts live under assigned Activities; there is no
  Activity toggle or global chronicles location.
- One current Activity uses `00000000_000000_active`; closed Activities retain stable
  IDs under UTC closure timestamp folders. Material definition/analysis/plan revisions
  preserve history after implementation starts. Completion may be analysis alone.
- Optional chronicles record exact durable-source exchanges in Activity segments.
  Recording starts with subsequent exchanges when enabled, without implicit backfill
  of off periods. Closed records allow attributable supplements and delayed old-source
  synchronization; new substantive work uses a new linked Activity. The host schedules
  ordinary prompt batches and optional Codex Chronicle-manager records them separately from ordinary
  record edits. Mandatory recording requires fresh verified proof before closure;
  optional pending or unavailable recording is reported without claiming coverage.
- Workspace agent registrations use `.hai_env/agents/catalogue.md`; a missing workspace catalogue means none are registered.
  Specialist definitions declare generic model class and effort; optional local
  profiles resolve supported models. Core operations require no agent profile.
- The optional `business-analyst`, `solution-architect`, `software-developer`, `quality-assurance` and `codex-chronicle-manager` definitions are golden packages in `hai_agents_library/agents/`, installed and registered in `.hai_env/agents/`. Missing optional owners are isolated task dependencies; core startup and Activity record discovery remain available.
- Product code and durable specifications remain in their canonical product locations.
  Activity records link to them rather than becoming product storage.

Every agent declares `configuration/contract.json` through SKILL metadata,
including agents with no customizable settings. Saved agent values live outside
packages at `.hai_env/config/agents/<name>.json`; missing files use declared
defaults. Git-manager owns Git/GitHub/auto-push and Specification-manager owns
specification enabled/location there. Activity location and chronicles remain
central in format 3; only specification settings move from prior format 2. See the [configuration standard](.hai/conventions/agent-configuration_conv.md)
and [migration guide](release-notes/agent-configuration-migration.md).

HAI is distributed under the [MIT license](LICENSE). See the [HAI concept](.hai/concepts/hai.md)
and [environment concept](.hai/concepts/environment.md) for detailed boundaries.
