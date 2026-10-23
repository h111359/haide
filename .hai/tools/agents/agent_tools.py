"""Read-only HAI agent format audit and exact runtime model resolution."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re
import sys

NAMES = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
CLASSES = {"light", "standard", "advanced"}
EFFORTS = {"low", "medium", "high", "xhigh", "max", "ultra"}
HEADINGS = ["Purpose", "Scope", "Definitions", "Required inputs", "Optional inputs",
            "Rules", "Procedures", "Expected outcome", "References"]
EXTENSIONS = {"hai-model-class", "hai-reasoning-effort"}


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
    try:
        if not path.is_file():
            raise Invalid("Expected a readable regular JSON file")
        return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_pairs)
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


def read_definition(path):
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
    headings = []
    fenced = False
    for line in lines[end + 1:]:
        if line.startswith("```") or line.startswith("~~~"):
            fenced = not fenced
        if not fenced:
            if re.match(r"^#\s", line):
                raise Invalid("Agent body must not contain an H1 title")
            if line.startswith("## "):
                headings.append(line[3:].strip())
    if headings != HEADINGS:
        raise Invalid("Body must contain exactly the nine required headings in order")
    return fields


def validate(workspace, definition):
    """Validate one canonical definition without loading its catalogue or environment."""
    path = contained(workspace, definition)
    if not re.fullmatch(r"(?:\.hai|\.hai_env)/agents/[^/]+/SKILL\.md", definition):
        raise InputInvalid("Definition must use a canonical HAI agent path")
    try:
        if path.with_name("knowledge.md").exists():
            raise Invalid("Both legacy and current definitions exist; explicit conflict resolution required")
        fields = read_definition(path)
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
    fields = read_definition(path)
    if fields["name"] == "leader":
        raise Invalid("Leader uses interface settings and is not spawned")
    metadata = fields["metadata"]
    request = {"agent": fields["name"], "model_class": metadata["hai-model-class"],
               "reasoning_effort": metadata["hai-reasoning-effort"]}
    try:
        profiles = read_profiles(contained(workspace, ".hai_env/model_profiles.json"))
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
    for origin in (".hai", ".hai_env"):
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
                    definition = read_definition(path)
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
        profile = contained(workspace, ".hai_env/model_profiles.json")
        if profile.exists() or (workspace / ".hai_env/model_profiles.json").is_symlink():
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
