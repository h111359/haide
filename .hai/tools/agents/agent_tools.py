"""Read-only HAI agent format audit and exact runtime model resolution."""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from environment_paths import STATE, PROFILES, INSTRUCTIONS, legacy_entries

sys.dont_write_bytecode = True

NAMES = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
CLASSES = {"light", "standard", "advanced"}
EFFORTS = {"low", "medium", "high", "xhigh", "max", "ultra"}
HEADINGS = ["Purpose", "Scope", "Out of Scope", "Rules", "Procedures", "References"]
PROCEDURE_HEADINGS = ["Description", "Inputs", "Prerequisites", "Rules", "Steps", "Outputs", "References"]
LOCAL_NAME = r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*"
LOCAL_REFERENCE = re.compile(r"\[(input|output):([^\[\]\r\n]+)\]")
TERM_REFERENCE = re.compile(r"\[term:([^\[\]:\r\n]+)\]")
NAMED_REFERENCE = re.compile(r"\[(term|input|output):([^\]\r\n]*)\]")
EXTENSIONS = {"hai-model-class", "hai-reasoning-effort"}
CONFIGURATION_CONTRACT = "configuration/contract.json"


class Invalid(ValueError):
    pass


class InputInvalid(Invalid):
    """A selected input cannot be read, rather than failing format validation."""


class UnsupportedYAML(ValueError):
    """Valid YAML may use this syntax, but this tool cannot verify it."""


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise Invalid(f"Nonstring or duplicate property: {key!r}")
        result[key] = value
    return result


