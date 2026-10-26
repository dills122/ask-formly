"""Audit saved transport and manual answer judgments; does not grade semantics."""
import json
import copy
from pathlib import Path
from candidate import preserved, checked_database
HERE=Path(__file__).resolve().parent


def require_identical(first, repeat):
    if first != repeat:raise ValueError('Changed packets require new caller judgment')


def validate_answers(answers, packets):
    ids=[row['id'] for row in answers]
    if len(ids)!=len(set(ids)) or set(ids)!=set(packets):raise ValueError('Missing/duplicate answers')
    for row in answers:
        if type(row['usable']) is not bool or not row['answer'].strip() or not row['reason'].strip():raise ValueError('Missing manual judgment')
        observed={f['id'] for f in packets[row['id']].get('facts',[])}
        if not set(row['citations'])<=observed:raise ValueError('Citation not delivered as a full fact')
    return sum(row['usable'] for row in answers)


def read_run(arm, repeat):
    folder=HERE/f'test-output/qualification/{arm}/r{repeat}'
    rows=[]
    for name in ['batch-1','batch-2','batch-3','discovery-page1','discovery-page2','fetch']:
        data=json.loads((folder/(name+'.json')).read_text())
        receipt=json.loads((folder/(name+'.receipt.json')).read_text())
        planned=json.loads((HERE/'test-output'/arm/(name+'.json')).read_text())
        expected=len(planned)
        if [{k:r[k] for k in ('id','tool','arguments')} for r in data]!=planned:raise ValueError('Saved calls differ from planned calls')
        if receipt!={'expected':expected,'attempted':expected,'errors':0,'unattempted':[]}:raise ValueError('Incomplete/error receipt')
        if len(data)!=expected or any(r['operational_or_tool_error'] or r['result'].get('isError') for r in data):raise ValueError('Failed tool calls')
        if 'OFFLINE_GUARDS_ACTIVE' not in (folder/(name+'.stderr')).read_text():raise ValueError('Missing offline guard')
        rows.extend(data)
    canonical=json.loads((HERE/'lookup-calls.json').read_text())
    actual=[{k:r[k] for k in ('id','tool','arguments')} for r in rows if r['tool']=='lookup_formly']
    if actual != canonical:raise ValueError('Initial calls differ from frozen canonical plans')
    scopes={r['id']:r['arguments'] for r in canonical}
    packets={}; initial_packets={}; observed={}; all_results=[]
    for row in rows:
        packet=row['result']['structuredContent'];all_results.append({'id':row['id'],'tool':row['tool'],'arguments':row['arguments'],'packet':packet})
        if row['tool']=='lookup_formly':
            if row['id'] in packets:raise ValueError('Duplicate lookup')
            packets[row['id']]=dict(packet,facts=list(packet.get('facts',[])))
            initial_packets[row['id']]=copy.deepcopy(packet)
            observed[row['id']]={f['id'] for f in packet.get('facts',[])}|{i for q in packet.get('questions',[]) for i in q.get('omitted_ids',[])}
        else:
            original=scopes[row['id']]
            for key in ('formly_version','ui_adapter'):
                if row['arguments'].get(key)!=original.get(key):raise ValueError('Recovery scope changed')
            if row['tool']=='discover_formly_candidates':
                for key in ('request','plan'):
                    if row['arguments'].get(key)!=original.get(key):raise ValueError('Discovery changed frozen plan')
                observed[row['id']].update(f['id'] for f in packet.get('candidates',[]))
        if row['tool']=='get_formly_facts':
            initial=packets[row['id']]
            seen=observed[row['id']]
            if not set(row['arguments']['fact_ids'])<=seen:raise ValueError('Fetched unseen ID')
            initial['facts'].extend(packet.get('facts',[]))
    expected_ids={r['id'] for r in json.loads((HERE/'cases.json').read_text())}
    if set(packets)!=expected_ids:raise ValueError('Wrong case coverage')
    return initial_packets,packets,all_results


def main():
    preserved();checked_database('baseline');checked_database('candidate')
    report={}; judgments={}
    for arm in ['baseline','candidate']:
        answers=json.loads((HERE/f'answers-{arm}.json').read_text()); first=None; scores=[]; initial_scores=[]
        initial_answers=json.loads((HERE/f'answers-initial-{arm}.json').read_text())
        for repeat in [1,2,3]:
            initial,packets,raw=read_run(arm,repeat)
            if first is None:first=raw
            else:require_identical(first,raw)
            scores.append(validate_answers(answers,packets))
            initial_scores.append(validate_answers(initial_answers,initial))
        judgments[arm]={r['id']:r['usable'] for r in answers}
        report[arm]={'usable_each_repeat':scores,'initial_usable_each_repeat':initial_scores,'unique_completed_caller_answers':len(answers),'unique_initial_assessments':len(initial_answers),'tool_calls_per_repeat':len(first),'packet_stability':'exact structured equality across all three repeats'}
    report['baseline_supported_regressions']=[i for i,v in judgments['baseline'].items() if v and not judgments['candidate'][i]]
    report['candidate_controls_pass']=all(v for i,v in judgments['candidate'].items() if i.startswith('C'))
    report['candidate_meets_numeric_gate']=all(n>=14 for n in report['candidate']['usable_each_repeat']) and report['candidate_controls_pass'] and not report['baseline_supported_regressions']
    report['semantic_judgments']='Manual caller assessments; see FINAL-REVIEW.md for independent verdict. Script checks coverage, citations, receipts and equality only.'
    report['total_lookup_observations']=90;report['total_tool_calls']=sum(x['tool_calls_per_repeat']*3 for x in [report['baseline'],report['candidate']])
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
