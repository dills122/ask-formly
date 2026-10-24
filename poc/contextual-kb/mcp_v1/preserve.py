"""Hash-only preservation, never interpret sealed evaluation content."""
import json,sys
from pathlib import Path
POC=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(POC))
from agent_contract.advisory_lookup_v1.preserve import snapshot as previous_snapshot,verify

def snapshot():
    result=previous_snapshot()
    for name in ['final-freeze.json','closeout-freeze.json']:
        path=POC/'agent_contract/advisory_lookup_v1/test-output'/name
        result[str(path)]=verify(path)
    return result
if __name__=='__main__':print(json.dumps(snapshot(),indent=2))
