# Activity objective and implementation scope

## Objective

Implement the approved single modular Python runtime in `.hai/`, replacing the built-in Leader and Environment-manager role packaging while preserving existing observable functionality and workspace data.

## Approved direction

- Keep `.hai/start.md` as a small bootstrap.
- Use `.hai/tools/hai.py` as the runtime entry point.
- Move deterministic core work into internal runtime modules; do not retain built-in Leader/Environment-manager as agent roles.
- Update required compatibility references across `.hai/`, installed `.hai_env/agents/`, source `hai_agents_library/agents/`, and documentation.

## Scope and constraints

- Implement the approved architecture across required compatibility consumers; preserve existing `.hai_env` formats, configuration, Activity history, and unrelated work.
- Keep optional external specialist agents behind the runtime/host adapter where supported.
- No commits or releases are authorized.
- The detailed implementation contract is being prepared by Solution-architect; planning is in progress while that contract is completed.

## Revision provenance

This implementation scope supersedes the prior read-only definition, preserved byte-for-byte at `files/revisions/definition/20261105_191137_01.md`. Source: the user's current-chat authorization and the intervening prompts preserved in `input.md`; recorded 2026-11-05T19:11:37Z. The predecessor described analysis-only scope; this revision adds the explicitly authorized implementation scope and its limits.
