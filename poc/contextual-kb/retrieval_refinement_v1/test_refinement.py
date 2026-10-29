import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('refinement_run',HERE/'run.py')
run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)


class FrozenRubricTests(unittest.TestCase):
    def test_freeze_and_referenced_fact_inventory(self):
        self.assertEqual(run.verify_freeze()['revision'],2)
        rubric=json.loads((HERE/'rubric.json').read_text())
        facts={doc['id']+'/'+fact['id'] for path in (HERE.parent/'authored').glob('*.json')
               for doc in [json.loads(path.read_text())] for fact in doc['facts']}
        for entry in rubric.values():
            for facet in entry['essential']:
                self.assertTrue(set(facet['any_of']) <= facts)
        self.assertEqual(rubric['K1-natural']['essential'][1]['any_of'],['public-field-api/key-id-name-roles'])

    def test_frozen_drift_rejects_before_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            for name in ('cases.json','rubric.json','policy.json','freeze.json'):
                (folder/name).write_bytes((HERE/name).read_bytes())
            (folder/'cases.json').write_text('[]')
            with self.assertRaisesRegex(ValueError,'Frozen input changed'):
                run.verify_freeze(folder)

    def test_equivalent_support_and_conditional_evidence_are_separate(self):
        facets=[{'id':'fallback','any_of':['first','equivalent']}]
        self.assertEqual(run.supported_facets({'equivalent'},facets),['fallback'])
        self.assertEqual(run.supported_facets({'conditional'},facets),[])

    def test_recovery_only_selects_returned_ids_and_uses_question(self):
        candidates=[{'id':'hook','claim':'onInit returned Observable subscription'},
                    {'id':'model','claim':'initial model defaultValue undefined'},
                    {'id':'seen','claim':'onInit Observable'}]
        self.assertEqual(run.select_recovery(candidates,{'seen'},'onInit Observable',1),['hook'])
        self.assertEqual(run.select_recovery(candidates,{'seen'},'initial model defaultValue',1),['model'])

    def test_question_selection_covers_unrepresented_question(self):
        questions=[{'question':'onInit Observable subscription'}, {'question':'model defaultValue undefined'}]
        delivered=[{'claim':'onInit Observable subscription'}]
        self.assertEqual(run.select_question(questions,delivered,set()),1)
        self.assertEqual(run.select_question(questions,delivered,{1}),0)

    def test_undiscovered_fetch_is_not_hidden_by_sufficient_coverage(self):
        row={'case_id':'x','calls':[
            {'tool':'lookup_formly','packet':{'status':'ok','facts':[]},'arguments':{},'is_error':False,'sdk_bytes':50,'packet_bytes':20},
            {'tool':'get_formly_facts','packet':{'facts':[{'id':'secret'}]},'arguments':{'fact_ids':['secret']},'is_error':False,'sdk_bytes':100,'packet_bytes':50}]}
        metric=run.grade(row,{'essential':[{'id':'facet','any_of':['secret']}],'conditional':{},'expected_status':'ok'})
        self.assertFalse(metric['missing_facets'])
        self.assertEqual(metric['undiscovered_fetch_ids'],['secret'])

    def test_missing_facets_regression_and_budget_fail_closed(self):
        policy=json.loads((HERE/'policy.json').read_text())
        base=dict(case_id='I1-values',repetition=1,status='ok',expected_status='ok',recovered_ids=['a'],
                  first_pass_facets=['a'],recovered_facets=['a'],essential_count=1,missing_facets=[],
                  diagnostic_only=False,followup_calls=0,undiscovered_fetch_ids=[],tool_errors=0,
                  max_sdk_bytes=100,max_packet_bytes=50)
        candidate=copy.deepcopy(base)
        candidate.update(first_pass_facets=[],recovered_facets=[],missing_facets=['a'],max_sdk_bytes=30001)
        failures=run.gate_failures({'baseline':[base],'candidate':[candidate]},policy)
        self.assertTrue(any('missing essentials' in x for x in failures))
        self.assertTrue(any('first-pass regression' in x for x in failures))
        self.assertTrue(any('byte budget' in x for x in failures))

    def test_no_grading_rubric_parameter_in_executor(self):
        import inspect
        self.assertEqual(list(inspect.signature(run.execute_case).parameters),['session','discovery_parameters','case','policy'])
        self.assertNotIn('rubric',inspect.getsource(run.execute_case).lower().replace('rubric-blind','').replace('expected ids',''))


if __name__=='__main__':unittest.main()
