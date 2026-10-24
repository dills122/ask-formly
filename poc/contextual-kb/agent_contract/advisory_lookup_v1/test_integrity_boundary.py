import contextlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import cli
from agent_contract.advisory_lookup_v1 import runtime
from lookup import AdvisoryLookup
from agent_contract.advisory_lookup_v1.runtime import IntegrityError
from transport import ProcessExtractor
from test_lookup import CORE,Q,Index,native

class IntegrityBoundaryTests(unittest.TestCase):
    def worker(self,body):
        d=tempfile.TemporaryDirectory(dir=Path(__file__).parent/'test-output');self.addCleanup(d.cleanup)
        p=Path(d.name)/'worker.py';p.write_text(body);return [sys.executable,'-B',str(p)]
    def test_startup_integrity_mismatch_is_hard_error(self):
        command=self.worker("import json\nprint(json.dumps({'ready':False,'error_type':'IntegrityError','error':'checkpoint mismatch'}),flush=True)")
        with self.assertRaises(IntegrityError):ProcessExtractor(command=command,timeout=2)
    def test_remote_verification_integrity_mismatch_is_hard_error(self):
        command=self.worker("import json,sys\nprint(json.dumps({'ready':True,'parameters':{'w':'old'},'load_seconds':0}),flush=True)\nfor line in sys.stdin:\n r=json.loads(line);print(json.dumps({'id':r['id'],'error_type':'IntegrityError','error':'changed parameters'}),flush=True)")
        e=ProcessExtractor(command=command,timeout=2);self.addCleanup(e.close)
        with self.assertRaises(IntegrityError):e.verify_unchanged()
        self.assertIsNotNone(e.process.poll())
    def test_local_before_after_mismatch_is_hard_error(self):
        command=self.worker("import json,sys\nprint(json.dumps({'ready':True,'parameters':{'w':'old'},'load_seconds':0}),flush=True)\nfor line in sys.stdin:\n r=json.loads(line);print(json.dumps({'id':r['id'],'result':{'parameters':{'w':'changed'},'checks':{'parameters_unchanged':True}}}),flush=True)")
        e=ProcessExtractor(command=command,timeout=2);self.addCleanup(e.close)
        with self.assertRaises(IntegrityError):e.verify_unchanged()
    def test_native_verifier_uses_typed_integrity_failure(self):
        e=object.__new__(runtime.FrozenExtractor);e.model=object();e.before={'w':'old'}
        with patch.object(runtime,'parameter_hashes',lambda _: {'w':'changed'}):
            with self.assertRaises(IntegrityError):e.verify_unchanged()
    def test_lookup_does_not_soften_observed_loading_mismatch(self):
        def factory():raise IntegrityError('checkpoint mismatch')
        i=Index()
        with self.assertRaises(IntegrityError):AdvisoryLookup(i,factory).lookup(Q,CORE)
        self.assertEqual(i.calls,[])
    def test_lookup_does_not_soften_observed_inference_mismatch(self):
        def extract(text):raise IntegrityError('observed inference integrity failure')
        i=Index()
        with self.assertRaises(IntegrityError):AdvisoryLookup(i,lambda:extract).lookup(Q,CORE)
        self.assertEqual(i.calls,[])
    def test_cli_does_not_soften_observed_verification_mismatch(self):
        instances=[]
        class Extractor:
            def __init__(self,seed):self.closed=False;instances.append(self)
            def __call__(self,text):return native()
            def verify_unchanged(self):raise IntegrityError('observed changed parameters')
            def close(self):self.closed=True
        with patch.object(cli,'ProcessExtractor',Extractor),patch.object(cli,'PilotIndex',lambda _:Index()),patch.object(cli,'readonly',lambda _:contextlib.nullcontext(None)),patch.object(cli,'digest',lambda _:'unchanged'):
            with self.assertRaises(IntegrityError):cli.run(Q,CORE)
        self.assertTrue(instances[0].closed)

    def test_real_pipe_integrity_failure_propagates_through_cli(self):
        command=self.worker("import json,sys\nprint(json.dumps({'ready':True,'parameters':{'w':'old'},'load_seconds':0}),flush=True)\nfor line in sys.stdin:\n r=json.loads(line)\n result={'id':r['id'],'result':{'entities':{}}} if r['op']=='extract' else {'id':r['id'],'error_type':'IntegrityError','error':'observed mismatch'}\n print(json.dumps(result),flush=True)")
        workers=[]
        def factory(seed):
            worker=ProcessExtractor(seed,command=command,timeout=2);workers.append(worker);return worker
        with patch.object(cli,'ProcessExtractor',factory),patch.object(cli,'PilotIndex',lambda _:Index()),patch.object(cli,'readonly',lambda _:contextlib.nullcontext(None)),patch.object(cli,'digest',lambda _:'unchanged'):
            with self.assertRaises(IntegrityError):cli.run(Q,CORE)
        self.assertIsNotNone(workers[0].process.poll())

if __name__=='__main__':unittest.main()
