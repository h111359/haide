"""Read-only specification checks; supported syntax and limits are in README.md."""

from __future__ import annotations

import argparse
from collections import deque
import json
import os
from pathlib import Path, PureWindowsPath
import re
import stat
import sys
import uuid


FORMAT = 1
PACKAGE_ROOT = Path(__file__).resolve().parent.parent


def read_text(path: Path) -> str:
    """Decode strict UTF-8 (optional BOM) and normalize all newline styles."""
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def is_alias(path: Path) -> bool:
    """Use lstat so Windows junctions and Unix links are never followed."""
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0)
        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    )


def inside(path: Path, parent: Path) -> bool:
    """Lexical containment with native platform case rules, not string prefixes."""
    try:
        common = os.path.commonpath((str(path), str(parent)))
    except ValueError:  # Different Windows drives.
        return False
    return os.path.normcase(common) == os.path.normcase(str(parent))


def locate_root(workspace: Path | None, root: str) -> tuple[Path, Path]:
    if not root.strip():
        raise ValueError("Root must be a nonempty specification folder.")
    if workspace is None:
        # An explicit standalone root trusts its parent, just as --workspace
        # trusts its supplied boundary. Never infer a product workspace.
        if ".." in Path(root).parts or (PureWindowsPath(root).drive and not Path(root).is_absolute()):
            raise ValueError("Standalone root must not contain parent traversal or a foreign/drive-relative path.")
        target = Path(os.path.abspath(root))
        if target == target.parent:
            raise ValueError("Specification root must not be a filesystem root.")
        workspace, root = target.parent, target.name
    # Explicit Workspace is trusted; canonicalize OS aliases such as macOS /tmp.
    workspace = workspace.resolve(strict=True)
    if not workspace.is_dir():
        raise ValueError("Workspace must be an existing directory.")
    if not root.strip() or Path(root).is_absolute() or PureWindowsPath(root).drive:
        raise ValueError("Root must be a nonempty workspace-relative folder.")
    target = Path(os.path.abspath(workspace / root))
    if target == workspace or not inside(target, workspace):
        raise ValueError("Root must be a workspace-relative folder strictly inside Workspace.")
    # Reject aliases inside that workspace before resolving/traversing Root.
    ancestors = []
    ancestor = target
    while ancestor != workspace:
        ancestors.append(ancestor)
        ancestor = ancestor.parent
    for ancestor in reversed(ancestors):
        if is_alias(ancestor):
            raise ValueError(f"Symlink/reparse-point path cannot be audited: {ancestor}")
    if not target.is_dir():
        raise ValueError(f"Specification root is not a directory: {root}")
    return workspace, target


def without_code(text: str) -> str:
    result = []
    fence = ""
    width = 0
    for line in text.splitlines():
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if match:
            run, tail = match.groups()
            if not fence:
                fence, width = run[0], len(run)
            elif run[0] == fence and len(run) >= width and not tail.strip():
                fence = ""
            continue
        if not fence and not re.match(r"^( {4}|\t)", line):
            result.append(re.sub(r"(`+).*?\1", "", line))
    return "\n".join(result)