def parse_frontmatter(source):
    """Parse the documented mapping/string subset, never a general YAML document.

    Line numbers include SKILL.md's opening frontmatter delimiter. Unsupported
    constructs are distinct from malformed supported syntax and schema failures.
    """
    lines = source.split('\n')
    terminal_break = source.endswith('\n')
    if terminal_break:
        lines.pop()

    def fail(message, index, unsupported=False):
        error = UnsupportedYAML if unsupported else Invalid
        raise error(f"Frontmatter line {index + 2}: {message}")

    def indent(index):
        line = lines[index]
        prefix = line[:len(line) - len(line.lstrip(' \t'))]
        if any(ch != ' ' for ch in prefix):
            fail("Only spaces are supported for indentation", index, True)
        return len(prefix)

    def quoted(text, index):
        quote, out, pos = text[0], [], 1
        escapes = {'0': '\0', 'a': '\a', 'b': '\b', 't': '\t', 'n': '\n',
                   'v': '\v', 'f': '\f', 'r': '\r', 'e': '\x1b', ' ': ' ',
                   '"': '"', '/': '/', '\\': '\\', 'N': '\x85', '_': '\xa0',
                   'L': '\u2028', 'P': '\u2029'}
        while pos < len(text):
            ch = text[pos]
            pos += 1
            if ch == quote:
                if quote == "'" and pos < len(text) and text[pos] == "'":
                    out.append("'")
                    pos += 1
                    continue
                return ''.join(out), text[pos:]
            if ch == '\\' and quote == '"':
                if pos == len(text):
                    fail("Multiline quoted scalars are unsupported", index, True)
                escape = text[pos]
                pos += 1
                if escape in escapes:
                    ch = escapes[escape]
                elif escape in 'xuU':
                    width = {'x': 2, 'u': 4, 'U': 8}[escape]
                    digits = text[pos:pos + width]
                    if len(digits) != width or not re.fullmatch('[0-9a-fA-F]+', digits):
                        fail("Malformed Unicode escape", index)
                    number = int(digits, 16)
                    if number > 0x10ffff or 0xd800 <= number <= 0xdfff:
                        fail("Escape is not a Unicode scalar value", index)
                    ch = chr(number)
                    pos += width
                else:
                    fail(f"Unknown quoted escape: \\{escape}", index)
            out.append(ch)
        fail("Unterminated or multiline quoted scalar", index, True)

    def scalar(text, index):
        if text.startswith(('"', "'")):
            value, tail = quoted(text, index)
            if tail and not (not tail.strip(' \t') or re.match(r'^[ \t]+#', tail)):
                fail("Unexpected content after quoted scalar", index)
            return value
        text = re.split(r'[ \t]+#', text, maxsplit=1)[0].rstrip(' \t')
        if not text or text.startswith('#'):
            return None
        if text[0] in '&*!{[}],?|>@`%' or text == '<<' or re.match(r'^[-:](?:[ \t]|$)', text):
            fail("Unsupported YAML construct; use a quoted string or block mapping", index, True)
        if re.search(r':(?:[ \t]|$)', text):
            fail("A plain scalar cannot contain colon followed by whitespace", index)
        if text in ('null', 'Null', 'NULL', '~'):
            return None
        if text in ('true', 'True', 'TRUE', 'yes', 'Yes', 'YES', 'on', 'On', 'ON'):
            return True
        if text in ('false', 'False', 'FALSE', 'no', 'No', 'NO', 'off', 'Off', 'OFF'):
            return False
        if re.fullmatch(r'[-+]?(?:0|[1-9][0-9]*)', text):
            return int(text)
        # Numeric/timestamp spellings vary across YAML schemas. Do not silently
        # turn an ambiguous implicit type into a string accepted by HAI metadata.
        if re.match(r'[-+]?(?:[0-9]|\.[0-9]|\.(?:inf|Inf|INF|nan|NaN|NAN)$)', text):
            fail("Ambiguous numeric/timestamp scalar; quote a string value", index, True)
        if text in ('---', '...'):
            fail("Multiple documents/document markers are unsupported", index, True)
        return text

    def skip(index):
        while index < len(lines) and (not lines[index].strip(' \t') or lines[index].lstrip(' \t').startswith('#')):
            index += 1
        return index

    def block(index, parent, header):
        header = re.split(r'[ \t]+#', header, maxsplit=1)[0].rstrip(' \t')
        if not re.fullmatch(r'[>|][-+]?', header):
            fail("Unsupported block scalar header (indent indicators are unsupported)", index, True)
        start = index + 1
        first = start
        while first < len(lines) and not lines[first].strip(' \t'):
            first += 1
        if first == len(lines) or indent(first) <= parent:
            breaks = first - start
            if first == len(lines) and not terminal_break and breaks:
                breaks -= 1
            return ('\n' * breaks if header.endswith('+') else ''), first
        width, end = indent(first), first
        if any(len(line) > width for line in lines[start:first]):
            fail("Leading blank block lines exceed content indentation", index)
        while end < len(lines) and (not lines[end].strip(' \t') or indent(end) > parent):
            if lines[end].strip(' \t') and indent(end) < width:
                fail("Inconsistent block scalar indentation", end)
            end += 1
        content = [line[width:] if line.strip(' \t') else '' for line in lines[start:end]]
        if any(not line.strip(' \t') and len(line) > width for line in lines[start:end]):
            fail("Space-only block content beyond indentation is unsupported", index, True)
        if header[0] == '>' and any(
                not content[n] and (content[n - 1].startswith(' ')
                                   or (n + 1 < len(content) and content[n + 1].startswith(' ')))
                for n in range(1, len(content))):
            fail("Folded blank lines beside more-indented content are unsupported", index, True)
        result = ''
        seen_text = False
        for offset, line in enumerate(content):
            result += line
            following = content[offset + 1] if offset + 1 < len(content) else None
            if following is None and end == len(lines) and not terminal_break:
                pass
            elif header[0] == '|' or following is None:
                result += '\n'
            elif line and following and not line.startswith(' ') and not following.startswith(' '):
                result += ' '
            elif not line and following and seen_text and not following.startswith(' '):
                pass
            else:
                result += '\n'
            seen_text = seen_text or bool(line)
        if header.endswith('-'):
            result = result.rstrip('\n')
        elif not header.endswith('+'):
            result = result.rstrip('\n') + ('\n' if any(content) and result.endswith('\n') else '')
        return result, end

    def mapping(index, width):
        result = {}
        while True:
            index = skip(index)
            if index == len(lines) or indent(index) < width:
                return result, index
            if indent(index) > width:
                fail("Unexpected indentation or unsupported multiline plain scalar", index, True)
            text = lines[index][width:]
            if text.startswith(('"', "'")):
                key, tail = quoted(text, index)
                tail = tail.lstrip(' \t')
                if not tail.startswith(':') or (len(tail) > 1 and tail[1] not in ' \t'):
                    fail("Expected mapping colon after quoted key", index)
                value_text = tail[1:].strip(' \t')
            else:
                match = re.match(r'^([^:]+):(?:[ \t]+(.*)|$)', text)
                if not match:
                    fail("Expected a block mapping entry; other YAML forms are unsupported", index, True)
                if re.search(r'[ \t]+#', match[1]):
                    fail('Mapping colon occurs inside a comment', index)
                key = scalar(match[1].rstrip(' \t'), index)
                value_text = (match[2] or '').strip(' \t')
            if key == '<<':
                fail("YAML merge keys are unsupported", index, True)
            if not isinstance(key, str) or key in result:
                fail(f"Nonstring or duplicate property: {key!r}", index)
            if value_text.startswith(('>', '|')):
                result[key], index = block(index, width, value_text)
            elif not value_text or value_text.startswith('#'):
                next_index = skip(index + 1)
                if next_index < len(lines) and indent(next_index) > width:
                    result[key], index = mapping(next_index, indent(next_index))
                else:
                    result[key], index = None, next_index
            else:
                result[key] = scalar(value_text, index)
                index += 1

    for index, line in enumerate(lines):
        if any(not (ch == '\t' or 0x20 <= ord(ch) <= 0x7e or ord(ch) == 0x85
                        or 0xa0 <= ord(ch) <= 0xd7ff or 0xe000 <= ord(ch) <= 0xfffd
                        or 0x10000 <= ord(ch) <= 0x10ffff) for ch in line):
            fail("Nonprintable character in YAML input", index)
        if any(ch in '\x85\u2028\u2029' for ch in line):
            fail("Unicode line separators must use quoted escapes", index, True)
    start = skip(0)
    if start == len(lines):
        return {}
    if indent(start):
        fail("Indented root mapping is unsupported", start, True)
    result, end = mapping(start, 0)
    if end != len(lines):
        fail("Unexpected trailing content", end)
    return result


