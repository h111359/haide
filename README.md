# HAI

HAI is a framework for AI-assisted development.

The first packaged prototype is **0.1.0**. See [installation and upgrade
instructions](INSTALL.md), [release notes](release-notes/0.1.0.md), and the
[release manifest](.hai/release-0.1.0.json). HAI is distributed under the
[MIT license](LICENSE).

Start with [the startup instructions](.hai/start.md).

- `.hai/` contains the reusable framework: agents, concepts, conventions, and tools.
- `.hai_env/` is the persistent local HAI environment: state, custom instructions, request records, and references. Startup initializes safely absent core state and the fixed mandatory instructions file while preserving existing material; optional features are configured through chat. Workspace agent registrations live in `.hai_env/agents/catalogue.md`, read together with `.hai/agents/catalogue.md` for role selection. A missing workspace catalogue means no registered workspace agents.
- Specialist definitions use `SKILL.md` frontmatter for generic model class and reasoning effort. Optional `.hai_env/model_profiles.json` maps classes to local model IDs; spawning checks current runtime support. Leader stays in the root chat with the interface settings.
- Product implementation remains in the workspace. Specifications may optionally be stored in the environment or at another configured workspace-relative location.

See the [HAI concept](.hai/concepts/hai.md) and [environment concept](.hai/concepts/environment.md) for the boundaries and definitions.
