"""Behavioral tests for operation-bound closure evidence; no optional owner needed."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from recording_gate import assess_closure


class ClosureGateTests(unittest.TestCase):
    def request(self):
        occurrence = {"source_session_id": "session", "source_position": 1}
        operation = {"activity_id": "activity", "operation_id": "closure-unique",
                     "cutoff": [occurrence], "enabled_intervals": [
                         {"start": occurrence, "end": None, "provenance": "explicit enablement"}]}
        requirement = {"enabled": True, "mandatory": False}
        sources = {"session": "a" * 64}
        artifacts = {"chronicles/segment.md": "b" * 64, "chronicles/checkpoint.json": "c" * 64}
        proof = {**copy.deepcopy(operation), "recording_requirement": copy.deepcopy(requirement),
                 "verification_id": "verification-unique", "verified_at": "2026-11-02T08:00:00Z",
                 "status": "verified", "retained_source_complete": True,
                 "gaps": [], "conflicts": [], "active_writes": False,
                 "source_snapshots": sources, "artifact_snapshots": artifacts}
        return {"recording_requirement": requirement, "operation": operation, "evidence": proof,
                "current_sources": copy.deepcopy(sources), "current_artifacts": copy.deepcopy(artifacts),
                "writers_stopped": True}

    def test_current_complete_proof_passes_without_optional_package(self):
        request = self.request()
        before = copy.deepcopy(request)
        self.assertEqual(assess_closure(request), {"ok": True, "status": "verified", "issues": []})
        self.assertEqual(request, before)

    def test_disabled_requires_no_owner_source_or_proof(self):
        result = assess_closure({"recording_requirement": {"enabled": False, "mandatory": False}})
        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "disabled_no_obligation")

    def test_independent_mandatory_recording_still_requires_proof(self):
        self.assertFalse(assess_closure({"recording_requirement": {"enabled": False, "mandatory": True}})["ok"])

    def test_stale_operation_activity_cutoff_and_intervals_block(self):
        for key, value in (("operation_id", "another-closure"), ("activity_id", "another-activity"),
                           ("cutoff", [{"source_session_id": "session", "source_position": 2}]),
                           ("enabled_intervals", [])):
            with self.subTest(key=key):
                request = self.request()
                request["operation"][key] = value
                self.assertFalse(assess_closure(request)["ok"])

    def test_changed_source_or_artifact_blocks_archival(self):
        for key in ("current_sources", "current_artifacts"):
            with self.subTest(key=key):
                request = self.request()
                first = next(iter(request[key]))
                request[key][first] = "d" * 64
                self.assertFalse(assess_closure(request)["ok"])

    def test_missing_partial_gap_incomplete_and_uncertain_evidence_block(self):
        for key, value in (("status", "partial"), ("retained_source_complete", None),
                           ("gaps", ["old missing source"]), ("conflicts", ["overlap"]),
                           ("active_writes", None), ("verification_id", ""),
                           ("verified_at", "not a timestamp"), ("source_snapshots", {})):
            with self.subTest(key=key):
                request = self.request()
                request["evidence"][key] = value
                self.assertFalse(assess_closure(request)["ok"])
        request = self.request()
        request["writers_stopped"] = False
        self.assertFalse(assess_closure(request)["ok"])

    def test_proof_bool_integer_coercion_is_rejected(self):
        request = self.request()
        request["evidence"]["recording_requirement"]["enabled"] = 1
        self.assertFalse(assess_closure(request)["ok"])
        request = self.request()
        request["evidence"]["cutoff"][0]["source_position"] = True
        self.assertFalse(assess_closure(request)["ok"])
        request = self.request()
        request["evidence"]["enabled_intervals"][0]["start"]["source_position"] = True
        self.assertFalse(assess_closure(request)["ok"])

    def test_current_requirement_and_cutoff_types_are_strict(self):
        request = self.request()
        request["recording_requirement"]["enabled"] = 1
        self.assertFalse(assess_closure(request)["ok"])
        request = self.request()
        request["operation"]["cutoff"][0]["source_position"] = True
        self.assertFalse(assess_closure(request)["ok"])

    def test_new_requirement_and_unassigned_source_snapshot_block(self):
        request = self.request()
        request["recording_requirement"]["mandatory"] = True
        self.assertFalse(assess_closure(request)["ok"])
        request = self.request()
        request["evidence"]["source_snapshots"] = {"another-session": "a" * 64}
        request["current_sources"] = {"another-session": "a" * 64}
        self.assertFalse(assess_closure(request)["ok"])

    def test_cli_duplicate_json_is_fatal_and_does_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"request.json"
            raw = '{"recording_requirement":{"enabled":false,"enabled":true,"mandatory":false}}'
            path.write_text(raw)
            result = subprocess.run([sys.executable, "-B", str(Path(__file__).with_name("recording_gate.py")), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(json.loads(result.stdout)["ok"])
            self.assertEqual(path.read_text(), raw)


if __name__ == "__main__":
    unittest.main()
