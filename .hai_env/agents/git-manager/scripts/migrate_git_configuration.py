"""Explicit, guarded legacy Git settings extraction; default operation is dry-run."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import uuid

sys.dont_write_bytecode = True
from validate_git_configuration import (
    CONTRACT_PATH, ConfigurationError, configuration_path, load_contract,
    load_json, validate_settings,
)

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / '.hai/tools/startup'))
from startup_check import safe_path, overlaps, state_context, state_contract, TEMPLATE


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def _checkpoint(stage):
    """Failure-injection seam for fixture verification, without a CLI bypass."""


def guarded_path(workspace, relative):
    # Migration writes reject all symlinks, including contained aliases. Reads by
    # the validator are more permissive; mutation identity needs the fixed path.
    path = workspace
    for part in Path(relative).parts:
        path /= part
        if path.is_symlink():
            raise ConfigurationError(f'Migration rejects symbolic links: {relative}')
    return safe_path(workspace, relative)


def inspect(workspace, accept_identical=False):
    workspace = Path(workspace).resolve(strict=True)
    if not workspace.is_dir():
        raise ConfigurationError('Workspace must be an existing directory')
    source = guarded_path(workspace, '.hai_env/state.json')
    if not source.is_file() or source.stat().st_nlink != 1:
        raise ConfigurationError('Source must be a regular file without hardlink aliases')
    for reserved in ('.hai', '.git', '.hai_env/agents', '.hai_env/config',
                     '.hai_env/agent_instructions.md', '.hai_env/model_profiles.json'):
        if overlaps(source, workspace / reserved):
            raise ConfigurationError('State aliases a reserved resource')
    before = source.read_bytes()
    state = load_json(source)
    try:
        # Core schema and supported versions belong to the installed core owner.
        # Extraction preserves the inspected version and is not core migration.
        state_context(workspace, state, load_json(ROOT / TEMPLATE), state_contract())
    except ValueError as exc:
        raise ConfigurationError(f'Core state prerequisite failed: {exc}') from exc
    integrations = state.get('integrations')
    if not isinstance(integrations, dict):
        raise ConfigurationError('Legacy integrations must be an object')
    owned = {key: copy.deepcopy(integrations[key]) for key in ('git', 'github') if key in integrations}
    if not owned:
        raise ConfigurationError('No legacy Git-owned settings to migrate; no automatic retry')
    # A present old entry required Boolean enabled under the legacy contract.
    for key, value in owned.items():
        if not isinstance(value, dict) or type(value.get('enabled')) is not bool:
            raise ConfigurationError(f'Legacy {key} requires Boolean enabled; repair separately')
        if key == 'git' and 'auto_push' in value:
            push = value['auto_push']
            if not isinstance(push, dict) or type(push.get('enabled')) is not bool:
                raise ConfigurationError('Legacy auto_push requires Boolean enabled; repair separately')
    if not validate_settings(owned)['ok']:
        raise ConfigurationError('Legacy settings have invalid independent gates; repair separately')
    contract = load_contract(CONTRACT_PATH, 'git-manager')
    destination = guarded_path(workspace, '.hai_env/config/agents/git-manager.json')
    if destination.exists() and (not destination.is_file() or destination.stat().st_nlink != 1):
        raise ConfigurationError('Destination must be a regular file without hardlink aliases')
    if destination != configuration_path(workspace, 'git-manager'):
        raise ConfigurationError('Destination path identity changed')
    envelope = {'config_format_version': contract['current_config_format_version'], 'settings': owned}
    destination_before = destination.read_bytes() if destination.exists() else None
    if destination_before is not None:
        if not accept_identical or load_json(destination) != envelope:
            raise ConfigurationError('Destination exists; refuse conflict unless explicitly accepted and exactly identical')
    after = copy.deepcopy(state)
    for key in owned:
        del after['integrations'][key]
    if source.read_bytes() != before:
        raise ConfigurationError('Source changed during inspection')
    return workspace, source, before, destination, destination_before, envelope, after


def _exclusive_write(path, content):
    with path.open('xb') as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())


def migrate(workspace, *, apply=False, expected_source_sha256=None, accept_identical=False):
    workspace, source, before, destination, destination_before, envelope, after = inspect(workspace, accept_identical)
    report = {'mode': 'apply' if apply else 'dry_run', 'source_sha256': digest(before),
              'source_state_format_version': after['state_format_version'],
              'destination': '.hai_env/config/agents/git-manager.json',
              'destination_action': 'preserve_identical' if destination_before is not None else 'create',
              'migrated_keys': list(envelope['settings']), 'readiness': 'not_checked',
              'completed': [], 'backups': []}
    if not apply:
        return report
    if expected_source_sha256 != digest(before):
        raise ConfigurationError('Apply requires the source SHA-256 from the reviewed dry-run')
    # Backups are additive and exclusive. No recovery, rollback or retry is automatic.
    backup_dir = guarded_path(workspace, '.hai_env/config/migration-backups')
    if overlaps(backup_dir, source) or overlaps(backup_dir, destination):
        raise ConfigurationError('Backup directory aliases a migration target')
    operation = uuid.uuid4().hex
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        for label, content in [('state', before), ('git-manager', destination_before)]:
            if content is not None:
                path = backup_dir / f'{operation}-{label}.json'
                report['backups'].append(path.relative_to(workspace).as_posix())
                _exclusive_write(path, content)
                if path.read_bytes() != content:
                    raise ConfigurationError('Backup readback failed; stop')
        # Repeat all input/path checks after backups, before any authority switch.
        current = inspect(workspace, accept_identical)
        if current[2] != before or current[4] != destination_before:
            raise ConfigurationError('Inputs changed after inspection')
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination_before is None:
            _exclusive_write(destination, encoded(envelope))
            report['completed'].append('destination_created')
        _checkpoint('after_destination_write')
        if (guarded_path(workspace, '.hai_env/state.json') != source
                or source.read_bytes() != before
                or guarded_path(workspace, '.hai_env/config/agents/git-manager.json') != destination
                or configuration_path(workspace, 'git-manager') != destination
                or load_json(destination) != envelope):
            raise ConfigurationError('Source/destination changed or failed readback; old authority retained')
        # Read back complete old and new objects before deleting the old owned keys.
        if load_json(source) != load_json(Path(workspace / report['backups'][0])):
            raise ConfigurationError('Legacy source no longer equals verified backup')
        candidate = encoded(after)
        fd, temporary = tempfile.mkstemp(prefix='.git-migration-', dir=source.parent)
        report['prepared_state'] = Path(temporary).relative_to(workspace).as_posix()
        with os.fdopen(fd, 'wb') as stream:
            stream.write(candidate)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, source.stat().st_mode & 0o777)
        _checkpoint('before_source_replace')
        if (guarded_path(workspace, '.hai_env/state.json') != source
                or source.stat().st_nlink != 1 or destination.stat().st_nlink != 1
                or configuration_path(workspace, 'git-manager') != destination
                or source.read_bytes() != before or load_json(destination) != envelope):
            raise ConfigurationError('Inputs changed before source replacement; stop')
        os.replace(temporary, source)
        report.pop('prepared_state')
        report['completed'].append('legacy_owned_keys_removed')
        if load_json(source) != after or load_json(destination) != envelope:
            raise ConfigurationError('Final readback failed; preserve partial results')
        report['completed'].append('readback_verified')
        return report
    except (OSError, ValueError, RuntimeError) as exc:
        raise ConfigurationError(json.dumps({'error': str(exc), 'partial_result': report})) from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--expected-source-sha256')
    parser.add_argument('--accept-identical-destination', action='store_true')
    args = parser.parse_args()
    try:
        result = migrate(args.workspace, apply=args.apply,
                         expected_source_sha256=args.expected_source_sha256,
                         accept_identical=args.accept_identical_destination)
        print(json.dumps({'ok': True, **result}, indent=2))
        return 0
    except (ConfigurationError, OSError, RuntimeError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, indent=2))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
