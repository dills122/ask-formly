import copy
import unittest
from contract import export_example, validate_annotation, FIELDS


def example():
    q = '☕ value and value without clearing'
    def s(a, b): return {'text': q[a:b], 'start': a, 'end': b}
    def a(i, target):
        return dict(id=i, target_anchor=target, **{k: [] for k in FIELDS},
                    )
    x, y = a('a1', s(2, 7)), a('a2', s(12, 17))
    for record in [x, y]:
        record['targets'] = [record['target_anchor']]
        record['negative_constraints'] = [s(18, len(q))]
    return dict(id='T', question=q, status='clear', aspects=[x,y],
                entities={k: [] for k in ['api','custom_identifier','literal','version','ui_adapter']},
                relations=[], rationale='Test fixture')


class ContractTests(unittest.TestCase):
    def test_occurrences_unicode_and_shared_negative_survive_export(self):
        row = example(); native = export_example(row)
        records = native['output']['json_structures']
        self.assertEqual([r['request']['target_anchor']['start'] for r in records], [2,12])
        self.assertEqual(records[0]['request']['negative_constraints'],
                         records[1]['request']['negative_constraints'])
        self.assertEqual(native['input'], row['question'])
        self.assertEqual(native['output']['record_metadata']['request']['anchor'], 'target_anchor')

    def test_same_anchor_requests_are_not_silently_merged(self):
        row = example(); row['aspects'][1] = copy.deepcopy(row['aspects'][0])
        row['aspects'][1]['id'] = 'a2'
        self.assertEqual(len(export_example(row)['output']['json_structures']), 2)

    def test_invalid_offsets_fail(self):
        row=example(); row['aspects'][0]['target_anchor']['start']=0
        with self.assertRaises(ValueError): validate_annotation(row)

    def test_unknown_or_missing_fields_fail(self):
        for field in ['conditions','negative_constraints']:
            row=example(); del row['aspects'][0][field]
            with self.assertRaises(ValueError): validate_annotation(row)
        row=example(); row['aspects'][0]['guessed_answer']='yes'
        with self.assertRaises(ValueError): validate_annotation(row)

    def test_ambiguity_requires_grounded_unresolved_span(self):
        row=example(); row['status']='needs_clarification'
        with self.assertRaises(ValueError): validate_annotation(row)
        row['aspects'][0]['unresolved_references']=[row['aspects'][0]['target_anchor']]
        validate_annotation(row)
        row['status']='clear'
        with self.assertRaises(ValueError): validate_annotation(row)

    def test_empty_labels_and_explicit_pairs_survive(self):
        row=example()
        row['relations']=[{'kind':'refers_to','head':row['aspects'][1]['target_anchor'],
                          'tail':row['aspects'][0]['target_anchor']}]
        native=export_example(row)
        self.assertEqual(native['output']['entities']['api'], [])
        self.assertEqual(native['output']['relations'][0]['refers_to']['head']['start'],12)
        self.assertEqual(native['output']['classifications'][0]['true_label'],'clear')

    def test_no_mutation_and_duplicate_ids_rejected(self):
        row=example(); before=copy.deepcopy(row); export_example(row)
        self.assertEqual(row,before)
        row['aspects'][1]['id']='a1'
        with self.assertRaises(ValueError): validate_annotation(row)

    def test_unknown_relation_and_out_of_bounds_rejected(self):
        row=example(); row['relations']=[{'kind':'answer_is','head':row['aspects'][0]['target_anchor'],
                                       'tail':row['aspects'][1]['target_anchor']}]
        with self.assertRaises(ValueError): validate_annotation(row)
        row=example(); row['aspects'][0]['conditions']=[{'text':'','start':50,'end':50}]
        with self.assertRaises(ValueError): validate_annotation(row)


if __name__ == '__main__': unittest.main()
