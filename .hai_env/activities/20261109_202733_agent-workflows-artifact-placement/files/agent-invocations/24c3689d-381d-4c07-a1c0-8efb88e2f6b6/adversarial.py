import sys,json,copy
from pathlib import Path
base=Path(__file__).resolve().parent
scripts=base/'stage/.hai_env/agents'
sys.path[:0]=[str(scripts/'software-developer/scripts'),str(scripts/'solution-architect/scripts')]
import execution_contract as dev, test_execution_contract as df
import plan_contract as plan, test_plan_contract as pf
root=base/'adversarial-root';root.mkdir(exist_ok=True)
results={}
fenced=df.DIRECT.replace('# Direct work\n\n','# Direct work\n\n```markdown\n',1)+'\n```\n'
results['fenced_direct_sections']=dev.preflight(root,fenced,df.context(fenced))
comments='# Direct work\n\n'+'\n\n'.join('## '+s+'\n\n<!-- TODO -->' for s in ['Outcome','Scope','Constraints','Acceptance','Tasks','Verification','Documentation'])+'\n'
results['comment_only_direct']=dev.preflight(root,comments,df.context(comments))
wrong_order=pf.sample_plan().split('## File inventory')[0]
inventory='## File inventory'+pf.sample_plan().split('## File inventory')[1]
wrong_order=wrong_order.replace('## Phase 1',inventory+'\n## Phase 1',1)
results['inventory_before_phases']=plan.validate(wrong_order)
results['unknown_plan_section']=plan.validate(pf.sample_plan()+'\n## Unspecified work\n\nImplement additional scope.\n')
results['invalid_phase_dependency']=plan.validate(pf.sample_plan().replace('| None | Exact readback. |','| 99 | Exact readback. |'))
for key,value in results.items():print(key,json.dumps(value))
(base/'adversarial-results.json').write_text(json.dumps(results,indent=2))
