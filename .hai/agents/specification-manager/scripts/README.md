# Specification audit

`audit_specification.py` is a read-only Python 3.11+ helper for Windows,
Linux, and macOS. It uses only the standard library; no packages or
installation steps run automatically. Copy the entire `specification-manager/`
folder, including `SKILL.md`, `contract.json`, `concepts/`, `conventions/`, and `scripts/`,
to use it independently. No HAI framework, environment state, leader, request
records, or model profiles are required. The format does not install or activate
a runtime skill; invoke the instructions and script using their installed paths.

`python` in these examples means a working Python 3.11+ interpreter. On
Linux/macOS, usually use `python3`; on Windows use a working `python`,
`py -3`, or the full path of an installed interpreter. A WindowsApps
alias can exist without a working command. In PowerShell, invoke a
quoted interpreter path with `&`. Check the chosen interpreter with
`--version` first; no executable location is embedded in these tools.

Supply an existing specification folder established by the caller. In standalone
mode, `--root` accepts an absolute path or a path relative to the current working
directory. The script can live elsewhere; knowledge and conventions are loaded
relative to the script's package, never from the target workspace. For example:

```sh
python3 -B /opt/specification-manager/scripts/audit_specification.py --root /work/product/specification
```

```powershell
python -B C:/tools/specification-manager/scripts/audit_specification.py --root 'C:/work/product/specification'
```

The tool never discovers a location, creates a tree, or changes state. An explicit
path does not authorize content edits. For HAI invocation, caller validation of
the enabled feature and configured location happens before running the tool;
the tool itself does not load or validate HAI state. From the HAI workspace root,
retain the explicit workspace containment boundary:

```text
python -B .hai/agents/specification-manager/scripts/audit_specification.py --workspace . --root path/to/specification
```

Earlier workspace-root commands without `--workspace` still locate the same
relative root, but standalone mode has no product-workspace containment claim.

The compact JSON result reports counts, depth range, actionable issues,
and manual-review boundaries. Exit codes: `0` means no detected errors
(warnings may remain), `1` means audit errors, and `2` means fatal input
or execution failure. A clean result establishes only the supported
mechanical checks, not full specification validity. Output JSON escapes
non-ASCII characters so shell output encoding does not lose information.

## Compatibility and catalogue

The package-local `contract.json` has exactly one positive JSON integer field,
`specification_compatibility_version`, currently `1`. The root `__ncf__.md`
carries its string counterpart, `specification_compatibility_version: "1"`.
Descendants cannot carry it. The JSON audit reports `compatibility` with `target`,
`found` (readable string or null), and `state`: `current`, `unmarked`, `older`,
`newer`, or `invalid`. Non-current states are audit errors but still return
structural inventories for assessment. A malformed/missing package contract is a
fatal input error, never replaced with workspace or environment data.

This checks the marker mechanically; it cannot establish that every contract
obligation was met or approve a migration. Follow
[contract versioning](../conventions/contract-versioning_conv.md) for the full
assessment, scoped plan, explicit human user approval (including marker-only adoption),
preservation, and verified completion process. Ordinary authorized content work
on a current tree does not need compatibility-migration approval.

Every tree has one root `__catalogue__.md`, derived from all node configurations.
It is permitted with either root kind and excluded from content/node counts;
nested catalogues are errors. Exact canonical comparison checks complete and
unique coverage, authoritative UUID/parent/kind/type/title fields, root-relative
links to each actual `__ncf__.md`, and breadth-first code-point lexical order.
The root's Parent ID and branch Type cells are blank. Literal metadata uses HTML
entities for Markdown/table characters and controls; link paths are percent
encoded. This catalogue contains no summaries, status, timestamps, or revision.
The auditor inspects actual nodes rather than treating a catalogue as authority.

Prepare the canonical Markdown without writing any file:

```text
python -B /path/to/specification-manager/scripts/audit_specification.py --root /work/product/specification --render-catalogue
```

On success stdout is only UTF-8-compatible Markdown text (the shell controls its
encoding), stderr explains that it is a candidate, and the exit code is `0`.
Errors produce the usual JSON failure and exit `2`; the renderer refuses tree
errors other than missing/stale catalogue and compatibility assessment findings.
Warnings still require the JSON audit's manual review. Root-only/alias violations,
duplicate UUIDs/metadata, and structural errors block rendering. No output file,
temporary file, marker, product content, or state is written. Inspect stdout and
save it only through a separately authorized edit; do not redirect it onto the
live catalogue, because shell redirection can truncate that input before audit.
When saving, use UTF-8 and retain a final newline. Rerun the normal audit after
the authorized save.

