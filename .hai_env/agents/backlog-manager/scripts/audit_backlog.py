"""Read-only consistency audit of an explicitly selected workspace backlog."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys

CORE = Path(__file__).resolve().parents[4] / '.hai/tools'
sys.path.insert(0, str(CORE / 'configuration'))
sys.path.insert(0, str(CORE / 'startup'))
from configuration_tools import (ConfigurationError, load_contract,
                                 read_configuration, workspace_directory_path)
import startup_check

ID = re.compile(r'BL-([0-9]{4,})\Z')
STATUSES = {'pending', 'completed', 'cancelled', 'rejected'}
FIELDS = {'ID', 'Status', 'Created', 'Updated', 'Closed', 'Activities', 'Source'}
HEADER = '| ID | Title | Status | File |'


def regular(path: Path):
    if path.is_symlink() or not path.is_file() or path.stat().st_nlink != 1:
        raise ValueError(f'Expected a regular nonlinked file: {path.name}')


def utc(value: str):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', value):
        raise ValueError('Expected an actual UTC timestamp')
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')


def parse_item(path: Path):
    regular(path)
    text = path.read_text(encoding='utf-8')
    heading = re.match(r'# (BL-[0-9]{4,}) — ([^\n]+)\n', text)
    if not heading or path.stem != heading[1]:
        raise ValueError('Item heading and filename must identify the same ID')
    fields = {}
    preamble = text[:text.find('\n## ')]
    if preamble.count('| Field | Value |') != 1:
        raise ValueError('Expected one item metadata table')
    for line in preamble.splitlines():
        if not line.startswith('|'):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        if cells == ['Field', 'Value'] or all(re.fullmatch(r':?-+:?', c) for c in cells):
            continue
        if len(cells) != 2 or not all(cells) or cells[0] in fields:
            raise ValueError('Invalid or duplicate metadata field')
        fields[cells[0]] = cells[1]
    if not FIELDS <= fields.keys() or fields['ID'] != heading[1]:
        raise ValueError('Missing metadata or inconsistent ID')
    if fields['Status'] not in STATUSES:
        raise ValueError('Unsupported status')
    for name in ['What', 'Why', 'Acceptance Criteria', 'History']:
        if len(re.findall(r'^## ' + re.escape(name) + r'$', text, re.M)) != 1:
            raise ValueError(f'Expected exactly one {name} section')
        section = re.search(r'^## ' + re.escape(name) + r'\n(.*?)(?=^## |\Z)', text, re.M | re.S)
        if not section or not section[1].strip():
            raise ValueError(f'Empty {name} section')
    updated = utc(fields['Updated'])
    if fields['Status'] == 'pending':
        if path.parent.name != 'new' or fields['Closed'] != '—':
            raise ValueError('Pending item must be in new/ with Closed —')
    else:
        if path.parent.name != 'closed' or utc(fields['Closed']) > updated:
            raise ValueError('Terminal item needs closed/ and a consistent closure timestamp')
        resolution = re.search(r'^## Resolution\n(.*?)(?=^## |\Z)', text, re.M | re.S)
        if len(re.findall(r'^## Resolution$', text, re.M)) != 1 or not resolution or not resolution[1].strip():
            raise ValueError('Terminal item needs one nonempty Resolution')
    return {'id': heading[1], 'title': heading[2], 'status': fields['Status'],
            'file': path.parent.name + '/' + path.name,
            'unknown_fields': sorted(set(fields) - FIELDS)}


def catalogue_row(item):
    title = item['title'].replace('|', '&#124;')
    return f"| {item['id']} | {title} | {item['status']} | [{item['id']}]({item['file']}) |"


def audit(workspace, location=None):
    workspace = Path(workspace).resolve(strict=True)
    issues, items = [], []
    result = {'ok': False, 'scope': 'read_only_backlog_structure_and_catalogue',
              'issues': issues, 'items': items}
    try:
        contract = load_contract(Path(__file__).resolve().parents[1] / 'configuration/contract.json', 'backlog-manager')
        configuration = read_configuration(workspace, 'backlog-manager', contract)
        result['configuration_status'] = configuration['status']
        if configuration['status'] not in ('configured', 'defaulted'):
            raise ValueError('Backlog configuration is invalid or unverified')
        location = location if location is not None else configuration['settings']['location']
        # Optional owner settings are independent of core state. Their uncertainty
        # must not be silently interpreted as an absent content location.
        owner = startup_check.check(workspace).get('agent_configurations', {}).get('specification-manager', {})
        if owner.get('status') in ('invalid', 'unverified'):
            raise ValueError('Specification content location is invalid or unverified')
        reserved = ['hai_agents_library']
        if owner.get('status') in ('configured', 'defaulted'):
            reserved.append(owner['settings']['location'])
        target = workspace_directory_path(workspace, location, reserved_paths=reserved)
        cursor = workspace
        for part in Path(location).parts:
            cursor /= part
            if cursor.is_symlink():
                raise ValueError('Linked backlog ancestors or root are unsupported')
        result['location'] = location
        if not target.is_dir():
            raise ValueError('Backlog root is absent or not a directory')
        identities = set()
        for folder in ['new', 'closed']:
            directory = target / folder
            if directory.is_symlink() or not directory.is_dir():
                raise ValueError(f'Missing or linked {folder}/ directory')
            for path in sorted(directory.iterdir()):
                try:
                    regular(path)
                    if path.name == '.gitkeep' and not path.read_bytes():
                        continue
                    if path.suffix != '.md' or not ID.fullmatch(path.stem):
                        raise ValueError('Unexpected entry in item folder')
                    item = parse_item(path)
                    number = int(ID.fullmatch(item['id'])[1])
                    if number == 0 or number in identities:
                        raise ValueError('Duplicate numeric identity or zero ID')
                    identities.add(number)
                    items.append(item)
                except (ValueError, OSError, UnicodeError) as exc:
                    issues.append(f'{folder}/{path.name}: {exc}')
        items.sort(key=lambda item: int(ID.fullmatch(item['id'])[1]))
        catalogue = target / 'catalogue.md'
        regular(catalogue)
        lines = catalogue.read_text(encoding='utf-8').splitlines()
        if lines.count(HEADER) != 1:
            raise ValueError('Expected exactly one catalogue table')
        start = lines.index(HEADER)
        if start + 1 >= len(lines) or lines[start + 1] != '| --- | --- | --- | --- |':
            raise ValueError('Unexpected catalogue separator')
        rows = []
        for line in lines[start + 2:]:
            if not line.startswith('|'):
                break
            rows.append(line)
        if rows != [catalogue_row(item) for item in items]:
            issues.append('Catalogue rows do not exactly match live items in numeric order')
        result['counts'] = {status: sum(i['status'] == status for i in items) for status in sorted(STATUSES)}
        result['ok'] = not issues
    except (ValueError, ConfigurationError, OSError, UnicodeError, KeyError) as exc:
        issues.append(str(exc))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', default='.')
    parser.add_argument('--location', help='Explicit root for bounded inspection; does not save settings')
    args = parser.parse_args()
    result = audit(args.workspace, args.location)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
