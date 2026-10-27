"""Fixture tests: python -B test_audit_specification.py (no external packages)."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import uuid

sys.dont_write_bytecode = True
from audit_specification import Audit, inside, locate_root, render_catalogue  # noqa: E402


SCRIPT = Path(__file__).with_name("audit_specification.py")


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="hai-spec-audit-")
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.package = self.workspace / "package"
        self.write("package/contract.json", '{"specification_compatibility_version": 1}\n')
        self.write("package/concepts/specification.md", "### Leaf types\n\n[Requirements](../conventions/functional-requirements_conv.md)\n")
        self.write("package/conventions/functional-requirements_conv.md", "## Content file\n\n`content.md`, in Markdown.\n")
        resource_patch = patch("audit_specification.PACKAGE_ROOT", self.package)
        resource_patch.start()
        self.addCleanup(resource_patch.stop)

    def write(self, path, text):
        target = self.workspace / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8"))
        return target

    def node(self, path="spec", kind="leaf", identity=None, body=""):
        identity = identity or str(uuid.uuid4())
        text = f"---\nid: {identity}\ntitle: Test node\nkind: {kind}\n"
        if len(Path(path).parts) == 1:
            text += 'specification_compatibility_version: "1"\n'
        if kind == "leaf":
            text += "type: functional-requirements\nstatus: draft\n"
        self.write(f"{path}/__ncf__.md", text + "---\n" + body)
        if kind == "leaf":
            self.write(f"{path}/content.md", "# Test content\n")
        self.refresh_catalogue(Path(path).parts[0])
        return identity

    def refresh_catalogue(self, root="spec"):
        """Fixture setup only; production audit/render never writes a catalogue."""
        nodes = Audit(self.workspace, root).run(inventory=True)["nodes"]
        self.write(f"{root}/__catalogue__.md", render_catalogue(nodes))

    def branch(self, path, children):
        body = "## Scope\nSubject.\n## Children\n| Folder | Purpose |\n| --- | --- |\n"
        body += "".join(f"| {child} | Subject {index} |\n" for index, child in enumerate(children))
        return self.node(path, "branch", body=body)

    def audit(self, root="spec", baseline=None):
        return Audit(self.workspace, root).run(inventory=True, baseline=baseline)

    @staticmethod
    def codes(result):
        return {issue["code"] for issue in result["issues"]}

    def test_valid_tree_and_depth_inventory(self):
        self.branch("spec", ["first", "[Second](second/)"])
        self.node("spec/first")
        self.node("spec/second")
        result = self.audit()
        self.assertEqual(result["summary"], dict(nodes=3, leaves=2, min_depth=1, max_depth=1, errors=0, warnings=0))
        self.assertEqual({node["path"] for node in result["nodes"]}, {".", "first", "second"})

    def test_unicode_crlf_and_exact_size_limit(self):
        self.node(body="\U0001f600")
        config = self.workspace / "spec/__ncf__.md"
        text = config.read_text(encoding="utf-8")
        text += "x" * (12000 - len(text))
        self.write("spec/__ncf__.md", text.replace("\n", "\r\n"))
        result = self.audit()
        self.assertEqual(result["nodes"][0]["config_codepoints"], 12000)
        self.assertNotIn("config-size", self.codes(result))
        self.assertIn("config-target", self.codes(result))
        self.write("spec/__ncf__.md", text + "x")
        self.assertIn("config-size", self.codes(self.audit()))

    def test_duplicate_uuid_case_normalized(self):
        self.branch("spec", ["first", "second"])
        identity = self.node("spec/first")
        self.node("spec/second", identity=identity.upper())
        self.assertIn("duplicate-uuid", self.codes(self.audit()))

    def test_uuid_requires_hyphenated_form(self):
        self.node(identity=uuid.uuid4().hex)
        self.assertIn("uuid", self.codes(self.audit()))

    def test_global_balance(self):
        self.branch("spec", ["shallow", "nested"])
        self.node("spec/shallow")
        self.branch("spec/nested", ["deeper"])
        self.branch("spec/nested/deeper", ["leaf"])
        self.node("spec/nested/deeper/leaf")
        result = self.audit()
        self.assertIn("balance", self.codes(result))
        self.assertEqual((result["summary"]["min_depth"], result["summary"]["max_depth"]), (1, 3))

    def test_nine_children(self):
        self.branch("spec", [f"child{index}" for index in range(9)])
        for index in range(9):
            self.node(f"spec/child{index}")
        self.assertIn("child-count", self.codes(self.audit()))

    def test_branch_size_and_exclusivity(self):
        self.branch("spec", ["child"])
        self.node("spec/child")
        config = self.workspace / "spec/__ncf__.md"
        self.write("spec/__ncf__.md", config.read_text() + "x" * 4001)
        self.write("spec/extra.md", "Extra")
        self.assertTrue({"config-size", "branch-files"} <= self.codes(self.audit()))

    def test_leaf_children_and_missing_content(self):
        self.node()
        self.node("spec/child")
        (self.workspace / "spec/content.md").unlink()
        self.assertTrue({"leaf-children", "content-file"} <= self.codes(self.audit()))

    def test_missing_configuration_does_not_hide_descendants(self):
        self.node("spec/child")
        result = self.audit()
        self.assertIn("missing-config", self.codes(result))
        self.assertEqual(result["summary"]["leaves"], 1)

    def test_children_table_missing_extra_and_duplicate(self):
        self.branch("spec", ["ghost", "ghost"])
        self.node("spec/child")
        issues = [issue for issue in self.audit()["issues"] if issue["code"] == "child-navigation"]
        self.assertEqual(len(issues), 3)

    def test_invalid_yaml_metadata_and_duplicate_keys(self):
        self.node()
        config = self.workspace / "spec/__ncf__.md"
        self.write("spec/__ncf__.md", config.read_text().replace("title: Test node", "title: |\n  Multiline\nid: duplicate"))
        self.assertTrue({"yaml-review", "duplicate-key", "required-metadata"} <= self.codes(self.audit()))

    def test_supported_quoted_metadata(self):
        self.node()
        config = self.workspace / "spec/__ncf__.md"
        original = config.read_text()
        for title in ("'It''s a title'", '"Title with \\n newline"', "Test node # comment"):
            self.write("spec/__ncf__.md", original.replace("Test node", title))
            self.refresh_catalogue()
            self.assertEqual(self.audit()["summary"]["errors"], 0)

    def test_registered_type_and_status_are_case_sensitive(self):
        self.node()
        config = self.workspace / "spec/__ncf__.md"
        self.write("spec/__ncf__.md", config.read_text().replace("functional-requirements", "Functional-Requirements").replace("status: draft", "status: unknown"))
        self.assertTrue({"leaf-type", "status"} <= self.codes(self.audit()))

    def test_dynamic_convention_content_filename(self):
        self.node()
        self.write("package/conventions/functional-requirements_conv.md", "## Content file\n\n`payload.json`\n")
        (self.workspace / "spec/content.md").rename(self.workspace / "spec/payload.json")
        self.assertEqual(self.audit()["summary"]["errors"], 0)

    def test_links_multiple_inline_code_exclusions_and_unicode(self):
        self.node()
        self.write("spec/present file.md", "# Present")  # Remove after using it to avoid leaf file-count issue being relevant.
        self.write("spec/content.md", '''[Missing](missing.md) and [Present](<present file.md>)
![Missing image](image.png)
[Present encoded](present%20file.md) [Anchor](#unknown) [External](https://example.invalid/missing)
```markdown
[Not a link](missing-in-fence.md)
```
`[Not a link](missing-in-code.md)`
    [Not a link](missing-in-indented-code.md)
''')
        issues = [issue for issue in self.audit()["issues"] if issue["code"] == "broken-link"]
        self.assertEqual({issue["detail"] for issue in issues}, {"missing.md", "image.png"})

    def test_unsupported_links_warn(self):
        self.node()
        self.write("spec/content.md", '[Reference][id]\n[id]: target.md\n[Complex](a(b).md)\n<a href="target.md">Text</a>')
        self.assertIn("link-review", self.codes(self.audit()))

    def test_identity_added_removed_and_moved(self):
        self.branch("spec", ["before", "removed"])
        moved = self.node("spec/before")
        removed = self.node("spec/removed")
        baseline = self.write("baseline.json", json.dumps(self.audit()))
        (self.workspace / "spec/before").rename(self.workspace / "spec/after")
        self.branch("spec", ["after", "added"])
        # Retain the root identity to isolate the intended identity changes.
        root_before = json.loads(baseline.read_text())["nodes"][0]["id"]
        root_config = self.workspace / "spec/__ncf__.md"
        root_config.write_text(root_config.read_text().replace(self.audit()["nodes"][0]["id"], root_before), encoding="utf-8")
        for file in (self.workspace / "spec/removed").iterdir():
            file.unlink()
        (self.workspace / "spec/removed").rmdir()
        added = self.node("spec/added")
        changes = self.audit(baseline=baseline)["identity_changes"]
        self.assertEqual({(change["change"], change["id"]) for change in changes}, {("moved", moved), ("removed", removed), ("added", added)})

    def test_invalid_and_duplicate_baselines_rejected(self):
        self.node()
        before = self.audit()
        before["summary"]["errors"] = 1
        baseline = self.write("baseline.json", json.dumps(before))
        with self.assertRaisesRegex(ValueError, "error-free"):
            self.audit(baseline=baseline)
        before["summary"]["errors"] = 0
        before["nodes"].append(before["nodes"][0])
        self.write("baseline.json", json.dumps(before))
        with self.assertRaisesRegex(ValueError, "duplicate UUID"):
            self.audit(baseline=baseline)
        before["summary"] = []
        self.write("baseline.json", json.dumps(before))
        with self.assertRaisesRegex(ValueError, "error-free"):
            self.audit(baseline=baseline)

    def test_baseline_review_warning_and_utf8_bom(self):
        self.node()
        before = self.audit()
        before["summary"]["warnings"] = 1
        baseline = self.write("baseline.json", "\ufeff" + json.dumps(before))
        self.assertIn("baseline-review", self.codes(self.audit(baseline=baseline)))

    def test_workspace_containment_and_prefix_collision(self):
        self.node()
        for invalid in ("", ".", "..", "../sibling", str(self.workspace / "spec"), "C:/outside"):
            with self.assertRaises((ValueError, OSError), msg=invalid):
                locate_root(self.workspace, invalid)
        self.assertFalse(inside(Path(str(self.workspace) + "-sibling"), self.workspace))
        # Native case rules must be retained; never casefold Unix paths.
        lower = Path(os.path.abspath("parentlower"))
        upper = lower.with_name("PARENTLOWER") / "child"
        self.assertEqual(inside(upper, lower), os.name == "nt")

    def test_standalone_root_and_invalid_paths(self):
        self.node()
        _, root = locate_root(None, str(self.workspace / "spec"))
        self.assertEqual(root, self.workspace.resolve() / "spec")
        self.assertEqual(Audit(None, str(root)).run()["summary"]["errors"], 0)
        for invalid in ("", "..", "spec/../spec", str(self.workspace.anchor)):
            with self.assertRaises((ValueError, OSError), msg=invalid):
                locate_root(None, invalid)

    def test_missing_packaged_registry_does_not_fall_back_to_workspace(self):
        self.node()
        # A historical shared-concept path must never act as a fallback registry.
        self.write(".hai/concepts/specification.md", "[Requirements](../conventions/functional-requirements_conv.md)\n")
        (self.package / "concepts/specification.md").unlink()
        with self.assertRaises(FileNotFoundError):
            self.audit()

    def test_relocated_package_without_hai_from_unrelated_directory(self):
        # Copy the complete distributable package; the target tree contains no
        # HAI state, framework, registry, or installation-specific metadata.
        copied = self.workspace / "relocated agent"
        shutil.copytree(SCRIPT.parent.parent, copied)
        self.node("product sp\u00e9cification")
        root = self.workspace / "product sp\u00e9cification"
        unrelated = self.workspace / "unrelated"
        unrelated.mkdir()
        command = [sys.executable, "-B", str(copied / "scripts/audit_specification.py")]
        original = {path.relative_to(self.workspace): path.read_bytes() for path in self.workspace.rglob("*") if path.is_file()}
        cases = (
            (unrelated, ["--root", str(root), "--inventory"]),
            (unrelated, ["--workspace", str(self.workspace), "--root", root.name]),
            (self.workspace, ["--root", root.name]),
            (root, ["--root", "."]),
        )
        for cwd, arguments in cases:
            with self.subTest(cwd=cwd, arguments=arguments):
                run = subprocess.run(command + arguments, cwd=cwd, capture_output=True, text=True, encoding="utf-8", check=False)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                result = json.loads(run.stdout)
                self.assertEqual(result["summary"]["errors"], 0)
                self.assertEqual(result["root"], arguments[arguments.index("--root") + 1])
        self.assertFalse((self.workspace / ".hai").exists())
        self.assertFalse((self.workspace / ".hai_env").exists())
        after = {path.relative_to(self.workspace): path.read_bytes() for path in self.workspace.rglob("*") if path.is_file()}
        self.assertEqual(original, after)

    def test_packaged_registry_covers_registered_leaf_conventions_only(self):
        self.node()
        package = SCRIPT.parent.parent
        with patch("audit_specification.PACKAGE_ROOT", package):
            registry = Audit(self.workspace, "spec").registry()
        conventions = {file.name.removesuffix("_conv.md") for file in (package / "conventions").glob("*_conv.md")}
        self.assertEqual(set(registry), conventions - {"contract-versioning"})
        self.assertEqual(len(registry), 28)
        self.assertTrue(all(registry.values()))

    def test_symlink_cycle_and_root_alias(self):
        self.branch("spec", ["loop"])
        link = self.workspace / "spec/loop"
        try:
            link.symlink_to(self.workspace / "spec", target_is_directory=True)
        except OSError as error:
            self.skipTest(f"Symlink creation not permitted: {error}")
        self.addCleanup(link.unlink)
        self.assertIn("reparse-point", self.codes(self.audit()))
        with self.assertRaisesRegex(ValueError, "Symlink/reparse-point"):
            locate_root(self.workspace, "spec/loop")
        with self.assertRaisesRegex(ValueError, "Symlink/reparse-point"):
            locate_root(None, str(link))

    def test_explicit_workspace_can_have_alias(self):
        self.node()
        alias = self.workspace / "workspace-alias"
        if os.name == "nt":
            subprocess.run(["cmd.exe", "/c", "mklink", "/J", str(alias), str(self.workspace)], check=True, capture_output=True)
            self.addCleanup(os.rmdir, alias)
        else:
            alias.symlink_to(self.workspace, target_is_directory=True)
            self.addCleanup(alias.unlink)
        canonical, root = locate_root(alias, "spec")
        self.assertEqual(canonical, self.workspace.resolve())
        self.assertEqual(root, self.workspace.resolve() / "spec")
        self.assertEqual(Audit(alias, "spec").run()["summary"]["errors"], 0)

    @unittest.skipUnless(os.name == "nt", "Windows junction fixture")
    def test_windows_junction_cycle(self):
        self.branch("spec", ["loop"])
        link = self.workspace / "spec/loop"
        subprocess.run(["cmd.exe", "/c", "mklink", "/J", str(link), str(self.workspace / "spec")], check=True, capture_output=True)
        self.addCleanup(os.rmdir, link)  # Remove junction itself; never recurse into target.
        self.assertIn("reparse-point", self.codes(self.audit()))
        with self.assertRaisesRegex(ValueError, "Symlink/reparse-point"):
            locate_root(self.workspace, "spec/loop")
        with self.assertRaisesRegex(ValueError, "Symlink/reparse-point"):
            locate_root(None, str(link))

    def test_utf8_errors_are_actionable(self):
        self.node()
        (self.workspace / "spec/__ncf__.md").write_bytes(b"\xff\xfe")
        self.assertIn("unreadable", self.codes(self.audit()))

    def test_cli_json_exit_codes_and_no_mutation(self):
        self.node(body="\U0001f600")
        original = {path.relative_to(self.workspace): path.read_bytes() for path in self.workspace.rglob("*") if path.is_file()}
        command = [sys.executable, "-B", str(SCRIPT), "--workspace", str(self.workspace)]
        for arguments, expected_code in ((["--root", "spec", "--inventory"], 0), (["--root", "missing"], 2), ([], 2)):
            run = subprocess.run(command + arguments, capture_output=True, text=True, encoding="utf-8", check=False)
            self.assertEqual(run.returncode, expected_code, run.stderr)
            self.assertIsInstance(json.loads(run.stdout), dict)
        self.write("spec/content.md", "[Missing](missing.md)")
        run = subprocess.run(command + ["--root", "spec"], capture_output=True, text=True, encoding="utf-8", check=False)
        self.assertEqual(run.returncode, 1)
        self.assertIn("broken-link", self.codes(json.loads(run.stdout)))
        self.write("spec/content.md", original[Path("spec/content.md")].decode("utf-8"))
        after = {path.relative_to(self.workspace): path.read_bytes() for path in self.workspace.rglob("*") if path.is_file()}
        self.assertEqual(original, after)

    def test_compatibility_states_and_canonical_string_markers(self):
        self.node()
        original = (self.workspace / "spec/__ncf__.md").read_text()
        cases = (
            ('specification_compatibility_version: "1"\n', "current"),
            ("", "unmarked"),
            ('specification_compatibility_version: "2"\n', "newer"),
            ('specification_compatibility_version: "01"\n', "invalid"),
            ('specification_compatibility_version: "0"\n', "invalid"),
            ('specification_compatibility_version: "-1"\n', "invalid"),
            ('specification_compatibility_version: 1\n', "invalid"),
            ('specification_compatibility_version: true\n', "invalid"),
            ('specification_compatibility_version: "1"\nspecification_compatibility_version: "2"\n', "invalid"),
        )
        for marker, state in cases:
            with self.subTest(marker=marker):
                self.write("spec/__ncf__.md", original.replace('specification_compatibility_version: "1"\n', marker))
                result = self.audit()
                self.assertEqual(result["compatibility"]["state"], state)
                self.assertEqual(result["summary"]["nodes"], 1)  # Assessment survives incompatibility.
                self.assertEqual("compatibility-" + state in self.codes(result), state != "current")
        self.write("package/contract.json", '{"specification_compatibility_version": 2}')
        self.write("spec/__ncf__.md", original)
        result = self.audit()
        self.assertEqual(result["compatibility"], dict(target=2, found="1", state="older"))
        self.assertIn("compatibility-older", self.codes(result))

    def test_malformed_package_contracts_fail_without_fallback(self):
        self.node()
        malformed = ("{}", "[]", "null", "{", '{"specification_compatibility_version": 1, "extra": 2}',
                     '{"specification_compatibility_version": 1, "specification_compatibility_version": 2}')
        malformed += tuple(json.dumps({"specification_compatibility_version": value}) for value in (0, -1, True, 1.5, "1", None, []))
        for contract in malformed:
            with self.subTest(contract=contract):
                self.write("package/contract.json", contract)
                with self.assertRaises(ValueError):
                    self.audit()
        (self.package / "contract.json").unlink()
        # Even a target workspace contract never supplies missing package knowledge.
        self.write("spec/contract.json", '{"specification_compatibility_version": 1}')
        with self.assertRaises(FileNotFoundError):
            self.audit()

    def test_compatibility_marker_is_root_only(self):
        self.branch("spec", ["child"])
        self.node("spec/child")
        config = self.workspace / "spec/child/__ncf__.md"
        self.write("spec/child/__ncf__.md", config.read_text().replace("kind: leaf\n", 'kind: leaf\nspecification_compatibility_version: "1"\n'))
        self.assertIn("compatibility-location", self.codes(self.audit()))

    def test_catalogue_root_leaf_and_branch_are_reserved_metadata(self):
        self.node()
        result = self.audit()
        self.assertEqual(result["summary"]["errors"], 0)
        self.assertEqual((result["summary"]["nodes"], result["summary"]["leaves"]), (1, 1))
        self.assertEqual(result["nodes"][0]["children"], 0)
        (self.workspace / "spec/content.md").unlink()
        self.branch("spec", ["child"])
        self.node("spec/child")
        self.assertEqual(self.audit()["summary"]["errors"], 0)
        self.write("spec/child/__catalogue__.md", "# Forbidden nested catalogue\n")
        self.assertTrue({"catalogue-location", "content-file"} <= self.codes(self.audit()))

    def test_catalogue_missing_stale_duplicate_links_fields_and_order(self):
        self.branch("spec", ["a", "b"])
        self.node("spec/a")
        self.node("spec/b")
        target = self.workspace / "spec/__catalogue__.md"
        original = target.read_text()
        rows = original.splitlines(keepends=True)
        variants = (
            "".join(rows[:-1]),  # Missing node.
            original + rows[-1],  # Duplicate node.
            original.replace("a/__ncf__.md", "ghost/__ncf__.md"),
            original.replace("Test node", "Stale title", 1),
            original.replace("| leaf |", "| branch |", 1),
            original.replace("| functional-requirements |", "| security |", 1),
            original.replace(self.audit()["nodes"][0]["id"], str(uuid.uuid4()), 1),
            "".join(rows[:-2] + [rows[-1], rows[-2]]),
        )
        for changed in variants:
            with self.subTest(changed=changed):
                self.write("spec/__catalogue__.md", changed)
                self.assertIn("catalogue-stale", self.codes(self.audit()))
        target.unlink()
        self.assertIn("catalogue-missing", self.codes(self.audit()))

    def test_catalogue_escapes_literal_metadata_and_encoded_paths(self):
        child = "snow & [brackets] (round) # \U0001f600"
        self.branch("spec", [child])
        self.node("spec/" + child)
        title = "A | [x] *bold* _u_ `code` \\ <&> \U0001f600\nnext 'quoted'"
        config = self.workspace / "spec" / child / "__ncf__.md"
        config.write_text(config.read_text().replace("title: Test node", "title: " + json.dumps(title)), encoding="utf-8")
        self.refresh_catalogue()
        rendered = (self.workspace / "spec/__catalogue__.md").read_text()
        self.assertIn("&#124; &#91;x&#93; &#42;bold&#42;", rendered)
        self.assertIn("&lt;&amp;&gt; \U0001f600&#10;next", rendered)
        self.assertIn("&#x27;quoted&#x27;", rendered)
        self.assertIn("snow%20%26%20%5Bbrackets%5D%20%28round%29%20%23%20%F0%9F%98%80/__ncf__.md", rendered)
        self.assertEqual(self.audit()["summary"]["errors"], 0)

    def test_catalogue_breadth_first_case_sensitive_stable_parent_links(self):
        root = self.branch("spec", ["b", "A"])
        first = self.branch("spec/A", ["deep"])
        deep = self.node("spec/A/deep")
        second = self.node("spec/b")
        result = self.audit()
        rendered = render_catalogue(list(reversed(result["nodes"])))
        self.assertEqual(rendered, (self.workspace / "spec/__catalogue__.md").read_text())
        rows = rendered.splitlines()[4:]
        self.assertEqual([row.split(" | ")[0].removeprefix("| ") for row in rows], [root, first, second, deep])
        self.assertIn(f"| {first} | {root} | branch |  |", rows[1])
        self.assertIn(f"| {deep} | {first} | leaf |", rows[3])

    def test_catalogue_breadth_first_orders_components_before_prefix_punctuation(self):
        self.branch("spec", ["a", "a!"])
        self.branch("spec/a", ["z"])
        first = self.node("spec/a/z")
        self.branch("spec/a!", ["x"])
        second = self.node("spec/a!/x")
        text = render_catalogue(self.audit()["nodes"])
        self.assertLess(text.index(first), text.index(second))

    def test_render_cli_prepares_unmarked_adoption_without_writes(self):
        self.node()
        config = self.workspace / "spec/__ncf__.md"
        self.write("spec/__ncf__.md", config.read_text().replace('specification_compatibility_version: "1"\n', ""))
        (self.workspace / "spec/__catalogue__.md").unlink()
        before = {path: path.read_bytes() for path in self.workspace.rglob("*") if path.is_file()}
        run = subprocess.run([sys.executable, "-B", str(SCRIPT), "--workspace", str(self.workspace), "--root", "spec", "--render-catalogue"], capture_output=True, text=True, encoding="utf-8", check=False)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertTrue(run.stdout.startswith("# Specification catalogue\n"))
        self.assertIn("does not validate compatibility", run.stderr)
        self.assertEqual(before, {path: path.read_bytes() for path in self.workspace.rglob("*") if path.is_file()})
        self.assertEqual(self.audit()["compatibility"]["state"], "unmarked")

    def test_render_cli_refuses_structural_errors(self):
        self.branch("spec", ["a", "b"])
        identity = self.node("spec/a")
        self.node("spec/b", identity=identity)
        run = subprocess.run([sys.executable, "-B", str(SCRIPT), "--root", str(self.workspace / "spec"), "--render-catalogue"], capture_output=True, text=True, encoding="utf-8", check=False)
        self.assertEqual(run.returncode, 2)
        self.assertIn("blocked by tree errors", json.loads(run.stdout)["fatal"])

    def test_audit_and_render_preserve_identity_product_approval_and_unknowns(self):
        identity = self.node()
        config = self.workspace / "spec/__ncf__.md"
        self.write("spec/__ncf__.md", config.read_text().replace("status: draft", "status: approved") + "\nApproval history: human decision SOURCE-7.\n")
        self.write("spec/content.md", "# Requirement REQ-1\nHuman approved SOURCE-7.\nUnknown: retention decision remains unresolved.\n")
        baseline = self.write("baseline.json", json.dumps(self.audit()))
        before = {path: path.read_bytes() for path in self.workspace.rglob("*") if path.is_file()}
        result = self.audit(baseline=baseline)
        render_catalogue(result["nodes"])
        self.assertEqual(result["identity_changes"], [])
        self.assertEqual(result["nodes"][0]["id"], identity)
        self.assertEqual(before, {path: path.read_bytes() for path in self.workspace.rglob("*") if path.is_file()})

    def test_catalogue_symlink_is_never_followed_or_rendered(self):
        self.node()
        target = self.workspace / "spec/__catalogue__.md"
        target.unlink()
        outside = self.write("outside.md", "# Untrusted external catalogue\n")
        try:
            target.symlink_to(outside)
        except OSError as error:
            self.skipTest(f"Symlink creation not permitted: {error}")
        self.assertTrue({"reparse-point", "catalogue-unreadable"} <= self.codes(self.audit()))
        self.assertEqual(outside.read_text(), "# Untrusted external catalogue\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
