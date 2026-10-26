"""Frozen gate over separately audited semantic judgments, never an answer grader."""
IDS=tuple(f'J{i:02}' for i in range(1,11))+tuple(f'C{i:02}' for i in range(1,6))


def gate(rows,delivery_failures):
    expected={(r,a,i) for r in (1,2,3) for a in ('baseline','candidate') for i in IDS}
    keys=[(x['repeat'],x['arm'],x['id']) for x in rows]
    complete=len(keys)==len(expected) and set(keys)==expected
    valid=all(type(x.get('usable')) is bool and type(x.get('critical')) is bool for x in rows)
    lookup={(x['repeat'],x['arm'],x['id']):x for x in rows};summaries=[]
    for repeat in (1,2,3):
        count=lambda arm:sum(lookup.get((repeat,arm,i),{}).get('usable') is True for i in IDS)
        controls=all(lookup.get((repeat,'candidate',i),{}).get('usable') is True for i in IDS if i.startswith('C'))
        regressions=[i for i in IDS if lookup.get((repeat,'baseline',i),{}).get('usable') is True and lookup.get((repeat,'candidate',i),{}).get('usable') is not True]
        summaries.append(dict(repeat=repeat,baseline_usable=count('baseline'),candidate_usable=count('candidate'),all_controls=controls,regressions=regressions))
    criticals=sum(x.get('critical') is True for x in rows)
    passed=complete and valid and delivery_failures==0 and criticals==0 and all(r['candidate_usable']>=14 and r['all_controls'] and not r['regressions'] for r in summaries)
    return dict(passed=passed,complete=complete,valid_judgments=valid,delivery_failures=delivery_failures,criticals=criticals,repeats=summaries)
