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
| Specification-manager | Durable product specification; independently portable package. HAI work requires validated enabled specification/root and Activity context. | `agents/specification-manager/` |
| Agent-definition-manager | HAI definition/source maintenance and human-directed copy/validate/register operations; requires compatible core conventions/tools and normal HAI context. | `agents/agent-definition-manager/` |
| Git-manager | Compatible HAI workspace Git/GitHub operations; requires installed core helpers, explicit integration settings and operation-specific recording checks. | `agents/git-manager/` |
| Release-manager | HAI core bundle releases, not generic product release policy; requires installed Git-manager for repository/service work and Environment-manager's state contract. Does not track specification compatibility, library versions or individual agent versions. | `agents/release-manager/` |

The `agents/` depth matches `.hai_env/agents/` so copied relative core/peer paths
retain their meaning. Copy each complete package, never just `SKILL.md`. This
library is currently repository source only: the HAI release allowlist ships core,
license and required documentation, excluding this library and `.hai_env`.

Use the manual human bootstrap and installation/update instructions in the root
`INSTALL.md` when the registered definition owner is absent. Source packages cannot
register themselves; do not ask Leader to invoke them to bootstrap.

Shared changes are made here first; installed snapshots change only after explicit
human approval of their update. Workspace-only installed customizations remain
local unless separately reviewed/promoted to golden source. Stop an update for
local differences or an unknown baseline until the human reviews complete differences
and explicitly chooses replacement, including any unattributed changes. Do not
invent change provenance. Preserve a recoverable prior copy and
replace a validated complete package rather than overlaying files. No automatic
synchronization, updater, agent version or mandatory provenance/state scheme exists.
Core, agent-format and helper compatibility assumptions still require review.

Validate source in a disposable installed layout beside the compatible core and
required peers. Core `agent_tools.py validate` accepts canonical runtime paths only;
the two runtime audits/registries remain unchanged. Verify installed snapshots work
with this library absent and source-only edits leave installed bytes unchanged.
