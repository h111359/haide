"""HTTP boundary and actual browser-independent portal server contracts."""
from __future__ import annotations
import http.client
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from contracts import Error
from portal import PortalServer, existing_portal

BASE = Path(__file__).resolve().parents[3] / "tests" / "runtime-fixtures"


class FakeEngine:
    def __init__(self, home):
        self.home = home
        self.actions = []
        self.initializations = 0
        self.revision = 1
        self.busy = False
        self.receipts = {}

    def initialize(self):
        self.initializations += 1
        return {"ok": True, "revision": self.revision, "reused": self.initializations > 1}

    def status(self):
        return {"revision": self.revision, "product": {"home": str(self.home), "name": "HTTP fixture"}, "busy": self.busy}

    def operations(self):
        return [{"id": "save-draft", "available": not self.busy}]

    def artifact(self, path):
        if ".." in path or path.startswith("/"):
            raise Error("workspace_boundary", "Unsafe path rejected")
        return {"text": "<script>alert('must remain inert')</script>"}

    def dispatch(self, operation, payload, expected_revision=None, idempotency_key=None, **kwargs):
        if idempotency_key in self.receipts:
            return self.receipts[idempotency_key]
        if self.busy and operation != "stop":
            raise Error("busy", "Stop only; no submission accepted")
        if expected_revision != self.revision:
            raise Error("revision-conflict", "Draft revision changed")
        self.actions.append((operation, payload))
        self.revision += 1
        result = {"ok": True, "revision": self.revision, "operation_id": "OP-fixture"}
        self.receipts[idempotency_key] = result
        return result


class PortalTests(unittest.TestCase):
    def setUp(self):
        BASE.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="portal-http-", dir=BASE)
        self.home = Path(self.temp.name)
        (self.home / ".aih").mkdir()
        (self.home / ".aih/USER_GUIDE.md").write_text("# Quick start\n\nLocal guide.")
        (self.home / ".aih/README.md").write_text("# AIH\n")
        self.engine = FakeEngine(self.home)
        self.server = PortalServer(self.home, 0, engine_factory=lambda: self.engine)
        self.thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": .01}, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp.cleanup()

    def request(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.server.port, timeout=3)
        conn.request(method, path, body, headers or {})
        response = conn.getresponse()
        result = response.status, dict(response.getheaders()), response.read().decode()
        conn.close()
        return result

    def post(self, body=None, **headers):
        envelope = body if body is not None else {"operation": "save-draft", "expected_revision": 1, "idempotency_key": "fixture-action", "payload": {"lane": "change", "text": "Readable request"}}
        base = {"Content-Type": "application/json", "Origin": self.server.url, "X-AIH-Token": self.server.csrf_token, **headers}
        return self.request("POST", "/api/operation", json.dumps(envelope), base)

    def test_assets_help_and_status_are_passive(self):
        for path in ("/", "/app.js", "/app.css", "/api/help", "/api/catalog", "/api/status"):
            with self.subTest(path=path):
                status, headers, text = self.request("GET", path)
                self.assertEqual(status, 200, text)
                self.assertIn("script-src 'self'", headers["Content-Security-Policy"])
                self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(self.engine.actions, [])
        self.assertEqual(self.engine.initializations, 0)
        self.assertEqual(json.loads(self.request("GET", "/api/status")[2])["csrf_token"], self.server.csrf_token)

    def test_cross_origin_and_missing_token_rejected_without_effect(self):
        for headers in ({"Origin": "https://attacker.invalid"}, {"Origin": "null"}, {"X-AIH-Token": ""}, {"Sec-Fetch-Site": "cross-site"}):
            with self.subTest(headers=headers):
                self.assertEqual(self.post(**headers)[0], 403)
        self.assertFalse(self.engine.actions)

    def test_dns_rebinding_host_and_unrestricted_paths_rejected(self):
        self.assertEqual(self.request("GET", "/api/status", headers={"Host": "attacker.invalid"})[0], 403)
        for path in ("/api/artifacts?path=../../etc/passwd", "/api/artifacts?path=%2Fetc%2Fpasswd", "/../../etc/passwd", "/api/command"):
            self.assertGreaterEqual(self.request("GET", path)[0], 400)
        self.assertFalse(self.engine.actions)

    def test_safe_artifact_rendering_and_no_cors(self):
        status, headers, body = self.request("GET", "/api/artifacts?path=output/result.md")
        self.assertEqual(status, 200)
        self.assertTrue(headers["Content-Type"].startswith("text/plain"))
        self.assertIn("<script>", body)
        self.assertNotIn("Access-Control-Allow-Origin", headers)
        self.assertEqual(self.request("OPTIONS", "/api/operation")[0], 403)

    def test_revision_idempotency_and_busy_forwarded(self):
        first = self.post()
        self.assertEqual(first[0], 200, first[2])
        self.assertEqual(self.post()[0], 200)
        self.assertEqual(len(self.engine.actions), 1)
        changed = {"operation": "save-draft", "expected_revision": 1, "idempotency_key": "other", "payload": {"text": "new"}}
        self.assertEqual(self.post(changed)[0], 409)
        self.engine.busy = True
        changed["expected_revision"] = self.engine.revision
        self.assertEqual(self.post(changed)[0], 409)
        self.assertEqual(len(self.engine.actions), 1)

    def test_sensitive_intake_rejected_without_echo_or_dispatch(self):
        secret = "sk-" + "A" * 36
        payload = {"operation": "save-draft", "expected_revision": 1, "idempotency_key": "secret", "payload": {"text": secret}}
        status, _, body = self.post(payload)
        self.assertEqual(status, 400)
        self.assertNotIn(secret, body)
        self.assertIn("sensitive-input", body)
        self.assertFalse(self.engine.actions)

    def test_envelope_requires_revision_key_and_typed_payload(self):
        for body in ({"operation": "save-draft"}, {"operation": "save-draft", "payload": "shell"}, {"operation": "save-draft", "command": "sh"}, {"operation": "save-draft", "expected_revision": True, "idempotency_key": "key", "payload": {}}):
            self.assertEqual(self.post(body)[0], 400)
        self.assertFalse(self.engine.actions)

    def test_initial_bootstrap_runs_once_and_reopen_does_not_resume(self):
        self.server.bootstrap()
        self.server.bootstrap()
        self.assertEqual([a[0] for a in self.engine.actions], ["reverse-engineer"])

    def test_existing_server_identity_matches_home(self):
        self.assertEqual(existing_portal(self.home, self.server.port), self.server.url)
        self.assertIsNone(existing_portal(self.home / "another", self.server.port))

    def test_download_filename_is_safe(self):
        status, headers, _ = self.request("GET", "/api/artifacts?path=output/file.md&download=1")
        self.assertEqual(status, 200)
        self.assertEqual(headers["Content-Disposition"], 'attachment; filename="file.md"')



