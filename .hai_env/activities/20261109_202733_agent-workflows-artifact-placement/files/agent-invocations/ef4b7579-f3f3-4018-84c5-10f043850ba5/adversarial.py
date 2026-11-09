import os,sys,tempfile
from pathlib import Path
base=Path(__file__).parent
scripts=base/'stage/.hai_env/agents/software-developer/scripts'
sys.path.insert(0,str(scripts))
import test_execution_contract as fixture
import execution_contract as c
root=base/'fixture_root';root.mkdir(exist_ok=True)
placeholder='# Direct work\n\n'+'\n\n'.join('## '+s+'\n\n- TODO\n- TBD' for s in ['Outcome','Scope','Constraints','Acceptance','Tasks','Verification','Documentation'])+'\n'
print('placeholder:',c.preflight(root,placeholder,fixture.context(placeholder)))
no_title=fixture.DIRECT.split('\n',2)[2]
print('no H1:',c.preflight(root,no_title,fixture.context(no_title)))
other=base/'outside_fixture_root.txt';other.write_text('shared inode')
link=root/'linked.txt'
if not link.exists():os.link(other,link)
print('hardlink write:',c.permitted_write(root,{'path':'linked.txt','operation':'modify'},[]),'link_count:',link.stat().st_nlink)
ctx=fixture.context();ctx['expected_checks'][0]['required']=False
ev=fixture.evidence(ctx);ev['checks'][0].update(required=False,status='failed')
print('failed optional sole acceptance check preflight:',c.preflight(root,fixture.DIRECT,ctx))
print('failed optional sole acceptance check verified evidence:',c.validate_evidence(ev,ctx))