def load_json(path):
    def reject_constant(value):
        raise Invalid(f"Non-JSON numeric constant: {value}")
    try:
        if not path.is_file():
            raise Invalid("Expected a readable regular JSON file")
        return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_pairs,
                          parse_constant=reject_constant)
    except (OSError, UnicodeError, ValueError) as exc:
        raise Invalid(f"Cannot read valid JSON: {exc}") from exc


def contained(workspace, relative):
    """Resolve existing ancestors, rejecting traversal and foreign path syntax."""
    if (not isinstance(relative, str) or not relative or "\\" in relative
            or ":" in relative or "?" in relative or "#" in relative
            or relative.startswith("/") or ".." in relative.split("/")):
        raise Invalid(f"Unsafe workspace-relative path: {relative!r}")
    try:
        target = (workspace / relative).resolve()
    except (OSError, RuntimeError) as exc:
        raise Invalid(f"Cannot resolve path: {relative}: {exc}") from exc
    if target == workspace or not target.is_relative_to(workspace):
        raise Invalid(f"Path escapes workspace: {relative}")
    return target


def unfenced(text):
    """Remove backtick/tilde fenced examples, preserving line boundaries."""
    result, fence = [], None
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
            result.append("")
        elif marker:
            fence = (marker[1][0], len(marker[1]))
            result.append("")
        else:
            result.append(line)
    if fence:
        raise Invalid("Unclosed Markdown fence")
    return "\n".join(result)


def sections(text, level, expected):
    pattern = re.compile(r"^" + "#" * level + r" (.+)$", re.M)
    matches = list(pattern.finditer(text))
    if [m[1].strip() for m in matches] != expected:
        raise Invalid(f"Expected headings in order: {', '.join(expected)}")
    return {m[1].strip(): text[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)]
            for i, m in enumerate(matches)}


def contract_table(text, headers):
    """Read one simple pipe table; HTML entities encode literal cell pipes."""
    lines = text.splitlines()
    positions = [i for i, line in enumerate(lines) if line.lstrip().startswith("|")]
    if len(positions) < 2 or positions != list(range(positions[0], positions[-1] + 1)):
        raise Invalid(f"Expected one contiguous table: {' | '.join(headers)}")
    rows = []
    for i in positions:
        line = lines[i].strip()
        if not line.endswith("|"):
            raise Invalid("Contract table rows must begin and end with pipes")
        row = [cell.strip() for cell in line[1:-1].split("|")]
        if len(row) != len(headers) or any(not cell for cell in row):
            raise Invalid("Contract table has wrong width or blank cells; encode literal pipes")
        rows.append(row)
    if rows[0] != headers or any(not re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1]):
        raise Invalid(f"Expected table headers: {' | '.join(headers)}")
    return rows[2:]


