import importlib.util
from pathlib import Path
p=Path('hai_agents_library/agents/business-analyst/scripts/clarification.py')
spec=importlib.util.spec_from_file_location('clarification',p); c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
a='63c11143-eec4-487a-a7f1-57220a2d09e5'
def ev(id,kind,**kw): return dict(event_id=id,kind=kind,author='human',source='fixture',at='2026-11-08T00:00:00Z',**kw)
def q(id): return dict(id=id,question='Which?',impact='Affects outcome',options=[],recommended=None,other='___',status='unanswered')
l=''
for e in [ev('batch','questions',batch_id='B001',questions=[q('Q001'),q('Q002')]),ev('r1','response',question_id='Q001',response_number=1,raw='old1',parts={'answer':'old1'},supersedes=None),ev('r2','response',question_id='Q002',response_number=1,raw='old2',parts={'answer':'old2'},supersedes=None),ev('amb','unresolved',raw='new1 and new2',reason='ambiguous mapping',candidate_question_ids=['Q001','Q002']),ev('map1','revision',question_id='Q001',response_number=2,raw='new1 and new2',parts={'answer':'new1'},supersedes='r1',resolves_event_id='amb',mapping_text='new1 belongs to Q001, new2 belongs to Q002',mapped_question_ids=['Q001','Q002'])]: l=c.prepare(l,a,e)
state=c.validate(c.parse(l,a),a)
print('unresolved=',state['unresolved'],'effective=',{k:v['event_id'] for k,v in state['effective'].items()})
sections=('Intent','Effective decisions','Context','Outcomes','Scope','Exclusions','Constraints and assumptions','Acceptance criteria')
p='\n\n'.join('### '+h+'\n\nContent.' for h in sections)
try:
 c.validate_proposal(p,{'status':'pass'},l,a)
 raise AssertionError('partial mapping allowed proposal')
except ValueError as e:
 assert 'unresolved' in str(e); print('partial proposal held:',e)
l=c.prepare(l,a,ev('map2','revision',question_id='Q002',response_number=2,raw='new1 and new2',parts={'answer':'new2'},supersedes='r2',resolves_event_id='amb',mapping_text='new1 belongs to Q001, new2 belongs to Q002',mapped_question_ids=['Q001','Q002']))
assert c.validate(c.parse(l,a),a)['unresolved']==[]
print('complete proposal=',c.validate_proposal(p,{'status':'pass'},l,a)['status'])
events=c.parse(l,a)
for field, value, index in [('sequence',True,0),('sequence',1.0,0),('response_number',True,1),('response_number',1.0,1)]:
 from copy import deepcopy
 altered=deepcopy(events); altered[index][field]=value
 try: c.validate(altered,a)
 except ValueError: pass
 else: raise AssertionError(f'{field} accepted {value!r}')
print('boolean and float sequence/response numbers rejected')
altered=deepcopy(events); altered[-1]['mapped_question_ids']=['Q002']
try: c.validate(altered,a)
except ValueError as e: print('inconsistent targets rejected:',e)
else: raise AssertionError('inconsistent targets accepted')
