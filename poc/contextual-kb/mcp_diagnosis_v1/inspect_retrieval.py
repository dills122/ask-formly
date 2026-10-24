"""Read-only diagnosis of frozen MCP failures, without changing serving behavior."""
import hashlib,json,os,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parent
sys.path.insert(0,str(POC))
from mcp_v1.preserve import snapshot
from agent_contract.retrieval_integration_v1.bridge import readonly
from kbcompiler.question_pilot import PilotIndex,reciprocal_rank_fusion,_terms

def main():
    before=snapshot()
    freeze=json.loads((POC/'mcp_v1/test-output/final-freeze.json').read_text())
    for p,h in freeze.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
    dbpath=POC/'build/knowledge.sqlite';dbhash=hashlib.sha256(dbpath.read_bytes()).hexdigest()
    os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(POC/'agent_contract/advisory_lookup_v1/test-output/embed-cache'),HF_HUB_OFFLINE='1')
    targets=['expression-callbacks-and-hooks/'+x for x in ['modern-callback-field-argument','legacy-callback-arguments','conditional-disabled-target','conditional-hide-target']]
    result={'diagnostic_only':True,'targets':targets,'queries':[]}
    with readonly(dbpath) as db:
        db.row_factory=__import__('sqlite3').Row
        facts=[dict(r) for r in db.execute('select * from facts order by id')]
        documents=[dict(r) for r in db.execute('select * from documents order by id')]
        evidence=[json.loads(r[0]) for r in db.execute('select record_json from evidence order by id')]
        result['inventory']={'facts':len(facts),'documents':len(documents),'evidence':len(evidence),'versions':sorted({d['formly_version'] for d in documents})}
        result['stored_term_hits']={term:[f['id'] for f in facts if term.lower() in json.dumps(f).lower()] for term in ['props.required','validator','asyncValidators','validation.messages','validation']}
        result['evidence_with_body']=[e['id'] for e in evidence if 'body_md' in e]
        result['relevant_stored_facts']=[f for f in facts if f['id'] in targets or f['id'].startswith('custom-types-and-wrappers/')]
        index=PilotIndex(db)
        for repeat in range(1,4):
            for path in (POC/f'mcp_v1/test-output/qualification/round-{repeat}/audit').glob('*.json'):
                audit=json.loads(path.read_text())
                if 'props.required' not in audit['request']:continue
                packet=audit['result']
                for qi,q in enumerate(packet['retrieval']['queries']):
                    text=q['text'];lex=index.lexical(text,46);dense=index.dense(text,46)
                    fused=reciprocal_rank_fusion([lex[:8],dense[:8]])
                    assert fused[:8]==q['ids'],(repeat,qi)
                    def rank(items,t):return items.index(t)+1 if t in items else None
                    targetrows=[]
                    for target in targets:
                        targetrows.append({'fact':target,'lexical_rank':rank(lex,target),'dense_rank':rank(dense,target),
                            'original_candidate_union':target in set(lex[:8]+dense[:8]),'original_fused_rank':rank(fused,target),
                            'in_query_top8':target in q['ids'],'in_final_packet':target in packet['retrieval']['ids']})
                    result['queries'].append({'round':repeat,'question_index':qi,'text':text,'lexical_terms':_terms(text),'lexical_top8':lex[:8],'dense_top8':dense[:8],'fused_original_candidates':fused,'targets':targetrows})
    assert snapshot()==before
    assert hashlib.sha256(dbpath.read_bytes()).hexdigest()==dbhash
    for p,h in freeze.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
    result['preservation']={'db_sha256':dbhash,'protected_chains':len(before),'mcp_frozen_files':len(freeze),'unchanged':True,'sealed_semantics_read':False}
    with (HERE/'diagnostic.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps({'inventory':result['inventory'],'stored_term_hits':result['stored_term_hits'],'queries':[{k:q[k] for k in ['round','question_index','targets']} for q in result['queries']],'preservation':result['preservation']},indent=2))
if __name__=='__main__':main()
