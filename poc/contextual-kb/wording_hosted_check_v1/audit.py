"""Read-only verification of authorized real-selector and calling-agent runs."""
import json,os,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parent
sys.path.insert(0,str(POC))
from agent_contract.advisory_lookup_v1.lookup import AdvisoryLookup
from agent_contract.retrieval_integration_v1.bridge import readonly
from kbcompiler.question_pilot import PilotIndex
from mcp_v1.backend import citations_for
from wording_candidate_v1.candidate import normalize
from agent_contract.qualification_v3.candidate import build_plan
from retrieval_repair_v1.preserve import snapshot
from retrieval_repair_v1.experiment import verify
from retrieval_repair_v1.policy import apply_repair

def read(path):return json.loads(path.read_text())
def main():
    verify(HERE/'test-output/harness-freeze.json')
    for name in ('retrieval_repair_v1','wording_candidate_v1'):verify(POC/name/'test-output/final-freeze.json')
    expected=read(HERE/'test-output/protected-before.json');assert snapshot()==expected
    os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(POC/'agent_contract/advisory_lookup_v1/test-output/embed-cache'),HF_HUB_OFFLINE='1')
    rows=[];receipts=[]
    with readonly(POC/'build/knowledge.sqlite') as db:
        index=PilotIndex(db);baseline=AdvisoryLookup(index,None)
        def check(packet,request,seed,case,kind,selector_root,seconds=None,answer=None):
            core=packet['plan']['question_plan'];build_plan(request,core)
            normalization=packet['generation']['wording_normalization']
            canonical,audit=normalize(request,normalization['original_plan'])
            assert canonical==core and audit==normalization
            original=baseline.lookup(request,core)
            assert packet['retrieval']['foundation_ids']==original['retrieval']['ids']
            for k in ('queries','questions','query_count'):assert packet['retrieval'][k]==original['retrieval'][k]
            assert packet['plan']['search_requests']==original['plan']['search_requests']
            ids=packet['retrieval']['ids'];old=packet['retrieval']['foundation_ids']
            assert len(ids)==len(set(ids))<=8 and len(set(ids)-set(old))<=2
            assert packet['facts']==[index.facts[f] for f in ids]
            assert packet['citations']==citations_for(db,ids)
            assert packet['runtime']['db_unchanged'] and packet['runtime']['extractor_seed']==seed
            checks=packet['runtime']['model_checks'];assert checks and all(c['parameters_unchanged'] for c in checks)
            assert packet['advisory']['status']=='available'
            selection=packet['selection'];assert selection['status'] in {'unchanged','repaired'},selection
            for q in selection['queries']:
                assert q['depth']==20 and q['text']==core['formly_questions'][q['question_index']]['question']
            # Reconstruct the exact hosted input, then replay its decision.
            from retrieval_repair_v1.policy import present
            union=list(dict.fromkeys(old+[f for q in selection['queries'] for f in q['ids']]))
            payload,mapping=present(core,old,union,index.facts,lambda f:db.execute('SELECT source_quote FROM facts WHERE id=?',(f,)).fetchone()[0])
            assert mapping==selection['mapping']
            exact=[p.parent for p in selector_root.glob('*/input.json') if read(p)==payload]
            assert len(exact)==1,(kind,case,len(exact))
            decision=read(exact[0]/'decision.json');assert apply_repair(decision,payload,mapping)==ids
            receipt=read(exact[0]/'receipt.json');assert receipt['exit_code']==0 and receipt['error'] is None
            receipts.append(str(exact[0]));
            if answer is not None:assert set(answer['cited_fact_ids'])<=set(ids)
            rows.append(dict(kind=kind,seed=seed,id=case,rewrites=len(audit['rewrites']),selection_status=selection['status'],added=sorted(set(ids)-set(old)),seconds=seconds,selector_seconds=receipt['seconds'],answer=answer,checks_pass=True))
        saved=read(POC/'retrieval_repair_v1/test-output/fresh/F01.json')
        for seed in (1701,1702):
            root=HERE/'test-output/saved'
            check(read(root/f'{seed}.json'),saved['request'],seed,'F01','saved',root/str(seed)/'selector')
            root=HERE/f'test-output/native/{seed}'
            assert read(root/'receipt.json')['exit_code']==0
            events=[json.loads(line) for line in (root/'events.jsonl').read_text().splitlines()]
            calls=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='mcp_tool_call']
            messages=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
            answers=json.loads(messages[-1])['answers'];audits=[read(p) for p in (root/'audit').glob('*.json')];cases=read(root/'prompt.json')
            assert len(calls)==len(answers)==len(audits)==len(cases)==4
            for case in cases:
                call,=[c for c in calls if c['arguments']=={'request':case['request']}]
                audit,=[a for a in audits if a['request']==case['request']]
                answer,=[a for a in answers if a['id']==case['id']]
                assert call['server']=='formly' and call['tool']=='lookup_formly' and call['error'] is None and call['status']=='completed'
                packet=call['result']['structured_content'];assert packet==audit['result']
                attempt=root/'runtime/planner'/packet['generation']['attempt_id']
                raw_events=[json.loads(line) for line in (attempt/'events.jsonl').read_text().splitlines()]
                raw_messages=[e['item']['text'] for e in raw_events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
                assert len(raw_messages)==1 and json.loads(raw_messages[0])==packet['generation']['wording_normalization']['original_plan']
                check(packet,case['request'],seed,case['id'],'calling-agent',root/'runtime/selector',audit['seconds'],answer)
    assert len(set(receipts))==10
    assert snapshot()==expected
    for name in ('retrieval_repair_v1','wording_candidate_v1'):verify(POC/name/'test-output/final-freeze.json')
    summary=dict(checks_pass=True,packets=len(rows),hosted_selector_calls=len(receipts),rows=rows)
    with (HERE/'test-output/audit.json').open('x') as f:json.dump(summary,f,indent=2)
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
