"""Standalone typed test/Git runner using the shared Linux confinement primitives.

No installed core or AIH lifecycle/product-state path is used. Runtime and output
locations come exclusively from the caller's validated invocation contract.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import json
import configparser
import re
from urllib.parse import urlparse
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import time

from execution import _restrict, confinement_diagnostics, READ, WRITE, WRITE_FILE, READ_FILE, EXECUTE, stop_process, process_identity
from storage import sanitize


def execute(contract, data, workspace, operation):
    try:
        from skill_helpers import ContractError, digest, now
    except ModuleNotFoundError:
        from helper import ContractError, digest, now
    diagnostics=confinement_diagnostics()
    if not diagnostics['available']:
        raise ContractError(diagnostics['reason'])
    expected_skills={'test-and-verify','implement-plan'} if operation=='run-test' else {'git-workflow'}
    if contract['skill'] not in expected_skills:
        raise ContractError('Selected package does not own this typed execution capability')
    required_effect='test-execution' if operation=='run-test' else 'git-'+data.get('action','')
    if required_effect not in contract['effects']:
        raise ContractError('The invoking user must explicitly authorize effect '+required_effect)
    runtime=contract.get('runtime')
    if not runtime:
        raise ContractError('An explicit root-qualified runtime directory is required')
    runtime_path=workspace.resolve(runtime,write=True)
    if '.aih_product' in runtime_path.parts or '.aih' in runtime_path.parts:
        raise ContractError('Executable runtime/cache effects must remain outside core/product state')
    # The initialization marker creates the declared runtime through safe helper
    # directory traversal. No runtime is inferred outside the invocation scope.
    marker={'root':runtime['root'],'path':runtime['path'].rstrip('/')+'/owner.json'}
    env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1','HOME':str(runtime_path),'TMPDIR':str(runtime_path),'TEMP':str(runtime_path),'TMP':str(runtime_path),'XDG_CACHE_HOME':str(runtime_path),'XDG_CONFIG_HOME':str(runtime_path),'XDG_DATA_HOME':str(runtime_path),'XDG_STATE_HOME':str(runtime_path)}
    writes=[runtime]
    credential_reads=[]
    credential_values=[]
    network=False
    pre_commands=[]
    timeout=data.get('timeout',120)
    if type(timeout) is not int or not 1<=timeout<=3600:
        raise ContractError('Execution timeout must be 1..3600 seconds')
    if operation=='run-test':
        for field in ('id','runner','environment','working_directory','source_paths','write_paths','prerequisites','isolation','cleanup','authorization','workspace_revision'):
            if field not in data:
                raise ContractError('Test-run contract missing '+field)
        if data['environment']!='python3' or data['isolation']!='linux-landlock-seccomp' or data['workspace_revision']!=contract['workspace_revision']:
            raise ContractError('Unsupported/stale test environment or isolation')
        if data['authorization']!=contract['authorization']['instruction_reference']:
            raise ContractError('Test authorization does not match the invocation instruction')
        if data['cleanup']!='retain':
            raise ContractError('Portable runner retains evidence/runtime; declare cleanup=retain')
        if not data['source_paths']:
            raise ContractError('A registered test source is required')
        for prereq in data['prerequisites']:
            if set(prereq)!={'file'} or not workspace.resolve(prereq['file']).is_file():
                raise ContractError('A test prerequisite is unavailable or unsupported')
        cwd=workspace.resolve(data['working_directory'])
        sources=[workspace.resolve(ref) for ref in data['source_paths']]
        if any('.aih_product' in path.parts for path in sources+[cwd]):
            raise ContractError('Product state is inert and cannot supply executable tests')
        writes+=data['write_paths']
        if data['runner']=='python-script' and len(sources)==1 and sources[0].is_file():
            command=[sys.executable,'-B',str(sources[0])]
        elif data['runner']=='python-unittest' and len(sources)==1 and sources[0].is_dir():
            pattern=data.get('pattern','test*.py')
            if not isinstance(pattern,str) or '/' in pattern or '\\' in pattern:
                raise ContractError('Invalid unittest filename pattern')
            command=[sys.executable,'-B','-m','unittest','discover','-s',str(sources[0]),'-p',pattern,'-v']
        else:
            raise ContractError('Use a typed Python script/unittest contract with one runnable source')
    else:
        if contract['authorization']['mode']!='git':
            raise ContractError('Git requires explicit Git operation authority')
        executable=shutil.which('git')
        if not executable:
            raise ContractError('Git is unavailable; install the declared prerequisite independently')
        cwd=workspace.resolve(data['repository'])
        gitdir=cwd/'.git'
        if not gitdir.is_dir() or gitdir.is_symlink():
            raise ContractError('Portable Git requires an ordinary local .git directory; linked worktrees need a separately configured confined adapter')
        workspace._reject_links(gitdir)
        # Prevent repository object/config indirections outside its declared tree.
        for marker_path in ('commondir','objects/info/alternates'):
            if (gitdir/marker_path).exists():
                raise ContractError('Git object/common-directory indirection needs explicit separate confined configuration')
        config_path=gitdir/'config'
        settings=configparser.RawConfigParser(strict=False)
        if config_path.is_file():
            try:
                settings.read_string(config_path.read_text(encoding='utf-8'))
            except (configparser.Error,UnicodeError) as exc:
                raise ContractError('Cannot validate repository configuration: '+str(exc))
        if any(section.casefold().startswith(('include','credential')) for section in settings.sections()):
            raise ContractError('Repository includes/credential helpers must be removed or reviewed through an independently operated tool; they are not executed by this runner')
        env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null',GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',GIT_ASKPASS='/bin/false',GIT_PAGER='cat',GIT_SSH_COMMAND='/bin/false')
        command=[str(Path(executable).resolve()),'-c','core.hooksPath=/dev/null','-c','core.fsmonitor=false','-c','commit.gpgsign=false','-c','tag.gpgsign=false','-c','credential.helper=','-c','protocol.allow=never','-c','protocol.https.allow=always','-c','http.followRedirects=false','-C',str(cwd)]
        for section in settings.sections():
            if section.startswith('filter "') and section.endswith('"'):
                filter_name=section[8:-1]
                if not re.fullmatch(r'[A-Za-z0-9_.-]+',filter_name):
                    raise ContractError('Unsupported filter identity')
                command[1:1]=['-c',f'filter.{filter_name}.clean=','-c',f'filter.{filter_name}.smudge=','-c',f'filter.{filter_name}.process=','-c',f'filter.{filter_name}.required=false']
        action=data.get('action')
        if action=='status':command+=['status','--porcelain=v1','--untracked-files=normal']
        elif action=='diff':command+=['diff','--no-ext-diff','--no-textconv','--']
        elif action=='log':command+=['log','-10','--format=%h %s']
        elif action in ('branch','commit','push'):
            # Registration does not authorize mutation: this gitdir must also
            # appear within the initiating contract's explicit writable scope.
            repository_ref=data['repository']
            git_ref={'root':repository_ref['root'],'path':repository_ref['path'].rstrip('/')+'/.git'}
            workspace.resolve(git_ref,write=True)
            writes.append(git_ref)
            if action in ('branch','push'):
                branch=data.get('branch','')
                if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_./-]{0,99}',branch) or '..' in branch or branch.endswith(('.','/','.lock')) or '//' in branch:
                    raise ContractError('Specify a non-destructive literal branch name')
            if action=='branch':
                command+=['branch','--',branch]
            elif action=='commit':
                message=data.get('message','')
                if not isinstance(message,str) or not message.strip() or len(message)>10000:
                    raise ContractError('Commit requires an explicit nonempty message up to 10,000 characters')
                from contracts import screen
                screen(message,'commit message')
                paths=data.get('paths',[])
                if not paths:
                    raise ContractError('Commit must identify explicit root-qualified files; unrelated index content is excluded')
                selected=[]
                for ref in paths:
                    target=workspace.resolve(ref)
                    try:
                        relative=target.relative_to(cwd)
                    except ValueError:
                        raise ContractError('Commit file is outside the selected repository')
                    if '.git' in relative.parts or not target.is_file():
                        raise ContractError('Commit must select existing ordinary working-tree files')
                    selected.append(relative.as_posix())
                for key,envkey in [('author_name','GIT_AUTHOR_NAME'),('author_email','GIT_AUTHOR_EMAIL')]:
                    value=data.get(key,'')
                    if not isinstance(value,str) or not value.strip() or any(c in value for c in '\r\n\0'):
                        raise ContractError('Record explicit commit author_name and author_email')
                    env[envkey]=value
                    env[envkey.replace('AUTHOR','COMMITTER')]=value
                # --only restricts the commit to these files and preserves
                # unrelated staged changes. Git writes temporary indexes only in
                # the explicitly authorized repository metadata directory.
                pre_commands.append([*command,'add','--intent-to-add','--',*selected])
                command+=['commit','--only','-m',message,'--',*selected]
            else:
                if contract['authorization'].get('network') is not True:
                    raise ContractError('Push requires explicit network/publication authorization in the invocation')
                remote=data.get('remote','')
                if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}',remote):
                    raise ContractError('Push requires an explicitly selected configured remote')
                section='remote "'+remote+'"'
                if not settings.has_section(section) or not settings.has_option(section,'url'):
                    raise ContractError('Selected Git remote is not configured')
                remote_url=settings.get(section,'pushurl',fallback=settings.get(section,'url'))
                parsed=urlparse(remote_url)
                if parsed.scheme!='https' or not parsed.hostname or parsed.username or parsed.password or remote_url!=data.get('expected_url'):
                    raise ContractError('Push requires the explicitly reviewed matching HTTPS URL without embedded credentials; SSH/custom helpers use an independently operated tool boundary')
                for section_name in settings.sections():
                    if section_name.startswith(('url "','http "')):
                        raise ContractError('URL rewriting and URL-scoped HTTP settings require explicit independent review')
                env_configs=[]
                auth_env=data.get('authorization_header_env')
                if auth_env:
                    if not re.fullmatch(r'[A-Z][A-Z0-9_]*',auth_env) or auth_env not in os.environ:
                        raise ContractError('The declared authorization-header environment reference is unavailable')
                    header=os.environ[auth_env]
                    if not header.startswith('Authorization: ') or any(c in header for c in '\r\n\0'):
                        raise ContractError('Authentication environment must contain one Authorization header; no value was retained')
                    env_configs.append(('http.extraHeader',header))
                    credential_values.extend([header,header.split(':',1)[1].strip(),header.rsplit(' ',1)[-1]])
                for field,key in [('tls_ca_file','http.sslCAInfo'),('tls_certificate','http.sslCert'),('tls_key','http.sslKey')]:
                    if data.get(field):
                        credential=Path(data[field])
                        if not credential.is_absolute() or not credential.is_file():
                            raise ContractError('Credential material must be an explicit existing absolute file')
                        workspace._reject_links(credential)
                        credential_reads.append(str(credential.resolve()))
                        env_configs.append((key,str(credential.resolve())))
                for index,(key,value) in enumerate(env_configs):
                    env['GIT_CONFIG_KEY_'+str(index)]=key;env['GIT_CONFIG_VALUE_'+str(index)]=value
                env['GIT_CONFIG_COUNT']=str(len(env_configs))
                network=True
                # No force, delete, wildcard, mirror, tags, or implicit branch
                # expansion. The user selected one exact non-destructive refspec.
                command+=['push','--porcelain','--',remote_url,'refs/heads/'+branch+':refs/heads/'+branch]
        else:
            raise ContractError('Supported typed Git actions: status, diff, log, branch, commit, push. Pull requests require an independently operated authorized tool; no PR or publication follows automatically.')
    if not cwd.is_dir():
        raise ContractError('Working directory is unavailable')
    workspace.write(marker,json.dumps({'invocation':contract['id'],'created':now(),'effects':required_effect}),exclusive=True)
    rules=[]
    for root in workspace.roots.values():rules.append((str(root['canonical']),READ))
    for ref in writes:
        target=workspace.resolve(ref,write=True)
        if not target.exists():raise ContractError('Declared write directory must exist; prepare it through validated scoped edits')
        if target.is_dir():
            for directory, dirs, files in os.walk(target,followlinks=False):
                for name in dirs+files:workspace._reject_links(Path(directory,name))
        rules.append((str(target),READ|WRITE))
    # Installed host runtimes/libraries are invocation prerequisites, not product
    # inspection authority. Credential/user-home directories are never added.
    prerequisites=['/usr','/lib','/lib64','/bin',sys.prefix,str(Path(sys.executable).resolve()),'/dev/null','/dev/urandom','/etc/ld.so.cache','/etc/ld.so.conf','/etc/localtime']
    if network:prerequisites+=['/etc/ssl','/etc/resolv.conf','/etc/hosts','/etc/nsswitch.conf']
    for path in prerequisites:
        target=Path(path)
        if target.exists():rules.append((str(target.resolve()),READ|EXECUTE))
    for path in credential_reads:rules.append((path,READ_FILE))
    rules.append(("/dev/null",READ_FILE|WRITE_FILE))
    pinned=[]
    for path,rights in rules:
        target_stat=os.stat(path)
        pinned.append((path,rights,[target_stat.st_dev,target_stat.st_ino]))
    started=now();start=time.monotonic()
    steps=[];status='exited';termination=True;stdout='';stderr='';returncode=None
    progress_ref={'root':runtime['root'],'path':runtime['path'].rstrip('/')+'/progress.json'}
    def scrub(value):
        for sensitive in credential_values:
            if len(sensitive)>=4:value=value.replace(sensitive,'[redacted declared credential]')
        return sanitize(value)
    for index,step_command in enumerate([*pre_commands,command],1):
        workspace.write(progress_ref,json.dumps({'invocation':contract['id'],'step':index,'status':'starting','completed_steps':steps}))
        process=subprocess.Popen(step_command,cwd=cwd,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True,preexec_fn=lambda:_restrict(pinned,network))
        identity=process_identity(process.pid)
        try:
            out,err=process.communicate(timeout=max(1,timeout-(time.monotonic()-start)))
        except subprocess.TimeoutExpired:
            stopped=stop_process(identity);termination=stopped.get('confirmed',False)
            if not termination:
                raise ContractError('Process termination uncertain; retain runtime ownership and reconcile before another invocation')
            out,err=process.communicate(timeout=5);status='timeout'
        from execution import _group_alive
        if _group_alive(identity['pgid']) if identity else False:
            termination=stop_process(identity).get('confirmed',False)
        returncode=process.returncode
        steps.append({'sequence':index,'command':step_command,'returncode':returncode,'termination_confirmed':termination,'stdout':scrub(out),'stderr':scrub(err)})
        workspace.write(progress_ref,json.dumps({'invocation':contract['id'],'step':index,'status':'completed' if returncode==0 and termination else 'incomplete','completed_steps':steps}))
        stdout+=out;stderr+=err
        if returncode!=0 or status!='exited' or not termination:break
    collected=None
    if operation=='run-test' and data['runner']=='python-unittest':
        match=re.search(r'\bRan (\d+) tests?\b',stderr)
        collected=int(match.group(1)) if match else 0
    passed=returncode==0 and status=='exited' and termination and collected!=0
    return {'schema_version':'1.0','invocation':contract['id'],'operation':operation,'task_id':data.get('task_id'),'command':command,'started':started,'completed':now(),'elapsed_seconds':round(time.monotonic()-start,4),'process_status':status,'returncode':returncode,'steps':steps,'status':'passed' if passed else 'blocked' if collected==0 else 'failed','tests_collected':collected,'termination_confirmed':termination,'stdout':scrub(stdout),'stderr':scrub(stderr),'workspace_revision':contract['workspace_revision'],'runtime':runtime,'usage':None,'evidence_boundary':'Actual confined process result; semantic acceptance and reconstruction require their own evidence.'}
