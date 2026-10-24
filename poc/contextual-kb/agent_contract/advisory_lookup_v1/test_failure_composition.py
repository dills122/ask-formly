import contextlib,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import cli
import verify_live
from test_lookup import Index,Q,CORE,native

class Extractor:
    instances=[]
    def __init__(self,seed):self.closed=False;self.before={'w':'hash'};self.after=None;self.instances.append(self)
    def __call__(self,text):raise RuntimeError('worker failed')
    def verify_unchanged(self):raise RuntimeError('worker unavailable')
    def close(self):self.closed=True

class FailureCompositionTests(unittest.TestCase):
    def test_cli_keeps_full_retrieval_when_worker_and_final_check_fail(self):
        index=Index()
        with patch.object(cli,'ProcessExtractor',Extractor),patch.object(cli,'PilotIndex',lambda _:index),patch.object(cli,'readonly',lambda _:contextlib.nullcontext(None)),patch.object(cli,'digest',lambda _:'unchanged'):
            result=cli.run(Q,CORE)
        self.assertEqual(result['retrieval']['ids'],list(index.facts));self.assertEqual(result['advisory']['status'],'degraded')
        self.assertIsNone(result['runtime']['model_checks'][0]['parameters_unchanged'])
        self.assertTrue(Extractor.instances[-1].closed)
        self.assertTrue(any('verification' in x for x in result['advisory']['diagnostics']))
    def test_final_check_failure_is_not_claimed_unchanged(self):
        class CheckFailure(Extractor):
            def __call__(self,text):return native()
        with patch.object(cli,'ProcessExtractor',CheckFailure),patch.object(cli,'PilotIndex',lambda _:Index()),patch.object(cli,'readonly',lambda _:contextlib.nullcontext(None)),patch.object(cli,'digest',lambda _:'unchanged'):
            result=cli.run(Q,CORE)
        self.assertEqual(result['advisory']['status'],'degraded');self.assertIsNone(result['runtime']['model_checks'][0]['parameters_unchanged'])
    def test_harness_session_closes_worker_on_body_failure(self):
        class Good(Extractor):
            def __call__(self,text):return native()
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent/'test-output') as d,patch.object(verify_live,'ProcessExtractor',Good):
            with self.assertRaisesRegex(RuntimeError,'body failed'):
                with verify_live.model_session(Index(),1701,Path(d)) as (service,loaded):
                    service.lookup(Q,CORE);self.assertEqual(len(loaded),1);raise RuntimeError('body failed')
        self.assertTrue(Good.instances[-1].closed)

if __name__=='__main__':unittest.main()
