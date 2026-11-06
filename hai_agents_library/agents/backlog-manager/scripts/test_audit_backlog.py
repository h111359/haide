"""Temporary-fixture checks; no live backlog writes or agent invocation."""
import json
import os
from pathlib import Path
import tempfile
import unittest

from audit_backlog import audit, catalogue_row, parse_item


class BacklogAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.workspace = Path(self.tmp.name)
        self.root = self.workspace / 'planning/team-backlog'
        (self.root / 'new').mkdir(parents=True)
        (self.root / 'closed').mkdir()

    def item(self, ident='BL-0001', status='pending'):
        folder = 'new' if status == 'pending' else 'closed'
        closed = '—' if status == 'pending' else '2026-11-06T05:00:00Z'
        path = self.root / folder / (ident + '.md')
        text = f'''# {ident} — Пример item

| Field | Value |
| --- | --- |
| ID | {ident} |
| Status | {status} |
| Created | 20261029 (time unspecified) |
| Updated | 2026-11-06T05:00:00Z |
| Closed | {closed} |
| Activities | — |
| Source | Explicit fixture |

## What

Preserve Unicode and whitespace.

## Why

An attributable reason.

## Acceptance Criteria

An observable result.

## History

- 2026-11-06T05:00:00Z — Fixture created.
'''
        if status != 'pending':
            text += '\n## Resolution\n\nFixture decision with source and evidence.\n'
        path.write_text(text, encoding='utf-8')
        return path

    def catalogue(self, paths):
        (self.root / 'catalogue.md').write_text('# Backlog\n\n| ID | Title | Status | File |\n| --- | --- | --- | --- |\n' + ''.join(catalogue_row(parse_item(p)) + '\n' for p in paths))

    def run_audit(self, location='planning/team-backlog'):
        return audit(self.workspace, location)

    def test_custom_location_and_read_only_unicode(self):
        self.catalogue([self.item()])
        snapshot = {p.relative_to(self.workspace): p.read_bytes() for p in self.workspace.rglob('*') if p.is_file()}
        result = self.run_audit()
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['counts']['pending'], 1)
        self.assertEqual(snapshot, {p.relative_to(self.workspace): p.read_bytes() for p in self.workspace.rglob('*') if p.is_file()})

    def test_default_location_and_saved_custom_location(self):
        self.catalogue([self.item()])
        config = self.workspace / '.hai_env/config/agents/backlog-manager.json'
        config.parent.mkdir(parents=True)
        config.write_text(json.dumps({'config_format_version': 1, 'settings': {'location': 'planning/team-backlog'}}))
        self.assertTrue(audit(self.workspace)['ok'])
        self.assertEqual(audit(self.workspace)['location'], 'planning/team-backlog')
        config.unlink()
        self.root.rename(self.workspace / 'backlog')
        self.assertTrue(audit(self.workspace)['ok'])
        self.root = self.workspace / 'backlog'
        config.write_text(json.dumps({'config_format_version': 1, 'settings': {'location': 'backlog'}}))
        self.assertEqual(audit(self.workspace)['configuration_status'], 'configured')
        config.write_text(json.dumps({'config_format_version': 1, 'settings': {'location': False}}))
        self.assertFalse(audit(self.workspace, 'backlog')['ok'])

    def test_all_terminal_outcomes(self):
        paths = [self.item(f'BL-{n:04}', status) for n, status in enumerate(['completed', 'cancelled', 'rejected'], 1)]
        self.catalogue(paths)
        self.assertTrue(self.run_audit()['ok'])
        paths[0].write_text(paths[0].read_text().replace('## Resolution', '## Other'))
        self.assertFalse(self.run_audit()['ok'])

    def test_status_folder_mismatch_and_unknown_status(self):
        p = self.item()
        self.catalogue([p])
        p.rename(self.root / 'closed' / p.name)
        self.assertFalse(self.run_audit()['ok'])
        p = self.root / 'closed' / p.name
        p.write_text(p.read_text().replace('| Status | pending |', '| Status | shipped |'))
        self.assertFalse(self.run_audit()['ok'])

    def test_duplicate_numeric_ids(self):
        self.catalogue([self.item()])
        self.item('BL-00001')
        result = self.run_audit()
        self.assertFalse(result['ok'])
        self.assertTrue(any('Duplicate numeric identity' in issue for issue in result['issues']))

    def test_stale_missing_and_escaping_catalogue_rows(self):
        self.catalogue([self.item()])
        cat = self.root / 'catalogue.md'
        original = cat.read_text()
        for changed in [original.replace('Пример item', 'Stale title'), original.replace('new/BL-0001.md', '../outside.md'), original + original.splitlines()[-1] + '\n']:
            cat.write_text(changed)
            self.assertFalse(self.run_audit()['ok'])

    def test_duplicate_metadata_and_empty_required_section(self):
        p = self.item()
        self.catalogue([p])
        original = p.read_text()
        for changed in [original.replace('| ID | BL-0001 |', '| ID | BL-0001 |\n| ID | BL-0001 |'), original.replace('An observable result.', ''), original.replace('2026-11-06T05:00:00Z', 'not-a-time')]:
            p.write_text(changed)
            self.assertFalse(self.run_audit()['ok'])

    def test_unsafe_roots_and_unexpected_entries(self):
        self.catalogue([self.item()])
        for location in ['../escape', '.', '.git/queue', '.hai_env/config/queue']:
            self.assertFalse(self.run_audit(location)['ok'])
        (self.root / 'new/not-an-item.txt').write_text('preserve me')
        self.assertFalse(self.run_audit()['ok'])

    def test_linked_root_and_item(self):
        p = self.item()
        self.catalogue([p])
        try:
            (self.workspace / 'alias').symlink_to(self.root, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('Symlinks unavailable on this host')
        self.assertFalse(self.run_audit('alias')['ok'])
        original = p.read_bytes()
        p.unlink()
        target = self.workspace / 'linked.md'
        target.write_bytes(original)
        p.symlink_to(target)
        self.assertFalse(self.run_audit()['ok'])

    def test_hardlinked_item(self):
        p = self.item()
        self.catalogue([p])
        try:
            os.link(p, self.workspace / 'alias.md')
        except OSError:
            self.skipTest('Hardlinks unavailable on this host')
        self.assertFalse(self.run_audit()['ok'])

    def test_configured_activity_store_is_reserved(self):
        self.catalogue([self.item()])
        state = self.workspace / '.hai_env/state.json'
        state.parent.mkdir(exist_ok=True)
        state.write_text(json.dumps({'activities': {'location': 'planning'}}))
        self.assertFalse(self.run_audit()['ok'])

    def test_nonempty_folder_marker_is_not_silently_ignored(self):
        self.catalogue([self.item()])
        marker = self.root / 'closed/.gitkeep'
        marker.write_text('')
        self.assertTrue(self.run_audit()['ok'])
        marker.write_text('unknown user data')
        self.assertFalse(self.run_audit()['ok'])


if __name__ == '__main__':
    unittest.main()
