# HAI

HAI is a framework for AI-assisted development.

Start with [the startup instructions](.hai/start.md).

- `.hai/` contains the reusable framework: agents, concepts, conventions, and tools.
- `.hai_env/` is the persistent local HAI environment: state, custom instructions, request records, and references. Startup initializes an absent environment with state only; optional features are configured through chat. Workspace agent registrations live in `.hai_env/agents/catalogue.md`, read together with `.hai/agents/catalogue.md` for role selection. A missing workspace catalogue means no registered workspace agents.
- Specialist definitions use `SKILL.md` frontmatter for generic model class and reasoning effort. Optional `.hai_env/model_profiles.json` maps classes to local model IDs; spawning checks current runtime support. Leader stays in the root chat with the interface settings.
- Product implementation remains in the workspace. Specifications may optionally be stored in the environment or at another configured workspace-relative location.

See the [HAI concept](.hai/concepts/hai.md) and [environment concept](.hai/concepts/environment.md) for the boundaries and definitions.
