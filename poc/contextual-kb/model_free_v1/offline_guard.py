"""Test-only enforcement wrapper, not a production launcher or model substitute."""
import importlib.abc
import os
import runpy
import sys

class NoModels(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in {'torch','numpy','onnxruntime','fastembed','gliner','gliner2','transformers','sentence_transformers'}:
            raise RuntimeError('Model dependency attempted: '+fullname)

sys.meta_path.insert(0,NoModels())
# Parent stdio transport creates the server process; inside this process no further
# process launches, external networking, DNS, or model-cache access are permitted.
def audit(event,args):
    if event in {'subprocess.Popen','os.system','os.posix_spawn','os.exec','socket.connect','socket.getaddrinfo','socket.bind','socket.sendto'}:
        raise RuntimeError('Offline guard denied '+event)
    if event=='open' and isinstance(args[0],str) and any(s in args[0] for s in ('/models/','/embed-cache/','/huggingface/')):
        raise RuntimeError('Model asset access denied')
sys.addaudithook(audit)
for key in list(os.environ):
    if any(s in key for s in ('TOKEN','API_KEY','CREDENTIAL','ANTHROPIC','OPENAI','AWS_','AZURE_')):os.environ.pop(key,None)
print('OFFLINE_GUARDS_ACTIVE',file=sys.stderr)
sys.argv=sys.argv[1:]
runpy.run_path(sys.argv[0],run_name='__main__')