def reference_path(source, href, workspace, concepts=False, package=None):
    relative, _, fragment = href.partition("#")
    if (not relative or relative.startswith(("/", "\\")) or "\\" in relative
            or ":" in relative or "?" in relative or ("#" in href and not fragment)):
        raise Invalid(f"Unsafe reference path: {href!r}")
    try:
        target = (source.parent / relative).resolve()
        if not target.is_relative_to(workspace) or not target.is_file():
            raise Invalid(f"Missing or escaping reference: {href}")
        if package is not None and not target.is_relative_to(package):
            raise Invalid(f"Reference escapes its agent package: {href}")
        if concepts and (target.suffix != ".md" or "concepts" not in target.parts):
            raise Invalid(f"Term mapping must reference a concept Markdown file: {href}")
        target.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError, RuntimeError, ValueError) as exc:
        raise Invalid(f"Unreadable reference: {href}: {exc}") from exc
    return target


def term_mappings(text, source, workspace, inherited=None):
    result, local = dict(inherited or {}), set()
    for line in text.splitlines():
        terms = TERM_REFERENCE.findall(line)
        if not terms:
            continue
        # A mapping is a single reference token plus an actual inline Markdown
        # link on that bullet's line; prose references are not declarations.
        links = re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", line)
        if not re.match(r"^\s*- ", line) or len(terms) != 1 or len(links) != 1:
            raise Invalid("Declare each term mapping on one References bullet with one concept link")
        name = terms[0]
        if name != name.strip() or not name or name in local:
            raise Invalid(f"Invalid or duplicate term mapping: {name!r}")
        target = reference_path(source, links[0], workspace, concepts=True)
        if name in result and result[name] != target:
            raise Invalid(f"Conflicting term mapping: {name}")
        local.add(name)
        result[name] = target
    return result


def check_terms(text, mappings):
    for name in TERM_REFERENCE.findall(text):
        if name not in mappings:
            raise Invalid(f"Undeclared term reference: {name}")


def check_reference_spelling(text):
    for start in re.finditer(r"\[(?:term|input|output):", text):
        match = NAMED_REFERENCE.match(text, start.start())
        if not match:
            raise Invalid("Unclosed named reference")
        kind, name = match.groups()
        if kind == "term":
            valid = name == name.strip() and re.fullmatch(r"[^\[\]:\r\n]+", name)
        else:
            valid = re.fullmatch(LOCAL_NAME, name)
        if not valid:
            raise Invalid(f"Invalid {kind} reference name: {name!r}")


def rule_wording(text):
    """Check explicit modal spelling, not whether a sentence has that meaning."""
    prose = re.sub(r"(?<!`)(`+)(?!`)(.*?)\1(?!`)", " ", text, flags=re.S)
    if re.search(r"\b(?:should|shall)\b|\bought\s+to\b|\bmustn['’]t\b", prose, re.I):
        raise Invalid("Rule wording permits MUST, MUST NOT, and MAY, not SHOULD/SHALL or obligation aliases")
    if re.search(r"\bMAY\s+NOT\b", prose):
        raise Invalid("Use MUST NOT for prohibition or a positive MAY permission, not MAY NOT")
    if any(match[0] not in ("MUST", "MAY")
           for match in re.finditer(r"\b(?:must|may)\b", prose, re.I)):
        raise Invalid("Rule modals MUST and MAY must be uppercase")
    if not re.search(r"\b(?:MUST|MAY)\b", prose):
        raise Invalid("Each rule body requires explicit MUST, MUST NOT, or MAY outside literal code")


