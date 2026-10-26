"""Apply this batch's frozen gates; semantic grades still require independent audit."""
import argparse
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def evaluate(summary, case_document):
    criteria=case_document['criteria'];cases=case_document['cases']
    ids={c['id'] for c in cases};categories={c['id']:c['category'] for c in cases}
    controls=set(criteria['all_control_ids_required'])
    if len(ids)!=15 or len(cases)!=15 or len(controls)!=5 or not controls<=ids or criteria['repeats']!=3:
        raise ValueError('Unexpected validation batch contract')
    reasons=[];diagnostics=[];indexed={}
    expected={(n,arm) for n in range(1,4) for arm in ('baseline','candidate')}
    rounds=summary.get('rounds',[])
    if not isinstance(rounds,list):rounds=[]
    for result in rounds:
        key=(result.get('round'),result.get('arm'))
        if key not in expected or key in indexed:
            reasons.append(f'Unexpected or duplicate round: {key}');continue
        indexed[key]=result
    if set(indexed)!=expected:reasons.append('Missing expected round/arm')
    valid_rows={}
    for key,result in indexed.items():
        rows=result.get('rows',[])
        if not isinstance(rows,list) or len(rows)!=15 or {r.get('id') for r in rows}!=ids:
            reasons.append(f'{key}: missing, duplicate or unexpected case');continue
        if any(type(r.get('usable')) is not bool or type(r.get('critical')) is not bool or
               r.get('category')!=categories[r['id']] or not isinstance(r.get('delivery_errors',[]),list) for r in rows):
            reasons.append(f'{key}: malformed assessment row');continue
        usable=sum(r['usable'] for r in rows);critical=sum(r['critical'] for r in rows)
        if result.get('total')!=15 or result.get('usable')!=usable or result.get('critical')!=critical:
            reasons.append(f'{key}: inconsistent aggregate counts')
        delivery=[r['id'] for r in rows if r.get('delivery_errors') or r.get('error')]
        if delivery:reasons.append(f'{key}: incomplete delivery/assessment: {delivery}')
        valid_rows[key]={r['id']:r for r in rows}
        diagnostics.append({'round':key[0],'arm':key[1],'usable':usable,'critical':critical,'delivery_failed_ids':delivery})
        if key[1]=='candidate':
            if usable<criteria['candidate_usable_minimum_per_repeat']:reasons.append(f'{key}: candidate below threshold')
            if critical>criteria['critical_maximum']:reasons.append(f'{key}: candidate critical error')
            failed=sorted(id for id in controls if not valid_rows[key][id]['usable'])
            if failed:reasons.append(f'{key}: failed controls: {failed}')
    for repeat in range(1,4):
        old=valid_rows.get((repeat,'baseline'));new=valid_rows.get((repeat,'candidate'))
        if old is None or new is None:continue
        regressions=sorted(id for id in ids if old[id]['usable'] and not new[id]['usable'])
        if len(regressions)>criteria['baseline_supported_regressions_maximum']:
            reasons.append(f'Round {repeat}: baseline-supported regressions: {regressions}')
    return {'qualified':not reasons,'reasons':reasons,'rounds':diagnostics,
        'policy':'Candidate quality gates apply per repeat; baseline critical errors are reported diagnostics. Both arms require complete delivery/assessment. Independent semantic review and preservation checks remain required.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args();root=args.root.absolute()
    if root!=root.resolve() or not root.is_relative_to(HERE/'test-output'):
        raise ValueError('Run must be canonical and inside batch test-output')
    result=evaluate(json.loads((root/'summary.json').read_text()),json.loads((HERE/'qualification-cases.json').read_text()))
    output=root/'qualification-decision.json'
    with output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))
    if not result['qualified']:raise SystemExit(1)


if __name__=='__main__':main()
