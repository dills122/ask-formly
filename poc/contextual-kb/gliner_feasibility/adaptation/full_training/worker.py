"""Offline pilot preflight or one bounded training seed; no evaluation command."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['preflight','train'])
    parser.add_argument('--seed',type=int,choices=[1701,2903],default=1701)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    output=args.output.resolve()
    if not output.is_relative_to(HERE/'test-output') or not output.is_dir():
        parser.error('Use controller.py with a fresh run directory')
    cache=output/'.cache';(cache/'tmp').mkdir(parents=True,exist_ok=False)
    os.environ.update(HF_HOME=str(cache/'hf'),HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',
                      TOKENIZERS_PARALLELISM='false',TMPDIR=str(cache/'tmp'),
                      PYTHONDONTWRITEBYTECODE='1',WANDB_DISABLED='true')
    from inputs import access_policy,load_manifest
    revision=HERE.parent/'identity_revision';pilot=HERE.parent/'pilot';base=HERE.parents[1]
    allowed=list(HERE.glob('*.py'))+list(revision.glob('*.py'))+list(pilot.glob('*.py'))
    allowed += [pilot/'adjudicated-v2.json']
    if args.mode=='train':allowed += [HERE/'training-manifest.json',HERE/'data/train.json',HERE/'data/dev.json']
    sys.addaudithook(access_policy(HERE.parents[4],allowed,output,[base/'models',base/'env']))
    import torch
    from checkpoint import verify_first_save,write_json,parameter_hashes,preserve_state
    from harness import run_training
    from native import NativeBackend,make_model,load_pilot,mean_loss,predict,prepare,verify_transport
    torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
    pilot_rows=load_pilot()
    if args.mode=='preflight':
        rows=pilot_rows;dev=[];manifest={'mode':'frozen-pilot'}
    else:
        manifest,rows,dev=load_manifest(HERE/'training-manifest.json')
        indexed={r['id']:r for r in rows}
        if any(indexed.get(r['id'])!=r for r in pilot_rows):
            raise ValueError('Full training must include unchanged canonical pilot rows')
    write_json(output/'inputs.json',{'manifest':manifest,'train_ids':[r['id'] for r in rows],
                                   'dev_ids':[r['id'] for r in dev]})
    model=make_model(args.seed,output)
    inventory={n:{'shape':list(p.shape),'trainable':p.requires_grad,'dtype':str(p.dtype)}
               for n,p in model.named_parameters()}
    write_json(output/'parameters.json',inventory)
    write_json(output/'initial-parameters.json',parameter_hashes(model))
    # All input labels must survive strict native preprocessing before any update.
    transport=[verify_transport(r,prepare(model,r)) for r in rows+dev]
    write_json(output/'transport.json',transport)
    from native import schema_for
    schema=schema_for(model).build()
    config={'seed':args.seed,'epochs':1 if args.mode=='preflight' else 8,
            'logical_batch_size':2,'accumulation':8,'native_forward_batch_size':1,
            'lr':1e-5,'weight_decay':.01,'clip':1.,'dtype':'float32','threads':4,
            'base_revision':'54785d51df8d86a0d8f2eb212fec15871aad2c4d',
            'gold_injection_training':1.,'inference_threshold':.5}
    from native import fingerprint
    schema_fingerprint=fingerprint(schema)
    write_json(output/'schema.json',schema_fingerprint)
    write_json(output/'config.json',config)
    import importlib.metadata
    write_json(output/'runtime.json',{p:importlib.metadata.version(p) for p in
                                     ('gliner2','torch','transformers','peft','numpy')})
    def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()
    context={'seed':args.seed,'base_sha':digest({n:h for n,h in parameter_hashes(model).items()
                                              if not dict(model.named_parameters())[n].requires_grad}),
             'schema_sha':digest(schema_fingerprint),'config_sha':digest(config)}
    backend=NativeBackend()
    def verify(model,epoch,step):
        return verify_first_save(model,backend,pilot_rows,output/f'checkpoint-{epoch}',
                                 dict(context,epoch=epoch,step=step))
    def dev_predictions(model,epoch):
        with preserve_state(model):
            return [{'id':r['id'],'output':p} for r,p in zip(dev,predict(model,[r['question'] for r in dev]))]
    if dev:
        from native import load_model
        base_model=load_model()
        write_json(output/'g0-dev.json',[{'id':r['id'],'output':p} for r,p in
                                        zip(dev,predict(base_model,[r['question'] for r in dev]))])
        del base_model
    optimizer=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=1e-5,weight_decay=.01)
    with (output/'task-losses.jsonl').open('x') as log:
        result=run_training(model,rows,optimizer,lambda m,rs:mean_loss(m,rs,log),verify,dev_predictions,
                            output,seed=args.seed,epochs=config['epochs'],preflight=args.mode=='preflight')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':
    try:main()
    except BaseException as exc:
        # Parent also records process failure/timeout even if failure precedes run.json.
        print(json.dumps({'worker_error':type(exc).__name__,'message':str(exc)}),file=sys.stderr,flush=True)
        raise
