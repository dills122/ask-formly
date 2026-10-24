import copy
import unittest
from qualify import compare_annotations, validate_partitions, boundary_findings


def span(q,text):
    start=q.index(text);return {'text':text,'start':start,'end':start+len(text)}

def row():
    q='Explain registration and removal of the wrapper.'
    fields=['targets','request_cues','conditions','negative_constraints','identifiers','literals','versions','ui_adapters','references','resolved_antecedents','unresolved_references']
    aspects=[]
    for i,cue in enumerate(['registration','removal']):
        a={k:[] for k in fields};a.update(id=str(i),target_anchor=span(q,'the wrapper'),targets=[span(q,'the wrapper')],request_cues=[span(q,'Explain'),span(q,cue)])
        aspects.append(a)
    return {'id':'x','question':q,'status':'clear','aspects':aspects,'entities':{k:[] for k in ['api','custom_identifier','literal','version','ui_adapter']},'relations':[],'rationale':''}

class QualificationTests(unittest.TestCase):
    def test_record_order_and_ids_do_not_change_agreement(self):
        a=row();b=copy.deepcopy(a);b['aspects'].reverse();b['aspects'][0]['id']='new'
        result=compare_annotations([a],[b]);self.assertEqual(result['span_attachment_f1'],1.)
    def test_same_anchor_records_are_not_collapsed(self):
        a=row();b=copy.deepcopy(a);b['aspects'].pop()
        result=compare_annotations([a],[b]);self.assertLess(result['span_attachment_f1'],1.)
        self.assertEqual(result['aspect_count_agreement'],0.)
    def test_wrong_attachment_reduces_agreement(self):
        a=row();a['aspects'][0]['negative_constraints']=[span(a['question'],'removal')]
        b=copy.deepcopy(a);b['aspects'][1]['negative_constraints']=b['aspects'][0]['negative_constraints'];b['aspects'][0]['negative_constraints']=[]
        self.assertLess(compare_annotations([a],[b])['span_attachment_f1'],1.)
    def test_changed_question_or_missing_ids_rejected(self):
        a=row();b=copy.deepcopy(a);b['question']+='x'
        with self.assertRaises(ValueError):compare_annotations([a],[b])
        with self.assertRaises(ValueError):compare_annotations([a],[])
    def test_shared_families_and_duplicate_questions_rejected(self):
        train=[{'id':'T','family':'f','question':'question one'}];dev=[{'id':'D','family':'g','question':'question two'}]
        validate_partitions(train,dev)
        with self.assertRaises(ValueError):validate_partitions(train,[dict(dev[0],family='f')])
        with self.assertRaises(ValueError):validate_partitions(train,[dict(dev[0],question=' question   one ')])
    def test_partial_word_selection_is_flagged(self):
        r=row();r['question']='Does props.disabled disable the field?';s=span(r['question'],'disable')
        r['aspects'][0]['request_cues']=[s]
        self.assertTrue(any(f['text']=='disable' for f in boundary_findings(r)))

if __name__=='__main__':unittest.main()
