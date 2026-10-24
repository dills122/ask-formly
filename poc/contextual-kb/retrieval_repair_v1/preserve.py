import json,sys,hashlib
from pathlib import Path
POC=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(POC))
from mcp_v1.preserve import snapshot as previous,verify

def snapshot():
    result=previous()
    manifest=POC/'mcp_v1/test-output/final-freeze.json'
    result[str(manifest)]=verify(manifest)
    for path in sorted((POC/'mcp_diagnosis_v1').glob('*')):
        if path.is_file():result[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
    return result
if __name__=='__main__':print(json.dumps(snapshot(),indent=2))
