"""Read-only Activity store consistency and bounded current continuity."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import stat
import uuid

from agent_tools import Invalid, load_json
from startup_check import safe_path
from path_contract import is_link_or_reparse

CURRENT = '00000000_000000_active'
STEPS = {'clarification', 'analysis', 'planning', 'implementation', 'verification'}
STEP_VALUES = {'not_started', 'in_progress', 'completed', 'skipped'}


def _regular(path):
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or is_link_or_reparse(info) or info.st_nlink != 1:
        raise Invalid('Expected a nonlinked regular file')
    with path.open('rb') as source:
        source.read(1)


def _timestamp(value):
    if not isinstance(value, str):
        return False
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%dT%H:%M:%SZ') == value
    except ValueError:
        return False


def _validate_state(state):
    if not isinstance(state, dict):
        raise Invalid('Activity state must be an object')
    ident = state.get('activity_id')
    try:
        if not isinstance(ident, str) or not ident.strip():
            raise ValueError()
        normalized = str(uuid.UUID(ident))
    except (ValueError, AttributeError):
        raise Invalid('activity_id must be a UUID string')
    lifecycle = state.get('lifecycle')
    if lifecycle not in ('active', 'closed') or not _timestamp(state.get('created_at')):
        raise Invalid('Invalid lifecycle or created_at')
    marker = state.get('implementation_started_at', False)
    if marker is not None and not _timestamp(marker):
        raise Invalid('Invalid implementation_started_at')
    steps = state.get('steps')
    if not isinstance(steps, dict) or not STEPS.issubset(steps) or any(steps[k] not in STEP_VALUES for k in STEPS):
        raise Invalid('Invalid required steps')
    if steps['implementation'] in ('in_progress', 'completed') and marker is None:
        raise Invalid('Implementation step requires original start marker')
    if lifecycle == 'active':
        if 'closed_at' not in state or state['closed_at'] is not None or 'outcome' not in state or state['outcome'] is not None:
            raise Invalid('Active Activity must have null closure and outcome')
    elif not _timestamp(state.get('closed_at')) or state.get('outcome') not in ('completed', 'cancelled', 'stopped'):
        raise Invalid('Closed Activity requires closure timestamp and outcome')
    return normalized


def _excerpt(path, limit, tail):
    _regular(path)
    size = path.stat().st_size
    with path.open('rb') as source:
        if tail and size > limit:
            source.seek(size - limit)
        data = source.read(limit)
    # Decode strictly except for the one partial UTF-8 character at a bounded edge.
    if size > limit:
        for cut in range(4):
            try:
                text = (data[cut:] if tail else data[:len(data)-cut] if cut else data).decode('utf-8')
                break
            except UnicodeDecodeError as exc:
                if (tail and exc.start != 0) or (not tail and exc.end != len(data)) or cut == 3:
                    raise
    else:
        text = data.decode('utf-8')
    return {'path': str(path), 'status': 'loaded', 'text': text,
            'truncated': size > limit, 'portion': 'tail' if tail else 'head', 'limit_bytes': limit}


def discover(workspace, location):
    workspace = Path(workspace).resolve(strict=True)
    result = {'status': 'unverified', 'store': location, 'activity_id': None,
              'path': None, 'state': None, 'continuity': {}, 'issues': []}
    issues = result['issues']
    def issue(path, exc, code='activity'):
        issues.append({'code': code, 'path': str(path), 'message': str(exc)})
    try:
        store = safe_path(workspace, location)
        if not store.exists():
            result['status'] = 'absent'
            return result
        if not store.is_dir():
            raise Invalid('Activity store must be a directory')
        children = sorted(store.iterdir(), key=lambda item: item.name)
    except (Invalid, OSError, RuntimeError) as exc:
        result['status'] = 'invalid'
        issue(location, exc)
        return result
    ids = {}
    active = []
    for child in children:
        relative = child.relative_to(workspace).as_posix()
        try:
            info = child.lstat()
            if not stat.S_ISDIR(info.st_mode) or is_link_or_reparse(info):
                raise Invalid('Activity store child must be a nonlinked directory')
            if child.resolve(strict=True).parent != store:
                raise Invalid('Activity folder escapes store')
            state_path = child / 'state.json'
            _regular(state_path)
            state = load_json(state_path)
            ident = _validate_state(state)
            if ident in ids:
                raise Invalid(f'Duplicate Activity ID also present at {ids[ident]}')
            ids[ident] = relative
            required = ('input.md', 'log.md') + (('outcome.md',) if state['lifecycle'] == 'closed' else ())
            for name in required:
                _regular(child / name)
            for name in ('decisions.md', 'definition.md', 'analysis.md', 'plan.md', 'outcome.md', 'chat.jsonl', 'usage.md', 'usage.json'):
                path = child / name
                if name not in required and (path.exists() or path.is_symlink()):
                    _regular(path)
            if state['lifecycle'] == 'closed':
                match = re.fullmatch(r'(\d{8}_\d{6})_([a-z0-9]+(?:-[a-z0-9]+){0,4})(?:_(\d{2,}))?', child.name)
                expected = state['closed_at'].replace('-', '').replace(':', '').replace('T', '_').removesuffix('Z')
                if (not match or match.group(1) != expected
                        or (match.group(3) is not None and int(match.group(3)) < 2)):
                    raise Invalid('Closed Activity folder must match closure timestamp and archive naming convention')
            if state['lifecycle'] == 'active':
                active.append((child, state))
                if child.name != CURRENT:
                    raise Invalid('Active Activity must use the current folder')
            elif child.name == CURRENT:
                raise Invalid('Current folder cannot contain a closed Activity')
        except (Invalid, OSError, UnicodeError, ValueError, TypeError, RuntimeError) as exc:
            issue(relative, exc)
    if len(active) > 1:
        issue(location, Invalid('Multiple active Activities'))
    if issues:
        result['status'] = 'invalid'
        return result
    if not active:
        result['status'] = 'absent'
        return result
    child, state = active[0]
    result.update(status='current', activity_id=state['activity_id'],
                  path=child.relative_to(workspace).as_posix(), state={key: state[key] for key in
                      ('activity_id', 'lifecycle', 'created_at', 'closed_at', 'outcome',
                       'implementation_started_at', 'steps')})
    result['state']['steps'] = {key: state['steps'][key] for key in sorted(STEPS)}
    for name, limit, tail in (('input.md', 384, False), ('plan.md', 768, True),
                               ('decisions.md', 512, True), ('log.md', 1024, True)):
        path = child / name
        relative = path.relative_to(workspace).as_posix()
        try:
            if not path.exists() and not path.is_symlink():
                result['continuity'][name] = {'path': relative, 'status': 'absent'}
                continue
            excerpt = _excerpt(path, limit, tail)
            excerpt['path'] = relative
            result['continuity'][name] = excerpt
        except (Invalid, OSError, UnicodeError, RuntimeError) as exc:
            result['continuity'][name] = {'path': relative, 'status': 'invalid'}
            issue(relative, exc, 'activity_continuity')
    return result
