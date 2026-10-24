import json,sys,tempfile,unittest
from pathlib import Path
from transport import ProcessExtractor

class TransportTests(unittest.TestCase):
    def worker(self,body):
        d=tempfile.TemporaryDirectory(dir=Path(__file__).parent/'test-output');self.addCleanup(d.cleanup)
        p=Path(d.name)/'worker.py';p.write_text(body)
        return [sys.executable,'-B',str(p)]
    def test_actual_json_pipe_roundtrip_and_close(self):
        command=self.worker('''import json,sys
print(json.dumps({'ready':True,'parameters':{'w':'hash'},'load_seconds':0}),flush=True)
for line in sys.stdin:
 r=json.loads(line)
 value={'entities':{}} if r['op']=='extract' else {'parameters':{'w':'hash'},'checks':{'parameters_unchanged':True}}
 print(json.dumps({'id':r['id'],'result':value}),flush=True)
''')
        c=ProcessExtractor(command=command,timeout=2);self.addCleanup(c.close)
        self.assertEqual(c('full question'),{'entities':{}});self.assertEqual(c.before,{'w':'hash'})
        self.assertTrue(c.verify_unchanged()['parameters_unchanged']);self.assertEqual(c.after,c.before)
        c.close();self.assertIsNotNone(c.process.poll())
    def test_startup_failure_is_explicit(self):
        with self.assertRaises(RuntimeError):ProcessExtractor(command=self.worker("raise RuntimeError('bad startup')"),timeout=2)
    def test_invalid_response_closes_worker(self):
        c=ProcessExtractor(command=self.worker("import json,sys\nprint(json.dumps({'ready':True,'parameters':{},'load_seconds':0}),flush=True)\nfor line in sys.stdin:print('{}',flush=True)"),timeout=2);self.addCleanup(c.close)
        with self.assertRaises(RuntimeError):c('q')
        self.assertIsNotNone(c.process.poll())
    def test_timeout_closes_worker(self):
        with self.assertRaises(TimeoutError):ProcessExtractor(command=self.worker('import time\ntime.sleep(10)'),timeout=.05)
    def test_native_error_is_reported(self):
        c=ProcessExtractor(command=self.worker("import json,sys\nprint(json.dumps({'ready':True,'parameters':{},'load_seconds':0}),flush=True)\nfor line in sys.stdin:\n r=json.loads(line);print(json.dumps({'id':r['id'],'error':'native failure'}),flush=True)"),timeout=2);self.addCleanup(c.close)
        with self.assertRaisesRegex(RuntimeError,'native failure'):c('q')

if __name__=='__main__':unittest.main()
