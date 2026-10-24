import hashlib,json,tempfile,unittest
from pathlib import Path
from contextlib import ExitStack
from question_planners.experiment import verify_manifest, schedule, normalize, statistics, collect_samples


class ExperimentTests(unittest.TestCase):
    def test_manifest_detects_mutation(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'x').write_text('before')
            m={'x':hashlib.sha256(b'before').hexdigest()}
            verify_manifest(root,m)
            (root/'x').write_text('after')
            with self.assertRaises(ValueError): verify_manifest(root,m)

    def test_paired_schedule_is_reproducible_complete_and_alternating(self):
        a=schedule(['h1','h2'],5)
        self.assertEqual(a,schedule(['h1','h2'],5))
        self.assertEqual(len(a),20)
        for i in range(0,len(a),2):
            self.assertEqual(a[i][:2],a[i+1][:2])
            self.assertNotEqual(a[i][2],a[i+1][2])
        for case in ['h1','h2']:
            self.assertEqual(sum(x[1]==case and x[2]=='A' for x in a),5)

    def test_normalization_preserves_semantics(self):
        a={'question':'Q','status':'planned','aspects':[{'id':'a1'}],
           'requests':[{'id':'q1','aspect_ids':['a1'],'query':'not hidden'}], 'ambiguities':[]}
        b=json.loads(json.dumps(a));b['requests'][0]['query']='hidden'
        self.assertNotEqual(normalize(a),normalize(b))

    def test_nearest_rank_and_failed_samples_included(self):
        rows=[{'seconds':n,'plan':{'status':'failed','failure':{'code':'timeout'}}} for n in range(1,21)]
        s=statistics(rows)
        self.assertEqual(s['p95_seconds'],19)
        self.assertEqual(s['timeout_count'],20)
        self.assertEqual(s['samples'],20)

    def test_timeout_preserved_and_later_samples_continue_after_recorded_recovery(self):
        class Process:
            stopped=False
            def poll(self): return 1 if self.stopped else None
        calls=[]
        instances=[]
        class Fake:
            startup_seconds=.01
            def __init__(self,arm):
                self.arm=arm; self.process=Process(); instances.append(self)
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def query(self,question):
                calls.append((self.arm,question))
                timeout=question=='first' and self.arm=='A'
                if timeout:self.process.stopped=True
                return {'seconds':10 if timeout else .1,'trace':{},'plan':{
                    'status':'failed' if timeout else 'planned',
                    'failure':{'code':'timeout'} if timeout else None}}
        import io
        with ExitStack() as stack:
            workers={a:stack.enter_context(Fake(a)) for a in ['A','B']}
            meta={}; rows=[]
            jobs=[(0,'c1','A'),(0,'c1','B'),(0,'c2','A'),(0,'c2','B')]
            cases={'c1':{'question':'first'},'c2':{'question':'second'}}
            collect_samples(jobs,cases,workers,stack,io.StringIO(),meta,rows,factory=Fake)
        self.assertEqual(len(rows),4)
        self.assertEqual(rows[0]['plan']['failure']['code'],'timeout')
        self.assertEqual(calls.count(('A','first')),1)
        self.assertEqual(calls.count(('A','second')),1)
        self.assertEqual(len(meta['recoveries']),1)
        self.assertIn('warmup',meta['recoveries'][0])
        self.assertTrue(rows[2]['after_recovery'])

    def test_hardware_manifest_explicitly_reports_unavailable_fields(self):
        from question_planners.environment import hardware_snapshot
        from unittest.mock import patch
        with patch('subprocess.check_output',side_effect=OSError('unavailable')):
            snapshot=hardware_snapshot()
        self.assertEqual(snapshot['cpu'],'unavailable')
        self.assertEqual(snapshot['memory_bytes'],'unavailable')
