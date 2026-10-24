"""Bounded loop and development-grade selection. No evaluation loader."""
import json
import random
import time
import torch
from checkpoint import parameter_hashes, write_json, seed_all


def groups(rows, batch_size=2, accumulation=8):
    if batch_size < 1 or accumulation < 1: raise ValueError('Invalid accumulation')
    for start in range(0, len(rows), batch_size*accumulation):
        block = rows[start:start+batch_size*accumulation]
        yield [block[i:i+batch_size] for i in range(0,len(block),batch_size)]


def train_epoch(model, rows, optimizer, loss_fn, batch_size=2, accumulation=8,
                clip=1., on_step=lambda event: None):
    """loss_fn returns a mean over examples, not a native batch-summed loss."""
    params = [p for p in model.parameters() if p.requires_grad]
    steps = 0
    model.train()
    for block in groups(rows, batch_size, accumulation):
        optimizer.zero_grad(set_to_none=True)
        size = sum(map(len,block)); losses=[]
        try:
            for microbatch in block:
                loss = loss_fn(model, microbatch)
                if loss.numel()!=1 or not torch.isfinite(loss): raise ValueError('Nonfinite/scalar loss')
                losses.append(float(loss.detach()))
                (loss*(len(microbatch)/size)).backward()
            grads = [p.grad for p in params if p.grad is not None]
            if not grads or any(not torch.isfinite(g).all() for g in grads): raise ValueError('Invalid gradients')
            norm = torch.nn.utils.clip_grad_norm_(params, clip, error_if_nonfinite=True)
            optimizer.step(); steps += 1
            on_step({'ids':[r.get('id') for batch in block for r in batch],
                     'examples':size, 'microbatch_losses':losses, 'gradient_norm':float(norm)})
        finally:
            optimizer.zero_grad(set_to_none=True)
    return steps


def run_training(model, rows, optimizer, loss_fn, verifier, predict_dev, destination,
                 seed, epochs=8, preflight=False):
    if seed not in (1701,2903): raise ValueError('Unregistered seed')
    if (len(rows),epochs) != ((24,1) if preflight else (120,8)):
        raise ValueError('Wrong fixed run size/budget')
    if len({r['id'] for r in rows}) != len(rows): raise ValueError('Duplicate training IDs')
    trainable = {n for n,p in model.named_parameters() if p.requires_grad}
    if not trainable or any('lora' not in n or 'encoder' not in n for n in trainable):
        raise ValueError('Only encoder LoRA may train')
    seed_all(seed)
    initial = parameter_hashes(model)
    frozen = {n:h for n,h in initial.items() if n not in trainable}
    report = {'status':'started','steps':0,'epochs':[], 'seed':seed,
              'scope':'pilot preflight' if preflight else 'training only'}
    started = time.monotonic()
    with (destination/'updates.jsonl').open('x') as log:
        def record(event):
            report['steps'] += 1
            event.update(step=report['steps'],elapsed=time.monotonic()-started)
            log.write(json.dumps(event,allow_nan=False)+'\n'); log.flush()
        try:
            for epoch in range(1,epochs+1):
                ordered = list(rows); random.Random(seed+epoch).shuffle(ordered)
                train_epoch(model,ordered,optimizer,loss_fn,on_step=record)
                current = parameter_hashes(model)
                if any(current[n]!=h for n,h in frozen.items()): raise ValueError('Frozen weights changed')
                receipt = verifier(model,epoch,report['steps'])
                if receipt['status']!='verified': raise ValueError('Checkpoint not verified')
                outputs = predict_dev(model,epoch)
                write_json(destination/f'dev-epoch-{epoch}.json',outputs)
                report['epochs'].append({'epoch':epoch,'step':report['steps'],'verified':True})
            report['changed_adapter_tensors']=sum(current[n]!=initial[n] for n in trainable)
            report['changed_frozen_tensors']=0
            if not report['changed_adapter_tensors']: raise ValueError('No adapter tensor changed')
            report['status']='completed'
            return report
        except BaseException as exc:
            report.update(status='failed',error={'type':type(exc).__name__,'message':str(exc)})
            raise
        finally:
            report['seconds']=time.monotonic()-started
            write_json(destination/'run.json',report)


def select_checkpoint(entries):
    """Consumes adjudicated blinded dev grades; never grades model semantics."""
    if len(entries)!=8 or {e['epoch'] for e in entries}!=set(range(1,9)):
        raise ValueError('Need all eight completed epochs')
    for e in entries:
        if e['verified'] is not True or e['cases']!=30:
            raise ValueError('Unverified/incomplete checkpoint')
        if any(type(e[k]) is not int or not 0<=e[k]<=30 for k in ('complete','critical')):
            raise ValueError('Invalid grades')
    return min(entries,key=lambda e:(-e['complete'],e['critical'],e['epoch']))
