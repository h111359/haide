# Optional workspace agents

An optional workspace agent is a reusable set of domain instructions and supporting resources. A registered installed package is discoverable in `.hai_env/agents/catalogue.md`; `hai_agents_library/agents/` contains source packages, not an execution origin. Installing, registering, selecting and authorizing work are separate decisions.

HAI core is a Python runtime, not a built-in agent or role. The host coordinator interprets the user request and decides whether an available extension is appropriate under the host's actual capabilities and permissions. A definition or model profile does not prove that the host can invoke an agent. Core initialization, environment operations and Activity administration do not require optional extensions. The [agent convention](../conventions/agent_conv.md) describes the compatibility format for installed packages.

Each extension may declare its own settings contract and domain knowledge; saved settings remain outside the package and are preserved on replacement. Activity context, source provenance, actual results and unresolved dependencies remain relevant to extensions using those facilities. See [agent configuration](agent-configuration.md) and [Activity](activity.md).
