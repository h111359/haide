"""Optional rendered Chrome walkthrough; browser writes are enforced under fixture roots.

Run with Python -B; websockets and an installed Chrome are review prerequisites,
not AIH runtime dependencies. The fixture is explicitly synthetic.
"""
from __future__ import annotations
import asyncio
import base64
import ctypes
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from portal import PortalServer
from workflow import catalog
from contracts import Error
from exchange import render as render_questions, review as review_answers
from execution import READ, WRITE, EXECUTE, READ_FILE, WRITE_FILE, MAKE_SOCK, MAKE_FIFO, process_identity
import websockets

REPO = Path(__file__).resolve().parents[3]
LOGS = REPO / "logs" / "portal-browser"
BASE = REPO / "tests"

class BrowserFixture:
    def __init__(self, home):
        self.home = home
        self.revision = 1
        self.busy = False
        self.draft = "Add a CSV export for filtered report rows."
        self.saved = []
        self.receipts = {}
        self.phase = "analysis"
        self.scenario = 'active'
        self.review_rows = None
        self.question_attachments = []
        self.reviewed = None
        self.q = [{"id": "Q-1", "revision": 1, "respondent": "Requestor", "kind": "single", "blocker": True, "category": "requirement", "question": "Which rows should be exported?", "explanation": "The report may contain more rows than currently displayed.", "why": "Defines the expected export content.", "instructions": "Choose one or explain an alternative.", "options": ["Filtered rows", "All rows"], "default": "Filtered rows", "answer": "", "selected": []}]
    def initialize(self):
        return {"reused": True, "revision": self.revision}
    def operations(self):
        return [{**o,"available":not self.busy or o['id']=='stop',"reason":"Stop is the only operational control." if self.busy and o['id']!='stop' else ''} for o in catalog()]
    def status(self):
        now='2026-09-22T17:30:00Z'
        tasks=[{"id":"T-1","title":"Add scoped CSV export","status":"pending","changes":[{"path":"home:src/export.py","action":"create"}],"requirements":["R-1"],"criteria":["Filtered rows exported"]},{"id":"T-2","title":"Run the complete required suite","status":"pending"},{"id":"T-3","title":"Apply documentation and record results","status":"pending"}]
        request={"id":"CR-browser","title":"CSV export for reports","status":"open","phase":self.phase,"scope_revision":2,"plan_revision":3,"plan_data":{"revision":3,"bindings":{"workspace_revision":1,"scope_revision":2,"interpretation_revision":4}},"plan":"# Plan\n\nExport only the filtered report rows.","tasks":tasks,"questions":self.q,"questionnaire":render_questions(self.q),"interpretation":"# Interpretation\n\nUsers need an export of filtered report rows. <img src=x onerror=window.evil=1>","assessment":"# Assessment\n\nReuse the existing authorized report query.","blockers":[],"approval":None,"completion_gates":[{"id":"tests","label":"Required suite passed","passed":False}],"ready_to_close":False,"review_revision":"review-1","documentation_increment":{"items":[{"id":"DOC-1","target":"Reports","change":"Describe filtered export","status":"planned"}]}}
        root={"id":"home","name":"Product home","path":str(self.home),"purpose":"Synthetic browser product","access":"read-write","available":True}
        operation={"id":"OP-browser","action":"implement","status":"running","created":now,"events":[{"time":now,"message":"Task T-1 accepted; evidence pending."}]} if self.busy else None
        state = {"revision":self.revision,"version":"1.0.0","product":{"name":"Northstar · browser test fixture","home":str(self.home)},"config":{"product_name":"Northstar · browser test fixture","workspace":{"revision":1,"roots":[root]},"default_profile":"manual","profiles":{"manual":{"adapter":"manual","name":"Reviewed handoff","timeout":1800}},"appearance":{"theme":"clear","size":16},"repair_budget":{"max_cycles":3},"capability_profiles":{}},"active_request":request,"busy":self.busy,"operation":operation,"setup":{"status":"complete"},"documentation":{"baseline":{"status":"complete"},"tree":{"nodes":[{"id":"root","title":"Product knowledge","kind":"catalog","path":"index.yaml","children":["reports"]},{"id":"reports","title":"Reporting and exports","kind":"content","parent":"root","path":"topics/reports.md","status":"current","updated":now,"sources":["home:src/reports.py"]}]},"known_defects":{"defects":[{"id":"D-1","summary":"Unrelated date parsing defect","status":"suspected","disposition":"investigate","impact":"Required regression test may fail."}]}},"tests":{"results":[{"suite_id":"regression","status":"not_run","checked_content":{"root":"home","workspace_revision":1}}]},"runs":[operation] if operation else [{"id":"OP-analysis","action":"analyze","status":"completed","created":now,"events":[{"time":now,"message":"Generated plan revision 3; awaiting human approval."}]}],"questions":[{"id":"Q-history","title":"How does filtering work?","status":"answered","answer":"Existing filters apply before export.","sources":["home:src/reports.py"]}],"history":[{"id":"CR-closed","title":"Earlier report change","outcome":"cancelled","closed_at":now,"location":"change_requests/history/CR-closed","path":"request:CR-closed"}],"ledger":[{"id":"EV-1","type":"plan-generated","summary":"Generated plan revision 3","created_at":now}],"draft":{"change":self.draft,"question":""},"questionnaires":render_questions(self.q),"amendments":[],"forms":[{"id":"FORM-1","revision":1,"path":"request:CR-browser/form.txt"}],"receipts":[{"id":"RECEIPT-1","review_revision":"review-1","status":"staged","rows":[{"question_id":"Q-1","status":"matched","answer":"Filtered rows","previous_answer":""}]}],"current_response":"Plan revision 3 is ready for your review. No implementation has started.","instructions":"# Human instructions\n\nPreserve report authorization.","skills":[{"id":"clarify-requirements","name":"Clarify requirements","version":"1.0.0","enabled":True,"description":"Refine the desired outcomes without selecting an implementation."},{"id":"git-integration","name":"Git integration","version":"1.0.0","enabled":False,"description":"Optional explicitly authorized Git workflow."}],"profiles":{"manual":{"adapter":"manual","name":"Reviewed handoff","timeout":1800}},"available_actions":self.operations(),"usage":{"tokens":None}}
        state['attachments']={'change':[],'question':self.question_attachments}
        if self.review_rows is not None:
            state['receipts'][0]['rows']=self.review_rows
        if self.scenario in ('empty','setup'):
            state['active_request']=None
            state['questionnaires']=''
            state['forms']=[]
            state['receipts']=[]
            if self.scenario=='setup':
                state['setup']={'status':'pending','message':'Product files are initialized. Documentation generation is waiting for a configured, authenticated agent.'}
                state['documentation']['baseline']['status']='pending'
                state['profiles']={}
        elif self.scenario=='ready':
            state['active_request']['status']='ready-to-close'
            state['active_request']['ready_to_close']=True
            state['active_request']['completion_gates']=[{'id':'all','label':'All completion gates','passed':True}]
            for task in state['active_request']['tasks']:task['status']='completed'
        elif self.scenario=='blocked':
            state['active_request']['blockers']=['Deferred defect D-1 fails a required test.']
            state['active_request']['status']='blocked'
            state['tests']['results'][0]['status']='failed'
        elif self.scenario=='manual':
            state['busy']=True
            state['operation']={'id':'OP-manual','action':'implement','status':'reserved','external':True,'handoff':{'id':'HANDOFF-1','status':'prepared-reserved','instructions':'Perform only scoped tasks, retain evidence, then stop and reconcile.'}}
        return state
    def artifact(self, path):
        return {"text":"# Stored documentation\n\nObserved report behavior, source references, and explicit uncertainties."}
    def dispatch(self, operation,payload,expected_revision=None,idempotency_key=None,**kw):
        if idempotency_key in self.receipts:return self.receipts[idempotency_key]
        if self.busy and operation!='stop':raise Error('busy','Another action owns execution.')
        if expected_revision!=self.revision:raise Error('revision-conflict','Saved revision changed; reconcile your draft.')
        if operation=='save-draft':self.draft=payload['text']
        elif operation=='stop':self.busy=False
        elif operation=='approve':self.phase='implementation'
        elif operation=='save-questionnaire':pass
        elif operation=='review-answers':
            self.reviewed=review_answers(self.q,self.status()['receipts'][0],payload['decisions'],'review-1')
            self.q=self.reviewed
        elif operation=='remove-attachment':
            if payload.get('lane')!='question':raise Error('wrong-lane','Question attachment removal must preserve its lane.')
            self.question_attachments=[x for x in self.question_attachments if x['id']!=payload['id']]

        self.saved.append((operation,payload));self.revision+=1
        result={'ok':True,'revision':self.revision,'operation_id':'OP-'+str(self.revision)};self.receipts[idempotency_key]=result
        return result

