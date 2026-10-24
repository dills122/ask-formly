import unittest
from question_planners.llama import decode, LlamaPlanner


class LlamaTests(unittest.TestCase):
    def test_search_and_ambiguity_transport(self):
        p=decode('Which field and how do wrappers work?',[
            {'tool_name':'formly_search','sub_question':'SEARCH: How do wrappers work?'},
            {'tool_name':'formly_search','sub_question':'AMBIGUITY: Which field is unspecified.'}])
        self.assertEqual(p.status,'ambiguous')
        self.assertEqual(p.requests[0].query,'How do wrappers work?')
        self.assertEqual(p.ambiguities[0].aspect_ids,[])

    def test_native_malformed_outputs_are_rejected(self):
        for rows in [[],[{'tool_name':'run_shell','sub_question':'SEARCH: x'}],
                     [{'tool_name':'formly_search','sub_question':'x'}],
                     [{'tool_name':'formly_search','sub_question':'SEARCH: '}],
                     [{'tool_name':'formly_search','sub_question':'SEARCH: x','extra':1}]]:
            with self.subTest(rows=rows), self.assertRaises(ValueError): decode('What?',rows)

    def test_capacity_explicit(self):
        with self.assertRaises(OverflowError):
            decode('What?',[{'tool_name':'formly_search','sub_question':'SEARCH: x'}]*9)

    def test_one_generation_and_native_trace(self):
        class Generator:
            calls=0
            def generate(self, tools, query):
                self.calls+=1
                self.query=query.query_str
                return [type('Sub',(),{'model_dump':lambda _:dict(tool_name='formly_search',sub_question='SEARCH: What is a wrapper?')})()]
        g=Generator(); p=LlamaPlanner(generator=g)
        plan,trace=p.plan('What is a wrapper?')
        self.assertEqual(g.calls,1)
        self.assertEqual(g.query,'What is a wrapper?')
        self.assertEqual(plan.status,'planned')
        self.assertEqual(trace['native'][0]['tool_name'],'formly_search')

    def test_error_is_not_retried(self):
        class Generator:
            calls=0
            def generate(self,*args):
                self.calls+=1
                raise ValueError('bad native JSON')
        g=Generator(); p=LlamaPlanner(generator=g)
        plan,trace=p.plan('What is a wrapper?')
        self.assertEqual(plan.failure.code,'invalid_output')
        self.assertEqual(g.calls,1)
        self.assertIn('bad native JSON',trace['error'])

if __name__=='__main__': unittest.main()
