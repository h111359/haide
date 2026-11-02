# Decisions and open design choices

Recorded 2026-11-02T06:52:54Z by Activity-manager from the current user follow-up supplied by Leader. Exact wording is in input.md; source timestamp was not supplied.

- User supports a separate Chronicle Manager; `codex-chronicle-manager` is tentative. Final name depends on Codex-specific versus cross-runtime scope.
- User prefers model-profile functionality in Environment-manager.
- Agent-definition-manager recommends keeping package installation/update and registration in Environment-manager; the user requested clarification of this responsibility, not an additional package agent.
- The four execution specialists and consolidation of remaining Activity duties into Environment-manager are proposed architecture, not implementation approval.
- Leader retains orchestration and source/boundary assignment; closure remains separately authorized.

No new agents, merger, configuration change, closure or transcript synchronization is authorized by this planning record.

## 2026-11-02T07:23:45Z — Implementation authorized

The user now explicitly authorizes implementing the discussed architecture and accepted proposed plan. Define business-analyst, solution-architect, software-developer, quality-assurance and codex-chronicle-manager as source packages under hai_agents_library, with runtime installation and registration in .hai_env rather than .hai. Consolidate remaining Activity ownership into Environment-manager and update routing, contracts and references as planned, preserving existing records. This dated authorization supersedes the earlier pending-approval statements; it does not erase their historical accuracy. Closure and transcript synchronization are not part of this record-only assignment.


## 2026-11-02T07:47:46Z — Implementation choices completed

The authorized implementation fixed the Chronicle role name as `codex-chronicle-manager`; placed the five requested role packages in `hai_agents_library/agents/` and their runtime registrations under `.hai_env/agents/`; kept package installation, registration and model profiles with Environment-manager; moved Activity lifecycle/record ownership into Environment-manager; retained Leader as sole orchestrator; and retired Activity-manager after its live consumers were migrated. Git-manager received the reviewed Chronicle-owner update. These are implementation results, not permission to close the Activity or synchronize transcripts.
