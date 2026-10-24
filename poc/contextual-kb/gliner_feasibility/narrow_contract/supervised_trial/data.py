"""Six-role exact-span data transport; no labels inferred from string matching."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'pilot'))
from contract import ROLES,validate
def export(row,descriptions):
 validate(row,row['question_id'],row['question'])
 if row['status']!='ok':raise ValueError('Training requires clear gold')
 entities={kind:[] for kind in ROLES}
 for m in row['mentions']:
  entities[m['kind']].append(dict(text=m['raw'],start=m['start'],end=m['end']))
 return {'input':row['question'],'output':{'entities':entities,'entity_descriptions':descriptions}}
def combine(pilot,new):
 rows=[r for r in pilot if r['status']=='ok']+list(new)
 if len({r['question_id'] for r in rows})!=len(rows) or len({r['question'] for r in rows})!=len(rows):
  raise ValueError('duplicate training identity/question')
 for r in rows:export(r,{})
 return rows
