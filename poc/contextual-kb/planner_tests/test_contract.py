import copy
import unittest
from question_planners.contract import Plan, make_plan, failed, validate_question
from pydantic import ValidationError


class ContractTests(unittest.TestCase):
    def test_original_unicode_and_condition_text_retained(self):
        q = '  🧭 Does resetOnHide: false keep its value?\n'
        p = make_plan(q, [q.strip()])
        self.assertEqual(p.question, q)
        self.assertEqual(p.requests[0].context, q)
        self.assertEqual(p.requests[0].query, q.strip())

    def test_input_bounds(self):
        for q in ['', '  ', 'x' * 8001, '\ud800']:
            with self.subTest(q=q[:20]), self.assertRaises(ValueError):
                validate_question(q)
        validate_question('x' * 8000)

    def test_malformed_plans_rejected(self):
        base = make_plan('What changes?', ['What changes?']).model_dump()
        variants = []
        for key, val in [('extra', 1), ('schema_version', True), ('status', 'supported')]:
            d = copy.deepcopy(base); d[key] = val; variants.append(d)
        d=copy.deepcopy(base); d['requests'][0]['context']='other'; variants.append(d)
        d=copy.deepcopy(base); d['requests'][0]['aspect_ids']=['a9']; variants.append(d)
        d=copy.deepcopy(base); d['requests']=[]; variants.append(d)
        d=copy.deepcopy(base); d['aspects'][0]['source_spans']=[[0,99]]; variants.append(d)
        d=copy.deepcopy(base); d['aspects'][0]['source_spans']=[[True,2]]; variants.append(d)
        d=copy.deepcopy(base); d['requests'][0]['query']=' '; variants.append(d)
        d=copy.deepcopy(base); d['aspects'][0]['id']='a2'; variants.append(d)
        d=copy.deepcopy(base); d['failure']={'code':'timeout','detail':'bad'}; variants.append(d)
        for d in variants:
            with self.subTest(d=d), self.assertRaises((ValueError,ValidationError)):
                Plan.model_validate(d)

    def test_ambiguity_only_and_mixed(self):
        p=make_plan('Which one?', [], ['The referent is unspecified.'])
        self.assertEqual(p.status,'ambiguous')
        p=make_plan('What is a hook and which one runs it?', ['What is a hook?'], ['Unclear referent.'])
        self.assertEqual(len(p.requests),1)

    def test_capacity_never_truncates(self):
        with self.assertRaises(ValueError): make_plan('Question?', ['ask']*9)
        with self.assertRaises(ValueError): make_plan('Question?', [], ['ambiguous']*9)

    def test_failed_input_echo_and_status_invariants(self):
        p=failed('', 'invalid_input', 'empty input')
        self.assertEqual(p.question,'')
        self.assertEqual(p.failure.code,'invalid_input')
        with self.assertRaises(ValueError): failed('', 'backend_error','bad')
        with self.assertRaises(ValueError): make_plan('Which one?', [])

    def test_spans_use_codepoints(self):
        d=make_plan('🧭 abc', ['What is abc?']).model_dump()
        d['aspects'][0]['source_spans']=[[2,5]]
        p=Plan.model_validate(d)
        self.assertEqual(p.question[slice(*p.aspects[0].source_spans[0])],'abc')

if __name__ == '__main__': unittest.main()
