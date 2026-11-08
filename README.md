# HAI

HAI is a framework for AI-assisted development. Start with [the startup
instructions](.hai/start.md).

Unreleased development adds an [Activity-local agent chat](.hai/conventions/activity-chat_conv.md).
Assigned agents read and append coordination messages through runtime commands;
each Activity retains its own history. This addition is not in the previously
prepared 0.3.0 ZIP.

Unreleased development also adds [per-invocation agent working folders](.hai/conventions/agent-invocation_conv.md).
The host allocates a distinct Activity-local folder before every new spawn and
passes it to the agent. Same-instance follow-ups retain that folder; new spawns
receive new ones. Material remains with its Activity on archival.

Unreleased development adds [Activity usage records](.hai/conventions/activity-usage_conv.md):
source-bounded token snapshots, separately labelled configured-rate credit
estimates and automatic refresh before closure. Missing charges remain unavailable;
account balances and subscription allowances are not treated as Activity spend.

This source tree prepares the **0.3.0 release candidate**,
using current environment state format **3**, with format **2** retained as read-only
specification-migration context. All substantive HAI work belongs to an Activity, including
brainstorming and analysis. Startup resumes current work; a new chat alone does
not create or close an Activity. The host coordinates work and uses the Python runtime for supported environment and Activity operations. Core provides source-backed recording; optional extensions provide domain instructions.

The first immutable packaged prototype is **0.1.0**, which uses state format **1**.
Its [release notes](release-notes/0.1.0.md) and [preserved manifest](https://github.com/h111359/haide/blob/c2a1e9246f21bc1f0ac30abc105fbc17757a6cb6/release-notes/0.1.0-manifest.json)
describe that historical bundle. The [0.2.0 notes](release-notes/0.2.0.md) and
[preserved manifest](https://github.com/h111359/haide/blob/c2a1e9246f21bc1f0ac30abc105fbc17757a6cb6/.hai/release-0.2.0.json) retain that release’s historical
compatibility targets. The [0.3.0 candidate notes](release-notes/0.3.0.md) and
[current manifest](.hai/release-0.3.0.json) describe the selected candidate. Exact source and package verification are recorded
separately from these notes. This source has not been published as 0.3.0. See [installation and upgrade instructions](INSTALL.md) and
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
  synchronization; new substantive work uses a new linked Activity. The host assigns explicit sources and schedules prompt batches. Core synchronizes and verifies enabled or independently mandatory recording before closure; missing or pending required source blocks closure.
- Workspace agent registrations use `.hai_env/agents/catalogue.md`; a missing workspace catalogue means none are registered.
  Specialist definitions declare generic model class and effort; optional local
  profiles resolve supported models. Core operations require no agent profile.
- The optional `business-analyst`, `solution-architect`, `software-developer`, `quality-assurance` definitions are golden packages in `hai_agents_library/agents/`, installed and registered in `.hai_env/agents/`. Missing optional owners are isolated task dependencies; core startup and Activity record discovery remain available.
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
