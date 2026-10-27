import asyncio
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('smoke',Path(__file__).with_name('installed_smoke.py'))
smoke=importlib.util.module_from_spec(spec);spec.loader.exec_module(smoke)

class SmokeTests(unittest.TestCase):
    def test_preflight_rejects_unpromoted_database_and_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'build').mkdir();(root/'build/knowledge.sqlite').write_bytes(b'fixture')
            digest=hashlib.sha256(b'fixture').hexdigest()
            for name,ident in smoke.MANIFESTS.items():
                p=root/name;p.parent.mkdir(exist_ok=True)
                p.write_text(json.dumps(dict(id=ident,files={'build/knowledge.sqlite':digest},knowledge=dict(facts=192,documents=36,promotion='knowledge-expansion/promotion-v13'))))
            self.assertEqual(smoke.installed_preflight(root,digest)['database_sha256'],digest)
            (root/'build/knowledge.sqlite').write_bytes(b'old')
            with self.assertRaises(ValueError):smoke.installed_preflight(root,digest)
            (root/'build/knowledge.sqlite').write_bytes(b'fixture')
            p=root/'mcp_runtime/model-free.json';m=json.loads(p.read_text());m['id']='old';p.write_text(json.dumps(m))
            with self.assertRaises(ValueError):smoke.installed_preflight(root,digest)

    def test_backed_calls_have_exact_scope_without_plan(self):
        rows=[dict(id=i,tool='lookup_formly',arguments=dict(request=i,plan={'questions':[]},formly_version='7' if i=='CONTROL-01' else '6.3.12')) for i in smoke.BACKED_IDS]
        calls=smoke.model_backed_calls(rows)
        self.assertEqual([x['id'] for x in calls],list(smoke.BACKED_IDS))
        self.assertTrue(all('plan' not in x['arguments'] for x in calls))
        self.assertEqual(calls[-1]['arguments']['formly_version'],'7')
        with self.assertRaises(ValueError):smoke.model_backed_calls(rows[:-1])

    def test_exact_result_identity_and_incomplete_delivery(self):
        expected=[dict(id='a',result={'isError':False,'content':[1]})]
        smoke.check_results(expected,expected)
        with self.assertRaises(ValueError):smoke.check_results([],expected)
        with self.assertRaises(ValueError):smoke.check_results([dict(id='a',result={'isError':False,'content':[2]})],expected)

    def test_launcher_offline_guard_and_seed(self):
        free=smoke.launcher_args('model-free',1701,Path('/tmp/output'))
        self.assertIn(str(smoke.POC/'model_free_v1/offline_guard.py'),free)
        self.assertNotIn('--seed',free)
        backed=smoke.launcher_args('model-backed',1702,Path('/tmp/output'))
        self.assertNotIn(str(smoke.POC/'model_free_v1/offline_guard.py'),backed)
        self.assertEqual(backed[-2:],['--seed','1702'])

    def test_run_refuses_before_promotion_without_output(self):
        with tempfile.TemporaryDirectory() as d, patch.object(smoke,'HERE',Path(d)), patch.object(smoke,'installed_preflight',side_effect=ValueError('not promoted')):
            with self.assertRaisesRegex(ValueError,'not promoted'):
                asyncio.run(smoke.run('model-free',1701,'refused'))
            self.assertFalse((Path(d)/'test-output').exists())

    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as d, patch.object(smoke,'HERE',Path(d)), patch.object(smoke,'installed_preflight',return_value={}), patch.object(smoke,'candidate_rows',return_value=[]):
            out=Path(d)/'test-output'/'retained';out.mkdir(parents=True)
            sentinel=out/'calls.json';sentinel.write_text('original')
            with self.assertRaises(FileExistsError):asyncio.run(smoke.run('model-free',1701,'retained'))
            self.assertEqual(sentinel.read_text(),'original')

    def test_candidate_packet_order_counts_and_seal(self):
        rows=smoke.candidate_rows()
        self.assertEqual(len(rows),44)
        self.assertEqual(len({r['id'] for r in rows}),40)
        self.assertEqual([r['id'] for r in rows if r['tool']!='lookup_formly'],['API-01','CONFIG-11','REGRESSION-05','REGRESSION-07'])
        self.assertLess(next(i for i,r in enumerate(rows) if r['id']=='CONTROL-01'),next(i for i,r in enumerate(rows) if r['id']=='REGRESSION-01'))

if __name__=='__main__':unittest.main()
