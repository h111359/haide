import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import context_registry as registry


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def put(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
        return target

    def entry(self, title, location='product/orders.md', read='yes', **fields):
        values = dict(Location=location, Summary='Order behavior', Read=read, **fields)
        return '### ' + title + '\n' + '\n'.join(f'- {k}: {v}' for k, v in values.items()) + '\n'

    def inspect(self, entries):
        self.put('context.md', '# Primary\n## References\n' + entries)
        return registry.inspect_registry(self.root, 'context.md', '.hai_env/activities')

    def test_order_independent_missing_resources_and_semantic_host_reads(self):
        self.put('product/orders.md', 'First complete order context.\nFinal line.\n')
        self.put('product/returns.md', 'Complete returns context.')
        self.put('product/tax.md', 'Unrelated tax context.')
        result = self.inspect(
            self.entry('Orders', Convention='missing-convention.md', Prompt='missing-prompt.py')
            + self.entry('Missing', 'missing-location.md', Convention='missing-c.md')
            + self.entry('Taxes', 'product/tax.md')
            + self.entry('Returns', 'product/returns.md'))
        self.assertEqual([e['title'] for e in result['entries']], ['Orders', 'Missing', 'Taxes', 'Returns'])
        self.assertEqual([e['eligible'] for e in result['entries']], [True, False, True, True])
        for path in ('missing-convention.md', 'missing-prompt.py', 'missing-location.md', 'missing-c.md'):
            self.assertIn(f'WARNING: Context registry resource unavailable: {path}. Proceeding without that resource.', result['diagnostics'])
        # A host simulation supplies relevance; the diagnostic itself never guesses it.
        selected = []
        for entry in result['entries']:
            if entry['eligible'] and entry['title'] in ('Orders', 'Returns'):
                path = entry['resources']['Location']['path']
                safe = registry.resource_path(self.root, path, '.hai_env/activities')
                selected.append((entry['title'], path, safe.read_text(encoding='utf-8')))
        self.assertEqual([x[0] for x in selected], ['Orders', 'Returns'])
        self.assertTrue(selected[0][2].endswith('Final line.\n'))

    def test_yes_no_invalid_flags_and_no_qualifying_extensions(self):
        self.put('product/orders.md', 'knowledge')
        result = self.inspect(self.entry('Upper', read='YES') + self.entry('Skip', read='No')
                              + self.entry('Invalid', read='maybe'))
        self.assertEqual([e['eligible'] for e in result['entries']], [True, False, False])
        self.assertIn('invalid Read value', ' '.join(result['diagnostics']))
        result = self.inspect(self.entry('Skip', read='NO'))
        self.assertFalse(any(e['eligible'] for e in result['entries']))
        self.put('empty.md', '# Sufficient primary files\nNo registry.\n')
        self.assertEqual(registry.inspect_registry(self.root, 'empty.md', 'custom/work')['entries'], [])

    def test_prompt_update_are_inert_and_diagnostics_read_only(self):
        self.put('product/orders.md', 'must not be read by diagnostics')
        self.put('convention.md', 'must not be read by diagnostics')
        self.put('prompt.py', 'raise AssertionError("PROMPT-SECRET")')
        document = self.put('context.md', '## References\n' + self.entry(
            'Orders', Convention='convention.md', Prompt='prompt.py', Update='execute prompt.py'))
        before = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        original = Path.read_text
        reads = []
        def read(path, *args, **kwargs):
            reads.append(path)
            return original(path, *args, **kwargs)
        with mock.patch.object(Path, 'read_text', read), mock.patch('subprocess.run', side_effect=AssertionError('execution forbidden')), mock.patch('socket.socket', side_effect=AssertionError('network forbidden')):
            result = registry.inspect_registry(self.root, 'context.md', '.hai_env/activities')
        self.assertEqual(reads, [document])
        self.assertNotIn('PROMPT-SECRET', json.dumps(result))
        after = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_unsafe_paths_and_custom_store_are_rejected(self):
        for value in ('../outside.md', '/etc/passwd', 'C:/tmp/x', 'a/../b', '.GIT/config',
                      'venv/notes.md', 'node_modules/x', '__pycache__/x', '.cache/x',
                      'custom/work/00000000_000000_active/input.md',
                      'custom/work/20261108_000000_old/input.md', 'other/20261108_000000_old/x'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                registry.resource_path(self.root, value, 'custom/work')
        self.put('ordinary.md', 'safe')
        result = self.inspect(self.entry('Unsafe convention', 'ordinary.md', Convention='../escape'))
        self.assertFalse(result['entries'][0]['eligible'])

    def test_symlink_and_hardlink_rejection(self):
        original = self.put('safe.md', 'safe')
        link = self.root / 'linked.md'
        try:
            link.symlink_to(original)
        except (OSError, NotImplementedError) as exc:
            self.skipTest('symlink creation unavailable: ' + str(exc))
        with self.assertRaisesRegex(ValueError, 'linked'):
            registry.resource_path(self.root, 'linked.md', '.hai_env/activities')
        link.unlink()
        link.hardlink_to(original)
        with self.assertRaisesRegex(ValueError, 'singly linked'):
            registry.resource_path(self.root, 'linked.md', '.hai_env/activities')

    def test_registry_subset_fences_duplicates_and_section_boundary(self):
        text = '```markdown\n## References\n### fake\n```\n## References\n' + self.entry('Real') + '- Read: no\n## Later\n' + self.entry('Outside')
        entries = registry.parse_registry(text)
        self.assertEqual([e['title'] for e in entries], ['Real'])
        self.assertIn('duplicate field: Read', entries[0]['issues'])
        with self.assertRaisesRegex(ValueError, 'unclosed'):
            registry.parse_registry('```\n## References')

    def test_unicode_crlf_missing_context_and_cli_exit_codes(self):
        self.put('данни.md', 'Здравей\r\n')
        self.put('context.md', ('## References\n' + self.entry('Поръчки', 'данни.md')).replace('\n', '\r\n'))
        command = [sys.executable, '-B', str(Path(registry.__file__)), '--workspace', str(self.root), '--document', 'context.md', '--activity-store', '.hai_env/activities']
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)['entries'][0]['title'], 'Поръчки')
        self.inspect(self.entry('Bad', read='sometimes'))
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)
        (self.root / 'context.md').unlink()
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('context.md', result.stdout)


if __name__ == '__main__':
    unittest.main()
