"""Fixture tests: python -B test_audit_specification.py (no external packages)."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import uuid

sys.dont_write_bytecode = True
from audit_specification import Audit, inside, locate_root  # noqa: E402


SCRIPT = Path(__file__).with_name("audit_specification.py")


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="hai-spec-audit-")
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.write(".hai_brain/concepts/specification.md", "[Requirements](../conventions/functional-requirements_conv.md)\n")
        self.write(".hai_brain/conventions/functional-requirements_conv.md", "## Content file\n\n`content.md`, in Markdown.\n")

    def write(self, path, text):
        target = self.workspace / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8"))
        return target

    def node(self, path="spec", kind="leaf", identity=None, body=""):
        identity = identity or str(uuid.uuid4())
        text = f"---\nid: {identity}\ntitle: Test node\nkind: {kind}\n"
        if kind == "leaf":
            text += "type: functional-requirements\nstatus: draft\n"
        self.write(f"{path}/__ncf__.md", text + "---\n" + body)
        if kind == "leaf":
            self.write(f"{path}/content.md", "# Test content\n")
        return identity

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
            self.assertEqual(self.audit()["summary"]["errors"], 0)

    def test_registered_type_and_status_are_case_sensitive(self):
        self.node()
        config = self.workspace / "spec/__ncf__.md"
        self.write("spec/__ncf__.md", config.read_text().replace("functional-requirements", "Functional-Requirements").replace("status: draft", "status: unknown"))
        self.assertTrue({"leaf-type", "status"} <= self.codes(self.audit()))

    def test_dynamic_convention_content_filename(self):
        self.node()
        self.write(".hai_brain/conventions/functional-requirements_conv.md", "## Content file\n\n`payload.json`\n")
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
