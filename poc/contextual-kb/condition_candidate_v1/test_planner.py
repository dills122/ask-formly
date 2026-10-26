"""Offline candidate regressions; no hosted generation or installed asset access."""
import copy
import json
import sys
import tempfile
import unittest
import jsonschema
from pathlib import Path
from unittest.mock import patch

POC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(POC))
from agent_contract.qualification_v3.candidate import build_plan
from mcp_foundation.capitalization import CapitalizingPlanner, normalize
from mcp_v1 import planner as frozen
from condition_candidate_v1 import planner as candidate

# Exact saved Q20 core/request, copied from attempt 8ec371824b9247c6a89fd54eb8a9b007.
# Keep the regression self-contained; tests never open historical qualification.
SAVED_REQUEST = 'An internal Formly source file exports TypeOption. Does that make it a public @ngx-formly/core import in 6.3.12? Explain a public typing alternative.'
SAVED_CORE = {'formly_questions': [{'question': 'In Formly 6.3.12, does an internal Formly source file exporting TypeOption make TypeOption a public @ngx-formly/core import?', 'reason': 'Verify whether an internal export establishes public package availability.'}, {'question': 'In Formly 6.3.12, what public typing alternative can be used instead of importing TypeOption from an internal Formly source file?', 'reason': 'Identify the requested publicly supported typing alternative.'}], 'library_constraints': {'formly_version': '6.3.12', 'ui_adapter': None}, 'condition_bindings': [{'condition': '6.3.12', 'question_indexes': [0, 1]}, {'condition': 'an internal Formly source file exports TypeOption', 'question_indexes': []}]}


def plan(questions, bindings):
    return {'formly_questions': [{'question': q, 'reason': 'Requested lookup.'} for q in questions],
            'library_constraints': {'formly_version': None, 'ui_adapter': None},
            'condition_bindings': [{'condition': c, 'question_indexes': ids} for c, ids in bindings]}