def rule_contract(text, group_level=3, local=False):
    """Check the titled-bullet subset, not rule meaning, scope, or precedence."""
    if text.strip() in (("None.",) if local else ("None", "None.")):
        return
    titles = set()
    in_rule = False
    has_content = False
    rule_body = []
    group = None
    group_has_rule = False
    for line in text.splitlines():
        if not line.strip():
            continue
        if re.fullmatch("#" * group_level + r" \S.*", line):
            if in_rule and not has_content:
                raise Invalid("Each rule must contain text after its title")
            if in_rule:
                rule_wording("\n".join(rule_body))
            if group is not None and not group_has_rule:
                raise Invalid("Rule groups must not be empty")
            group, group_has_rule = line, False
            in_rule = False
            continue
        match = re.match(r"^- \*\*([^*]+)\*\*(.*)$", line)
        if match:
            if in_rule and not has_content:
                raise Invalid("Each rule must contain text after its title")
            if in_rule:
                rule_wording("\n".join(rule_body))
            title = match[1].strip().rstrip(".:").casefold()
            if not title or title in titles or re.fullmatch(r"(?:r|rule[-_ ]?)\d+", title):
                raise Invalid(f"Duplicate or non-descriptive rule title: {match[1]}")
            titles.add(title)
            in_rule, has_content, group_has_rule = True, bool(match[2].strip()), True
            rule_body = [match[2]]
        elif (in_rule and line[:1].isspace()
              and not re.match(r"^\s*(?:[-*+] |\d+[.)] |#)", line)):
            has_content = True
            rule_body.append(line)
        else:
            raise Invalid("Rules require titled '-' bullets, optional subject groups, or None. alone")
    if not titles or (in_rule and not has_content):
        raise Invalid("Rules must contain titled instructions or None. alone")
    if in_rule:
        rule_wording("\n".join(rule_body))
    if group is not None and not group_has_rule:
        raise Invalid("Rule groups must not be empty")


def procedure_contract(text, source, workspace, inherited_terms, level=2):
    check_reference_spelling(text)
    parts = sections(text, level, PROCEDURE_HEADINGS)
    if parts["Description"].strip() in ("", "None", "None."):
        raise Invalid("Procedure Description must contain a short purpose and intended result")
    rule_contract(parts["Rules"], group_level=level + 1, local=True)
    inputs = contract_table(parts["Inputs"], ["Input", "Meaning", "Requirement", "Source", "If absent"])
    outputs = contract_table(parts["Outputs"], ["Output", "Meaning", "Completion criteria"])
    declared = {"input": set(), "output": set()}
    for kind, rows in (("input", inputs), ("output", outputs)):
        for row in rows:
            token = row[0]
            if token.startswith("`") and token.endswith("`"):
                token = token[1:-1]
            match = re.fullmatch(r"\[" + kind + ":(" + LOCAL_NAME + r")\]", token)
            if not match or match[1] in declared[kind]:
                raise Invalid(f"Invalid or duplicate {kind} declaration: {row[0]}")
            declared[kind].add(match[1])
            if kind == "input" and row[2] not in ("Mandatory", "Optional"):
                raise Invalid("Input Requirement must be Mandatory or Optional")
    for kind, name in LOCAL_REFERENCE.findall(text):
        if not re.fullmatch(LOCAL_NAME, name) or name not in declared[kind]:
            raise Invalid(f"Undeclared local {kind} reference: {name}")
    mappings = term_mappings(parts["References"], source, workspace, inherited_terms)
    check_terms(text, mappings)


def definition_body(text, path, workspace):
    body = unfenced(text)
    check_reference_spelling(body)
    if re.search(r"^# ", body, re.M):
        raise Invalid("Agent body must not contain an H1 title")
    parts = sections(body, 2, HEADINGS)
    mappings = term_mappings(parts["References"], path, workspace)
    rule_contract(parts["Rules"])
    procedures = parts["Procedures"]
    if re.search(r"^### ", procedures, re.M):
        names = re.findall(r"^### (.+)$", procedures, re.M)
        if len(names) != 1:
            raise Invalid("Only a single procedure may be inline")
        if procedures[:procedures.index("### ")].strip():
            raise Invalid("Inline procedure must begin with its name")
        header = procedures.index("#### ") if "#### " in procedures else len(procedures)
        trigger = procedures[procedures.index("\n", procedures.index("### ")):header].strip()
        if not re.fullmatch(r"Trigger: \S[^\n]*", trigger):
            raise Invalid("Inline procedure requires one nonblank Trigger: line")
        procedure_contract(procedures, path, workspace, mappings, level=4)
        outside = "\n".join(value for key, value in parts.items() if key != "Procedures")
        if LOCAL_REFERENCE.search(outside):
            raise Invalid("Input/output references must be local to a procedure")
        check_terms(outside, mappings)
    else:
        if LOCAL_REFERENCE.search(body):
            raise Invalid("Input/output references must be local to a procedure")
        check_terms(body, mappings)
        rows = contract_table(procedures, ["Procedure", "Trigger", "File"])
        if not rows:
            raise Invalid("Procedure index must contain at least one procedure")
        seen_names, seen_files = set(), set()
        for name, trigger, link in rows:
            match = re.fullmatch(r"\[[^\]\n]+\]\((procedures/[a-z][a-z0-9]*(?:-[a-z0-9]+)*\.md)\)", link)
            if not match or name.casefold() in seen_names:
                raise Invalid("Procedure index requires unique names and local procedures/<name>.md links")
            relative = match[1]
            target = reference_path(path, relative, workspace, package=path.parent.resolve())
            if not target.is_relative_to(path.parent.resolve()) or target in seen_files:
                raise Invalid("Procedure file must be unique and remain inside its agent package")
            seen_names.add(name.casefold())
            seen_files.add(target)
            content = unfenced(target.read_text(encoding="utf-8-sig"))
            headings = re.findall(r"^# (.+)$", content, re.M)
            if len(headings) != 1 or not content.lstrip().startswith("# "):
                raise Invalid(f"Procedure requires one initial H1 name: {relative}")
            if not re.match(r"\A\s*# [^\n]+\n\s*(?=## Description(?:\n|$))", content):
                raise Invalid("External procedure Description must immediately follow its H1 name")
            if re.search(r"^\s*(?:\*\*)?Trigger(?:\*\*)?:", content, re.M):
                raise Invalid("External procedure trigger belongs only in the SKILL index")
            procedure_contract(content, target, workspace, mappings)


