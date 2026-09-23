#!/usr/bin/env python3
"""AIH portable deterministic helpers. Python 3.11+, standard library only.

This source is bundled verbatim into each released skill. It never imports AIH,
executes inspected product code, follows product links, or grants new authority.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
import argparse
import ast
import contextlib
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile

VERSION = "1.0.0"
SCHEMA_VERSION = "1.0"

class ContractError(ValueError):
    pass

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

def digest(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()

def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode()

def screen(value):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    patterns = [r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", r"\b(?:sk|ghp|github_pat|xox[baprs])[-_][A-Za-z0-9_-]{15,}", r"(?im)\b(?:password|passwd|secret|access_token|api_key)\s*[:=]\s*[\"']?(?!\[REDACTED\]|<|\$\{|unknown\b|unavailable\b|none\b)[A-Za-z0-9_+/=-]{8,}"]
    if any(re.search(p, text) for p in patterns):
        raise ContractError("Sensitive input rejected before persistence; resubmit without credential values.")
    return value

def schema_validate(value, schema, location="$"):
    """Small deterministic validator for the shipped schema vocabulary."""
    expected = schema.get("type")
    kinds = {"object": dict, "array": list, "string": str, "integer": int, "number": (int, float), "boolean": bool, "null": type(None)}
    if expected and (not isinstance(value, kinds[expected]) or expected in ("integer", "number") and isinstance(value, bool)):
        raise ContractError(f"{location}: expected {expected}")
    if "enum" in schema and value not in schema["enum"]:
        raise ContractError(f"{location}: unsupported value")
    if isinstance(value, dict):
        missing = set(schema.get("required", [])) - value.keys()
        if missing:
            raise ContractError(f"{location}: missing {sorted(missing)}")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False and set(value) - props.keys():
            raise ContractError(f"{location}: unsupported fields {sorted(set(value)-props.keys())}")
        for key, item in value.items():
            if key in props:
                schema_validate(item, props[key], f"{location}.{key}")
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ContractError(f"{location}: too few items")
        for index, item in enumerate(value):
            schema_validate(item, schema.get("items", {}), f"{location}[{index}]")
    elif isinstance(value, str) and len(value) < schema.get("minLength", 0):
        raise ContractError(f"{location}: empty value")
    return value

def validate_tree(tree, max_children=8):
    nodes = tree.get("nodes", [])
    by_id = {node["id"]: node for node in nodes}
    if len(by_id) != len(nodes) or tree.get("root") not in by_id:
        raise ContractError("Duplicate node ID or missing root")
    visited, depths = set(), []
    def visit(identifier, parent, depth):
        if identifier in visited:
            raise ContractError("Documentation cycle or multiple parents")
        if identifier not in by_id:
            raise ContractError("Missing documentation target")
        visited.add(identifier)
        node = by_id[identifier]
        if node.get("parent") != parent:
            raise ContractError("Incorrect structural parent")
        children = node.get("children", [])
        if node["kind"] == "content":
            if children or not node.get("path"):
                raise ContractError("Content must be a terminal leaf with a path")
            depths.append(depth)
        elif node["kind"] == "catalog":
            if len(children) > max_children or not children:
                raise ContractError("Catalog must contain 1..max_children children")
            for child in children:
                visit(child, identifier, depth + 1)
        else:
            raise ContractError("Unknown documentation node kind")
    visit(tree["root"], None, 0)
    if len(visited) != len(nodes) or not depths or max(depths) - min(depths) > 1:
        raise ContractError("Unreachable content or unbalanced documentation tree")
    return {"valid": True, "nodes": len(nodes), "leaves": len(depths), "min_depth": min(depths), "max_depth": max(depths)}

class Workspace:
    """Fail-closed path resolver with fd-relative mutations on supported POSIX hosts.

    All links/reparse points and multiply linked files are rejected. This is
    intentionally stricter than merely proving a symlink's current destination.
    Windows read operations work; mutations fail closed without a handle-safe
    platform backend. External actors and arbitrary executables are not isolated.
    """
    def __init__(self, contract):
        self.contract = contract
        self.roots = {}
        for item in contract["workspace"]:
            key = item["id"]
            if not re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", key) or key in self.roots:
                raise ContractError("Invalid or duplicate folder ID")
            root = Path(item["path"])
            if not root.is_absolute() or not root.is_dir():
                raise ContractError(f"Folder {key} must be an existing absolute directory")
            self._reject_links(root)
            canonical = root.resolve(strict=True)
            if str(canonical) != str(root):
                raise ContractError("Folder paths must be canonical")
            if item["access"] not in ("read-write", "read-only"):
                raise ContractError("Unknown folder access")
            for registered in self.roots.values():
                old = registered["canonical"]
                if canonical == old or canonical in old.parents or old in canonical.parents or os.path.samefile(canonical, old):
                    raise ContractError("Duplicate, aliased, or overlapping workspace roots")
            self.roots[key] = dict(item, canonical=canonical, identity=(canonical.stat().st_dev, canonical.stat().st_ino))
    @staticmethod
    def _reject_links(path):
        for component in [path, *path.parents]:
            if component.exists() or component.is_symlink():
                st = component.lstat()
                if stat.S_ISLNK(st.st_mode) or getattr(st, "st_file_attributes", 0) & 0x400:
                    raise ContractError("Symbolic links, junctions, and reparse points are not accepted")
                if stat.S_ISREG(st.st_mode) and st.st_nlink != 1:
                    raise ContractError("Hard-linked files are not accepted")
    def resolve(self, ref, write=False):
        if not isinstance(ref, dict) or not isinstance(ref.get("path"), str) or ref.get("root") not in self.roots:
            raise ContractError("Expected root-qualified reference {root, path}")
        root = self.roots[ref["root"]]
        parts = PurePosixPath(ref["path"]).parts
        if not ref["path"] or ref["path"].startswith("/") or "\\" in ref["path"] or ":" in ref["path"] or ".." in parts:
            raise ContractError("Relative portable path required; traversal denied")
        path = root["canonical"].joinpath(*parts)
        self._reject_links(path)
        current = root["canonical"].stat()
        if (current.st_dev, current.st_ino) != root["identity"]:
            raise ContractError("Workspace root changed since validation")
        if write:
            if root["access"] != "read-write":
                raise ContractError("Read-only folder mutation denied")
            scopes = self.contract.get("scope", [])
            if not any(s["root"] == ref["root"] and (ref["path"] == s["path"] or ref["path"].startswith(s["path"].rstrip("/") + "/") or s["path"] == ".") for s in scopes):
                raise ContractError("Write falls outside the invocation scope")
            if ".aih" in parts or ".aih_product" in parts and path.suffix.lower() in (".py", ".pyc", ".sh", ".cmd", ".bat", ".exe", ".js", ".ps1", ".so", ".dll"):
                raise ContractError("Core and executable product-state mutations are forbidden")
        return path
    @contextlib.contextmanager
    def parent_fd(self, ref, create=False):
        self.resolve(ref, write=create)
        if os.name != "posix" or not hasattr(os, "O_NOFOLLOW") or os.open not in os.supports_dir_fd:
            raise ContractError("Safe directory-handle backend unavailable; mutation is blocked on this platform")
        root = self.roots[ref["root"]]
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        fd = os.open(root["canonical"], flags)
        try:
            info = os.fstat(fd)
            if (info.st_dev, info.st_ino) != root["identity"]:
                raise ContractError("Workspace identity changed")
            parts = PurePosixPath(ref["path"]).parts
            for part in parts[:-1]:
                if create:
                    try:
                        os.mkdir(part, mode=0o700, dir_fd=fd)
                    except FileExistsError:
                        pass
                child = os.open(part, flags, dir_fd=fd)
                os.close(fd)
                fd = child
            parent=self.resolve(ref,write=create).parent.stat()
            opened=os.fstat(fd)
            if (parent.st_dev,parent.st_ino)!=(opened.st_dev,opened.st_ino):
                raise ContractError('Parent identity changed before scoped access')
            yield fd, parts[-1]
        finally:
            os.close(fd)
    def read(self, ref):
        path = self.resolve(ref)
        if os.name == "posix":
            with self.parent_fd(ref) as (fd, name):
                target = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
                try:
                    st = os.fstat(target)
                    if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
                        raise ContractError("Read target is not a single-owner regular file")
                    with os.fdopen(target, "rb", closefd=False) as stream:
                        return stream.read()
                finally:
                    os.close(target)
        self._reject_links(path)
        return path.read_bytes()
    def write(self, ref, data, expected=None, exclusive=False):
        if isinstance(data, str):
            data = data.encode()
        screen(data.decode("utf-8"))
        self.resolve(ref, write=True)
        with self.parent_fd(ref, create=True) as (fd, name):
            exists = False
            original=None
            try:
                st = os.stat(name, dir_fd=fd, follow_symlinks=False)
                if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1:
                    raise ContractError("Unsafe existing destination")
                exists = True
                original=(st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns)
            except FileNotFoundError:
                pass
            if exclusive and exists:
                raise ContractError("Immutable record already exists")
            if expected is not None:
                actual = digest(self.read(ref)) if exists else None
                if actual != expected:
                    raise ContractError("Revision conflict: refresh the displayed record")
            temp_name = ".aih-write-" + os.urandom(12).hex()
            tmp = os.open(temp_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=fd)
            try:
                with os.fdopen(tmp, "wb") as stream:
                    stream.write(data)
                    stream.flush()
                    os.fsync(stream.fileno())
                self.resolve(ref, write=True)
                parent=self.resolve(ref,write=True).parent.stat()
                opened=os.fstat(fd)
                if (parent.st_dev,parent.st_ino)!=(opened.st_dev,opened.st_ino):
                    raise ContractError('Parent identity changed before replacement')
                try:
                    latest=os.stat(name,dir_fd=fd,follow_symlinks=False)
                    current=(latest.st_dev,latest.st_ino,latest.st_size,latest.st_mtime_ns,latest.st_ctime_ns)
                    if not stat.S_ISREG(latest.st_mode) or latest.st_nlink!=1:
                        raise ContractError('Destination became aliased or unsafe')
                except FileNotFoundError:
                    current=None
                if original!=current:
                    raise ContractError('Destination changed during write; retained the competing version')
                os.replace(temp_name, name, src_dir_fd=fd, dst_dir_fd=fd)
                os.fsync(fd)
            finally:
                try:
                    os.unlink(temp_name, dir_fd=fd)
                except FileNotFoundError:
                    pass
        return {"ref": ref, "sha256": digest(data)}

def validate_contract(contract, skill=None):
    package=Path(__file__).resolve().parents[1]
    schema_file=package/'resources/schemas.json' if (package/'resources/schemas.json').is_file() else package/'conventions/schemas.json'
    schema_validate(contract,json.loads(schema_file.read_text())['standalone_invocation'])
    required = ("schema_version", "id", "skill", "instruction", "workspace", "inputs", "output", "scope", "effects", "authorization", "constraints", "workspace_revision")
    for field in required:
        if field not in contract:
            raise ContractError("Invocation missing " + field)
    if contract["schema_version"] != SCHEMA_VERSION or not str(contract["instruction"]).strip() or not contract["workspace"]:
        raise ContractError("Invalid invocation version, instruction, or workspace")
    if skill is not None and contract["skill"] != skill:
        raise ContractError("Invocation skill differs from selected package")
    ws = Workspace(contract)
    for ref in contract["inputs"]:
        ws.resolve(ref)
    ws.resolve(contract["output"], write=True)
    authorization = contract["authorization"]
    if authorization.get("mode") not in ("read-only", "requirements", "analysis", "documentation", "setup", "approved-plan", "direct-implementation", "git"):
        raise ContractError("Missing explicit applicable authorization mode")
    if not authorization.get("instruction_reference"):
        raise ContractError("Authorization must reference the initiating user instruction")
    if contract["skill"] == "implement-plan":
        if authorization["mode"] not in ("approved-plan", "direct-implementation"):
            raise ContractError("Implementation requires approved-plan or direct-implementation authorization")
        if authorization["mode"] == "approved-plan" and not contract.get("plan"):
            raise ContractError("Approved implementation requires a plan reference")
        if authorization["mode"] == "approved-plan":
            if not authorization.get("plan_sha256"):
                raise ContractError("Approval must bind the exact plan fingerprint")
            if digest(ws.read(contract["plan"])) != authorization["plan_sha256"]:
                raise ContractError("Approved plan fingerprint changed; obtain applicable renewed authority")
    if contract["skill"] == "answer-product-questions" and authorization["mode"] != "read-only":
        raise ContractError("Questions require read-only product authority")
    if authorization["mode"] in ("read-only", "requirements", "analysis", "documentation", "setup") and "implementation" in contract["effects"]:
        raise ContractError("Consequential authority contradicts declared implementation effects")
    return ws

def output_ref(contract, name):
    if not re.fullmatch(r"[a-zA-Z0-9_./-]+", name) or ".." in PurePosixPath(name).parts:
        raise ContractError("Invalid output artifact name")
    return {"root": contract["output"]["root"], "path": contract["output"]["path"].rstrip("/") + "/" + name}

def record(contract, name, value, expected=None, exclusive=False):
    ws = validate_contract(contract)
    content = json_bytes(value) if not isinstance(value, str) else value
    return ws.write(output_ref(contract, name), content, expected, exclusive)

def inventory(contract):
    ws = validate_contract(contract)
    entries, omitted = [], []
    excluded = {".aih", ".aih_product", ".git", "node_modules", "__pycache__", ".venv", ".aih-runtime", ".aih_runtime"}
    generated=[ws.resolve(contract['output'])]+([ws.resolve(contract['runtime'])] if contract.get('runtime') else [])
    def is_generated(path):
        return any(path==output or output in path.parents for output in generated)
    for ref in contract["inputs"]:
        source = ws.resolve(ref)
        root = ws.roots[ref["root"]]["canonical"]
        if source.is_file():
            candidates = [source]
        else:
            candidates = []
            for current, dirs, files in os.walk(source, followlinks=False):
                dirs[:] = sorted(d for d in dirs if d not in excluded and not Path(current, d).is_symlink() and not is_generated(Path(current,d)))
                candidates.extend(Path(current, file) for file in sorted(files) if not is_generated(Path(current,file)))
        for path in candidates:
            if is_generated(path):continue
            qualified = {"root": ref["root"], "path": path.relative_to(root).as_posix()}
            try:
                raw = ws.read(qualified)
                item = {"ref": qualified, "workspace_revision": contract["workspace_revision"], "sha256": digest(raw), "bytes": len(raw)}
                if len(raw) > 2 * 1024 * 1024:
                    item["extraction"] = {"status": "omitted-large", "limitation": "Fingerprint only; semantic inspection remains required where relevant."}
                else:
                    try:
                        text = raw.decode("utf-8")
                        screen(text)
                        facts = {"status": "text", "lines": len(text.splitlines())}
                        if path.suffix == ".py":
                            try:
                                tree = ast.parse(text)
                                facts["definitions"] = [{"name": n.name, "kind": type(n).__name__, "line": n.lineno} for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
                                facts["imports"] = sorted({n.names[0].name for n in ast.walk(tree) if isinstance(n, ast.Import)} | {n.module or "" for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)})
                            except SyntaxError as exc:
                                facts["parse_error_line"] = exc.lineno
                        facts["verification"] = "static observation; no code executed"
                        item["extraction"] = facts
                    except UnicodeDecodeError:
                        item["extraction"] = {"status": "binary", "limitation": "No semantic decoder supplied"}
                entries.append(item)
            except (ContractError, OSError):
                omitted.append({"ref": qualified, "status": "unavailable-or-sensitive", "limitation": "No content retained; review local access or sensitive data."})
    result = {"schema_version": SCHEMA_VERSION, "invocation": contract["id"], "workspace_revision": contract["workspace_revision"], "entries": entries, "omitted": omitted, "extractor_version": VERSION, "verification": "not run"}
    result["manifest_hash"] = digest(json_bytes(entries))
    return result

def validate_questions(questions):
    from exchange import parse_questionnaire, render
    return parse_questionnaire(render(questions))

def render_questions(request, questions, interpretation_revision, previous=None):
    from exchange import export_form
    return export_form(request, questions, interpretation_revision, previous)

def parse_answers(text, current_request, forms, current_questions, review_revision):
    from exchange import receive
    return receive(text, current_request, forms, current_questions, review_revision)

def review_answers(questions, receipt, decisions, revision):
    from exchange import review
    return review(questions, receipt, decisions, revision)

def amendment_revision(identifier, text, previous=None, source="Framework user", disposition="saved-not-submitted"):
    screen(text)
    if not re.fullmatch(r"[A-Za-z0-9_-]+", identifier) or disposition not in ("draft", "saved-not-submitted", "submitted", "applied", "superseded", "withdrawn", "needs-clarification"):
        raise ContractError("Invalid amendment identity or disposition")
    return {"schema_version": SCHEMA_VERSION, "id": identifier, "revision": (previous or {}).get("revision", 0) + 1, "text": text, "sha256": digest(text), "source": source, "disposition": disposition, "previous_sha256": (previous or {}).get("sha256"), "captured_at": now()}

def validate_plan(plan, contract):
    from contracts import validate
    package = Path(__file__).resolve().parent.parent
    schema_path = package / "conventions/runtime.schema.json"
    if not schema_path.exists():
        schema_path = package / "resources/runtime.schema.json"
    schemas = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(plan, schemas["$defs"]["plan"], root=schemas)
    bindings = plan["bindings"]
    if not bindings.get("interpretation_revision") or bindings.get("workspace_revision") != contract["workspace_revision"]:
        raise ContractError("Plan must bind current interpretation and workspace revisions")
    tasks = plan["tasks"]
    if len({t["id"] for t in tasks}) != len(tasks):
        raise ContractError("Plan tasks require unique stable identities")
    required = {"tests", "verify", "documentation", "evidence"}
    kinds = {t.get("kind") for t in tasks}
    if not required <= kinds:
        raise ContractError("Plan missing completion tasks: " + ", ".join(sorted(required-kinds)))
    ws = validate_contract(contract)
    done = set()
    for seq, task in enumerate(tasks, 1):
        if task.get("sequence") != seq:
            raise ContractError("Task sequence must be contiguous")
        if not set(task.get("dependencies", [])) <= done:
            raise ContractError("Task dependencies must precede the task")
        for change in task.get("changes", []):
            if change.get("action") not in ("create", "modify", "move", "delete"):
                raise ContractError("Unknown planned effect")
            for value in [change["path"]] + ([change["destination"]] if change["action"] == "move" else []):
                if not isinstance(value, str) or ":" not in value:
                    raise ContractError("Plan effect needs root:relative/path")
                root, path = value.split(":", 1)
                ws.resolve({"root": root, "path": path}, write=True)
        done.add(task["id"])
    return {"valid": True, "tasks": len(tasks), "plan_sha256": digest(json_bytes(plan))}

def check_bundle(package):
    package = Path(package).absolute()
    Workspace._reject_links(package)
    manifest_path=package/'resources/manifest.json'
    Workspace._reject_links(manifest_path)
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('schema_version')!=SCHEMA_VERSION or manifest.get('bundle_version')!=VERSION or not isinstance(manifest.get('files'),dict) or not manifest['files']:
        raise ContractError('Unsupported or incomplete bundled resource manifest')
    for path, expected in manifest["files"].items():
        if not isinstance(path,str) or not path or PurePosixPath(path).is_absolute() or '..' in PurePosixPath(path).parts or '\\' in path or ':' in path:
            raise ContractError('Bundled resource path escapes its package')
        target = package / path
        Workspace._reject_links(target)
        if not target.is_file() or digest(target.read_bytes()) != expected:
            raise ContractError("Bundled resource integrity mismatch: " + path)
    return {"valid": True, "version": manifest["bundle_version"], "files": len(manifest["files"])}

def main(argv=None):
    if sys.version_info < (3,11):
        print(json.dumps({"ok":False,"error":"python-version","message":"AIH requires Python 3.11 or newer; Python 3.12.3 was tested."}))
        return 2
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["validate", "inventory", "extract", "record", "export-form", "receive", "review", "amendment", "validate-plan", "validate-tree", "apply-edits", "reconcile", "run-test", "git", "integrity"])
    parser.add_argument("--contract", help="Explicit local invocation JSON file; read-only intake")
    parser.add_argument("--data", help="Root-qualified JSON reference to an input data file")
    parser.add_argument("--artifact", default="result.json", help="Relative output artifact name")
    args = parser.parse_args(argv)
    try:
        if args.operation == "integrity":
            result = check_bundle(Path(__file__).resolve().parent.parent)
        else:
            if not args.contract:
                raise ContractError("--contract is required")
            # The explicitly supplied contract is controlled intake, not permission to inspect its neighbors.
            contract = screen(json.loads(Path(args.contract).read_text(encoding="utf-8")))
            package = Path(__file__).resolve().parent.parent
            if (package/'SKILL.md').is_file():
                check_bundle(package)
            ws = validate_contract(contract, skill=package.name if (package / "SKILL.md").is_file() else None)
            data = screen(json.loads(ws.read(json.loads(args.data)))) if args.data else {}
            if args.operation == "validate":
                result = {"valid": True, "skill": contract["skill"], "authority_assurance": "user instruction recorded; host identity is not independently verified"}
            elif args.operation in ("inventory", "extract"):
                result = inventory(contract)
            elif args.operation == "record":
                result = data
            elif args.operation == "export-form":
                result = render_questions(**data)
                if result is None:
                    result = {"status": "no-outstanding-requestor-questions"}
            elif args.operation == "receive":
                result = parse_answers(**data)
            elif args.operation == "review":
                result = review_answers(**data)
            elif args.operation == "amendment":
                result = amendment_revision(**data)
            elif args.operation == "validate-plan":
                result = validate_plan(data, contract)
            elif args.operation == "validate-tree":
                result = validate_tree(data)
            elif args.operation in ("run-test", "git"):
                from portable_process import execute
                result = execute(contract, data, ws, args.operation)
            elif args.operation in ('apply-edits','reconcile'):
                from portable_edits import execute
                result=execute(contract,data,ws,args.operation)
            effective = dict(contract, helper_version=VERSION, recorded_at=now(), identity_assurance="initiating instruction recorded; host identity not independently verified")
            record(contract, "invocation.json", effective)
            artifact = record(contract, args.artifact, result)
            result = {"ok": True, "operation": args.operation, "artifact": artifact, "usage": {"tokens": None, "status": "unavailable"}}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "error": type(exc).__name__, "message": str(exc)}))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
