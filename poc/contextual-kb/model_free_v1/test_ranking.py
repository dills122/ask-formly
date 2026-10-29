"""Source-independent regression cases for lexical relevance, not answer scores."""
import unittest

from ranking import diagnostics, rerank, query_text, canonical_identifiers


def fact(claim, context='', conditions=(), limits=(), title=''):
    return dict(claim=claim, context=context, conditions=list(conditions),
                limits=list(limits), title=title)


class RankingTests(unittest.TestCase):
    def test_known_member_aliases_share_ranking_but_do_not_rewrite_facts(self):
        facts = {'state': fact('formState changes trigger expression updates.'),
                 'context': fact('options.formState carries shared form context.'),
                 'other': fact('Model updates rebuild fields.')}
        original = repr(facts)
        bare = rerank('How does formState trigger expression updates?', facts, list(facts))
        qualified = rerank('How does options.formState trigger expression updates?', facts, list(facts))
        self.assertEqual(bare, qualified)
        self.assertEqual('state', bare[0])
        self.assertEqual(original, repr(facts))
        result = diagnostics('options.formState', facts, list(facts))
        self.assertEqual([{'supplied': 'options.formState', 'canonical': 'formState'}], result['identifier_aliases'])

    def test_aliases_do_not_strip_arbitrary_qualifiers_or_merge_distinct_paths(self):
        self.assertEqual('application.formState', canonical_identifiers('application.formState'))
        self.assertEqual('props.disabled templateOptions.disabled',
                         canonical_identifiers('props.disabled templateOptions.disabled'))
        self.assertEqual('hooks.customHook', canonical_identifiers('hooks.customHook'))
        self.assertEqual('onInit', canonical_identifiers('field.hooks.onInit'))

    def test_collision_expansion_requires_model_value_intent(self):
        text = 'Two sections have name fields; how do I avoid their values colliding?'
        self.assertTrue(query_text(text).endswith(' key model path fieldGroup'))
        for query in ('Do duplicate DOM names collide?', 'How do registered type names collide?',
                      'Which wrapper name wins a registration collision?'):
            self.assertEqual(query, query_text(query))
        result = diagnostics(text, {'scope': fact('key fieldGroup model scope')}, ['scope'])
        self.assertEqual(['key', 'model', 'path', 'fieldGroup'], result['lexical_expansions'])
        self.assertEqual('not_assessed', result['semantic_relevance'])

    def test_collision_vocabulary_can_reach_model_scope_without_topic_penalty(self):
        facts = {'appearance': fact('Set the appearance name.', title='Material appearance'),
                 'scope': fact('A keyed fieldGroup provides a nested model path for child values.')}
        self.assertEqual('scope', rerank('Two name fields in sections have colliding values.', facts, list(facts))[0])

    def test_query_scope_prefix_stripped_but_subject_material_retained(self):
        self.assertEqual('hide a field', query_text('For Formly 6.3.12 with Material, hide a field'))
        self.assertEqual('Material select compareWith', query_text('Material select compareWith'))

    def test_control_lifecycle_offers_contrasting_evidence_without_rewriting(self):
        facts = {'render': fact('Lazy rendering avoids creating the rendered component.'),
                 'removal': fact('Hiding unregisters the control.', 'control lifetime'),
                 'addition': fact('Showing registers the control.', 'control lifetime')}
        original = repr(facts)
        query = 'Do hidden controls stay registered?'
        ranked = rerank(query, facts, list(facts))
        self.assertIn('removal', ranked[:2])
        self.assertEqual(original, repr(facts))
        signal = diagnostics(query, facts, list(facts))
        self.assertEqual(['register', 'registered', 'registration', 'unregister',
                          'unregistered', 'unregistration'], signal['lexical_expansions'])
        self.assertEqual('not_assessed', signal['semantic_relevance'])
        self.assertTrue(query_text('Do not unregister controls').startswith('Do not unregister controls'))
        self.assertEqual(rerank(query, facts, list(facts)),
                         rerank(query + ' registered' * 50, facts, list(facts)))

    def test_lifecycle_expansion_requires_control_and_plain_registration_words(self):
        for query in ('Register a component type', 'Which registered wrapper wins?',
                      'Registration of an unknown type', 'unregisterField controls',
                      'registerField controls', 'controls unknownRegistration',
                      'Register application.formControl', 'Controls are hidden',
                      'How do I register a custom control type?',
                      'Register a custom control component',
                      'Which provider registers a formControl?',
                      'Registration of wrappers for controls'):
            self.assertEqual(query, query_text(query))
        self.assertIn('unregistration', query_text('field.formControl registration'))
        self.assertIn('unregistration', query_text('Do hidden custom component controls remain registered?'))

    def test_hide_claim_beats_incidental_array_fixture(self):
        facts = {
            'fixture': fact('An array insertion fixture expects one child.',
                            conditions=['resetOnHide is false; hide preserves a model value.']),
            'retention': fact('resetOnHide false preserves the model value.',
                             'hide value retention'),
            'registration': fact('hide unregisters the control.', 'hide control registration'),
        }
        ids = rerank('hide resetOnHide model value control registration', facts,
                     ['fixture', 'retention', 'registration'])
        self.assertEqual({'retention', 'registration'}, set(ids[:2]))

    def test_keyed_scope_beats_callback_qualifier(self):
        facts = {
            'callback': fact('Debounce controls value callbacks.',
                             limits=['key model fieldGroup scope is not established.']),
            'scope': fact('A fieldGroup with key creates nested model scope.'),
            'keyless': fact('A keyless fieldGroup shares its parent model scope.'),
        }
        ids = rerank('fieldGroup key model scope', facts, list(facts))
        self.assertEqual({'scope', 'keyless'}, set(ids[:2]))

    def test_initialization_api_beats_incidental_default_fixture(self):
        facts = {
            'fixture': fact('Array insertion creates a child.',
                            conditions=['onInit prePopulate defaultValue initialize the fixture.']),
            'hook': fact('An Observable returned by onInit is managed.', 'onInit lifetime'),
            'extension': fact('prePopulate runs before onPopulate.', 'extension build phases'),
            'defaults': fact('defaultValue fills an undefined model value.'),
        }
        ids = rerank('onInit prePopulate defaultValue initialization', facts, list(facts))
        self.assertEqual({'hook', 'extension', 'defaults'}, set(ids[:3]))

    def test_collision_api_beats_unrelated_family(self):
        facts = {
            'schema': fact('The converter creates schema groups.',
                           conditions=['shareFormControl and key configure these generated groups.']),
            'control': fact('shareFormControl determines parent control lookup at a key path.'),
            'validators': fact('Fields sharing a control compose participating validators.'),
        }
        self.assertEqual('control', rerank('shareFormControl key control validators',
                                          facts, list(facts))[0])

    def test_json_schema_is_not_globally_demoted(self):
        facts = {
            'core': fact('Fields use validation.', limits=['uniqueItems is not specified.']),
            'schema': fact('uniqueItems compares serialized array values.',
                           'JSON Schema array uniqueness'),
        }
        self.assertEqual('schema', rerank('JSON Schema uniqueItems array validation',
                                         facts, list(facts))[0])

    def test_material_is_not_globally_demoted(self):
        facts = {
            'core': fact('Model values update controls.', limits=['No compareWith guarantee.']),
            'material': fact('Material select compareWith controls option comparison.'),
        }
        self.assertEqual('material', rerank('Material select compareWith', facts, list(facts))[0])

    def test_scope_prefix_does_not_turn_core_request_into_material_search(self):
        facts = {'renderer': fact('Material renders a field.', title='Material widgets'),
                 'core': fact('A hidden control leaves the control tree.', title='Hiding')}
        query = 'For Formly 6.3.12 with Material, hide control'
        self.assertEqual('core', rerank(query, facts, list(facts))[0])

    def test_prose_inflections_match_without_rewriting_returned_claims(self):
        facts = {'other': fact('Different model values.'),
                 'control': fact('A hidden control is unregistered.', title='Hiding')}
        self.assertEqual('control', rerank('hide controls', facts, list(facts))[0])
        self.assertEqual('A hidden control is unregistered.', facts['control']['claim'])

    def test_api_negation_and_dotted_names_are_not_collapsed(self):
        facts = {'wrong': fact('registerField performs registration.'),
                 'right': fact('unregisterField removes a control.')}
        self.assertEqual('right', rerank('unregisterField', facts, list(facts))[0])
        self.assertEqual(['unregisterField'],
                         diagnostics('unregisterField', facts, list(facts))['recognized_identifiers'])

    def test_preserves_candidate_boundary_and_ties(self):
        facts = {'excluded': fact('alpha alpha alpha'),
                 'b': fact('alpha'), 'a': fact('alpha')}
        self.assertEqual(['b', 'a'], rerank('alpha', facts, ['b', 'a', 'b']))
        self.assertEqual(['b', 'a'], rerank('unmatched', facts, ['b', 'a']))
        self.assertEqual([], rerank('alpha', facts, []))

    def test_duplicate_query_terms_cannot_stuff_ranking(self):
        facts = {'a': fact('alpha beta'), 'b': fact('alpha gamma')}
        self.assertEqual(rerank('alpha beta', facts, list(facts)),
                         rerank('alpha ' * 100 + 'beta', facts, list(facts)))

    def test_lowercase_apis_receive_diagnostic_recognition(self):
        facts = {'a': fact('hide key model determine field behavior.')}
        result = diagnostics('hide key model', facts, ['a'])
        self.assertEqual(['hide', 'key', 'model'], result['recognized_identifiers'])
        self.assertEqual('not_assessed', result['semantic_relevance'])

    def test_missing_topic_hint_does_not_claim_nonexistence(self):
        result = diagnostics('stepper wizard', {'a': fact('Fields have controls.')}, ['a'])
        self.assertEqual('no_recognized_identifier', result['signal'])
        self.assertEqual(['stepper', 'wizard'], result['unmatched_primary_terms'])
        self.assertEqual('not_assessed', result['semantic_relevance'])
        self.assertNotIn('unsupported', result['hint'])

    def test_diagnostics_are_bounded_and_preserve_exact_identifier_spelling(self):
        names = [f'customApi{i}' for i in range(30)]
        facts = {'a': fact(' '.join(names))}
        result = diagnostics(' '.join(names), facts, ['a'])
        self.assertEqual(16, len(result['recognized_identifiers']))
        self.assertEqual(30, result['recognized_identifier_count'])
        self.assertEqual([], diagnostics('customapi0', facts, ['a'])['recognized_identifiers'])


if __name__ == '__main__':
    unittest.main()
