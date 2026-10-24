"""Read-only protection chain; no semantic inspection of sealed payloads."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent_contract.refinement_v5.preserve import snapshot as previous_snapshot,verify

def snapshot():
    result=previous_snapshot()
    manifest=Path(__file__).resolve().parent.parent/'refinement_v5/test-output/final-freeze.json'
    result[str(manifest)]=verify(manifest)
    return result

if __name__=='__main__':print(json.dumps(snapshot(),indent=2))
