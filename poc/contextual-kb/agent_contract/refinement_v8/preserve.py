"""Byte-only frozen-state audit. Never interpret sealed payloads."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent_contract.refinement_v7.preserve import snapshot as previous_snapshot,verify

def snapshot():
    result=previous_snapshot()
    manifest=Path(__file__).resolve().parent.parent/'refinement_v7/test-output/final-freeze.json'
    result[str(manifest)]=verify(manifest)
    return result

if __name__=='__main__':print(json.dumps(snapshot(),indent=2))
