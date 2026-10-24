"""Hash-only prior experiment preservation, including sealed files."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent_contract.retrieval_integration_v1.preserve import snapshot as previous_snapshot,verify

def snapshot():
 result=previous_snapshot()
 manifest=Path(__file__).resolve().parent.parent/'retrieval_integration_v1/test-output/final-freeze.json'
 result[str(manifest)]=verify(manifest)
 return result
if __name__=='__main__':print(json.dumps(snapshot(),indent=2))
