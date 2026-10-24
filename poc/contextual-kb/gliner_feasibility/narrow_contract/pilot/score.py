"""Raw diagnostics and accepted-contract metrics are deliberately separate."""
import json
from pathlib import Path
from contract import ROLES,validate,tokens,counts,metrics,score_case
HERE=Path(__file__).resolve().parent
def aggregate(pairs,role='all'):
 c=dict(tp=0,fp=0,fn=0)
 for p,g in pairs:
  if role!='all':p={s for s in p if s[0]==role};g={s for s in g if s[0]==role}
  for k,v in counts(p,g).items():c[k]+=v
 return metrics(c)
def evaluate(questions,gold,rows):
 byid={r['id']:r for r in rows};ids={q['id'] for q in questions}
 if len(byid)!=len(rows) or set(byid)-ids:raise ValueError('duplicate/unknown result')
 results={q['id']:score_case(gold[q['id']],byid.get(q['id'])) for q in questions}
 pairs={}
 for arm in ('raw','accepted'):
  pairs[arm]={id:(tokens(r['raw_mentions'] if arm=='raw' else r['envelope']['mentions']),tokens(gold[id]['mentions'])) for id,r in results.items()}
 report={arm:{role:aggregate(pairs[arm].values(),role) for role in ('all',*ROLES)} for arm in pairs}
 report.update(exact=sum(r['exact'] for r in results.values()),invalid=sum(r['error'] is not None for r in results.values()),
 status_matches=sum(r['status_match'] for r in results.values()),seconds=sum(r.get('seconds',0) for r in rows),questions=len(questions),cases=results)
 report['exact_by_gold']={}
 for category in ('with_mentions','clear_empty','ambiguous_empty'):
  selected=[id for id in results if ('with_mentions' if gold[id]['mentions'] else 'clear_empty' if gold[id]['status']=='ok' else 'ambiguous_empty')==category]
  report['exact_by_gold'][category]=dict(total=len(selected),exact=sum(results[id]['exact'] for id in selected),
   raw_nonempty=sum(bool(results[id]['raw_mentions']) for id in selected))
 report['needs_review_gold']={id:dict(predicted_status=results[id]['envelope']['status'],status_match=results[id]['status_match']) for id in results if gold[id]['status']=='needs_review'}
 report['groups']={}
 for field in ('family','origin','parent'):
  groups={}
  for group in sorted({q[field] for q in questions}):
   selected=[q['id'] for q in questions if q[field]==group]
   groups[group]={arm:aggregate([pairs[arm][id] for id in selected]) for arm in pairs}
   groups[group]['seconds']=sum(byid[id].get('seconds',0) for id in selected if id in byid)
   if field=='parent':
    groups[group]['unique_raw']=aggregate([(set((s[0],s[3]) for id in selected for s in pairs['raw'][id][0]),
      set((s[0],s[3]) for id in selected for s in pairs['raw'][id][1]))])
  report['groups'][field]=groups
 special={'compound_api':lambda s:s[0]=='api_reference' and ('.' in s[3] or '[' in s[3]),
 'quoted_name_key_value':lambda s:s[0] in ('registration_name','model_key','value') and s[3][:1] in ("'",'"')}
 report['boundary_diagnostics']={}
 for name,predicate in special.items():
  expected=sum(sum(predicate(s) for s in g) for p,g in pairs['raw'].values())
  found=sum(sum(predicate(s) for s in p&g) for p,g in pairs['raw'].values())
  report['boundary_diagnostics'][name]=dict(expected=expected,exact_found=found,missed=expected-found)
 return report
def main():
 from run import check
 check(HERE/'test-output/inference-freeze.json')
 qs=json.loads((HERE/'questions.json').read_text())
 gold_rows=json.loads((HERE/'gold.json').read_text())
 assert len(qs)==len(gold_rows)==24
 gold={r['question_id']:r for r in gold_rows};assert set(gold)=={q['id'] for q in qs}
 for q in qs:validate(gold[q['id']],q['id'],q['question'])
 raw=[json.loads(l) for l in (HERE/'test-output/predictions.jsonl').read_text().splitlines()]
 if any(r['schema'] not in ('bare','described') for r in raw):raise ValueError('schema')
 report={schema:evaluate(qs,gold,[r for r in raw if r['schema']==schema]) for schema in ('bare','described')}
 differences=[]
 for q in qs:
  id=q['id'];g=tokens(gold[id]['mentions'])
  a=tokens(report['bare']['cases'][id]['raw_mentions']);b=tokens(report['described']['cases'][id]['raw_mentions'])
  differences.append(dict(id=id,new_correct=sorted((b&g)-a),lost_correct=sorted((a&g)-b),
   new_false_positives=sorted((b-g)-a),removed_false_positives=sorted((a-g)-b)))
 for name,data in [('scores.json',report),('differences.json',differences)]:
  with (HERE/'test-output'/name).open('x') as f:json.dump(data,f,indent=2)
 print(json.dumps({k:{field:v[field] for field in ('raw','accepted','invalid','exact','status_matches','boundary_diagnostics','seconds')} for k,v in report.items()},indent=2))
if __name__=='__main__':main()
