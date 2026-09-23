"""Source-grounded extraction and balanced documentation with transactional catalogs."""
from __future__ import annotations
import ast
import math
import re
from pathlib import Path
from contracts import CORE, VERSION, Error, digest, dumps, now, screen


def extraction_dependencies(workspace, inventory):
    """Reuse is valid only for the same interpretation and workspace contracts."""
    instructions = []
    directory = workspace.resolve("home:.aih_product/instructions")
    if directory.exists():
        for path in sorted(directory.glob("*.md")):
            ref = "home:" + path.relative_to(workspace.home).as_posix()
            instructions.append({"ref": ref, "sha256": digest(workspace.read_text(ref))})
    source_instructions = [{"ref": item["ref"], "sha256": item["sha256"]} for item in inventory["files"] if Path(item["path"]).name in ("AGENTS.md", "CLAUDE.md")]
    contracts = {}
    for relative in ("conventions/runtime.schema.json", "conventions/schemas.json", "integrity.json", "engine/documentation.py"):
        path = CORE / relative
        if path.is_file():
            contracts[relative] = digest(path.read_bytes())
    return digest({"workspace": workspace.registry, "instructions": instructions, "source_instructions": source_instructions, "core_version": VERSION, "contracts": contracts})


def extract(workspace, inventory, previous=None):
    dependencies = extraction_dependencies(workspace, inventory)
    reusable = (previous or {}).get("dependency_fingerprint") == dependencies
    old = {x["ref"]: x for x in (previous or {}).get("facts", [])}
    facts, reused = [], 0
    for item in inventory["files"]:
        if reusable and item["ref"] in old and old[item["ref"]].get("sha256") == item["sha256"] and (previous or {}).get("extractor_version") == "1.0":
            facts.append(old[item["ref"]]); reused += 1; continue
        fact = {**item, "kind": "binary-or-unsupported", "facts": [], "limitations": ["Static observations do not establish business intent or runtime behavior."]}
        if item["bytes"] > 1024 * 1024:
            fact["limitations"].append("Content exceeds 1 MiB extraction limit; retained inventory coverage requires semantic disposition.")
            facts.append(fact); continue
        try:
            text = workspace.read_text(item["ref"])
            screen(text, "source extraction")
        except (UnicodeError, Error):
            fact["limitations"].append("Content omitted: non-UTF-8 or sensitive material. No value is retained.")
            facts.append(fact); continue
        suffix = Path(item["path"]).suffix.lower()
        fact["kind"] = "text"
        if suffix == ".py":
            try:
                tree = ast.parse(text)
                fact["kind"] = "python"
                fact["facts"] = [{"type": type(node).__name__, "name": node.name, "line": node.lineno, "docstring": (ast.get_docstring(node) or "")[:2000]} for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
                fact["imports"] = sorted({n.name for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)) for n in node.names})
            except SyntaxError:
                fact["limitations"].append("Python parsing failed; no code executed.")
        if suffix in (".md", ".txt", ".rst"):
            fact["headings"] = re.findall(r"^#{1,6}\s+(.+)$", text, re.M)
        fact["excerpt"] = text[:12000]
        fact["omitted_characters"] = max(0, len(text) - 12000)
        facts.append(fact)
    return {"schema_version": "1.0", "extractor_version": "1.0", "dependency_fingerprint": dependencies, "workspace_revision": workspace.revision, "inventory_fingerprint": inventory["fingerprint"], "created": now(), "facts": facts, "reused": reused, "new_or_changed": len(facts) - reused, "usage": None}


def balanced_tree(leaves, revision=1, max_children=8):
    if not 2 <= max_children <= 8:
        raise Error("tree-setting", "Catalog child limit must be between two and eight.")
    nodes = [dict(leaf, kind="content", children=[]) for leaf in leaves]
    current = nodes[:]
    level = 0
    while len(current) > max_children:
        level += 1
        groups = math.ceil(len(current) / max_children)
        size, extra = divmod(len(current), groups)
        next_level, offset = [], 0
        for i in range(groups):
            children = current[offset:offset + size + (i < extra)]; offset += len(children)
            ids = [n["id"] for n in children]
            node_id = "catalog-" + digest(ids)[:16]
            cat = {"id": node_id, "kind": "catalog", "title": children[0]["title"] + " · " + children[-1]["title"], "summary": "Related product knowledge: " + ", ".join(x["title"] for x in children[:3]), "status": "current", "when_to_read": "Follow this branch for its listed topics.", "children": ids, "path": "catalogs/" + node_id + ".yaml"}
            for child in children:
                child["parent"] = node_id
            nodes.append(cat); next_level.append(cat)
        current = next_level
    for node in current:
        node["parent"] = "root"
    root = {"id": "root", "kind": "catalog", "parent": None, "path": "index.yaml", "title": "Product knowledge", "summary": "Current product definition, evidence and limitations.", "status": "current", "when_to_read": "Read first, then follow only relevant branches.", "children": [n["id"] for n in current]}
    return {"schema_version": "1.0", "revision": revision, "root": "root", "nodes": [root] + nodes}


