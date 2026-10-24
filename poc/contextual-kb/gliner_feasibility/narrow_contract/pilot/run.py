"""Frozen local base-model schema comparison; no labels are fed to inference."""
import json,os,sys,time,hashlib
from pathlib import Path
from contract import ROLES,adapt
HERE=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(path):
 for name,h in json.loads(path.read_text()).items():
  if digest(Path(name))!=h:raise ValueError('changed: '+name)
def main():
 check(HERE/'test-output/selection-freeze.json')
 files=[HERE/n for n in ('questions.json','gold.json','annotation-a.json','annotation-b.json','labels.json','PROTOCOL.md','ADJUDICATION.md','contract.py','run.py','score.py')]
 with (HERE/'test-output/inference-freeze.json').open('x') as f:json.dump({str(p):digest(p) for p in files},f,indent=2)
 os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HOME=str(HERE/'test-output/.cache'))
 sys.path.insert(0,str(HERE.parents[1]/'adaptation/full_training'))
 from native import load_model
 import torch
 torch.use_deterministic_algorithms(True)
 start=time.perf_counter();model=load_model();model.eval();load_seconds=time.perf_counter()-start
 labels=json.loads((HERE/'labels.json').read_text());assert list(labels)==list(ROLES)
 schemas={'bare':model.create_schema().entities(list(ROLES)),'described':model.create_schema().entities(labels)}
 assert dict(schemas['described'].schema['entity_descriptions'])==labels
 with (HERE/'test-output/schemas.json').open('x') as f:json.dump({k:s.to_dict() for k,s in schemas.items()},f,indent=2)
 with (HERE/'test-output/predictions.jsonl').open('x') as f:
  for i,q in enumerate(json.loads((HERE/'questions.json').read_text())):
   for name in (('bare','described') if i%2==0 else ('described','bare')):
    start=time.perf_counter()
    try:
     with torch.inference_mode():
      output=model.extract(q['question'],schemas[name],threshold=.5,include_spans=True,include_confidence=True,overlap_policy='nested')
     result={'output':output}
    except Exception as e:result={'error':type(e).__name__+': '+str(e)}
    inference_seconds=time.perf_counter()-start
    envelope,_,error=adapt(q['id'],q['question'],result)
    result.update(id=q['id'],schema=name,seconds=time.perf_counter()-start,inference_seconds=inference_seconds,load_seconds=load_seconds,envelope=envelope,validation_error=error)
    f.write(json.dumps(result)+'\n');f.flush()
   print(i+1,q['id'],flush=True)
 check(HERE/'test-output/inference-freeze.json')
if __name__=='__main__':main()
