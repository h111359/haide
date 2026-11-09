# Migrate environment layout

## Description

Relocate an existing environment's three fixed files into `.hai_env/config/`
without changing their bytes, schema versions, settings or Activity records.

## Inputs

| Input | Meaning | Requirement | Source | If absent |
| --- | --- | --- | --- | --- |
| Workspace | Existing workspace root | Mandatory | Human/host | Resolve before access |
| Authority | Explicit migration instruction | Mandatory | Human | Preview and diagnose only |
| Provenance | Nonblank source and reason | Mandatory | Actual instruction | Return dependency |

## Prerequisites

Python 3.11+, compatible installed core, readable mandatory legacy instructions,
valid supported legacy state, and safe source/destination paths. Stop all other
environment writers before apply; the cooperative lock does not stop old processes.

## Rules

- The host MUST apply safely read legacy instructions before dependent migration work and reload canonical instructions after success.
- The migration MUST preserve exact file bytes and unrelated workspace data.
- The host MUST retain partial results and report explicit recovery needs without automatic rollback, merge or retry.

## Steps

1. Validate and read `.hai_env/agent_instructions.md` safely; empty content is valid.
   Root-level state, profiles and instructions are migration inputs only.
2. Save a workspace-contained UTF-8 request, for example `layout-request.json`:

   ```json
   {"provenance":{"source":"explicit human migration instruction","reason":"group environment configuration under config"}}
   ```

3. Preview with `<absolute-python> -B .hai/tools/hai.py environment migrate-layout --workspace . --request layout-request.json`.
   Inspect moves, source hashes and unresolved issues. Preview writes nothing.
4. After covering authority and ended-writer checks, run the same command with `--apply`.
   It uses `.hai_env/.runtime.lock`, exclusively creates recovery copies and
   destinations, verifies bytes, then removes old files with state last.
5. Inspect `changed_files`, the backup path and `config/layout-migration.json`.
   The operation is not a multi-file transaction. Partial failures leave originals,
   created destinations and recovery copies in their actual observed state.
6. Run startup and reload `.hai_env/config/agent_instructions.md`. Supported
   format-2 state remains format 2; run the existing explicit
   `environment migrate-specification` workflow separately before ordinary work.

Mixed layouts, even identical duplicates, stop before mutation. Missing mandatory
files, unsafe paths, invalid source JSON/instructions and unexplained locks also
block apply. Optional profiles remain absent when absent originally.

For an interrupted operation, inspect the manifest's hashes and recovery copies,
compare every source/destination and stop writers. Obtain an explicit scoped
recovery decision before restoring or removing files; do not delete the manifest
to bypass the check. There is no automatic recovery command.

Completed migration is repeatable as an unchanged operation. An incomplete
manifest blocks both migration retries and fresh initialization.

## Outputs

| Output | Meaning | Completion criteria |
| --- | --- | --- |
| Migration result | Moves, hashes, actual changed paths and backup location | Readback validates preserved bytes and new-layout startup, or reports exact partial effects |
| Schema status | Original schema version | No relocation is described as schema conversion |