class PortalEngineIntegrationTests(unittest.TestCase):
    def setUp(self):
        from workflow import Engine
        BASE.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="portal-engine-", dir=BASE)
        self.home = Path(self.temp.name)
        (self.home / ".aih/engine").mkdir(parents=True)
        (self.home / ".aih/engine/cli.py").write_text("# Explicit installation marker for this synthetic test fixture.\n")
        (self.home / ".aih/USER_GUIDE.md").write_text("# Test fixture help\n")
        (self.home / ".aih/README.md").write_text("# Test fixture\n")
        self.engine = Engine(self.home)
        self.engine.initialize()
        self.server = PortalServer(self.home, 0)
        self.thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": .01}, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join(timeout=2)
        self.temp.cleanup()

    def request(self, method, path, body=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.server.port, timeout=5)
        headers = {"Content-Type": "application/json", "Origin": self.server.url, "X-AIH-Token": self.server.csrf_token}
        conn.request(method, path, json.dumps(body) if body is not None else None, headers)
        response = conn.getresponse()
        result = response.status, response.read().decode()
        conn.close()
        return result

    def op(self, action, payload, key):
        revision = self.engine.status()["revision"]
        return self.request("POST", "/api/operation", {"operation": action, "payload": payload, "expected_revision": revision, "idempotency_key": key})

    def test_real_draft_persistence_baseline_gate_and_passive_reads(self):
        code, body = self.op("save-draft", {"lane": "change", "text": "Add a filtered export.", "title": "CSV export"}, "http-save")
        self.assertEqual(code, 200, body)
        state = self.engine.status()
        value = state["draft"]["change"]
        self.assertEqual(value.get("text") if isinstance(value, dict) else value, "Add a filtered export.")
        self.assertIsNone(state["active_request"])
        self.assertFalse(state["busy"])
        revision = state["revision"]
        for _ in range(2):
            self.assertEqual(self.request("GET", "/api/status")[0], 200)
            self.assertEqual(self.request("GET", "/api/catalog")[0], 200)
        self.assertEqual(self.engine.status()["revision"], revision)
        code, body = self.op("clarify", {}, "http-clarify")
        self.assertGreaterEqual(code, 400)
        self.assertIn("baseline", body)
        self.assertIsNone(self.engine.status()["active_request"])

    def test_real_settings_validation_and_artifact_boundary(self):
        code, body = self.op("settings-save", {"appearance": {"theme": "midnight", "size": 18}}, "http-appearance")
        self.assertEqual(code, 200, body)
        self.assertEqual(self.engine.status()["config"]["appearance"], {"theme": "midnight", "size": 18})
        code, body = self.op("settings-save", {"appearance": {"theme": "clear", "size": 500}}, "http-bad-theme")
        self.assertGreaterEqual(code, 400)
        self.assertEqual(self.engine.status()["config"]["appearance"]["size"], 18)
        self.assertEqual(self.request("GET", "/api/artifacts?path=input/current.md")[0], 200)
        self.assertGreaterEqual(self.request("GET", "/api/artifacts?path=home:../outside.txt")[0], 400)


if __name__ == "__main__":
    unittest.main()
