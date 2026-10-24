"""Exact manually annotated span scoring; never infer semantics from validity."""
import json
import math
from pathlib import Path
from integration import map_hints, score_sets, summarize_times
HERE=Path(__file__).resolve().parent
ROLES=('api_reference','registration_name','model_key','value','version','ui_adapter')


def extraction_coverage(arm, questions, extractions):
    expected=[] if arm=='foundation' else list(range(len(questions)))
    if not isinstance(extractions,list):return ['extractions must be a list']
    if [e.get('question_index') for e in extractions if isinstance(e,dict)]!=expected or len(extractions)!=len(expected):
        return ['extraction question coverage/order mismatch']
    errors=[]
    for e in extractions:
        i=e['question_index']
        if type(i) is not int or e.get('text')!=questions[i]['question']:
            errors.append('extraction question identity mismatch')
        if not {'raw','error','seconds'}<=set(e):errors.append('missing extraction evidence')
        elapsed=e.get('seconds')
        if type(elapsed) not in (float,int) or not math.isfinite(elapsed) or elapsed<0:
            errors.append('invalid extraction timing')
    return errors

def span(m):return (m['start'],m['end'],m['text'],m['role'])
def untyped(s):return s[:3]

def metrics(gold_rows, predictions):
    gold_all,pred_all=set(),set();rows=[];roles={r:[set(),set()] for r in ROLES}
    for row in gold_rows:
        identity=row['id'];gold={span(m) for m in row['gold']};pred={span(m) for m in predictions.get(identity,[])}
        g={(identity,)+s for s in gold};p={(identity,)+s for s in pred};gold_all|=g;pred_all|=p
        for role in ROLES:
            roles[role][0]|={s for s in g if s[-1]==role};roles[role][1]|={s for s in p if s[-1]==role}
        rows.append(dict(id=identity,missing=identity not in predictions,exact=gold==pred and identity in predictions,
                         nonempty=bool(gold),has_correct=bool(gold&pred),empty_fp=not gold and bool(pred),
                         misses=sorted(gold-pred),extras=sorted(pred-gold)))
    typed=score_sets(gold_all,pred_all)
    boundary=score_sets({s[:-1] for s in gold_all},{s[:-1] for s in pred_all})
    n=sum(r['nonempty'] for r in rows);covered=sum(r['nonempty'] and r['has_correct'] for r in rows)
    empty_fp=sum(r['empty_fp'] for r in rows);missing=sum(r['missing'] for r in rows)
    gate=(not missing and typed['precision'] is not None and typed['precision']>=.95 and typed['recall'] is not None and typed['recall']>=.80 and n>0 and covered/n>=.5 and empty_fp==0)
    return dict(questions=len(rows),typed=typed,untyped=boundary,roles={r:score_sets(*s) for r,s in roles.items()},
                exact_questions=sum(r['exact'] for r in rows),missing=missing,gold_nonempty_questions=n,
                correctly_annotated_nonempty_questions=covered,empty_false_positive_questions=empty_fp,
                value_gate=gate,cases=rows)

def main():
    read=lambda p:json.loads(p.read_text())
    records=read(HERE/'data/records.json');gold=read(HERE/'data/gold.json')
    if any(row['alternatives'] for row in gold):raise ValueError('explicit alternative scoring required before inference')
    out=HERE/'test-output/inference';report={}
    for arm in ('foundation','1701','1702'):
        lines=[json.loads(line) for line in (out/f'{arm}.jsonl').read_text().splitlines()]
        actual={r['id']:r for r in lines}
        if len(actual)!=len(lines):raise ValueError('duplicate output identity')
        safety=[];errors=[];extraction_times=[];raw_questions={};accepted_questions={};conflicts=[]
        for record in records:
            result=actual.get(record['id'])
            if result is None:
                safety.append(dict(id=record['id'],pass_=False,error='missing'));continue
            plan=result['plan'];core=record['output']
            preserved=plan['question_plan']==core and plan['search_requests']==[{'query':q['question']} for q in core['formly_questions']]
            anchored=all(h['usable_as_filter'] is False and core['formly_questions'][h['question_index']]['question'][h['start']:h['end']]==h['text'] for h in plan['role_hints'])
            safety.append(dict(id=record['id'],pass_=preserved and anchored))
            coverage=extraction_coverage(arm,core['formly_questions'],result['extractions'])
            errors.extend(dict(record_id=record['id'],error=e) for e in coverage)
            if arm=='foundation':
                for i,q in enumerate(core['formly_questions']):
                    raw_questions[(record['id'],i)]=[];accepted_questions[(record['id'],i)]=[]
            if coverage:continue
            for e in result['extractions']:
                extraction_times.append(e['seconds']);key=(record['id'],e['question_index'])
                accepted_questions[key]=[h for h in plan['role_hints'] if h['question_index']==e['question_index']]
                raw_questions[key]=[]
                if e['error']:errors.append(dict(record_id=record['id'],question_index=e['question_index'],error=e['error']))
                try:raw_questions[key]=map_hints(e['raw'],e['question_index'])
                except (ValueError,TypeError,KeyError):pass
                raw=raw_questions[key]
                for i,a in enumerate(raw):
                    for b in raw[i+1:]:
                        if a['start']==b['start'] and a['end']==b['end'] and a['role']!=b['role']:
                            conflicts.append(dict(record_id=record['id'],question_index=e['question_index'],first=a,second=b))
        mapped={}
        for mode,source in [('raw',raw_questions),('accepted',accepted_questions)]:
            predictions={row['id']:([] if row['empty_control'] else source[(row['record_id'],row['question_index'])]) for row in gold if row['record_id'] in actual and (row['empty_control'] or (row['record_id'],row['question_index']) in source)}
            mapped[mode]=dict(combined=metrics(gold,predictions),saved=metrics([r for r in gold if r['record_id'].startswith('P')],predictions),new=metrics([r for r in gold if r['record_id'].startswith('I')],predictions))
        g={(r['record_id'],r['question_index'],*span(m)) for r in gold for m in r['gold']}
        rawset={(r,i,*span(m)) for (r,i),ms in raw_questions.items() for m in ms};acceptedset={(r,i,*span(m)) for (r,i),ms in accepted_questions.items() for m in ms}
        report[arm]=dict(scheduled=len(records),delivered=len(lines),safety_pass=sum(r['pass_'] for r in safety),safety=safety,
            extraction_errors=errors,cross_role_conflicts=conflicts,annotation=mapped,
            correct_gold_spans_lost_to_filtering=sorted((rawset&g)-acceptedset),
            raw_mentions=len(rawset),accepted_mentions=len(acceptedset),
            extraction_question_seconds=summarize_times(extraction_times),
            extraction_request_seconds=summarize_times([r['extraction_seconds'] for r in lines]),
            projection_seconds=summarize_times([r['projection_seconds'] for r in lines]),
            advisory_value_pass=len(lines)==len(records) and all(r['pass_'] for r in safety) and not errors and mapped['accepted']['combined']['value_gate'])
    with (HERE/'test-output/scores.json').open('x') as f:json.dump(report,f,indent=2)
    for arm,r in report.items():print(arm, 'safety',r['safety_pass'],'typed',r['annotation']['accepted']['combined']['typed'],'value',r['advisory_value_pass'])

if __name__=='__main__':main()
