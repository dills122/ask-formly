"""Qualification assertions over prepared data, not model performance tests."""
import hashlib,json,sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from pilot.contract import validate_annotation
from qualify import validate_partitions,boundary_findings

def read(name):return json.loads((HERE/name).read_text())
class DatasetTests(unittest.TestCase):
    def test_canonical_rows_and_unchanged_pilot(self):
        train=read('adjudicated-v1/train.json');dev=read('adjudicated-v1/dev.json')
        pilot=json.loads((HERE.parent/'pilot/adjudicated-v2.json').read_text())
        self.assertEqual((len(train),len(dev)),(120,30));self.assertEqual(train[:24],pilot)
        for row in train+dev:
            validate_annotation(row);self.assertFalse(boundary_findings(row));self.assertLessEqual(len(row['aspects']),32)
    def test_split_families_quotas_and_final_source(self):
        from collections import Counter
        meta=read('adjudicated-v1/metadata.json');validate_partitions(meta['train'],meta['dev'])
        self.assertEqual(set(Counter(x['stratum'] for x in meta['train']).values()),{20})
        self.assertEqual(set(Counter(x['stratum'] for x in meta['dev']).values()),{5})
        self.assertEqual(len(Counter(x['stratum'] for x in meta['train'])),6)
        final=read('questions-v3.json')
        for split in ['train','dev']:
            actual={r['id']:r['question'] for r in read(f'adjudicated-v1/{split}.json')}
            for row in final[split]:self.assertEqual(actual[row['id']],row['question'])
    def test_raw_agreement_and_audit_coverage(self):
        self.assertTrue(read('agreement-v1.json')['training_sample']['passes_gate'])
        self.assertTrue(read('agreement-final-development.json')['passes_gate'])
        chosen=set(read('questions.json')['double_annotate_training_ids'])
        audited={r['id'] for r in read('remaining-training-audit.json')}
        self.assertFalse(chosen&audited);self.assertEqual(len(chosen),24);self.assertEqual(len(audited),72)
        self.assertEqual(chosen|audited,{r['id'] for r in read('questions.json')['train']})
    def test_native_transport_all_rows_and_raw_evidence_preserved(self):
        report=read('native-transport-v1/report.json')
        self.assertEqual(report['status'],'passed');self.assertFalse(report['failures']);self.assertEqual(len(report['cases']),150)
        self.assertEqual(report['optimizer_steps'],0);self.assertEqual(report['inference_calls'],0)
        for name,digest in read('raw-freeze-v1.json').items():self.assertEqual(hashlib.sha256((HERE/name).read_bytes()).hexdigest(),digest)

if __name__=='__main__':unittest.main()
