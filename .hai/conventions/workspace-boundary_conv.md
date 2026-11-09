# Workspace write boundary

## Scope and principle

HAI work stays inside the validated current workspace by default. This principle
applies in every HAI workspace to the host coordinator, assigned agents, framework
automation and agent-owned tools. Filesystem access and user authorization are
separate: a writable location does not grant permission to use it.

## Rules

- **Workspace writes.** The host, assigned agents and tools MUST keep file creation, modification, deletion and movement inside the validated current workspace unless the user explicitly authorizes the outside location and purpose.
- **Indirect writes.** The host and assigned agents MUST apply the same boundary to tool side effects, temporary files, generated artifacts, logs, caches, test fixtures, dependency installation and cleanup.
- **Destination validation.** Each writer MUST resolve the destination and its existing ancestor links before writing; a workspace-relative path that resolves outside the workspace requires the same explicit user permission as an outside absolute path.
- **No implied permission.** The host, assigned agents and tools MUST NOT treat sandbox writable roots, operating-system temporary directories such as `/tmp`, a tool's default location, or a generated plan as user permission for outside writes.
- **Working material.** The host and assigned agents MUST use the assigned Activity or invocation working area, or another authorized folder inside the workspace, for temporary material and MUST configure controlled tool outputs and caches to respect the boundary before execution.
- **Blocked operations.** IF an operation cannot respect the boundary and covering user permission is absent, the host or assigned agent MUST stop that operation, identify the required outside location and purpose, and request explicit permission before proceeding; independent permitted work MAY continue.
- **Bounded permission.** Each writer MUST keep any authorized outside writes within the location, purpose and operations covered by the actual user instruction; permission for one operation does not authorize unrelated changes or cleanup.
- **Delegation.** The host coordinator MUST pass the validated workspace boundary and any covering outside-write permission to assigned agents; delegation MUST NOT expand that permission.

## Verification and limits

Tool documentation identifies write destinations and controls for temporary files
and caches. Invocation preparation checks those destinations, including indirect
effects. Completion evidence identifies actual outside writes and their covering
user permission, or reports a boundary violation and partial results accurately.

This is a framework instruction contract. Its presence does not establish an
operating-system sandbox or prove that an arbitrary external tool enforces it.
Existing files outside the workspace do not become authorized cleanup targets.

## References

- [Startup](../start.md) — host entry and application of the principle.
- [Agent convention](agent_conv.md) — role execution and delegated assignments.
- [Tooling convention](tooling_conv.md) — tool preparation and fixture placement.
