# Model profiles

Optional `.hai_env/model_profiles.json` maps reusable optional-agent model classes to concrete model IDs. Absence does not invalidate core state, startup or runtime operations. Profile mappings are configuration, not evidence that the current host can invoke a given model or effort. Resolve the selected extension's requirements against current host capabilities and report unsupported combinations without silent substitution.

Profiles are strict JSON with integer `format_version` 1 and a `models` mapping containing nonblank `light`, `standard`, and `advanced` strings. Preserve unknown properties when making an explicitly authorized change. Validate paths, collisions and the complete candidate, recheck inspected inputs before writing, and report partial results. See the [runtime commands](../tools/runtime/README.md) and [agent convention](agent_conv.md).
