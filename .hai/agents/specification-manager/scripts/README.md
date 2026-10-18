# Specification audit

`audit_specification.py` is a read-only Python 3.11+ helper for Windows,
Linux, and macOS. It uses only the standard library; no packages or
installation steps run automatically. See the framework
[tooling convention](../../../conventions/tooling_conv.md).

`python` in these examples means a working Python 3.11+ interpreter. On
Linux/macOS, usually use `python3`; on Windows use a working `python`,
`py -3`, or the full path of an installed interpreter. A WindowsApps
alias can exist without a working command. In PowerShell, invoke a
quoted interpreter path with `&`. Check the chosen interpreter with
`--version` first; no executable location is embedded in these tools.

From the workspace root, supply the location established by the human
or environment-manager. The tool never discovers a location or changes state:

```text
python -B .hai/agents/specification-manager/scripts/audit_specification.py --root path/to/specification
```

The compact JSON result reports counts, depth range, actionable issues,
and manual-review boundaries. Exit codes: `0` means no detected errors
(warnings may remain), `1` means audit errors, and `2` means fatal input
or execution failure. A clean result establishes only the supported
mechanical checks, not full specification validity. Output JSON escapes
non-ASCII characters so shell output encoding does not lose information.

## Inventory and identity comparison

Add `--inventory` when a structural overview or UUID baseline is needed.
Its `nodes` array contains paths, IDs, kinds, types, depths, child counts,
and configuration sizes. Leaf content is not printed.

Capture an error-free inventory before restructuring, outside the
specification tree. The caller saves this file; the auditor never writes.
For example, on Linux/macOS:

```sh
python3 -B .hai/agents/specification-manager/scripts/audit_specification.py --root path/to/specification --inventory > /tmp/spec-before.json
```

In Windows PowerShell, use explicit UTF-8 (its `>` operator may write UTF-16):

```powershell
$baseline = Join-Path $env:TEMP ('spec-before-' + [guid]::NewGuid() + '.json')
$report = python -B .hai/agents/specification-manager/scripts/audit_specification.py --root path/to/specification --inventory
if ($LASTEXITCODE -ne 0) { throw 'Resolve or report audit errors before capturing a baseline.' }
$report | Set-Content -LiteralPath $baseline -Encoding UTF8
```

After authorized edits, pass the saved file:

```text
python -B .hai/agents/specification-manager/scripts/audit_specification.py --root path/to/specification --baseline /path/to/spec-before.json
```

`--baseline` accepts an error-free format-1 inventory for the same root
argument and reports added, removed, and moved IDs. Baseline warnings
make the comparison provisional. Interpret these changes: the helper
cannot prove identity continuity, identify retired-node replacements,
or distinguish a legitimate split from lost content. Existing error-free
UTF-8 format-1 PowerShell inventories remain readable.

Use `--workspace /path/to/workspace` when running elsewhere. This explicit
workspace is trusted and canonicalized, accommodating OS aliases such
as macOS `/tmp` and `/var`. The supplied root must remain strictly inside
that workspace; symlinks/junctions within the root path or tree are
rejected or skipped with errors. Containment uses native platform case
rules rather than ignoring case on Unix.

## Automated checks

- Node configuration presence, supported metadata, duplicate keys/UUIDs,
  required values, registered leaf types/statuses, branch/leaf exclusivity,
  expected content filenames, and branch contents.
- Registered types come from convention links in
  `.hai/concepts/specification.md`. Expected content filenames are
  read from each convention's Content file section rather than assumed.
- Branch child limits, global leaf-depth range, and Unicode code-point
  counts for whole configuration files after LF normalization. Astral
  characters count once. Content files do not inherit configuration limits.
- Branch Scope headings and immediate-child coverage in recognized
  Children tables, including missing, extra, and duplicate entries.
- Existence of simple relative inline Markdown/image link targets in all
  Markdown files within the tree. Code fences, indented code, and simple
  inline code are excluded; external URLs are not fetched.
- Symlink/junction traversal refusal, including cycles. Special filesystem
  entries are not read. The helper performs no filesystem mutations.

## Supported syntax and manual review

This is not a full YAML or Markdown parser. Metadata supports flat
lowercase keys with nonempty string values: plain strings (including
trailing comments), single-quoted strings with doubled apostrophes, and
double-quoted strings using JSON-compatible escapes. Multiline values,
nested structures, YAML anchors/tags, and other unsupported forms produce
review warnings and may prevent required-field validation. Do not rewrite
valid richer YAML merely to satisfy the helper; review it manually.

Children tables use leading/trailing pipes, a header and separator row,
and an immediate folder name in the first column, optionally in backticks
or a simple Markdown link. Other column orders or escaped pipes need
manual review; unfamiliar entries can produce navigation errors.

Link checks support simple inline destinations, optional double-quoted
titles, and angle-bracket destinations. They check file/folder existence,
not anchors or query semantics. Reference links and HTML links are flagged
for review. Nested/escaped Markdown, comments, complicated inline code,
and other extensions need manual review; they may be missed or produce
false positives. Links from outside the tree, URL health, descriptions,
classification, leaf-content requirements, canonical facts, sources,
approvals, and preservation of meaning remain the agent's responsibility.

## Fixture tests

```text
python -B .hai/agents/specification-manager/scripts/test_audit_specification.py
```

Tests use standard-library `unittest` and temporary workspaces with scoped
cleanup. They cover CLI output/exit codes and absence of mutations,
metadata, topology, sizes, links, baselines, paths, and alias/cycle cases.
Windows junction tests run only on Windows; symbolic-link tests report a
skip if creation privileges are unavailable. Target support is Windows,
Linux, and macOS; this migration was executed on Windows with Python
3.15.0. Linux/macOS execution and older supported Python versions still
require validation.
