"""Library acceptance tests. A failure is a compatibility finding, not skipped.

The oracle test supplies perfect candidate scores to remove model accuracy from
the question of whether one exact target occurrence can seed two request records.
"""
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
import torch
from gliner2.training.data import InputExample
from gliner2.models.boundary.records import RecordHead, decode_group
from gliner2.processing.records import RecordSpec, RecordFieldSpec, FieldCardinality
from contract import export_example

HERE=Path(__file__).resolve().parent


def oracle_group(anchor_spans):
    fields=(RecordFieldSpec(0,'target_anchor',0,FieldCardinality.REQUIRED_ONE,True),
            RecordFieldSpec(1,'request_cues',1,FieldCardinality.ZERO_OR_MORE))
    spec=RecordSpec(0,'request','json_structures','natural',fields,0)
    n=len(anchor_spans)
    candidates=SimpleNamespace(
        indices=torch.tensor([[anchor_spans+[(0,0)]*(2-n),[(4,5),(6,7)]]]),
        valid_mask=torch.tensor([[[True]*n+[False]*(2-n),[True,True]]]),
        pair_logits=torch.full((1,2,2),10.),candidate_states=torch.zeros((1,2,2,4)))
    # Exercise real instance formation, not a manually chosen output record count.
    group=RecordHead(hidden_size=4,record_dim=4,instance_queries=4).forward_group(
        spec,torch.zeros((2,4)),candidates,0)
    group.assign_logits=[torch.full((group.num_instances,1+n),10.),
                         torch.tensor([[-10.,10.,10.]]*group.num_instances)]
    return group


class NativeAcceptance(unittest.TestCase):
    def test_all_24_explicit_labels_roundtrip_native_api(self):
        rows=json.loads((HERE/'adjudicated-v2.json').read_text())
        for row in rows:
            with self.subTest(case=row['id']):
                exported=export_example(row)
                native=InputExample.from_dict(exported)
                self.assertTrue(native.is_valid(), native.validate())
                restored=native.to_dict()
                for key,value in exported['output'].items():
                    if key=='classifications':
                        # Public API canonicalizes a scalar label to a list and
                        # omits default multi_label=False. Check meaning explicitly.
                        actual=restored['output'][key][0]
                        self.assertEqual(actual['true_label'],[row['status']])
                        self.assertEqual(actual['labels'],value[0]['labels'])
                        self.assertEqual(actual['task'],value[0]['task'])
                        self.assertFalse(actual.get('multi_label',False))
                    else:
                        self.assertEqual(restored['output'].get(key,[] if key=='relations' else None),value)

    def test_distinct_anchor_positive_control_can_emit_two_records(self):
        self.assertEqual(len(decode_group(oracle_group([(1,3),(8,10)]))),2)

    def test_same_exact_target_must_support_two_different_requests(self):
        # P04's two requests anchor the same occurrence of 'the wrapper'.
        # Natural mode seeds one instance per distinct detected anchor candidate.
        output=decode_group(oracle_group([(1,3)]))
        self.assertEqual(len(output),2,
                         'Two gold requests sharing an exact target collapse to one native instance')


if __name__=='__main__':unittest.main()
