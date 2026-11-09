import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import plan_contract as contract

ACTIVITY = '088c1e8e-caa9-4971-9328-cb742a4db998'


def sample_plan():
    info = {k: 'Evidence or explicit constraint.' for k in contract.PLAN_FIELDS}
    info.update(Format='hai-plan-v1', Activity=ACTIVITY, **{'Input revision': 'input-1', 'Decision revision': 'decision-1',
                'Mode': 'normal', 'Readiness': 'ready', 'Business readiness': 'passed'})
    return ('# Delivery plan\n\n## Execution contract\n\n' + '\n'.join('- '+k+': '+v for k,v in info.items()) + '''

## Acceptance criteria

| ID | Criterion | Verification |
| --- | --- | --- |
| A1 | Preserve Unicode input. | Named regression passes. |

## Plan overview

| Phase | Goal | Depends on | Expected result |
| --- | --- | --- | --- |
| 1 — Preserve input | Store exact text. | None | Exact readback. |

## Phase 1 — Preserve input

### Purpose

Preserve user input.

### Why now

Required before later reads.

### Visible result

Exact text available.

### Scope

One UTF-8 document.

### Actions

| Step | Action | Purpose or expected result |
| --- | --- | --- |
| 1.1 | Preserve exact text in notes.md. | No lost intent. |

| Task | Target | Operation | Depends on | Acceptance | Check |
| --- | --- | --- | --- | --- | --- |
| 1.1 | notes.md | Write supplied text without normalization. | None | A1 | Compare exact UTF-8 readback. |

### Affected files

notes.md

### Complete when

Exact readback passes.

## File inventory

| Path | Change | Purpose |
| --- | --- | --- |
| notes.md | Add | Preserve text. |
''')


def sample_assessment():
    blocks = []
    for title in contract.ASSESSMENT_SECTIONS:
        body = 'Current attributed evidence; no unresolved critical choices.'
        if title == 'Identity and input': body = '- Activity: '+ACTIVITY+'\n- Input revision: input-1\n- Decision revision: decision-1'
        if title == 'Readiness': body = '| Check | Status | Evidence |\n| --- | --- | --- |\n'+'\n'.join('| '+c+' | passed | Observed evidence for '+c+'. |' for c in contract.TECHNICAL_CHECKS)
        blocks.append('## '+title+'\n\n'+body)
    return '# Technical assessment\n\n'+'\n\n'.join(blocks)+'\n'


