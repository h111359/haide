import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.dont_write_bytecode=True
ENGINE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ENGINE))
from contracts import Error
from installation import build_manifest, inspect_core, install, upgrade, recover_upgrade
from storage import Store

class Installation(unittest.TestCase):
    def setUp(self):
        parent=ENGINE.parent.parent/'.aih-runtime'/'installation-tests';parent.mkdir(parents=True,exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(dir=parent);self.root=Path(self.tmp.name)
        self.source=self.root/'release'/'.aih';self.source.mkdir(parents=True)
        for name in ['engine','conventions','prompts','skills']:(self.source/name).mkdir()
        (self.source/'engine/cli.py').write_text('print("release fixture, not a product")\n')
        (self.source/'menu.sh').write_text('#!/bin/sh\nexit 0\n')
        for name in ['run.md','README.md','USER_GUIDE.md']:(self.source/name).write_text(name+'\n')
        (self.source/'prompts/action.md').write_text('Semantic fixture')
        (self.source/'skills/catalog.yaml').write_text('{"skills": []}')
        (self.source/'conventions/runtime.schema.json').write_text(json.dumps({'$defs':{'state':{'properties':{'schema_version':{'enum':['1.0']}}}}}))
        build_manifest(self.source)
        self.home=self.root/'product';self.home.mkdir();(self.home/'human.txt').write_text('keep')
    def tearDown(self):self.tmp.cleanup()
    def test_install_reuse_and_integrity(self):
        result=install(self.source,self.home);self.assertTrue(result['installed'])
        self.assertEqual((self.home/'human.txt').read_text(),'keep')
        if os.name == 'posix':self.assertTrue(os.access(self.home/'.aih/menu.sh',os.X_OK))
        self.assertTrue(install(self.source,self.home)['reused'])
        (self.source/'README.md').write_text('unexpected')
        with self.assertRaises(Error):install(self.source,self.root/'other')
        self.assertFalse((self.root/'other').exists())
    def test_upgrade_gate_and_preservation(self):
        install(self.source,self.home);store=Store(self.home)
        state={'schema_version':'1.0','revision':1,'owner':None,'active_request':'CR-X'};store.write('state.yaml',state)
        (self.source/'README.md').write_text('new release');build_manifest(self.source,'1.0.1')
        with self.assertRaises(Error):upgrade(self.home,self.source)
        state['active_request']=None;state['owner']={'id':'external','status':'reserved'};store.write('state.yaml',state)
        with self.assertRaises(Error):upgrade(self.home,self.source)
        state['owner']=None;store.write('state.yaml',state)
        result=upgrade(self.home,self.source)
        self.assertTrue(result['upgraded']);self.assertEqual((self.home/'.aih/README.md').read_text(),'new release')
        self.assertEqual((self.home/'human.txt').read_text(),'keep');self.assertIsNone(store.read('state.yaml')['owner'])
        self.assertTrue((self.home/result['backup'].split(':',1)[1]/'README.md').is_file())
    def test_interrupted_replacement_recoverable_without_silent_rollback(self):
        install(self.source,self.home);store=Store(self.home)
        store.write('state.yaml',{'schema_version':'1.0','revision':1,'owner':None,'active_request':None})
        (self.source/'README.md').write_text('next');build_manifest(self.source,'1.0.1')
        import installation
        real=installation._swap;calls=[]
        def interrupt(workspace,source,destination):
            calls.append(destination)
            if len(calls)==2:raise OSError('simulated interruption after retaining old core')
            return real(workspace,source,destination)
        with patch('installation._swap',side_effect=interrupt):
            with self.assertRaises(OSError):upgrade(self.home,self.source)
        self.assertFalse((self.home/'.aih').exists());self.assertIsNotNone(store.read('state.yaml')['owner'])
        journals=list((self.home/'.aih_product/ledger/operations').glob('*/core-upgrade.yaml'));self.assertEqual(len(journals),1)
        result=recover_upgrade(self.home,journals[0].relative_to(self.home/'.aih_product').as_posix())
        self.assertTrue(result['recovered']);self.assertEqual((self.home/'.aih/README.md').read_text(),'next');self.assertIsNone(store.read('state.yaml')['owner'])
    @unittest.skipUnless(os.name=='posix','POSIX aliases')
    def test_symlink_package_refused(self):
        (self.source/'README.md').unlink();(self.source/'README.md').symlink_to(self.home/'human.txt')
        with self.assertRaises(Error):inspect_core(self.source)

if __name__=='__main__':unittest.main()
