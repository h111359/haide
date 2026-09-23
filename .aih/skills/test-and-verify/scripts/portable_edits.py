"""Standalone plan-bound edits using canonical product journals and explicit output.

The adapters below provide the small workspace/store interfaces required by
product_edits. No lifecycle initialization or fixed product-state path is used.
"""
from __future__ import annotations
import contextlib
import json
import os
from pathlib import PurePosixPath
import stat
from product_edits import apply_edits, reconcile
from security import BoundaryError


def helpers():
    try:
        import skill_helpers as helper
    except ModuleNotFoundError:
        import helper
    return helper


class ScopedWorkspace:
    def __init__(self,workspace,contract):
        self.wrapped=workspace
        self.roots=workspace.roots
        self.revision=contract['workspace_revision']

    def parse(self,ref):
        if not isinstance(ref,str) or ':' not in ref:
            raise BoundaryError('Product effects require root-qualified paths')
        rid,path=ref.split(':',1)
        self.wrapped.resolve({'root':rid,'path':path})
        return rid,list(PurePosixPath(path).parts)

    def ref(self,ref):
        rid,parts=self.parse(ref)
        return {'root':rid,'path':'/'.join(parts)}

    def resolve(self,ref,write=False,scope=None):
        try:
            rid,parts=self.parse(ref)
            if write:
                if not parts or '.aih' in parts or '.aih_product' in parts:
                    raise BoundaryError('Standalone product edits cannot mutate core or framework state')
                if not scope or ref not in scope:
                    raise BoundaryError('Effect is outside this exact planned task scope')
            return self.wrapped.resolve({'root':rid,'path':'/'.join(parts)},write=write)
        except helpers().ContractError as exc:
            raise BoundaryError(str(exc)) from exc

    def read_bytes(self,ref):
        return self.wrapped.read(self.ref(ref))

    def atomic_write(self,ref,data,scope=None,expected_hash='unchecked'):
        self.resolve(ref,write=True,scope=scope)
        return self.wrapped.write(self.ref(ref),data,expected=None if expected_hash=='unchecked' else expected_hash,exclusive=expected_hash is None)

    def unlink(self,ref,scope=None,expected_hash='unchecked'):
        helper=helpers();self.resolve(ref,write=True,scope=scope)
        reference=self.ref(ref)
        with self.wrapped.parent_fd(reference) as (parent,name):
            before=os.stat(name,dir_fd=parent,follow_symlinks=False)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink!=1:
                raise BoundaryError('Delete needs an ordinary unaliased file')
            if expected_hash!='unchecked' and helper.digest(self.wrapped.read(reference))!=expected_hash:
                raise BoundaryError('Delete content changed since review')
            target=self.resolve(ref,write=True,scope=scope)
            actual_parent=target.parent.stat();opened_parent=os.fstat(parent)
            latest=os.stat(name,dir_fd=parent,follow_symlinks=False)
            identity=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
            if identity(before)!=identity(latest) or (actual_parent.st_dev,actual_parent.st_ino)!=(opened_parent.st_dev,opened_parent.st_ino):
                raise BoundaryError('Delete target changed before use')
            os.unlink(name,dir_fd=parent);os.fsync(parent)


