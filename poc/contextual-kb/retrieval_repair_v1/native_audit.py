"""Read-only audit of the six real MCP calls; no generation or resampling."""
import json, os, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; POC=HERE.parent
sys.path.insert(0,str(POC))
from agent_contract.advisory_lookup_v1.lookup import AdvisoryLookup
from agent_contract.retrieval_integration_v1.bridge import readonly
from kbcompiler.question_pilot import PilotIndex
from mcp_v1.backend import citations_for
from retrieval_repair_v1.preserve import snapshot
from retrieval_repair_v1.experiment import verify

def main():
    read=lambda p:json.loads(p.read_text())
    verify(HERE/'test-output/design-freeze.json')
    assert snapshot()==read(HERE/'test-output/protected-before.json')
    os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(POC/'agent_contract/advisory_lookup_v1/test-output/embed-cache'),HF_HUB_OFFLINE='1')
    rows=[]
    with readonly(POC/'build/knowledge.sqlite') as db:
        index=PilotIndex(db); baseline=AdvisoryLookup(index,None)
        for seed in (1701,1702):
            root=HERE/f'test-output/native/{seed}'
            assert read(root/'receipt.json')['exit_code']==0
            events=[json.loads(line) for line in (root/'events.jsonl').read_text().splitlines()]
            calls=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='mcp_tool_call']
            messages=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
            answers=json.loads(messages[-1])['answers']
            audits=[read(p) for p in (root/'audit').glob('*.json')]
            cases=read(root/'prompt.json')
            assert len(calls)==len(answers)==len(audits)==len(cases)==3
            for case in cases:
                call,=[c for c in calls if c['arguments']=={'request':case['request']}]
                audit,=[a for a in audits if a['request']==case['request']]
                answer,=[a for a in answers if a['id']==case['id']]
                packet=call['result']['structured_content']; core=packet['plan']['question_plan']
                assert call['error'] is None and call['status']=='completed' and packet==audit['result']
                assert call['server']=='formly' and call['tool']=='lookup_formly'
                before=baseline.lookup(case['request'],core)
                assert packet['retrieval']['foundation_ids']==before['retrieval']['ids']
                for key in ('queries','questions','query_count'):assert packet['retrieval'][key]==before['retrieval'][key]
                assert packet['plan']['search_requests']==before['plan']['search_requests']
                ids=packet['retrieval']['ids']; old=packet['retrieval']['foundation_ids']
                assert len(ids)==len(set(ids))<=8 and len(set(ids)-set(old))<=2
                assert packet['facts']==[index.facts[f] for f in ids]
                assert packet['citations']==citations_for(db,ids)
                assert set(answer['cited_fact_ids'])<=set(ids)
                assert packet['runtime']['db_unchanged']
                assert packet['runtime']['extractor_seed']==seed
                assert packet['runtime']['model_checks'] and all(c['parameters_unchanged'] for c in packet['runtime']['model_checks'])
                for q in packet['selection']['queries']:
                    assert q['text']==core['formly_questions'][q['question_index']]['question'] and q['depth']==20
                rows.append(dict(seed=seed,id=case['id'],answer=answer,selection_status=packet['selection']['status'],added=sorted(set(ids)-set(old)),seconds=audit['seconds'],selector_seconds=packet['selection']['seconds'],baseline_parity=True,delivery_parity=True,stored_facts_and_citations=True,model_preserved=True))
    assert snapshot()==read(HERE/'test-output/protected-before.json')
    summary=dict(calls=len(rows),mechanical_checks_pass=True,replacements=sum(bool(r['added']) for r in rows),rows=rows,limitation='Live generated plans already retrieved callback context; native calls validate serving, not a causal replacement gain.')
    with (HERE/'test-output/native/audit-summary.json').open('x') as f:json.dump(summary,f,indent=2)
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
