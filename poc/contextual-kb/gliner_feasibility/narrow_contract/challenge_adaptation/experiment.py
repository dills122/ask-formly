"""Trial-only annotation transport, split guard and predeclared paired decision."""
import re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'pilot'))
from contract import validate,ROLES

def annotation(identifier,marked):
 # This parses explicitly authored gold markup; it never infers model labels.
 question='';mentions=[];cursor=0
 for match in re.finditer(r'<([a-z_]+)>(.*?)</\1>',marked):
  prefix=marked[cursor:match.start()];kind,raw=match.groups()
  if '<' in prefix or '<' in raw or kind not in ROLES:raise ValueError('invalid annotation')
  question+=prefix;start=len(question);question+=raw
  mentions.append(dict(kind=kind,raw=raw,start=start,end=len(question)))
  cursor=match.end()
 tail=marked[cursor:]
 if '<' in tail:raise ValueError('unclosed annotation')
 question+=tail
 row=dict(question_id=identifier,question=question,schema_version='narrow-mentions-v1',mentions=mentions,status='ok',issues=[])
 validate(row,identifier,question)
 return row

def verify_splits(train,test):
 rows=list(train)+list(test)
 if len({r['question_id'] for r in rows})!=len(rows) or len({r['question'] for r in rows})!=len(rows):
  raise ValueError('duplicate identity/question across splits')
 for row in rows:
  validate(row,row['question_id'],row['question'])
  if row['status']!='ok':raise ValueError('clear cases only')

def paired_decision(pairs):
 checks=[]
 for old,new,old_reg,new_reg in pairs:
  families=[k for k,v in old['groups']['family'].items()
   if new['groups']['family'][k]['accepted']['f1']<v['accepted']['f1']-.05-1e-12]
  gain=new['accepted']['all']['f1']-old['accepted']['all']['f1']
  regression=new_reg['accepted']['all']['f1']-old_reg['accepted']['all']['f1']
  checks.append(dict(accepted_gain=gain,exact_gain=new['exact']-old['exact'],
   family_regressions=families,regression_gain=regression,
   invalid_increase=new_reg['invalid']-old_reg['invalid']))
 return dict(improved=len(checks)==2 and all(c['accepted_gain']>=.03-1e-12 and c['exact_gain']>0
  and not c['family_regressions'] and c['regression_gain']>=-.02-1e-12 and c['invalid_increase']<=0 for c in checks),checks=checks)

def challenge_hashes(manifest):
 if manifest.get('schema_version')!='challenge-freeze-v1':raise ValueError('unknown challenge manifest')
 return {name:record['sha256'] for name,record in manifest['files'].items()}
