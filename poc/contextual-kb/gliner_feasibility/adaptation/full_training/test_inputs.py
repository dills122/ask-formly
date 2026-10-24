import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from inputs import load_split, access_policy, load_manifest
from controller import bounded_process

HERE=Path(__file__).resolve().parent
class InputTests(unittest.TestCase):
    def test_forbidden_paths_and_db_are_rejected_without_open(self):
        check=access_policy(HERE.parents[4],[],HERE/'test-output',[])
        for path in [HERE/'sealed.json', HERE/'test-output/knowledge.db', HERE.parent/'pilot/unknown.json']:
            with self.subTest(path=path),self.assertRaises(PermissionError):check('open',(str(path),'r',0))
        with self.assertRaises(PermissionError):check('socket.connect',())
        with self.assertRaises(PermissionError):check('subprocess.Popen',())
        with self.assertRaises(PermissionError):check('open',(str(HERE.parent/'outside.txt'),'w',0))

    def test_only_fixed_split_paths_can_be_loaded(self):
        with tempfile.TemporaryDirectory(dir=HERE/'test-output') as td:
            root=Path(td); (root/'data').mkdir()
            data=json.dumps([{'id':'t1'}]).encode();(root/'data/train.json').write_bytes(data)
            spec={'path':'data/train.json','sha256':hashlib.sha256(data).hexdigest(),'count':1}
            self.assertEqual(load_split(root,spec,'train',expected_count=1),[{'id':'t1'}])
            for path in ['../sealed.json','data/evaluation.json','data/dev.json']:
                with self.assertRaises(ValueError):load_split(root,dict(spec,path=path),'train',expected_count=1)
            with self.assertRaises(ValueError):load_split(root,dict(spec,sha256='bad'),'train',expected_count=1)

    def test_manifest_does_not_accept_evaluation_content_or_missing_readiness(self):
        with tempfile.TemporaryDirectory(dir=HERE/'test-output') as td:
            root=Path(td);path=root/'manifest.json'
            for payload in [{}, {'evaluation':{'path':'sealed.json'}}]:
                path.write_text(json.dumps(payload))
                with self.assertRaises(ValueError):load_manifest(path)

    def test_controller_terminates_timeout_and_preserves_log(self):
        import sys
        with tempfile.TemporaryDirectory(dir=HERE/'test-output') as td:
            result=bounded_process([sys.executable,'-c','import time; print("started",flush=True); time.sleep(5)'],
                                   Path(td),.15)
            self.assertEqual(result['status'],'timeout')
            self.assertTrue((Path(td)/'worker.log').exists())
            self.assertTrue((Path(td)/'controller.json').exists())

if __name__=='__main__':unittest.main()
