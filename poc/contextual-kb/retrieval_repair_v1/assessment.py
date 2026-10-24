"""Authoritative per-group identity assessment; retains original coarse score evidence."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def compare_groups(before,after,groups):
    before=set(before);after=set(after)
    old={i for i,g in enumerate(groups) if before&set(g)}
    new={i for i,g in enumerate(groups) if after&set(g)}
    return dict(baseline_group_indexes=sorted(old),candidate_group_indexes=sorted(new),
                lost_group_indexes=sorted(old-new),gained_group_indexes=sorted(new-old),nonregression=not bool(old-new))

def main():
    p=HERE/'test-output/panel'
    records=json.loads((p/'inputs.json').read_text());decisions={r['id']:r for r in json.loads((p/'all-decisions.json').read_text())}
    scores=json.loads((p/'scores.json').read_text());byid={s['id']:s for s in scores};rows=[]
    for r in records:
        s=dict(byid[r['id']]);d=decisions[r['id']]
        if r['gold'] is not None:s.update(compare_groups(r.get('baseline',{}).get('ids',[]),d['ids'],r['gold']['required_groups']))
        s['upstream_failure']=bool(r.get('error'));rows.append(s)
    valid=[r for r in rows if not r['upstream_failure']]
    callback=[r for r in valid if r['id'].endswith('M03') or r['id'].split('-')[0] in {'F01','F02','F03'}]
    conditional=all(not r['error'] and not r.get('relevant_lost') and not r.get('lost_group_indexes') and not r.get('unsupported_replacements') for r in valid) and all(r['callback_present'] for r in callback)
    summary=dict(total=len(rows),upstream_failure_slots=sum(r['upstream_failure'] for r in rows),valid_plan_slots=len(valid),relevant_fact_losses=sum(len(r.get('relevant_lost',[])) for r in rows),lost_groups=sum(len(r.get('lost_group_indexes',[])) for r in rows),conditional_retrieval_gates_pass=conditional,strict_original_overall_gate_pass=conditional and len(valid)==len(rows),caveat='Conditional retrieval gate does not erase upstream failures or replace the frozen overall gate.')
    for name,value in [('per-group-audit.json',rows),('final-gate.json',summary)]:
        with (p/name).open('x') as f:json.dump(value,f,indent=2);f.write('\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
