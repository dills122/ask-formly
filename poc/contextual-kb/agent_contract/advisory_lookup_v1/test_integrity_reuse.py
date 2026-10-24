import sys,tempfile,unittest
from pathlib import Path
from lookup import AdvisoryLookup
from transport import ProcessExtractor
from agent_contract.advisory_lookup_v1.runtime import IntegrityError
from test_lookup import Index,Q,CORE

class IntegrityReuseTests(unittest.TestCase):
    def worker(self,body):
        d=tempfile.TemporaryDirectory(dir=Path(__file__).parent/'test-output');self.addCleanup(d.cleanup)
        p=Path(d.name)/'worker.py';p.write_text(body);return [sys.executable,'-B',str(p)]
    def test_loading_integrity_failure_remains_hard_on_reuse(self):
        calls=[]
        def factory():calls.append(1);raise IntegrityError('known checkpoint mismatch')
        index=Index();service=AdvisoryLookup(index,factory)
        for _ in range(2):
            with self.assertRaisesRegex(IntegrityError,'known checkpoint mismatch'):service.lookup(Q,CORE)
        self.assertEqual(calls,[1]);self.assertEqual(index.calls,[])
    def test_inference_integrity_failure_remains_hard_on_reuse(self):
        calls=[]
        def extract(text):
            calls.append(1)
            if len(calls)==1:raise IntegrityError('known inference mismatch')
            return {'entities':{}}
        index=Index();service=AdvisoryLookup(index,lambda:extract)
        for _ in range(2):
            with self.assertRaisesRegex(IntegrityError,'known inference mismatch'):service.lookup(Q,CORE)
        self.assertEqual(calls,[1]);self.assertEqual(index.calls,[])
    def test_remote_integrity_failure_survives_closed_worker(self):
        command=self.worker("import json,sys\nprint(json.dumps({'ready':True,'parameters':{'w':'old'},'load_seconds':0}),flush=True)\nfor line in sys.stdin:\n r=json.loads(line);print(json.dumps({'id':r['id'],'error_type':'IntegrityError','error':'remote mismatch'}),flush=True)")
        worker=ProcessExtractor(command=command,timeout=2);self.addCleanup(worker.close)
        with self.assertRaises(IntegrityError):worker.verify_unchanged()
        with self.assertRaisesRegex(IntegrityError,'remote mismatch'):worker('later request')
    def test_local_integrity_failure_closes_and_remains_hard(self):
        command=self.worker("import json,sys\nprint(json.dumps({'ready':True,'parameters':{'w':'old'},'load_seconds':0}),flush=True)\nfor line in sys.stdin:\n r=json.loads(line);print(json.dumps({'id':r['id'],'result':{'parameters':{'w':'new'},'checks':{'parameters_unchanged':True}}}),flush=True)")
        worker=ProcessExtractor(command=command,timeout=2);self.addCleanup(worker.close)
        with self.assertRaises(IntegrityError):worker.verify_unchanged()
        self.assertIsNotNone(worker.process.poll())
        with self.assertRaises(IntegrityError):worker('later request')

if __name__=='__main__':unittest.main()
