"""Offline paired inference; no gold files are opened."""
import os,sys,json,time,hashlib,gc
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HOME=str(HERE/'test-output/.cache'),PYTHONDONTWRITEBYTECODE='1')
sys.path.insert(0,str(HERE.parent/'adaptation/full_training'))
from native import load_model,schema_for,PeftModel
import torch
TYPES=['api','custom_identifier','literal','version','ui_adapter']
def main():
 for p,h in json.loads((HERE/'input-freeze.json').read_text()).items():
  assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
 torch.use_deterministic_algorithms(True)
 rows=json.loads((HERE/'inputs.json').read_text())
 freeze={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'PROTOCOL.md',HERE/'ANNOTATION.md',HERE/'run.py']}
 with (HERE/'test-output/run-freeze.json').open('x') as f:json.dump(freeze,f,indent=2)
 for model_name in ['base','adapted']:
  start=time.perf_counter();model=load_model()
  if model_name=='adapted':
   model=PeftModel.from_pretrained(model,str(HERE.parent/'adaptation/full_training/test-output/full-seed-1701/checkpoint-8/adapter'),is_trainable=False)
  model.eval();load_seconds=time.perf_counter()-start
  for schema_name in ['full','entities']:
   schema=schema_for(model) if schema_name=='full' else model.create_schema().entities(TYPES)
   with (HERE/f'test-output/{model_name}-{schema_name}.jsonl').open('x') as f:
    for i,row in enumerate(rows):
     start=time.perf_counter()
     try:
      with torch.inference_mode():
       output=model.extract(row['question'],schema,threshold=.5,include_spans=True,include_confidence=True,overlap_policy='nested')
      result={'output':output}
     except Exception as e:result={'error':type(e).__name__+': '+str(e)}
     result.update(id=row['id'],seconds=time.perf_counter()-start,load_seconds=load_seconds,model=model_name,schema=schema_name)
     f.write(json.dumps(result)+'\n');f.flush()
     if (i+1)%15==0: print(model_name,schema_name,i+1,flush=True)
  del model;gc.collect()
if __name__=='__main__':main()
