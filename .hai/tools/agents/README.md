# Agent definition tools

`agent_tools.py` is a read-only Python 3.11+ format auditor and exact model
resolver for Windows, Linux, and macOS. It never spawns agents, changes state,
repairs registrations, or installs dependencies. Use a working interpreter per
[the tooling convention](../../conventions/tooling_conv.md).

The tool and tests use only the Python standard library. No downloads, package
installation, or PyYAML are needed. HAI's state and `.hai_env/` are not a Python
virtual environment.

The frontmatter reader supports a documented YAML subset, not the entire YAML
language. This is a tool limit, not a change to HAI's agent format contract.
Supported forms are space-indented block mappings, nested mappings, one-line plain
and single/double-quoted strings, comments, doubled single quotes, YAML double-quote
escapes (including Unicode), and literal/folded block strings with `-`, default,
or `+` chomping. Folded strings decode before catalogue comparison. Mapping keys
must be strings and unique after decoding at every level. Ordinary decimal integers,
YAML nulls, and booleans (including legacy yes/no/on/off forms) remain nonstrings,
so they cannot accidentally satisfy HAI's string metadata requirements. Quote values
intended as strings.

Unsupported forms produce an explicit `unsupported` issue and leave the definition
unverified: anchors, aliases, tags, merge keys, sequences, flow mappings (including
JSON-style mappings), complex keys, multiline plain/quoted strings, numeric/timestamp
spellings beyond ordinary decimal integers, indentation indicators on block scalars,
indented root mappings, Unicode line separators other than escaped quoted content,
and folded blank lines next to more-indented content. Space-only block content past
its indentation is also unsupported. These restrictions avoid guessing at semantics.
Malformed supported syntax, duplicate keys, and HAI schema failures are separate
validation findings. Parser errors include frontmatter line numbers where applicable.
The supported scalar rules follow the [YAML specification](https://yaml.org/spec/1.2.2/)
with conservative handling of implicit types across YAML versions.

From the workspace root:

```text
python -B .hai/tools/agents/agent_tools.py audit
python -B .hai/tools/agents/agent_tools.py validate --definition .hai/agents/agent-definition-manager/SKILL.md
python -B .hai/tools/agents/agent_tools.py resolve --definition .hai/agents/environment-manager/SKILL.md --runtime /path/to/runtime.json
python -B .hai/tools/agents/test_agent_tools.py
```

Use `--workspace /path/to/workspace` before the command when running elsewhere.
The audit reads both catalogues, their referenced definitions, and optional model
profiles. This full authoring/migration audit is not ordinary startup discovery.
It checks YAML (including duplicate keys and string metadata), names, specialist
execution labels, the six ordered role headings, procedure contracts, absence of agent H1 titles, canonical
links, catalogue description equality, collisions, path containment, legacy links,
and the profile schema. Missing workspace catalogue/profiles are valid and stay
absent. Legacy rows and conflicts are reported with names and never removed;
valid independent registrations remain in the result.

`validate --definition <canonical-workspace-relative-path>` checks one existing
`SKILL.md` under `.hai/agents/<name>/` or `.hai_env/agents/<name>/`, including an
unregistered definition. It reads neither catalogue, model profiles, nor core
environment state. Framework validation works with no `.hai_env/` directory;
workspace definition inspection does not require initialized environment state.
Paths must use `/` separators, match the canonical layout, and resolve within the
explicit workspace. The command checks frontmatter, name, metadata, six role headings,
including agreement between the selected path's name and the resolved definition,
and conflicting legacy definition files using the same definition validator as
`audit`. It follows the selected role's indexed procedures and declared concept
mapping paths. It does not register the target, reconstruct catalogues, inspect other
supporting references, check cross-origin name collisions, validate role semantics, or establish
execution permission. Both framework and workspace definitions require valid
registration before selection for execution or delegation; an explicit name or path
does not bypass that requirement.

Use `validate` for one definition before registration or after editing; use `audit`
for registered definitions and catalogue/profile consistency. Agent-definition-manager
owns the creation/update/audit/registration workflow and its semantic review; leader
owns runtime selection. These shared commands do not perform either role's mutations.

## Procedure and reference validation

The supported role format has exactly Purpose, Scope, Out of Scope, Rules,
Procedures, References as H2 headings. Rules use '-' bullets beginning with unique
bold readable titles; terminal periods/colons and case are ignored for duplicate
checks within that Rules section. Optional H3 subject groups do not establish
precedence. Numbered rule IDs such as R01 are rejected. `None` or `None.` alone
may represent an empty shared rule set. Indented prose can continue a rule;
unlabelled prose, empty rule bodies, nested lists, and empty groups are rejected.

Every shared/local rule body has an explicit uppercase `MUST`, `MUST NOT`, or
`MAY`, following [instruction-writing_conv.md](../../conventions/instruction-writing_conv.md).
Titles and literal inline-code examples do not satisfy this requirement. Closed
backtick spans (including matching longer backtick delimiters) and fenced examples
are excluded from the word checks; quotation marks alone are not an exemption.
Whole-word checks reject SHOULD/SHALL (any case), `ought to`, `mustn't`/`mustn’t`,
lowercase `must`/`may`, and ambiguous `MAY NOT`. Substrings in ordinary words do
not count. `None.` needs no modal; shared `None` remains accepted for compatibility.
Ordinary capability words such as `can` and adjectives such as `required checks`
are not rejected. The parser does not infer their normative use or detect every
possible synonym. Actor clarity, complete conditions, correct permission, preserving
preferences/defaults, and plainness still require human review.

External procedures use one simple Procedure/Trigger/File index table. Names and
resolved files are unique, triggers are nonblank, and links must be inline Markdown
links to `procedures/<lower-case-kebab-name>.md` inside the same resolved agent
package. Missing, unreadable, escaping, or duplicate files are invalid. Each external
file has one initial H1 name and exactly Description, Inputs, Prerequisites, Rules, Steps,
Outputs, References as H2 headings. Description immediately follows the title and
contains one or two short sentences stating the specific purpose and intended result;
empty text or `None` is rejected. Triggers remain in the index. A single inline procedure
instead uses one H3 name, one `Trigger: ...` line, and those seven H4 sections, with
Description immediately after the trigger. The
validator rejects mixed/multiple inline procedures.
Description presence and nonblank content are checked structurally; its brevity,
specificity, and fidelity to the procedure still require semantic review.

The mandatory local Rules section is between Prerequisites and Steps. Use exactly
`None.` alone for no additional local rules; shared `SKILL.md` rules always apply.
Otherwise use the same titled-bullet subset, with titles unique in that local Rules
section and optional H3 groups (H5 for inline procedures). Local input/output
references resolve to that procedure's declarations. Local rules cannot override
or duplicate shared rules; this semantic distinction is reviewed manually,
not inferred from titles or proven by the parser. Prerequisites are entry conditions
and Steps are ordered actions/branches, as explained in the
[Procedure concept](../../concepts/procedure.md).

Inputs and Outputs each use one contiguous table with the exact columns in
[procedure_conv.md](../../conventions/procedure_conv.md). Rows occupy one physical
line with leading/trailing pipes, nonblank cells, and `---` separators (edge colons
allowed). Encode literal pipes as `&#124;`. Header-only input/output tables explicitly
declare no parameters. Prerequisites may be `None`; structural acceptance does not
prove that steps are meaningful or outputs sufficient.

Input/output first cells declare `[input:snake_case]` or `[output:snake_case]`, plain
or wrapped in one backtick pair. Duplicate declarations, undeclared uses, invalid
names, and requirements other than Mandatory/Optional are rejected. Names are local
to each procedure. Agent-global parameter references are invalid; foreign target
names in a call use plain code names. Markdown fences are excluded and must close.
HTML comments/tables, multiline table cells, escaped literal pipes, and reference-style
procedure links are not interpreted as alternative contract syntax.

Term mappings are declared on one References bullet per name, with exactly one
inline link to a readable contained `concepts/` Markdown file. SKILL mappings apply
to its procedures; local additions are allowed, with no conflicting remapping.
The check verifies mapping names/paths, not semantic equivalence to concept prose.
Other supporting links and heading fragments still need appropriate author review.
Reference tokens are literal human contracts; the tool performs no interpolation,
value passing, permission checks, or execution.

CLI operations pass the original validated workspace through reference checks even
when definitions resolve through contained aliases. Direct `read_definition(path)`
library calls without an explicit workspace assume a canonical resolved origin/
agents/name/SKILL.md layout; pass `workspace` when using an alias.

Provide a UTF-8 JSON capability snapshot using current runtime evidence, for
example a runtime advertising exactly these combinations:

```json
{
  "models": {
    "gpt-6-luna": ["low", "medium", "high", "xhigh", "max"],
    "gpt-6.1-sol": ["low", "medium", "high", "xhigh", "max", "ultra"],
    "gpt-6-astra": ["low", "medium", "high", "xhigh", "max", "ultra"]
  }
}
```

The resolver reads only the selected definition, local profiles, and the supplied
snapshot; it accepts no fallback. This example does not establish availability in
another session. It reports the requested class, effort, model when resolved, and
any unavailable combination. Missing profiles return an issue; the caller applies
the separately documented startup bootstrap or human override instead. Neither
exception is inferred by the helper. A supplied snapshot cannot prove freshness
or runtime fork/permission support; leader must verify those before spawning.

JSON output uses `ok` and `issues`; audit adds `agents` and profile status,
resolution adds `request`, and validation adds `definition` plus `agent` on success.
Exit codes are `0` for supported checks passing, `1`
for detected validation/unavailability issues, and `2` for fatal input errors
(including unreadable selected definitions or runtime files). Validation reports
definition-format or legacy-conflict findings with exit `1`, and unsafe/noncanonical
paths or missing/unreadable definition files with exit `2`. Argument-parser errors
also exit `2` but use argparse's usage text rather than JSON. Unsupported YAML
produces `unsupported`: `validate` and `audit` exit `1`; `resolve` exits `2` because
the selected definition cannot be interpreted. Audit excludes unverified definitions
from successful results and continues independent catalogue/profile/agent checks.
Missing Python prevents
the command from starting. No output is proof of semantic ownership,
input sufficiency, reference meaning, core-state validity, or successful spawning.
The auditor recognizes simple three-column catalogue tables, not arbitrary
Markdown. Review complex fences/Markdown manually; unrelated tables are rejected.
Unregistered definitions are not reconstructed or registered by the audit.

Tests use temporary fixtures and standard-library `unittest`; run them when
modifying the helper. All frontmatter parser tests run without third-party packages.
Isolated CLI tests disable site-packages (`-I -S`) and verify real validation,
audit, resolution, error reporting, and absence of mutations. Parser fixtures cover
quoted/escaped Unicode, comments, nested duplicate keys, nonstring metadata,
folding/chomping, malformed input, and explicitly unsupported syntax. OS-specific
symlink checks may skip when unavailable; report those separately from passing tests.
