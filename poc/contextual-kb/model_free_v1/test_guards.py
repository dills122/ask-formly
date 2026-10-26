import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE=Path(__file__).resolve().parent

class GuardTests(unittest.TestCase):
    def test_actual_network_process_and_model_attempts_are_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);probe=root/'probe.py'
            probe.write_text('''import json,socket,subprocess,sys
out=[]
for label,fn in [('network',lambda:socket.create_connection(('127.0.0.1',1))),('process',lambda:subprocess.run([sys.executable,'-c','pass'])),('model',lambda:__import__('numpy'))]:
 try: fn()
 except RuntimeError: out.append(label)
print(json.dumps(out))
''')
            run=subprocess.run([sys.executable,'-B',str(HERE/'offline_guard.py'),str(probe)],env={'HOME':tmp,'PATH':''},capture_output=True,text=True)
            self.assertEqual(0,run.returncode,run.stderr)
            self.assertEqual(['network','process','model'],json.loads(run.stdout))
