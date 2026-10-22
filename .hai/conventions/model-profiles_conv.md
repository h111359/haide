# Model profiles

## Purpose and location

Agent definitions declare generic capability class and reasoning effort; local
`.hai_env/model_profiles.json` maps classes to concrete runtime model IDs. Leader
remains the root chat using the interface-selected model and effort. Model profiles
are separate from `.hai_env/state.json` and optional-feature flags; they do not
change the core state format version or enable a feature. An absent profile file is
valid environment state, but normal specialist spawning requires configuration.

## Format

UTF-8 JSON with no duplicate property names:

```json
{
  "format_version": 1,
  "models": {
    "light": "gpt-6-luna",
    "standard": "gpt-6.1-sol",
    "advanced": "gpt-6-astra"
  }
}
```

All three classes are required nonblank model-ID strings; this example is local
configuration, not a framework guarantee of availability. `format_version` must
be integer `1`. Preserve unrelated additional properties when updating the file;
unknown properties never grant implicit runtime support. Profile configuration
must resolve inside the workspace, be a readable regular file, and not escape via
symlinks/junctions. Before setup or use, ensure the profile file does not overlap
any configured optional-feature location, including disabled ones. Report a profile
configuration conflict without invalidating previously compatible core state or
overwriting feature content. Do not create it during state-only initialization.

Environment-manager owns profile inspection and explicitly requested setup or
repair. Present existing values and requested changes through chat, preserve
unmentioned settings, validate supported combinations for intended specialists,
recheck inputs before writing, and verify the result. Never infer authorization
to replace a model merely because a runtime no longer advertises it. On partial
failure, preserve files and report completed changes and unresolved issues.

## Resolution

Leader reads the selected definition and resolves its `hai-model-class` through
the profile. Pair that model ID with the definition's `hai-reasoning-effort`.
Before spawning, obtain the current runtime's supported model IDs and per-model
efforts from its tool/API capabilities. Validate the exact pair, including runtime
restrictions on explicit overrides and context forks. Do not treat examples,
prior-session availability, model name similarity, or another model's effort list
as runtime evidence. Profile validity alone does not prove runtime availability.

The shared [agent tools](../tools/agents/README.md) can validate and resolve a pair
using an explicit capability snapshot supplied by the caller; they do not query
runtime support, spawn, or choose fallbacks. If capability evidence is missing or
the pair is unavailable, report the requested role, class, resolved model if known,
effort, and reason. Pause dependent spawning while preserving ordinary leader chat
and independent work. Offer concrete profile setup/repair or a human-selected
supported override; never silently reduce effort or substitute a model.

An explicit human model/effort choice for a particular invocation takes priority
over defaults, must itself be runtime-supported, and is reported as an override.
It changes no declaration or profile unless separately requested. Such an override
can route environment-manager profile repair when the stored mapping is unusable;
configuration errors must not force the human into an unresolvable setup loop.

## Startup bootstrap

Startup must still validate an existing environment or initialize an absent one
with state only when no profile file exists. For this case only, leader may invoke
environment-manager inheriting the root interface's model and effort, explicitly
reporting **inherited startup bootstrap settings** before delegation. This is a
bounded bootstrap exception to specialist defaults, not profile resolution or an
implicit mapping. Limit it to environment validation, state-only initialization,
and returning profile setup status; create no model profiles or optional resources.
Use a runtime-supported inherited-settings spawn without explicit overrides. If
that runtime cannot inherit settings, report the limitation and request an explicit
supported invocation choice. Never guess concrete interface settings.

A present malformed or unsupported profile does not trigger this exception. Report
it and use an explicit human-selected supported override for repair or startup
validation. Other specialists wait for successful resolution or an explicit human
override. Missing profiles never make valid core state invalid; leader reports
profile setup needs alongside the validated environment and available next actions.

## Compatibility

This optional configuration is additive. Preserve existing environments without a
profile, legacy registration data, and optional-feature settings. Agent-format
migration follows [agent_conv.md](agent_conv.md); incompatible core state follows
[state_conv.md](state_conv.md). Do not silently migrate either format, manufacture
missing choices, or lose registrations during a framework upgrade.
