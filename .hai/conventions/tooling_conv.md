# Tooling convention

## Scope

Implementation details for the Python automation policy in
[HAI](../concepts/hai.md#tools). Applies to framework automation,
including framework and workspace agent-owned scripts; it does not choose
the product's runtime.

## Runtime and dependencies

- Use Python 3.11 or newer and the standard library where practical.
- Document any higher minimum version and any external dependencies,
  their supported versions, and setup commands. Do not install packages
  or runtimes implicitly when a tool runs.
- Identify a working interpreter before execution. Use `python3` on
  Linux/macOS or an available `python`, `py -3`, or explicit interpreter
  path on Windows. A Windows application alias is not proof that a
  working runtime is installed.
- Keep core logic portable across Windows, Linux, and macOS. Use native
  path APIs, explicit text encodings, and documented platform-specific
  handling where filesystem behavior differs. Avoid shell-dependent
  command construction and hardcoded executable locations.

## Placement and usage

- Shared framework tools live under `.hai/tools/`.
- Agent-owned tools live under `.hai/agents/<name>/scripts/`.
- Workspace agent-owned tools live under `.hai_env/agents/<name>/scripts/`
  and follow the same runtime, documentation, and verification rules.
- Use descriptive `snake_case.py` filenames and `test_*.py` test files.
- Keep the owning agent's SKILL.md focused on when to run tools.
  Put detailed arguments, examples, side effects, dependencies, exit
  codes, and parsing or validation limits in the adjacent README.md.
- Document machine-readable output and exit codes for automated callers.
  Use UTF-8 for text files and explicit JSON serialization for JSON output.

## Verification

- Keep meaningful fixture tests with tools whose behavior warrants them;
  prefer standard-library `unittest` for dependency-free scripts.
- Run relevant tests when changing a tool. Include path containment,
  Unicode, line endings, symlinks/junctions, and case sensitivity where
  they affect its behavior. Use temporary fixtures with scoped cleanup.
- Verify changes on each target OS when available. Report which systems
  and Python versions were actually tested, and any skipped checks;
  portability intent alone does not establish verification on all systems.
