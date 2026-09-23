"""Independent regression audit of approval/closure freshness after a completed run."""
import copy
import base64
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.dont_write_bytecode=True
sys.path[:0]=[str(Path(__file__).resolve().parents[1]),str(Path(__file__).resolve().parent)]
import test_workflow
from contracts import Error

class ClosureFreshnessReview(unittest.TestCase):
    def setUp(self):
        self.fixture=test_workflow.WorkflowTests('test_complete_lifecycle_requires_explicit_successful_close')
        self.fixture.setUpClass();self.fixture.setUp()
    def tearDown(self):self.fixture.tearDown()
    def ready(self):
        self.fixture.analyzed();self.fixture.set_response(self.fixture.implementation_response())
        self.assertEqual(self.fixture.call('implement')['status'],'completed')
        self.assertEqual(self.fixture.engine.status()['active_request']['status'],'ready-to-close')
    def test_instruction_change_cannot_close_using_old_passes(self):
        self.ready();self.fixture.call('instructions-save',{'text':'Human correction: review the existing greeting against this changed instruction before closure.'})
        with self.assertRaises(Error):self.fixture.call('close',{'outcome':'completed'})
        self.assertIsNotNone(self.fixture.engine.status()['active_request'])
    def test_changed_suite_contract_requires_new_verification(self):
        self.ready();engine=self.fixture.engine
        suites=engine.store.read('documentation/test_inventory.yaml')['suites']
        changed=copy.deepcopy(suites[0]);changed.update(runner='python-script',source_paths=['home:tests/test_app.py'])
        self.fixture.call('register-test',{'contract':changed})
        with self.assertRaises(Error):self.fixture.call('close',{'outcome':'completed'})
    def test_plan_edit_cannot_reuse_prior_human_approval(self):
        self.fixture.analyzed();engine=self.fixture.engine
        plan=engine.store.read(engine.reqpath('analysis/plan.yaml'));plan['tasks'][0]['outcome']='A materially different effect without refreshed human approval'
        engine.store.write(engine.reqpath('analysis/plan.yaml'),plan)
        self.fixture.set_response(self.fixture.implementation_response())
        with self.assertRaises(Error):self.fixture.call('implement')
        self.assertIn('Hi',(self.fixture.home/'app.py').read_text())
    def test_documentation_edit_invalidates_reconciled_increment(self):
        self.ready();engine=self.fixture.engine
        leaf=next(n for n in engine.store.read('documentation/tree.yaml')['nodes'] if n['kind']=='content')
        engine.store.write('documentation/'+leaf['path'],'# Human correction\n\nThis current product description has changed and must be reconciled before previous evidence can establish successful closure.')
        with self.assertRaises(Error):self.fixture.call('close',{'outcome':'completed'})

    def test_omitted_acceptance_criterion_blocks_completion(self):
        self.fixture.analyzed()
        response=self.fixture.implementation_response()
        response['fixture_responses']['T5']['acceptance'][0]['criterion']='different-criterion'
        self.fixture.set_response(response)
        self.assertEqual(self.fixture.call('implement')['status'],'blocked')
        self.assertIn('every canonical acceptance criterion',self.fixture.engine.status()['current_response'])
        with self.assertRaises(Error):self.fixture.call('close',{'outcome':'completed'})

    def test_edited_acceptance_record_cannot_reuse_previous_verification(self):
        self.ready();engine=self.fixture.engine
        path=engine.request['acceptance_evidence'];evidence=engine.store.read(path)
        evidence['acceptance']=[];engine.store.write(path,evidence)
        with self.assertRaises(Error):self.fixture.call('close',{'outcome':'completed'})

    def test_historical_redaction_removes_transaction_recovery_copies(self):
        engine=self.fixture.engine
        # Simulate an opaque sensitive value discovered after a historical
        # admission. Detection is best effort; the correction must remove
        # derived encoded recovery copies as well as the visible record.
        secret='opaque historical sensitive value 73910'
        selected='communications/history/legacy.md'
        original_write=engine.store.write
        def interrupt(path,value,**kwargs):
            if path=='communications/history/second.md':raise OSError('Simulated interruption after first historical record write')
            return original_write(path,value,**kwargs)
        with patch.object(engine.store,'write',side_effect=interrupt):
            with self.assertRaises(OSError):engine.store.transaction({selected:'Retained user evidence: '+secret,'communications/history/second.md':'Derived evidence: '+secret})
        self.fixture.call('redact',{'paths':[selected],'value':secret,'reason':'Explicitly remove the discovered credential from framework-owned history.'})
        self.assertNotIn(secret,engine.store.read_text(selected))
        for path in (self.fixture.home/'.aih_product/ledger/transactions').glob('*.json'):
            journal=json.loads(path.read_text())
            for step in journal.get('steps',[]):
                if step.get('data_base64'):
                    self.assertNotIn(secret,base64.b64decode(step['data_base64']).decode('utf-8'))
        engine.store.recover(apply=True)
        for path in (self.fixture.home/'.aih_product').rglob('*'):
            if path.is_file():self.assertNotIn(secret.encode(),path.read_bytes())

    def test_redacted_product_proposal_does_not_authorize_replay(self):
        from product_edits import apply_edits,reconcile,ProductEditError
        engine=self.fixture.engine
        secret='opaque discovered product credential 85206'
        effects=apply_edits(engine.store,engine.workspace,[{'path':'home:legacy.txt','action':'create','expected_hash':None,'content':secret}],['home:legacy.txt'],'old-operation','old-task')
        self.fixture.call('redact',{'paths':[effects['journal']],'value':secret,'reason':'Remove retained sensitive proposal content; source correction needs separate scope.'})
        self.assertNotIn(secret,engine.store.read_text(effects['journal']))
        self.assertEqual(secret,(self.fixture.home/'legacy.txt').read_text())
        with self.assertRaises(ProductEditError):reconcile(engine.store,engine.workspace,'old-operation','old-task',['home:legacy.txt'],apply=True)
        with self.assertRaises(Error):self.fixture.call('redact',{'paths':[effects['journal']],'value':secret,'reason':'Do not persist '+secret})
        for path in (self.fixture.home/'.aih_product').rglob('*'):
            if path.is_file():self.assertNotIn(secret.encode(),path.read_bytes())

if __name__=='__main__':unittest.main()
