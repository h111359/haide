"""Pinned local core installation and gated recoverable replacement.

Incoming package code is never executed. Copies use validated descriptor-relative
writes. Executable staging remains outside the information-only product state.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
import json
from contextlib import contextmanager
import os
from pathlib import Path, PurePosixPath
import stat
import uuid

from contracts import Error, VERSION, SCHEMA_VERSION, digest, dumps, now, parse, validate_record
from security import Workspace, BoundaryError, canonical_directory
from storage import Store

CORE_DIRS = {'engine','conventions','prompts','skills'}
REQUIRED = {'engine/cli.py','run.md','README.md','USER_GUIDE.md','conventions/runtime.schema.json','skills/catalog.yaml'}


def _files(core):
    """Inspect only the explicitly supplied package, rejecting all aliases."""
    core=canonical_directory(core)
    files={}
    for current, dirs, names in os.walk(core, followlinks=False):
        for name in dirs + names:
            target=Path(current,name)
            info=target.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info,'st_file_attributes',0)&0x400 or stat.S_ISREG(info.st_mode) and info.st_nlink!=1:
                raise Error('unsafe-package','Core packages cannot contain links, aliases or reparse points.')
            if not stat.S_ISREG(info.st_mode) and not stat.S_ISDIR(info.st_mode):
                raise Error('unsafe-package','Core packages cannot contain special files.')
        for name in names:
            path=Path(current,name)
            relative=path.relative_to(core).as_posix()
            if '__pycache__' in path.parts or path.suffix in ('.pyc','.pyo'):
                raise Error('unsafe-package','Remove runtime bytecode from the immutable incoming package.')
            flags=os.O_RDONLY | getattr(os,'O_NOFOLLOW',0)
            descriptor=os.open(path,flags)
            try:
                before=os.fstat(descriptor)
                if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
                    raise Error('unsafe-package','Package identity changed while reading.')
                with os.fdopen(descriptor,'rb',closefd=False) as stream:
                    data=stream.read(32*1024*1024+1)
                if len(data)>32*1024*1024:
                    raise Error('package-size','Each incoming core file must be at most 32 MiB.')
                after=os.fstat(descriptor)
                if (before.st_size,before.st_mtime_ns,before.st_ino)!=(after.st_size,after.st_mtime_ns,after.st_ino):
                    raise Error('package-changed','Incoming package changed during validation.')
                files[relative]=data
            finally:
                os.close(descriptor)
    return files


@contextmanager
def core_maintenance(core):
    """Serialize explicit maintenance; broken or busy state cannot bypass it."""
    core=canonical_directory(core)
    if not (core.parent/'.aih_product').exists():
        _files(core)
        yield core
        return
    store=Store(core.parent)
    with store.lock():
        state=store.read('state.yaml')
        if not isinstance(state,dict):
            raise Error('maintenance-state','Existing product state is missing or invalid; reconcile it before core maintenance.')
        validate_record('state',state)
        if state.get('owner') or state.get('active_request'):
            raise Error('maintenance-busy','Core maintenance requires no open request or operational owner, including blocked requests and external reservations.')
        _files(core)
        yield core


def build_manifest(core, version=VERSION):
    """Explicit release/maintenance operation with its own fail-closed gate."""
    with core_maintenance(core) as core:
        files=_files(core)
        manifest={'schema_version':SCHEMA_VERSION,'version':version,'files':{name:digest(data) for name,data in sorted(files.items()) if name!='integrity.json'}}
        (core/'integrity.json').write_text(dumps(manifest),encoding='utf-8')
        return manifest


def inspect_core(source):
    source=Path(source)
    if source.name!='.aih' and (source/'.aih').is_dir():
        source=source/'.aih'
    files=_files(source)
    missing=REQUIRED-files.keys()
    if missing:
        raise Error('invalid-core','Incoming local core is incomplete.',{'missing':sorted(missing)})
    if 'integrity.json' not in files:
        raise Error('unpinned-core','The local source needs its reviewed release integrity.json manifest.')
    manifest=parse(files['integrity.json'].decode('utf-8'),'core integrity manifest')
    if manifest.get('schema_version')!=SCHEMA_VERSION or not isinstance(manifest.get('version'),str) or not manifest['version']:
        raise Error('incompatible-core','Unsupported core manifest or missing pinned version.')
    declared=manifest.get('files',{})
    actual={k:digest(v) for k,v in files.items() if k!='integrity.json'}
    if declared!=actual:
        raise Error('core-integrity','Incoming/installed core files differ from their pinned manifest.',{'missing':sorted(declared.keys()-actual.keys()),'unexpected':sorted(actual.keys()-declared.keys()),'modified':sorted(k for k in actual.keys()&declared.keys() if actual[k]!=declared[k])})
    directories={PurePosixPath(p).parts[0] for p in files if '/' in p}
    if directories != CORE_DIRS:
        raise Error('core-organization','Core immediate directories must be engine, conventions, prompts and skills.')
    schema=parse(files['conventions/runtime.schema.json'].decode('utf-8'),'incoming runtime schemas')
    versions=schema.get('$defs',{}).get('state',{}).get('properties',{}).get('schema_version',{}).get('enum',[])
    if SCHEMA_VERSION not in versions:
        raise Error('migration-required','Incoming state schema requires an explicitly implemented migration. No product state was changed.')
    return source.resolve(),manifest,files


class MaintenanceWorkspace(Workspace):
    """Narrow explicit core-maintenance capability, never exposed to agent content."""
    def _authorize(self,rid,parts,*,write=False,scope=None,internal=False):
        if write and rid=='home' and parts and (parts[0]=='.aih' or len(parts)>1 and parts[:2]==['.aih_runtime','core-upgrade']):
            if self.roots[rid]['access']!='read-write':
                raise BoundaryError('Maintenance requires writable home')
            return
        return super()._authorize(rid,parts,write=write,scope=scope,internal=internal)


def _prepare_home(destination):
    selected=Path(destination).absolute()
    if selected.exists():
        return canonical_directory(selected)
    # Only the explicitly selected final folder is created. Missing ancestors
    # require a separate deliberate user choice instead of expanding the scope.
    parent=canonical_directory(selected.parent)
    if os.name!='posix':
        raise Error('platform-unsupported','Safe native installation mutations require Linux/WSL.')
    fd=os.open(parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        os.mkdir(selected.name,mode=0o700,dir_fd=fd)
        os.fsync(fd)
    finally:
        os.close(fd)
    return canonical_directory(selected)


def _stage(workspace,relative,files):
    for path,data in sorted(files.items()):
        ref = 'home:'+relative+'/'+path
        workspace.atomic_write(ref,data,scope=['home:.aih_runtime/core-upgrade'])
        if path == 'menu.sh' and os.name == 'posix':
            with workspace._parent(ref,write=True,scope=['home:.aih_runtime/core-upgrade']) as (parent,name):
                descriptor = os.open(name,os.O_RDONLY | os.O_NOFOLLOW,dir_fd=parent)
                try:
                    info = os.fstat(descriptor)
                    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                        raise Error('unsafe-package','Staged Linux launcher identity changed.')
                    os.fchmod(descriptor,0o700)
                    os.fsync(descriptor)
                finally:
                    os.close(descriptor)


def _swap(workspace,source,destination):
    """Same-home directory rename, both directory handles validated at use."""
    with workspace._parent('home:'+source,write=True,scope=['home:.aih_runtime/core-upgrade']) as (src,srcname):
        info=os.stat(srcname,dir_fd=src,follow_symlinks=False)
        if not stat.S_ISDIR(info.st_mode):
            raise Error('upgrade-target','Core replacement source must be a directory.')
        with workspace._parent('home:'+destination,write=True,scope=['home:.aih_runtime/core-upgrade'],create=True) as (dst,dstname):
            try:
                os.stat(dstname,dir_fd=dst,follow_symlinks=False)
                raise Error('upgrade-target','Replacement destination already exists; reconcile the journal.')
            except FileNotFoundError:
                pass
            os.rename(srcname,dstname,src_dir_fd=src,dst_dir_fd=dst)
            os.fsync(src);os.fsync(dst)


def install(source,destination):
    incoming,manifest,files=inspect_core(source)
    home=_prepare_home(destination)
    if incoming==home/'.aih':
        return {'ok':True,'installed':True,'reused':True,'home':str(home),'version':manifest['version']}
    if incoming in home.parents or home==incoming or home in incoming.parents:
        raise Error('install-overlap','Source package and selected destination home must be disjoint.')
    target=home/'.aih'
    if target.exists():
        _,existing,_=inspect_core(target)
        if existing==manifest:
            return {'ok':True,'installed':True,'reused':True,'home':str(home),'version':manifest['version']}
        raise Error('already-installed','A different core is installed. Use explicit gated upgrade; nothing was overwritten.')
    store=Store(home)
    with store.lock():
        state=store.read('state.yaml',{})
        if state.get('owner') or state.get('active_request'):
            raise Error('maintenance-busy','Installation/repair requires no open request or operational owner.')
        workspace=MaintenanceWorkspace(home)
        opid='install-'+uuid.uuid4().hex
        staging='.aih_runtime/core-upgrade/'+opid+'/incoming'
        journal={'schema_version':'1.0','id':opid,'action':'install','status':'staging','home':str(home),'version':manifest['version'],'staging':staging,'created':now()}
        path='ledger/operations/'+opid+'/core-install.yaml'
        store.write(path,journal)
        _stage(workspace,staging,files)
        inspect_core(home/staging)
        journal['status']='prepared';store.write(path,journal)
        _swap(workspace,staging,'.aih')
        journal['status']='committed';journal['completed']=now();store.write(path,journal)
        return {'ok':True,'installed':True,'home':str(home),'version':manifest['version'],'journal':path}


def upgrade(home,source):
    home=canonical_directory(home)
    incoming,manifest,files=inspect_core(source)
    store=Store(home)
    with store.lock():
        state=store.read('state.yaml',{})
        if state.get('owner') or state.get('active_request'):
            raise Error('maintenance-busy','Core upgrade requires no open request and confirmed release of every managed/external owner.')
        _,old,_=inspect_core(home/'.aih')
        if old==manifest:
            return {'ok':True,'upgraded':False,'reused':True,'version':manifest['version']}
        opid='upgrade-'+uuid.uuid4().hex
        workspace=MaintenanceWorkspace(home)
        base='.aih_runtime/core-upgrade/'+opid
        staging=base+'/incoming';backup=base+'/previous'
        journal={'schema_version':'1.0','id':opid,'action':'upgrade','status':'staging','home':str(home),'from_version':old['version'],'to_version':manifest['version'],'staging':staging,'backup':backup,'created':now(),'steps':[]}
        path='ledger/operations/'+opid+'/core-upgrade.yaml'
        store.write(path,journal)
        if state:
            state['owner']={'id':opid,'action':'core-upgrade','status':'starting','created':now()};state['revision']+=1;store.write('state.yaml',state)
        try:
            _stage(workspace,staging,files)
            inspect_core(home/staging)
            journal['status']='prepared';store.write(path,journal)
            _swap(workspace,'.aih',backup)
            journal['steps'].append('previous-core-retained');journal['status']='replacing';store.write(path,journal)
            _swap(workspace,staging,'.aih')
            journal['steps'].append('incoming-core-installed')
            inspect_core(home/'.aih')
            journal['status']='committed';journal['completed']=now();store.write(path,journal)
            if state:
                state['owner']=None;state['revision']+=1;store.write('state.yaml',state)
            return {'ok':True,'upgraded':True,'version':manifest['version'],'previous_version':old['version'],'backup':'home:'+backup,'journal':path,'migration':'Schema 1.0 unchanged; product files and registry history preserved.'}
        except Exception:
            journal['status']='interrupted';store.write(path,journal)
            # Never silently roll back. The durable record and intact backup
            # permit an explicit recovery even if the installed entrypoint moved.
            raise


def recover_upgrade(home,journal_path,*,choice='complete'):
    """Explicit operator recovery from an interrupted pinned replacement.

    Invoke from the retained previous core if the current CLI is missing. This
    procedure does not restore former workspace memberships or product authority.
    """
    home=canonical_directory(home);store=Store(home)
    with store.lock():
        journal=store.read(journal_path)
        if journal.get('action') not in ('upgrade','install') or journal.get('home')!=str(home):
            raise Error('recovery-journal','Journal does not identify this core/home.')
        state=store.read('state.yaml',{})
        if state.get('active_request') or state.get('owner') and state['owner'].get('id')!=journal['id']:
            raise Error('maintenance-busy','Recovery cannot overlap a request or another owner.')
        workspace=MaintenanceWorkspace(home)
        if choice=='complete':
            if (home/'.aih').exists():
                _,current,_=inspect_core(home/'.aih')
                if current['version']!=journal.get('to_version',journal.get('version')):
                    raise Error('recovery-conflict','Existing core version does not match the pending installation.')
            else:
                inspect_core(home/journal['staging']);_swap(workspace,journal['staging'],'.aih')
        elif choice=='restore-previous' and journal.get('backup'):
            inspect_core(home/journal['backup'])
            if (home/'.aih').exists():
                raise Error('recovery-conflict','An installed core exists; explicit review is required before replacing it.')
            _swap(workspace,journal['backup'],'.aih')
        else:
            raise Error('recovery-choice','Choose complete or restore-previous for an interrupted upgrade.')
        journal['status']='recovered';journal['recovery_choice']=choice;journal['completed']=now();store.write(journal_path,journal)
        if state:
            state['owner']=None;state['revision']+=1;store.write('state.yaml',state)
        return {'ok':True,'recovered':True,'choice':choice,'journal':journal_path}
