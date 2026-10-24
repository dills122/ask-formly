"""Offline single-pass inference, frozen inputs, no training or DB access."""
import gc
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import time
from integration import integrate

HERE = Path(__file__).resolve().parent
POC = HERE.parents[1]
NARROW = POC / 'gliner_feasibility/narrow_contract'
OUT = HERE / 'test-output'

def read(path): return json.loads(path.read_text())
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path, value):
    with path.open('x') as f: json.dump(value, f, indent=2, allow_nan=False)
def verify(manifest):
    for path, expected in manifest.items():
        if digest(Path(path)) != expected: raise ValueError('frozen file changed: '+path)
def parameters(model):
    return {name:hashlib.sha256(p.detach().cpu().contiguous().numpy().tobytes()).hexdigest()
            for name,p in model.named_parameters()}

def main():
    freeze=read(OUT/'run-freeze.json');verify(freeze)
    if read(HERE/'REVIEW-2-DECISION.json')['verdict'] != 'ready':
        raise ValueError('preflight not ready')
    records=read(HERE/'data/records.json')
    if len(records)!=174 or len({r['id'] for r in records})!=174:raise ValueError('record coverage')
    output=OUT/'inference';output.mkdir(exist_ok=False)
    save(output/'first-save.json',dict(freeze_sha256=digest(OUT/'run-freeze.json'),records=174,python=sys.version))
    with (output/'foundation.jsonl').open('x') as f:
        for row in records:
            result=integrate(row['request'],row['output'])
            f.write(json.dumps(dict(id=row['id'],**result),allow_nan=False)+'\n');f.flush()
    os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HOME=str(output/'.cache'),TOKENIZERS_PARALLELISM='false')
    started=time.perf_counter()
    import torch
    from gliner2 import AutoExtractor
    from gliner2.processor import SamplingConfig
    from peft import PeftModel
    import_seconds=time.perf_counter()-started
    torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
    metadata=dict(import_seconds=import_seconds,versions={x:importlib.metadata.version(x) for x in ('torch','gliner2','peft')},device='cpu',dtype='float32',threads=4)
    save(output/'environment.json',metadata)
    labels=read(NARROW/'pilot/labels.json')
    for seed in (1701,1702):
        started=time.perf_counter();torch.manual_seed(1701)
        base=AutoExtractor.from_pretrained(str(POC/'gliner_feasibility/models/gliner2.5-base-v1'),local_files_only=True,map_location='cpu').float()
        base.processor.sampling_config=SamplingConfig(remove_json_structure_prob=0,shuffle_json_fields=False,remove_json_field_prob=0,remove_entities_prob=0,shuffle_entities=False,remove_entity_prob=0,synthetic_entity_label_prob=0,remove_relations_prob=0,swap_head_tail_prob=0,remove_classification_prob=0,shuffle_classification_labels=False,remove_classification_label_prob=0,synthetic_label_prob=0,include_true_label_prob=1)
        checkpoint=NARROW/f'role_boundary_adaptation/test-output/after-{seed}'
        model=PeftModel.from_pretrained(base,str(checkpoint/'epoch-6/adapter'),is_trainable=False);model.eval()
        for parameter in model.parameters():parameter.requires_grad_(False)
        schema=model.create_schema().entities(labels)
        load_seconds=time.perf_counter()-started
        before=parameters(model)
        if before!=read(checkpoint/'training-receipt.json')['final_hashes']:raise ValueError('in-memory checkpoint mismatch')
        save(output/f'{seed}-before.json',dict(load_seconds=load_seconds,parameters=before))
        def extract(text):
            with torch.inference_mode():
                return model.extract(text,schema,threshold=.5,overlap_policy='flat',include_spans=True,include_confidence=True)
        with (output/f'{seed}.jsonl').open('x') as f:
            for number,row in enumerate(records,1):
                result=integrate(row['request'],row['output'],extract)
                f.write(json.dumps(dict(id=row['id'],**result),allow_nan=False)+'\n');f.flush()
                if number%30==0:print(seed,number,'/',len(records),flush=True)
        after=parameters(model)
        save(output/f'{seed}-after.json',dict(parameters=after,unchanged=after==before))
        if after!=before:raise ValueError('model mutated')
        del model,base;gc.collect()
    verify(freeze)
    save(output/'completion.json',dict(records=174,models=[1701,1702],complete=True))
    save(OUT/'inference-freeze.json',{str(p):digest(p) for p in output.rglob('*') if p.is_file()})

if __name__=='__main__':main()
