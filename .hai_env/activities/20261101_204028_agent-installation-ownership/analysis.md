# Agent layout and ownership

Revised 2026-11-01T20:28:22Z from the user's clarified decisions and Leader's returned specialist assessment. The [previous analysis](files/revisions/analysis/20261101_202822_01.md) is preserved exactly. These are design decisions for future changes; current framework behavior has not been modified.

## Settled deployment model

New workspaces receive only self-contained `.hai/`. Its bundled core agents initialize `.hai_env/`. Optional agents are later downloaded individually into `.hai_env/agents/`; the whole `hai_agents_library/` is neither copied nor required at runtime.

## Settled ownership decision

- **Agent-definition-manager** creates and maintains agent definitions and verifies their conformance to conventions. It must not own installation.
- **Environment-manager** installs selected optional packages into the environment.

This replaces the earlier suggestion that first optional installation would require bundling Agent-definition-manager with core or introducing a separate bootstrap installer. Environment-manager is already available in `.hai/`.

## Specialist assessment

Environment-manager can validate staged packages using shared validation tools without invoking an absent Agent-definition-manager, then install them under `.hai_env/agents/`. Shared mechanical validation is distinct from the semantic authoring and conformance-review role. Optional packages can be acquired selectively without the whole source library.

Keep the delivery roles clear: `.hai/agents/` contains bootstrap/core agents; `.hai_env/agents/` contains installed extensions and local agents; `hai_agents_library/` is this repository's reusable-package development/distribution source. All share the same agent-format and configuration conventions. Library membership alone grants no execution permission.

## Open proposal and limits

Installation-related registration could also belong to Environment-manager, under explicit authorization, so one owner handles the package copy and registry entry. This is a proposal, not a user decision.

Creation alone must not silently install or register an agent. Update and removal boundaries have not gained new authorization. No framework changes, moves, implementation plan or implementation start are authorized by this discussion; Activity remains active with analysis complete.
