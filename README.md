# HAI

HAI is a framework for AI-assisted development.

Start with [the startup instructions](.hai/start.md).

- `.hai/` contains the reusable framework: agents, concepts, conventions, and tools.
- `.hai_env/` is the persistent local HAI environment: state, custom instructions, request records, and references. It is initialized separately, with explicit authorization.
- Product implementation remains in the workspace. Specifications may optionally be stored in the environment or at another configured workspace-relative location.

See the [HAI concept](.hai/concepts/hai.md) and [environment concept](.hai/concepts/environment.md) for the boundaries and definitions.
