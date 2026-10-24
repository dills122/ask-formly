"""Training primitives with explicit question weighting and checkpoint preservation."""
import hashlib
import random
from pathlib import Path
import numpy as np
import torch

ROLES = ('api_reference','registration_name','model_key','value','version','ui_adapter')


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def verify_manifest(manifest):
    changed = [p for p,h in manifest.items() if not Path(p).is_file() or digest(p) != h]
    if changed:
        raise ValueError('changed protected inputs: '+str(changed))
    return len(manifest)


def validate_rows(rows):
    ids = set(); used = []; empty = []
    for row in rows:
        name,text,occurrences = row['id'],row['text'],row['occurrences']
        if not isinstance(name,str) or not name or name in ids or not isinstance(text,str):
            raise ValueError('invalid/duplicate question identity')
        ids.add(name); seen = set()
        for o in occurrences:
            a,b,y = o['start'],o['end'],o['targets']
            if type(a) is not int or type(b) is not int or not 0 <= a < b <= len(text) or text[a:b] != o['text'] or (a,b) in seen:
                raise ValueError('invalid exact occurrence')
            seen.add((a,b))
            if len(y) != 7 or any(type(v) is not int or v not in (0,1) for v in y) or sum(y[1:]) != y[0]:
                raise ValueError('invalid complete-and-role targets')
            if y[0] and o.get('source_kind') != ROLES[y[1:].index(1)]:
                raise ValueError('role provenance mismatch')
            if not y[0] and not isinstance(o.get('negative_family'),str):
                raise ValueError('missing negative provenance')
        (used if occurrences else empty).append(row)
    return used,empty


def schedule(ids,seed,updates=124,batch_size=8):
    if not ids or len(ids) != len(set(ids)) or updates < 1 or batch_size < 1:
        raise ValueError('invalid schedule')
    rng = random.Random(seed); flat = []
    while len(flat) < updates*batch_size:
        cycle = list(ids); rng.shuffle(cycle); flat.extend(cycle)
    return [flat[i:i+batch_size] for i in range(0,updates*batch_size,batch_size)]


def batch_backward(model,rows,scorer):
    if not rows:
        raise ValueError('empty batch')
    total = 0.
    for row in rows:
        z,y = scorer(model,row)
        if z.ndim != 2 or z.shape != y.shape or z.shape[1] != 7 or not z.numel() or not torch.isfinite(z).all() or not torch.isfinite(y).all() or not ((y==0)|(y==1)).all():
            raise ValueError('invalid loss tensors')
        loss = torch.nn.functional.binary_cross_entropy_with_logits(z,y)/len(rows)
        total += float(loss.detach()); loss.backward()
    return total


def state_hashes(model):
    return {n:hashlib.sha256(v.detach().cpu().contiguous().numpy().tobytes()).hexdigest()
            for n,v in model.state_dict().items()}


def checkpoint(model,path,predict,save,load):
    """First/final verification includes buffers; loading may consume RNG."""
    rng = (random.getstate(),np.random.get_state(),torch.get_rng_state())
    mode = model.training
    try:
        path.mkdir(parents=True,exist_ok=False)
        model.eval(); before = state_hashes(model)
        with torch.no_grad(): expected = predict(model)
        save(model,path); fresh = load(path); fresh.eval()
        with torch.no_grad(): actual = predict(fresh)
        same_state = before == state_hashes(fresh) == state_hashes(model)
        if not same_state or actual != expected:
            raise ValueError('save/reload state or prediction mismatch')
        return dict(state_identical=True,predictions_identical=True,state_hashes=before)
    finally:
        random.setstate(rng[0]);np.random.set_state(rng[1]);torch.set_rng_state(rng[2]);model.train(mode)


def train_steps(model,by_id,batches,optimizer,scorer,save_at,log):
    trainable = {n:p for n,p in model.named_parameters() if p.requires_grad}
    optimized = [p for g in optimizer.param_groups for p in g['params']]
    if not trainable or any('lora_' not in n for n in trainable) or len(optimized) != len(trainable) or {id(p) for p in optimized} != {id(p) for p in trainable.values()}:
        raise ValueError('optimizer must contain exactly the new LoRA parameters')
    before = state_hashes(model); exposures = 0
    for step,ids in enumerate(batches,1):
        model.train(); optimizer.zero_grad(set_to_none=True)
        value = batch_backward(model,[by_id[i] for i in ids],scorer)
        norm = torch.nn.utils.clip_grad_norm_(optimized,1.,error_if_nonfinite=True)
        if not torch.isfinite(norm):
            raise ValueError('nonfinite gradient')
        optimizer.step();exposures += len(ids)
        log(dict(step=step,ids=ids,question_mean_bce=value,gradient_norm=float(norm)))
        if step in (1,len(batches)):
            current = state_hashes(model)
            if any(current[k] != v for k,v in before.items() if k not in trainable):
                raise ValueError('frozen parameter or buffer changed')
            save_at(step)
    after = state_hashes(model)
    changed = [k for k in before if before[k] != after[k]]
    frozen = [k for k in changed if k not in trainable]
    if frozen or not changed:
        raise ValueError('frozen mutation or no update')
    return dict(updates=len(batches),exposures=exposures,changed_trainable=len(changed),changed_frozen_state=frozen)


def guarded_run(work,checks,on_success,on_failure):
    """Audit even failed setup/work, and never publish completion before integrity."""
    errors = []; result = None; cause = None
    try:
        result = work()
    except BaseException as exc:
        cause = exc; errors.append(dict(phase='work',type=type(exc).__name__,message=str(exc)))
    for name,check in checks:
        try:
            check()
        except BaseException as exc:
            cause = cause or exc
            errors.append(dict(phase=name,type=type(exc).__name__,message=str(exc)))
    if errors:
        on_failure(errors)
        raise RuntimeError('run failed; see failure receipt') from cause
    on_success(result)
    return result