async def review(wsurl,server,fixture,process):
    async with websockets.connect(wsurl,max_size=32*1024*1024) as ws:
        counter=0;errors=[]
        async def call(method,params=None):
            nonlocal counter
            counter+=1;ident=counter
            await ws.send(json.dumps({'id':ident,'method':method,'params':params or {}}))
            while True:
                result=json.loads(await ws.recv())
                if result.get('method')=='Runtime.exceptionThrown':errors.append(result['params'])
                if result.get('id')==ident:
                    if 'error' in result:raise AssertionError(result['error'])
                    return result.get('result',{})
        async def js(expression):
            r=await call('Runtime.evaluate',{'expression':expression,'awaitPromise':True,'returnByValue':True})
            if 'exceptionDetails' in r:raise AssertionError(r['exceptionDetails'])
            return r.get('result',{}).get('value')
        await call('Runtime.enable');await call('Page.enable')
        await call('Emulation.setDeviceMetricsOverride',{'width':1440,'height':1100,'deviceScaleFactor':1,'mobile':False})
        await call('Page.navigate',{'url':server.url})
        for _ in range(60):
            await asyncio.sleep(.1)
            if await js("!!document.querySelector('#main h1')"):break
        if not await js("!!document.querySelector('#main')"):
            raise AssertionError(await js("({url:location.href,title:document.title,body:document.body?.innerText})"))
        results=[]
        routes=['overview','request/input','request/analysis','request/plan','request/implementation','request/verification','request/outcome','questions','documentation','documentation/reports','runs','history','history/ledger','settings/workspace','settings/profiles','settings/skills','settings/product','settings/instructions','settings/appearance','help/quick-start']
        for route in routes:
            await js('location.hash='+json.dumps(route));await asyncio.sleep(.12)
            content=await js("({title:document.querySelector('#main h1')?.textContent,text:document.querySelector('#main').innerText.length,overflow:document.documentElement.scrollWidth>innerWidth+2})")
            assert content['title'] and content['text']>120,(route,content)
            assert not content['overflow'],('overflow',route)
            if route=='request/plan':
                assert await js("[...document.querySelectorAll('.meta-list dd')].map(e=>e.innerText).join('|')")=='3|2|1|4'
                assert 'home:src/export.py' in await js("document.querySelector('.task-list').textContent")

            results.append({'route':route,**content})
            if route in ['overview','request/input','request/plan','settings/workspace','settings/appearance']:
                shot=await call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False})
                (LOGS/(route.replace('/','-')+'.png')).write_bytes(base64.b64decode(shot['data']))
        assert not await js('!!window.evil'),'Unsafe Markdown executed'
        # Editing and passive navigation do not start work; explicit save does.
        await js("location.hash='request/input'");await asyncio.sleep(.15)
        await js("(()=>{let e=document.querySelector('#change-text');e.value='Revised filtered CSV request';e.dispatchEvent(new Event('input',{bubbles:true}));})()")
        assert not fixture.saved
        assert await js("document.querySelector('[data-operation=clarify]').disabled")
        await js("document.querySelector('a[href=\"#questions\"]').click()")
        assert await js("document.querySelector('#modal').open")
        await js("document.querySelector('[data-dialog=\"2\"]').click()")
        await js("document.querySelector('[data-operation=\"save-draft\"]').click()")
        await asyncio.sleep(.3)
        assert fixture.saved[-1][0]=='save-draft'
        assert fixture.draft=='Revised filtered CSV request'
        # Real deterministic review receives visible checkbox/comments fields, while duplicate rows remain unadopted.
        fixture.q.append({**fixture.q[0],'id':'Q-2','question':'Which records can members export?'})
        fixture.review_rows=[
            {'question_id':'Q-1','question_revision':1,'question':fixture.q[0]['question'],'explanation':fixture.q[0]['explanation'],'attributed_to':'Requestor','status':'duplicate','answer':'','selected':['Filtered rows'],'comments':'First duplicate'},
            {'question_id':'Q-1','question_revision':1,'question':fixture.q[0]['question'],'explanation':fixture.q[0]['explanation'],'attributed_to':'Requestor','status':'duplicate','answer':'','selected':['All rows'],'comments':'Second duplicate'},
            {'question_id':'Q-2','question_revision':1,'question':fixture.q[1]['question'],'explanation':fixture.q[1]['explanation'],'attributed_to':'Requestor','status':'matched','answer':'','selected':['Filtered rows'],'comments':'Only visible rows'}]
        fixture.revision+=1
        await asyncio.sleep(2.7)
        await js("document.querySelector('[data-local=accept-matched]').closest('details').open=true")
        assert await js("document.querySelector('#receipt-RECEIPT-1-2-selected').value")=='Filtered rows'
        assert await js("document.querySelector('#receipt-RECEIPT-1-2-comments').value")=='Only visible rows'
        assert 'Attributed respondent: Requestor' in await js("document.querySelector('#main').innerText")
        await js("document.querySelector('[data-operation=review-answers]').click()");await asyncio.sleep(.3)
        assert fixture.saved[-1][1]['decisions']==[]
        assert all(not q['selected'] for q in fixture.q)
        async def set_review(index,decision):
            await js("(()=>{const e=document.querySelector('#receipt-RECEIPT-1-"+str(index)+"-choice');e.value="+json.dumps(decision)+";e.dispatchEvent(new Event('change',{bubbles:true}));})()")
        await set_review(0,'retain')
        await js("document.querySelector('[data-operation=review-answers]').click()");await asyncio.sleep(.3)
        assert len(fixture.saved[-1][1]['decisions'])==1
        assert not fixture.q[0]['selected']
        await js("document.querySelector('[data-local=accept-matched]').click()")
        assert await js("document.querySelector('#receipt-RECEIPT-1-0-choice').value")=='unresolved'
        assert await js("document.querySelector('#receipt-RECEIPT-1-2-choice').value")=='accept'
        await js("document.querySelector('[data-operation=review-answers]').click()");await asyncio.sleep(.3)
        assert fixture.q[1]['selected']==['Filtered rows'] and fixture.q[1]['comments']=='Only visible rows'
        assert not fixture.q[0]['selected']
        await set_review(1,'edit')
        await js("document.querySelector('[data-operation=review-answers]').click()");await asyncio.sleep(.3)
        assert fixture.q[0]['selected']==['All rows'] and fixture.q[0]['comments']=='Second duplicate'
        assert fixture.q[0]['source']['attributed_to']=='Framework user correction'
        before_duplicate=len(fixture.saved)
        await set_review(0,'retain');await set_review(1,'edit')
        await js("document.querySelector('[data-operation=review-answers]').click()");await asyncio.sleep(.1)
        assert len(fixture.saved)==before_duplicate
        assert 'Choose one decision' in await js("document.querySelector('#toast').textContent")
        await set_review(0,'unresolved');await set_review(1,'unresolved')
        await js("document.querySelector('[data-operation=review-answers]').click()");await asyncio.sleep(.3)
        await js("document.querySelector('[data-local=accept-matched]').closest('details').scrollIntoView({block:'start'});document.querySelector('#toast').textContent=''")
        await asyncio.sleep(.1)
        shot=await call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False})
        (LOGS/'request-receipt-review.png').write_bytes(base64.b64decode(shot['data']))
        results.append({'scenario':'receipt-review','route':'request/input','expected':'Visible complete answer fields; unresolved duplicates skipped; one explicit correction per current question'})
        # Question attachments preserve lane when removed through the shared operation.
        fixture.question_attachments=[{'id':'question-notes.txt','name':'question-notes.txt','path':'input/questions/attachments/question-notes.txt','size':24}]
        fixture.revision+=1
        await asyncio.sleep(2.7)
        await js("location.hash='questions'");await asyncio.sleep(.15)
        await js("document.querySelector('[data-operation=remove-attachment]').click()");await asyncio.sleep(.3)
        assert fixture.saved[-1]==('remove-attachment',{'id':'question-notes.txt','lane':'question'})
        assert not fixture.question_attachments
        # Selected run identity and explicit profile override reach the shared Resume operation.
        await js("location.hash='runs/OP-analysis'");await asyncio.sleep(.15)
        await js("(()=>{const e=document.querySelector('#run-profile');e.value='manual';e.dispatchEvent(new Event('change',{bubbles:true}));})()")
        await js("document.querySelector('[data-operation=resume]').click()");await asyncio.sleep(.3)
        assert fixture.saved[-1]==('resume',{'operation_id':'OP-analysis','profile':'manual'}),fixture.saved[-1]
        await js("location.hash='request/input'");await asyncio.sleep(.15)
        # Rich conflict view preserves local edits.
        await js("(()=>{let e=document.querySelector('#change-text');e.value='Conflicting local request';e.dispatchEvent(new Event('input',{bubbles:true}));})()")
        fixture.revision+=1
        await js("document.querySelector('[data-operation=\"save-draft\"]').click()")
        await asyncio.sleep(.3)
        assert 'Revision conflict' in await js("document.querySelector('#modal-title').textContent")
        await js("document.querySelector('[data-dialog=\"0\"]').click()")
        # Busy ownership disables form editors and every operation except Stop.
        fixture.busy=True;fixture.revision+=1
        await js("location.hash='request/input'");await asyncio.sleep(2.7)
        assert await js("[...document.querySelectorAll('[data-operation]')].filter(x=>!x.disabled).every(x=>x.dataset.operation==='stop')")
        assert await js("[...document.querySelectorAll('textarea,input[data-draft],select[data-draft]')].every(x=>x.disabled)")
        # Passive routes remain accessible while busy.
        for route in ['questions','settings/workspace','settings/profiles','settings/appearance','help']:
            await js('location.hash='+json.dumps(route));await asyncio.sleep(.1)
            assert await js("[...document.querySelectorAll('[data-operation]')].filter(x=>!x.disabled).every(x=>x.dataset.operation==='stop')"),route
        await js("document.querySelector('[data-operation=stop]').click()");await asyncio.sleep(.3)
        assert not fixture.busy
        # Meaningful empty, setup-pending, blocked, ready-to-close, and external-reservation views.
        for scenario,route,expected in [('empty','overview','No change request is open'),('setup','overview','waiting for a configured'),('blocked','overview','Deferred defect'),('ready','request/outcome','Ready to close'),('manual','request/implementation','Manual handoff')]:
            fixture.scenario=scenario;fixture.revision+=1
            await js('location.hash='+json.dumps(route));await asyncio.sleep(.1)
            await js("fetch('/api/status').then(()=>document.querySelector('[data-local=refresh]')?.click())")
            await asyncio.sleep(2.7)
            assert expected in await js("document.querySelector('#main').innerText"),(scenario,expected)
            if scenario=='ready':assert not await js("document.querySelector('[data-operation=close]').disabled")
            if scenario=='manual':assert await js("[...document.querySelectorAll('[data-operation]')].filter(x=>!x.disabled).every(x=>x.dataset.operation==='stop')")
            results.append({'scenario':scenario,'route':route,'expected':expected})
        fixture.scenario='active';fixture.revision+=1
        await asyncio.sleep(2.7)
        # Mobile drawer and 22px reflow.
        await call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':1,'mobile':True})
        await js("location.hash='settings/workspace';document.documentElement.style.fontSize='22px'");await asyncio.sleep(.2)
        assert not await js('document.documentElement.scrollWidth>innerWidth+2')
        await js("document.querySelector('[data-local=\"open-nav\"]').click()")
        assert await js("document.querySelector('#sidebar').classList.contains('open')")
        await call('Input.dispatchKeyEvent',{'type':'keyDown','key':'Escape','code':'Escape','windowsVirtualKeyCode':27})
        assert not await js("document.querySelector('#sidebar').classList.contains('open')")
        await js("document.querySelector('#toast').textContent=''")
        shot=await call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False})
        (LOGS/'mobile-workspace.png').write_bytes(base64.b64decode(shot['data']))
        assert not errors,errors
        (LOGS/'review.json').write_text(json.dumps({'fixture':'Synthetic browser-only workflow fixture, not real agent execution','browser':'Installed Google Chrome headless','routes':results,'checks':['All eight pages and six request tabs rendered','No page overflow at desktop size','Safe Markdown did not execute HTML','Explicit saved versus unsaved input','Navigation guard with keep editing','Revision conflict with preserved local draft','Stop-only busy operations and disabled editors across pages','Passive navigation while busy','Stop releases fixture execution','Resume dispatch uses selected operation identity and explicit profile','Real exchange helper validates checkbox/comments review and safe duplicate decisions','Question attachment removal retains question lane','Actual plan binding and change fields render','Mobile drawer Escape and 22px text reflow'],'javascript_errors':errors,'actions':fixture.saved},indent=2))
        print(json.dumps({'routes':len(results),'javascript_errors':len(errors),'result':'passed','evidence':str(LOGS)},indent=2))