Rendering is available for unmarked/older/newer/invalid marker assessment so an
adoption plan can include a candidate catalogue before changing the live marker.
It does not override compatibility findings or approve any migration, downgrade,
or tree edit. For adoption/migration, assess and approve first, transform within
scope, verify all target obligations (using a staged candidate if needed), then
write the live target marker and run final verification. A renderer exit `0` is
not a successful compatibility audit or a recorded applied migration.

## Inventory and identity comparison

Add `--inventory` when a structural overview or UUID baseline is needed.
Its `nodes` array contains paths, IDs, kinds, types, depths, child counts,
and configuration sizes. Leaf content is not printed.

Capture an error-free inventory before restructuring, outside the
specification tree. The caller saves this file; the auditor never writes.
For example, on Linux/macOS:

```sh
python3 -B .hai/agents/specification-manager/scripts/audit_specification.py --workspace . --root path/to/specification --inventory > /tmp/spec-before.json
```

In Windows PowerShell, use explicit UTF-8 (its `>` operator may write UTF-16):

```powershell
$baseline = Join-Path $env:TEMP ('spec-before-' + [guid]::NewGuid() + '.json')
$report = python -B .hai/agents/specification-manager/scripts/audit_specification.py --workspace . --root path/to/specification --inventory
if ($LASTEXITCODE -ne 0) { throw 'Resolve or report audit errors before capturing a baseline.' }
$report | Set-Content -LiteralPath $baseline -Encoding UTF8
```

After authorized edits, pass the saved file:

```text
python -B .hai/agents/specification-manager/scripts/audit_specification.py --workspace . --root path/to/specification --baseline /path/to/spec-before.json
```

`--baseline` accepts an error-free format-1 inventory for the same exact root
argument and reports added, removed, and moved IDs. Baseline warnings
make the comparison provisional. Interpret these changes: the helper
cannot prove identity continuity, identify retired-node replacements,
or distinguish a legitimate split from lost content. Existing error-free
UTF-8 format-1 PowerShell inventories remain readable. Keep the same root
argument and workspace when reusing an existing baseline. Switching between
absolute and relative spellings requires a fresh baseline; the tool does not
guess whether differently spelled roots identify the same tree.

With `--workspace /path/to/workspace`, `--root` must be a nonempty relative
folder strictly inside that workspace, preserving the existing containment
contract. Absolute, drive-qualified, outside-workspace, and workspace-root
arguments are rejected. This explicit workspace is trusted and canonicalized,
accommodating OS aliases such as macOS `/tmp` and `/var`. Aliases between the
workspace and specification root are rejected.

Without `--workspace`, the explicitly supplied root's parent is the trusted,
canonicalized boundary, not an inferred product workspace. The root itself and
all tree descendants still reject symlinks/junctions; ancestor aliases outside
the root are trusted in this mode. Empty roots, parent-traversal components,
foreign/drive-relative paths, and filesystem roots are rejected. Use
`--workspace` when containment within a known workspace must be enforced.
Both modes reject or skip tree aliases with errors and use native platform case
rules rather than ignoring case on Unix. Neither mode follows tree aliases.

## Automated checks

- Node configuration presence, supported metadata, duplicate keys/UUIDs,
  required values, registered leaf types/statuses, branch/leaf exclusivity,
  expected content filenames, and branch contents.
- Registered types come only from convention links in the Leaf types section of
  this package's `concepts/specification.md`; contract conventions are not types. Expected content filenames are
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
- Independent compatibility marker/contract checks and complete root catalogue
  canonical comparison. Catalogue links are verified through actual inventory
  equality rather than the helper's limited generic Markdown link parser.

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
python -B /path/to/specification-manager/scripts/test_audit_specification.py
```

Tests use standard-library `unittest` and temporary workspaces with scoped
cleanup. They cover extraction/relocation of the complete package without HAI,
execution from unrelated working directories, CLI output/exit codes, absence
of mutations, metadata, topology, sizes, links, baselines, paths, and alias/cycle
cases, compatibility states and malformed contracts, catalogue staleness,
root-only metadata exclusion, escaping, and candidate rendering without writes.
Windows junction tests run only on Windows; symbolic-link tests report a
skip if creation privileges are unavailable. Target support is Windows,
Linux, and macOS. The baseline-1 changes were verified on Linux with Python
3.12.3; Windows junction tests are skipped there. Windows, macOS, and other
supported Python versions were not executed for these changes.
