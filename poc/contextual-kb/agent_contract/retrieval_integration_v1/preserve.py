"""Hash-only preservation of all prior experiment artifacts."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent_contract.gliner_integration_v1.preserve import snapshot as previous_snapshot,verify

def snapshot():
 result=previous_snapshot()
 manifest=Path(__file__).resolve().parent.parent/'gliner_integration_v1/test-output/final-freeze.json'
 result[str(manifest)]=verify(manifest)
 return result
if __name__=='__main__':print(json.dumps(snapshot(),indent=2))
