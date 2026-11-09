import sys,json,copy,os,subprocess
from pathlib import Path
base=Path(__file__).resolve().parent
scripts=base/'stage/.hai_env/agents'
sys.path[:0]=[str(scripts/'software-developer/scripts'),str(scripts/'solution-architect/scripts')]
import execution_contract as dev, test_execution_contract as df
import plan_contract as plan, test_plan_contract as pf
root=base/'independent-root';root.mkdir(exist_ok=True)
results={}
def check(name,actual,expected):
    results[name]={'actual':actual,'expected':expected,'passed':actual==expected}
def direct(body):
    return '# Direct work\n\n'+'\n\n'.join('## '+s+'\n\n'+body for s in ['Outcome','Scope','Constraints','Acceptance','Tasks','Verification','Documentation'])+'\n'
check('valid_direct',dev.preflight(root,df.DIRECT,df.context())['ok'],True)
for name,body in [('placeholder','- TODO\n- **TBD**'),('comment_only','<!-- TODO -->'),('list_comment','- <!-- TODO -->'),('inline_comment','TODO <!-- marker -->'),('empty_span','<span></span>')]:
 d=direct(body);check(name,dev.preflight(root,d,df.context(d))['ok'],False)
fenced=df.DIRECT.replace('# Direct work\n\n','# Direct work\n\n```markdown\n',1)+'\n```\n'
check('fenced_direct',dev.preflight(root,fenced,df.context(fenced))['ok'],False)
# Same inode outside fixture root but within assigned invocation area.
shared=base/'shared-inode.txt';shared.write_text('preserve baseline')
linked=root/'linked.txt'
if not linked.exists():os.link(shared,linked)
check('hardlink_unknown_containment',dev.permitted_write(root,{'path':'linked.txt','operation':'modify'},[]),False)
ctx=df.context();ctx['expected_checks'][0]['required']=False
check('optional_only_preflight',dev.preflight(root,df.DIRECT,ctx)['ok'],False)
e=df.evidence(ctx);e['checks'][0].update(required=False,status='failed')
check('optional_only_verified',dev.validate_evidence(e,ctx)['ok'],False)
ctx=df.context();ctx['writes']=[{'path':'.hai/rule.md','operation':'modify'}]
check('omitted_protected',dev.preflight(root,df.DIRECT,ctx)['ok'],False)
ctx=df.context();e=df.evidence(ctx);e['changes'][0]['path']='unplanned.txt'
check('unplanned_delivery',dev.validate_evidence(e,ctx)['ok'],False)
check('valid_standalone_plan',plan.validate(pf.sample_plan())['ok'],True)
check('unknown_plan_section',plan.validate(pf.sample_plan()+'\n## Unspecified work\n\nExtra.\n')['ok'],False)
check('nonexistent_phase_dependency',plan.validate(pf.sample_plan().replace('| None | Exact readback. |','| 99: depends on nonexistent output | Exact readback. |'))['ok'],False)
# Actual CLI exact-byte CRLF/Unicode hashing, files remain unchanged.
d=df.DIRECT.replace('Preserve exact submitted text.','Запази 日本語 exactly.').replace('\n','\r\n')
(root/'directive.md').write_bytes(d.encode('utf-8'))
(root/'context.json').write_text(json.dumps(df.context(d),ensure_ascii=False),encoding='utf-8')
snapshot={p.name:p.read_bytes() for p in root.iterdir() if p.is_file()}
r=subprocess.run([sys.executable,'-B',str(scripts/'software-developer/scripts/execution_contract.py'),'--workspace',str(root),'--directive','directive.md','--context','context.json'],capture_output=True,text=True)
check('crlf_unicode_cli',r.returncode,0)
check('read_only_cli',{p.name:p.read_bytes() for p in root.iterdir() if p.is_file()}==snapshot,True)
check('shared_inode_unmodified',shared.read_text()=='preserve baseline',True)
for name,row in results.items():print(name,'PASS' if row['passed'] else 'FAIL',row['actual'])
(base/'independent-regression-results.json').write_text(json.dumps(results,indent=2))
sys.exit(0 if all(r['passed'] for r in results.values()) else 1)
