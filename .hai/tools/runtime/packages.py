"""External package inspection and explicit local installation."""
from pathlib import Path
import hashlib
import os
import re
import shutil
import stat
import sys
import uuid
from .storage import SafetyError, checked_path, fingerprint, write_bytes, lock
from .activities import envelope, provenance, rename_exclusive, rename_preflight
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'agents'))
import agent_tools as agents

def snapshot(root, relative):
    base = checked_path(root, relative, allow_missing=False)
    if not base.is_dir(): raise SafetyError('package source must be a directory')
    result = {}
    for directory, dirs, files in os.walk(base, followlinks=False):
        for name in dirs + files:
            p = Path(directory) / name; rel = str(p.relative_to(root)); checked_path(root, rel, allow_missing=False)
            mode = p.lstat().st_mode
            if not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)): raise SafetyError('package contains nonregular entry')
            if stat.S_ISREG(mode): result[str(p.relative_to(base))] = fingerprint(p)
    if 'SKILL.md' not in result: raise SafetyError('package lacks SKILL.md')
    return result

def handle(operation, workspace, request, apply, _locked=False):
    root = Path(workspace).resolve(strict=True); op = operation.split('.')[-1].split('/')[-1]; changed = []
    try:
        fields = {'validate':{'definition'}, 'audit':set(), 'resolve':{'definition','runtime'}, 'install':{'source','name','replace','register','reviewed_differences','provenance'}, 'register':{'name','provenance'}}
        if not isinstance(request,dict) or (op in fields and set(request) - fields[op]): raise ValueError('Unknown or invalid request fields')
        def run():
            if apply and op in ('install','register'):
                from .startup import require_mutation_context
                require_mutation_context(root)
            if op == 'validate':
                result = agents.validate(root, request.get('definition'))
                return envelope(operation, 'ok' if result['ok'] else 'blocked', result, issues=result.get('issues'))
            if op == 'audit':
                result = agents.audit(root)
                return envelope(operation, 'ok' if result['ok'] else 'blocked', result, issues=result.get('issues'))
            if op == 'resolve':
                result = agents.resolve(root, request.get('definition'), request.get('runtime'))
                return envelope(operation, 'ok' if result['ok'] else 'blocked', result, issues=result.get('issues'))
            provenance(request)
            name = request.get('name')
            if not isinstance(name,str) or len(name)>64 or not agents.NAMES.fullmatch(name): raise ValueError('invalid package name')
            dest = '.hai_env/agents/' + name; target = checked_path(root,dest)
            if op == 'register':
                result = agents.validate(root, dest + '/SKILL.md')
                if not result['ok']: raise SafetyError(str(result['issues']))
                fields = agents.read_definition(checked_path(root,dest + '/SKILL.md',allow_missing=False),root)
                cat = '.hai_env/agents/catalogue.md'; path = checked_path(root,cat); fp = fingerprint(path)
                if fp:
                    audit = agents.audit(root)
                    unrelated = [i for i in audit['issues'] if i.get('code') != 'profiles' and not (i.get('agent') == name and i.get('message') == 'Catalogue copy differs from canonical decoded description')]
                    if unrelated: raise SafetyError('Catalogue cannot be safely updated: ' + str(unrelated))
                content = path.read_text(encoding='utf-8') if fp else '# Agent catalogue\n\n| Agent | Selection guide | Definition |\n| --- | --- | --- |\n'
                lines = content.splitlines(keepends=True); headers = [i for i,x in enumerate(lines) if x.strip() == '| Agent | Selection guide | Definition |']
                if len(headers)!=1 or headers[0]+1>=len(lines) or lines[headers[0]+1].strip() != '| --- | --- | --- |': raise SafetyError('unsupported catalogue structure')
                idx = headers[0]+2; found = None
                while idx<len(lines) and lines[idx].lstrip().startswith('|'):
                    row = [cell.strip() for cell in lines[idx].strip().strip('|').split('|')]
                    if len(row) != 3 or not re.fullmatch(r'`[a-z0-9]+(?:-[a-z0-9]+)*`',row[0]) or not row[1] or row[2] != f'[SKILL.md]({row[0][1:-1]}/SKILL.md)': raise SafetyError('malformed catalogue row')
                    if row[0][1:-1].casefold() == name.casefold():
                        if found is not None or row[0] != f'`{name}`': raise SafetyError('duplicate or conflicting registration')
                        found = idx
                    idx += 1
                description = fields['description'].replace('&','&amp;').replace('\\','&#92;').replace('|','&#124;')
                row = f'| `{name}` | {description} | [SKILL.md]({name}/SKILL.md) |\n'
                if found is None: lines.insert(idx, row)
                else: lines[found] = row
                new = ''.join(lines).encode()
                if apply and (fp is None or path.read_bytes() != new): write_bytes(root,cat,new,fp); changed.append(cat)
                return envelope(operation,'ok' if apply else 'planned',{'path':cat,'description':fields['description']},changed)
            if op != 'install': return envelope(operation,'unsupported',issues=['Remote acquisition and this package operation are unsupported'])
            source = request.get('source')
            if not isinstance(source,str) or '://' in source: return envelope(operation,'unsupported',issues=['Only workspace-relative local package sources are supported'])
            src = checked_path(root,source,allow_missing=False)
            if src.name != name: raise ValueError('source folder name must equal package name')
            if src == target or src in target.parents or target in src.parents: raise SafetyError('source and installed paths must be distinct')
            files = snapshot(root,source)
            if (src / 'knowledge.md').exists() or (src / 'knowledge.md').is_symlink(): raise SafetyError('conflicting legacy knowledge.md')
            fields = agents.read_definition(src / 'SKILL.md',root)
            if fields['name'] != name: raise SafetyError('package identity mismatch')
            replace = request.get('replace',False); register = request.get('register',False)
            if type(replace) is not bool or type(register) is not bool: raise ValueError('replace and register must be booleans')
            previous = snapshot(root,dest) if target.exists() else None
            differences = sorted(set(files) | set(previous or {}))
            differences = [x for x in differences if x not in files or x not in (previous or {}) or files[x][-1] != previous[x][-1]]
            if previous is not None and not replace: raise SafetyError('installed package exists; replacement not authorized')
            if previous is not None and request.get('reviewed_differences') != differences: raise SafetyError('replacement requires exact reviewed_differences')
            result = {'source':source,'destination':dest,'differences':differences,'registration_requested':register}
            if not apply: return envelope(operation,'planned',result)
            if snapshot(root,source) != files or (previous is not None and snapshot(root,dest) != previous): raise SafetyError('package changed since inspection')
            rename_preflight()
            agents_dir = checked_path(root, '.hai_env/agents')
            if not agents_dir.exists(): agents_dir.mkdir(); changed.append('.hai_env/agents')
            # Staging stays recoverable on a partial failure and is never silently deleted.
            stage = '.hai_env/agents/.hai-stage-' + uuid.uuid4().hex; container = checked_path(root,stage); container.mkdir(); changed.append(stage)
            stagepath = checked_path(root,stage + '/' + name)
            shutil.copytree(src,stagepath,symlinks=False); changed.append(stage + '/' + name)
            if snapshot(root,source) != files or {k:v[-1] for k,v in snapshot(root,stage + '/' + name).items()} != {k:v[-1] for k,v in files.items()}: raise SafetyError('source or staging changed during copy')
            agents.read_definition(stagepath / 'SKILL.md', root)
            if previous is not None:
                backup = '.hai_env/agents/.hai-backup-' + uuid.uuid4().hex
                rename_exclusive(target,checked_path(root,backup)); changed.append(backup); result['backup'] = backup
            if target.exists(): raise SafetyError('destination appeared during installation')
            rename_exclusive(stagepath,target); changed.append(dest)
            if previous is not None and not register:
                cat = checked_path(root, '.hai_env/agents/catalogue.md')
                if cat.exists() and re.search(r'^\|\s*`' + re.escape(name) + r'`\s*\|', cat.read_text(encoding='utf-8'), re.M | re.I):
                    result['registration_sync'] = 'pending; run packages register to synchronize description'
                    return envelope(operation,'partial',result,changed,['Existing registration requires review and synchronization'])
            if register:
                registration = run_registration(root, name, request)
                changed.extend(registration['changed_files'])
                if not registration['ok']: return envelope(operation,'partial',result,changed,registration['issues'])
            return envelope(operation,result=result,changed=changed)
        if apply and op in ('install','register') and not _locked:
            with lock(root): return run()
        return run()
    except (agents.Invalid, agents.UnsupportedYAML, SafetyError, OSError, UnicodeError) as exc:
        changed.extend(x for x in getattr(exc, 'changed_files', []) if x not in changed)
        return envelope(operation,'partial' if changed else 'blocked',changed=changed,issues=[str(exc)])
    except (ValueError,TypeError,KeyError) as exc:
        return envelope(operation,'partial' if changed else 'input_error',changed=changed,issues=[str(exc)])

def run_registration(root, name, request):
    return handle('register', root, {'name': name, 'provenance': request['provenance']}, True, _locked=True)
