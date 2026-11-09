"""Activity-owned one-off exact-commit packager; no publication effects."""
from pathlib import Path,PurePosixPath
import argparse,subprocess,tarfile,io,json,hashlib,datetime,zipfile,os,re
p=argparse.ArgumentParser();p.add_argument('--commit',required=True);args=p.parse_args()
root=Path.cwd().resolve();activity=root/'.hai_env/activities/00000000_000000_active';work=activity/'files/release';scratch=activity/'files/test-work'
commit=subprocess.check_output(['git','rev-parse','--verify',args.commit+'^{commit}'],text=True).strip()
assert re.fullmatch(r'[0-9a-f]{40}',commit)
raw=subprocess.check_output(['git','archive','--format=tar',commit,'--','.hai','LICENSE','README.md','INSTALL.md','release-notes'])
files={};modes={}
with tarfile.open(fileobj=io.BytesIO(raw),mode='r:') as archive:
    for entry in archive.getmembers():
        path=PurePosixPath(entry.name)
        assert not path.is_absolute() and '..' not in path.parts and '\\' not in entry.name,entry.name
        allowed=(path.parts[0]=='.hai' or entry.name in ['LICENSE','README.md','INSTALL.md'] or (path.parts[0]=='release-notes' and len(path.parts)==2 and path.suffix=='.md'))
        if entry.isdir():continue
        if not allowed:continue
        assert entry.isfile() and not entry.issym() and not entry.islnk(),entry.name
        assert not any(x in path.parts for x in ['.git','.hai_env','__pycache__']) and path.suffix not in ['.pyc','.pyo'],entry.name
        assert entry.name not in files,entry.name
        files[entry.name]=archive.extractfile(entry).read();modes[entry.name]=entry.mode
assert all(p in files for p in ['LICENSE','README.md','INSTALL.md','.hai/start.md','.hai/tools/hai.py','.hai/tools/configuration/configuration_tools.py','.hai/contracts/state.json','.hai/release-0.4.0.json'])
def strict_json(data):
    def pairs(items):
        result={}
        for key,value in items:
            assert key not in result,'Duplicate JSON key: '+key;result[key]=value
        return result
    return json.loads(data,object_pairs_hook=pairs,parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
manifest=strict_json(files['.hai/release-0.4.0.json']);state=strict_json(files['.hai/contracts/state.json'])
assert set(manifest)=={'version','contracts'} and manifest['version']=='0.4.0' and set(manifest['contracts'])=={'environment_state'}
assert manifest['contracts']['environment_state']==state and set(state)=={'current_state_format_version','supported_state_format_versions'}
assert type(state['current_state_format_version']) is int and state['current_state_format_version']>0
versions=state['supported_state_format_versions'];assert versions and all(type(v) is int and v>0 for v in versions) and len(versions)==len(set(versions)) and state['current_state_format_version'] in versions
assert [x for x in files if re.fullmatch(r'\.hai/release-[^/]+\.json',x)]==['.hai/release-0.4.0.json']
assert not any(x.startswith(('hai_agents_library/','.hai_env/','.git/')) for x in files)
assert not any(x.startswith('release-notes/') and x.endswith('.json') for x in files)
# Verify local documentation targets against actual package membership, not worktree files.
def visible(text):
    out=[];fence=None
    for line in text.splitlines():
        m=re.match(r'^\s*(`{3,}|~{3,})(.*)$',line)
        if m:
            token,tail=m.groups()
            if fence is None:fence=token
            elif token[0]==fence[0] and len(token)>=len(fence) and not tail.strip():fence=None
        elif fence is None:out.append(line)
    return '\n'.join(out)
links=0
for name,data in files.items():
    if not name.endswith('.md'):continue
    for target in re.findall(r'\]\(([^)]+)\)',visible(data.decode('utf-8'))):
        if '://' in target or target.startswith('mailto:'):continue
        filename,_,anchor=target.partition('#');parts=list(PurePosixPath(name).parent.parts)
        for part in PurePosixPath(filename).parts if filename else []:
            if part=='..':assert parts;parts.pop()
            elif part!='.':parts.append(part)
        dest='/'.join(parts) if filename else name
        assert dest in files,(name,target,dest)
        if anchor and dest.endswith('.md'):
            slugs=[];counts={}
            for title in re.findall(r'^#{1,6} (.+)$',visible(files[dest].decode('utf-8')),re.M):
                slug=re.sub(r'[^\w\- ]','',title.replace('`','').lower()).replace(' ','-');n=counts.get(slug,0);counts[slug]=n+1;slugs.append(slug+('-'+str(n) if n else ''))
            assert anchor in slugs,(name,target)
        links+=1
out=root/'dist/hai-0.4.0.zip';checksum=root/'dist/hai-0.4.0.zip.sha256'
for destination in [out,checksum]:
    assert destination.resolve().is_relative_to(root) and not destination.exists(),destination
    assert subprocess.run(['git','check-ignore','--quiet',str(destination.relative_to(root))]).returncode==0
out.parent.mkdir(exist_ok=True)
assert not out.parent.is_symlink()
time=int(subprocess.check_output(['git','show','-s','--format=%ct',commit],text=True).strip())
stamp=datetime.datetime.fromtimestamp(time,datetime.timezone.utc);stamp=max(stamp,datetime.datetime(1980,1,1,tzinfo=datetime.timezone.utc))
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as bundle:
    for name,data in sorted(files.items()):
        info=zipfile.ZipInfo(name,stamp.timetuple()[:6]);info.create_system=3;info.external_attr=(modes[name]&0xffff)<<16;info.compress_type=zipfile.ZIP_DEFLATED
        bundle.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(out) as bundle:
    assert bundle.testzip() is None
    assert bundle.namelist()==sorted(files)
    for name,data in files.items():assert bundle.read(name)==data,name
unpacked=scratch/('unpacked-0.4.0-'+commit[:12]);unpacked.mkdir()
for name,data in files.items():
    dest=unpacked/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);dest.chmod(modes[name]&0o777)
digest=hashlib.sha256(out.read_bytes()).hexdigest()
with checksum.open('x',encoding='utf-8') as f:f.write(digest+'  '+out.name+'\n')
result={'version':'0.4.0','status':'packaged; validation of extracted tree follows','source_commit':commit,'published_baseline_commit':'f35b69b7f16d29b06bbfdc66c0022a306087ad90','asset':str(out.relative_to(root)),'sha256':digest,'bytes':out.stat().st_size,'entries':len(files),'documentation_links_checked':links,'contracts':manifest['contracts'],'unpacked':str(unpacked.relative_to(root)),'file_sha256':{name:hashlib.sha256(data).hexdigest() for name,data in sorted(files.items())},'exclusions_verified':['.hai_env','hai_agents_library','.git','historical manifests','caches/generated output']}
(work/'package-inspection.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='file_sha256'},indent=2))
