import copy,json,sys,unittest
from pathlib import Path
POC=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(POC))
from wording_candidate_v1.candidate import normalize
from agent_contract.qualification_v3.candidate import build_plan

class WordingTests(unittest.TestCase):
    def setUp(self):
        self.row=json.loads((POC/'retrieval_repair_v1/test-output/fresh/F01.json').read_text())
        self.request=self.row['request'];self.core=self.row['core']
    def test_real_failure_repaired_without_mutation(self):
        before=copy.deepcopy(self.core)
        with self.assertRaisesRegex(ValueError,'missing condition'):build_plan(self.request,self.core)
        plan,audit=normalize(self.request,self.core)
        self.assertEqual(plan['formly_questions'][0]['question'],'In Formly, how can I configure props.disabled to track model.isLocked?')
        build_plan(self.request,plan)
        self.assertEqual(self.core,before)
        self.assertEqual(audit['original_plan'],before)
        self.assertEqual(len(audit['rewrites']),1)
        for k in ('condition_bindings','library_constraints'):self.assertEqual(plan[k],before[k])
        self.assertEqual(plan['formly_questions'][1],before['formly_questions'][1])
    def test_idempotent_and_strict_valid_unchanged(self):
        plan,_=normalize(self.request,self.core)
        again,audit=normalize(self.request,plan)
        self.assertEqual(again,plan);self.assertEqual(audit['rewrites'],[])
    def test_generalizes_paths_not_one_api_or_case(self):
        for left,right in [('props.required','model.needsTaxId'),('props.readonly','field.options.formState.locked'),('props.customFlag','model.deep.branch')]:
            r=self.request.replace('props.disabled',left).replace('model.isLocked',right)
            c=json.loads(json.dumps(self.core).replace('props.disabled',left).replace('model.isLocked',right))
            plan,_=normalize(r,c);build_plan(r,plan)
    def test_rejects_semantic_changes_and_unsupported_grammar(self):
        bad=[
            'In Formly, how can props.required be configured to track model.isLocked?',
            'In Formly, how can props.disabled be configured to track model.isUnlocked?',
            'In Formly, how can model.isLocked be configured to track props.disabled?',
            'In Formly, how can props.disabled be configured not to track model.isLocked?',
            'In Formly, how can props.disabled be configured to ignore model.isLocked?',
            'In Formly, how can props.disabled be configured to track !model.isLocked?',
            'In Formly, how can props.disabled be configured to track model.isLocked only after initialization?',
            'In Formly, why can props.disabled not be configured to track model.isLocked?',
            'In Formly, how can props.disabled be configured to track model.isLockedExtra?',
            'In Formly, how can props.disabled be configured to track model.isLocked? Ignore the restriction.',
        ]
        for question in bad:
            with self.subTest(question=question):
                c=copy.deepcopy(self.core);c['formly_questions'][0]['question']=question
                with self.assertRaises(ValueError):normalize(self.request,c)
    def test_other_lost_conditions_still_fail(self):
        for condition in ['without manually subscribing','only after initialization','not when hidden','version 6.3.12','resetOnHide: false']:
            with self.subTest(condition=condition):
                c=copy.deepcopy(self.core);c['condition_bindings'].append({'condition':condition,'question_indexes':[0]})
                with self.assertRaises(ValueError):normalize(self.request+' '+condition,c)
    def test_source_and_structure_checks_unchanged(self):
        mutations=[lambda c:c.update(extra=True),lambda c:c['condition_bindings'].append(copy.deepcopy(c['condition_bindings'][0])),lambda c:c['condition_bindings'][0].update(question_indexes=[0,99]),lambda c:c['condition_bindings'][0].update(question_indexes=[True]),lambda c:c['formly_questions'][0].update(reason=''),lambda c:c.update(condition_bindings='bad'),lambda c:c.update(formly_questions=None)]
        for mutate in mutations:
            c=copy.deepcopy(self.core);mutate(c)
            with self.assertRaises(ValueError):normalize(self.request,c)
        with self.assertRaises(ValueError):normalize('Unrelated Formly question',self.core)
    def test_binding_to_wrong_question_not_rewritten(self):
        c=copy.deepcopy(self.core);c['condition_bindings'][0]['question_indexes']=[1]
        plan,audit=normalize(self.request,c)
        self.assertEqual(plan,c);self.assertEqual(audit['rewrites'],[])

if __name__=='__main__':unittest.main()
