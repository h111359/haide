from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import clarification as dialogue

REPO = Path(__file__).resolve().parents[4]
PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / '.hai/tools'))
from runtime import activities, packages, environment


class RuntimeDialogueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / '.hai/templates').mkdir(parents=True)
        shutil.copy(REPO / '.hai/templates/state.json', self.root / '.hai/templates/state.json')
        (self.root / '.hai_env').mkdir()
        (self.root / '.hai_env/agent_instructions.md').write_text('', encoding='utf-8')
        (self.root / '.hai_env/state.json').write_text(json.dumps({
            'state_format_version': 3, 'activities': {'location': '.hai_env/activities'},
            'features': {'chronicles': {'enabled': False, 'record_every_prompts': 5}},
            'integrations': {}}), encoding='utf-8')
        self.provenance = {'source': 'isolated fixture host', 'reason': 'BL-0011 behavior check'}
        created = self.call('create', initial_input='Original exact human request.\n', provenance=self.provenance)
        self.assertTrue(created['ok'], created)
        self.activity = created['result']['state']['activity_id']
        self.base = self.root / created['result']['path']
        self.path = self.base / 'decisions.md'

    def call(self, operation, **kwargs):
        return activities.handle(operation, self.root, kwargs, True)

    def event(self, identity, kind, **kwargs):
        return dict(event_id=identity, kind=kind, author='fixture-human' if kind != 'questions' else 'fixture-analyst',
                    source='explicit isolated fixture occurrence ' + identity, at='2026-11-08T00:00:00Z', **kwargs)

    def question(self, identity):
        return dict(id=identity, question='Missing audience changes acceptance.\nWho should use this?',
                    impact='Determines permissions and acceptance checks.',
                    options=[dict(label='A', text='Editors', checked=False), dict(label='B', text='Viewers', checked=False)],
                    recommended='A', other='___', status='unanswered')

    def batch(self, count=1):
        return self.event('batch-receipt-1', 'questions', batch_id='B001',
                          questions=[self.question(f'Q{i:03}') for i in range(1, count + 1)])

    def save(self, event, *, capability=True, corrupt_readback=False):
        # Simulated serialized host handshake, using the real runtime as the writer.
        if not capability:
            raise RuntimeError(str(self.path) + ': activity record capability unavailable')
        before, _ = dialogue.read_ledger(self.path, self.activity)
        candidate = dialogue.prepare(before, self.activity, event)
        if candidate != before:
            current, _ = dialogue.read_ledger(self.path, self.activity)
            if current != before:
                raise RuntimeError(str(self.path) + ': inspected predecessor changed')
            result = self.call('record', activity_id=self.activity,
                               artifacts=[dict(name='decisions.md', text=candidate, reason='append fixture event')],
                               log='Fixture event persistence; dependent work held until readback.', provenance=self.provenance)
            if not result['ok']:
                raise RuntimeError(str(self.path) + ': ' + json.dumps(result))
        actual, _ = dialogue.read_ledger(self.path, self.activity)
        if corrupt_readback:
            actual = actual.replace('Editors', 'Intruders')
        return dialogue.verify_readback(before, candidate, actual, self.activity, event['event_id'])

    def test_first_question_exact_readback_batch_display_and_unanswered_reuse(self):
        self.assertEqual(dialogue.read_ledger(self.path, self.activity), ('', []))
        self.assertFalse(self.path.exists())
        saved = self.save(self.batch(3))
        visible = dialogue.display(saved)
        self.assertIn('Q001: A [ ], B [ ], Other: ___', visible)
        self.assertIn('Q003', visible)
        self.assertIn('(Recommended)', visible)
        self.assertEqual(visible.count('Status: unanswered'), 3)
        before = self.path.read_bytes()
        self.save(self.batch(3))  # Same receipt on restart never re-appends.
        self.assertEqual(self.path.read_bytes(), before)
        events = dialogue.parse(before.decode(), self.activity)
        self.assertEqual(len(events), 1)
        self.assertEqual(dialogue.next_ids(before.decode(), self.activity), ('B002', 'Q004'))
        self.assertFalse((self.base / 'requirements.md').exists())

    def test_verbatim_multipart_answers_revision_and_restart(self):
        self.save(self.batch(2))
        raw = 'Q001: B; preserve  spaces\nQ002: Other: Екипът\n'
        first = self.event('answer-1-part1', 'response', question_id='Q001', response_number=1,
                           raw=raw, parts={'choice': 'B', 'explanation': 'preserve  spaces'}, supersedes=None)
        self.save(first)
        second = self.event('answer-1-part2', 'response', question_id='Q002', response_number=1,
                            raw=raw, parts={'Other': 'Екипът'}, supersedes=None)
        self.save(second)
        revision = self.event('answer-2', 'revision', question_id='Q001', response_number=2,
                              raw='Actually Q001: A\nKeep the explanation.',
                              parts={'choice': 'A', 'explanation': 'Keep the explanation.'}, supersedes='answer-1-part1')
        self.save(revision)
        before = self.path.read_text(encoding='utf-8')
        self.save(revision)
        self.assertEqual(before, self.path.read_text(encoding='utf-8'))
        state = dialogue.validate(dialogue.parse(before, self.activity), self.activity)
        self.assertEqual(state['effective']['Q001']['response_number'], 2)
        self.assertEqual(state['responses']['Q001'][0]['raw'], raw)
        self.assertEqual(state['effective']['Q002']['parts']['Other'], 'Екипът')
        self.assertFalse(state['unanswered'])
        revisions = list((self.base / 'files/revisions/decisions').iterdir())
        self.assertEqual(len(revisions), 3)
        self.assertTrue(before.startswith(revisions[0].read_text(encoding='utf-8')))

    def test_ambiguous_raw_answer_waits_for_actual_mapping(self):
        self.save(self.batch(2))
        unresolved = self.event('ambiguous-1', 'unresolved', raw='B please', reason='Question mapping unclear',
                                candidate_question_ids=['Q001', 'Q002'])
        self.save(unresolved)
        state = dialogue.validate(dialogue.parse(self.path.read_text(), self.activity), self.activity)
        self.assertEqual(state['unresolved'], ['ambiguous-1'])
        self.assertEqual(state['effective'], {})
        answer = self.event('mapped-1', 'response', question_id='Q002', response_number=1,
                            raw='B please', parts={'choice': 'B'}, supersedes=None,
                            resolves_event_id='ambiguous-1', mapping_text='I meant Q002.', mapped_question_ids=['Q002'])
        saved = self.save(answer)
        self.assertEqual(saved['raw'], 'B please')
        self.assertEqual(saved['mapping_text'], 'I meant Q002.')
        state = dialogue.validate(dialogue.parse(self.path.read_text(), self.activity), self.activity)
        self.assertEqual(state['unanswered'], ['Q001'])
        self.assertEqual(state['unresolved'], [])

    def test_invalid_ids_recommendation_preselection_and_revision_links(self):
        for mutate in (lambda e: e['questions'][0].update(id='Q002'),
                       lambda e: e['questions'][0]['options'][0].update(checked=True),
                       lambda e: e['questions'][0].update(recommended='C')):
            event = self.batch(); mutate(event)
            with self.assertRaises(ValueError):
                dialogue.prepare('', self.activity, event)
        self.save(self.batch())
        changed = self.batch(); changed['questions'][0]['question'] = 'Different question'
        with self.assertRaisesRegex(ValueError, 'event_id reused'):
            self.save(changed)
        revision = self.event('bad-revision', 'revision', question_id='Q001', response_number=1,
                              raw='A', parts={'choice': 'A'}, supersedes='not-saved')
        with self.assertRaisesRegex(ValueError, 'latest effective'):
            self.save(revision)
        blank = self.event('blank', 'response', question_id='Q001', response_number=1,
                           raw='', parts={'choice': ''}, supersedes=None)
        with self.assertRaises(ValueError):
            self.save(blank)
        state = dialogue.validate(dialogue.parse(self.path.read_text(), self.activity), self.activity)
        self.assertEqual(state['unanswered'], ['Q001'])

    def test_capability_read_write_and_verification_failures_stop_dependent_work(self):
        displayed = []
        with self.assertRaisesRegex(RuntimeError, 'decisions.md.*unavailable'):
            displayed.append(self.save(self.batch(), capability=False))
        self.assertFalse(self.path.exists())
        original = activities.write_bytes
        def fail(root, path, data, expected=None):
            if path.endswith('/decisions.md'):
                raise OSError('injected ledger write denied')
            return original(root, path, data, expected)
        with mock.patch.object(activities, 'write_bytes', side_effect=fail):
            with self.assertRaisesRegex(RuntimeError, 'decisions.md.*injected ledger write denied'):
                displayed.append(self.save(self.batch()))
        self.assertFalse(self.path.exists())
        self.save(self.batch())
        with mock.patch.object(Path, 'open', side_effect=OSError(str(self.path) + ': injected read denied')):
            with self.assertRaisesRegex(OSError, 'decisions.md.*injected read denied'):
                dialogue.read_ledger(self.path, self.activity)
        with self.assertRaisesRegex(ValueError, 'readback mismatch'):
            displayed.append(self.save(self.batch(), corrupt_readback=True))
        self.assertEqual(displayed, [])
        self.assertEqual(len(dialogue.parse(self.path.read_text(), self.activity)), 1)

    def test_partial_runtime_write_retains_ledger_and_prevents_display(self):
        original = activities.write_bytes
        def fail_log(root, path, data, expected=None):
            if path.endswith('/log.md'):
                raise OSError('injected log failure after ledger write')
            return original(root, path, data, expected)
        with mock.patch.object(activities, 'write_bytes', side_effect=fail_log):
            with self.assertRaisesRegex(RuntimeError, 'partial'):
                self.save(self.batch())
        self.assertTrue(self.path.exists())
        self.assertEqual(len(dialogue.parse(self.path.read_text(), self.activity)), 1)

    def test_multipart_revision_mapping_holds_proposal_until_every_target_is_saved(self):
        self.save(self.batch(2))
        for number in (1, 2):
            self.save(self.event(f'old-{number}', 'response', question_id=f'Q{number:03}', response_number=1,
                                 raw=f'Q{number:03}: A', parts={'choice': 'A'}, supersedes=None))
        self.save(self.event('ambiguous-change', 'unresolved', raw='Both should change to B.',
                             reason='Unclear which two questions.', candidate_question_ids=['Q001', 'Q002']))
        for number in (1, 2):
            mapped = self.event(f'mapped-change-{number}', 'revision', question_id=f'Q{number:03}', response_number=2,
                                raw='Both should change to B.', parts={'choice': 'B'}, supersedes=f'old-{number}',
                                resolves_event_id='ambiguous-change', mapping_text='Both Q001 and Q002.',
                                mapped_question_ids=['Q001', 'Q002'])
            self.save(mapped)
            ledger = self.path.read_text()
            state = dialogue.validate(dialogue.parse(ledger, self.activity), self.activity)
            self.assertEqual(state['unresolved'], ['ambiguous-change'] if number == 1 else [])
            if number == 1:
                with self.assertRaisesRegex(ValueError, 'unresolved dialogue'):
                    dialogue.validate_proposal('', {'status': 'pass'}, ledger, self.activity)
        self.assertEqual([state['effective'][q]['response_number'] for q in ('Q001', 'Q002')], [2, 2])

    def test_existing_crlf_decisions_are_preserved_as_exact_bytes(self):
        result = self.call('record', activity_id=self.activity,
                           artifacts=[dict(name='decisions.md', text='Prior unrelated decision.\r\nSecond line.\r\n', reason='fixture prefix')],
                           log='Initial unrelated decisions.', provenance=self.provenance)
        self.assertTrue(result['ok'], result)
        prefix = self.path.read_bytes()
        self.save(self.batch())
        self.assertTrue(self.path.read_bytes().startswith(prefix))

    def test_damaged_history_wrong_activity_and_event_marker_in_raw_text(self):
        self.save(self.batch())
        raw = '<!-- hai-clarification-event:v1 -->\n```json\nraw answer\n```'
        event = self.event('raw-markers', 'response', question_id='Q001', response_number=1,
                           raw=raw, parts={'Other': raw}, supersedes=None)
        self.assertEqual(self.save(event)['raw'], raw)
        saved = self.path.read_text()
        with self.assertRaises(ValueError):
            dialogue.parse(saved, '00000000-0000-0000-0000-000000000001')
        with self.assertRaisesRegex(ValueError, 'incomplete|differs'):
            dialogue.parse(saved[:-200] + '<!-- hai-clarification-event:v2 -->', self.activity)

    def test_ledger_survives_later_work_and_authorized_fixture_archival(self):
        self.save(self.batch())
        before = self.path.read_bytes()
        result = self.call('record', activity_id=self.activity,
                           artifacts=[dict(name='requirements.md', text='Proposed requirements, pending review.', reason='fixture later work')],
                           input_append='\nAttributed scope note; original retained.', log='Later work fixture.', provenance=self.provenance)
        self.assertTrue(result['ok'], result)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertTrue((self.base / 'input.md').read_text().startswith('Original exact human request.\n'))
        result = self.call('close', activity_id=self.activity, outcome='completed', archive_label='dialogue-fixture',
                           outcome_text='Isolated fixture complete; not a real product Activity.',
                           recording={'status': 'disabled', 'details': 'Explicit fixture-only disabled recording.'}, provenance=self.provenance)
        self.assertTrue(result['ok'], result)
        archived = self.root / result['result']['archive_path'] / 'decisions.md'
        self.assertEqual(archived.read_bytes(), before)
        self.assertEqual(len(dialogue.read_ledger(archived, self.activity)[1]), 1)

    def test_staged_source_package_and_empty_configuration_validate(self):
        shutil.copytree(REPO / '.hai', self.root / '.hai', dirs_exist_ok=True)
        target = self.root / '.hai_env/agents/business-analyst'
        shutil.copytree(PACKAGE, target)
        result = packages.handle('validate', self.root, {'definition': '.hai_env/agents/business-analyst/SKILL.md'}, False)
        self.assertTrue(result['ok'], result)
        result = environment.handle('configuration/read', self.root, {'agent': 'business-analyst'}, False)
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['result']['settings'], {})


