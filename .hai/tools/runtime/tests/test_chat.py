"""Behavior, preservation and failure checks for Activity coordination chat."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
import uuid
from unittest import mock

TOOLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(TOOLS))
from runtime import activities, chat


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='hai-chat-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / '.hai_env/activities').mkdir(parents=True)
        (self.root / '.hai_env/config').mkdir()
        (self.root / '.hai/templates').mkdir(parents=True)
        shutil.copy(TOOLS.parent / 'templates/state.json', self.root / '.hai/templates/state.json')
        (self.root / '.hai_env/config/agent_instructions.md').write_text('')
        (self.root / '.hai_env/config/state.json').write_text(json.dumps({
            'state_format_version': 3, 'activities': {'location': '.hai_env/activities'},
            'features': {'chronicles': {'enabled': False, 'record_every_prompts': 5}}}))
        self.prov = {'source': 'fixture agent assignment', 'reason': 'verify chat behavior'}
        created = activities.handle('create', self.root, {'initial_input': 'Chat fixture', 'provenance': self.prov}, True)
        self.assertTrue(created['ok'], created)
        self.ident = created['result']['state']['activity_id']
        self.base = self.root / created['result']['path']
        self.path = self.base / 'chat.jsonl'

    def post(self, author='software-developer', text='A finding', apply=True, **extra):
        return activities.handle('chat-post', self.root, {
            'activity_id': self.ident, 'author': author, 'text': text,
            'provenance': self.prov, **extra}, apply)

    def read(self, **extra):
        return activities.handle('chat-read', self.root, {'activity_id': self.ident, **extra}, False)

    def test_empty_read_and_preview_do_not_create_history(self):
        self.assertEqual(self.read()['result']['messages'], [])
        preview = self.post(apply=False)
        self.assertEqual(preview['status'], 'planned')
        self.assertFalse(self.path.exists())
        self.assertEqual(preview['changed_files'], [])

    def test_multiple_authors_exact_append_and_distinct_occurrences(self):
        message = '  Резултат\nwith whitespace\n'
        first = self.post(text=message)
        original = self.path.read_bytes()
        inode = self.path.stat().st_ino
        second = self.post(author='quality-assurance', text=message)
        self.assertTrue(first['ok'] and second['ok'])
        self.assertTrue(self.path.read_bytes().startswith(original))
        self.assertEqual(self.path.stat().st_ino, inode)
        messages = self.read()['result']['messages']
        self.assertEqual([m['author'] for m in messages], ['software-developer', 'quality-assurance'])
        self.assertEqual([m['sequence'] for m in messages], [1, 2])
        self.assertEqual([m['text'] for m in messages], [message, message])
        self.assertNotEqual(messages[0]['message_id'], messages[1]['message_id'])

    def test_pagination_and_strict_numeric_arguments(self):
        for n in range(3):
            self.assertTrue(self.post(text=str(n))['ok'])
        page = self.read(limit=2)['result']
        self.assertTrue(page['has_more'])
        self.assertEqual(page['next_after_sequence'], 2)
        self.assertEqual(self.read(after_sequence=2)['result']['messages'][0]['sequence'], 3)
        for kw in [{'limit': False}, {'limit': 1001}, {'after_sequence': True}, {'after_sequence': -1}]:
            self.assertFalse(self.read(**kw)['ok'])
        self.assertEqual(self.read(after_sequence=50)['result']['messages'], [])

    def test_no_edit_delete_or_record_artifact_overwrite(self):
        self.assertTrue(self.post()['ok'])
        original = self.path.read_bytes()
        for op in ['chat-edit', 'chat-delete', 'chat-clear']:
            result = activities.handle(op, self.root, {'activity_id': self.ident, 'provenance': self.prov}, True)
            self.assertFalse(result['ok'])
            self.assertEqual(self.path.read_bytes(), original)
        result = activities.handle('record', self.root, {'activity_id': self.ident, 'artifacts': [
            {'name': 'chat.jsonl', 'text': 'replacement', 'reason': 'not permitted'}],
            'log': 'invalid overwrite attempt', 'provenance': self.prov}, True)
        self.assertFalse(result['ok'])
        self.assertEqual(self.path.read_bytes(), original)

    def test_invalid_post_arguments_leave_no_file(self):
        for kwargs in [{'author': '../agent'}, {'text': ' '}, {'text': 'x' * 65537},
                       {'message_id': str(uuid.uuid4())}, {'sequence': 4}, {'created_at': 'fake'}]:
            self.assertFalse(self.post(**kwargs)['ok'])
            self.assertFalse(self.path.exists())

    def test_malformed_or_wrong_activity_history_blocks_append(self):
        self.assertTrue(self.post()['ok'])
        original = self.path.read_bytes()
        message = json.loads(original)
        corruptions = [original[:-1], original + b'\n', b'{"sequence":1,"sequence":1}\n']
        for field, value in [('activity_id', str(uuid.uuid4())), ('sequence', True),
                             ('chat_format_version', False), ('created_at', 'yesterday'),
                             ('author', 'Agent Name'), ('text', ''), ('message_id', 'not-a-uuid')]:
            bad = {**message, field: value}
            corruptions.append((json.dumps(bad) + '\n').encode())
        corruptions.append(original + (json.dumps({**message, 'sequence': 2}) + '\n').encode())
        for raw in corruptions:
            with self.subTest(raw=raw[:70]):
                self.path.write_bytes(raw)
                self.assertFalse(self.read()['ok'])
                result = self.post()
                self.assertFalse(result['ok'])
                self.assertEqual(result['changed_files'], [])
                self.assertEqual(self.path.read_bytes(), raw)

    def test_archive_keeps_history_and_new_activity_is_empty(self):
        self.assertTrue(self.post()['ok'])
        raw = self.path.read_bytes()
        closed = activities.handle('close', self.root, {'activity_id': self.ident,
            'outcome': 'completed', 'archive_label': 'chat-test', 'outcome_text': 'Fixture done',
            'recording': {'status': 'disabled', 'details': 'Fixture recording off'},
            'provenance': self.prov}, True)
        self.assertTrue(closed['ok'], closed)
        self.assertEqual((self.root / closed['result']['archive_path'] / 'chat.jsonl').read_bytes(), raw)
        self.assertEqual(len(self.read()['result']['messages']), 1)
        self.assertFalse(self.post()['ok'])
        new = activities.handle('create', self.root, {'initial_input': '', 'provenance': self.prov}, True)
        self.assertTrue(new['ok'])
        old_id = self.ident
        self.ident = new['result']['state']['activity_id']
        self.assertEqual(self.read()['result']['messages'], [])
        self.assertTrue(self.post(author='host-coordinator', text='New Activity')['ok'])
        archived = activities.handle('chat-read', self.root, {'activity_id': old_id}, False)
        self.assertEqual(len(archived['result']['messages']), 1)

    def test_short_write_is_partial_and_old_prefix_survives(self):
        self.assertTrue(self.post()['ok'])
        raw = self.path.read_bytes()
        real_write = chat.os.write
        with mock.patch.object(chat.os, 'write', side_effect=lambda fd, data: real_write(fd, data[:9])):
            result = self.post(text='Partial append')
        self.assertEqual(result['status'], 'partial', result)
        self.assertIn(str(self.path.relative_to(self.root)), result['changed_files'])
        self.assertTrue(self.path.read_bytes().startswith(raw))
        partial = self.path.read_bytes()
        self.assertFalse(self.post()['ok'])
        self.assertEqual(self.path.read_bytes(), partial)

    def test_runtime_lock_blocks_competing_writer_before_append(self):
        started, release = threading.Event(), threading.Event()
        real_append = chat.append
        def held(*args):
            started.set()
            if not release.wait(5):
                raise RuntimeError('Fixture timed out')
            return real_append(*args)
        with ThreadPoolExecutor(max_workers=1) as pool:
            with mock.patch.object(chat, 'append', side_effect=held):
                future = pool.submit(self.post)
                try:
                    self.assertTrue(started.wait(5))
                    competing = self.post(author='quality-assurance')
                    self.assertEqual(competing['status'], 'blocked')
                    self.assertFalse(self.path.exists())
                finally:
                    release.set()
                self.assertTrue(future.result()['ok'])
        self.assertTrue(self.post(author='quality-assurance')['ok'])
        self.assertEqual([m['sequence'] for m in self.read()['result']['messages']], [1, 2])

    def test_linked_history_is_rejected_without_touching_target(self):
        target = self.root / 'external.txt'
        target.write_text('leave me alone')
        try:
            self.path.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable')
        self.assertFalse(self.post()['ok'])
        self.assertFalse(self.read()['ok'])
        self.assertEqual(target.read_text(), 'leave me alone')

    def test_custom_store_and_missing_instructions(self):
        destination = self.root / 'project/activities'
        destination.parent.mkdir()
        (self.root / '.hai_env/activities').rename(destination)
        state_path = self.root / '.hai_env/config/state.json'
        state = json.loads(state_path.read_text())
        state['activities']['location'] = 'project/activities'
        state_path.write_text(json.dumps(state))
        self.assertTrue(self.post()['ok'])
        result = self.read()
        self.assertTrue(result['result']['path'].startswith('project/activities/'))
        (self.root / '.hai_env/config/agent_instructions.md').unlink()
        self.assertFalse(self.post()['ok'])

    def test_startup_checks_type_without_loading_chat_content(self):
        self.path.write_text('deliberately malformed chat content\n')
        result = subprocess.run([sys.executable, '-B', str(TOOLS / 'hai.py'), 'startup',
                                 '--workspace', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn('deliberately malformed', result.stdout)
        self.assertFalse(self.read()['ok'])

    def test_hardlinked_history_is_rejected(self):
        self.assertTrue(self.post()['ok'])
        original = self.path.read_bytes()
        try:
            os.link(self.path, self.root / 'alias.jsonl')
        except OSError:
            self.skipTest('Hardlinks unavailable')
        self.assertFalse(self.read()['ok'])
        self.assertFalse(self.post()['ok'])
        self.assertEqual(self.path.read_bytes(), original)

    def test_fsync_failure_reports_written_message_without_rollback(self):
        self.assertTrue(self.post()['ok'])
        original = self.path.read_bytes()
        with mock.patch.object(chat.os, 'fsync', side_effect=OSError('fixture fsync failure')):
            result = self.post(text='Written before sync failed')
        self.assertEqual(result['status'], 'partial', result)
        self.assertTrue(self.path.read_bytes().startswith(original))
        self.assertEqual(len(self.read()['result']['messages']), 2)

    def test_cli_preview_apply_read_and_read_apply_rejection(self):
        request = self.root / 'request.json'
        request.write_text(json.dumps({'activity_id': self.ident, 'author': 'host-coordinator',
                                      'text': 'CLI message', 'provenance': self.prov}))
        args = [sys.executable, '-B', str(TOOLS / 'hai.py'), 'activity', 'chat-post',
                '--workspace', str(self.root), '--request', str(request)]
        preview = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(preview.returncode, 0, preview.stdout)
        self.assertFalse(self.path.exists())
        applied = subprocess.run(args + ['--apply'], capture_output=True, text=True)
        self.assertEqual(applied.returncode, 0, applied.stdout)
        request.write_text(json.dumps({'activity_id': self.ident}))
        args[4] = 'chat-read'
        read = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(read.returncode, 0, read.stdout)
        self.assertEqual(json.loads(read.stdout)['result']['messages'][0]['text'], 'CLI message')
        raw = self.path.read_bytes()
        rejected = subprocess.run(args + ['--apply'], capture_output=True, text=True)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertEqual(self.path.read_bytes(), raw)


if __name__ == '__main__':
    unittest.main()
