"""Activity-local coordination messages with read and append operations only."""
from datetime import datetime
import json
import os
import re
import uuid

from .storage import SafetyError, _pairs, checked_path, fingerprint

MAX_TEXT_BYTES = 65536
FIELDS = {'chat_format_version', 'activity_id', 'message_id', 'sequence',
          'created_at', 'author', 'text', 'provenance'}
AUTHOR = re.compile(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z')


def author(value):
    if not isinstance(value, str) or len(value) > 64 or not AUTHOR.fullmatch(value):
        raise ValueError('author must be a lower-case agent name or host-coordinator (up to 64 characters)')
    return value


def text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('text must be nonempty text')
    if len(value.encode('utf-8')) > MAX_TEXT_BYTES:
        raise ValueError('text exceeds 65536 UTF-8 bytes')
    return value


def _uuid(value):
    return isinstance(value, str) and str(uuid.UUID(value)) == value


def load(root, relative, activity_id):
    """Validate the whole existing history without changing it."""
    path = checked_path(root, relative)
    before = fingerprint(path)
    if before is None:
        return [], b'', None
    raw = path.read_bytes()
    if fingerprint(checked_path(root, relative)) != before:
        raise SafetyError('Chat changed while reading')
    if raw and not raw.endswith(b'\n'):
        raise SafetyError('Chat has an incomplete final record; preserve it for inspection')
    messages, identities = [], set()
    for number, line in enumerate(raw.split(b'\n')[:-1], 1):
        try:
            message = json.loads(line.decode('utf-8'), object_pairs_hook=_pairs,
                                 parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Invalid JSON constant')))
            if not isinstance(message, dict) or set(message) != FIELDS:
                raise ValueError('Unexpected message schema')
            if type(message['chat_format_version']) is not int or message['chat_format_version'] != 1:
                raise ValueError('Unsupported chat format')
            if message['activity_id'] != activity_id:
                raise ValueError('Message belongs to another Activity')
            if not _uuid(message['message_id']) or message['message_id'] in identities:
                raise ValueError('Invalid or duplicate message ID')
            if type(message['sequence']) is not int or message['sequence'] != number:
                raise ValueError('Message sequence is missing, duplicated or reordered')
            stamp = message['created_at']
            if not isinstance(stamp, str) or datetime.strptime(stamp, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%dT%H:%M:%SZ') != stamp:
                raise ValueError('Invalid message timestamp')
            author(message['author']); text(message['text'])
            prov = message['provenance']
            if not isinstance(prov, dict) or set(prov) != {'source', 'reason'} or any(not isinstance(v, str) or not v.strip() for v in prov.values()):
                raise ValueError('Invalid message provenance')
        except (ValueError, UnicodeError, TypeError, KeyError, AttributeError, SafetyError) as exc:
            raise SafetyError(f'Invalid chat record {number}: {exc}') from exc
        identities.add(message['message_id'])
        messages.append(message)
    return messages, raw, before


def read(root, base, activity_id, request):
    after = request.get('after_sequence', 0)
    limit = request.get('limit', 100)
    if type(after) is not int or after < 0:
        raise ValueError('after_sequence must be a nonnegative integer')
    if type(limit) is not int or not 1 <= limit <= 1000:
        raise ValueError('limit must be an integer from 1 through 1000')
    relative = base + '/chat.jsonl'
    messages, _, _ = load(root, relative, activity_id)
    page = messages[after:after + limit]
    cursor = page[-1]['sequence'] if page else after
    return {'activity_id': activity_id, 'path': relative, 'messages': page,
            'total_messages': len(messages), 'next_after_sequence': cursor,
            'has_more': cursor < len(messages)}


def prepare(root, base, activity_id, request, stamp):
    who, content = author(request.get('author')), text(request.get('text'))
    relative = base + '/chat.jsonl'
    messages, raw, before = load(root, relative, activity_id)
    message = {'chat_format_version': 1, 'activity_id': activity_id,
               'message_id': str(uuid.uuid4()), 'sequence': len(messages) + 1,
               'created_at': stamp, 'author': who, 'text': content,
               'provenance': {key: request['provenance'][key] for key in ('source', 'reason')}}
    return relative, message, raw, before


def append(root, relative, activity_id, message, raw, expected):
    """Append once, under the caller's runtime lock; never replace old bytes."""
    path = checked_path(root, relative)
    if fingerprint(path) != expected:
        raise SafetyError('Chat changed before append')
    record = (json.dumps(message, ensure_ascii=True, separators=(',', ':')) + '\n').encode('utf-8')
    flags = os.O_WRONLY | os.O_APPEND | getattr(os, 'O_NOFOLLOW', 0)
    flags |= os.O_CREAT | os.O_EXCL if expected is None else 0
    fd = None
    may_have_changed = False
    try:
        fd = os.open(path, flags, 0o600)
        if expected is None:
            may_have_changed = True
        current = fingerprint(checked_path(root, relative))
        opened = os.fstat(fd)
        if ((expected is not None and current != expected)
                or opened.st_nlink != 1 or current is None
                or (opened.st_dev, opened.st_ino, opened.st_size) != current[:3]):
            raise SafetyError('Chat target changed before append')
        # One append syscall; a short or failed write is reported, never retried.
        may_have_changed = True
        if os.write(fd, record) != len(record):
            raise SafetyError('Partial chat append; inspect retained bytes before further work')
        os.fsync(fd)
        os.close(fd); fd = None
        if checked_path(root, relative).read_bytes() != raw + record:
            raise SafetyError('Chat readback differs from the exact old prefix plus new record')
        messages, _, _ = load(root, relative, activity_id)
        if messages[-1] != message:
            raise SafetyError('Appended message readback mismatch')
    except (OSError, ValueError, SafetyError) as exc:
        raise SafetyError(str(exc), [relative] if may_have_changed else []) from exc
    finally:
        if fd is not None:
            os.close(fd)
