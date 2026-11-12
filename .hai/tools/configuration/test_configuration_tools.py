"""Isolated tests for read-only agent configuration loading."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import configuration_tools as config


class ConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hai_configuration_")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.root.joinpath(".hai_env/config").mkdir(parents=True)
        self.root.joinpath(".hai_env/config/agent_instructions.md").write_text("", encoding="utf-8")
        self.contract = {
            "contract_format_version": 1, "agent": "git-manager",
            "current_config_format_version": 1, "supported_config_format_versions": [1],
            "settings": {
                "git.enabled": {"type": "boolean", "default": False},
                "git.auto_push.enabled": {"type": "boolean", "default": True},
                "github.enabled": {"type": "boolean", "default": False},
            },
        }
        self.contract_path = self.root / ".hai_env/agents/git-manager/configuration/contract.json"
        self.contract_path.parent.mkdir(parents=True)
        self.contract_path.write_text(json.dumps(self.contract), encoding="utf-8")
        self.loaded = config.load_contract(self.contract_path, "git-manager")

    def config_path(self):
        return self.root / ".hai_env/config/agents/git-manager.json"

    def result(self):
        return config.read_configuration(self.root, "git-manager", self.loaded)

    def test_missing_file_uses_declared_nested_defaults(self):
        result = self.result()
        self.assertEqual(result["status"], "defaulted")
        self.assertEqual(result["settings"], {
            "git": {"enabled": False, "auto_push": {"enabled": True}},
            "github": {"enabled": False},
        })
        self.assertEqual(result["configured_fields"], [])
        self.assertEqual(result["issues"], [])

    def test_valid_override_returns_only_declared_settings(self):
        path = self.config_path()
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({"config_format_version": 1, "settings": {
            "git": {"enabled": True, "auto_push": {"enabled": False}},
            "github": {"enabled": True}, "future": {"opaque": "ignored"},
        }, "future_envelope": "ignored"}), encoding="utf-8")
        result = self.result()
        self.assertEqual(result["status"], "configured")
        self.assertEqual(result["settings"], {
            "git": {"enabled": True, "auto_push": {"enabled": False}},
            "github": {"enabled": True},
        })
        self.assertEqual(result["configured_fields"], [
            "git.enabled", "git.auto_push.enabled", "github.enabled"])

    def test_missing_leaf_uses_default_but_wrong_container_or_leaf_is_invalid(self):
        path = self.config_path()
        path.parent.mkdir(parents=True)
        path.write_text('{"config_format_version":1,"settings":{"git":{"enabled":true}}}', encoding="utf-8")
        result = self.result()
        self.assertEqual(result["status"], "configured")
        self.assertTrue(result["settings"]["git"]["enabled"])
        self.assertTrue(result["settings"]["git"]["auto_push"]["enabled"])
        for settings in ({"git": False}, {"git": {"enabled": "true"}},
                         {"git": {"auto_push": False}}):
            with self.subTest(settings=settings):
                path.write_text(json.dumps({"config_format_version": 1, "settings": settings}), encoding="utf-8")
                result = self.result()
                self.assertEqual(result["status"], "invalid")
                self.assertEqual(result["settings"], {})

    def test_malformed_duplicate_and_unsupported_configuration_are_invalid(self):
        path = self.config_path()
        path.parent.mkdir(parents=True)
        bad = ["not-json", '{"config_format_version":1,"config_format_version":1,"settings":{}}',
               '{"config_format_version":true,"settings":{}}',
               '{"config_format_version":2,"settings":{}}',
               '{"config_format_version":1,"settings":[]}']
        for text in bad:
            with self.subTest(text=text):
                path.write_text(text, encoding="utf-8")
                self.assertEqual(self.result()["status"], "invalid")

    def test_settings_free_agent_rejects_nonempty_override(self):
        contract = {**self.contract, "agent": "advisor", "settings": {}}
        path = self.root / "advisor-contract.json"
        path.write_text(json.dumps(contract), encoding="utf-8")
        loaded = config.load_contract(path, "advisor")
        self.assertEqual(config.read_configuration(self.root, "advisor", loaded)["status"], "defaulted")
        override = self.root / ".hai_env/config/agents/advisor.json"
        override.parent.mkdir(parents=True)
        override.write_text('{"config_format_version":1,"settings":{"future":{"enabled":true}}}', encoding="utf-8")
        self.assertEqual(config.read_configuration(self.root, "advisor", loaded)["status"], "invalid")

    def test_contract_rejects_schema_and_identity_errors(self):
        for invalid in (
            {**self.contract, "extra": True},
            {**self.contract, "agent": "other"},
            {**self.contract, "settings": {"git": {"type": "boolean", "default": False},
                                            "git.enabled": {"type": "boolean", "default": False}}},
            {**self.contract, "settings": {"git.enabled": {"type": "boolean", "default": 0}}},
            {**self.contract, "supported_config_format_versions": [True]},
        ):
            with self.subTest(invalid=invalid):
                self.contract_path.write_text(json.dumps(invalid), encoding="utf-8")
                with self.assertRaises(config.ConfigurationError):
                    config.load_contract(self.contract_path, "git-manager")

    def test_contract_v2_directory_setting_is_validated_even_when_disabled(self):
        contract = {
            "contract_format_version": 2, "agent": "specification-manager",
            "current_config_format_version": 1, "supported_config_format_versions": [1],
            "settings": {"enabled": {"type": "boolean", "default": False},
                         "location": {"type": "workspace-relative-directory",
                                      "default": ".hai_env/specifications"}},
        }
        path = self.root / ".hai_env/agents/specification-manager/configuration/contract.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(contract), encoding="utf-8")
        loaded = config.load_contract(path, "specification-manager")
        result = config.read_configuration(self.root, "specification-manager", loaded)
        self.assertEqual(result["status"], "defaulted")
        self.assertEqual(result["settings"], {"enabled": False, "location": ".hai_env/specifications"})

        override = self.root / ".hai_env/config/agents/specification-manager.json"
        override.parent.mkdir(parents=True)
        override.write_text(json.dumps({"config_format_version": 1, "settings": {
            "enabled": False, "location": "workspace-specifications"}}), encoding="utf-8")
        result = config.read_configuration(self.root, "specification-manager", loaded)
        self.assertEqual(result["status"], "configured")
        self.assertEqual(result["settings"]["location"], "workspace-specifications")

        activity = self.root / "workspace-activities"
        activity.mkdir()
        (self.root / ".hai_env/config/state.json").write_text(json.dumps({
            "activities": {"location": "workspace-activities"}, "features": {}}), encoding="utf-8")
        override.write_text(json.dumps({"config_format_version": 1, "settings": {
            "enabled": False, "location": "workspace-activities"}}), encoding="utf-8")
        result = config.read_configuration(self.root, "specification-manager", loaded)
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["settings"], {})

    def test_workspace_directory_candidate_reservations_apply_when_disabled(self):
        (self.root / "specifications").mkdir()
        with self.assertRaises(config.ConfigurationError):
            config.workspace_directory_path(self.root, "specifications",
                                            reserved_paths=("specifications",))

    def test_alias_with_reserved_and_configured_paths_is_rejected(self):
        path = self.config_path()
        path.parent.mkdir(parents=True)
        (self.root / ".hai_env/config/model_profiles.json").write_text("{}", encoding="utf-8")
        try:
            path.symlink_to(self.root / ".hai_env/config/model_profiles.json")
        except OSError as exc:
            if getattr(exc, 'winerror', None) == 1314:
                self.skipTest('Windows symlink privilege unavailable')
            raise
        result = self.result()
        self.assertEqual(result["status"], "invalid")
        path.unlink()
        state = {"activities": {"location": "saved-configs"}, "features": {
            "specification": {"location": ".hai_env/specifications"}}}
        (self.root / ".hai_env/config/state.json").write_text(json.dumps(state), encoding="utf-8")
        (self.root / "saved-configs").mkdir()
        path.symlink_to(self.root / "saved-configs")
        self.assertEqual(self.result()["status"], "invalid")

    def test_alias_with_other_agent_configuration_is_rejected(self):
        path = self.config_path()
        path.parent.mkdir(parents=True)
        path.write_text('{"config_format_version":1,"settings":{}}', encoding="utf-8")
        alias = path.with_name("advisor.json")
        try:
            alias.symlink_to(path)
        except OSError as exc:
            if getattr(exc, 'winerror', None) == 1314:
                self.skipTest('Windows symlink privilege unavailable')
            raise
        result = self.result()
        self.assertEqual(result["status"], "invalid")
        self.assertEqual(result["settings"], {})

    def test_hardlink_to_reserved_file_is_rejected_when_supported(self):
        profiles = self.root / ".hai_env/config/model_profiles.json"
        profiles.write_text('{"format_version":1}', encoding="utf-8")
        path = self.config_path()
        path.parent.mkdir(parents=True)
        try:
            os.link(profiles, path)
        except (OSError, NotImplementedError):
            self.skipTest("Hard links are unavailable")
        self.assertEqual(self.result()["status"], "invalid")

    def test_missing_config_is_independent_of_invalid_core_state(self):
        (self.root / ".hai_env/config/state.json").write_text("malformed", encoding="utf-8")
        result = self.result()
        self.assertEqual(result["status"], "defaulted")
        self.assertEqual(result["settings"]["git"]["enabled"], False)
        state_path = self.root / ".hai_env/config/state.json"
        state_path.unlink()
        outside = Path(self.temp.name).parent / (Path(self.temp.name).name + "_outside_state")
        try:
            state_path.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable")
        self.assertEqual(self.result()["status"], "defaulted")

    def test_cli_checks_one_canonical_contract_and_configuration(self):
        script = Path(config.__file__).resolve()
        proc = subprocess.run([sys.executable, "-I", "-S", "-B", str(script),
                               "--workspace", str(self.root), "--agent", "git-manager",
                               "--contract", ".hai_env/agents/git-manager/configuration/contract.json"],
                              cwd=self.root, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result["status"], "defaulted")
        self.assertTrue(result["ok"])


if __name__ == "__main__":
    unittest.main()
