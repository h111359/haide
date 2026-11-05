# Decisions

## Runtime entry and built-in role model — 2026-11-05T19:11:37Z

- Keep `.hai/start.md` as the small bootstrap.
- Put the single modular runtime entry point at `.hai/tools/hai.py`.
- Replace built-in Leader and Environment-manager agent packaging with internal runtime modules.
- Implement the approved runtime architecture and required compatibility updates across `.hai/`, installed `.hai_env/agents/`, source `hai_agents_library/agents/`, and documentation.
- Preserve environment formats, Activity history, configuration, and unrelated work.
- No commits or releases are authorized.

Source: current user chat. The exact intervening prompts and authorization are preserved in `input.md`. Detailed implementation mechanics remain pending the Solution-architect's implementation contract.


## Commit and closure authorization

The user requested: `ok. commit and close the activity`. This authorizes a local commit of the reviewed runtime migration and durable Activity records, and closure of this Activity. Generated Activity-local test workspaces remain local and are ignored. The earlier no-commit scope is superseded for this requested operation. Source: current user chat, recorded 2026-11-05T19:41:53Z.


Revision provenance: source: current user chat; reason: user explicitly requested commit and Activity closure; reason: record the new explicit commit and closure authority while preserving prior scope history; recorded 2026-11-05T19:41:53Z.
