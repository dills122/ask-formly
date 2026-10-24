"""Real installed-model processor acceptance, without predictions or optimization."""
import hashlib
import json
import os
from pathlib import Path
import sys
import unittest
from contract import export_example, FIELDS
from pilot_tools import HERE, BASE, check_access

os.environ.update(HF_HOME=str(HERE/'.cache/hf'),HF_HUB_OFFLINE='1',
                  TRANSFORMERS_OFFLINE='1',TOKENIZERS_PARALLELISM='false')


class PreprocessingAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import torch
        from gliner2 import AutoExtractor
        from gliner2.processor import SamplingConfig
        torch.set_num_threads(4);torch.manual_seed(1701)
        for name,digest in json.loads((HERE/'evidence/annotation-freeze-v2.json').read_text()).items():
            if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=digest:
                raise ValueError('Frozen annotations changed')
        cls.rows=json.loads((HERE/'adjudicated-v2.json').read_text())
        sys.addaudithook(check_access)
        cls.model=AutoExtractor.from_pretrained(str(BASE/'models/gliner2.5-base-v1'),
                                                local_files_only=True,map_location='cpu')
        # No stochastic label/schema removal during this lossless transport check.
        cls.model.processor.sampling_config=SamplingConfig(
            remove_json_structure_prob=0,shuffle_json_fields=False,remove_json_field_prob=0,
            remove_entities_prob=0,shuffle_entities=False,remove_entity_prob=0,
            synthetic_entity_label_prob=0,remove_relations_prob=0,swap_head_tail_prob=0,
            remove_classification_prob=0,shuffle_classification_labels=False,
            remove_classification_label_prob=0,synthetic_label_prob=0,include_true_label_prob=1)

    def test_all_24_training_records_preserve_exact_field_occurrences(self):
        evidence=[]
        for row in self.rows:
            with self.subTest(case=row['id']):
                native=export_example(row)
                batch=self.model.processor.collate_fn_train(
                    [(native['input'],native['output'])],architecture='boundary',
                    error_policy='raise',on_capacity_exceeded='raise',
                    dedupe_contained_entity_spans=False)
                records=batch.targets.records[0]
                self.assertEqual(len(records),len(row['aspects']))
                specs=batch.record_specs[0]
                decoded=[]
                for record in records:
                    spec=specs[record.task_index]
                    fields={}
                    for fs in spec.fields:
                        ft=record.field_for_query(fs.query_id)
                        offsets=[]
                        for alternatives in ft.values:
                            self.assertEqual(len(alternatives),1,'Explicit offset has multiple resolutions')
                            start,end=alternatives[0]
                            offsets.append((batch.start_mappings[0][start],batch.end_mappings[0][end-1]))
                        fields[fs.name]=sorted(offsets)
                    decoded.append(fields)
                expected=[]
                for a in row['aspects']:
                    fields={k:sorted((s['start'],s['end']) for s in a[k]) for k in FIELDS}
                    fields['target_anchor']=[(a['target_anchor']['start'],a['target_anchor']['end'])]
                    expected.append(fields)
                evidence.append({'id':row['id'],'records':len(records),'task_types':batch.task_types,
                                 'decoded':decoded,'expected':expected})
                self.assertEqual(decoded,expected)
        # Preserve diagnostic evidence even when subtests fail.
        if os.environ.get('PILOT_WRITE_EVIDENCE')=='1':
            with (HERE/'evidence/preprocessing-v2.json').open('x') as out:
                json.dump(evidence,out,indent=2)


if __name__=='__main__':unittest.main()
