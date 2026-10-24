"""One bounded pilot pass: task gradients, 24 updates, frozen weights and reload.

No checkpoint selection, tuning, held-out input or accuracy grading. Uses installed
GLiNER/PEFT training setup and PyTorch optimizer; this is not a full trainer run.
"""
import hashlib
import json
import os
import sys
from time import perf_counter
from revision import HERE,BASE,FIELDS,load_pilot,export_example,check_access
os.environ.update(HF_HOME=str(HERE/'.cache/hf'),HF_HUB_OFFLINE='1',
                  TRANSFORMERS_OFFLINE='1',TOKENIZERS_PARALLELISM='false',
                  TMPDIR=str(HERE/'.cache/tmp'))
import torch
from gliner2.training.trainer import ExtractorTrainer,TrainingConfig
from peft import PeftModel
from compatibility import load_model,prepare,verify_transport


def tensor_hash(t):
    return hashlib.sha256(t.detach().cpu().contiguous().numpy().tobytes()).hexdigest()


def schema_for(model):
    schema=(model.create_schema().entities(['api','custom_identifier','literal','version','ui_adapter'])
            .relations(['has_value','refers_to'])
            .classification('interpretation',['clear','needs_clarification']))
    record=schema.structure('request',mode='anchorless')
    record.field('target_anchor',dtype='str')
    for name in FIELDS:record.field(name,dtype='list')
    return schema


def predictions(model,rows):
    model.eval();schema=schema_for(model)
    with torch.inference_mode():
        return [model.extract(r['question'],schema,threshold=.5,include_spans=True,
                              include_confidence=True,overlap_policy='nested') for r in rows]


def run_smoke():
    started=perf_counter()
    output=HERE/'smoke-run'
    output.mkdir(exist_ok=False)
    (HERE/'.cache/tmp').mkdir(parents=True,exist_ok=True)
    report={'status':'started','optimizer_steps':0,'cases':[],
            'training_scope':'one pilot pass; not full trainer/quality evaluation'}
    # Per-attempt output is exclusive; do not overwrite failed runs to hide them.
    log=(output/'steps.jsonl').open('x')
    try:
        rows=load_pilot()
        sys.addaudithook(check_access)
        base=load_model()
        for row in rows:verify_transport(row,prepare(base,row))
        trainer=ExtractorTrainer(base,TrainingConfig(
            output_dir=str(output/'trainer'),num_epochs=1,max_steps=24,batch_size=1,
            gradient_accumulation_steps=1,encoder_lr=1e-5,task_lr=5e-4,
            fp16=False,bf16=False,num_workers=0,use_lora=True,lora_r=8,
            lora_alpha=16.,lora_dropout=0.,lora_target_modules=['encoder'],
            save_adapter_only=True,report_to_wandb=False,eval_strategy='no',seed=1701))
        model=trainer.model
        trainable={n:p for n,p in model.named_parameters() if p.requires_grad}
        if not trainable or any('lora_' not in n for n in trainable):
            raise AssertionError('Unexpected non-adapter trainable parameters')
        inventory={n:{'shape':list(p.shape),'count':p.numel(),'dtype':str(p.dtype)} for n,p in trainable.items()}
        (output/'trainable.json').write_text(json.dumps(inventory,indent=2)+'\n')
        frozen={n:tensor_hash(p) for n,p in model.named_parameters() if not p.requires_grad}
        before={n:tensor_hash(p) for n,p in trainable.items()}
        params=list(trainable.values())
        # Fixed positive example P02 exercises every task. No update in these checks.
        source=export_example(rows[1])
        task_keys={'entities':['entities'],
                   'records':['json_structures','record_metadata'],
                   'relations':['relations'],'classification':['classifications']}
        norms={};model.train()
        for task,keys in task_keys.items():
            batch=model.processor.collate_fn_train(
                [(source['input'],{k:source['output'][k] for k in keys})],
                architecture='boundary',error_policy='raise',on_capacity_exceeded='raise',
                dedupe_contained_entity_spans=False)
            out=model(batch,gold_injection_prob=1.)
            if task=='records':loss=out.losses['record_field_loss']+out.losses['record_object_loss']
            elif task=='relations':loss=out.losses['relation_loss']
            elif task=='classification':loss=out.losses['classification_loss']
            else:loss=out.total_loss
            if not torch.isfinite(loss):raise AssertionError(f'Nonfinite {task} loss')
            grads=torch.autograd.grad(loss,params,allow_unused=True)
            if any(not torch.isfinite(g).all() for g in grads if g is not None):raise AssertionError('Nonfinite gradient')
            norms[task]=sum(float(g.abs().sum()) for g in grads if g is not None)
            if norms[task]<=0:raise AssertionError(f'No adapter gradient for {task}')
            log.write(json.dumps({'task':task,'loss':float(loss.detach()),'gradient_l1':norms[task]})+'\n');log.flush()
            del out,grads,loss
        report['task_gradient_norms']=norms
        optimizer=torch.optim.AdamW(params,lr=1e-5,weight_decay=.01)
        for row in rows:
            optimizer.zero_grad(set_to_none=True)
            batch=prepare(model,row)
            out=model(batch,gold_injection_prob=1.)
            required={'classification_loss','record_object_loss','record_field_loss','relation_loss'}
            if not required.issubset(out.losses):raise AssertionError(f'Dropped auxiliary losses: {out.losses.keys()}')
            loss=out.total_loss
            if not torch.isfinite(loss):raise AssertionError('Nonfinite joint loss')
            loss.backward()
            grads=[p.grad for p in params if p.grad is not None]
            if not grads or any(not torch.isfinite(g).all() for g in grads):raise AssertionError('Invalid joint gradients')
            norm=torch.nn.utils.clip_grad_norm_(params,1.,error_if_nonfinite=True)
            optimizer.step()
            report['optimizer_steps']+=1;report['cases'].append(row['id'])
            log.write(json.dumps({'id':row['id'],'loss':float(loss.detach()),'gradient_norm':float(norm),
                                 'losses':{k:float(v.detach()) for k,v in out.losses.items() if torch.is_tensor(v) and v.numel()==1}})+'\n');log.flush()
            print(row['id'],report['optimizer_steps'],round(float(loss.detach()),4),flush=True)
            del out,loss,batch
        report['changed_adapter_tensors']=sum(tensor_hash(p)!=before[n] for n,p in trainable.items())
        report['changed_frozen_tensors']=sum(tensor_hash(p)!=frozen[n] for n,p in model.named_parameters() if n in frozen)
        if report['changed_frozen_tensors']:raise AssertionError('Frozen base changed')
        saved=output/'adapter';model.save_pretrained(str(saved))
        before_predictions=predictions(model,rows)
        (output/'before-reload.json').write_text(json.dumps(before_predictions,ensure_ascii=False,indent=2)+'\n')
        fresh=load_model()
        restored=PeftModel.from_pretrained(fresh,str(saved),is_trainable=False)
        after_predictions=predictions(restored,rows)
        (output/'after-reload.json').write_text(json.dumps(after_predictions,ensure_ascii=False,indent=2)+'\n')
        report['reload_checks']=len(rows)
        report['reload_parity']=before_predictions==after_predictions
        if not report['reload_parity']:raise AssertionError('Prediction reload mismatch')
        report['status']='completed'
        return report
    except BaseException as exc:
        report['status']='failed';report['error']={'type':type(exc).__name__,'message':str(exc)}
        raise
    finally:
        report['seconds']=perf_counter()-started
        log.close()
        (output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
