"""Byte-only prior-state audit, including qualification1."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent_contract.qualification_v1.preserve import snapshot as previous_snapshot, verify

def snapshot():
    result=previous_snapshot()
    manifest=Path(__file__).resolve().parent.parent/'qualification_v1/test-output/final-freeze.json'
    result[str(manifest)]=verify(manifest)
    return result

if __name__=='__main__':
    print(json.dumps(snapshot(),indent=2))
