import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from assess_run import assess_run

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('fixture_summarize',HERE.parent/'extensions-v1/summarize.py')
summarizer=importlib.util.module_from_spec(spec);spec.loader.exec_module(summarizer)

class FixtureGrader:
    def __init__(self): self.calls=[]
    def assessment_complete(self,job):
        path=job/'assessment/results.json'
        return path.exists() and 'rows' in json.loads(path.read_text())
    def grade(self,job,cases):
        self.calls.append(job.name)
        out=job/'assessment';out.mkdir(exist_ok=True)
        (out/'attempt-1').mkdir()
        ids={c['id'] for c in json.loads((job/'prompt.json').read_text())}
        (out/'results.json').write_text(json.dumps({'rows':[dict(c,usable=True,assessment={'critical':False}) for c in cases if c['id'] in ids]}))

class AssessRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.expansion=Path(self.tmp.name).resolve()/'knowledge-expansion';self.expansion.mkdir()
        self.impl=self.expansion/'extensions-v1';self.impl.mkdir()
        for name in ('assess.py','summarize.py'): (self.impl/name).write_text('# test implementation pin\n')
        self.root=self.expansion/'combined-v1/test-output/run-1';self.root.mkdir(parents=True)
        self.cases=self.expansion/'combined-v1/cases.json'
        self.cases.write_text(json.dumps({'cases':[dict(id='A',category='target',request='One'),dict(id='B',category='target',request='Two')]}))
        self.grader=FixtureGrader()

    def job(self,name='r1-b1-candidate'):
        job=self.root/name;job.mkdir()
        (job/'receipt.json').write_text('{"exit_code":0}')
        (job/'prompt.json').write_text('[{"id":"A","request":"One"}]')
        return job

    def run_assessment(self,**kwargs):
        return assess_run('extensions-v1',self.root,self.cases,2,['candidate'],expansion=self.expansion,grader=self.grader,summarizer=summarizer,**kwargs)

    def test_grades_once_and_preserves_fixed_denominators_and_selected_arms(self):
        self.job()
        result=self.run_assessment()
        self.assertEqual(self.grader.calls,['r1-b1-candidate'])
        self.assertEqual([(r['round'],r['arm'],r['total'],r['usable']) for r in result['rounds']],[(1,'candidate',2,1),(2,'candidate',2,0)])
        self.assertEqual(json.loads((self.root/'summary.json').read_text()),result)
        self.run_assessment()
        self.assertEqual(len(self.grader.calls),1)

    def test_prior_attempt_without_result_blocks_provider_retry(self):
        job=self.job();(job/'assessment/attempt-1').mkdir(parents=True)
        with self.assertRaisesRegex(ValueError,'prior assessment attempt'): self.run_assessment()
        self.assertEqual(self.grader.calls,[])

    def test_missing_receipt_is_not_graded_but_remains_in_denominator(self):
        job=self.job();(job/'receipt.json').unlink()
        result=self.run_assessment()
        self.assertEqual(self.grader.calls,[])
        self.assertEqual(result['rounds'][0]['total'],2)
        self.assertEqual(result['rounds'][0]['usable'],0)

    def test_only_selected_arm_is_graded(self):
        self.job('r1-b1-baseline');self.job()
        self.run_assessment()
        self.assertEqual(self.grader.calls,['r1-b1-candidate'])

    def test_root_outside_test_output_and_symlink_escape_rejected(self):
        original=self.root;self.root=self.expansion/'combined-v1'
        with self.assertRaises(ValueError): self.run_assessment()
        self.root=original
        (self.root/'alias').symlink_to(self.tmp.name)
        with self.assertRaisesRegex(ValueError,'symlink'): self.run_assessment()
        self.assertEqual(self.grader.calls,[])

    def test_cases_outside_expansion_and_implementation_traversal_rejected(self):
        self.cases=Path(self.tmp.name)/'outside.json';self.cases.write_text('{}')
        with self.assertRaises(ValueError): self.run_assessment()
        with self.assertRaises(ValueError): assess_run('../outside',self.root,self.cases,1,['candidate'],expansion=self.expansion,grader=self.grader,summarizer=summarizer)

    def test_duplicate_case_ids_and_out_of_range_jobs_rejected(self):
        cases=json.loads(self.cases.read_text());cases['cases'].append(cases['cases'][0]);self.cases.write_text(json.dumps(cases))
        with self.assertRaisesRegex(ValueError,'unique'): self.run_assessment()
        cases['cases'].pop();self.cases.write_text(json.dumps(cases))
        self.job('r3-b1-candidate')
        with self.assertRaisesRegex(ValueError,'repeat'): self.run_assessment()

    def test_invalid_existing_result_is_not_regraded(self):
        job=self.job();(job/'assessment').mkdir();(job/'assessment/results.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'existing assessment'):self.run_assessment()
        self.assertEqual(self.grader.calls,[])

    def test_changed_request_with_same_id_rejects_cached_grade(self):
        self.job();self.run_assessment()
        cases=json.loads(self.cases.read_text());cases['cases'][0]['request']='Changed request'
        self.cases.write_text(json.dumps(cases))
        with self.assertRaisesRegex(ValueError,'prompt.*current cases'):self.run_assessment()
        self.assertEqual(len(self.grader.calls),1)

    def test_changed_rubric_or_added_case_field_rejects_cached_grade(self):
        cases=json.loads(self.cases.read_text())
        cases['cases'][0].update(answer_checks=['Original criterion'],required_support=['fact/original'])
        self.cases.write_text(json.dumps(cases));self.job();self.run_assessment()
        original=self.cases.read_text()
        for key,value in [('answer_checks',['New criterion']),('required_support',['fact/new']),('category','new-category'),('new_field','new constraint')]:
            with self.subTest(field=key):
                changed=json.loads(original);changed['cases'][0][key]=value
                self.cases.write_text(json.dumps(changed))
                with self.assertRaisesRegex(ValueError,'cached assessment.*current cases'):self.run_assessment()
        removed=json.loads(original);del removed['cases'][0]['answer_checks']
        self.cases.write_text(json.dumps(removed))
        with self.assertRaisesRegex(ValueError,'cached assessment.*current cases'):self.run_assessment()
        self.assertEqual(len(self.grader.calls),1)

    def test_saved_prompt_id_request_mismatch_blocks_all_new_grading(self):
        self.job('r1-b1-candidate')
        job=self.job('r1-b2-candidate')
        for prompt in [[{'id':'B','request':'One'}],[{'id':'UNKNOWN','request':'One'}],[{'id':'A','request':'Other'}]]:
            with self.subTest(prompt=prompt):
                (job/'prompt.json').write_text(json.dumps(prompt))
                with self.assertRaisesRegex(ValueError,'prompt.*current cases'):self.run_assessment()
        self.assertEqual(self.grader.calls,[])

    def test_cached_row_original_request_must_match_even_when_prompt_matches(self):
        job=self.job();self.run_assessment()
        result=job/'assessment/results.json';report=json.loads(result.read_text())
        report['rows'][0]['request']='Other request';result.write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError,'cached assessment.*current cases'):self.run_assessment()
        self.assertEqual(len(self.grader.calls),1)

if __name__=='__main__':unittest.main()