def configuration_contract(path, workspace, metadata, name):
    """Validate package data using the helper installed beside this auditor."""
    if metadata.get("hai-configuration-contract") != CONFIGURATION_CONTRACT:
        raise Invalid("Every agent requires hai-configuration-contract: configuration/contract.json")
    package = path.parent.resolve()
    contract_path = (package / CONFIGURATION_CONTRACT).resolve()
    if not contract_path.is_relative_to(package) or not contract_path.is_relative_to(workspace):
        raise Invalid("Configuration contract must remain inside its agent package and workspace")
    helper = Path(__file__).resolve().parents[1] / "configuration/configuration_tools.py"
    spec = importlib.util.spec_from_file_location("hai_configuration_tools", helper)
    module = importlib.util.module_from_spec(spec)
    try:
        if not contract_path.is_file() or contract_path.stat().st_nlink > 1:
            raise Invalid("Configuration contract must be a regular file without hardlink aliases")
        spec.loader.exec_module(module)
        module.load_contract(contract_path, name)
    except (OSError, ValueError, RuntimeError) as exc:
        raise Invalid(f"Invalid configuration contract: {exc}") from exc


def read_definition(path, workspace=None):
    # CLI callers pass the original validated workspace explicitly, even when the
    # canonical definition path resolves through a contained alias. Direct library
    # use without it assumes a canonical resolved origin/agents/name/SKILL.md path.
    workspace = Path(workspace).resolve() if workspace is not None else path.parents[3]
    try:
        if not path.is_file():
            raise InputInvalid("Expected a readable regular definition file")
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise InputInvalid(f"Cannot read definition: {exc}") from exc
    lines = text.split('\n')
    if not lines or lines[0] != "---":
        raise Invalid("Definition requires YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise Invalid(f"Invalid YAML frontmatter: {exc}") from exc
    fields = parse_frontmatter("\n".join(lines[1:end]) + '\n')
    if not isinstance(fields, dict):
        raise Invalid("Frontmatter must be a mapping")
    if set(fields) - {"name", "description", "metadata", "license", "compatibility", "allowed-tools"}:
        raise Invalid("HAI extensions must be under metadata")
    name, description = fields.get("name"), fields.get("description")
    if (not isinstance(name, str) or len(name) > 64 or not NAMES.fullmatch(name)
            or name != path.parent.name):
        raise Invalid("Name must be valid and exactly match the parent directory")
    if (not isinstance(description, str) or not description.strip() or len(description) > 1024
            or "\n" in description or "\r" in description):
        raise Invalid("Description must be a nonblank single paragraph of at most 1024 characters")
    for key in ("license", "compatibility", "allowed-tools"):
        if key in fields and (not isinstance(fields[key], str) or not fields[key].strip()):
            raise Invalid(f"{key} must be a nonblank string")
    if len(fields.get("compatibility", "")) > 500:
        raise Invalid("Compatibility exceeds 500 characters")
    metadata = fields.get("metadata", {})
    if (not isinstance(metadata, dict)
            or any(not isinstance(k, str) or not isinstance(v, str) for k, v in metadata.items())):
        raise Invalid("Metadata keys and values must be strings")
    if name == "leader":
        if EXTENSIONS & metadata.keys():
            raise Invalid("Leader must omit specialist execution metadata")
    elif (metadata.get("hai-model-class") not in CLASSES
          or metadata.get("hai-reasoning-effort") not in EFFORTS):
        raise Invalid("Specialist requires valid hai-model-class and hai-reasoning-effort metadata")
    configuration_contract(path, workspace, metadata, name)
    definition_body("\n".join(lines[end + 1:]), path, workspace)
    return fields


def validate(workspace, definition):
    """Validate one canonical definition without loading its catalogue or environment."""
    path = contained(workspace, definition)
    if not re.fullmatch(r"(?:\.hai|\.hai_env)/agents/[^/]+/SKILL\.md", definition):
        raise InputInvalid("Definition must use a canonical HAI agent path")
    try:
        if path.parent.name != definition.split("/")[-2]:
            raise Invalid("Resolved definition identity differs from the selected canonical agent path")
        if path.with_name("knowledge.md").exists():
            raise Invalid("Both legacy and current definitions exist; explicit conflict resolution required")
        fields = read_definition(path, workspace)
        if fields["name"] != definition.split("/")[-2]:
            raise Invalid("Resolved definition identity differs from the selected canonical agent path")
    except UnsupportedYAML as exc:
        return {"ok": False, "definition": definition,
                "issues": [{"code": "unsupported", "path": definition, "message": str(exc)}]}
    except InputInvalid:
        raise
    except Invalid as exc:
        return {"ok": False, "definition": definition,
                "issues": [{"code": "definition", "path": definition, "message": str(exc)}]}
    return {"ok": True, "definition": definition, "agent": fields["name"], "issues": []}


def read_profiles(path):
    data = load_json(path)
    if (not isinstance(data, dict) or type(data.get("format_version")) is not int
            or data["format_version"] != 1 or not isinstance(data.get("models"), dict)):
        raise Invalid("Profiles require format_version 1 and a models mapping")
    if any(not isinstance(data["models"].get(k), str) or not data["models"][k].strip() for k in CLASSES):
        raise Invalid("Profiles require nonblank model IDs for light, standard, and advanced")
    return data


def resolve(workspace, definition, runtime):
    path = contained(workspace, definition)
    if not re.fullmatch(r"(?:\.hai|\.hai_env)/agents/[^/]+/SKILL\.md", definition):
        raise Invalid("Definition must use a canonical HAI agent path")
    if path.with_name("knowledge.md").exists():
        raise Invalid("Both legacy and current definitions exist; explicit conflict resolution required")
    fields = read_definition(path, workspace)
    if fields["name"] == "leader":
        raise Invalid("Leader uses interface settings and is not spawned")
    metadata = fields["metadata"]
    request = {"agent": fields["name"], "model_class": metadata["hai-model-class"],
               "reasoning_effort": metadata["hai-reasoning-effort"]}
    try:
        profiles = read_profiles(contained(workspace, PROFILES))
        request["model"] = profiles["models"][request["model_class"]]
        models = runtime.get("models") if isinstance(runtime, dict) else None
        if (not isinstance(models, dict) or not models
                or any(not isinstance(k, str) or not isinstance(v, list)
                       or any(not isinstance(e, str) for e in v) for k, v in models.items())):
            raise Invalid("Runtime snapshot requires model IDs mapped to supported effort lists")
        if request["model"] not in models:
            raise Invalid("Configured model is not advertised by the current runtime")
        if request["reasoning_effort"] not in models[request["model"]]:
            raise Invalid("Requested effort is not advertised for the configured model")
    except Invalid as exc:
        return {"ok": False, "request": request, "issues": [{"code": "unavailable", "message": str(exc)}]}
    return {"ok": True, "request": request, "issues": []}


def decode_cell(cell):
    # Decode exactly the three catalogue entities once; do not interpret arbitrary HTML.
    return re.sub(r"&(?:amp|#92|#124);", lambda m: html.unescape(m.group()), cell)


def audit(workspace):
    issues, agents = [], []
    framework_names = set()
    for origin in (".hai_env",):
        relative = f"{origin}/agents/catalogue.md"
        try:
            catalogue = contained(workspace, relative)
            if (origin == ".hai_env" and not catalogue.exists()
                    and not (workspace / relative).is_symlink()):
                continue
            if not catalogue.is_file():
                raise Invalid("Expected a readable regular catalogue file")
            lines = catalogue.read_text(encoding="utf-8-sig").splitlines()
            tables = [i for i, line in enumerate(lines) if line.lstrip().startswith("|")
                      and (i == 0 or not lines[i - 1].lstrip().startswith("|"))]
            if len(tables) != 1:
                raise Invalid("Catalogue must contain exactly one table")
            start = tables[0]
            cells = lambda line: [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells(lines[start]) != ["Agent", "Selection guide", "Definition"]:
                raise Invalid("Unexpected catalogue columns")
            if start + 1 >= len(lines) or cells(lines[start + 1]) != ["---"] * 3:
                raise Invalid("Invalid catalogue table separator")
            rows = []
            for line in lines[start + 2:]:
                if not line.lstrip().startswith("|"):
                    break
                row = cells(line)
                match = re.fullmatch(r"`([^`]+)`", row[0]) if len(row) == 3 else None
                name = match[1] if match else ""
                rows.append((name, row))
            duplicates = {name.casefold() for name, _ in rows
                          if sum(other.casefold() == name.casefold() for other, _ in rows) > 1}
            if origin == ".hai":
                framework_names = {name.casefold() for name, _ in rows if name}
            for name, row in rows:
                try:
                    if (not NAMES.fullmatch(name) or len(name) > 64 or name.casefold() in duplicates
                            or (origin == ".hai_env" and name.casefold() in framework_names)):
                        raise Invalid("Invalid, duplicate, or conflicting agent name")
                    if not row[1].strip():
                        raise Invalid("Blank selection description")
                    if row[2] == f"[knowledge.md]({name}/knowledge.md)":
                        raise Invalid("Legacy registration preserved; authorized agent-format migration required")
                    if row[2] != f"[SKILL.md]({name}/SKILL.md)":
                        raise Invalid("Definition link must use canonical <name>/SKILL.md")
                    path = contained(workspace, f"{origin}/agents/{name}/SKILL.md")
                    if path.with_name("knowledge.md").exists():
                        raise Invalid("Conflicting legacy knowledge.md remains")
                    definition = read_definition(path, workspace)
                    if decode_cell(row[1]) != definition["description"]:
                        raise Invalid("Catalogue copy differs from canonical decoded description")
                    agents.append({"name": name, "definition": f"{origin}/agents/{name}/SKILL.md"})
                except UnsupportedYAML as exc:
                    issues.append({"code": "unsupported", "path": relative, "agent": name, "message": str(exc)})
                except (Invalid, OSError, UnicodeError) as exc:
                    issues.append({"code": "agent", "path": relative, "agent": name, "message": str(exc)})
        except (Invalid, OSError, UnicodeError) as exc:
            issues.append({"code": "catalogue", "path": relative, "message": str(exc)})
    profile_status = "absent"
    try:
        profile = contained(workspace, PROFILES)
        if profile.exists() or (workspace / PROFILES).is_symlink():
            read_profiles(profile)
            profile_status = "valid"
    except Invalid as exc:
        profile_status = "invalid"
        issues.append({"code": "profiles", "message": str(exc)})
    return {"ok": not issues, "agents": agents, "profiles": profile_status, "issues": issues}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=".")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("audit")
    checked = commands.add_parser("validate")
    checked.add_argument("--definition", required=True)
    selected = commands.add_parser("resolve")
    selected.add_argument("--definition", required=True)
    selected.add_argument("--runtime", required=True, help="Explicit JSON runtime capability snapshot")
    args = parser.parse_args()
    try:
        workspace = Path(args.workspace).resolve(strict=True)
        if not workspace.is_dir():
            raise Invalid("Workspace must be a directory")
        if args.command == "audit":
            result = audit(workspace)
        elif args.command == "validate":
            result = validate(workspace, args.definition)
        else:
            result = resolve(workspace, args.definition, load_json(Path(args.runtime)))
    except UnsupportedYAML as exc:
        result = {"ok": False, "issues": [{"code": "unsupported", "message": str(exc)}]}
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 2
    except (Invalid, OSError, UnicodeError) as exc:
        result = {"ok": False, "issues": [{"code": "input", "message": str(exc)}]}
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
