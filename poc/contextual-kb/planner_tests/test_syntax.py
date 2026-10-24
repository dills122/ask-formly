import unittest
from question_planners.syntax import SyntaxPlanner


class SyntaxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.planner = SyntaxPlanner()

    def test_shared_condition_retained_for_coordinated_outcomes(self):
        p, t = self.planner.plan('If I hide a field with resetOnHide: false, what happens to its value and its FormControl?')
        self.assertEqual(p.status, 'planned')
        self.assertEqual(len(p.requests), 2)
        for r in p.requests:
            self.assertIn('resetOnHide: false', r.query)
            self.assertIn('hide a field', r.query)
        self.assertIn('value', p.requests[0].query)
        self.assertNotIn('FormControl', p.requests[0].query)
        self.assertIn('FormControl', p.requests[1].query)
        self.assertNotIn('value', p.requests[1].query)
        self.assertTrue(t['dependencies'])

    def test_coordinated_verbs_borrow_subject_and_condition(self):
        p, _ = self.planner.plan('When the field is hidden, can I keep its answer and retain its control?')
        self.assertEqual(len(p.requests), 2)
        self.assertIn('can I retain', p.requests[1].query)
        for r in p.requests: self.assertIn('When the field is hidden', r.query)

    def test_comparison_not_split(self):
        q = 'What is the difference between expressions and expressionProperties?'
        p, _ = self.planner.plan(q)
        self.assertEqual([r.query for r in p.requests], [q])

    def test_negation_and_generic_tokens_survive(self):
        for q in ['Can a disabled field keep its value without removing its control?',
                  'Can FormlyFieldConfig<MyProps> type a custom prop?']:
            p, _ = self.planner.plan(q)
            self.assertEqual([r.query for r in p.requests], [q])

    def test_unresolved_deictic_reference(self):
        p, _ = self.planner.plan('What does that setting do?')
        self.assertEqual(p.status, 'ambiguous')
        self.assertEqual(p.requests, [])
