import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
import harness

class HarnessTests(unittest.TestCase):
    def test_actual_guarded_entrypoint_imports_before_help(self):
        result=subprocess.run([sys.executable,"-B",str(harness.POC/"model_free_v1/offline_guard.py"),str(harness.HERE/"server.py"),"--help"],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn("OFFLINE_GUARDS_ACTIVE",result.stderr)

    def test_only_frozen_arms(self):
        with self.assertRaises(ValueError):harness.database('auto')
        self.assertEqual(harness.database('baseline')[0],harness.POC/'build/knowledge.sqlite')
        self.assertNotEqual(harness.database('candidate')[0],harness.POC/'build/knowledge.sqlite')
    def test_calls_allowlist_and_required_fields(self):
        for row in [{},{'tool':'shell','arguments':{}},{'tool':'lookup_formly','arguments':{}}]:
            with self.assertRaises(ValueError):harness.validate_call(row)
        row={'id':'J01','tool':'lookup_formly','arguments':{'request':'q'}}
        self.assertEqual(harness.validate_call(row),row)
    def test_new_output_cannot_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'new'/'calls.json';harness.reserve(p)
            with self.assertRaises(FileExistsError):harness.reserve(p)
    def test_receipt_counts_errors_and_missing_attempts(self):
        calls=[{'id':'a'},{'id':'b'},{'id':'c'}]
        r=harness.receipt(calls,[{'id':'a','operational_or_tool_error':False},{'id':'b','operational_or_tool_error':True}])
        self.assertEqual(r,{'expected':3,'attempted':2,'errors':1,'unattempted':['c']})
if __name__=='__main__':unittest.main()
