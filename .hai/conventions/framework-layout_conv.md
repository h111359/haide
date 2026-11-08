# Framework layout

`.hai/` contains the reusable Python runtime in `tools/`, shared concepts in `concepts/`, conventions in `conventions/`, state contract in `contracts/state.json`, and initialization defaults in `templates/state.json`. `.hai/start.md` is the host entry instruction. `.hai_env/` contains workspace-specific state, fixed instructions, Activity records, optional installed extensions and their settings. Upgrades must preserve workspace data and follow the [state convention](state_conv.md).

Optional workspace agent packages live at `.hai_env/agents/<name>/` and their explicit registration catalogue at `.hai_env/agents/catalogue.md`. Their reusable source packages under `hai_agents_library/agents/` are data, not a runtime execution origin. A package's settings are stored separately in `.hai_env/config/agents/`; source changes do not automatically replace installed packages. See [agent convention](agent_conv.md) and [agent configuration](agent-configuration_conv.md).

Activity records use the configured store and the shared [Activity convention](activity_conv.md). Core source-backed recording lives in `tools/chronicles/` and runtime; see [chronicles](chronicles_conv.md) and [recording evidence](recording-evidence_conv.md). Explicit source assignment remains the host’s responsibility.
