"""Behavioral fixtures and real CLI checks for bounded, read-only startup."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import startup_check as startup

SCRIPT = Path(startup.__file__).resolve()
TEMPLATE = SCRIPT.parents[2] / "agents/environment-manager/templates/state.json"
DEFAULT = json.loads(TEMPLATE.read_text(encoding="utf-8"))


class StartupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hai_startup_")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.state = copy.deepcopy(DEFAULT)
        self.write(startup.TEMPLATE, TEMPLATE.read_text(encoding="utf-8"))
        self.write(".hai/agents/leader/SKILL.md", "This is deliberately not a parsed definition.")
        self.table(".hai", [("leader", "Call to coordinate.", "leader/SKILL.md")])
        self.write(startup.INSTRUCTIONS, "")
        self.save_state()

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8"))
        return path

    def save_state(self):
        self.write(".hai_env/state.json", json.dumps(self.state))

    def table(self, origin, entries, newline="\n"):
        rows = ["# Catalogue", "", "| Agent | Selection guide | Definition |", "| --- | --- | --- |"]
        for name, guide, link in entries:
            label = "knowledge.md" if link.endswith("knowledge.md") else "SKILL.md"
            rows.append(f"| `{name}` | {guide} | [{label}]({link}) |")
        return self.write(f"{origin}/agents/catalogue.md", newline.join(rows) + newline)

    def profiles(self, text=None):
        return self.write(".hai_env/model_profiles.json", text or json.dumps({
            "format_version": 1, "models": {"light": "one", "standard": "two", "advanced": "three"}}))

    def snapshot(self):
        return {str(path.relative_to(self.root)): path.read_bytes() if path.is_file() else None
                for path in self.root.rglob("*")}

    def test_valid_state_absent_optional_files_and_no_writes(self):
        before = self.snapshot()
        result = startup.check(self.root)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["environment"], "valid")
        self.assertEqual(result["state_status"], "valid")
        self.assertEqual(result["instructions_status"], "loaded")
        self.assertEqual(result["agent_instructions"]["text"], "")
        self.assertEqual(set(result["features"]), {"requests", "specification", "chronicles"})
        self.assertEqual(result["integrations"], {
            "git": {"enabled": False, "status": "disabled",
                    "auto_push": {"enabled": False, "status": "disabled",
                                  "readiness": "not_checked"}},
            "github": {"enabled": False, "status": "disabled"}})
        self.assertEqual(result["profiles"]["status"], "absent")
        self.assertEqual(result["catalogues"]["workspace"], "absent")
        self.assertEqual([a["name"] for a in result["agents"]], ["leader"])
        self.assertEqual(before, self.snapshot())

    def test_integrations_are_optional_independent_and_returned_as_context(self):
        self.state.pop("integrations", None)
        self.save_state()
        legacy = startup.check(self.root)
        self.assertEqual(legacy["environment"], "valid")
        self.assertEqual(legacy["integrations"], {
            "git": {"enabled": False, "status": "unconfigured",
                    "auto_push": {"enabled": False, "status": "unconfigured",
                                  "readiness": "not_checked"}},
            "github": {"enabled": False, "status": "unconfigured"}})

        self.state["integrations"] = {
            "git": {"enabled": True, "custom_note": "preserved by writers"},
            "github": {"enabled": False}}
        self.save_state()
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "valid")
        self.assertTrue(result["integrations"]["git"]["enabled"])
        self.assertEqual(result["integrations"]["git"]["status"], "enabled")
        self.assertEqual(result["integrations"]["github"],
                         {"enabled": False, "status": "disabled"})
        self.assertEqual(result["integrations"]["git"]["auto_push"],
                         {"enabled": False, "status": "unconfigured",
                          "readiness": "not_checked"})

    def test_auto_push_setting_is_separate_and_never_claims_live_readiness(self):
        self.state["integrations"] = {
            "git": {"enabled": True, "auto_push": {"enabled": True}},
            "github": {"enabled": False}}
        self.save_state()
        result = startup.check(self.root)
        self.assertTrue(result["integrations"]["git"]["enabled"])
        self.assertEqual(result["integrations"]["git"]["auto_push"],
                         {"enabled": True, "status": "enabled",
                          "readiness": "not_checked"})

    def test_malformed_auto_push_isolated_from_git_and_github(self):
        for push in (None, [], {}, {"enabled": 1}, {"enabled": 0}, {"enabled": "true"}):
            with self.subTest(push=push):
                self.state["integrations"] = {
                    "git": {"enabled": True, "auto_push": push},
                    "github": {"enabled": True}}
                self.save_state()
                result = startup.check(self.root)
                self.assertEqual(result["environment"], "valid")
                self.assertTrue(result["integrations"]["git"]["enabled"])
                self.assertEqual(result["integrations"]["git"]["auto_push"],
                                 {"enabled": False, "status": "invalid",
                                  "readiness": "not_checked"})
                self.assertTrue(result["integrations"]["github"]["enabled"])
                self.assertTrue(any(issue["path"] == "integrations.git.auto_push"
                                    for issue in result["issues"]))

    def test_auto_push_requires_enabled_git_integration(self):
        invalid_git_values = [
            {"enabled": False, "auto_push": {"enabled": True}},
            {"auto_push": {"enabled": True}},
            {"enabled": "true", "auto_push": {"enabled": True}},
        ]
        for git in invalid_git_values:
            with self.subTest(git=git):
                self.state["integrations"] = {"git": git, "github": {"enabled": False}}
                self.save_state()
                result = startup.check(self.root)
                self.assertEqual(result["environment"], "valid")
                self.assertFalse(result["integrations"]["git"]["auto_push"]["enabled"])
                self.assertEqual(result["integrations"]["git"]["auto_push"]["status"], "invalid")

    def test_malformed_integrations_are_isolated_from_core_and_instructions(self):
        malformed = [None, [], {"git": {"enabled": "yes"}, "github": {"enabled": True}},
                     {"git": {"enabled": True}, "github": {"enabled": 1}},
                     {"git": {"enabled": 0}, "github": {"enabled": True}},
                     {"git": {}, "github": {"enabled": True}},
                     {"git": {"enabled": True}, "github": None}]
        for configured in malformed:
            with self.subTest(configured=configured):
                self.state["integrations"] = configured
                self.save_state()
                result = startup.check(self.root)
                self.assertEqual(result["environment"], "valid")
                self.assertEqual(result["state_status"], "valid")
                self.assertEqual(result["instructions_status"], "loaded")
                self.assertTrue(any(issue["code"] == "integration" for issue in result["issues"]))
                self.assertFalse(result["ok"])
                for integration in result["integrations"].values():
                    if integration["status"] == "invalid":
                        self.assertFalse(integration["enabled"])
                if isinstance(configured, dict) and isinstance(configured.get("github"), dict):
                    if type(configured["github"].get("enabled")) is bool:
                        self.assertEqual(result["integrations"]["github"]["enabled"],
                                         configured["github"]["enabled"])

    def test_integration_context_is_unverified_when_core_state_is_invalid(self):
        self.write(".hai_env/state.json", "not JSON")
        result = startup.check(self.root)
        self.assertEqual(result["state_status"], "invalid")
        self.assertEqual(result["integrations"], {
            "git": {"enabled": False, "status": "unverified",
                    "auto_push": {"enabled": False, "status": "unverified",
                                  "readiness": "not_checked"}},
            "github": {"enabled": False, "status": "unverified"}})

    def test_missing_instructions_keeps_validated_integration_facts_but_blocks_environment(self):
        self.state["integrations"] = {"git": {"enabled": True}, "github": {"enabled": True}}
        self.save_state()
        (self.root / startup.INSTRUCTIONS).unlink()
        result = startup.check(self.root)
        self.assertEqual(result["state_status"], "valid")
        self.assertEqual(result["instructions_status"], "missing")
        self.assertEqual(result["environment"], "invalid")
        self.assertTrue(result["integrations"]["git"]["enabled"])
        self.assertTrue(result["integrations"]["github"]["enabled"])

    def test_absent_supported_integration_entry_is_unconfigured(self):
        self.state["integrations"] = {"git": {"enabled": True}, "future": {"enabled": True}}
        self.save_state()
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "valid")
        self.assertEqual(result["integrations"]["git"],
                         {"enabled": True, "status": "enabled",
                          "auto_push": {"enabled": False, "status": "unconfigured",
                                        "readiness": "not_checked"}})
        self.assertEqual(result["integrations"]["github"],
                         {"enabled": False, "status": "unconfigured"})
        self.state["integrations"] = {"github": {"enabled": False}}
        self.save_state()
        result = startup.check(self.root)
        self.assertEqual(result["integrations"]["git"]["auto_push"],
                         {"enabled": False, "status": "unconfigured",
                          "readiness": "not_checked"})
        self.assertTrue(result["ok"], result)

    def test_absent_state_is_not_initialized_and_preserves_container(self):
        (self.root / ".hai_env/state.json").unlink()
        self.write(".hai_env/independent.txt", "preserve")
        before = self.snapshot()
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "absent")
        self.assertFalse(result["ok"])
        self.assertEqual(before, self.snapshot())

    def test_absent_container_is_not_created(self):
        (self.root / ".hai_env/state.json").unlink()
        (self.root / startup.INSTRUCTIONS).unlink()
        (self.root / ".hai_env").rmdir()
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "absent")
        self.assertFalse((self.root / ".hai_env").exists())

    def test_duplicate_keys_at_root_and_nested_depth(self):
        for text in ('{"compatible_version":4,"compatible_version":4,"features":{}}',
                     json.dumps(self.state).replace('"enabled": false', '"enabled": false,"enabled": true', 1)):
            with self.subTest(text=text):
                self.write(".hai_env/state.json", text)
                self.assertEqual(startup.check(self.root)["environment"], "invalid")

    def test_schema_version_legacy_and_types(self):
        cases = [{}, [], {**self.state, "compatible_version": True},
                 {**self.state, "compatible_version": 99}, {**self.state, "agents": {}},
                 {**self.state, "current_request": None}]
        for value in cases:
            with self.subTest(value=value):
                self.write(".hai_env/state.json", json.dumps(value))
                self.assertEqual(startup.check(self.root)["environment"], "invalid")
        self.state["features"]["requests"]["enabled"] = 1
        self.save_state()
        self.assertEqual(startup.check(self.root)["environment"], "invalid")

    def test_template_controls_supported_version(self):
        template = copy.deepcopy(DEFAULT)
        template["compatible_version"] = 17
        self.write(startup.TEMPLATE, json.dumps(template))
        self.assertEqual(startup.check(self.root)["environment"], "invalid")
        self.state["compatible_version"] = 17
        self.save_state()
        self.assertEqual(startup.check(self.root)["environment"], "valid")

    def test_strict_json_rejects_constants_in_unknown_properties(self):
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                self.write(".hai_env/state.json", json.dumps(self.state)[:-1] + ',"extra":' + constant + '}')
                self.assertEqual(startup.check(self.root)["environment"], "invalid")

    def test_disabled_paths_still_reject_unsafe_reserved_and_collisions(self):
        for location in ("/tmp", "C:/data", "\\\\server\\share", "../escape", "data\\requests", ".",
                         " ", ".git/data", ".hai/data", ".hai_env", ".hai_env/state.json",
                         ".hai_env/agents/x", ".hai_env/specifications/nested", "CON", "data. "):
            with self.subTest(location=location):
                self.state["features"]["requests"]["location"] = location
                self.save_state()
                self.assertEqual(startup.check(self.root)["environment"], "invalid")

    def test_types_container_state_and_features(self):
        self.write(".hai_env/requests", "wrong type")
        self.assertEqual(startup.check(self.root)["environment"], "invalid")
        (self.root / ".hai_env/requests").unlink()
        (self.root / ".hai_env/state.json").unlink()
        (self.root / ".hai_env/state.json").mkdir()
        self.assertEqual(startup.check(self.root)["environment"], "invalid")
        (self.root / ".hai_env/state.json").rmdir()
        (self.root / startup.INSTRUCTIONS).unlink()
        (self.root / ".hai_env").rmdir()
        self.write(".hai_env", "wrong container type")
        self.assertEqual(startup.check(self.root)["environment"], "invalid")

    def test_mandatory_unicode_crlf_instructions_always_load(self):
        text = "# Инструкции\r\n\r\nPreserve café.\r\n"
        self.write(".hai_env/agent_instructions.md", text)
        result = startup.check(self.root)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["agent_instructions"]["text"], text)

    def test_missing_mandatory_instructions_is_explicit_and_not_recreated(self):
        (self.root / startup.INSTRUCTIONS).unlink()
        before = self.snapshot()
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "invalid")
        self.assertEqual(result["state_status"], "valid")
        self.assertEqual(result["instructions_status"], "missing")
        self.assertIsNone(result["agent_instructions"])
        self.assertIn("agent_instructions", [i["code"] for i in result["issues"]])
        self.assertTrue(result["agents"])
        self.assertEqual(before, self.snapshot())

    def test_wrong_type_invalid_utf8_and_unreadable_instructions_fail(self):
        path = self.root / startup.INSTRUCTIONS
        path.unlink()
        path.mkdir()
        self.assertEqual(startup.check(self.root)["instructions_status"], "invalid")
        path.rmdir()
        path.write_bytes(b"\xff\xfe")
        self.assertEqual(startup.check(self.root)["instructions_status"], "invalid")
        path.write_bytes(b"")
        original_open = Path.open
        def denied(candidate, *args, **kwargs):
            if candidate == path:
                raise PermissionError("Fixture denies access to mandatory instructions")
            return original_open(candidate, *args, **kwargs)
        with patch.object(Path, "open", denied):
            result = startup.check(self.root)
        self.assertEqual(result["instructions_status"], "invalid")
        self.assertEqual(result["state_status"], "valid")
        self.assertFalse(result["ok"])

    def test_retired_setting_rejected_in_v5_without_writes(self):
        self.state["features"]["agent_instructions"] = {
            "enabled": False, "location": ".hai_env/alternate.md"}
        self.save_state()
        before = self.snapshot()
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "invalid")
        self.assertEqual(result["instructions_status"], "loaded")
        self.assertEqual(before, self.snapshot())

    def test_v4_is_not_silently_migrated_and_preserves_legacy_content(self):
        self.state["compatible_version"] = 4
        self.state["features"]["agent_instructions"] = {
            "enabled": True, "location": "legacy/instructions.md"}
        self.write("legacy/instructions.md", "Preserve custom legacy instructions.")
        self.write(startup.INSTRUCTIONS, "Canonical instructions remain active.")
        self.save_state()
        before = self.snapshot()
        result = startup.check(self.root)
        self.assertEqual(result["state_status"], "invalid")
        self.assertEqual(result["agent_instructions"]["text"], "Canonical instructions remain active.")
        self.assertEqual(before, self.snapshot())

    def test_instructions_load_with_absent_or_invalid_state(self):
        self.write(startup.INSTRUCTIONS, "Always apply this instruction.")
        self.write(".hai_env/state.json", "bad JSON")
        result = startup.check(self.root)
        self.assertEqual(result["state_status"], "invalid")
        self.assertEqual(result["agent_instructions"]["text"], "Always apply this instruction.")
        (self.root / ".hai_env/state.json").unlink()
        result = startup.check(self.root)
        self.assertEqual(result["state_status"], "absent")
        self.assertEqual(result["instructions_status"], "loaded")

    def test_feature_cannot_overlap_mandatory_file_even_when_disabled(self):
        for location in (startup.INSTRUCTIONS, startup.INSTRUCTIONS + "/nested"):
            with self.subTest(location=location):
                self.state["features"]["requests"]["location"] = location
                self.save_state()
                self.assertEqual(startup.check(self.root)["state_status"], "invalid")

    def test_startup_does_not_enumerate_optional_stores_or_parse_definitions(self):
        self.state["features"]["requests"]["enabled"] = True
        self.save_state()
        self.write(".hai_env/requests/secret/record.md", "invalid lifecycle data")
        with patch.object(Path, "iterdir", side_effect=AssertionError("No directory scans allowed")):
            result = startup.check(self.root)
        self.assertTrue(result["ok"], result)

    def test_catalogue_bad_rows_keep_independent_entries_and_decode_guides(self):
        self.write(".hai_env/agents/good/SKILL.md", "No YAML loaded")
        self.table(".hai_env", [("good", "Call: A &amp; B &#124; C &#92; D.", "good/SKILL.md"),
                                ("missing", "Call missing.", "missing/SKILL.md"),
                                ("leader", "Conflict.", "leader/SKILL.md"),
                                ("legacy", "Legacy.", "legacy/knowledge.md")], "\r\n")
        result = startup.check(self.root)
        self.assertEqual(result["catalogues"]["workspace"], "partial")
        self.assertEqual([a["name"] for a in result["agents"]], ["leader", "good"])
        self.assertEqual(result["agents"][1]["selection_guide"], "Call: A & B | C \\ D.")
        self.assertEqual(len(result["issues"]), 3)

    def test_duplicate_names_exclude_all_rows_including_case_conflicts(self):
        self.write(".hai_env/agents/good/SKILL.md", "content")
        self.table(".hai_env", [("good", "One.", "good/SKILL.md"),
                                ("Good", "Two.", "Good/SKILL.md")])
        result = startup.check(self.root)
        self.assertEqual([a["name"] for a in result["agents"]], ["leader"])
        self.assertEqual(len(result["issues"]), 2)

    def test_malformed_whole_catalogue_and_isolated_row(self):
        self.write(".hai_env/agents/good/SKILL.md", "content")
        path = self.table(".hai_env", [("good", "Call.", "good/SKILL.md")])
        path.write_text(path.read_text() + "| malformed |\n", encoding="utf-8")
        result = startup.check(self.root)
        self.assertEqual(result["catalogues"]["workspace"], "partial")
        self.assertEqual([a["name"] for a in result["agents"]], ["leader", "good"])
        path.write_text("| Bad | Header |\n| --- | --- |\n", encoding="utf-8")
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "valid")
        self.assertEqual(result["catalogues"]["workspace"], "invalid")

    def test_invalid_framework_prevents_guessing_workspace_collisions(self):
        self.write(".hai/agents/catalogue.md", "malformed")
        self.assertEqual(startup.check(self.root)["catalogues"]["workspace"], "unverified")

    def test_fenced_example_is_not_a_registration_table(self):
        path = self.root / ".hai/agents/catalogue.md"
        table = path.read_text(encoding="utf-8")
        path.write_text("```markdown\n" + table + "```\n", encoding="utf-8")
        self.assertEqual(startup.check(self.root)["catalogues"]["framework"], "invalid")
        path.write_text("~~~markdown\n" + table + "~~~\n\n" + table, encoding="utf-8")
        self.assertEqual(startup.check(self.root)["catalogues"]["framework"], "valid")

    def test_invalid_core_does_not_load_workspace_catalogue_but_loads_instructions(self):
        self.write(".hai_env/state.json", "bad JSON")
        self.write(".hai_env/agents/catalogue.md", "malformed")
        result = startup.check(self.root)
        self.assertEqual(result["catalogues"]["workspace"], "unverified")
        self.assertEqual([i["code"] for i in result["issues"]], ["state"])
        self.assertEqual(result["instructions_status"], "loaded")
        self.assertTrue(result["agents"])

    def test_profiles_schema_duplicates_and_overlap_are_isolated(self):
        self.profiles()
        result = startup.check(self.root)
        self.assertEqual(result["profiles"]["status"], "valid")
        self.assertEqual(result["profiles"]["runtime_availability"], "not_checked")
        for text in ('{"format_version":1,"models":{}}',
                     '{"format_version":1,"format_version":1,"models":{}}'):
            with self.subTest(text=text):
                self.profiles(text)
                result = startup.check(self.root)
                self.assertEqual(result["environment"], "valid")
                self.assertEqual(result["profiles"]["status"], "invalid")
        self.profiles()
        (self.root / startup.INSTRUCTIONS).unlink()
        os.link(self.root / ".hai_env/model_profiles.json", self.root / startup.INSTRUCTIONS)
        result = startup.check(self.root)
        self.assertEqual(result["state_status"], "valid")
        self.assertEqual(result["instructions_status"], "invalid")
        self.assertEqual(result["profiles"]["status"], "invalid")

    def test_safe_instructions_not_suppressed_by_invalid_profile_path(self):
        actual = startup.safe_path
        def bad_profile(workspace, relative):
            if relative == ".hai_env/model_profiles.json":
                raise startup.Invalid("Fixture: unrelated dangling or escaping profile")
            return actual(workspace, relative)
        with patch.object(startup, "safe_path", side_effect=bad_profile):
            result = startup.check(self.root)
        self.assertEqual(result["environment"], "valid")
        self.assertEqual(result["instructions_status"], "loaded")
        self.assertEqual(result["profiles"]["status"], "invalid")

    def make_link(self, relative, target, directory=False):
        link = self.root / relative
        link.parent.mkdir(parents=True, exist_ok=True)
        try:
            link.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Symlink creation unavailable: {exc}")
        return link

    def test_dangling_state_link_is_invalid_not_absent(self):
        (self.root / ".hai_env/state.json").unlink()
        self.make_link(".hai_env/state.json", self.root / "missing.json")
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "invalid")
        self.assertEqual(result["instructions_status"], "loaded")

    def test_dangling_or_escaping_instructions_link_is_invalid(self):
        (self.root / startup.INSTRUCTIONS).unlink()
        link = self.make_link(startup.INSTRUCTIONS, self.root / "missing-instructions.md")
        self.assertEqual(startup.check(self.root)["instructions_status"], "invalid")
        link.unlink()
        with tempfile.TemporaryDirectory(prefix="hai_outside_instructions_") as outside:
            target = Path(outside) / "instructions.md"
            target.write_text("outside", encoding="utf-8")
            self.make_link(startup.INSTRUCTIONS, target)
            self.assertEqual(startup.check(self.root)["instructions_status"], "invalid")

    def test_instructions_alias_to_state_is_invalid(self):
        (self.root / startup.INSTRUCTIONS).unlink()
        os.link(self.root / ".hai_env/state.json", self.root / startup.INSTRUCTIONS)
        result = startup.check(self.root)
        self.assertEqual(result["instructions_status"], "invalid")
        self.assertFalse(result["ok"])

    def test_dangling_ancestor_is_invalid_even_with_absent_descendant(self):
        self.make_link("dangling", self.root / "missing", True)
        self.state["features"]["requests"]["location"] = "dangling/requests"
        self.save_state()
        self.assertEqual(startup.check(self.root)["environment"], "invalid")

    def test_escaping_feature_link_and_safe_alias_collision(self):
        with tempfile.TemporaryDirectory(prefix="hai_outside_") as outside:
            link = self.make_link("escape", Path(outside), True)
            self.state["features"]["requests"]["location"] = "escape/missing"
            self.save_state()
            self.assertEqual(startup.check(self.root)["environment"], "invalid")
            link.unlink()
        (self.root / "shared").mkdir()
        self.make_link("alias", self.root / "shared", True)
        self.state["features"]["requests"]["location"] = "shared/requests"
        self.state["features"]["specification"]["location"] = "alias/requests/spec"
        self.save_state()
        self.assertEqual(startup.check(self.root)["environment"], "invalid")

    def test_escaping_catalogue_reference_is_excluded(self):
        with tempfile.TemporaryDirectory(prefix="hai_definition_") as outside:
            target = Path(outside) / "SKILL.md"
            target.write_text("outside", encoding="utf-8")
            self.make_link(".hai_env/agents/escape/SKILL.md", target)
            self.table(".hai_env", [("escape", "Call.", "escape/SKILL.md")])
            result = startup.check(self.root)
            self.assertEqual([a["name"] for a in result["agents"]], ["leader"])
            self.assertEqual(result["catalogues"]["workspace"], "partial")

    @unittest.skipUnless(os.name == "nt", "Windows junction behavior")
    def test_windows_escaping_junction_with_absent_descendant(self):
        with tempfile.TemporaryDirectory(prefix="hai_junction_") as outside:
            link = self.root / "junction"
            proc = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), outside], capture_output=True)
            if proc.returncode:
                self.skipTest("Junction creation unavailable")
            self.addCleanup(lambda: link.rmdir() if link.exists() else None)
            self.state["features"]["requests"]["location"] = "junction/not-created"
            self.save_state()
            self.assertEqual(startup.check(self.root)["environment"], "invalid")

    @unittest.skipUnless(os.name == "nt", "Windows junction behavior")
    def test_windows_bad_profile_junction_does_not_suppress_instructions(self):
        with tempfile.TemporaryDirectory(prefix="hai_profile_junction_") as outside:
            target = Path(outside) / "target"
            target.mkdir()
            link = self.root / ".hai_env/model_profiles.json"
            proc = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True)
            if proc.returncode:
                self.skipTest("Junction creation unavailable")
            try:
                for dangling in (False, True):
                    with self.subTest(dangling=dangling):
                        if dangling:
                            target.rmdir()
                        result = startup.check(self.root)
                        self.assertEqual(result["environment"], "valid")
                        self.assertEqual(result["instructions_status"], "loaded")
                        self.assertEqual(result["profiles"]["status"], "invalid")
            finally:
                link.rmdir()

    def test_case_sensitive_or_insensitive_collisions_follow_filesystem(self):
        (self.root / "Feature").mkdir()
        self.state["features"]["requests"]["location"] = "Feature"
        self.state["features"]["specification"]["location"] = "feature"
        self.save_state()
        result = startup.check(self.root)
        expected = "invalid" if (self.root / "feature").exists() else "valid"
        self.assertEqual(result["environment"], expected)

    def test_cli_isolated_read_only_and_exit_codes(self):
        before = self.snapshot()
        def run(workspace):
            return subprocess.run([sys.executable, "-I", "-S", str(SCRIPT), "--workspace", str(workspace)],
                                  capture_output=True, text=True, encoding="utf-8")
        proc = run(self.root)
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertTrue(json.loads(proc.stdout)["ok"])
        self.assertEqual(before, self.snapshot())
        (self.root / ".hai_env/state.json").unlink()
        proc = run(self.root)
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["environment"], "absent")
        proc = run(self.root / "not-existing")
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["issues"][0]["code"], "input")


if __name__ == "__main__":
    unittest.main(verbosity=2)
