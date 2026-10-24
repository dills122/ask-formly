"""Run the two immutable extractors on the new frozen development questions."""
import gc,hashlib,json,os,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parents[1];NARROW=POC/'gliner_feasibility/narrow_contract'
sys.path.insert(0,str(POC))
from agent_contract.gliner_integration_v1.integration import integrate

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):
 with p.open('x') as f:json.dump(v,f,indent=2,allow_nan=False)
def verify():
 for p,h in read(HERE/'test-output/run-freeze.json').items():
  if sha(Path(p))!=h:raise ValueError('input drift '+p)
def weights(model):return {n:hashlib.sha256(p.detach().cpu().contiguous().numpy().tobytes()).hexdigest() for n,p in model.named_parameters()}
def main():
 verify()
 if read(HERE/'PREFLIGHT-DECISION.json')['verdict']!='ready':raise ValueError('preflight required')
 out=HERE/'test-output/extraction';out.mkdir(exist_ok=False);write(out/'first-save.json',{'freeze':sha(HERE/'test-output/run-freeze.json')})
 rows=read(HERE/'data/records.json')
 if len(rows)!=36 or len({r['id'] for r in rows})!=36:raise ValueError('input coverage')
 with (out/'foundation.jsonl').open('x') as f:
  for r in rows:f.write(json.dumps(dict(id=r['id'],batch=r['batch'],**integrate(r['request'],r['output'])))+'\n')
 os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HOME=str(out/'.cache'),TOKENIZERS_PARALLELISM='false')
 import torch
 from gliner2 import AutoExtractor
 from gliner2.processor import SamplingConfig
 from peft import PeftModel
 torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
 for seed in (1701,1702):
  started=time.perf_counter();torch.manual_seed(1701)
  base=AutoExtractor.from_pretrained(str(POC/'gliner_feasibility/models/gliner2.5-base-v1'),local_files_only=True,map_location='cpu').float()
  base.processor.sampling_config=SamplingConfig(remove_json_structure_prob=0,shuffle_json_fields=False,remove_json_field_prob=0,remove_entities_prob=0,shuffle_entities=False,remove_entity_prob=0,synthetic_entity_label_prob=0,remove_relations_prob=0,swap_head_tail_prob=0,remove_classification_prob=0,shuffle_classification_labels=False,remove_classification_label_prob=0,synthetic_label_prob=0,include_true_label_prob=1)
  checkpoint=NARROW/f'role_boundary_adaptation/test-output/after-{seed}'
  model=PeftModel.from_pretrained(base,str(checkpoint/'epoch-6/adapter'),is_trainable=False);model.eval()
  for parameter in model.parameters():parameter.requires_grad_(False)
  schema=model.create_schema().entities(read(NARROW/'pilot/labels.json'));load=time.perf_counter()-started
  before=weights(model)
  if before!=read(checkpoint/'training-receipt.json')['final_hashes']:raise ValueError('checkpoint mismatch')
  write(out/f'{seed}-before.json',dict(parameters=before,load_seconds=load))
  def predict(text):
   with torch.inference_mode():return model.extract(text,schema,threshold=.5,overlap_policy='flat',include_spans=True,include_confidence=True)
  with (out/f'{seed}.jsonl').open('x') as f:
   for r in rows:
    result=integrate(r['request'],r['output'],predict);f.write(json.dumps(dict(id=r['id'],batch=r['batch'],**result),allow_nan=False)+'\n');f.flush()
  after=weights(model);write(out/f'{seed}-after.json',dict(parameters=after,unchanged=after==before))
  if before!=after:raise ValueError('model changed')
  print('completed',seed,flush=True);del model,base;gc.collect()
 verify();write(out/'completion.json',dict(records=36,seeds=[1701,1702],complete=True))
 write(HERE/'test-output/extraction-freeze.json',{str(p):sha(p) for p in out.rglob('*') if p.is_file()})
if __name__=='__main__':main()
