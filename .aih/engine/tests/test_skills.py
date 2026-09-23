"""Behavioral helper and isolated copied-package tests; no semantic-agent claim."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ENGINE=Path(__file__).resolve().parents[1]
CORE=ENGINE.parent
HOME=CORE.parent
sys.path.insert(0,str(ENGINE))
from skill_helpers import ContractError, Workspace, amendment_revision, check_bundle, digest, inventory, json_bytes, validate_contract, validate_plan, validate_tree
from build_skills import build, discover, metadata
from exchange import answered, export_form, receive, review
from contracts import Error

SKILLS={'clarify-requirements','analyze-and-plan','implement-plan','test-and-verify','reverse-engineer-product','maintain-documentation','answer-product-questions','git-workflow'}

class PortableSkills(unittest.TestCase):
    def setUp(self):
        base=HOME/'.aih-runtime'/'skill-tests'
        base.mkdir(parents=True,exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=base)
        self.root=Path(self.tmp.name)
        self.product=self.root/'product';self.product.mkdir()
        (self.product/'src').mkdir();(self.product/'src'/'app.py').write_text('def greet(name):\n    return "Hello " + name\n')
        self.contract={'schema_version':'1.0','id':'TEST','skill':'reverse-engineer-product','instruction':'Inventory this explicit fixture without executing its source.','workspace_revision':1,'workspace':[{'id':'product','name':'Fixture','path':str(self.product),'purpose':'Test','access':'read-write'}],'inputs':[{'root':'product','path':'src'}],'output':{'root':'product','path':'results'},'scope':[{'root':'product','path':'results'}],'effects':['scoped-output-records'],'authorization':{'mode':'setup','instruction_reference':'test instruction'},'constraints':['no subprocess product execution']}
    def tearDown(self):self.tmp.cleanup()
    def test_catalog_maintenance_gates_installed_state_and_owner(self):
        from storage import Store
        from installation import build_manifest
        installed=self.root/'installed'/'.aih';shutil.copytree(CORE,installed)
        store=Store(installed.parent)
        state={'schema_version':'1.0','revision':1,'workspace_revision':1,'setup':{},'active_request':'CR-BLOCKED','owner':None}
        store.write('state.yaml',state)
        before=(installed/'skills/catalog.yaml').read_bytes()
        with self.assertRaises(Error):build(installed)
        with self.assertRaises(Error):build_manifest(installed)
        result=subprocess.run([sys.executable,'-B',str(installed/'engine/build_skills.py'),'--core',str(installed),'--build'],text=True,capture_output=True)
        self.assertNotEqual(result.returncode,0)
        state['active_request']=None;state['owner']={'id':'external','status':'reserved'};store.write('state.yaml',state)
        with self.assertRaises(Error):build(installed)
        store.write('state.yaml',{'schema_version':'1.0'})
        with self.assertRaises(Error):build(installed)
        self.assertEqual(before,(installed/'skills/catalog.yaml').read_bytes())
        state['owner']=None;store.write('state.yaml',state)
        result=build(installed);self.assertEqual(len(result['skills']),8)
        self.assertEqual(before,(installed/'skills/catalog.yaml').read_bytes())
    def test_all_packages_copy_and_execute_without_installed_engine(self):
        discovered=discover(CORE)
        self.assertFalse(discovered['diagnostics'])
        self.assertEqual(SKILLS,{s['id'] for s in discovered['skills']})
        for skill in discovered['skills']:
            with self.subTest(skill=skill['id']):
                self.assertEqual(skill['enabled'],skill['id']!='git-workflow')
                self.assertTrue(skill['available'],skill['diagnostics'])
                self.assertNotIn('SKILL.md',json.dumps(skill))
                self.assertNotIn('body',skill)
                package=self.root/skill['id'];shutil.copytree(CORE/skill['package'],package)
                contract=json.loads(json.dumps(self.contract));contract['skill']=skill['id']
                if skill['id']=='answer-product-questions':contract['authorization']['mode']='read-only'
                if skill['id']=='git-workflow':contract['authorization']['mode']='git'
                if skill['id']=='implement-plan':contract['authorization']['mode']='direct-implementation'
                contract_file=self.root/(skill['id']+'.json');contract_file.write_text(json.dumps(contract))
                env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH='')
                for args in (['integrity'],['validate','--contract',str(contract_file)],['inventory','--contract',str(contract_file),'--artifact',skill['id']+'.json']):
                    run=subprocess.run([sys.executable,'-B',str(package/'scripts/helper.py'),*args],cwd=self.root,env=env,text=True,capture_output=True)
                    self.assertEqual(run.returncode,0,run.stdout+run.stderr)
                result=json.loads((self.product/'results'/f"{skill['id']}.json").read_text())
                self.assertEqual(result['entries'][0]['extraction']['definitions'][0]['name'],'greet')
                self.assertFalse(list(package.rglob('__pycache__')))
                (package/'resources/coverage.json').write_text('{}')
                altered=subprocess.run([sys.executable,'-B',str(package/'scripts/helper.py'),'integrity'],cwd=self.root,text=True,capture_output=True)
                self.assertNotEqual(altered.returncode,0)
    def test_discovery_reports_new_disabled_malformed_duplicate_and_incompatible(self):
        core=self.root/'catalog'/'.aih';shutil.copytree(CORE,core)
        before=(core/'skills/catalog.yaml').read_bytes()
        disabled=discover(core,{'skills':{'clarify-requirements':{'enabled':False}}})
        self.assertFalse(next(s for s in disabled['skills'] if s['id']=='clarify-requirements')['enabled'])
        new=core/'skills/new-review';shutil.copytree(core/'skills/analyze-and-plan',new)
        text=(new/'SKILL.md').read_text();front=json.loads(text.split('---',2)[1]);front['name']='new-review';extension=json.loads(front['metadata']['aih']);extension['id']='new-review';front['metadata']['aih']=json.dumps(extension)
        (new/'SKILL.md').write_text('---\n'+json.dumps(front)+'\n---\n'+text.split('---',2)[2])
        discovered=discover(core);entry=next(s for s in discovered['skills'] if s['id']=='new-review')
        self.assertFalse(entry['available']);self.assertIn('stale-catalog',' '.join(entry['diagnostics']))
        self.assertFalse(entry['authorized']);self.assertEqual(before,(core/'skills/catalog.yaml').read_bytes())
        bad=core/'skills/bad';bad.mkdir();(bad/'SKILL.md').write_text('---\n{not JSON or supported YAML}\n---\n')
        duplicate=core/'skills/duplicate';shutil.copytree(core/'skills/analyze-and-plan',duplicate)
        result=discover(core);self.assertTrue({'bad','duplicate'}<={d['package'] for d in result['diagnostics']})
        shutil.rmtree(bad);shutil.rmtree(duplicate)
        extension['bundle_version']='99.0.0';front['metadata']['aih']=json.dumps(extension)
        (new/'SKILL.md').write_text('---\n'+json.dumps(front)+'\n---\nIndependent future package\n')
        build(core)
        incompatible=next(s for s in discover(core)['skills'] if s['id']=='new-review')
        self.assertFalse(incompatible['compatible']);self.assertFalse(incompatible['available']);self.assertIn('Incompatible',' '.join(incompatible['diagnostics']))

    def test_bundle_resource_paths_cannot_escape_or_alias(self):
        package=self.root/'safe-package';shutil.copytree(CORE/'skills/clarify-requirements',package)
        manifest_path=package/'resources/manifest.json';manifest=json.loads(manifest_path.read_text())
        manifest['files']['../outside.json']=digest(b'outside')
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaises(ContractError):check_bundle(package)
        manifest['files'].pop('../outside.json');manifest_path.write_text(json.dumps(manifest))
        if os.name=='posix':
            outside=self.root/'outside.json';outside.write_bytes((package/'resources/coverage.json').read_bytes())
            (package/'resources/coverage.json').unlink();(package/'resources/coverage.json').symlink_to(outside)
            with self.assertRaises(ContractError):check_bundle(package)
    @unittest.skipUnless(sys.platform=='linux','Linux confinement backend')
    def test_copied_packages_execute_confined_tests_and_local_git(self):
        from execution import confinement_diagnostics
        if not confinement_diagnostics()['available']:
            self.skipTest('Landlock/seccomp unavailable')
        # This intentionally attempts forbidden writes and verifies the kernel
        # denies them; a passing process alone is not called semantic acceptance.
        outside=self.root/'outside.txt';outside.write_text('unchanged')
        script=self.product/'src'/'check.py'
        script.write_text('from pathlib import Path\np=Path('+repr(str(outside))+')\ntry:\n p.write_text("bad")\nexcept PermissionError:\n pass\nelse:\n raise AssertionError("outside write succeeded")\nprint("contained")\n')
        for skill,operation in [('test-and-verify','run-test'),('git-workflow','git')]:
            package=self.root/'execute'/skill;shutil.copytree(CORE/'skills'/skill,package)
            contract=json.loads(json.dumps(self.contract));contract['skill']=skill;contract['authorization']['mode']='approved-plan' if operation=='run-test' else 'git'
            contract['runtime']={'root':'product','path':'runtime-'+skill};contract['scope'].append(contract['runtime'])
            contract['effects'].append('test-execution' if operation=='run-test' else 'git-status')
            if operation=='run-test':
                data={'id':'safe-test','runner':'python-script','environment':'python3','working_directory':{'root':'product','path':'src'},'source_paths':[{'root':'product','path':'src/check.py'}],'write_paths':[],'prerequisites':[],'isolation':'linux-landlock-seccomp','cleanup':'retain','authorization':'test instruction','workspace_revision':1}
            else:
                if not shutil.which('git'):continue
                env=dict(os.environ,HOME=str(self.root),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
                repo=self.product/'repo';repo.mkdir();subprocess.run(['git','init','--quiet',str(repo)],env=env,check=True)
                (repo/'note.txt').write_text('fixture file')
                data={'repository':{'root':'product','path':'repo'},'action':'status'}
            data_file=self.product/'execution-input.json';data_file.write_text(json.dumps(data));contract_file=self.root/'execution-contract.json';contract_file.write_text(json.dumps(contract))
            run=subprocess.run([sys.executable,'-B',str(package/'scripts/helper.py'),operation,'--contract',str(contract_file),'--data',json.dumps({'root':'product','path':'execution-input.json'}),'--artifact',skill+'-run.json'],cwd=self.root,text=True,capture_output=True)
            self.assertEqual(run.returncode,0,run.stdout+run.stderr)
            result=json.loads((self.product/'results'/(skill+'-run.json')).read_text());self.assertEqual(result['status'],'passed',result)
            self.assertTrue(result['termination_confirmed']);self.assertEqual(outside.read_text(),'unchanged')
            if operation=='git':
                contract['scope'].append({'root':'product','path':'repo/.git'})
                (repo/'unrelated.txt').write_text('retain staged work')
                subprocess.run(['git','-C',str(repo),'add','--','unrelated.txt'],env=env,check=True)
                for action in ('commit','branch'):
                    contract['runtime']={'root':'product','path':'runtime-git-'+action};contract['scope'].append(contract['runtime']);contract['effects'].append('git-'+action)
                    action_data={'repository':{'root':'product','path':'repo'},'action':action,'branch':'reviewed-feature'}
                    if action=='commit':action_data.update(message='Record the explicitly selected fixture',paths=[{'root':'product','path':'repo/note.txt'}],author_name='AIH fixture',author_email='fixture@example.invalid')
                    data_file.write_text(json.dumps(action_data));contract_file.write_text(json.dumps(contract))
                    change=subprocess.run([sys.executable,'-B',str(package/'scripts/helper.py'),'git','--contract',str(contract_file),'--data',json.dumps({'root':'product','path':'execution-input.json'}),'--artifact',action+'.json'],cwd=self.root,text=True,capture_output=True)
                    self.assertEqual(change.returncode,0,change.stdout+change.stderr)
                    evidence=json.loads((self.product/'results'/(action+'.json')).read_text());self.assertEqual(evidence['status'],'passed',evidence)
                self.assertTrue((repo/'.git/refs/heads/reviewed-feature').is_file())
                retained=subprocess.run(['git','-C',str(repo),'status','--porcelain=v1'],env=env,text=True,capture_output=True,check=True)
                self.assertIn('A  unrelated.txt',retained.stdout)

    def test_root_union_and_write_scope(self):
        readonly=self.root/'reference';readonly.mkdir();(readonly/'notes.txt').write_text('reference')
        self.contract['workspace'].append({'id':'reference','name':'Reference','path':str(readonly),'purpose':'Read only','access':'read-only'})
        ws=validate_contract(self.contract)
        with self.assertRaises(ContractError):ws.write({'root':'reference','path':'notes.txt'},'changed')
        with self.assertRaises(ContractError):ws.write({'root':'product','path':'src/app.py'},'changed')
        with self.assertRaises(ContractError):ws.resolve({'root':'product','path':'../outside.txt'})
        with self.assertRaises(ContractError):ws.resolve({'root':'product','path':'/tmp/outside.txt'})
        with self.assertRaises(ContractError):ws.resolve({'root':'unknown','path':'a'})
        ws.write({'root':'product','path':'results/check.json'},'{}')
        self.assertEqual((readonly/'notes.txt').read_text(),'reference')
    @unittest.skipUnless(os.name=='posix','POSIX links')
    def test_symlink_and_hardlink_refused(self):
        outside=self.root/'outside.txt';outside.write_text('untouched')
        (self.product/'results').symlink_to(self.root,target_is_directory=True)
        with self.assertRaises(ContractError):validate_contract(self.contract)
        (self.product/'results').unlink();(self.product/'results').mkdir()
        os.link(outside,self.product/'results/alias.txt')
        ws=validate_contract(self.contract)
        with self.assertRaises(ContractError):ws.write({'root':'product','path':'results/alias.txt'},'changed')
        self.assertEqual(outside.read_text(),'untouched')
    def test_overlapping_registry_refused(self):
        self.contract['workspace'].append({'id':'nested','name':'Nested','path':str(self.product/'src'),'purpose':'Bad','access':'read-only'})
        with self.assertRaises(ContractError):validate_contract(self.contract)
    def test_revision_conflict_and_sensitive_refusal_preserve_existing(self):
        ws=validate_contract(self.contract);ref={'root':'product','path':'results/answer.txt'}
        first=ws.write(ref,'old')
        with self.assertRaises(ContractError):ws.write(ref,'new',expected='wrong')
        self.assertEqual(ws.read(ref),b'old')
        with self.assertRaises(ContractError):ws.write(ref,'password = abcdefghijklmnop')
        self.assertEqual(ws.read(ref),b'old')
        ws.write(ref,'new',expected=first['sha256']);self.assertEqual(ws.read(ref),b'new')
        real_fsync=os.fsync
        raced=[False]
        def competing_write(fd):
            real_fsync(fd)
            if not raced[0]:
                raced[0]=True;(self.product/'results/answer.txt').write_text('human correction')
        with patch('skill_helpers.os.fsync',side_effect=competing_write):
            with self.assertRaises(ContractError):ws.write(ref,'overwrite',expected=digest(b'new'))
        self.assertEqual(ws.read(ref),b'human correction')
    def test_missing_or_contradictory_authority_fails_before_writes(self):
        self.contract['skill']='implement-plan'
        with self.assertRaises(ContractError):validate_contract(self.contract)
        self.assertFalse((self.product/'results').exists())
        self.contract['skill']='answer-product-questions';self.contract['authorization']['mode']='read-only';self.contract['effects'].append('implementation')
        with self.assertRaises(ContractError):validate_contract(self.contract)
    def test_inventory_is_static_and_provenance_bound(self):
        (self.product/'src'/'danger.py').write_text('raise RuntimeError("must not run")\n')
        result=inventory(self.contract)
        self.assertEqual(len(result['entries']),2)
        self.assertEqual(result['verification'],'not run')
        self.assertEqual(result['entries'][0]['workspace_revision'],1)
        self.assertEqual(inventory(self.contract)['manifest_hash'],result['manifest_hash'])
    def test_inventory_excludes_declared_outputs_and_runtime_without_self_drift(self):
        self.contract['inputs']=[{'root':'product','path':'.'}]
        self.contract['runtime']={'root':'product','path':'custom-execution'}
        before=inventory(self.contract)
        (self.product/'results').mkdir();(self.product/'results/evidence.json').write_text('{"generated":true}')
        (self.product/'custom-execution').mkdir();(self.product/'custom-execution/cache.txt').write_text('generated runtime')
        (self.product/'.aih_runtime').mkdir();(self.product/'.aih_runtime/events.json').write_text('{"generated":true}')
        after=inventory(self.contract)
        self.assertEqual(before['manifest_hash'],after['manifest_hash']);self.assertEqual(before['entries'],after['entries'])
    def test_questionnaire_review_does_not_imply_approval(self):
        qs=[{'id':'Q-AUDIENCE','revision':1,'respondent':'Requestor','kind':'text','blocker':True,'category':'requirement','question':'Who needs to read the report?','explanation':'Tell us which people use the report and why.','why':'This defines the audience for acceptance.','instructions':'Name the groups or write I do not know.','example':'A purchasing team could read monthly totals.','options':[],'selected':[],'answer':'','comments':''}]
        form=export_form({'id':'CR-1','title':'Report'},qs,1)
        self.assertIn('Why we ask:',form['text']);self.assertIn('illustration only',form['text'])
        received=form['text'].replace('Answer: ','Answer: Purchasing team',1)
        receipt=receive(received,'CR-1',[form],qs,4)
        self.assertEqual(receipt['rows'][0]['status'],'matched')
        saved=review(qs,receipt,[{'question_id':'Q-AUDIENCE','choice':'accept'}],4)
        self.assertEqual(qs[0]['answer'],'');self.assertEqual(saved[0]['answer'],'Purchasing team')
        self.assertNotIn('approval',saved[0]);self.assertEqual(saved[0]['source']['attributed_to'],'Requestor')
        with self.assertRaises(Error):review(qs,receipt,[{'question_id':'Q-AUDIENCE','choice':'accept','answer':'Altered by reviewer'}],4)
        corrected=review(qs,receipt,[{'question_id':'Q-AUDIENCE','choice':'edit','answer':'Authorized correction'}],4)
        self.assertEqual(corrected[0]['source']['attributed_to'],'Framework user correction')
        with self.assertRaises(Error):review(qs,receipt,[{'question_id':'Q-AUDIENCE','choice':'accept'}],5)
        partial=receive(form['text'],'CR-1',[form],qs,4);self.assertEqual(partial['rows'][0]['status'],'unanswered')
        wrong=receive(received,'CR-2',[form],qs,4);self.assertEqual(wrong['status'],'unassigned')
        stale=[dict(qs[0],revision=2)];self.assertEqual(receive(received,'CR-1',[form],stale,4)['rows'][0]['status'],'stale')
        with self.assertRaises(Error):receive(received+'\npassword: abcdefghijklmnop','CR-1',[form],qs,4)
    def test_unknown_and_duplicate_imports_remain_unresolved(self):
        self.assertFalse(answered({"answer": "I don't know / Needs discussion", "selected": []}))
        qs=[{'id':'Q-X','revision':1,'respondent':'Requestor','kind':'text','blocker':True,'category':'requirement','question':'Who receives the report?','explanation':'Identify the people who need the report.','why':'This defines the required audience.','instructions':'Name the group or say unknown.','answer':'','selected':[],'options':[]}]
        form=export_form({'id':'CR-X'},qs,1)
        returned=form['text'].replace('Answer: ','Answer: Managers',1)
        duplicate=returned+'\n'+returned[returned.index('## '):]
        receipt=receive(duplicate,'CR-X',[form],qs,1)
        self.assertEqual([r['status'] for r in receipt['rows']],['duplicate','duplicate'])
        with self.assertRaises(Error):review(qs,receipt,[{'question_id':'Q-X','choice':'accept'}],1)
        repeated=receive(returned+'\nRequest: OTHER','CR-X',[form],qs,1)
        self.assertEqual(repeated['status'],'unassigned')

    def test_amendment_history_and_balance_invariants(self):
        first=amendment_revision('A-1','Monthly only')
        second=amendment_revision('A-1','Weekly instead',first,disposition='submitted')
        self.assertEqual(second['revision'],2);self.assertEqual(second['previous_sha256'],first['sha256'])
        tree={'root':'root','nodes':[{'id':'root','parent':None,'kind':'catalog','children':['a','b']},{'id':'a','parent':'root','kind':'content','path':'a.md'},{'id':'b','parent':'root','kind':'content','path':'b.md'}]}
        self.assertEqual(validate_tree(tree)['leaves'],2)
        tree['nodes'][0]['children'].append('a')
        with self.assertRaises(ContractError):validate_tree(tree)

if __name__=='__main__':unittest.main()
