"""Independent structural, provenance, coverage and incremental documentation checks."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.dont_write_bytecode=True
ENGINE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ENGINE))
from contracts import Error,digest
from documentation import apply_proposal,balanced_tree,coverage_categories,extract,validate_tree
from security import Workspace
from storage import Store

class Documentation(unittest.TestCase):
    def setUp(self):
        parent=ENGINE.parent.parent/'.aih-runtime'/'documentation-tests';parent.mkdir(parents=True,exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=parent);self.home=Path(self.tmp.name)
        (self.home/'source').mkdir();(self.home/'source/app.py').write_text('"""A greeting fixture."""\ndef greet(name):\n    return "Hello " + name\n')
        self.workspace=Workspace(self.home);self.store=Store(self.home)
        self.inventory=self.workspace.inventory()
    def tearDown(self):self.tmp.cleanup()
    def proposal(self):
        return {'topics':[{'id':'greeting','title':'Greeting behavior','summary':'The observed greeting fixture','content':'# Greeting behavior\n\nThe source defines a greeting function accepting a name and returning a Hello prefix with that name. This is a static observation, not a verified runtime acceptance result.','sources':['home:source/app.py'],'when_to_read':'When changing greeting behavior'}], 'coverage':[{'id':x['id'],'title':x['title'],'status':'applicable' if x['id'] in ('purpose','interfaces','workspace') else 'not-applicable','rationale':'Small isolated greeting fixture has no independently configured subsystem in this category.' if x['id'] not in ('purpose','interfaces','workspace') else 'The source function and its caller-facing purpose are described in the linked topic.','topics':['greeting'] if x['id'] in ('purpose','interfaces','workspace') else []} for x in coverage_categories()], 'source_dispositions':[], 'reconstruction_review':{k:'Reviewed against home:source/app.py; static behavior specified, independent reconstruction and runtime acceptance not demonstrated.' for k in ['business_rules','interfaces','expected_results','dependencies','acceptance_tests','recovery']}}
    def test_strict_balance_grows_without_padding_or_lost_identity(self):
        for count in (1,8,9,64,65,512,513):
            with self.subTest(leaves=count):
                leaves=[{'id':'topic-'+str(n),'path':'topics/'+str(n)+'.md','title':'Topic '+str(n),'summary':'Specific topic','status':'current','when_to_read':'When relevant'} for n in range(count)]
                tree=balanced_tree(leaves)
                result=validate_tree(tree,lambda _: 'A substantive product topic with evidence links and current knowledge preserved for the reader.')
                self.assertEqual(result['leaves'],count);self.assertLessEqual(result['max_depth']-result['min_depth'],1)
                self.assertEqual({x['id'] for x in leaves},{x['id'] for x in tree['nodes'] if x['kind']=='content'})
                self.assertTrue(all(1<=len(x['children'])<=8 for x in tree['nodes'] if x['kind']=='catalog'))
    def test_cycles_duplicate_ids_missing_and_crosslinks_refused(self):
        tree=balanced_tree([{'id':'a','path':'a.md','title':'A'}])
        mutations=[lambda t:t['nodes'].append(dict(t['nodes'][1])),lambda t:t['nodes'][0]['children'].append('missing'),lambda t:t['nodes'][0]['children'].append('root')]
        for mutate in mutations:
            broken=copy.deepcopy(tree);mutate(broken)
            with self.assertRaises(Error):validate_tree(broken)
        with self.assertRaises(Error):validate_tree(tree,lambda _:'See [nonexistent](aih-doc:absent) topic for the authoritative product contract.')
    def test_substantive_coverage_and_reconstruction_required(self):
        for change in ('missing-category','uncovered-source','missing-review','empty-topic'):
            result=self.proposal()
            if change=='missing-category':result['coverage'].pop()
            if change=='uncovered-source':result['topics'][0]['sources']=[]
            if change=='missing-review':result['reconstruction_review'].pop('recovery')
            if change=='empty-topic':result['topics'][0]['content']='Short heading'
            with self.subTest(case=change),self.assertRaises(Error):apply_proposal(self.store,self.workspace,result,self.inventory,'OP-1')
        self.assertIsNone(self.store.read('documentation/baseline.yaml'))
    def test_baseline_complete_does_not_claim_runtime_verification(self):
        result=apply_proposal(self.store,self.workspace,self.proposal(),self.inventory,'OP-1')
        self.assertEqual(result['status'],'complete');self.assertEqual(result['reconstruction'],'specified but not demonstrated')
        self.assertIn('not established',result['product_tests'])
        self.assertEqual(self.store.read('documentation/tree.yaml')['revision'],1)
        journals=list((self.home/'.aih_product/ledger/transactions').glob('*.json'));self.assertTrue(journals)
        self.assertTrue(all(json.loads(p.read_text())['status']=='committed' for p in journals))
    def test_human_edit_conflict_preserved(self):
        apply_proposal(self.store,self.workspace,self.proposal(),self.inventory,'OP-1')
        ref='documentation/topics/greeting.md';original=self.store.read(ref,raw=True)
        self.store.write(ref,original+'\nHuman clarification remains authoritative.\n')
        with self.assertRaises(Error):apply_proposal(self.store,self.workspace,self.proposal(),self.inventory,'OP-2')
        self.assertIn('Human clarification',self.store.read(ref,raw=True))
    def test_changed_source_requires_incremental_topic_reconciliation(self):
        apply_proposal(self.store,self.workspace,self.proposal(),self.inventory,'OP-1')
        (self.home/'source/app.py').write_text('def greet(name):\n    return "Welcome " + name\n')
        result=self.proposal();result['topics']=[{'id':'new-topic','title':'New topic','content':'This replacement topic contains enough substantive words but it intentionally does not reconcile the previously documented changed greeting behavior.','sources':['home:source/app.py']}]
        with self.assertRaises(Error):apply_proposal(self.store,self.workspace,result,self.workspace.inventory(),'OP-2')
    def test_extraction_reuses_unchanged_sources_and_invalidates_changed_source(self):
        before=extract(self.workspace,self.inventory)
        again=extract(self.workspace,self.inventory,before);self.assertEqual(again['reused'],1)
        (self.home/'source/app.py').write_text('def greet(name):\n    return "Welcome " + name\n')
        refreshed=extract(self.workspace,self.workspace.inventory(),before);self.assertEqual(refreshed['reused'],0)
    def test_extraction_invalidates_instruction_and_workspace_changes(self):
        before=extract(self.workspace,self.inventory)
        self.store.write('instructions/product.md','Human instruction: greetings must preserve the supplied name.')
        updated=extract(self.workspace,self.inventory,before)
        self.assertEqual(updated['reused'],0)
        registry=copy.deepcopy(self.workspace.registry);registry['revision']=2
        changed=extract(Workspace(self.home,registry),self.inventory,updated)
        self.assertEqual(changed['reused'],0)
    def test_duplicate_coverage_category_refused(self):
        result=self.proposal();result['coverage'].append(dict(result['coverage'][0]))
        with self.assertRaises(Error):apply_proposal(self.store,self.workspace,result,self.inventory,'OP-1')

if __name__=='__main__':unittest.main()