def own_descendants():
    records = {}
    for item in Path('/proc').iterdir():
        if not item.name.isdigit():
            continue
        try:
            text = (item/'stat').read_text()
            fields = text[text.rfind(')')+2:].split()
            records[int(item.name)] = {'pid':int(item.name),'ppid':int(fields[1]),'start_ticks':fields[19],'state':fields[0]}
        except (OSError,ValueError,IndexError):
            pass
    parents = {os.getpid()}
    result = {}
    while True:
        extra = {pid:r for pid,r in records.items() if r['ppid'] in parents and pid not in result}
        if not extra:
            break
        result.update(extra)
        parents.update(extra)
    return result


def cleanup_browser(process):
    # A subreaper adopts detached/orphaned children. Identity checks prevent PID reuse kills.
    for _ in range(80):
        records=own_descendants()
        active={pid:r for pid,r in records.items() if r['state']!='Z'}
        for pid,record in active.items():
            identity=process_identity(pid)
            if identity and identity['start_ticks']==record['start_ticks']:
                try:os.kill(pid,signal.SIGKILL)
                except ProcessLookupError:pass
        try:process.wait(timeout=.05)
        except subprocess.TimeoutExpired:pass
        while True:
            try:
                pid,_=os.waitpid(-1,os.WNOHANG)
                if not pid:break
            except ChildProcessError:break
        if not own_descendants():
            return
        time.sleep(.025)
    raise RuntimeError('Browser descendants remained unconfirmed; fixture reservation was not released.')


