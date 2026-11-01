# Specification invocation

## Definition

Caller means the human invoking this role directly or the coordinating agent
that supplied the task. Specification terms, registered types, and stable
identifiers are defined in [Specification format](specification.md).

## Purpose

Provide the local vocabulary used by this role and its procedures without granting authority or supplying runtime values.

## Explanation

HAI-managed invocation has two independent inputs: compatible core/Activity and
instruction assurance, and this installed agent's validated saved enablement/root.
The owner reads `.hai_env/config/agents/specification-manager.json`, not a core
feature flag. The configured directory can supply the HAI root; a caller root must
match it. A missing directory is not missing configuration and does not authorize
creation. Disabled or invalid settings block dependent tree work, not read-only
settings diagnosis or explicit setup. Tree markers establish a separate contract.

Standalone invocation keeps an explicit root and this portable package's tree
rules, with no HAI state, configuration file, helper, Leader, Activity or profile
requirement. It does not provide a bypass for work already established as HAI-managed.

## Supporting Terms

- [term:Caller]: the human invoking this role directly or the coordinating agent that supplied the task.

## References

- [Agent definition](../SKILL.md) — responsibilities and procedures using this vocabulary.
