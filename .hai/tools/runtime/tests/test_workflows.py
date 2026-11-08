import json
import hashlib
import os
from pathlib import Path
import shutil
import sys
import unittest
import uuid
from unittest import mock

TOOLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(TOOLS))
from runtime import activities, recording, host, packages

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.root = Path.cwd() / ('fixture-' + uuid.uuid4().hex)
        (self.root / '.hai_env/activities').mkdir(parents=True)
        (self.root / '.hai/templates').mkdir(parents=True)
        shutil.copy(TOOLS.parent / 'templates/state.json', self.root / '.hai/templates/state.json')
        (self.root / '.hai_env/agent_instructions.md').write_text('')
        (self.root / '.hai_env/state.json').write_text(json.dumps({'state_format_version': 3, 'activities': {'location': '.hai_env/activities'}, 'features': {'chronicles': {'enabled': True, 'record_every_prompts': 5}}, 'integrations': {}}))
        self.prov = {'source': 'test', 'reason': 'exercise'}
    def tearDown(self):
        shutil.rmtree(self.root)
    def call(self, op, **kw):
        return activities.handle(op, self.root, kw, True)
    def test_create_record_revision_close_and_supplement(self):
        created = self.call('create', initial_input='exact\ninput', provenance=self.prov)
        self.assertTrue(created['ok'], created)
        ident = created['result']['state']['activity_id']; base = self.root / created['result']['path']
        self.assertEqual((base/'input.md').read_text(), 'exact\ninput')
        r = self.call('record', activity_id=ident, implementation_start=True, steps={'implementation':'in_progress'}, artifacts=[{'name':'plan.md','text':'first','reason':'initial'}], log='started', provenance=self.prov)
        self.assertTrue(r['ok'], r); marker = r['result']['state']['implementation_started_at']
        old = (base/'plan.md').read_bytes()
        r = self.call('record', activity_id=ident, implementation_start=True, steps={}, artifacts=[{'name':'plan.md','text':'second','reason':'revision'}], input_append='\nnext exact', log='changed', provenance=self.prov)
        self.assertTrue(r['ok'], r); self.assertEqual(r['result']['state']['implementation_started_at'], marker)
        self.assertEqual(next((base/'files/revisions/plan').iterdir()).read_bytes(), old)
        self.assertEqual((base/'input.md').read_text(), 'exact\ninput\nnext exact')
        state = json.loads((self.root / '.hai_env/state.json').read_text())
        state['features']['chronicles']['enabled'] = False
        (self.root / '.hai_env/state.json').write_text(json.dumps(state))
        closed = self.call('close', activity_id=ident, outcome='completed', archive_label='test', outcome_text='done', recording={'status':'disabled','details':'fixture recording disabled'}, provenance=self.prov)
        self.assertTrue(closed['ok'], closed)
        supplement = self.call('supplement', activity_id=ident, text='additional evidence', provenance=self.prov)
        self.assertTrue(supplement['ok'], supplement)
        self.assertIn('additional evidence', (self.root/closed['result']['archive_path']/'log.md').read_text())
    def test_safety_and_recording(self):
        c = self.call('create', initial_input='x', provenance=self.prov); ident=c['result']['state']['activity_id']
        r = self.call('record', activity_id=ident, steps={'implementation':'in_progress'}, artifacts=[], log='x', provenance=self.prov)
        self.assertFalse(r['ok'])
        r = self.call('close', activity_id=ident, outcome='completed', archive_label='x', outcome_text='x', recording={'status':'pending','details':'x','mandatory':True}, provenance=self.prov)
        self.assertFalse(r['ok'])
        self.assertFalse(self.call('create',initial_input='x',provenance=self.prov)['ok'])
        r=recording.handle('schedule',self.root,{'occurrence_ids':['1','2','3','4','5'], 'covered_ids':['1'], 'last_dispatched_count':1},False)
        self.assertFalse(r['result']['dispatch_due']); self.assertEqual(r['result']['gaps'],['2','3','4','5'])
        self.assertFalse(host.handle('invoke',self.root,{},False)['ok'])
    def test_verified_closure_checks_actual_file_bytes(self):
        c = self.call('create',initial_input='x',provenance=self.prov); ident=c['result']['state']['activity_id']; base=c['result']['path']
        (self.root/'source.txt').write_text('source')
        (self.root/base/'segment.txt').write_text('artifact')
        digest = lambda text: hashlib.sha256(text.encode()).hexdigest()
        sources={'session':digest('source')}; artifacts={'segment':digest('artifact')}
        occurrence={'source_session_id':'session','source_position':1}
        operation={'activity_id':ident,'operation_id':'unique','cutoff':[occurrence],'enabled_intervals':[{'start':occurrence,'end':None,'provenance':'enabled'}]}
        requirement={'enabled':True,'mandatory':False}
        evidence={**operation,'recording_requirement':requirement,'verification_id':'v1','verified_at':'2026-11-05T19:00:00Z','status':'verified','retained_source_complete':True,'gaps':[],'conflicts':[],'active_writes':False,'source_snapshots':sources,'artifact_snapshots':artifacts}
        proof={'recording_requirement':requirement,'operation':operation,'evidence':evidence,'current_sources':sources,'current_artifacts':artifacts,'writers_stopped':True}
        args={'activity_id':ident,'outcome':'completed','archive_label':'verified','outcome_text':'done','recording':{'status':'verified','details':'proof supplied'},'recording_proof':proof,'recording_paths':{'sources':{'session':'source.txt'},'artifacts':{'segment':base+'/segment.txt'}},'provenance':self.prov}
        (self.root/'source.txt').write_text('changed')
        self.assertFalse(self.call('close',**args)['ok'])
        (self.root/'source.txt').write_text('source')
        result=self.call('close',**args)
        self.assertTrue(result['ok'],result)

    def test_guard_and_partial_write(self):
        (self.root/'.hai_env/agent_instructions.md').unlink()
        r = self.call('create', initial_input='x', provenance=self.prov)
        self.assertFalse(r['ok']); self.assertFalse((self.root/'.hai_env/activities/00000000_000000_active').exists())
        (self.root/'.hai_env/agent_instructions.md').write_text('')
        c = self.call('create', initial_input='x', provenance=self.prov); ident = c['result']['state']['activity_id']
        original = activities.write_bytes
        def fail_log(root, path, data, expected=None):
            if path.endswith('/log.md'): raise OSError('simulated write failure')
            return original(root,path,data,expected)
        with mock.patch.object(activities, 'write_bytes', side_effect=fail_log):
            r = self.call('record', activity_id=ident, steps={}, artifacts=[{'name':'plan.md','text':'preserved','reason':'test'}], log='x', provenance=self.prov)
        self.assertEqual(r['status'],'partial'); self.assertTrue((self.root/c['result']['path']/'plan.md').exists())

    def test_real_package_install_and_registration(self):
        source_repo = TOOLS.parent.parent
        shutil.copytree(source_repo / '.hai', self.root / '.hai', dirs_exist_ok=True)
        source = self.root / 'sources/agents/software-developer'
        source.parent.mkdir(parents=True)
        shutil.copytree(source_repo / '.hai_env/agents/software-developer', source)
        req = {'source':'sources/agents/software-developer', 'name':'software-developer', 'provenance':self.prov, 'register':True}
        result = packages.handle('install',self.root,req,True)
        self.assertTrue(result['ok'],result)
        self.assertTrue((self.root / '.hai_env/agents/software-developer/SKILL.md').is_file())
        result = packages.handle('register',self.root,{'name':'software-developer','provenance':self.prov},True)
        self.assertTrue(result['ok'], result); self.assertEqual(result['changed_files'], [])

    def test_untrusted_packages_rejected(self):
        (self.root/'src').mkdir(); (self.root/'src/pkg').mkdir(); (self.root/'src/pkg/SKILL.md').symlink_to('/etc/passwd')
        (self.root/'.hai_env/agents').mkdir()
        r=packages.handle('install',self.root,{'source':'src/pkg','name':'pkg','provenance':self.prov},True)
        self.assertFalse(r['ok']); self.assertFalse((self.root/'.hai_env/agents/pkg').exists())
        r=packages.handle('install',self.root,{'source':'https://example.test/p','name':'pkg','provenance':self.prov},True)
        self.assertEqual(r['status'],'unsupported')

if __name__ == '__main__': unittest.main()
