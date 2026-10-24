import json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
SOURCE=P.parents[1]/'agent_contract/refinement_v2'
def save(name,value):
 with (P/name).open('x') as f:json.dump(value,f,indent=2,ensure_ascii=False)
def main():
 cases=json.loads((SOURCE/'cases.json').read_text());outputs={r['id']:r['output'] for r in json.loads((SOURCE/'test-output/beta1.json').read_text())}
 rows=[]
 for case in cases:
  rows.append({'id':case['id']+'/original','parent':case['id'],'arm':'original','question':case['request']})
  for i,q in enumerate(outputs[case['id']]['formly_questions'],1):
   rows.append({'id':case['id']+f'/focused/{i}','parent':case['id'],'arm':'focused','question':q['question']})
 save('inputs.json',rows)
 for i in range(3):
  ids={c['id'] for c in cases[i*10:(i+1)*10]}
  save(f'annotation-{i+1}.json',[r for r in rows if r['parent'] in ids])
 paths=[SOURCE/'cases.json',SOURCE/'test-output/beta1.json',P/'inputs.json']
 adapter=P.parent/'adaptation/full_training/test-output/full-seed-1701/checkpoint-8/adapter'
 paths += list(adapter.glob('*'))
 save('input-freeze.json',{str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()})
 print(len(rows),'inputs',sum(r['arm']=='focused' for r in rows),'focused')
if __name__=='__main__':main()
