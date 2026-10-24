"""Byte-only preservation audit; sealed case content is never interpreted."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent_contract.refinement_v4.preserve import snapshot as prior_snapshot,verify


def snapshot():
    result=prior_snapshot()
    previous=Path(__file__).resolve().parent.parent/'refinement_v4/test-output/final-freeze.json'
    result[str(previous)]=verify(previous)
    return result


if __name__=='__main__':
    print(json.dumps(snapshot(),indent=2))
