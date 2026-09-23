"""Actual copied implementation helper; no full AIH lifecycle or model assumed."""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.dont_write_bytecode=True
ENGINE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ENGINE))
from skill_helpers import ContractError,Workspace,digest,json_bytes,validate_contract
from portable_edits import execute,ScopedWorkspace
from product_edits import ProductEditError


class StandaloneEdits(unittest.TestCase):
    def setUp(self):
        base=ENGINE.parent.parent/'.aih-runtime/standalone-edits';base.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=base);self.root=Path(self.temp.name)
        self.left=self.root/'left';self.left.mkdir();self.right=self.root/'right';self.right.mkdir()
        (self.left/'keep.txt').write_text('before');(self.left/'move.txt').write_text('move content');(self.right/'delete.txt').write_text('remove content')
        self.contract={'schema_version':'1.0','id':'STANDALONE-1','skill':'implement-plan','instruction':'Apply only the reviewed task in the isolated fixture.','workspace_revision':1,'workspace':[{'id':name,'name':name,'path':str(path),'purpose':'Fixture','access':'read-write'} for name,path in [('left',self.left),('right',self.right)]],'inputs':[{'root':'left','path':'.'}],'output':{'root':'left','path':'results'},'plan':{'root':'left','path':'plan.json'},'scope':[{'root':'left','path':'.'},{'root':'right','path':'.'}],'effects':['scoped-output-records','implementation'],'authorization':{'mode':'direct-implementation','instruction_reference':'explicit fixture instruction'},'constraints':['registered filesystem effects only']}
        self.edits=[{'path':'left:keep.txt','action':'modify','expected_hash':digest(b'before'),'content':'after'},{'path':'left:create.txt','action':'create','expected_hash':None,'content':'created'},{'path':'left:move.txt','action':'move','destination':'right:moved.txt','expected_hash':digest(b'move content')},{'path':'right:delete.txt','action':'delete','expected_hash':digest(b'remove content')}]
        changes=[{k:v for k,v in edit.items() if k in ('path','action','destination')} for edit in self.edits]
        self.plan={'id':'P1','revision':1,'bindings':{'interpretation_revision':1,'workspace_revision':1},'tasks':[{'id':'T'+str(i),'sequence':i,'kind':kind,'outcome':'Fixture '+kind,'requirements':['AC1'],'changes':changes if i==1 else [],'dependencies':[] if i==1 else ['T'+str(i-1)],'completion_criteria':['Evidence retained']} for i,kind in enumerate(['implement','tests','verify','documentation','evidence'],1)]}
        (self.left/'plan.json').write_bytes(json_bytes(self.plan));self.data={'task_id':'T1','edits':self.edits}
    def tearDown(self):self.temp.cleanup()
    def test_copied_helper_creates_modifies_moves_deletes_and_preserves_history(self):
        package=self.root/'implement-plan';shutil.copytree(ENGINE.parent/'skills/implement-plan',package)
        contract_path=self.root/'invocation.json';contract_path.write_text(json.dumps(self.contract))
        (self.left/'effects.json').write_text(json.dumps(self.data))
        command=[sys.executable,'-B',str(package/'scripts/helper.py'),'apply-edits','--contract',str(contract_path),'--data',json.dumps({'root':'left','path':'effects.json'}),'--artifact','task-result.json']
        for _ in range(2):
            result=subprocess.run(command,cwd=self.root,env=dict(os.environ,PYTHONPATH='',PYTHONDONTWRITEBYTECODE='1'),text=True,capture_output=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertEqual((self.left/'keep.txt').read_text(),'after');self.assertEqual((self.left/'create.txt').read_text(),'created');self.assertFalse((self.left/'move.txt').exists());self.assertEqual((self.right/'moved.txt').read_text(),'move content');self.assertFalse((self.right/'delete.txt').exists())
        evidence=json.loads((self.left/'results/task-result.json').read_text());self.assertFalse(evidence['atomic_cross_root']);self.assertEqual(len(evidence['changed']),4)
        self.assertTrue((self.left/'results/ledger/operations/STANDALONE-1/results-T1.md').exists());self.assertFalse(list(self.root.rglob('.aih_product')))
        (self.left/'keep.txt').write_text('later human edit')
        retry=subprocess.run(command,cwd=self.root,text=True,capture_output=True);self.assertNotEqual(retry.returncode,0);self.assertEqual((self.left/'keep.txt').read_text(),'later human edit')
    def test_omission_wrong_kind_and_out_of_plan_destination_do_not_change_product(self):
        for edits in (self.edits[:-1],[dict(e,action='delete') if e['path']=='left:keep.txt' else e for e in self.edits],[dict(e,destination='right:unplanned.txt') if e['action']=='move' else e for e in self.edits]):
            with self.assertRaises(ContractError):execute(self.contract,{'task_id':'T1','edits':edits},validate_contract(self.contract),'apply-edits')
        self.assertEqual((self.left/'keep.txt').read_text(),'before');self.assertTrue((self.left/'move.txt').exists());self.assertTrue((self.right/'delete.txt').exists())
    def test_interrupted_move_requires_current_authority_and_recognizes_written_copy(self):
        original=ScopedWorkspace.unlink
        def interrupted(adapter,ref,*args,**kwargs):
            if ref=='left:move.txt':raise OSError('Simulated interruption after destination copy')
            return original(adapter,ref,*args,**kwargs)
        with patch('portable_edits.ScopedWorkspace.unlink',new=interrupted):
            with self.assertRaises(OSError):execute(self.contract,self.data,validate_contract(self.contract),'apply-edits')
        self.assertTrue((self.left/'move.txt').exists());self.assertTrue((self.right/'moved.txt').exists())
        restricted=copy.deepcopy(self.contract);restricted['workspace'][1]['access']='read-only'
        with self.assertRaises((ContractError,ProductEditError)):execute(restricted,{'task_id':'T1','apply':True},validate_contract(restricted),'reconcile')
        self.assertTrue((self.left/'move.txt').exists());self.assertTrue((self.right/'delete.txt').exists())
        recovered=execute(self.contract,{'task_id':'T1','apply':True},validate_contract(self.contract),'reconcile')
        self.assertEqual(recovered['status'],'completed');self.assertFalse((self.left/'move.txt').exists());self.assertFalse((self.right/'delete.txt').exists())
    def test_later_task_and_changed_plan_cannot_bypass_retained_binding(self):
        self.plan['tasks'][1]['changes']=[{'path':'left:second.txt','action':'create'}]
        (self.left/'plan.json').write_bytes(json_bytes(self.plan))
        with self.assertRaises(ContractError):execute(self.contract,{'task_id':'T2','edits':[{'path':'left:second.txt','action':'create','expected_hash':None,'content':'later'}]},validate_contract(self.contract),'apply-edits')
        self.assertFalse((self.left/'second.txt').exists())
        self.plan['tasks'][0]['outcome']='A changed plan needs fresh explicit authority'
        (self.left/'plan.json').write_bytes(json_bytes(self.plan))
        with self.assertRaises(ContractError):execute(self.contract,self.data,validate_contract(self.contract),'apply-edits')
        self.assertEqual((self.left/'keep.txt').read_text(),'before')
    @unittest.skipUnless(sys.platform=='linux','Linux confinement backend')
    def test_shipped_example_runs_actual_regression_and_empty_suite_blocks(self):
        from execution import confinement_diagnostics
        if not confinement_diagnostics()['available']:self.skipTest('Landlock/seccomp unavailable')
        package=self.root/'example-package'/'implement-plan';shutil.copytree(ENGINE.parent/'skills/implement-plan',package)
        product=self.root/'example-product';product.mkdir()
        for source,target in [('example-plan.json','approved-plan.json'),('example-edits.json','edits.json'),('example-test-edits.json','test-edits.json'),('example-test-contract.json','test-contract.json')]:shutil.copyfile(package/'resources'/source,product/target)
        contract=json.loads((package/'resources/example-contract.json').read_text());contract['workspace'][0]['path']=str(product)
        contract_file=self.root/'example-invocation.json';contract_file.write_text(json.dumps(contract))
        for operation,data,artifact in [('apply-edits','edits.json','T1.json'),('apply-edits','test-edits.json','T2.json'),('run-test','test-contract.json','T3.json')]:
            result=subprocess.run([sys.executable,'-B',str(package/'scripts/helper.py'),operation,'--contract',str(contract_file),'--data',json.dumps({'root':'product','path':data}),'--artifact',artifact],cwd=self.root,text=True,capture_output=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        tested=json.loads((product/'results/implement-plan/T3.json').read_text());self.assertEqual(tested['status'],'passed');self.assertEqual(tested['tests_collected'],1)
        (product/'empty-tests').mkdir();suite=json.loads((product/'test-contract.json').read_text());suite['source_paths']=[{'root':'product','path':'empty-tests'}];(product/'test-contract.json').write_text(json.dumps(suite))
        contract['runtime']={'root':'product','path':'.aih-runtime/empty-suite'};contract['scope'].append(contract['runtime']);contract_file.write_text(json.dumps(contract))
        result=subprocess.run([sys.executable,'-B',str(package/'scripts/helper.py'),'run-test','--contract',str(contract_file),'--data',json.dumps({'root':'product','path':'test-contract.json'}),'--artifact','empty-result.json'],cwd=self.root,text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        empty=json.loads((product/'results/implement-plan/empty-result.json').read_text());self.assertEqual(empty['status'],'blocked');self.assertEqual(empty['tests_collected'],0)

if __name__=='__main__':unittest.main()