class OutputStore:
    def __init__(self,workspace,contract):
        self.workspace=workspace;self.contract=contract;self.depth=0

    def reference(self,path):
        return helpers().output_ref(self.contract,path)

    def read(self,path,default=None):
        try:return json.loads(self.workspace.read(self.reference(path)))
        except FileNotFoundError:return default

    def write(self,path,value,expected_hash='unchecked'):
        data=value if isinstance(value,(str,bytes)) else helpers().json_bytes(value)
        return self.workspace.write(self.reference(path),data,expected=None if expected_hash=='unchecked' else expected_hash,exclusive=expected_hash is None)

    @contextlib.contextmanager
    def lock(self):
        if self.depth:
            self.depth+=1
            try:yield self
            finally:self.depth-=1
            return
        if os.name!='posix':raise helpers().ContractError('Safe standalone edit locking requires Linux/compatible POSIX')
        import fcntl
        lock=self.reference('implementation.lock')
        with self.workspace.parent_fd(lock,create=True) as (parent,name):
            descriptor=os.open(name,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600,dir_fd=parent)
        try:
            info=os.fstat(descriptor)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1:raise helpers().ContractError('Unsafe standalone operation lock')
            try:fcntl.flock(descriptor,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:raise helpers().ContractError('Another standalone edit owns this output journal; no action queued')
            self.depth=1
            try:yield self
            finally:self.depth=0
        finally:os.close(descriptor)


def execute(contract,data,workspace,operation):
    helper=helpers()
    if contract['skill']!='implement-plan' or 'implementation' not in contract['effects'] or contract['authorization']['mode'] not in ('approved-plan','direct-implementation'):
        raise helper.ContractError('Standalone edits require the implementation skill and explicit current implementation authority/effect')
    if not contract.get('plan'):
        raise helper.ContractError('Persist the complete direct/approved plan and identify it before first effect')
    raw=workspace.read(contract['plan']);plan=helper.screen(json.loads(raw));helper.validate_plan(plan,contract)
    tasks=plan['tasks'];task=next((t for t in tasks if t['id']==data.get('task_id')),None)
    if task is None:raise helper.ContractError('Select a task from the persisted plan')
    allowed=task['changes'];scope=[]
    if not allowed:raise helper.ContractError('This helper executes declared product effects; record nonmutation task evidence through its appropriate helper')
    for change in allowed:
        scope.append(change['path'])
        if change['action']=='move':scope.append(change['destination'])
    plan_ref=contract['plan']['root']+':'+contract['plan']['path']
    output_ref=contract['output']['root']+':'+contract['output']['path'].rstrip('/')
    if any(ref==plan_ref or ref==output_ref or ref.startswith(output_ref+'/') for ref in scope):
        raise helper.ContractError('Product tasks must preserve their plan and output journal/evidence')
    store=OutputStore(workspace,contract);adapter=ScopedWorkspace(workspace,contract)
    binding_path='ledger/operations/'+contract['id']+'/plan-binding.json'
    binding={'plan_sha256':helper.digest(raw),'plan_ref':contract['plan'],'workspace_revision':contract['workspace_revision'],'authority':contract['authorization'],'instruction':contract['instruction'],'scope':contract['scope'],'roots':contract['workspace']}
    with store.lock():
        previous=store.read(binding_path)
        if previous and previous!=binding:raise helper.ContractError('Invocation plan/authority/workspace changed; reconcile partial outcomes and use renewed explicit authority')
        if not previous:store.write(binding_path,binding,expected_hash=None)
        # Prior mutation tasks need their actual canonical completed journal.
        # Nonmutation evidence is supplied explicitly and checked as a retained
        # standalone outcome; no AIH lifecycle or stronger identity is invented.
        supplied={item.get('task_id'):item for item in data.get('previous_task_evidence',[])}
        for earlier in tasks[:task['sequence']-1]:
            if earlier['changes']:
                outcome=store.read('ledger/operations/'+contract['id']+'/edits-'+earlier['id']+'-journal.yaml')
            else:
                evidence=supplied.get(earlier['id'],{})
                if not evidence.get('ref') or not evidence.get('sha256'):raise helper.ContractError('Earlier task needs explicit recorded outcome evidence: '+earlier['id'])
                content=workspace.read(evidence['ref'])
                if helper.digest(content)!=evidence['sha256']:raise helper.ContractError('Earlier task evidence changed')
                outcome=json.loads(content)
                if outcome.get('task_id')!=earlier['id']:raise helper.ContractError('Earlier task evidence identity differs')
            process_pass=bool(outcome and outcome.get('operation')=='run-test' and outcome.get('status')=='passed' and outcome.get('returncode')==0 and outcome.get('termination_confirmed') is True)
            if not outcome or outcome.get('status')!='completed' and not process_pass:raise helper.ContractError('Sequential task is incomplete: '+earlier['id'])
        summary_path='ledger/operations/'+contract['id']+'/results-'+task['id']+'.md'
        store.write(summary_path,'# Standalone task '+task['id']+'\n\nIntent recorded under the current persisted plan. Product outcomes remain unverified until their separate checks finish.\n')
        try:
            if operation=='apply-edits':
                edits=data.get('edits')
                if not isinstance(edits,list):raise helper.ContractError('Supply a typed edits array')
                actual={(e.get('path'),e.get('action'),e.get('destination')) for e in edits}
                planned={(e.get('path'),e.get('action'),e.get('destination')) for e in allowed}
                if actual!=planned or len(actual)!=len(edits):raise helper.ContractError('Edits must cover exactly this planned task; omitted, duplicate or unplanned effects are refused')
                for edit in edits:
                    if edit.get('action')=='move' and not any(c.get('path')==edit.get('path') and c.get('action')=='move' and c.get('destination')==edit.get('destination') for c in allowed):raise helper.ContractError('Move destination differs from the approved task')
                result=apply_edits(store,adapter,edits,scope,contract['id'],task['id'],allowed_changes=allowed)
            else:
                result=reconcile(store,adapter,contract['id'],task['id'],scope,apply=data.get('apply') is True)
        except Exception as exc:
            store.write(summary_path,'# Standalone task '+task['id']+' incomplete\n\n'+str(exc)+'\n\nInspect retained per-effect journal before explicit reconciliation. No task success or automatic continuation is inferred.\n')
            raise
        result['journal']=store.reference(result['journal'])
        result.update(task_id=task['id'],plan_sha256=binding['plan_sha256'],authority_assurance='Invoking instruction recorded; no independent host identity assurance.',verification='Product effect observations only; required tests/documentation/acceptance remain separate.')
        store.write(summary_path,'# Standalone task '+task['id']+'\n\n'+helper.json_bytes(result).decode())
        return result
