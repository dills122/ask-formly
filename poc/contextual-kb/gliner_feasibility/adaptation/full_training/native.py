"""Pinned GLiNER binding; only canonical question annotations enter training."""
from collections.abc import Mapping
from dataclasses import fields,is_dataclass
from enum import Enum
import hashlib
import json
from pathlib import Path
import sys
import torch
from checkpoint import seed_all,tensor_hash,REQUIRED_LOSSES

HERE=Path(__file__).resolve().parent
REVISION=HERE.parent/'identity_revision'
sys.path.insert(0,str(REVISION))
from revision import FIELDS,export_example,load_pilot,BASE
from compatibility import load_model,prepare as native_prepare,verify_transport
from gliner2.training.trainer import ExtractorTrainer,TrainingConfig
from peft import PeftModel


def prepare(model,row):
    if len(row.get('aspects',[]))>32:
        raise ValueError('Native checkpoint has only 32 record instance queries')
    return native_prepare(model,row)


def fingerprint(value):
    if torch.is_tensor(value):return {'shape':list(value.shape),'dtype':str(value.dtype),'sha256':tensor_hash(value)}
    if isinstance(value,Enum):return {'enum':type(value).__qualname__,'value':fingerprint(value.value)}
    if value is None or isinstance(value,(str,int,float,bool)):return value
    if isinstance(value,type):return {'type':value.__module__+'.'+value.__qualname__}
    if isinstance(value,Mapping):return {str(k):fingerprint(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [fingerprint(v) for v in value]
    if isinstance(value,(set,frozenset)):return sorted([fingerprint(v) for v in value],key=lambda v:json.dumps(v,sort_keys=True))
    if is_dataclass(value):return {f.name:fingerprint(getattr(value,f.name)) for f in fields(value)}
    if hasattr(value,'__dict__'):return {k:fingerprint(v) for k,v in vars(value).items()}
    raise TypeError(f'Unsupported batch metadata: {type(value)}')


def schema_for(model):
    schema=(model.create_schema().entities(['api','custom_identifier','literal','version','ui_adapter'])
            .relations(['has_value','refers_to'])
            .classification('interpretation',['clear','needs_clarification']))
    record=schema.structure('request',mode='anchorless')
    record.field('target_anchor',dtype='str')
    for name in FIELDS:record.field(name,dtype='list')
    return schema


def predict(model,questions):
    """Only strings are accepted; gold records cannot be passed to inference."""
    if any(not isinstance(q,str) for q in questions):raise ValueError('Inference accepts question strings only')
    model.eval();schema=schema_for(model)
    with torch.inference_mode():
        return [model.extract(q,schema,threshold=.5,include_spans=True,
                              include_confidence=True,overlap_policy='nested') for q in questions]


def loss_terms(output):
    terms={k:float(v.detach()) for k,v in output.losses.items() if torch.is_tensor(v) and v.numel()==1}
    terms['total_loss']=float(output.total_loss.detach())
    if not REQUIRED_LOSSES.issubset(terms):raise ValueError('Required native loss dropped')
    json.dumps(terms,allow_nan=False)
    return terms


class NativeBackend:
    def capture(self,model,rows):
        cases=[]
        model.train()
        with torch.no_grad():
            for index,row in enumerate(rows):
                seed_all(1701+index)
                batch=prepare(model,row)
                frozen_batch=fingerprint(batch)
                out=model(batch,gold_injection_prob=1.)
                cases.append({'id':row['id'],'batch':frozen_batch,'losses':loss_terms(out)})
        outputs=predict(model,[r['question'] for r in rows])
        for case,output in zip(cases,outputs):case['output']=output
        return {'cases':cases}

    def save(self,model,path):model.save_pretrained(str(path))

    def restore(self,path):
        return PeftModel.from_pretrained(load_model(),str(path),is_trainable=False)


def make_model(seed,output):
    model=load_model()
    seed_all(seed)  # load_model uses historical seed; reset before adapter initialization.
    trainer=ExtractorTrainer(model,TrainingConfig(
        output_dir=str(output/'native-trainer'),num_epochs=8,max_steps=64,batch_size=2,
        gradient_accumulation_steps=8,encoder_lr=1e-5,task_lr=5e-4,
        fp16=False,bf16=False,num_workers=0,use_lora=True,lora_r=8,
        lora_alpha=16.,lora_dropout=0.,lora_target_modules=['encoder'],
        save_adapter_only=True,report_to_wandb=False,eval_strategy='no',seed=seed))
    return trainer.model


def mean_loss(model,rows,log=None):
    # Native heads reduce over different numbers of fields/edges, not uniformly
    # over examples. Evaluate each example and explicitly mean the two losses.
    losses=[]
    for row in rows:
        batch=prepare(model,row)
        out=model(batch,gold_injection_prob=1.)
        terms=loss_terms(out)
        if log is not None:
            log.write(json.dumps({'id':row['id'],'batch':fingerprint(batch),'losses':terms},allow_nan=False)+'\n')
            log.flush()
        losses.append(out.total_loss)
    return torch.stack(losses).mean()