class CandidateTests(unittest.TestCase):
    def test_schema_only_tightens_nonempty_indices(self):
        expected = json.loads((POC/'mcp_v1/plan.schema.json').read_text())
        expected['properties']['condition_bindings']['items']['properties']['question_indexes']['minItems'] = 1
        self.assertEqual(json.loads(candidate.SCHEMA.read_text()), expected)

    def test_schema_rejects_empty_binding_and_accepts_mapped_plan(self):
        schema = json.loads(candidate.SCHEMA.read_text())
        core = copy.deepcopy(SAVED_CORE)
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(core, schema)
        core = plan(['An internal export names TypeOption. Is TypeOption public?'],
                    [('An internal export names TypeOption', [0])])
        jsonschema.validate(core, schema)
        jsonschema.validate(plan([], []), schema)

    def test_contract_preserves_all_existing_semantic_rules(self):
        original = frozen.CONTRACT.read_text()
        self.assertTrue(candidate.CONTRACT.read_text().startswith(original))
        self.assertIn('question_indexes must contain at least one', candidate.CONTRACT.read_text())
        self.assertIn('Never delete an applicable condition', candidate.CONTRACT.read_text())

    def test_candidate_paths_model_and_raw_audit(self):
        core = plan(['What is a Formly wrapper?'], [])
        events = [{'type': 'item.completed', 'item': {'type': 'agent_message', 'text': json.dumps(core)}},
                  {'type': 'turn.completed'}]
        seen = []
        class Process:
            returncode = 0
            def __init__(self, command, **kwargs):
                seen.append(command)
                kwargs['stdout'].write(('\n'.join(map(json.dumps, events))+'\n').encode())
            def communicate(self, request, timeout):
                self.input = request
        with tempfile.TemporaryDirectory() as directory, patch.object(candidate.subprocess, 'Popen', Process):
            generated, receipt = candidate.CodexPlanner(directory)('What is a Formly wrapper?')
            self.assertEqual(generated, core)
            self.assertEqual(len(seen), 1)
            command = seen[0]
            self.assertEqual(command[command.index('--output-schema')+1], str(candidate.SCHEMA))
            self.assertIn('model_instructions_file='+json.dumps(str(candidate.CONTRACT)), command)
            for setting in ('features.shell_tool=false', 'features.multi_agent=false', 'features.apps=false', 'web_search="disabled"'):
                self.assertIn(setting, command)
            self.assertEqual(receipt['model'], frozen.MODEL)
            self.assertEqual(receipt['reasoning_effort'], frozen.EFFORT)
            job = Path(directory)/receipt['attempt_id']
            self.assertEqual(json.loads((job/'request.json').read_text()), 'What is a Formly wrapper?')
            self.assertEqual([json.loads(x) for x in (job/'events.jsonl').read_text().splitlines()], events)
            self.assertEqual(json.loads((job/'receipt.json').read_text()), receipt)
        self.assertEqual(frozen.CONTRACT, POC/'agent_contract/qualification_v3/CONTRACT.md')

    def test_saved_failure_remains_rejected_with_capitalization_only(self):
        request = SAVED_REQUEST
        core = copy.deepcopy(SAVED_CORE)
        before = copy.deepcopy(core)
        with self.assertRaisesRegex(ValueError, 'condition not grounded'):
            normalize(request, core)
        self.assertEqual(core, before)
        core['condition_bindings'][1]['condition'] = 'An internal Formly source file exports TypeOption'
        with self.assertRaisesRegex(ValueError, 'invalid question indices'):
            normalize(request, core)

    def test_successful_nonempty_binding_preserves_source_and_api(self):
        request = 'An internal export names TypeOption. Is TypeOption public?'
        core = plan(['An internal export names TypeOption. Is TypeOption a public Formly import?'], [('An internal export names TypeOption', [0])])
        fixed, _ = normalize(request, core)
        self.assertEqual(fixed, core)

    def test_lost_condition_and_negation_fail_without_repair(self):
        request = 'Can Formly observe changes without polling?'
        for question in ('Can Formly observe changes?', 'Can Formly observe changes with polling?'):
            with self.subTest(question=question), self.assertRaisesRegex(ValueError, 'missing condition'):
                normalize(request, plan([question], [('without polling', [0])]))

    def test_api_spelling_is_not_casefolded(self):
        request = 'Does Formly preserve resetOnHide: false?'
        core = plan(['Does Formly preserve resetonhide: false?'], [('resetonhide: false', [0])])
        with self.assertRaisesRegex(ValueError, 'condition not grounded'):
            normalize(request, core)

    def test_local_restriction_remains_local(self):
        request = 'Does Formly support observation? If supported, how can I use it without polling?'
        core = plan(['Does Formly support observation?', 'If supported, how can I use Formly observation without polling?'],
                    [('If supported', [1]), ('without polling', [1])])
        fixed, _ = normalize(request, core)
        self.assertEqual(fixed, core)
        core['condition_bindings'][1]['question_indexes'] = [0, 1]
        with self.assertRaisesRegex(ValueError, 'missing condition in question 0'):
            normalize(request, core)

    def test_bad_indices_fail_closed(self):
        for ids in ([], [True], [-1], [1], [0, 0]):
            with self.subTest(ids=ids), self.assertRaisesRegex(ValueError, 'invalid question indices'):
                normalize('without polling', plan(['Use Formly without polling?'], [('without polling', ids)]))

    def test_existing_wrapper_rejects_candidate_invalid_plan_without_retry(self):
        calls = []
        def generator(request):
            calls.append(request)
            return plan(['Can Formly observe changes?'], [('without polling', [])]), {}
        with self.assertRaises(ValueError):
            CapitalizingPlanner(generator)('Can Formly observe changes without polling?')
        self.assertEqual(len(calls), 1)

    def test_no_condition_request_still_permits_empty_ledger(self):
        core = plan(['What is a Formly wrapper?'], [])
        self.assertEqual(build_plan('What is a Formly wrapper?', core)['question_plan'], core)
        empty = plan([], [])
        self.assertEqual(build_plan('Change my app logo.', empty)['question_plan'], empty)


if __name__ == '__main__':
    unittest.main()
