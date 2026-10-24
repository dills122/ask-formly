"""Verify frozen prior artifacts by bytes, without opening sealed cases semantically."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent_contract.v3_stress.audit import audit,verify


def snapshot():
    result=audit()
    previous=Path(__file__).resolve().parent.parent/'v3_stress/test-output/final-freeze.json'
    result[str(previous)]=verify(previous)
    return result


if __name__=='__main__':
    print(json.dumps(snapshot(),indent=2))
