"""Audit frozen development calls against original foundation-only retrieval."""
import hashlib,json,os,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parent
sys.path.insert(0,str(POC))
from agent_contract.advisory_lookup_v1.lookup import AdvisoryLookup
from agent_contract.retrieval_integration_v1.bridge import readonly
from kbcompiler.question_pilot import PilotIndex
from mcp_v1.preserve import snapshot

def main():
    output=HERE/'test-output/results';output.mkdir()
    freeze=json.loads((HERE/'test-output/qualification-freeze.json').read_text())
    for path,h in freeze.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==h,path
    protected=snapshot();assert protected==json.loads((HERE/'test-output/protected-before.json').read_text())
    cases=json.loads((HERE/'cases.json').read_text());byrequest={c['request']:c for c in cases}
    os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(POC/'agent_contract/advisory_lookup_v1/test-output/embed-cache'),HF_HUB_OFFLINE='1')
    rows=[];rounds=[];facts={};citations={}
    with readonly(POC/'build/knowledge.sqlite') as db:
        index=PilotIndex(db);baseline=AdvisoryLookup(index,None)
        for repeat in range(1,4):
            root=HERE/f'test-output/qualification/round-{repeat}'
            receipt=json.loads((root/'receipt.json').read_text())
            events=[json.loads(s) for s in (root/'events.jsonl').read_text().splitlines() if s]
            calls=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='mcp_tool_call']
            messages=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
            try:answers=json.loads(messages[-1])['answers']
            except (ValueError,KeyError,IndexError):answers=[]
            audits=[json.loads(p.read_text()) for p in (root/'audit').glob('*.json')]
            rounds.append(dict(receipt,calls=len(calls),answers=len(answers),audit_records=len(audits)))
            for case in cases:
                matches=[c for c in calls if c['arguments']=={'request':case['request']} and c['tool']=='lookup_formly' and c['server']=='formly']
                matches_a=[a for a in audits if a['request']==case['request']]
                matches_answer=[a for a in answers if a.get('id')==case['id']]
                row={'round':repeat,**case,'single_call':len(matches)==1,'single_audit':len(matches_a)==1,'single_answer':len(matches_answer)==1}
                row['answer']=matches_answer[0] if len(matches_answer)==1 else None
                if len(matches)==1 and len(matches_a)==1:
                    call=matches[0];audit=matches_a[0]
                    result=call.get('result') or {};packet=result.get('structured_content')
                    row['delivery']=packet is not None and call['error'] is None and call['status']=='completed' and packet==audit.get('result')
                    row['seconds']=audit['seconds'];row['error']=audit.get('error') or call.get('error')
                    if row['delivery']:
                        plan=packet['plan']['question_plan'];row['plan']=plan
                        check=baseline.lookup(case['request'],plan)
                        row['parity']=all(packet['retrieval'][k]==check['retrieval'][k] for k in ['ids','queries','questions','query_count']) and packet['facts']==check['facts'] and packet['plan']['search_requests']==check['plan']['search_requests']
                        row['fact_ids']=packet['retrieval']['ids'];row['advisory']=packet['advisory'];row['runtime']=packet['runtime'];row['generation']=packet['generation']
                        row['citations_complete']=set(packet['citations'])==set(row['fact_ids'])
                        row['cited_ids_valid']=row['answer'] is not None and set(row['answer']['cited_fact_ids'])<=set(row['fact_ids'])
                        for fact in packet['facts']:facts[fact['id']]=fact
                        citations.update(packet['citations'])
                rows.append(row)
    summary={'rounds':rounds,'scheduled':30,'single_calls':sum(r['single_call'] for r in rows),'deliveries':sum(r.get('delivery',False) for r in rows),'parity':sum(r.get('parity',False) for r in rows),'citation_packets':sum(r.get('citations_complete',False) for r in rows),'valid_cited_ids':sum(r.get('cited_ids_valid',False) for r in rows),'protected_chains':len(protected),'semantic_grading':'pending; mechanical checks are not usability scores'}
    for name,value in [('mechanical.json',summary),('rows.json',rows),('facts.json',facts),('citations.json',citations),('protected-after.json',protected)]:
        (output/name).write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
