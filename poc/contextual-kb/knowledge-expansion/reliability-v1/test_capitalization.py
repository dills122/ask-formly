import copy
import unittest
from capitalization import normalize
from agent_contract.qualification_v3.candidate import build_plan


REQUEST = 'An internal Formly source file exports TypeOption. Does that make it a public @ngx-formly/core import in 6.3.12? Explain a public typing alternative.'


def core(condition='an internal Formly source file exports TypeOption'):
    return {'formly_questions': [
        {'question': f'In Formly 6.3.12, does the fact that {condition} make TypeOption a public @ngx-formly/core import?', 'reason': 'Check public exports.'},
        {'question': 'In Formly 6.3.12, what public typing alternative can be used?', 'reason': 'Find public typing.'}],
        'library_constraints': {'formly_version': '6.3.12', 'ui_adapter': None},
        'condition_bindings': [{'condition': '6.3.12', 'question_indexes': [0, 1]},
                               {'condition': condition, 'question_indexes': [0]}]}


class CapitalizationTests(unittest.TestCase):
    def test_saved_failure_restored_to_exact_source_without_mutation(self):
        value=core();before=copy.deepcopy(value)
        with self.assertRaisesRegex(ValueError, 'not grounded'):build_plan(REQUEST,value)
        fixed,audit=normalize(REQUEST,value)
        build_plan(REQUEST,fixed)
        self.assertEqual(fixed['condition_bindings'][1]['condition'],'An internal Formly source file exports TypeOption')
        self.assertIn('An internal Formly source file exports TypeOption',fixed['formly_questions'][0]['question'])
        self.assertEqual(fixed['formly_questions'][1],before['formly_questions'][1])
        self.assertEqual(value,before)
        self.assertEqual(audit['original_plan'],before)
        self.assertTrue(audit['rewrites'])

    def test_valid_plan_unchanged_and_repair_idempotent(self):
        valid=core('An internal Formly source file exports TypeOption')
        fixed,audit=normalize(REQUEST,valid)
        self.assertEqual(fixed,valid);self.assertEqual(audit['rewrites'],[])

    def test_api_and_literal_case_is_not_normalized(self):
        for term in ['typeOption','TYPEOPTION','"TypeOption"']:
            with self.subTest(term=term),self.assertRaises(ValueError):
                normalize(REQUEST,core('an internal Formly source file exports '+term))

    def test_missing_or_wrongly_bound_condition_not_inserted(self):
        for index in (0,1):
            value=core();value['formly_questions'][0]['question']='In Formly 6.3.12, what is TypeOption?'
            value['condition_bindings'][1]['question_indexes']=[index]
            with self.assertRaises(ValueError):normalize(REQUEST,value)

    def test_negation_and_remainder_changes_rejected(self):
        for phrase in ['an internal Formly source file does not export TypeOption','an internal Formly source file exports TypeOptionExtra','an internal Formly source file exports TypeOption only for Material']:
            with self.subTest(phrase=phrase),self.assertRaises(ValueError):normalize(REQUEST,core(phrase))

    def test_quoted_article_or_identifier_prefix_rejected(self):
        for request in ['"An internal Formly source file exports TypeOption" is a label in 6.3.12.', 'xAn internal Formly source file exports TypeOption in 6.3.12.']:
            with self.subTest(request=request),self.assertRaises(ValueError):normalize(request,core())

    def test_ambiguous_source_occurrence_rejected(self):
        with self.assertRaises(ValueError):normalize(REQUEST+' '+REQUEST,core())

    def test_invalid_structure_and_lost_additional_restriction_rejected(self):
        for mutation in ('extra','indexes','restriction'):
            value=core();request=REQUEST
            if mutation=='extra':value['extra']=True
            elif mutation=='indexes':value['condition_bindings'][1]['question_indexes']=[True]
            else:
                request+=' Without deep imports.'
                value['condition_bindings'].append({'condition':'Without deep imports','question_indexes':[0]})
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):normalize(request,value)

    def test_other_opening_articles_and_shared_bindings(self):
        for lower in ('a','the'):
            phrase=lower+' custom type uses props.disabled'
            request=phrase.capitalize().replace('Props.disabled','props.disabled')+' in Formly 6.3.12.'
            value=core(phrase)
            value['formly_questions'][1]['question']='In Formly 6.3.12, explain why '+phrase+'?'
            value['condition_bindings'][1]['question_indexes']=[0,1]
            fixed,_=normalize(request,value)
            build_plan(request,fixed)
            again,audit=normalize(request,fixed)
            self.assertEqual(again,fixed);self.assertEqual(audit['rewrites'],[])

    def test_existing_voice_rewrite_still_runs(self):
        request=REQUEST+' Configure props.disabled to track model.isLocked.'
        value=core()
        value['formly_questions'].append({'question':'In Formly, how can props.disabled be configured to track model.isLocked?','reason':'Configure the dependency.'})
        value['condition_bindings'].append({'condition':'props.disabled to track model.isLocked','question_indexes':[2]})
        fixed,audit=normalize(request,value)
        self.assertEqual(len(audit['rewrites']),2)
        self.assertEqual(fixed['formly_questions'][2]['question'],'In Formly, how can I configure props.disabled to track model.isLocked?')

    def test_no_prefix_or_quoted_question_repair(self):
        for text in ['In Formly 6.3.12, explain "an internal Formly source file exports TypeOption".', 'In Formly 6.3.12, an internal Formly source file exports TypeOption.member?']:
            value=core();value['formly_questions'][0]['question']=text
            with self.assertRaises(ValueError):normalize(REQUEST,value)

    def test_phrase_inside_longer_literal_is_not_rewritten(self):
        for opening,closing in [('"','"'),("'","'"),('`','`'),('“','”'),('‘','’')]:
            value=core()
            value['formly_questions'][0]['question']=f'In Formly 6.3.12, explain the label {opening}prefix an internal Formly source file exports TypeOption{closing}.'
            with self.subTest(opening=opening),self.assertRaises(ValueError):normalize(REQUEST,value)

    def test_closed_quotes_and_contractions_do_not_block_plain_text(self):
        value=core()
        value['formly_questions'][0]['question']='In Formly 6.3.12, "example" is closed; it\'s known that an internal Formly source file exports TypeOption. Explain.'
        fixed,_=normalize(REQUEST,value)
        build_plan(REQUEST,fixed)

    def test_code_markers_are_outside_automatic_repair_scope(self):
        for delimiter in ('`','``','```','````','~~~'):
            value=core()
            value['formly_questions'][0]['question']=f'In Formly 6.3.12, explain {delimiter}prefix an internal Formly source file exports TypeOption{delimiter}.'
            with self.subTest(delimiter=delimiter),self.assertRaises(ValueError):normalize(REQUEST,value)
        for text in ['In Formly 6.3.12, <code>prefix an internal Formly source file exports TypeOption</code>.', 'In Formly 6.3.12,\n    prefix an internal Formly source file exports TypeOption.']:
            value=core();value['formly_questions'][0]['question']=text
            with self.subTest(text=text),self.assertRaises(ValueError):normalize(REQUEST,value)


if __name__=='__main__':unittest.main()