def browser_child(config):
    from execution import _restrict
    deadline=time.monotonic()+10
    while True:
        try:
            record=json.loads(Path(config['ownership_record']).read_text())
            if record['identity']==process_identity(os.getpid()) and record['status']=='running':break
        except (OSError,ValueError,KeyError):pass
        if time.monotonic()>deadline:raise RuntimeError('Browser supervisor did not acknowledge ownership')
        time.sleep(.01)
    _restrict(config['paths'],True,allow_session_creation=True)
    os.execvpe(config['command'][0],config['command'],os.environ)


def main():
    if ctypes.CDLL(None).prctl(36,1,0,0,0)!=0:
        raise RuntimeError('Cannot establish a browser child-subreaper; no browser was launched')
    LOGS.mkdir(parents=True,exist_ok=True);BASE.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='b-',dir=BASE) as td:
        home=Path(td);(home/'.aih').mkdir();shutil.copy(REPO/'.aih/USER_GUIDE.md',home/'.aih/USER_GUIDE.md');shutil.copy(REPO/'.aih/README.md',home/'.aih/README.md')
        fixture=BrowserFixture(home);server=PortalServer(home,0,engine_factory=lambda:fixture)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        profile=home/'browser-profile';cache=home/'browser-cache';runtime=home/'t'
        for path in (profile,cache,runtime):path.mkdir()
        (cache/'fontconfig').mkdir()
        chrome='/opt/google/chrome/chrome'
        command=[chrome,'--headless=new','--no-sandbox','--disable-dev-shm-usage','--disable-gpu','--disable-background-networking','--disable-component-update','--disable-sync','--disable-extensions','--disable-breakpad','--disable-crash-reporter','--no-first-run','--no-default-browser-check','--no-proxy-server','--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE localhost, EXCLUDE 127.0.0.1','--disable-component-extensions-with-background-pages','--remote-debugging-port=0','--remote-allow-origins=http://localhost',f'--user-data-dir={profile}',f'--disk-cache-dir={cache}','about:blank']
        restriction={'paths':[('/',READ|EXECUTE,[Path('/').stat().st_dev,Path('/').stat().st_ino]),(str(home),READ|WRITE|MAKE_SOCK|MAKE_FIFO,[home.stat().st_dev,home.stat().st_ino]),('/dev/null',READ_FILE|WRITE_FILE,[Path('/dev/null').stat().st_dev,Path('/dev/null').stat().st_ino])],'network':True,'command':command,'ownership_record':str(home/'browser-ownership.json')}
        env={**os.environ,'TMPDIR':str(runtime),'XDG_CACHE_HOME':str(cache),'XDG_CONFIG_HOME':str(profile),'XDG_DATA_HOME':str(profile),'XDG_STATE_HOME':str(profile),'XDG_RUNTIME_DIR':str(runtime),'PYTHONDONTWRITEBYTECODE':'1','CHROME_LOG_FILE':str(home/'chrome.log')}
        stderr_file=(home/'chrome-stderr.log').open('wb')
        process=subprocess.Popen([sys.executable,'-B',str(Path(__file__).resolve()),'--browser-child',json.dumps(restriction)],env=env,cwd=home,start_new_session=True,stdout=subprocess.DEVNULL,stderr=stderr_file)
        (home/'browser-ownership.json').write_text(json.dumps({'identity':process_identity(process.pid),'status':'running'}))
        try:
            for _ in range(250):
                if (profile/'DevToolsActivePort').exists():break
                if process.poll() is not None:raise RuntimeError((home/'chrome-stderr.log').read_text())
                time.sleep(.1)
            if not (profile/'DevToolsActivePort').exists():raise RuntimeError('Chrome did not expose DevTools: '+(home/'chrome-stderr.log').read_text()[-6000:])
            port=(profile/'DevToolsActivePort').read_text().splitlines()[0]
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/json') as response:target=next(t for t in json.load(response) if t.get('type')=='page' and not t.get('url','').startswith('chrome-extension:'))
            try:
                asyncio.run(review(target['webSocketDebuggerUrl'],server,fixture,process))
            except Exception:
                print((home/'chrome-stderr.log').read_text()[-8000:],file=sys.stderr)
                raise
        finally:
            cleanup_browser(process)
            server.shutdown();server.server_close();stderr_file.close()
if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--browser-child':browser_child(json.loads(sys.argv[2]))
    else:main()
