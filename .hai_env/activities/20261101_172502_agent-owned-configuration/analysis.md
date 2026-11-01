# Per-agent configuration design review

Recorded at 2026-11-01T13:31:39Z by Activity-manager from Leader's report of the registered Agent-definition-manager's completed read-only review. This is attributed specialist evidence and a recommendation, not a user-approved design or implementation result.

## Findings

- The state convention already assigns extension-owned subtrees. Git-manager owns `integrations.git` and `integrations.github`, while its `scripts/validate_git_configuration.py:66` reads shared `.hai_env/state.json`.
- Shared JSON storage couples independent owners: malformed shared JSON can block core startup before an individual extension is selected.
- The user's question concerns moving installed agents' configuration out of shared environment state. No implementation or migration was authorized by that question or the subsequent record-creation approval.

## Proposed recommendation

Use optional mutable configuration at `.hai_env/config/agents/<name>.json`, outside installed agent package folders. Each owning agent defines its schema/version, defaults, validation and migrations. Validate owner-specific configuration when that agent is invoked. Agents without configurable settings need no empty configuration file.

Keep a minimal shared core state for Activity and feature coordination. Mandatory instructions, registration and model profiles remain central. This separates agent-specific configuration ownership without claiming every agent can become independent of shared environment context.

Git-manager is a suitable first migration candidate because its integration settings already have a clear owner. Any migration would require explicit authorization, a defined migration procedure, and one authoritative location afterward; this review did not perform or approve that migration.

## Tradeoffs and unresolved work

Benefits: better isolation between owners, safer package upgrades, and reduced conflict between configuration writers. Costs: more configuration files and independently managed schema migrations.

The user has not chosen this design or authorized implementation. Exact naming, schemas, defaults and migration details remain for a subsequent agreed design/implementation scope. No framework/configuration edits or implementation tests were performed. No durable transcript source was supplied and no transcript synchronization was assigned.
