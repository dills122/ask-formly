"""Read-only audit of stable-launcher real-agent evidence."""
import json,os,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parent
sys.path.insert(0,str(POC))
from agent_contract.advisory_lookup_v1.lookup import AdvisoryLookup
from agent_contract.retrieval_integration_v1.bridge import readonly
from kbcompiler.question_pilot import PilotIndex
from mcp_v1.backend import citations_for
from wording_candidate_v1.candidate import normalize
from retrieval_repair_v1.policy import present,apply_repair
from retrieval_repair_v1.preserve import snapshot
from retrieval_repair_v1.experiment import verify

def read(p):return json.loads(p.read_text())
def events(p):return [json.loads(line) for line in p.read_text().splitlines()]
def messages(es):return [e['item']['text'] for e in es if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
def main():
    verify(HERE/'test-output/implementation-freeze-v2.json')
    for n in ('retrieval_repair_v1','wording_candidate_v1','wording_hosted_check_v1'):verify(POC/n/'test-output/final-freeze.json')
    assert snapshot()==read(HERE/'test-output/protected-before.json')
    os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(POC/'agent_contract/advisory_lookup_v1/test-output/embed-cache'),HF_HUB_OFFLINE='1')
    rows=[];hosted=[];workers=[]
    with readonly(POC/'build/knowledge.sqlite') as db:
        index=PilotIndex(db);baseline=AdvisoryLookup(index,None)
        for seed in (1701,1702):
            root=HERE/f'test-output/native/{seed}';assert read(root/'receipt.json')['exit_code']==0
            es=events(root/'events.jsonl');calls=[e['item'] for e in es if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='mcp_tool_call']
            answers=json.loads(messages(es)[-1])['answers'];audits=[read(p) for p in (root/'audit').glob('*.json')];cases=read(root/'prompt.json')
            assert len(calls)==len(answers)==len(audits)==len(cases)==4
            remaining=list(calls);logs=set()
            for case in cases:
                matches=[c for c in remaining if c['arguments']=={'request':case['request']}]
                assert matches;call=matches[0];remaining.remove(call)
                assert call['status']=='completed' and call['error'] is None and call['tool']=='lookup_formly' and call['server']=='formly'
                packet=call['result']['structured_content'];audit,=[a for a in audits if a.get('result')==packet];assert audit['request']==case['request']
                answer,=[a for a in answers if a['id']==case['id']]
                core=packet['plan']['question_plan'];normal=packet['generation']['wording_normalization']
                canonical,trace=normalize(case['request'],normal['original_plan']);assert canonical==core and trace==normal
                raw=messages(events(root/'runtime/planner'/packet['generation']['attempt_id']/'events.jsonl'))
                assert len(raw)==1 and json.loads(raw[0])==normal['original_plan']
                base=baseline.lookup(case['request'],core)
                assert packet['retrieval']['foundation_ids']==base['retrieval']['ids']
                for k in ('queries','questions','query_count'):assert packet['retrieval'][k]==base['retrieval'][k]
                assert packet['plan']['search_requests']==base['plan']['search_requests']
                ids=packet['retrieval']['ids'];old=packet['retrieval']['foundation_ids']
                assert len(ids)==len(set(ids))<=8 and len(set(ids)-set(old))<=2
                assert packet['facts']==[index.facts[f] for f in ids] and packet['citations']==citations_for(db,ids)
                assert set(answer['cited_fact_ids'])<=set(ids)
                runtime=packet['runtime'];assert runtime['db_unchanged'] and runtime['extractor_seed']==seed
                assert runtime['model_checks'] and all(c['parameters_unchanged'] for c in runtime['model_checks'])
                logs.update(c['worker_log'] for c in runtime['model_checks'])
                selection=packet['selection'];seconds=None
                if core['formly_questions']:
                    assert selection['status'] in ('unchanged','repaired') and packet['advisory']['status']=='available'
                    for q in selection['queries']:assert q['text']==core['formly_questions'][q['question_index']]['question'] and q['depth']==20
                    pool=list(dict.fromkeys(old+[f for q in selection['queries'] for f in q['ids']]))
                    payload,mapping=present(core,old,pool,index.facts,lambda f:db.execute('SELECT source_quote FROM facts WHERE id=?',(f,)).fetchone()[0])
                    assert mapping==selection['mapping']
                    matches=[p.parent for p in sorted((root/'runtime/selector').glob('*/input.json')) if str(p.parent) not in hosted and read(p)==payload and read(p.parent/'decision.json')=={'replacements':selection['replacements']}]
                    assert matches
                    path=matches[0]  # Consume identical repeated requests as a multiset.
                    decision=read(path/'decision.json');assert apply_repair(decision,payload,mapping)==ids
                    receipt=read(path/'receipt.json');assert receipt['exit_code']==0 and receipt['error'] is None
                    se=events(path/'events.jsonl');assert se[-1]['type']=='turn.completed' and json.loads(messages(se)[0])==decision
                    seconds=receipt['seconds'];hosted.append(str(path))
                else:
                    assert selection['status']=='not_needed' and ids==[] and case['id']=='U04'
                if case['id']=='U04':assert core['formly_questions']==[]
                rows.append(dict(seed=seed,id=case['id'],seconds=audit['seconds'],selector_seconds=seconds,selection=selection['status'],answer=answer,checks_pass=True))
            assert not remaining and len(logs)==1
            workers.extend(logs)
    assert len(set(workers))==2 and len(hosted)==6
    assert snapshot()==read(HERE/'test-output/protected-before.json')
    summary=dict(packets=len(rows),hosted_selector_calls=len(hosted),worker_reuse_verified=True,fresh_processes_verified=True,checks_pass=True,rows=rows)
    with (HERE/'test-output/audit.json').open('x') as f:json.dump(summary,f,indent=2)
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
