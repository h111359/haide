# Specification

## Definition

[specification] is durable product documentation organized as a navigable tree
of folders and files. It describes the product's business, technical,
operational, and other relevant aspects, including domain knowledge needed
to understand it.

## Purpose

The specification supports specification-driven product development and lets
humans and AI agents find relevant knowledge without reading unrelated material.

## Explanation

The authoritative tree format, node metadata, balance and identity rules,
classification scopes, leaf-type registry, and content lifecycle live in
[Specification format](../agents/specification-manager/references/specification.md).
Leaf content conventions live in the specification-manager package and are
linked from that registry. These resources are available to all specification
readers; reading them does not require invoking the agent.

[Specification-manager](../agents/specification-manager/SKILL.md) owns durable
specification edits and can also run independently from HAI with an explicitly
supplied specification root and task. Its package contains its procedures,
format knowledge, conventions, and audit helper.

For HAI-managed specification work, leader obtains validated enabled-feature
and location context from environment-manager before handing off the task.
Use `features.specification.location` only when
`features.specification.enabled` is true. Missing, invalid, or incompatible state,
a disabled feature, or a supplied location differing from state requires
environment-manager setup through leader before dependent specification work.
Do not bypass HAI governance by relabeling that work as standalone. This does
not block reading or maintaining the reusable framework itself.

The environment records a location without asserting that content exists or
authorizing tree creation. Requests and other temporary work records remain
outside the specification; promote only durable product knowledge. The
standalone package does not require or manage HAI state or work records.

## Supporting Terms

None.

## References

- `../agents/specification-manager/references/specification.md`: authoritative specification format and leaf-type registry.
- `../agents/specification-manager/SKILL.md`: maintenance procedures and standalone inputs.
- `environment.md`: HAI environment and optional specification feature.
- `../conventions/state_conv.md`: HAI location validation and configuration ownership.
