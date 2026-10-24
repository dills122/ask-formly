"""Apply clarified guide to author's raw labels, without reading other labels."""
import json
from pathlib import Path
from contract import validate_annotation
p=Path(__file__).parent
rows=json.loads((p/'annotator-one.json').read_text())
for r in rows:
 q=r['question']
 def s(t):
  a=q.index(t);return dict(text=t,start=a,end=a+len(t))
 if r['id']=='P08':
  r['aspects'][0]['negative_constraints']=[]
  r['aspects'][1]['request_cues'].insert(0,s('How do I'))
 if r['id']=='P10':
  r['aspects'][0]['identifiers'].insert(1,s('MyProps'))
 if r['id']=='P12':
  r['aspects'][0]['references']=[s('this configuration')]
  target=s('{ key: "nickname", props: { placeholder: "Café ☕" } }')
  r['aspects'][0]['resolved_antecedents']=[target]
  r['relations'].append(dict(kind='refers_to',head=s('this configuration'),tail=target))
 if r['id']=='P18':
  r['entities']['custom_identifier']=[s("'audit-shell'")]
  r['aspects'][0]['identifiers']=[s("'audit-shell'")]
 if r['id']=='P19': r['aspects'][0]['negative_constraints']=[s('stop this from being removed')]
 validate_annotation(r)
(p/'annotator-one-v2.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
