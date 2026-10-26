"""Read-only post-run integrity audit; does not grade answer meaning."""
import hashlib
import json
from pathlib import Path
import sys
from collections import Counter

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
POC=HERE.parents[1]
sys.path.insert(0,str(POC/'model_free_v1'))
from candidate import Store
from harness import database
from scope import same_scope


def run(run_root=None):
    run_root=Path(run_root) if run_root else HERE/"test-output"
    expected=json.loads((HERE/'cases.json').read_text())
    plans={r['id']:r['arguments'] for r in json.loads((HERE/'lookup-calls.json').read_text())}
    all_cases={x['id'] for x in expected};summary=[];tool_counts=Counter();total_errors=0
    stages=['batch-1-lookup','batch-2-lookup','batch-3-lookup','discovery','discovery2','fetch']
    for repeat in (1,2,3):
        for arm in ('baseline','candidate'):
            directory=run_root/f'r{repeat}/{arm}'
            seen={i:set() for i in all_cases};full={i:set() for i in all_cases};initial={i:set() for i in all_cases}
            rows=[];failures=0;scope_failures=[];lookup_scopes={}
            store=Store(*database(arm))
            try:
                for stage in stages:
                    path=directory/(stage+'.json');calls=json.loads(path.read_text())
                    receipt=json.loads(path.with_suffix('.receipt.json').read_text())
                    assert receipt['attempted']==len(calls)
                    assert receipt['expected']==receipt['attempted']+len(receipt['unattempted'])
                    failures+=receipt['errors']+len(receipt['unattempted'])
                    assert 'OFFLINE_GUARDS_ACTIVE' in path.with_suffix('.stderr').read_text()
                    for row in calls:
                        rows.append(row);i=row['id'];tool=row['tool'];tool_counts[tool]+=1
                        assert i in plans
                        if row.get('operational_or_tool_error'):continue
                        packet=row['result']['structuredContent'];args=row['arguments']
                        if tool!='get_formly_facts':
                            assert {k:args[k] for k in plans[i]}==plans[i]
                            if tool=='discover_formly_candidates':assert args['limit']==16 and args['offset'] in (0,16)
                        else:
                            assert set(args['fact_ids'])<=seen[i],('unobserved fetch',i,args)
                            if not same_scope(lookup_scopes[i],packet):scope_failures.append(i)
                        if i=='C05':assert tool=='lookup_formly' and packet['status']=='unsupported_scope'
                        facts=packet.get('facts',[]);candidates=packet.get('candidates',[])
                        ids=[f['id'] for f in facts]
                        if facts:
                            truth,citations=store.records(ids,packet['version_context']['selected'],packet['ui_adapter'])
                            assert facts==truth and packet['citations']==citations,('changed delivered evidence',i)
                            assert set(ids)<=packet['citations'].keys()
                        if candidates:
                            truth,_=store.records([f['id'] for f in candidates],packet['version_context']['selected'],packet['ui_adapter']);assert candidates==truth
                        full[i].update(ids);seen[i].update(f['id'] for f in facts+candidates)
                        if tool=='lookup_formly':
                            initial[i].update(ids);lookup_scopes[i]=packet
                assert Counter(r['id'] for r in rows if r['tool']=='lookup_formly')==Counter(plans.keys())
                answers=json.loads((directory/'answers.json').read_text())
                assert len(answers)==15 and {a['id'] for a in answers}==all_cases
                for a in answers:
                    assert a['request']==next(c['request'] for c in expected if c['id']==a['id'])
                    assert set(a['citations'])<=full[a['id']],('undelivered citation',a['id'])
                    if a['id']=='C04':assert a['no_call_reason'] and not a['citations']
                summary.append(dict(repeat=repeat,arm=arm,calls=len(rows),errors=failures,scope_failures=scope_failures,initial_ids={k:sorted(v) for k,v in initial.items()},delivered_ids={k:sorted(v) for k,v in full.items()}));total_errors+=failures
            finally:store.close()
    preservation=json.loads((HERE/'preservation.json').read_text())['files'];freeze=json.loads((HERE/'freeze.json').read_text())['files']
    for base,pins in [(REPO,preservation),(HERE,freeze)]:
        for name,sha in pins.items():assert hashlib.sha256((base/name).read_bytes()).hexdigest()==sha,('preservation changed',name)
    return dict(passed=total_errors==0 and not any(s["scope_failures"] for s in summary),protocol_scope_failures=sum(len(s["scope_failures"]) for s in summary),answer_observations=90,distinct_authored_answers=30,repeat_answers='retained after exact result equality, not independent generation',tool_counts=dict(tool_counts),delivery_failures=total_errors,preserved_files=len(preservation),frozen_experiment_files=len(freeze),sessions=summary)

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'test-output'
    result=run(root);(root/'mechanical-audit.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='sessions'}))
