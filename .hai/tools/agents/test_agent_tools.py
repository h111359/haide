"""Run with python -B test_agent_tools.py; requires PyYAML 6.x."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from agent_tools import HEADINGS, Invalid, audit, read_definition, read_profiles, resolve


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hai-agent-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.definition = ".hai/agents/worker/SKILL.md"
        self.description = "Call to inspect café & pipes | paths \\ and report."
        self.write_definition()
        encoded = self.description.replace("&", "&amp;").replace("\\", "&#92;").replace("|", "&#124;")
        self.catalogue = ("# Agents\n\n| Agent | Selection guide | Definition |\n| --- | --- | --- |\n"
                          f"| `worker` | {encoded} | [SKILL.md](worker/SKILL.md) |\n")
        self.write(".hai/agents/catalogue.md", self.catalogue)
        self.profiles = {"format_version": 1, "models": {"light": "small", "standard": "normal", "advanced": "large"}}
        self.write(".hai_env/model_profiles.json", json.dumps(self.profiles))
        self.runtime = {"models": {"small": ["low", "high"], "normal": ["high"], "large": ["high", "ultra"]}}

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8"))
        return target

    def write_definition(self, name="worker", metadata=None, extra=""):
        metadata = metadata or 'metadata:\n  hai-model-class: "light"\n  hai-reasoning-effort: "high"\n'
        text = (f'---\nname: {name}\ndescription: {json.dumps(self.description)}\n'
                + metadata + extra + '---\n\n' + ''.join(f"## {h}\n\nNone.\n\n" for h in HEADINGS))
        return self.write(self.definition, text)

    def test_audit_exact_decoding_unicode_and_crlf(self):
        for path in self.root.rglob("*.md"):
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        result = audit(self.root)
        self.assertTrue(result["ok"], result)
        self.assertEqual(len(result["agents"]), 1)

    def test_exact_supported_pair(self):
        result = resolve(self.root, self.definition, self.runtime)
        self.assertTrue(result["ok"])
        self.assertEqual(result["request"]["model"], "small")
        self.assertEqual(result["request"]["reasoning_effort"], "high")

    def test_unavailable_effort_never_substitutes(self):
        self.runtime["models"]["small"] = ["low"]
        result = resolve(self.root, self.definition, self.runtime)
        self.assertFalse(result["ok"])
        self.assertEqual(result["request"]["reasoning_effort"], "high")
        self.assertEqual(result["request"]["model"], "small")

    def test_unavailable_model_never_substitutes(self):
        del self.runtime["models"]["small"]
        self.assertFalse(resolve(self.root, self.definition, self.runtime)["ok"])

    def test_missing_profiles_valid_audit_but_no_normal_resolution(self):
        (self.root / ".hai_env/model_profiles.json").unlink()
        self.assertTrue(audit(self.root)["ok"])
        self.assertFalse(resolve(self.root, self.definition, self.runtime)["ok"])
        self.assertFalse((self.root / ".hai_env/model_profiles.json").exists())

    def test_duplicate_json_and_boolean_version_rejected(self):
        path = self.write(".hai_env/model_profiles.json", '{"format_version":1,"format_version":1}')
        with self.assertRaises(Invalid):
            read_profiles(path)
        self.profiles["format_version"] = True
        path.write_text(json.dumps(self.profiles))
        with self.assertRaises(Invalid):
            read_profiles(path)

    def test_duplicate_yaml_and_nonstring_metadata_rejected(self):
        for extra in ('name: worker\n', 'metadata:\n  hai-model-class: true\n  hai-reasoning-effort: high\n'):
            with self.subTest(extra=extra):
                path = self.write_definition(extra=extra)
                with self.assertRaises(Invalid):
                    read_definition(path)
        self.write_definition(metadata='metadata:\n  hai-model-class: true\n  hai-reasoning-effort: high\n')
        self.assertFalse(audit(self.root)["ok"])

    def test_folded_yaml_description_is_canonical_decoded_value(self):
        path = self.write_definition()
        path.write_text(path.read_text().replace('description: ' + json.dumps(self.description),
                                                'description: >-\n  Call to inspect\n  and report.'))
        self.assertEqual(read_definition(path)["description"], "Call to inspect and report.")

    def test_wrong_name_sections_and_h1_rejected(self):
        path = self.write_definition()
        original = path.read_text()
        for text in (original.replace('name: worker', 'name: other'),
                     original.replace('## Scope', '## Purpose'), original + '# Worker\n'):
            path.write_text(text)
            with self.assertRaises(Invalid):
                read_definition(path)

    def test_leader_must_omit_execution_metadata(self):
        self.definition = ".hai/agents/leader/SKILL.md"
        path = self.write_definition(name="leader")
        with self.assertRaises(Invalid):
            read_definition(path)
        self.write_definition(name="leader", metadata="\n")
        self.assertEqual(read_definition(path)["name"], "leader")
        with self.assertRaises(Invalid):
            resolve(self.root, self.definition, self.runtime)

    def test_stale_copy_rejected(self):
        self.write(".hai/agents/catalogue.md", self.catalogue.replace('Call to inspect', 'Call to write'))
        self.assertFalse(audit(self.root)["ok"])

    def test_duplicate_rows_and_workspace_collisions(self):
        self.write(".hai_env/agents/catalogue.md", self.catalogue)
        result = audit(self.root)
        self.assertFalse(result["ok"])
        self.assertEqual(len(result["agents"]), 1)
        self.write(".hai/agents/catalogue.md", self.catalogue + self.catalogue.splitlines()[-1] + '\n')
        self.assertFalse(audit(self.root)["agents"])

    def test_legacy_registration_preserved_and_independent_entry_kept(self):
        text = self.catalogue + '| `old` | Call to help. | [knowledge.md](old/knowledge.md) |\n'
        path = self.write(".hai/agents/catalogue.md", text)
        result = audit(self.root)
        self.assertFalse(result["ok"])
        self.assertEqual(len(result["agents"]), 1)
        self.assertEqual(result["issues"][0]["agent"], "old")
        self.assertEqual(path.read_text(), text)

    def test_old_new_conflict_rejected(self):
        self.write(".hai/agents/worker/knowledge.md", "# Old worker\n")
        self.assertFalse(audit(self.root)["ok"])
        with self.assertRaises(Invalid):
            resolve(self.root, self.definition, self.runtime)

    def test_escaping_symlink_rejected(self):
        with tempfile.TemporaryDirectory(prefix="hai-external-") as external:
            path = self.root / self.definition
            path.unlink()
            outside = Path(external) / "SKILL.md"
            outside.write_text("do not read")
            try:
                path.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks unavailable")
            self.assertFalse(audit(self.root)["ok"])
            with self.assertRaises(Invalid):
                resolve(self.root, self.definition, self.runtime)

    def test_dangling_profile_is_invalid_not_absent(self):
        path = self.root / ".hai_env/model_profiles.json"
        path.unlink()
        try:
            path.symlink_to(self.root / "missing-profile.json")
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable")
        result = audit(self.root)
        self.assertFalse(result["ok"])
        self.assertEqual(result["profiles"], "invalid")

    def test_traversal_and_noncanonical_selected_path_rejected(self):
        for path in ("../outside/SKILL.md", "/tmp/SKILL.md", "C:/SKILL.md", "other/SKILL.md"):
            with self.subTest(path=path), self.assertRaises(Invalid):
                resolve(self.root, path, self.runtime)

    def test_no_mutations_to_state_or_catalogue(self):
        state = self.write(".hai_env/state.json", '{"unrelated":"preserve"}\n')
        before = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        audit(self.root)
        resolve(self.root, self.definition, self.runtime)
        after = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(state.read_text(), '{"unrelated":"preserve"}\n')


if __name__ == "__main__":
    unittest.main()
