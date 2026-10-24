"""Replay exposed development plans only; no generation or sealed content reads."""
import hashlib,json,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parent
sys.path.insert(0,str(POC))
from wording_candidate_v1.candidate import normalize
from agent_contract.qualification_v3.candidate import build_plan
from retrieval_repair_v1.preserve import snapshot
from retrieval_repair_v1.experiment import verify

def main():
    verify(POC/'retrieval_repair_v1/test-output/final-freeze.json')
    expected=json.loads((POC/'retrieval_repair_v1/test-output/protected-before.json').read_text())
    assert snapshot()==expected
    inputs=json.loads((POC/'retrieval_repair_v1/test-output/panel/inputs.json').read_text())
    rows=[]
    for row in inputs:
        before=json.dumps(row['core'],sort_keys=True)
        try:build_plan(row['request'],row['core']);old_error=None
        except ValueError as e:old_error=str(e)
        start=time.perf_counter()
        result,audit=normalize(row['request'],row['core'])
        elapsed=time.perf_counter()-start
        build_plan(row['request'],result)
        assert before==json.dumps(row['core'],sort_keys=True)
        if old_error is None:assert result==row['core'] and not audit['rewrites']
        else:assert row['id'].startswith('F01-') and len(audit['rewrites'])==1
        rows.append(dict(id=row['id'],old_error=old_error,accepted=True,rewrites=audit['rewrites'],seconds=elapsed))
    summary=dict(slots=len(rows),unchanged=sum(not r['rewrites'] for r in rows),repaired=sum(bool(r['rewrites']) for r in rows),distinct_repaired_outputs=1,scope='Structural replay only; not new retrieval/answer qualification',rows=rows)
    with (HERE/'test-output/replay.json').open('x') as f:json.dump(summary,f,indent=2)
    assert snapshot()==expected
    with (HERE/'test-output/protected-before.json').open('x') as f:json.dump(expected,f,indent=2)
    print(json.dumps({k:v for k,v in summary.items() if k!='rows'}))
if __name__=='__main__':main()
