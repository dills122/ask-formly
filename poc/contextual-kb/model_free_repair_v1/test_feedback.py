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

    def test_explicit_scope_omission_then_repair_preserves_request(self):
        request='For Formly 6.3.12 with Material, guarantee that all controls pass keyboard and screen-reader testing in every browser.'
        p=plan(request)
        packet,error=self.call(request,plan=p)
        self.assertTrue(error)
        self.assertEqual('needs_refinement',packet['status'])
        self.assertEqual(['MISSING_SCOPE_METADATA']*2,[i['code'] for i in packet['issues']])
        self.assertEqual(['/plan/library_constraints/formly_version','/plan/library_constraints/ui_adapter'],[i['path'] for i in packet['issues']])
        self.assertEqual({'formly_version':None,'ui_adapter':None},p['library_constraints'])
        self.assertNotIn('facts',packet)
        p['library_constraints']={'formly_version':'6.3.12','ui_adapter':'material'}
        packet,error=self.call(request,plan=p)
        self.assertFalse(error)
        self.assertEqual(request,packet['request'])
        self.assertEqual('material',packet['ui_adapter'])

    def test_missing_scope_is_rejected_before_backend_or_settings(self):
        self.store.expected_sha='broken'
        packet,error=self.call('Use Formly 6.3.12 with Material. Explain alpha.',plan=plan('alpha'),project_id='example',formly_version='6.3.12',ui_adapter='material')
        self.assertTrue(error)
        self.assertEqual('MISSING_SCOPE_METADATA',packet['issues'][0]['code'])

    def test_partial_scope_only_requests_missing_field(self):
        p=plan('alpha');p['library_constraints']['formly_version']='6.3.12'
        packet,error=self.call('In Formly 6.3.12 with Material, explain alpha.',plan=p)
        self.assertTrue(error)
        self.assertEqual(['/plan/library_constraints/ui_adapter'],[i['path'] for i in packet['issues']])

    def test_unsupported_explicit_scope_still_stops_after_metadata_repair(self):
        for version,adapter in [('7.0.0','Material'),('6.3.12','Bootstrap')]:
            with self.subTest(version=version,adapter=adapter):
                request=f'In Formly {version} with {adapter}, explain alpha.'
                p=plan('alpha')
                packet,error=self.call(request,plan=p)
                self.assertTrue(error);self.assertEqual('needs_refinement',packet['status'])
                p['library_constraints']={'formly_version':version,'ui_adapter':adapter}
                packet,error=self.call(request,plan=p)
                self.assertFalse(error);self.assertEqual('unsupported_scope',packet['status'])
                self.assertEqual('stop',packet['next_action']['type'])

    def test_unrecognized_or_quoted_scope_does_not_infer_metadata(self):
        for request in ['Explain alpha.', 'If using Formly 6.3.12 with Material, explain alpha.',
                        'Compare Formly 6.3.12 with Material and Formly 7.',
                        'The docs say "For Formly 6.3.12 with Material, alpha".',
                        'For Formly 6.3.12-beta with Material, explain alpha.',
                        'For Formly 6.3.12.4 with Material, explain alpha.',
                        'For Formly 6.3.12 or 7.0.0, explain alpha.']:
            with self.subTest(request=request):
                packet,error=self.call(request,plan=plan('alpha'))
                self.assertFalse(error);self.assertEqual('ok',packet['status'])

    def test_version_only_prefix_does_not_invent_adapter(self):
        request='  use formly 6.3.12. Explain alpha.'
        packet,error=self.call(request,plan=plan('alpha'))
        self.assertTrue(error)
        self.assertEqual(['/plan/library_constraints/formly_version'],[i['path'] for i in packet['issues']])

if __name__=='__main__':unittest.main()
