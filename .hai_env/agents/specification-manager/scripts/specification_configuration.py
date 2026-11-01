"""Validate or explicitly configure HAI specification settings; never edits a tree."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
_PACKAGE = Path(__file__).resolve().parents[1]
_INSTALLED_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_INSTALLED_ROOT / '.hai/tools/configuration'))
sys.path.insert(0, str(_INSTALLED_ROOT / '.hai/tools/startup'))
from configuration_tools import (ConfigurationError, configuration_path, load_contract,
                                 load_json, read_configuration, workspace_directory_path)
from startup_check import check as check_core, safe_path, instruction_path

AGENT = 'specification-manager'
RELATIVE = f'.hai_env/config/agents/{AGENT}.json'


def contract():
    path = _PACKAGE / 'configuration/contract.json'
    if not path.resolve().is_relative_to(_PACKAGE) or not path.is_file() or path.stat().st_nlink > 1:
        raise ConfigurationError('Specification configuration contract must be package-contained without hardlink aliases')
    return load_contract(path, AGENT)


def check(workspace):
    """Read only this owner's settings; core assurance remains a separate result."""
    result = read_configuration(workspace, AGENT, contract())
    result['ok'] = result['status'] in ('defaulted', 'configured')
    result['scope'] = 'saved_specification_configuration_only'
    return result


def _snapshot(path):
    data = path.read_bytes() if path.exists() else None
    return data, hashlib.sha256(data).hexdigest() if data is not None else 'absent'


def _mutation_path(workspace):
    current = workspace
    for part in RELATIVE.split('/'):
        current = current / part
        if current.is_symlink() or getattr(current, 'is_junction', lambda: False)():
            raise ConfigurationError('Configuration writes reject linked path components')
    path = configuration_path(workspace, AGENT)
    if path.exists() and path.stat().st_nlink > 1:
        raise ConfigurationError('Configuration writes reject hardlink aliases')
    return path


def _dependency_paths(workspace):
    return (safe_path(workspace, '.hai_env/state.json'), instruction_path(workspace))


def _recheck_dependencies(workspace, dependencies):
    if _dependency_paths(workspace) != tuple(dependencies):
        raise ConfigurationError('Core or instruction path changed during preparation')
    if any(item.read_bytes() != value for item, value in dependencies.items()):
        raise ConfigurationError('Core or instructions changed during preparation')


def configure(workspace, *, enabled=None, location=None, apply=False, expected_source=None):
    """Prepare chosen fields, then guard a separately authorized owner-file write."""
    workspace = Path(workspace).resolve(strict=True)
    if enabled is None and location is None:
        if apply:
            raise ConfigurationError('Apply requires an explicit chosen setting')
        return check(workspace)
    if enabled is not None and type(enabled) is not bool:
        raise ConfigurationError('enabled must be Boolean')
    assurance = check_core(workspace)
    if (assurance.get('environment') != 'valid'
            or assurance.get('state_format_version') != 3
            or assurance.get('instructions_status') != 'loaded'):
        raise ConfigurationError('Setting changes require validated format-3 core and readable mandatory instructions')
    # Read dependency bytes only after safe core validation, then validate that
    # stable snapshot again to avoid using a different state than the assurance.
    dependencies = {item: item.read_bytes() for item in _dependency_paths(workspace)}
    repeated = check_core(workspace)
    if (repeated.get('environment') != 'valid' or repeated.get('state_format_version') != 3
            or repeated.get('instructions_status') != 'loaded'):
        raise ConfigurationError('Core assurance changed during preparation')
    _recheck_dependencies(workspace, dependencies)
    original = check(workspace)
    if not original['ok']:
        raise ConfigurationError('Existing invalid settings require separately scoped repair')
    path = _mutation_path(workspace)
    before, digest = _snapshot(path)
    original_mode = stat.S_IMODE(path.stat().st_mode) if before is not None else 0o600
    data = load_json(path) if before is not None else {
        'config_format_version': contract()['current_config_format_version'], 'settings': {}}
    candidate = copy.deepcopy(data)
    if enabled is not None:
        candidate['settings']['enabled'] = enabled
    if location is not None:
        # Validate disabled locations as well; an absent directory remains valid.
        workspace_directory_path(workspace, location)
        candidate['settings']['location'] = location
    selected = candidate['settings']
    effective = dict(original['settings'])
    effective.update({key: selected[key] for key in ('enabled', 'location') if key in selected})
    workspace_directory_path(workspace, effective['location'])
    result = {'ok': True, 'mode': 'apply' if apply else 'dry_run', 'path': RELATIVE,
              'source_sha256': digest, 'settings': effective, 'stages': [],
              'scope': 'specification_settings_only'}
    if not apply:
        return result
    if expected_source != digest:
        raise ConfigurationError('Apply requires the unchanged reviewed source_sha256')
    # Shared state/instructions are independent inputs. Recheck before any write.
    if check(workspace) != original or _snapshot(path)[0] != before:
        raise ConfigurationError('Configuration changed during preparation')
    _mutation_path(workspace)
    _recheck_dependencies(workspace, dependencies)
    encoded = (json.dumps(candidate, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    temporary = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        _mutation_path(workspace)
        if _snapshot(path)[0] != before:
            raise ConfigurationError('Configuration changed before write')
        if before is None:
            _recheck_dependencies(workspace, dependencies)
            if _mutation_path(workspace) != path:
                raise ConfigurationError('Configuration path changed before creation')
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, 'wb') as stream:
                stream.write(encoded)
        else:
            with tempfile.NamedTemporaryFile(mode='wb', dir=path.parent,
                                             prefix=f'.{AGENT}-', suffix='.tmp', delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(encoded)
            temporary.chmod(original_mode)
            _recheck_dependencies(workspace, dependencies)
            if _mutation_path(workspace) != path or _snapshot(path)[0] != before:
                raise ConfigurationError('Configuration path or bytes changed before replacement')
            if temporary.is_symlink() or temporary.stat().st_nlink != 1 or temporary.read_bytes() != encoded:
                raise ConfigurationError('Prepared configuration file changed before replacement')
            temporary.replace(path)
            temporary = None
        result['stages'].append('owner_configuration_written')
        observed = check(workspace)
        if not observed['ok'] or observed['settings'] != effective or path.read_bytes() != encoded:
            raise ConfigurationError('Owner configuration readback failed')
        _recheck_dependencies(workspace, dependencies)
        result['stages'].append('readback_verified')
        result['configuration_status'] = observed['status']
    except (OSError, ValueError, RuntimeError) as exc:
        result.update(ok=False, error=str(exc))
        if temporary is not None:
            result['temporary_path'] = str(temporary)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--enabled', choices=('true', 'false'))
    parser.add_argument('--location')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--expected-source-sha256')
    args = parser.parse_args()
    try:
        result = configure(args.workspace, enabled=None if args.enabled is None else args.enabled == 'true',
                           location=args.location, apply=args.apply,
                           expected_source=args.expected_source_sha256)
    except (ValueError, OSError, UnicodeError, RuntimeError) as exc:
        result = {'ok': False, 'scope': 'specification_settings_only', 'error': str(exc)}
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
