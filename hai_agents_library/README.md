# Optional HAI agent source library

This is the golden source for complete reusable HAI-compatible optional packages.
It is not a runtime origin, registry or automatic discovery/install mechanism.
Only copied packages under `.hai_env/agents/<name>/` with explicit canonical
workspace registration execute. Ordinary runtime knowledge/helpers/contracts must
resolve to the installed package, installed peers or stable `.hai` core, never
back to this library. Source maintenance, copying, tests/staging and packaging can
read selected source files as data without adopting their roles.

| Package | Intended use and dependencies | Source |
| --- | --- | --- |
| Business-analyst | Business clarification, domain analysis, requirements and acceptance criteria; returns attributable results through Leader. | `agents/business-analyst/` |
| Solution-architect | Technical analysis, architecture, tradeoffs and implementation/verification planning. | `agents/solution-architect/` |
| Software-developer | Authorized implementation and developer checks; requires pre-implementation Activity marker. | `agents/software-developer/` |
| Quality-assurance | Product verification and defect/coverage reporting, separate from Activity/source verification. | `agents/quality-assurance/` |
| Codex Chronicle-manager | Explicit saved Codex source extraction, exact transcripts/checkpoints and operation-bound coverage evidence; core startup never requires this optional package. | `agents/codex-chronicle-manager/` |
| Specification-manager | Durable product specification; independently portable package. HAI work requires its own validated enabled/location file plus separate core/Activity context; standalone roots remain explicit. | `agents/specification-manager/` |
| Agent-definition-manager | HAI definition/source authoring and convention validation; returns metadata for core Environment-manager, which owns installation and runtime catalogues. | `agents/agent-definition-manager/` |
| Git-manager | Compatible HAI workspace Git/GitHub operations; requires installed core helpers, explicit integration settings and operation-specific recording checks. | `agents/git-manager/` |
| Release-manager | HAI core bundle releases, not generic product release policy; requires installed Git-manager for repository/service work and Environment-manager's state contract. Does not track specification compatibility, library versions or individual agent versions. | `agents/release-manager/` |

The `agents/` depth matches `.hai_env/agents/` so copied relative core/peer paths
retain their meaning. Copy each complete package, never just `SKILL.md`. This
library is currently repository source only: the HAI release allowlist ships core,
license and required documentation, excluding this library and `.hai_env`.

Every source package includes `configuration/contract.json` and its SKILL metadata
declaration, even when settings are empty. Copy these with the complete package.
Workspace values at `.hai_env/config/agents/<name>.json` are external: upgrades
preserve them, assess compatibility and report owner migrations without silently
converting settings. Source packages and installation never activate capabilities.

Use core Environment-manager's selective installation/update and registration
procedures through Leader. It already ships in `.hai`, can validate with shared
core tools, and installs the first optional package without Agent-definition-manager
or this whole library. External workspaces need only `.hai` initially; later they
obtain selected individual complete packages from an explicitly chosen source.
No source definition is invoked as an installer or a runtime fallback.

Shared changes are made here first; installed snapshots change only after an explicitly scoped
Environment-manager update approved by the human. Workspace-only installed customizations remain
local unless separately reviewed/promoted to golden source. Stop an update for
local differences or an unknown baseline until the human reviews complete differences
and explicitly chooses replacement, including any unattributed changes. Do not
invent change provenance. Environment-manager preserves a recoverable prior copy and
replaces a validated complete package rather than overlaying files. No automatic
synchronization, updater, agent version or mandatory provenance/state scheme exists.
Core, agent-format and helper compatibility assumptions still require review.

Validate source in a disposable installed layout beside the compatible core and
required peers. Core `agent_tools.py validate` accepts canonical runtime paths only;
the two runtime audits/registries remain unchanged. Verify installed snapshots work
with this library absent and source-only edits leave installed bytes unchanged.