def validate_tree(tree, content_reader=None, max_children=8, word_target=1500):
    nodes = {n["id"]: n for n in tree.get("nodes", [])}
    if len(nodes) != len(tree.get("nodes", [])) or tree.get("root") not in nodes:
        raise Error("documentation-tree", "Duplicate canonical IDs or missing root.")
    visited, depths, content = set(), [], []
    def walk(node_id, parent, depth):
        if node_id in visited or node_id not in nodes:
            raise Error("documentation-tree", "Cycle, duplicate parent or missing target.")
        visited.add(node_id)
        node = nodes[node_id]
        if node.get("parent") != parent:
            raise Error("documentation-tree", "Structural parent does not match catalog edge.")
        for field in ("title", "summary", "status", "when_to_read", "path"):
            if not node.get(field):
                raise Error("documentation-tree", f"{node_id} needs {field}.")
        if node.get("kind") == "catalog":
            children = node.get("children", [])
            if not children or len(children) > max_children:
                raise Error("documentation-tree", "Catalogs need one to eight children; empty padding catalogs are invalid.")
            for child in children:
                walk(child, node_id, depth + 1)
        elif node.get("kind") == "content":
            if node.get("children"):
                raise Error("documentation-tree", "Content belongs only in terminal leaves.")
            depths.append(depth); content.append(node)
            if content_reader:
                text = content_reader(node["path"])
                if not text.strip():
                    raise Error("documentation-empty", "Empty documentation content is prohibited.")
                if len(text.split()) > word_target and not node.get("word_limit_exception"):
                    raise Error("documentation-size", f"Split {node_id} at meaningful boundaries, or justify indivisible reference material.")
                for target in re.findall(r"\]\(aih-doc:([\w.-]+)\)", text):
                    if target not in nodes:
                        raise Error("documentation-link", f"Missing cross-reference {target}.")
        else:
            raise Error("documentation-tree", "Unknown node kind.")
    walk(tree["root"], None, 0)
    if visited != set(nodes) or not depths or max(depths) - min(depths) > 1:
        raise Error("documentation-tree", "Unreachable nodes or strict depth balance failure.")
    return {"valid": True, "leaves": len(content), "catalogs": len(nodes) - len(content), "min_depth": min(depths), "max_depth": max(depths)}


def coverage_categories():
    from contracts import parse
    path = CORE / "conventions/coverage.json"
    if path.exists():
        value = parse(path.read_text("utf-8"))
        return value.get("categories", value) if isinstance(value, dict) else value
    return [{"id": name, "title": name.replace("-", " ").title()} for name in ["purpose", "requirements", "nonfunctional", "architecture", "workspace", "data", "analytics", "interfaces", "ux", "security", "dependencies", "deployment", "testing", "recovery", "observability", "operations", "guides", "additional"]]


