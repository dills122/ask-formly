"""Offline fixture validation, not evidence of hosted semantic compliance."""
import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

POC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(POC))
from condition_candidate_v1 import test_planner as inherited
from condition_candidate_v2 import planner as candidate
from mcp_foundation.capitalization import normalize

plan = inherited.plan


class InheritedCandidateTests(inherited.CandidateTests):
    def setUp(self):
        replacement = patch.object(inherited, 'candidate', candidate)
        replacement.start()
        self.addCleanup(replacement.stop)


class PremiseContrastFixtureTests(unittest.TestCase):
    def test_runtime_schema_unchanged_and_contract_only_appended(self):
        old = POC/'condition_candidate_v1'
        for name in ('planner.py', 'plan.schema.json'):
            self.assertEqual((old/name).read_bytes(), (candidate.HERE/name).read_bytes())
        self.assertTrue(candidate.CONTRACT.read_bytes().startswith((old/'CONTRACT.md').read_bytes()))

    def test_attributed_and_uncertain_premise_fixtures_validate(self):
        fixtures = [
            ('A teammate claims hide removes the control', 'Does that imply its model value is cleared?',
             'Given the unverified user report "A teammate claims hide removes the control", does the reported removal imply clearing its model value in Formly?'),
            ('I suspect defaultValue runs on every rebuild', 'Would that overwrite an existing value?',
             'Given the tentative user assertion "I suspect defaultValue runs on every rebuild", would that asserted behavior overwrite an existing value in Formly?'),
        ]
        for premise, followup, question in fixtures:
            with self.subTest(premise=premise):
                request = premise+'. '+followup
                core = plan([question], [(premise, [0])])
                self.assertEqual(normalize(request, core)[0], core)

    def test_target_only_fixtures_allow_empty_ledger(self):
        for question in ('What does hide do in Formly?', 'What is defaultValue in Formly?'):
            with self.subTest(question=question):
                core = plan([question], [])
                self.assertEqual(normalize(question, core)[0], core)

    def test_premise_binds_implication_but_not_independent_general_lookup(self):
        premise = 'I suspect defaultValue runs on every rebuild'
        request = premise+'. Would that overwrite an existing value? Independently, what is defaultValue?'
        core = plan([
            'Given the tentative user assertion "'+premise+'", would that asserted behavior overwrite an existing value in Formly?',
            'What is defaultValue in Formly?',
        ], [(premise, [0])])
        self.assertEqual(normalize(request, core)[0], core)
        wrong_scope = copy.deepcopy(core)
        wrong_scope['condition_bindings'][0]['question_indexes'] = [0, 1]
        with self.assertRaisesRegex(ValueError, 'missing condition in question 1'):
            normalize(request, wrong_scope)

    def test_declared_premise_without_question_excerpt_fails(self):
        premise = 'I suspect defaultValue runs on every rebuild'
        request = premise+'. Would that overwrite an existing value?'
        core = plan(['Would defaultValue overwrite an existing value in Formly?'], [(premise, [0])])
        with self.assertRaisesRegex(ValueError, 'missing condition'):
            normalize(request, core)

    def test_missing_premise_in_both_prose_and_ledger_is_validator_blind_spot(self):
        request = 'I suspect defaultValue runs on every rebuild. Would that overwrite an existing value?'
        # Semantically incomplete under v2, but the unchanged validator does not
        # infer undeclared conditions. This passing test records that limitation.
        incomplete = plan(['Would defaultValue overwrite an existing value in Formly?'], [])
        self.assertEqual(normalize(request, incomplete)[0], incomplete)


if __name__ == '__main__':
    unittest.main()
