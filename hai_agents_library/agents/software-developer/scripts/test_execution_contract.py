import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import execution_contract as contract

ACTIVITY = '088c1e8e-caa9-4971-9328-cb742a4db998'
DIRECT = '# Direct work\n\n'+'\n\n'.join('## '+s+'\n\n'+v for s,v in [
    ('Outcome','Preserve exact submitted text.'),('Scope','Write notes.md only.'),('Constraints','UTF-8, no normalization.'),
    ('Acceptance','A1: exact content readback.'),('Tasks','1.1: write the submitted text to notes.md.'),
    ('Verification','Read back notes.md and compare exact bytes.'),('Documentation','notes.md is the requested document; no other documentation update needed.')])+'\n'


def context(directive=DIRECT):
    return dict(activity_id=ACTIVITY,input_revision='input-1',decision_revision='decision-1',
                directive_sha256=hashlib.sha256(directive.encode()).hexdigest(),mode='direct',direct_selected=True,
                authority={'text':'Implement the current bounded work.','source':'human current chat','origin':'human'},
                business_readiness={'status':'passed','evidence':'All current checks have evidence.'},unresolved_decisions=[],
                implementation_start_verified=True,conventions=[{'name':'coding','required':True,'status':'ready'}],owners=[],
                writes=[{'path':'notes.md','operation':'create'}],outside_permissions=[],protected_changes=[],
                expected_tasks=['1.1'],acceptance_ids=['A1'],expected_checks=[{'id':'C1','required':True,'acceptance':['A1']}])


def evidence(ctx):
    return dict(**{k:ctx[k] for k in ['activity_id','directive_sha256','input_revision','decision_revision']},status='verified',
                tasks=[{'id':'1.1','status':'completed','result':'Wrote exact input.'}],
                changes=[{'path':'notes.md','operation':'create','baseline':'absent','result':'Exact readback.'}],
                checks=[{'id':'C1','required':True,'status':'passed','result':'Exact byte comparison passed.'}],owners=[],
                documentation='Requested document current.',protection='No protected changes, baseline compared.',
                history='Host record prepared.',blockers=[])


class ExecutionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']);self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)

    def test_explicit_direct_work_and_optional_absence(self):
        ctx=context();ctx['conventions'].append({'name':'optional context','required':False,'status':'missing'})
        self.assertTrue(contract.preflight(self.root,DIRECT,ctx)['ok'])

    def test_every_required_context_field(self):
        for field in context():
            if field=='outside_permissions':continue
            ctx=context();del ctx[field]
            with self.subTest(field=field): self.assertFalse(contract.preflight(self.root,DIRECT,ctx)['ok'])

    def test_empty_template_or_unselected_direct(self):
        for directive in ['',DIRECT.replace('Preserve exact submitted text.','TODO'), '# Template\nTODO']:
            self.assertFalse(contract.preflight(self.root,directive,context(directive))['ok'])
        ctx=context();ctx['direct_selected']=False
        self.assertFalse(contract.preflight(self.root,DIRECT,ctx)['ok'])

    def test_stale_hash_unresolved_decisions_and_missing_marker(self):
        for key,value in [('directive_sha256','stale'),('unresolved_decisions',['Q001']),('implementation_start_verified',False)]:
            ctx=context();ctx[key]=value
            self.assertFalse(contract.preflight(self.root,DIRECT,ctx)['ok'])

    def test_failed_dependencies_and_readiness(self):
        for field in ['conventions','owners']:
            ctx=context();ctx[field]=[{'name':'required','required':True,'status':'missing'}]
            self.assertFalse(contract.preflight(self.root,DIRECT,ctx)['ok'])
        ctx=context();ctx['business_readiness']['status']='blocked'
        self.assertFalse(contract.preflight(self.root,DIRECT,ctx)['ok'])

    def test_generated_maintenance_claim_and_actual_covering_evidence(self):
        ctx=context();ctx['protected_changes']=['.hai/rule.md']
        self.assertFalse(contract.preflight(self.root,DIRECT,ctx)['ok'])
        ctx['maintenance_authority']={'text':'Maintain this rule.','source':'current chat','origin':'generated','paths':['.hai/rule.md']}
        self.assertFalse(contract.preflight(self.root,DIRECT,ctx)['ok'])
        ctx['maintenance_authority']['origin']='human'
        self.assertTrue(contract.preflight(self.root,DIRECT,ctx)['ok'])

    def test_linked_escape_needs_location_operation_and_purpose(self):
        # Both test directories are inside the actual workspace; outside is relative to the fixture root only.
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as other:
            (self.root/'escape').symlink_to(other,target_is_directory=True)
            ctx=context();ctx['writes']=[{'path':'escape/out.md','operation':'create','purpose':'export'}]
            self.assertFalse(contract.preflight(self.root,DIRECT,ctx)['ok'])
            grant={'location':other,'operations':['create'],'purpose':'export','text':'Create export here.','source':'human chat','origin':'human'}
            ctx['outside_permissions']=[grant]
            self.assertTrue(contract.preflight(self.root,DIRECT,ctx)['ok'])
            for field,value in [('purpose','other'),('origin','generated'),('operations','create')]:
                changed=copy.deepcopy(ctx);changed['outside_permissions'][0][field]=value
                self.assertFalse(contract.preflight(self.root,DIRECT,changed)['ok'])

    def test_missing_plan_peer_blocks_plan_only(self):
        ctx=context();ctx['mode']='plan'
        self.assertFalse(contract.preflight(self.root,DIRECT,ctx)['ok'])
        self.assertTrue(contract.preflight(self.root,DIRECT,context())['ok'])

    def test_installed_plan_peer_and_standalone_handoff(self):
        installed=Path(__file__).resolve().parents[2]/'solution-architect/scripts'
        dest=self.root/'.hai_env/agents/solution-architect/scripts';dest.mkdir(parents=True)
        shutil.copyfile(installed/'plan_contract.py',dest/'plan_contract.py')
        spec=importlib.util.spec_from_file_location('plan_fixtures',installed/'test_plan_contract.py')
        fixtures=importlib.util.module_from_spec(spec)
        sys.path.insert(0,str(installed))
        try: spec.loader.exec_module(fixtures)
        finally: sys.path.pop(0)
        plan=fixtures.sample_plan();ctx=context(plan);ctx['mode']='plan'
        self.assertTrue(contract.preflight(self.root,plan,ctx)['ok'])
        ctx['decision_revision']='new answer'
        self.assertFalse(contract.preflight(self.root,plan,ctx)['ok'])
        self.assertFalse((dest/'__pycache__').exists())

    def test_complete_evidence_and_all_failure_statuses(self):
        ctx=context();self.assertTrue(contract.validate_evidence(evidence(ctx),ctx)['ok'])
        for status in ['failed','skipped','unavailable']:
            e=evidence(ctx);e['checks'][0]['status']=status
            self.assertFalse(contract.validate_evidence(e,ctx)['ok'])
            e['status']='blocked';e['blockers']=['C1 not passed']
            self.assertTrue(contract.validate_evidence(e,ctx)['ok'])

    def test_omitted_or_downgraded_checks_tasks_and_owner(self):
        ctx=context();ctx['owners']=[{'name':'knowledge owner','required':True,'status':'ready'}]
        self.assertFalse(contract.validate_evidence(evidence(ctx),ctx)['ok'])
        for key,value in [('tasks',[]),('checks',[]),('checks',[{'id':'C1','required':False,'status':'passed','result':'claim'}])]:
            e=evidence(context());e[key]=value
            self.assertFalse(contract.validate_evidence(e,context())['ok'])
        e=evidence(ctx);e['owners']=[{'name':'knowledge owner','required':True,'status':'pending','evidence':'not delivered'}]
        self.assertFalse(contract.validate_evidence(e,ctx)['ok'])
        e['owners'][0].update(status='completed',evidence='Validated readback.')
        self.assertTrue(contract.validate_evidence(e,ctx)['ok'])

    def test_preexisting_work_preserved_and_cli_readonly(self):
        untouched=self.root/'unrelated.txt';untouched.write_text('pre-existing edit')
        directive=self.root/'directive.md';directive.write_text(DIRECT,encoding='utf-8')
        source=self.root/'context.json';source.write_text(json.dumps(context(),ensure_ascii=False))
        snapshot={p.name:p.read_bytes() for p in self.root.iterdir()}
        result=subprocess.run([sys.executable,'-B',str(Path(contract.__file__)),'--workspace',str(self.root),
                               '--directive','directive.md','--context','context.json'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout)
        self.assertEqual(snapshot,{p.name:p.read_bytes() for p in self.root.iterdir()})
        source.write_text('{"mode":"direct","mode":"plan"}')
        result=subprocess.run([sys.executable,'-B',str(Path(contract.__file__)),'--workspace',str(self.root),
                               '--directive','directive.md','--context','context.json'],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertEqual(untouched.read_text(),'pre-existing edit')

    def test_stale_delivery_and_incomplete_coverage(self):
        ctx=context();e=evidence(ctx);e['input_revision']='old'
        self.assertFalse(contract.validate_evidence(e,ctx)['ok'])
        ctx['acceptance_ids'].append('A2')
        self.assertFalse(contract.preflight(self.root,DIRECT,ctx)['ok'])

    def test_cli_preserves_crlf_for_exact_directive_hash(self):
        directive=DIRECT.replace('\n','\r\n').replace('Preserve exact submitted text.','Запази 日本語 exactly.')
        (self.root/'directive.md').write_bytes(directive.encode('utf-8'))
        (self.root/'context.json').write_text(json.dumps(context(directive),ensure_ascii=False))
        result=subprocess.run([sys.executable,'-B',str(Path(contract.__file__)),'--workspace',str(self.root),
                               '--directive','directive.md','--context','context.json'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout)
        self.assertEqual((self.root/'directive.md').read_bytes(),directive.encode('utf-8'))

    def test_independent_review_placeholder_bullets_and_title(self):
        for body in ['- TODO\n- TBD', '- [ ] TODO\n- **TBD**', '<fill outcome>']:
            directive='# Direct work\n\n'+'\n\n'.join('## '+name+'\n\n'+body for name in
                      ['Outcome','Scope','Constraints','Acceptance','Tasks','Verification','Documentation'])
            self.assertFalse(contract.preflight(self.root,directive,context(directive))['ok'])
        directive=DIRECT.split('\n',2)[2]
        self.assertFalse(contract.preflight(self.root,directive,context(directive))['ok'])

    def test_independent_review_hardlink_write_is_unknown_containment(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as other:
            source=Path(other)/'shared.txt';source.write_text('pre-existing shared bytes')
            os.link(source,self.root/'hard.txt')
            self.assertFalse(contract.permitted_write(self.root,{'path':'hard.txt','operation':'modify'},[]))
            self.assertEqual(source.read_text(),'pre-existing shared bytes')

    def test_independent_review_optional_failed_acceptance_cannot_verify(self):
        ctx=context();ctx['expected_checks'][0]['required']=False
        self.assertFalse(contract.preflight(self.root,DIRECT,ctx)['ok'])
        result=evidence(ctx);result['checks'][0].update(required=False,status='failed')
        self.assertFalse(contract.validate_evidence(result,ctx)['ok'])

    def test_protected_write_cannot_be_omitted_from_declared_inspection(self):
        ctx=context();ctx['writes']=[{'path':'.hai/rule.md','operation':'modify'}]
        self.assertFalse(contract.preflight(self.root,DIRECT,ctx)['ok'])
        ctx['protected_changes']=['.hai/rule.md']
        ctx['maintenance_authority']={'text':'Maintain rule.','source':'current human chat','origin':'human','paths':['.hai/rule.md']}
        self.assertTrue(contract.preflight(self.root,DIRECT,ctx)['ok'])

    def test_actual_unplanned_change_requires_refreshed_preflight(self):
        ctx=context();result=evidence(ctx)
        result['changes'][0]['path']='other.md'
        self.assertFalse(contract.validate_evidence(result,ctx)['ok'])

    def test_final_review_fenced_headings_and_comment_only_sections(self):
        fenced='```markdown\n'+DIRECT+'```\n'
        self.assertFalse(contract.preflight(self.root,fenced,context(fenced))['ok'])
        commented='# Direct work\n\n'+'\n\n'.join('## '+s+'\n\n<!-- TODO -->' for s in
                  ['Outcome','Scope','Constraints','Acceptance','Tasks','Verification','Documentation'])
        self.assertFalse(contract.preflight(self.root,commented,context(commented))['ok'])
        example=DIRECT+'\n```markdown\n## Scope\nexample only\n```\n'
        self.assertTrue(contract.preflight(self.root,example,context(example))['ok'])
        self.assertFalse(contract.preflight(self.root,DIRECT+'\n```\nunclosed',context(DIRECT+'\n```\nunclosed'))['ok'])

    def test_final_review_inline_and_list_html_is_not_substantive(self):
        for body in ['- <!-- TODO -->','TODO <!-- template marker -->','<span></span>', '- <div/>']:
            directive='# Direct work\n\n'+'\n\n'.join('## '+name+'\n\n'+body for name in
                      ['Outcome','Scope','Constraints','Acceptance','Tasks','Verification','Documentation'])
            self.assertFalse(contract.preflight(self.root,directive,context(directive))['ok'])


if __name__ == '__main__': unittest.main()
