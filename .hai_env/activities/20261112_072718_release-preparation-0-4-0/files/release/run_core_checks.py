from pathlib import Path
import os,subprocess,json,re,sys
root=Path(__file__).resolve().parents[5]
# Root above is the workspace: files/release -> Activity -> activities -> .hai_env -> root.
assert (root/'.hai').is_dir(),root
activity=root/'.hai_env/activities/00000000_000000_active'
work=activity/'files/release';scratch=activity/'files/test-work';scratch.mkdir(exist_ok=True);tmp=scratch/'tmp';tmp.mkdir(exist_ok=True)
env=os.environ.copy();env['TMPDIR']=str(tmp);env['PYTHONDONTWRITEBYTECODE']='1'
results=[]
for folder in ['startup','agents','configuration','activities','chronicles','runtime/tests']:
    args=[sys.executable,'-B','-m','unittest','discover','-s',str(root/'.hai/tools'/folder),'-p','test_*.py']
    r=subprocess.run(args,cwd=scratch,env=env,capture_output=True,text=True)
    text=r.stdout+r.stderr;label=folder.replace('/','-');(work/(label+'-tests.txt')).write_text(text)
    count=re.search(r'Ran (\d+) tests?',text);skipped=re.search(r'skipped=(\d+)',text)
    item={'suite':folder,'command':args,'returncode':r.returncode,'tests':int(count.group(1)) if count else None,'skipped':int(skipped.group(1)) if skipped else 0,'output':str((work/(label+'-tests.txt')).relative_to(root))}
    results.append(item);(work/'core-test-results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(item),flush=True)
    if r.returncode:raise SystemExit(r.returncode)
