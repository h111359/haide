# Agent configuration

## Definition

Agent configuration is an agent's declared, versioned set of installation-specific
settings. Every agent has a configuration contract, including an explicit empty
contract when it has no customizable settings. A workspace file is needed only
when values are saved; its absence has the contract's declared meaning.

## Purpose

Keep settings with their responsible owner while preserving reusable packages and
workspace choices independently during upgrades.

## Explanation

The installed package supplies the contract and defaults. Workspace values live
outside packages at `.hai_env/config/agents/<agent-name>.json`. Replacing a package
therefore does not replace user settings. A new contract can require assessment or
migration without silently changing existing values. Golden library packages are
source data; runtime contracts come from installed packages.

Ownership is distinct from independence. An agent can depend on shared environment,
Activity, feature or model-profile assurance and another owner's validated result.
Configuration does not register an agent, prove credentials or grant task permission.
An invalid optional configuration affects its dependent work, rather than every
other role. Missing values use declared defaults; malformed values do not become
defaults merely because a caller cannot use them.

Core state remains shared. Activity location and chronicles retain their Environment-manager owner.
Specification-manager owns specification enabled/location separately from core
format 3; format 2 is migration context, not a runtime settings fallback.
Activity checkpoints, transcript coverage and worker progress are working records,
not configuration. Agent configuration contains no credentials or live readiness
claims and does not override fixed instructions or reusable agent rules.

## Supporting Terms

- [term:configuration contract]: package-owned data declaring supported setting names, types, defaults and configuration-format versions.
- [term:workspace configuration]: saved agent-owned settings outside the agent package, interpreted only under its installed contract.

## References

- [Agent configuration convention](../conventions/agent-configuration_conv.md): representation, safe paths and validation.
- [Agent concept](agent.md): ownership, selection and source boundaries.
- [Environment](environment.md): shared setup and continuity.
