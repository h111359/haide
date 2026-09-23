"""A controlled executable exercises the actual Codex event transport, not model behavior."""
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from adapters import diagnostics, execute
from security import Workspace

BASE = Path(__file__).resolve().parents[3] / "tests/runtime-fixtures"


class ControlledCodexTransport(unittest.TestCase):
    def setUp(self):
        BASE.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="adapter unicode Ω & spaces ", dir=BASE)
        self.home = Path(self.temp.name)
        self.workspace = Workspace(self.home)
        self.executable = self.home / "fake ; codex Ω"
        self.profile = {"id": "controlled-codex", "adapter": "codex", "executable": str(self.executable), "timeout": 5, "permissions": {"network": False}}

    def tearDown(self):
        self.temp.cleanup()

    def program(self, behavior="ok"):
        script = "#!" + sys.executable + "\n" + '''import json,sys,time,os
mode=BEHAVIOR
if '--version' in sys.argv:
 print('codex 0.154.0 controlled-test');raise SystemExit(7 if mode=='version-error' else 0)
if '--help' in sys.argv:
 print('--json --skip-git-repo-check --sandbox '+('' if mode=='incompatible' else '--ephemeral'));raise SystemExit(0)
if 'login' in sys.argv:
 print('Authentication unavailable' if mode=='auth-error' else 'Controlled authenticated fixture');raise SystemExit(1 if mode=='auth-error' else 0)
prompt=sys.stdin.read()
print(json.dumps({'type':'thread.started','thread_id':'controlled-session'}),flush=True)
if mode=='malformed':print('not JSON: controlled transport event',flush=True)
if mode=='reasoning':print(json.dumps({'type':'item.completed','item':{'type':'reasoning','text':'PRIVATE_TEST_REASONING'}}),flush=True)
if mode=='timeout':time.sleep(60)
print(json.dumps({'type':'item.completed','item':{'type':'agent_message','text':json.dumps({'answer':'Здравей Ω '+prompt[-35:]})}}),flush=True)
if mode!='usage-missing':print(json.dumps({'type':'turn.completed','usage':{'input_tokens':17,'cached_input_tokens':5,'output_tokens':9}}),flush=True)
raise SystemExit(4 if mode=='nonzero' else 0)
'''
        self.executable.write_text(script.replace("BEHAVIOR", repr(behavior)), encoding="utf-8")
        self.executable.chmod(0o700)

    def test_unicode_spaces_literal_arguments_events_and_usage(self):
        self.program()
        events = []
        result = execute(self.profile, self.workspace, "Prompt Ω & $(must-not-execute)", on_event=events.append, operation_id="unicode")
        self.assertEqual(result["returncode"], 0)
        self.assertEqual(result["session_id"], "controlled-session")
        self.assertEqual(result["usage"]["input_tokens"], 17)
        self.assertIn("Здравей", json.loads(result["text"])["answer"])
        self.assertIn("$(must-not-execute)", json.loads(result["text"])["answer"])
        self.assertTrue(result["termination_confirmed"])
        self.assertTrue(events)

    def test_version_authentication_and_incompatible_help_diagnostics(self):
        for behavior in ("version-error", "auth-error", "incompatible"):
            self.program(behavior)
            result = diagnostics(self.profile, self.workspace)
            self.assertFalse(result["available"], behavior)
            self.assertFalse(result.get("service_access_verified", False))

    def test_malformed_event_nonzero_and_unavailable_usage_are_explicit(self):
        self.program("malformed")
        result = execute(self.profile, self.workspace, "Read only", operation_id="malformed")
        self.assertTrue(any(e["type"] == "unparsed_stdout" for e in result["events"]))
        self.program("nonzero")
        self.assertEqual(execute(self.profile, self.workspace, "Read only", operation_id="nonzero")["returncode"], 4)
        self.program("usage-missing")
        self.assertIsNone(execute(self.profile, self.workspace, "Read only", operation_id="usage-missing")["usage"])

    def test_timeout_and_new_session_resume_are_truthfully_labeled(self):
        self.program("timeout")
        result = execute({**self.profile, "timeout": 1}, self.workspace, "Read only", operation_id="timeout")
        self.assertEqual(result["status"], "timeout")
        self.assertTrue(result["termination_confirmed"])
        self.program()
        result = execute(self.profile, self.workspace, "Resume from persisted evidence", operation_id="resume", checkpoint={"completed": ["T1"], "outstanding": ["T2"]})
        self.assertEqual(result["resume_mode"], "new-session-from-persisted-harness-state")
        self.assertEqual(result["returncode"], 0)

    def test_reasoning_events_are_not_retained(self):
        self.program("reasoning")
        result = execute(self.profile, self.workspace, "Return concise observable work", operation_id="reasoning", output_ref="output/transport.yaml")
        self.assertNotIn("PRIVATE_TEST_REASONING", json.dumps(result))
        self.assertNotIn("PRIVATE_TEST_REASONING", (self.home / ".aih_product/output/transport.yaml").read_text())


if __name__ == "__main__":
    unittest.main()
