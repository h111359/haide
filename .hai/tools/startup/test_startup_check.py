"""Behavioral fixtures and real CLI checks for bounded, read-only startup."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shutil
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
        self.state = {"state_format_version": 3, **copy.deepcopy(DEFAULT)}
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

    def register_specification_manager(self, settings=None, contract=None):
        self.write(".hai_env/agents/specification-manager/SKILL.md", "Not parsed during startup.")
        contract = contract or {
            "contract_format_version": 2, "agent": "specification-manager",
            "current_config_format_version": 1, "supported_config_format_versions": [1],
            "settings": {"enabled": {"type": "boolean", "default": False},
                         "location": {"type": "workspace-relative-directory",
                                      "default": ".hai_env/specifications"}},
        }
        self.write(".hai_env/agents/specification-manager/configuration/contract.json", json.dumps(contract))
        self.table(".hai_env", [("specification-manager", "Manage durable specifications.",
                                  "specification-manager/SKILL.md")])
        if settings is not None:
            self.write(".hai_env/config/agents/specification-manager.json", json.dumps({
                "config_format_version": 1, "settings": settings}))

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
        self.assertEqual(result["state_format_version"], 3)
        self.assertEqual(result["activities"], {"location": ".hai_env/activities", "available": False, "target_type": "directory"})
        self.assertEqual(set(result["features"]), {"chronicles"})
        self.assertEqual(result["agent_configurations"]["specification-manager"]["status"], "unavailable")
        self.assertEqual(result["features"]["chronicles"],
                         {"enabled": False, "record_every_prompts": 5})
        self.assertNotIn("integrations", result)
        self.assertEqual(result["profiles"]["status"], "absent")
        self.assertEqual(result["catalogues"]["workspace"], "absent")
        self.assertEqual([a["name"] for a in result["agents"]], ["leader"])
        self.assertEqual(before, self.snapshot())

    def test_registered_specification_defaults_and_configured_values_are_bounded(self):
        self.register_specification_manager()
        before = self.snapshot()
        result = startup.check(self.root)
        self.assertTrue(result["ok"], result)
        status = result["agent_configurations"]["specification-manager"]
        self.assertEqual(status["status"], "defaulted")
        self.assertEqual(status["settings"], {"enabled": False, "location": ".hai_env/specifications"})
        self.assertEqual(before, self.snapshot())

        self.register_specification_manager(settings={"enabled": True, "location": "docs/specs"})
        (self.root / "docs/specs").mkdir(parents=True)
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "valid")
        self.assertTrue(result["agent_configurations"]["specification-manager"]["settings"]["enabled"])
        self.assertEqual(result["agent_configurations"]["specification-manager"]["settings"]["location"], "docs/specs")

    def test_invalid_spec_configuration_is_isolated_and_has_no_active_values(self):
        self.register_specification_manager(settings={"enabled": "true", "location": ".hai_env/specifications"})
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "valid")
        self.assertEqual(result["state_status"], "valid")
        self.assertEqual(result["agent_configurations"]["specification-manager"]["status"], "invalid")
        self.assertEqual(result["agent_configurations"]["specification-manager"]["settings"], {})
        self.assertFalse(result["ok"])

    def test_core_startup_without_optional_extension_or_executable(self):
        self.state.pop("integrations", None)
        self.save_state()
        self.assertFalse((self.root / ".hai/agents/git-manager").exists())
        self.assertFalse((self.root / ".hai_env/agents/git-manager").exists())
        before = self.snapshot()
        with patch.dict(os.environ, {"PATH": ""}), patch.object(
                subprocess, "Popen", side_effect=AssertionError("No external process is needed")):
            result = startup.check(self.root)
        self.assertTrue(result["ok"], result)
        self.assertNotIn("integrations", result)
        environment = dict(os.environ, PATH="")
        proc = subprocess.run([sys.executable, "-I", "-S", "-B", str(SCRIPT),
                               "--workspace", str(self.root)], cwd=self.root, env=environment,
                              capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertTrue(json.loads(proc.stdout)["ok"])
        self.assertEqual(before, self.snapshot())

    def test_opaque_extension_values_are_not_consulted_or_changed(self):
        self.state.pop("integrations", None)
        self.save_state()
        baseline = startup.check(self.root)
        for configured in (None, [], False, "legacy", {"enabled": "not a core field"},
                           {"git": {"enabled": "yes", "auto_push": []}, "github": None}):
            with self.subTest(configured=configured):
                self.state["integrations"] = configured
                self.state["future_extension"] = {"owned": [1, None, {"anything": True}]}
                self.save_state()
                before = self.snapshot()
                result = startup.check(self.root)
                self.assertEqual(result, baseline)
                self.assertEqual(before, self.snapshot())

    def test_template_needs_no_extension_defaults(self):
        self.assertNotIn("integrations", DEFAULT)
        template = copy.deepcopy(DEFAULT)
        template.pop("integrations", None)
        self.write(startup.TEMPLATE, json.dumps(template))
        self.assertTrue(startup.check(self.root)["ok"])
        for opaque in (None, [], {"enabled": "arbitrary"}):
            with self.subTest(opaque=opaque):
                template["future_extension"] = opaque
                self.write(startup.TEMPLATE, json.dumps(template))
                self.assertTrue(startup.check(self.root)["ok"])

    def test_optional_workspace_extension_requires_catalogue_registration(self):
        self.write('.hai_env/agents/git-manager/SKILL.md', 'Not parsed during startup.')
        before = startup.check(self.root)
        self.assertEqual([agent['name'] for agent in before['agents']], ['leader'])
        self.assertEqual(before['catalogues']['workspace'], 'absent')
        self.table('.hai_env', [('git-manager', 'Operate the optional extension.', 'git-manager/SKILL.md')])
        result = startup.check(self.root)
        self.assertTrue(result['ok'], result)
        entry = next(agent for agent in result['agents'] if agent['name'] == 'git-manager')
        self.assertEqual(entry['origin'], '.hai_env')
        self.assertEqual(entry['definition'], '.hai_env/agents/git-manager/SKILL.md')
        self.assertNotIn('integrations', result)

    def test_unknown_extension_data_does_not_mask_invalid_core(self):
        self.state["integrations"] = {"unknown": "opaque"}
        self.state["features"]["specification"] = {"enabled": False,
                                                       "location": ".hai_env/specifications"}
        self.save_state()
        before = self.snapshot()
        result = startup.check(self.root)
        self.assertEqual(result["state_status"], "invalid")
        self.assertNotIn("integrations", result)
        self.assertTrue(any(issue["code"] == "state" for issue in result["issues"]))
        self.assertFalse(any(issue["code"] == "integration" for issue in result["issues"]))
        self.assertEqual(before, self.snapshot())

    def test_missing_instructions_block_core_without_extension_interpretation(self):
        self.state["integrations"] = ["opaque", {"enabled": "not a core value"}]
        self.save_state()
        (self.root / startup.INSTRUCTIONS).unlink()
        before = self.snapshot()
        result = startup.check(self.root)
        self.assertEqual(result["state_status"], "valid")
        self.assertEqual(result["instructions_status"], "missing")
        self.assertEqual(result["environment"], "invalid")
        self.assertNotIn("integrations", result)
        self.assertEqual(before, self.snapshot())

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
        for text in ('{"state_format_version":1,"state_format_version":1,"features":{}}',
                     json.dumps(self.state).replace('"enabled": false', '"enabled": false,"enabled": true', 1)):
            with self.subTest(text=text):
                self.write(".hai_env/state.json", text)
                self.assertEqual(startup.check(self.root)["environment"], "invalid")

    def test_schema_version_legacy_and_types(self):
        cases = [{}, [], {**self.state, "state_format_version": True},
                 {**self.state, "state_format_version": 0},
                 {**self.state, "state_format_version": 99},
                 {**self.state, "compatible_version": 1}, {**self.state, "agents": {}},
                 {**self.state, "current_request": None}, {**self.state, "current_activity": "x"}, {**self.state, "requests": {}},
                 {**self.state, "features": {**self.state["features"], "requests": {"enabled": False, "location": ".hai_env/requests"}}}]
        for value in cases:
            with self.subTest(value=value):
                self.write(".hai_env/state.json", json.dumps(value))
                self.assertEqual(startup.check(self.root)["environment"], "invalid")
        self.state["features"]["specification"] = {"enabled": 1,
                                                       "location": ".hai_env/specifications"}
        self.save_state()
        self.assertEqual(startup.check(self.root)["environment"], "invalid")

    def test_contract_is_installed_authority_and_contract_errors_fail_core_state(self):
        # A target workspace copy cannot override the contract shipped with this helper.
        self.write(".hai/agents/environment-manager/contract.json",
                   json.dumps({"current_state_format_version": 99,
                               "supported_state_format_versions": [99]}))
        self.assertEqual(startup.check(self.root)["environment"], "valid")
        contract_path = self.root / "installed/contract.json"
        contract_path.parent.mkdir(parents=True)
        valid = {"current_state_format_version": 3,
                 "supported_state_format_versions": [2, 3]}
        with patch.object(startup, "CONTRACT", contract_path):
            result = startup.check(self.root)
            self.assertEqual(result["state_status"], "invalid")
            self.assertEqual(result["instructions_status"], "loaded")
            self.assertIn("contract", result["issues"][0]["message"].lower())
            contract_path.write_text(json.dumps(valid), encoding="utf-8")
            original_open = Path.open
            def denied(candidate, *args, **kwargs):
                if candidate == contract_path:
                    raise PermissionError("Fixture denies installed contract access")
                return original_open(candidate, *args, **kwargs)
            with patch.object(Path, "open", denied):
                result = startup.check(self.root)
            self.assertEqual(result["state_status"], "invalid")
            self.assertEqual(result["instructions_status"], "loaded")
            self.assertIn("contract", result["issues"][0]["message"].lower())
        invalid_contracts = [
            "{\"current_state_format_version\":1,\"current_state_format_version\":1,\"supported_state_format_versions\":[1]}",
            {}, [], {**valid, "current_state_format_version": True},
            {**valid, "supported_state_format_versions": []},
            {**valid, "supported_state_format_versions": [2, 2]},
            {**valid, "supported_state_format_versions": [True]},
            {**valid, "extra": "ignored fields are not allowed"},
        ]
        with patch.object(startup, "CONTRACT", contract_path):
            for invalid in invalid_contracts:
                with self.subTest(contract=invalid):
                    contract_path.write_text(invalid if isinstance(invalid, str)
                                             else json.dumps(invalid), encoding="utf-8")
                    result = startup.check(self.root)
                    self.assertEqual(result["state_status"], "invalid")
                    self.assertEqual(result["instructions_status"], "loaded")
                    self.assertEqual(result["agent_instructions"]["text"], "")
                    self.assertIn("contract", result["issues"][0]["message"].lower())
            contract_path.write_text(json.dumps(valid), encoding="utf-8")
            self.state["state_format_version"] = 2
            self.state["features"]["specification"] = {"enabled": False,
                                                          "location": ".hai_env/specifications"}
            self.save_state()
            self.assertEqual(startup.check(self.root)["state_status"], "valid")

    def test_strict_json_rejects_constants_in_unknown_properties(self):
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                self.write(".hai_env/state.json", json.dumps(self.state)[:-1] + ',"extra":' + constant + '}')
                self.assertEqual(startup.check(self.root)["environment"], "invalid")

    def test_disabled_paths_still_reject_unsafe_reserved_and_collisions(self):
        for location in ("/tmp", "C:/data", "\\\\server\\share", "../escape", "data\\activities", ".",
                         " ", ".git/data", ".hai/data", ".hai_env", ".hai_env/state.json",
                         ".hai_env/agents/x", "CON", "data. "):
            with self.subTest(location=location):
                self.register_specification_manager(settings={"enabled": False, "location": location})
                result = startup.check(self.root)
                self.assertEqual(result["environment"], "valid")
                self.assertEqual(result["agent_configurations"]["specification-manager"]["status"], "invalid")

    def test_types_container_state_and_features(self):
        self.register_specification_manager()
        self.write(".hai_env/specifications", "wrong type")
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "valid")
        self.assertEqual(result["agent_configurations"]["specification-manager"]["status"], "invalid")
        (self.root / ".hai_env/specifications").unlink()
        (self.root / ".hai_env/state.json").unlink()
        (self.root / ".hai_env/state.json").mkdir()
        self.assertEqual(startup.check(self.root)["environment"], "invalid")
        (self.root / ".hai_env/state.json").rmdir()
        (self.root / startup.INSTRUCTIONS).unlink()
        shutil.rmtree(self.root / ".hai_env")
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

    def test_legacy_settings_have_specific_diagnostics(self):
        legacy_cases = [
            ({**self.state, "features": {**self.state["features"], "requests": {"enabled": False, "location": ".hai_env/requests"}}}, "features.requests"),
            ({**self.state, "features": {**self.state["features"], "agent_instructions": {"enabled": False, "location": "elsewhere"}}}, "features.agent_instructions"),
            ({**self.state, "features": {**self.state["features"], "chronicles": {"enabled": False, "location": ".hai_env/chronicles"}}}, "global features.chronicles.location"),
        ]
        for value, expected in legacy_cases:
            with self.subTest(expected=expected):
                self.write(".hai_env/state.json", json.dumps(value))
                result = startup.check(self.root)
                self.assertEqual(result["state_status"], "invalid")
                state_issue = next(issue for issue in result["issues"] if issue["code"] == "state")
                self.assertIn(expected, state_issue["message"])

    def test_format2_reports_migration_without_effective_specification_fallback(self):
        self.state["state_format_version"] = 2
        self.state["features"]["specification"] = {"enabled": True,
                                                       "location": ".hai_env/specifications"}
        self.write(".hai_env/activities/one/chronicles/session.md", "transcript")
        self.state["features"]["chronicles"]["enabled"] = True
        self.save_state()
        before = self.snapshot()
        result = startup.check(self.root)
        self.assertEqual(result["activities"]["available"], True)
        self.assertTrue(result["features"]["chronicles"]["enabled"])
        self.assertEqual(result["migration_required"]["status"], "required")
        self.assertEqual(result["agent_configurations"]["specification-manager"]["status"], "migration_required")
        self.assertNotIn("specification", result["features"])
        self.assertEqual(before, self.snapshot())
        self.state["features"]["chronicles"]["location"] = ".hai_env/chronicles"
        self.save_state()
        result = startup.check(self.root)
        self.assertEqual(result["state_status"], "invalid")
        self.assertIn("global features.chronicles.location", result["issues"][0]["message"])

    def test_chronicles_prompt_threshold_defaults_validates_and_propagates(self):
        # Missing chronicles thresholds receive the documented effective default.
        self.state["features"]["chronicles"].pop("record_every_prompts", None)
        self.save_state()
        result = startup.check(self.root)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["features"]["chronicles"],
                         {"enabled": False, "record_every_prompts": 5})

        self.state["features"]["chronicles"]["record_every_prompts"] = 12
        self.save_state()
        result = startup.check(self.root)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["features"]["chronicles"]["record_every_prompts"], 12)

    def test_chronicles_prompt_threshold_rejects_invalid_values_even_when_disabled(self):
        for invalid in (True, False, 0, -1, 1.5, "5", None, [], {}):
            with self.subTest(invalid=invalid):
                self.state["features"]["chronicles"]["enabled"] = False
                self.state["features"]["chronicles"]["record_every_prompts"] = invalid
                self.save_state()
                result = startup.check(self.root)
                self.assertEqual(result["state_status"], "invalid")
                issue = next(issue for issue in result["issues"] if issue["code"] == "state")
                self.assertIn("record_every_prompts", issue["message"])

    def test_activity_store_location_is_configurable_safe_and_preserves_extra_properties(self):
        self.state["activities"] = {"location": "workspace-activities", "note": "keep"}
        (self.root / "workspace-activities").mkdir()
        self.save_state()
        result = startup.check(self.root)
        self.assertEqual(result["activities"], {"location": "workspace-activities", "available": True, "target_type": "directory"})
        self.assertEqual(self.state["activities"]["note"], "keep")
        for location in ("../outside", ".hai", ".hai_env/state.json", ".hai_env/agent_instructions.md") :
            with self.subTest(location=location):
                self.state["activities"] = {"location": location}
                self.save_state()
                self.assertEqual(startup.check(self.root)["state_status"], "invalid")
        self.state["activities"] = {"location": ".hai_env/activities", "enabled": True}
        self.save_state()
        self.assertEqual(startup.check(self.root)["state_status"], "invalid")
        self.state["activities"] = {"location": ".hai_env/activities"}
        self.write(".hai_env/activities", "wrong type")
        self.save_state()
        self.assertEqual(startup.check(self.root)["state_status"], "invalid")

    def test_retired_setting_rejected_without_writes(self):
        self.state["features"]["agent_instructions"] = {"enabled": False, "location": ".hai_env/alternate.md"}
        self.save_state()
        before = self.snapshot()
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "invalid")
        self.assertEqual(result["instructions_status"], "loaded")
        self.assertEqual(before, self.snapshot())

    def test_legacy_field_is_not_silently_accepted_and_preserves_content(self):
        self.state["compatible_version"] = 5
        self.state["features"]["agent_instructions"] = {
            "enabled": True, "location": "legacy/instructions.md"}
        self.write("legacy/instructions.md", "Preserve custom legacy instructions.")
        self.write(startup.INSTRUCTIONS, "Canonical instructions remain active.")
        self.save_state()
        before = self.snapshot()
        result = startup.check(self.root)
        self.assertEqual(result["state_status"], "invalid")
        self.assertIn("compatible_version", result["issues"][0]["message"])
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
                self.register_specification_manager(settings={"enabled": False, "location": location})
                result = startup.check(self.root)
                self.assertEqual(result["state_status"], "valid")
                self.assertEqual(result["agent_configurations"]["specification-manager"]["status"], "invalid")

    def test_core_destinations_cannot_overlap_agent_configuration_storage(self):
        for location in (".hai_env/config", ".hai_env/config/agents"):
            with self.subTest(location=location):
                self.state["activities"] = {"location": location}
                self.save_state()
                result = startup.check(self.root)
                self.assertEqual(result["state_status"], "invalid")
                self.state["activities"] = {"location": ".hai_env/activities"}
        self.save_state()

        self.register_specification_manager(settings={"enabled": False, "location": ".hai_env/config"})
        result = startup.check(self.root)
        self.assertEqual(result["state_status"], "valid")
        self.assertEqual(result["agent_configurations"]["specification-manager"]["status"], "invalid")
        self.register_specification_manager(settings={"enabled": False, "location": ".hai_env/specifications"})
        config_root = self.root / ".hai_env/config"
        config_root.mkdir(parents=True, exist_ok=True)
        profiles = self.root / ".hai_env/model_profiles.json"
        profiles.unlink(missing_ok=True)
        profiles.symlink_to(config_root)
        result = startup.check(self.root)
        self.assertEqual(result["state_status"], "valid")
        self.assertEqual(result["profiles"]["status"], "invalid")

    def test_startup_does_not_enumerate_optional_stores_or_parse_definitions(self):
        self.state["features"]["chronicles"]["enabled"] = True
        self.save_state()
        self.write(".hai_env/activities/secret/record.md", "invalid lifecycle data")
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
        self.register_specification_manager(settings={"enabled": False, "location": "dangling/specs"})
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "valid")
        self.assertEqual(result["agent_configurations"]["specification-manager"]["status"], "invalid")

    def test_escaping_feature_link_and_safe_alias_collision(self):
        with tempfile.TemporaryDirectory(prefix="hai_outside_") as outside:
            link = self.make_link("escape", Path(outside), True)
            self.register_specification_manager(settings={"enabled": False, "location": "escape/missing"})
            result = startup.check(self.root)
            self.assertEqual(result["environment"], "valid")
            self.assertEqual(result["agent_configurations"]["specification-manager"]["status"], "invalid")
            link.unlink()
        (self.root / "shared").mkdir()
        self.make_link("alias", self.root / "shared", True)
        self.state["activities"] = {"location": "shared"}
        self.save_state()
        self.register_specification_manager(settings={"enabled": False, "location": "alias/specs/nested"})
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "valid")
        self.assertEqual(result["agent_configurations"]["specification-manager"]["status"], "invalid")

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
            self.register_specification_manager(settings={"enabled": False, "location": "junction/not-created"})
            result = startup.check(self.root)
            self.assertEqual(result["environment"], "valid")
            self.assertEqual(result["agent_configurations"]["specification-manager"]["status"], "invalid")

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
        self.state["activities"] = {"location": "Feature"}
        self.save_state()
        self.register_specification_manager(settings={"enabled": False, "location": "feature"})
        result = startup.check(self.root)
        expected = "invalid" if (self.root / "feature").exists() else "configured"
        self.assertEqual(result["agent_configurations"]["specification-manager"]["status"], expected)

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