class Audit:
    def __init__(self, workspace: Path | None, root: str):
        self.workspace, self.root = locate_root(workspace, root)
        self.root_argument = root
        self.issues: list[dict] = []
        self.nodes: list[dict] = []
        self.ids: dict[str, str] = {}
        self.leaf_depths: list[int] = []

    def relative(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def issue(self, severity: str, code: str, path: str, detail: str):
        self.issues.append(dict(severity=severity, code=code, path=path, detail=detail))

    def metadata(self, text: str, path: str) -> dict[str, str]:
        values = {}
        seen = set()
        match = re.match(r"\A---\n([\s\S]*?)\n---(?:\n|\Z)", text)
        if not match:
            self.issue("error", "metadata", path, "Missing or unsupported YAML front matter delimiters.")
            return values
        for line in match[1].splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            entry = re.fullmatch(r"([a-z][a-z0-9_-]*):[ \t]*(.*)", line)
            if not entry:
                self.issue("warning", "yaml-review", path, "Unsupported YAML syntax; validate manually.")
                continue
            key, value = entry[1], entry[2].strip()
            if key in seen:
                self.issue("error", "duplicate-key", path, f"Duplicate metadata key: {key}")
                continue
            seen.add(key)
            if re.fullmatch(r"'(?:[^']|'')*'", value):
                value = value[1:-1].replace("''", "'")
            elif value.startswith('"'):
                try:
                    value = json.loads(value)
                    if not isinstance(value, str):
                        raise ValueError("Not a string")
                except (ValueError, json.JSONDecodeError):
                    self.issue("warning", "yaml-review", path, f"Unsupported quoted scalar: {key}")
                    continue
            elif not value or re.search(r"^[|>&*!{\[\"']|:\s", value):
                self.issue("warning", "yaml-review", path, f"Unsupported scalar for {key}; validate manually.")
                continue
            else:
                value = re.sub(r"\s+#.*$", "", value).strip()
                if re.fullmatch(r"(?i:true|false|null|~)|[-+]?\d+(?:\.\d+)?", value):
                    self.issue("warning", "yaml-review", path, f"Non-string YAML scalar for {key}; validate manually.")
                    continue
            values[key] = value
        return values

    def registry(self) -> dict[str, str | None]:
        concept = read_text(PACKAGE_ROOT / "concepts/specification.md")
        registry = {}
        for type_name in re.findall(r"\]\(\.\./conventions/([a-z]+(?:-[a-z]+)*)_conv\.md\)", concept):
            body = read_text(PACKAGE_ROOT / f"conventions/{type_name}_conv.md")
            match = re.search(r"^## Content file\s*\n\s*`([^`\r\n/\\]+)`", body, re.MULTILINE)
            registry[type_name] = match[1] if match else None
            if not match:
                self.issue("warning", "convention-review", type_name, "Cannot determine content filename from convention.")
        if not registry:
            raise ValueError("No registered leaf-type convention links found.")
        return registry

    def check_links(self, file: Path):
        from urllib.parse import unquote, urlsplit

        path = self.relative(file)
        try:
            text = without_code(read_text(file))
        except (OSError, UnicodeError) as error:
            self.issue("error", "unreadable", path, str(error))
            return
        if re.search(r"^\s*\[[^\]]+\]:|\[[^\]]+\]\s*\[[^\]]*\]|<(?:a|img)\b", text, re.MULTILINE):
            self.issue("warning", "link-review", path, "Reference-style or HTML links require manual review.")
        for match in re.finditer(r"!?\[[^\]\n]*\]\(([^\n)]*)\)", text):
            raw = match[1].strip()
            destination = re.fullmatch(r'<([^>]+)>(?:\s+"[^"]*")?', raw)
            if not destination:
                destination = re.fullmatch(r'([^\s()]+)(?:\s+"[^"]*")?', raw)
            if not destination:
                self.issue("warning", "link-review", path, f"Unsupported link destination: {raw}")
                continue
            target = destination[1]
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith(("//", "#")):
                continue
            if target.startswith("/"):
                self.issue("warning", "link-review", path, f"Absolute URL path needs manual review: {target}")
                continue
            try:
                local = unquote(urlsplit(target).path)
                resolved = file.parent / local
                if not resolved.exists():
                    self.issue("error", "broken-link", path, target)
            except (OSError, ValueError) as error:
                self.issue("error", "link-path", path, f"Invalid relative link {target}: {error}")

    def children_table(self, text: str, path: str, children: list[Path]):
        if not re.search(r"^#+ Scope\s*$", text, re.MULTILINE):
            self.issue("error", "scope", path, "Missing Scope heading.")
        section = re.search(r"^#+ Children\s*\n(.*?)(?=^#+ |\Z)", text, re.MULTILINE | re.DOTALL)
        if not section:
            self.issue("error", "children-table", path, "Missing Children section.")
            return
        rows = re.findall(r"^\s*\|\s*([^|]+)\|", section[1], re.MULTILINE)
        if len(rows) < 2 or not re.fullmatch(r":?-+:?", rows[1].strip()):
            self.issue("warning", "children-review", path, "Children table not recognized; inspect manually.")
            return
        listed = []
        for cell in rows[2:]:
            cell = cell.strip()
            link = re.fullmatch(r"\[[^\]]+\]\((?:\./)?([^/)]+)(?:/|/__ncf__\.md)?\)", cell)
            if link:
                cell = link[1]
            else:
                cell = cell.strip("`").removesuffix("/").removeprefix("./")
            listed.append(cell)
        names = {child.name for child in children}
        for name in sorted(names - set(listed)):
            self.issue("error", "child-navigation", path, f"Child absent from recognized table entries: {name}")
        for name in sorted(set(listed) - names):
            self.issue("error", "child-navigation", path, f"Table entry is not an immediate child: {name}")
        if len(set(listed)) != len(listed):
            self.issue("error", "child-navigation", path, "Duplicate Children entries.")

    def inspect_node(self, folder: Path, depth: int, registry: dict) -> list[Path]:
        path = self.relative(folder)
        try:
            entries = sorted(folder.iterdir(), key=lambda item: item.name)
        except OSError as error:
            self.issue("error", "unreadable", path, str(error))
            return []
        children, files = [], []
        for entry in entries:
            try:
                if is_alias(entry):
                    self.issue("error", "reparse-point", self.relative(entry), "Skipped symlink/junction; audit is incomplete.")
                elif entry.is_dir():
                    children.append(entry)
                elif entry.is_file():
                    files.append(entry)
                else:
                    self.issue("error", "special-file", self.relative(entry), "Unsupported filesystem entry; not read.")
            except OSError as error:
                self.issue("error", "unreadable", self.relative(entry), str(error))
        config = folder / "__ncf__.md"
        if config.name not in {file.name for file in files}:
            self.issue("error", "missing-config", path, "Missing __ncf__.md")
            return children
        try:
            text = read_text(config)
        except (OSError, UnicodeError) as error:
            self.issue("error", "unreadable", path, str(error))
            return children
        metadata = self.metadata(text, path)
        for key in ("id", "title", "kind"):
            if not metadata.get(key):
                self.issue("error", "required-metadata", path, f"Missing readable {key}")
        if metadata.get("id"):
            try:
                canonical = str(uuid.UUID(metadata["id"]))
                if metadata["id"].lower() != canonical:
                    raise ValueError("Noncanonical UUID")
                if canonical in self.ids:
                    self.issue("error", "duplicate-uuid", path, f"UUID also used by {self.ids[canonical]}")
                else:
                    self.ids[canonical] = path
            except ValueError:
                self.issue("error", "uuid", path, "id must be a UUID in canonical hyphenated form.")
        kind = metadata.get("kind")
        size = len(text)
        self.nodes.append(dict(path=path, id=metadata.get("id"), kind=kind, type=metadata.get("type"), depth=depth, children=len(children), config_codepoints=size))
        content = [file for file in files if file.name != "__ncf__.md"]
        if kind == "branch":
            if size > 4000:
                self.issue("error", "config-size", path, f"{size} > 4000 code points")
            if len(children) > 8:
                self.issue("error", "child-count", path, f"{len(children)} > 8 children")
            if not children:
                self.issue("error", "empty-branch", path, "Branch has no child nodes.")
            if content:
                self.issue("error", "branch-files", path, "Branch contains files other than __ncf__.md.")
            self.children_table(text, path, children)
        elif kind == "leaf":
            self.leaf_depths.append(depth)
            if size > 12000:
                self.issue("error", "config-size", path, f"{size} > 12000 code points")
            elif size > 8000:
                self.issue("warning", "config-target", path, f"{size} > advisory 8000-code-point target")
            if children:
                self.issue("error", "leaf-children", path, "Leaf contains child folders.")
            if metadata.get("status") not in ("draft", "approved", "deprecated"):
                self.issue("error", "status", path, "Invalid or missing leaf status.")
            type_name = metadata.get("type")
            if type_name not in registry:
                self.issue("error", "leaf-type", path, "Invalid or missing registered type.")
            elif len(content) != 1 or (registry[type_name] and content[0].name != registry[type_name]):
                self.issue("error", "content-file", path, f"Expected one content file named {registry[type_name]}.")
        else:
            self.issue("error", "kind", path, "kind must be branch or leaf.")
        for file in files:
            if file.suffix.lower() == ".md":
                self.check_links(file)
        return children

    def compare(self, baseline: Path) -> list[dict]:
        before = json.loads(read_text(baseline))
        if not isinstance(before, dict) or before.get("format") != FORMAT or before.get("root") != self.root_argument or not isinstance(before.get("nodes"), list) or not isinstance(before.get("summary"), dict) or before["summary"].get("errors") != 0:
            raise ValueError("Baseline must be an error-free inventory audit (format 1) for the same root.")
        if not isinstance(before["summary"].get("warnings", 0), int):
            raise ValueError("Baseline summary warnings must be an integer.")
        if before["summary"].get("warnings", 0):
            self.issue("warning", "baseline-review", ".", "Baseline has review warnings; identity comparison is provisional.")
        old = {}
        for node in before["nodes"]:
            if not isinstance(node, dict) or not isinstance(node.get("path"), str):
                raise ValueError("Baseline contains an invalid node.")
            try:
                identity = str(uuid.UUID(node["id"]))
            except (ValueError, KeyError, AttributeError, TypeError) as error:
                raise ValueError("Baseline contains an invalid UUID.") from error
            if identity in old:
                raise ValueError("Baseline contains duplicate UUIDs.")
            old[identity] = node["path"]
        changes = []
        for identity, path in sorted(self.ids.items()):
            if identity not in old:
                changes.append(dict(change="added", id=identity, path=path))
            elif old[identity] != path:
                changes.append(dict(change="moved", id=identity, before=old[identity], path=path))
        changes.extend(dict(change="removed", id=identity, path=old[identity]) for identity in sorted(old.keys() - self.ids.keys()))
        return changes

    def run(self, inventory: bool = False, baseline: Path | None = None) -> dict:
        registry = self.registry()
        queue = deque([(self.root, 0)])
        while queue:
            folder, depth = queue.popleft()
            queue.extend((child, depth + 1) for child in self.inspect_node(folder, depth, registry))
        minimum = min(self.leaf_depths, default=None)
        maximum = max(self.leaf_depths, default=None)
        if minimum is None:
            self.issue("error", "no-leaves", ".", "No readable leaf metadata found.")
        elif maximum - minimum > 1:
            self.issue("error", "balance", ".", f"Leaf depth range {minimum}..{maximum} exceeds one level.")
        changes = self.compare(baseline) if baseline else None
        result = dict(
            format=FORMAT,
            root=self.root_argument,
            summary=dict(nodes=len(self.nodes), leaves=len(self.leaf_depths), min_depth=minimum, max_depth=maximum, errors=sum(issue["severity"] == "error" for issue in self.issues), warnings=sum(issue["severity"] == "warning" for issue in self.issues)),
            issues=self.issues,
            manual_review=[
                "Meaning, classification, canonical facts, approval, leaf content requirements, navigation descriptions, and identity continuity.",
                "Only flat scalar YAML and simple pipe Children tables are checked. Link existence only: no anchors, reference links, HTML, escaped/nested Markdown, or external URLs.",
            ],
        )
        if inventory:
            result["nodes"] = self.nodes
        if baseline:
            result["identity_changes"] = changes
        return result


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Existing specification folder; absolute or relative to the current directory, or workspace-relative with --workspace")
    parser.add_argument("--workspace", type=Path, help="Optional trusted workspace boundary; root must then be relative and strictly inside it")
    parser.add_argument("--inventory", action="store_true")
    parser.add_argument("--baseline", type=Path)
    root = None
    try:
        args = parser.parse_args(argv)
        root = args.root
        result = Audit(args.workspace, root).run(args.inventory, args.baseline)
        code = 1 if result["summary"]["errors"] else 0
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        result = dict(format=FORMAT, root=root, fatal=str(error))
        code = 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
