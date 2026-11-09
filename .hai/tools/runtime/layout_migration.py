"""Explicit byte-preserving relocation; never repairs mixed or partial layouts."""
from pathlib import Path
import hashlib
import uuid

from environment_paths import STATE, PROFILES, INSTRUCTIONS, LEGACY, legacy_entries
from .storage import (SafetyError, checked_path, fingerprint, read_json, lock,
                      write_bytes, write_json)

MANIFEST = '.hai_env/config/layout-migration.json'


def _inspect(root):
    # Import through environment so standalone/CLI entry points share validators.
    from .environment import startup, agent_tools
    marker = checked_path(root, MANIFEST)
    if marker.exists() and read_json(marker).get('status') != 'completed':
        raise SafetyError('Incomplete layout migration; inspect layout-migration.json and recovery copies. Explicit recovery is required.')
    legacy = legacy_entries(root)
    if not legacy:
        context = startup.check(root)
        if context['environment'] != 'valid' or context['instructions_status'] != 'loaded':
            raise SafetyError('No valid legacy or current environment to migrate')
        return [], {}
    if marker.exists():
        raise SafetyError('Legacy files coexist with a previous migration; reconcile explicitly')
    entries = []
    for new, old in LEGACY.items():
        source = checked_path(root, old)
        target = checked_path(root, new)
        if target.exists():
            raise SafetyError('Mixed layout or destination collision; reconcile explicitly: ' + new)
        before = fingerprint(source)
        if before is None:
            if new == PROFILES:
                continue
            raise SafetyError('Mandatory legacy file is missing: ' + old)
        content = source.read_bytes()
        if new == INSTRUCTIONS:
            content.decode('utf-8-sig')  # Empty is valid; preserve bytes exactly.
        elif new == PROFILES:
            agent_tools.read_profiles(source)
        else:
            state = read_json(source)
            startup.state_context(root, state,
                                  read_json(checked_path(root, startup.TEMPLATE, allow_missing=False)),
                                  startup.state_contract())
        entries.append({'source': old, 'destination': new, 'before': before,
                        'content': content, 'sha256': hashlib.sha256(content).hexdigest()})
    # Backup all files before any source is removed; retire state last.
    entries.sort(key=lambda entry: entry['destination'] == STATE)
    dependencies = {}
    for relative in ('.hai/templates/state.json', '.hai_env/config/agents/specification-manager.json'):
        dependencies[relative] = fingerprint(checked_path(root, relative))
    return entries, dependencies


def migrate(workspace, request, apply=False):
    root = Path(workspace).resolve(strict=True)
    changed = []
    try:
        entries, dependencies = _inspect(root)
        moves = [{'source': e['source'], 'destination': e['destination'], 'sha256': e['sha256']}
                 for e in entries]
        if not entries:
            return {'ok': True, 'status': 'unchanged', 'result': {'moves': []}, 'changed_files': [], 'issues': []}
        result = {'moves': moves, 'schema_conversion': 'Separate explicit operation when state_format_version is 2',
                  'writer_requirement': 'Stop other environment writers before applying'}
        if not apply:
            return {'ok': True, 'status': 'planned', 'result': result, 'changed_files': [], 'issues': []}
        with lock(root):
            current, current_dependencies = _inspect(root)
            if current != entries or current_dependencies != dependencies:
                raise SafetyError('Inspected migration inputs changed')
            config = checked_path(root, '.hai_env/config')
            if not config.exists():
                config.mkdir(); changed.append('.hai_env/config/')
            backups_rel = '.hai_env/config/migration-backups'
            backups = checked_path(root, backups_rel)
            if not backups.exists():
                backups.mkdir(); changed.append(backups_rel + '/')
            backup_rel = backups_rel + '/' + str(uuid.uuid4())
            checked_path(root, backup_rel).mkdir(); changed.append(backup_rel + '/')
            result['backup_path'] = backup_rel
            manifest = {'status': 'in_progress', 'provenance': request['provenance'],
                        'backup_path': backup_rel, 'moves': moves}
            write_json(root, MANIFEST, manifest); changed.append(MANIFEST)
            for e in entries:
                backup = backup_rel + '/' + Path(e['source']).name
                write_bytes(root, backup, e['content']); changed.append(backup)
                if checked_path(root, backup).read_bytes() != e['content']:
                    raise SafetyError('Recovery copy verification failed: ' + backup)
            for e in entries:
                if fingerprint(checked_path(root, e['source'])) != e['before']:
                    raise SafetyError('Source changed: ' + e['source'])
                write_bytes(root, e['destination'], e['content']); changed.append(e['destination'])
            # Verify the whole candidate before deleting any legacy resource.
            for e in entries:
                if checked_path(root, e['destination']).read_bytes() != e['content']:
                    raise SafetyError('Destination readback failed: ' + e['destination'])
                if fingerprint(checked_path(root, e['source'])) != e['before']:
                    raise SafetyError('Source changed before retirement: ' + e['source'])
            for relative, before in dependencies.items():
                if fingerprint(checked_path(root, relative)) != before:
                    raise SafetyError('Dependency changed: ' + relative)
            for e in entries:
                if (fingerprint(checked_path(root, e['source'])) != e['before']
                        or checked_path(root, e['destination']).read_bytes() != e['content']):
                    raise SafetyError('Inspected migration input changed during retirement')
                checked_path(root, e['source'], allow_missing=False).unlink()
                changed.append(e['source'])
            before = fingerprint(checked_path(root, MANIFEST))
            manifest['status'] = 'completed'
            write_json(root, MANIFEST, manifest, before)
            from .environment import startup
            context = startup.check(root)
            if context['environment'] != 'valid' or context['instructions_status'] != 'loaded':
                raise SafetyError('Post-migration startup failed; inspect retained recovery copies')
            result['state_format_version'] = context['state_format_version']
        return {'ok': True, 'status': 'migrated', 'result': result, 'changed_files': changed, 'issues': []}
    except Exception as exc:
        changed.extend(getattr(exc, 'changed_files', []))
        return {'ok': False, 'status': 'partial' if changed else 'blocked',
                'result': {'recovery': 'Preserve all files; inspect layout-migration.json and migration-backups before explicit recovery'},
                'changed_files': list(dict.fromkeys(changed)),
                'issues': [{'code': 'layout_migration', 'message': str(exc)}]}