class ReadinessProposalProtectionTests(unittest.TestCase):
    def setUp(self):
        self.convention = (PACKAGE / 'conventions/requirements-readiness.md').read_text(encoding='utf-8')
        self.items = dialogue.readiness_items(self.convention)
        self.checks = {key: dict(satisfied=True, evidence='Fixture evidence for ' + key) for key in self.items}

    def test_all_eight_categories_28_checks_pass_fail_and_scope_reassessment(self):
        self.assertEqual(len(self.items), 28)
        self.assertEqual([sum(i.startswith(f'R{c}.') for i in self.items) for c in range(1, 9)], [4, 3, 3, 4, 2, 4, 5, 3])
        self.assertEqual(dialogue.assess_readiness(self.items, self.checks)['status'], 'pass')
        for key in self.items:
            with self.subTest(item=key):
                changed = deepcopy(self.checks); changed[key] = dict(satisfied=False, evidence='Scope changed; pending decision.')
                result = dialogue.assess_readiness(self.items, changed)
                self.assertEqual(result['status'], 'fail')
                self.assertEqual(result['failed'], [key])
        self.assertEqual(dialogue.assess_readiness(self.items, self.checks, blockers=['undocumented critical conflict'])['status'], 'fail')

    def test_assumptions_deferrals_and_human_decision_limits(self):
        check = self.checks['R6.3']
        check.update(basis='assumption', resolves_uncertainty=True, requires_human_decision=False,
                     consequences_if_false='Scope must be reassessed.')
        self.assertEqual(dialogue.assess_readiness(self.items, self.checks)['status'], 'pass')
        check['requires_human_decision'] = True
        self.assertEqual(dialogue.assess_readiness(self.items, self.checks)['failed'], ['R6.3'])
        check.update(basis='deferral', requires_human_decision=False, resolves_uncertainty=False)
        self.assertEqual(dialogue.assess_readiness(self.items, self.checks)['status'], 'fail')

    def test_only_two_narrow_exemptions_and_no_blocker_bypass(self):
        cases = [dict(kind='internal_framework_upkeep', reason='Pure refactoring.', user_visible_change=False),
                 dict(kind='urgent_clear_defect', reason='Restore typo-broken flag.', urgent=True, clear=True, single_reversible_change=True)]
        for exemption in cases:
            self.assertEqual(dialogue.assess_readiness(self.items, {}, exemption=exemption)['status'], 'exempt')
            self.assertEqual(dialogue.assess_readiness(self.items, {}, exemption=exemption, blockers=['decision'])['status'], 'fail')
        for exemption in (dict(kind='internal_framework_upkeep', reason='New behavior.', user_visible_change=True),
                          dict(kind='urgent_clear_defect', reason='Large migration.', urgent=True, clear=True, single_reversible_change=False)):
            with self.assertRaises(ValueError):
                dialogue.assess_readiness(self.items, {}, exemption=exemption)

    def test_compatible_extensions_preserve_historical_review(self):
        old = dialogue.assess_readiness(self.items, self.checks)
        extended = self.convention.replace('### R2 — People', '- [ ] **R1.5 New evidence:** Evidence for a new intent concern.\n\n### R2 — People')
        extended = extended.replace('## Compatible extension', '### R9 — New category\n\nAdditional review evidence.\n\n- [ ] **R9.1 New check:** Evidence for the additional dimension.\n\n## Compatible extension')
        items = dialogue.readiness_items(extended)
        self.assertEqual(len(items), 30)
        self.assertEqual(dialogue.assess_readiness(items, self.checks)['failed'], ['R1.5', 'R9.1'])
        self.assertEqual(old['status'], 'pass')
        for damaged in (self.convention.replace('R1.1 ', 'R1.9 '), extended.replace('R9.1 ', 'R10.1 '),
                        extended.replace('R1.5 ', 'R1.6 ')):
            with self.assertRaises(ValueError):
                dialogue.readiness_items(damaged)

    def test_proposal_deeper_headings_no_overwrite_and_gate_hold(self):
        sections = ('Intent', 'Effective decisions', 'Context', 'Outcomes', 'Scope', 'Exclusions',
                    'Constraints and assumptions', 'Acceptance criteria')
        proposal = '\n\n'.join('### ' + s + '\n\nObservable fixture content for ' + s + '.' for s in sections)
        assessment = dialogue.assess_readiness(self.items, self.checks)
        activity = '00000000-0000-0000-0000-000000000001'
        result = dialogue.validate_proposal(proposal, assessment, '', activity)
        self.assertEqual(result['status'], 'ready_for_human_review')
        self.assertEqual(dialogue.validate_proposal(proposal, assessment, '', activity), result)
        with self.assertRaisesRegex(ValueError, 'headings'):
            dialogue.validate_proposal('## Request\n' + proposal, assessment, '', activity)
        with self.assertRaisesRegex(ValueError, 'readiness'):
            dialogue.validate_proposal(proposal, dict(status='fail'), '', activity)
        with self.assertRaisesRegex(ValueError, 'blockers'):
            dialogue.validate_proposal(proposal, assessment, '', activity, blockers=['unresolved'])

    def test_protection_baseline_authority_and_sorted_untouched_changes(self):
        before = {'.hai/preexisting.md': 'already dirty', '.hai/z.md': 'old', 'product.py': 'old'}
        after = dict(before, **{'.hai/z.md': 'new', '.hai/a.md': 'created', 'product.py': 'new'})
        result = dialogue.protection_check(before, after)
        self.assertEqual(result['unauthorized'], ['.hai/a.md', '.hai/z.md'])
        self.assertEqual(result['error'], 'ERROR: Protected framework modified without authorization; workflow stopped.')
        self.assertEqual(after['.hai/preexisting.md'], 'already dirty')
        self.assertTrue(dialogue.protection_check(before, after, ('.hai',))['ok'])
        self.assertEqual(after['.hai/z.md'], 'new')  # Never automatically reverted.


if __name__ == '__main__':
    unittest.main()
