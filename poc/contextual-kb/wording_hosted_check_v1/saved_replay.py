"""Saved raw-plan replay through real frozen extractors and candidate backend, with the actual hosted selector (explicit user approval).

No new foundation generation: this isolates the normalization of the known failure.
"""
import asyncio,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parent
sys.path.insert(0,str(POC))
from wording_candidate_v1.serve import make_service
from retrieval_repair_v1.integration import Backend
from retrieval_repair_v1.preserve import snapshot
from retrieval_repair_v1.experiment import verify

async def main():
    expected=json.loads((POC/'wording_candidate_v1/test-output/protected-before.json').read_text())
    assert snapshot()==expected
    verify(POC/'retrieval_repair_v1/test-output/final-freeze.json')
    row=json.loads((POC/'retrieval_repair_v1/test-output/fresh/F01.json').read_text())
    root=HERE/'test-output/saved';root.mkdir()
    summary=[]
    for seed in (1701,1702):
        service=make_service(seed,root/str(seed),planner=lambda _: (row['core'],{'source':'saved-F01-replay-not-new-generation'}))
        try:
            result=await service.lookup(row['request'])
            with (root/f'{seed}.json').open('x') as f:json.dump(result,f,indent=2)
            assert len(result['generation']['wording_normalization']['rewrites'])==1
            assert result['generation']['wording_normalization']['original_plan']==row['core']
            for q,query in zip(result['plan']['question_plan']['formly_questions'],result['plan']['search_requests']):assert q['question']==query['query']
            assert result['runtime']['db_unchanged']
            assert result['runtime']['model_checks'] and all(c['parameters_unchanged'] for c in result['runtime']['model_checks'])
            assert result['advisory']['status']=='available',result['advisory']
            assert len(result['retrieval']['ids'])<=8
            assert result['selection']['status'] in {'unchanged','repaired'},result['selection']
            summary.append(dict(selector_mode='actual hosted selector',seed=seed,selector_status=result['selection']['status'],ids=result['retrieval']['ids'],parameters_unchanged=True))
        finally:await service.close()
    assert snapshot()==expected
    verify(POC/'retrieval_repair_v1/test-output/final-freeze.json')
    with (root/'summary.json').open('x') as f:json.dump(summary,f,indent=2)
    print(json.dumps(summary))
if __name__=='__main__':asyncio.run(main())