class PlanTests(unittest.TestCase):
    def test_standalone_plan_and_unicode(self):
        result = contract.validate(sample_plan().replace('No lost intent.', 'Български 日本語 intent.'))
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['tasks'], ['1.1'])
        self.assertEqual(result['semantic_verification'], 'not_performed')

    def test_required_fields_individually(self):
        for field in contract.PLAN_FIELDS:
            with self.subTest(field=field):
                text = '\n'.join(l for l in sample_plan().splitlines() if not l.startswith('- '+field+':'))
                self.assertFalse(contract.validate(text)['ok'])

    def test_identity_and_revisions(self):
        identity = {'Activity': ACTIVITY, 'Input revision': 'input-1', 'Decision revision': 'decision-1'}
        self.assertTrue(contract.validate(sample_plan(), expected=identity)['ok'])
        for key in identity:
            changed = copy.copy(identity);changed[key] = 'revised'
            self.assertFalse(contract.validate(sample_plan(), expected=changed)['ok'])
        self.assertFalse(contract.validate(sample_plan(), expected={})['ok'])

    def test_accelerated_does_not_bypass_readiness(self):
        text = sample_plan().replace('Mode: normal', 'Mode: accelerated')
        self.assertTrue(contract.validate(text)['ok'])
        self.assertFalse(contract.validate(text.replace('Business readiness: passed', 'Business readiness: blocked'))['ok'])
        self.assertFalse(contract.validate(text.replace('Readiness: ready', 'Readiness: blocked'))['ok'])

    def test_each_phase_section_is_required(self):
        for section in contract.PHASE_SECTIONS:
            with self.subTest(section=section):
                self.assertFalse(contract.validate(sample_plan().replace('### '+section, '### Wrong'))['ok'])

    def test_broken_action_contracts(self):
        for before,after in [(' | A1 | Compare', ' | A2 | Compare'), ('| None | A1 |', '| 9.1 | A1 |'),
                             ('| 1.1 | notes.md', '| 1.2 | notes.md'), ('| notes.md | Add', '| other.md | Add'),
                             ('| notes.md | Add', '| notes.md | Unknown'), ('| A1 | Preserve', '| invalid | Preserve')]:
            with self.subTest(after=after): self.assertFalse(contract.validate(sample_plan().replace(before,after))['ok'])

    def test_target_escape_and_duplicate_sections(self):
        for target in ['../outside.md','/tmp/out','a/../../b','C:\\tmp\\out','.git/config','a//b']:
            with self.subTest(target=target): self.assertFalse(contract.validate(sample_plan().replace('notes.md',target))['ok'])
        self.assertFalse(contract.validate(sample_plan()+'\n## File inventory\nDuplicate')['ok'])

    def test_fenced_examples_are_not_structure(self):
        text=sample_plan()+'\n```markdown\n## Execution contract\n```\n'
        self.assertTrue(contract.validate(text)['ok'])
        self.assertFalse(contract.validate(text+'```\nunclosed')['ok'])

    def test_legacy_and_placeholder_are_actionable(self):
        self.assertFalse(contract.validate('# Legacy plan\n\n## Old format\ntext')['ok'])
        self.assertFalse(contract.validate(sample_plan().replace('Evidence or explicit constraint.', 'TODO'))['ok'])

    def test_assessment_all_checks_and_order(self):
        text=sample_assessment();self.assertTrue(contract.validate(text,'assessment')['ok'])
        for check in contract.TECHNICAL_CHECKS:
            self.assertFalse(contract.validate(text.replace('| '+check+' | passed','| '+check+' | blocked'),'assessment')['ok'])
        self.assertFalse(contract.validate(text.replace('## Options','## Edge conditions'),'assessment')['ok'])

    def test_final_review_section_order_and_unknown_sections(self):
        plan=sample_plan();prefix,rest=plan.split('## Phase 1 — Preserve input',1)
        phase,inventory=rest.split('## File inventory',1)
        misplaced=prefix+'## File inventory'+inventory+'\n## Phase 1 — Preserve input'+phase
        self.assertFalse(contract.validate(misplaced)['ok'])
        self.assertFalse(contract.validate(plan+'\n## Unknown instructions\nextra')['ok'])
        self.assertTrue(contract.validate(plan+'\n## Risks\nDocumented risk.\n\n## References\nNo external semantics.')['ok'])

    def test_final_review_phase_dependencies_and_reasons(self):
        plan=sample_plan()
        for dependency in ['99: missing phase','1: self dependency','1','None, 99: invalid']:
            bad=plan.replace('text. | None | Exact readback.', 'text. | '+dependency+' | Exact readback.')
            self.assertFalse(contract.validate(bad)['ok'])
        prefix,rest=plan.split('## Phase 1 — Preserve input',1)
        phase,inventory=rest.split('## File inventory',1)
        prefix=prefix.replace('| 1 — Preserve input | Store exact text. | None | Exact readback. |',
                              '| 1 — Preserve input | Store exact text. | None | Exact readback. |\n| 2 — Verify input | Inspect text. | 1: stored text required | Exact match. |')
        second=phase.replace('1.1','2.1').replace('notes.md','checked.md').replace('| None | A1 |','| 1.1 | A1 |')
        two=prefix+'## Phase 1 — Preserve input'+phase+'\n## Phase 2 — Verify input'+second+'\n## File inventory'+inventory+'| checked.md | Add | Verification. |\n'
        self.assertTrue(contract.validate(two)['ok'],contract.validate(two))
        self.assertFalse(contract.validate(two.replace('1: stored text required','1: stored, 1: repeated'))['ok'])

    def test_inline_html_structure_is_unsupported(self):
        for html in ['<span></span>','- <!-- TODO -->','text <!-- hidden -->']:
            self.assertFalse(contract.validate(sample_plan().replace('Preserve user input.',html))['ok'])

    def test_cli_readonly_safe_paths_and_json(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as folder:
            root=Path(folder);p=root/'plan.md';p.write_text(sample_plan(),encoding='utf-8')
            before=p.read_bytes()
            cli=[sys.executable,'-B',str(Path(contract.__file__)), '--workspace',str(root),'--document','plan.md']
            result=subprocess.run(cli,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout)
            self.assertTrue(json.loads(result.stdout)['ok']);self.assertEqual(p.read_bytes(),before)
            expected=root/'current.json';expected.write_text('{"Activity":"a","Activity":"b"}')
            result=subprocess.run(cli+['--expected','current.json'],capture_output=True,text=True)
            self.assertEqual(result.returncode,2)
            (root/'linked.md').symlink_to(p)
            with self.assertRaises(ValueError): contract.safe_file(root,'linked.md')
            with self.assertRaises(ValueError): contract.safe_file(root,'../outside')
            os.link(p,root/'hard.md')
            with self.assertRaises(ValueError): contract.safe_file(root,'plan.md')


if __name__ == '__main__': unittest.main()
