"""Fixture tests for the explicit format-2 specification extraction."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch

import migrate_specification_configuration as migration
import startup_check as startup


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hai_spec_migration_")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.contract = {
            "contract_format_version": 2, "agent": "specification-manager",
            "current_config_format_version": 1, "supported_config_format_versions": [1],
            "settings": {"enabled": {"type": "boolean", "default": False},
                         "location": {"type": "workspace-relative-directory",
                                      "default": ".hai_env/specifications"}},
        }
        self.write(startup.TEMPLATE, (Path(startup.__file__).resolve().parents[2] / "templates/state.json").read_text(encoding="utf-8"))
        self.write(startup.INSTRUCTIONS, "")
        self.write(".hai/agents/leader/SKILL.md", "Unparsed leader fixture.")
        self.table(".hai", [("leader", "Coordinate work.", "leader/SKILL.md")])
        self.write(".hai_env/agents/specification-manager/SKILL.md", "Unparsed installed fixture.")
        self.write(migration.CONTRACT, json.dumps(self.contract))
        self.table(".hai_env", [("specification-manager", "Manage durable specifications.",
                                  "specification-manager/SKILL.md")])
        self.state = {"state_format_version": 2,
                      **copy.deepcopy(json.loads((Path(startup.__file__).resolve().parents[2] / "templates/state.json").read_text(encoding="utf-8"))),
                      "extension_data": {"keep": [1, {"x": True}]}}
        self.state["features"]["specification"] = {"enabled": True, "location": "spec-data",
                                                       "owner_note": "keep in migrated config"}
        self.state["features"]["chronicles"].update(enabled=True, record_every_prompts=9)
        self.state["features"]["future_feature"] = {"opaque": "preserve"}
        (self.root / "spec-data").mkdir()
        self.save_state()

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8"))
        return path

    def save_state(self):
        self.write(migration.STATE, json.dumps(self.state, ensure_ascii=False, indent=2) + "\n")

    def table(self, origin, entries):
        rows = ["# Catalogue", "", "| Agent | Selection guide | Definition |", "| --- | --- | --- |"]
        for name, guide, link in entries:
            rows.append(f"| `{name}` | {guide} | [SKILL.md]({link}) |")
        self.write(f"{origin}/agents/catalogue.md", "\n".join(rows) + "\n")

    def test_rehearsal_is_read_only_and_apply_preserves_all_other_state(self):
        state_path = self.root / migration.STATE
        if os.name != "nt":
            state_path.chmod(0o640)
        source = (self.root / migration.STATE).read_bytes()
        before = {path.relative_to(self.root).as_posix(): path.read_bytes()
                  for path in self.root.rglob("*") if path.is_file()}
        rehearsal = migration.migrate(self.root)
        self.assertTrue(rehearsal["ok"], rehearsal)
        self.assertEqual(rehearsal["status"], "ready")
        self.assertEqual(source, (self.root / migration.STATE).read_bytes())
        self.assertEqual(before, {path.relative_to(self.root).as_posix(): path.read_bytes()
                                  for path in self.root.rglob("*") if path.is_file()})

        applied = migration.migrate(self.root, apply=True)
        self.assertTrue(applied["ok"], applied)
        self.assertEqual(applied["status"], "migrated")
        self.assertTrue((self.root / ".hai_env/config/agents").is_dir())
        self.assertEqual((self.root / migration.BACKUP).read_bytes(), source)
        if os.name != "nt":
            self.assertEqual(stat.S_IMODE(state_path.stat().st_mode), 0o640)
        updated = json.loads((self.root / migration.STATE).read_text(encoding="utf-8"))
        self.assertEqual(updated["state_format_version"], 3)
        self.assertNotIn("specification", updated["features"])
        self.assertEqual(updated["features"]["chronicles"], {"enabled": True,
                                                               "record_every_prompts": 9})
        self.assertEqual(updated["features"]["future_feature"], {"opaque": "preserve"})
        self.assertEqual(updated["extension_data"], {"keep": [1, {"x": True}]})
        configuration = json.loads((self.root / ".hai_env/config/agents/specification-manager.json").read_text())
        self.assertEqual(configuration, {"config_format_version": 1,
                                         "settings": {"enabled": True, "location": "spec-data",
                                                      "owner_note": "keep in migrated config"}})
        result = startup.check(self.root)
        self.assertEqual(result["environment"], "valid")
        self.assertEqual(result["state_format_version"], 3)
        self.assertEqual(result["agent_configurations"]["specification-manager"]["status"], "configured")
        self.assertEqual(result["agent_configurations"]["specification-manager"]["settings"],
                         {"enabled": True, "location": "spec-data"})

    def test_existing_destination_is_a_conflict_and_is_not_overwritten(self):
        target = self.root / ".hai_env/config/agents/specification-manager.json"
        target.parent.mkdir(parents=True)
        target.write_text('{"keep":"existing"}', encoding="utf-8")
        before = (self.root / migration.STATE).read_bytes()
        with self.assertRaises(Exception):
            migration.migrate(self.root, apply=True)
        self.assertEqual((self.root / migration.STATE).read_bytes(), before)
        self.assertEqual(target.read_text(encoding="utf-8"), '{"keep":"existing"}')
        self.assertFalse((self.root / migration.BACKUP).exists())

    def test_activity_collision_blocks_without_writes(self):
        self.state["activities"]["location"] = "spec-data"
        self.save_state()
        before = (self.root / migration.STATE).read_bytes()
        with self.assertRaises(Exception):
            migration.migrate(self.root, apply=True)
        self.assertEqual((self.root / migration.STATE).read_bytes(), before)
        self.assertFalse((self.root / migration.BACKUP).exists())

    def test_interrupted_state_replace_preserves_partial_files_without_retry(self):
        source = (self.root / migration.STATE).read_bytes()
        with patch.object(migration.os, "replace", side_effect=OSError("simulated replace failure")):
            result = migration.migrate(self.root, apply=True)
        self.assertFalse(result["ok"])
        self.assertEqual(result["status"], "partial")
        self.assertTrue((self.root / migration.BACKUP).exists())
        self.assertTrue((self.root / ".hai_env/config/agents/specification-manager.json").exists())
        self.assertEqual((self.root / migration.STATE).read_bytes(), source)
        with self.assertRaises(Exception):
            migration.migrate(self.root, apply=True)

    def test_hardlinked_source_state_is_rejected(self):
        state_path = self.root / migration.STATE
        alias = self.root / ".hai_env/state-copy.json"
        try:
            os.link(state_path, alias)
        except (OSError, NotImplementedError):
            self.skipTest("Hard links are unavailable")
        with self.assertRaises(Exception):
            migration.migrate(self.root, apply=True)
        self.assertFalse((self.root / migration.BACKUP).exists())
        self.assertFalse((self.root / ".hai_env/config/agents/specification-manager.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