def apply_proposal(store, workspace, result, inventory, owner, existing=None):
    """Apply semantic documentation only after complete local coverage and provenance checks."""
    topics = result.get("topics", [])
    categories = result.get("coverage", [])
    if not topics:
        raise Error("baseline-incomplete", "Semantic documentation has no substantive topics. Configure a compatible profile and resume.")
    old = store.read("documentation/tree.yaml", {"revision": 0, "nodes": []})
    old_nodes = {n["id"]: n for n in old["nodes"] if n.get("kind") == "content"}
    files = {f["ref"]: f for f in inventory["files"]}
    writes, leaves, covered = {}, [], set()
    for topic in topics:
        from contracts import identifier
        identifier(topic.get("id"), "topic ID")
        tid = topic["id"]
        text = screen(topic.get("content", ""), "documentation")
        if len(text.split()) < 12:
            raise Error("baseline-incomplete", f"Topic {tid} is not substantive documentation.")
        sources = topic.get("sources", [])
        for source in sources:
            ref = source if isinstance(source, str) else source["ref"]
            if ref not in files:
                raise Error("documentation-provenance", f"Topic {tid} references a source absent from the current inventory.")
            covered.add(ref)
        path = "topics/" + tid + ".md"
        before = store.read("documentation/" + path, None, raw=True)
        if before is not None and tid in old_nodes:
            previous_hash = old_nodes[tid].get("content_sha256")
            if previous_hash and digest(before) != previous_hash:
                raise Error("documentation-conflict", f"Human edits to {tid} must be preserved and reconciled explicitly.", {"topic_id": tid, "actual": digest(before), "expected": previous_hash})
            expected_hash = topic.get("expected_hash", previous_hash)
            if expected_hash and digest(before) != expected_hash:
                raise Error("revision-conflict", f"Documentation {tid} changed after generation began.")
            if before != text:
                writes[f"documentation/revisions/{owner}/{tid}.md"] = before
        writes["documentation/" + path] = text
        leaves.append({"id": tid, "path": path, "title": topic["title"], "summary": topic.get("summary", topic["title"]), "status": "current", "when_to_read": topic.get("when_to_read", "When working on " + topic["title"]), "sources": [files[s if isinstance(s, str) else s["ref"]] for s in sources], "content_sha256": digest(text), "updated": now(), "owner": owner, "verification": topic.get("verification", "observed, not runtime verified"), "word_limit_exception": topic.get("word_limit_exception")})
    # Incremental proposals can preserve valid leaves, but never overwrite human text silently.
    for tid, node in old_nodes.items():
        if tid not in {leaf["id"] for leaf in leaves}:
            source_refs = {s["ref"] for s in node.get("sources", [])}
            if all(ref in files and files[ref]["sha256"] == next(s["sha256"] for s in node["sources"] if s["ref"] == ref) for ref in source_refs):
                leaves.append(node); covered.update(source_refs)
            else:
                raise Error("documentation-stale", f"Incremental refresh omitted affected topic {tid}.")
    dispositions = result.get("source_dispositions", [])
    for disposition in dispositions:
        if disposition.get("ref") not in files or not disposition.get("reason"):
            raise Error("baseline-coverage", "Every uncovered local source needs an explicit reason and valid reference.")
        covered.add(disposition["ref"])
    if set(files) - covered or not inventory["complete"]:
        raise Error("baseline-coverage", "Documentation does not cover the complete registered local inventory.", {"uncovered": sorted(set(files) - covered), "inventory_problems": inventory["problems"]})
    required = {c["id"] if isinstance(c, dict) else c for c in coverage_categories()}
    if len(categories) != len(required) or {c.get("id") for c in categories} != required:
        raise Error("baseline-coverage", "Provide applicability for every required documentation category.", {"required": sorted(required)})
    topic_ids = {x["id"] for x in leaves}
    for category in categories:
        if category.get("status") not in ("applicable", "not-applicable", "unknown") or not category.get("rationale"):
            raise Error("baseline-coverage", "Coverage categories need a supported status and evidence-based rationale.")
        if category["status"] == "applicable" and (not category.get("topics") or not set(category["topics"]) <= topic_ids):
            raise Error("baseline-coverage", "Applicable coverage must reference existing substantive topics.")
    review = result.get("reconstruction_review", {})
    required_review = {"business_rules", "interfaces", "expected_results", "dependencies", "acceptance_tests", "recovery"}
    if not required_review <= set(review) or any(not review[k] for k in required_review):
        raise Error("reconstruction-review", "Record completeness and traceability findings for all six reconstruction dimensions.")
    tree = balanced_tree(leaves, old["revision"] + 1)
    validation = validate_tree(tree, lambda path: writes.get("documentation/" + path) or store.read("documentation/" + path, raw=True))
    for node in tree["nodes"]:
        if node["kind"] == "catalog":
            children = [next(x for x in tree["nodes"] if x["id"] == cid) for cid in node["children"]]
            writes["documentation/" + node["path"]] = {"id": node["id"], "title": node["title"], "children": [{k: c[k] for k in ("id", "path", "title", "summary", "status", "when_to_read")} for c in children]}
    baseline = {"schema_version": "1.0", "status": "complete", "workspace_revision": workspace.revision, "registry": workspace.registry, "manifest_hash": inventory["fingerprint"], "owner": owner, "completed": now(), "coverage_review": categories, "source_dispositions": dispositions, "reconstruction_review": review, "reconstruction": "specified but not demonstrated", "validation": validation, "product_tests": "not established by documentation generation"}
    writes.update({"documentation/tree.yaml": tree, "documentation/applicability.yaml": {"categories": categories}, "documentation/baseline.yaml": baseline, "documentation/inventory.yaml": inventory})
    store.transaction(writes)
    return baseline
