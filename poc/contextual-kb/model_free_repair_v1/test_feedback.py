import asyncio
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'model_free_v1'))
import test_candidate as base
plan=base.plan
from feedback import RepairService

class FeedbackTests(base.CandidateTests):
    def setUp(self):
        super().setUp();self.repair=RepairService(self.service)
    def call(self,*args,**kwargs):return asyncio.run(self.repair.lookup(*args,**kwargs))
    def test_missing_plan_is_actionable_without_backend_lookup(self):
        packet,error=self.call('alpha')
        self.assertFalse(error);self.assertEqual('PLAN_REQUIRED',packet['issues'][0]['code'])
        self.assertEqual('needs_refinement',packet['status'])
    def test_missing_condition_then_repair(self):
        p=plan('How does alpha behave without beta?','without beta')
        p['formly_questions'].append(dict(question='What about alpha?',reason='Control'))
        p['condition_bindings'][0]['question_indexes']=[0,1]
        packet,error=self.call('Explain alpha without beta',plan=p)
        self.assertTrue(error);issue=packet['issues'][0]
        self.assertEqual('MISSING_DECLARED_CONDITION',issue['code'])
        self.assertEqual('/plan/formly_questions/1/question',issue['path'])
        self.assertEqual('without beta',issue['condition'])
        p['formly_questions'][1]['question']='What about alpha without beta?'
        packet,error=self.call('Explain alpha without beta',plan=p)
        self.assertFalse(error);self.assertEqual('ok',packet['status'])
    def test_invalid_index_and_source_are_specific(self):
        p=plan('alpha without beta','without beta');p['condition_bindings'][0]['question_indexes']=[9]
        packet,error=self.call('alpha without beta',plan=p)
        self.assertEqual('INVALID_QUESTION_INDEX',packet['issues'][0]['code'])
        p=plan('alpha without beta','without beta')
        packet,error=self.call('alpha',plan=p)
        self.assertEqual('UNGROUNDED_CONDITION',packet['issues'][0]['code'])
    def test_scope_conflict_is_repair_but_unsupported_is_stop(self):
        p=plan('alpha');p['library_constraints']['formly_version']='7'
        packet,error=self.call('alpha',plan=p,formly_version='6.3.12')
        self.assertTrue(error);self.assertEqual('SCOPE_CONFLICT',packet['issues'][0]['code'])
        packet,error=self.call('alpha',plan=p)
        self.assertFalse(error);self.assertEqual('unsupported_scope',packet['status'])
        self.assertEqual('stop',packet['next_action']['type'])
    def test_invalid_explicit_scope_points_to_explicit_argument(self):
        packet,error=self.call('alpha',plan=plan('alpha'),formly_version='bad')
        self.assertTrue(error)
        self.assertEqual('INVALID_SCOPE',packet['issues'][0]['code'])
        self.assertEqual('/formly_version',packet['issues'][0]['path'])
    def test_no_matches_is_not_nonexistence(self):
        packet,error=self.call('quuxUnseenToken',plan=plan('quuxUnseenToken'))
        self.assertFalse(error);self.assertEqual('no_evidence',packet['status'])
    def test_integrity_errors_are_not_plan_repairs(self):
        self.store.expected_sha='broken'
        with self.assertRaisesRegex(ValueError,'DB hash'):self.call('alpha',plan=plan('alpha'))

if __name__=='__main__':unittest.main()
