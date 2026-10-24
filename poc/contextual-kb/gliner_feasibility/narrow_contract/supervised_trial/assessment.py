"""Frozen-protocol decision and paired raw/contract scoring."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'pilot'))
from score import evaluate
def decision(base,trained):
 checks=[]
 for candidate in trained:
  regressions=[role for role,value in base['raw'].items() if role!='all' and value['recall'] is not None
   and (candidate['raw'][role]['recall'] is None or candidate['raw'][role]['recall']<value['recall']-.05-1e-12)]
  checks.append(dict(raw_gain=candidate['raw']['all']['f1']-base['raw']['all']['f1'],
   accepted_gain=candidate['accepted']['all']['f1']-base['accepted']['all']['f1'],
   recall_regressions=regressions))
 worth=len(trained)==2 and all(c['raw_gain']>=.10-1e-12 and c['accepted_gain']>0 and not c['recall_regressions'] for c in checks)
 qualified=len(trained)==2 and all(c['invalid']==0 and all(v['exact_found']==v['expected'] for v in c.get('boundary_diagnostics',{}).values()) and all(v.get('precision') is not None and v['precision']>=.9
  and v['recall'] is not None and v['recall']>=.9 for v in c['raw'].values()) for c in trained)
 return dict(worth_continuing=worth,qualified=qualified,checks=checks)
def main():
 train=json.loads((HERE/'test-output/train.json').read_text())
 dev=json.loads((HERE/'dev.json').read_text())
 report={}
 for split,gold_rows in (('train',train),('dev',dev)):
  questions=[dict(id=r['question_id'],question=r['question'],parent=r['question_id'],
   family='training' if split=='train' else ('paths','names_keys','values','scope','conditions','negative')[i//4],
   origin=split) for i,r in enumerate(gold_rows)]
  gold={r['question_id']:r for r in gold_rows}
  outputs={'base':HERE/f'test-output/base-{split}.json',
   'seed1701':HERE/f'test-output/seed-1701/final-{split}.json',
   'seed1702':HERE/f'test-output/seed-1702/final-{split}.json'}
  report[split]={}
  for name,file in outputs.items():
   rows=json.loads(file.read_text())
   if len(rows)!=len(questions) or {r['id'] for r in rows}!=set(gold):raise ValueError('prediction coverage')
   report[split][name]=evaluate(questions,gold,rows)
 report['decision']=decision(report['dev']['base'],[report['dev']['seed1701'],report['dev']['seed1702']])
 with (HERE/'test-output/scores.json').open('x') as f:json.dump(report,f,indent=2)
 print(json.dumps({split:{k:{'raw':v['raw'],'accepted':v['accepted']['all'],'exact':v['exact'],'invalid':v['invalid']} for k,v in report[split].items()} for split in ('train','dev')},indent=2))
 print(report['decision'])
if __name__=='__main__':main()
