"""Exact human-authorized correction of retained records and recovery copies."""
from __future__ import annotations
import base64
import binascii
import json
from contracts import Error, digest, dumps, screen

REPLACEMENT='[REDACTED by explicit human authorization]'


def validate_intake(payload):
    """Check non-sensitive audit fields before an operation is persisted."""
    sensitive=payload.get('value')
    reason=payload.get('reason')
    paths=payload.get('paths')
    if not isinstance(sensitive,str) or len(sensitive)<8 or not isinstance(reason,str) or not reason.strip() or not isinstance(paths,list) or not paths or any(not isinstance(path,str) for path in paths):
        raise Error('redaction-scope','Identify the sensitive value, retained AIH-owned record paths, and a non-sensitive reason.')
    metadata=dumps({key:value for key,value in payload.items() if key!='value'})
    screen(metadata,'non-sensitive redaction metadata')
    if sensitive in metadata:
        raise Error('redaction-metadata','Redaction audit fields must not repeat the sensitive value.')


def rewrite(value, sensitive):
    """Return corrected data without storing the supplied sensitive value."""
    if isinstance(value,str):
        return value.replace(sensitive,REPLACEMENT)
    if isinstance(value,list):
        return [rewrite(item,sensitive) for item in value]
    if not isinstance(value,dict):
        return value
    corrected={key:rewrite(item,sensitive) for key,item in value.items()}
    # Interrupted information transactions retain a base64 replay payload. A
    # plaintext-only scan misses it and a later recovery could restore secrets.
    if isinstance(value.get('data_base64'),str):
        try:
            raw=base64.b64decode(value['data_base64'],validate=True).decode('utf-8')
            updated=redact_text(raw,sensitive)
        except (UnicodeError,ValueError,binascii.Error):
            updated=raw=None
        if raw is not None and updated!=raw:
            corrected['data_base64']=base64.b64encode(updated.encode('utf-8')).decode('ascii')
            corrected['redaction']={'original_after':value.get('after'),'requires_evidence_reconciliation':True}
            if 'after' in value:
                corrected['after']=digest(updated)
    return corrected


def redact_text(text,sensitive):
    """Preserve ordinary text; decode structured records before exact matching."""
    try:
        original=json.loads(text)
    except (ValueError,TypeError):
        return text.replace(sensitive,REPLACEMENT)
    corrected=rewrite(original,sensitive)
    return dumps(corrected) if corrected!=original else text


def retained_copy(path,text,sensitive):
    corrected=redact_text(text,sensitive)
    if corrected!=text and '/edits-' in path and path.endswith('-journal.yaml'):
        # Editing retained proposals does not authorize changing ordinary product
        # files. Preserve recorded hashes and block their replay for new review.
        record=json.loads(corrected)
        record['redaction_requires_reauthorization']=True
        record['redaction_note']='Historical content was corrected; reconcile current product evidence and issue fresh explicit edit authority before replay.'
        corrected=dumps(record)
    return corrected
