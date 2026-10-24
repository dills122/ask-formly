"""Offline runner. Default preflight performs no encoder forward or optimizer step."""
import argparse
import gc
import importlib.metadata
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NARROW = HERE.parent
ROOT = HERE.parents[4]
PLAN = NARROW/'verifier_training_plan'
sys.path.insert(0,str(NARROW/'supervised_trial'))
from train import load_model, seed, PeftModel, torch
sys.path.insert(0,str(NARROW/'verifier_compatibility'))
from verifier import score, schema, align
sys.path.insert(0,str(HERE))
from harness import digest, verify_manifest, validate_rows, schedule, checkpoint, train_steps, guarded_run

CONFIG = dict(seeds=[1701,1702],updates=124,batch_size=8,learning_rate=1e-4,weight_decay=.01,
              gradient_clip=1.,lora_r=8,lora_alpha=16.,lora_dropout=0.,targets=['encoder','extractive_head'],
              dtype='float32',device='cpu',threads=4,selection='final scheduled update only')


def read(path):
    return json.loads(path.read_text())


def write(path,value):
    with path.open('x') as stream:
        json.dump(value,stream,indent=2,allow_nan=False)


def protected():
    prior = PLAN/'test-output'
    manifests = [ROOT/r['manifest'] for r in read(prior/'protected-after.json')]+[prior/'final-freeze.json']
    reports = []
    for manifest in manifests:
        resolved = {}
        for name,expected in read(manifest).items():
            p = Path(name)
            if not p.is_absolute():
                p = ROOT/p if p.parts[0]=='poc' else manifest.parent.parent/p
            resolved[str(p)] = expected
        reports.append(dict(manifest=str(manifest.relative_to(ROOT)),checked=verify_manifest(resolved),changed=[]))
    return reports


def inputs():
    rows = read(PLAN/'test-output/training-labels.json')
    calibration = read(PLAN/'test-output/calibration.json')
    used,empty = validate_rows(rows);validate_rows(calibration)
    if (len(rows),len(used),len(empty),len(calibration)) != (242,216,26,30):
        raise ValueError('frozen dataset counts differ')
    if [r['id'] for r in empty] != read(PLAN/'test-output/training-row-policy.json')['coverage_only_ids']:
        raise ValueError('coverage-only row policy differs')
    if sum(o['targets'][0] for r in rows for o in r['occurrences']) != 580 or sum(not o['targets'][0] for r in rows for o in r['occurrences']) != 534:
        raise ValueError('training target counts differ')
    if {r['id'] for r in rows}&{r['id'] for r in calibration}:
        raise ValueError('split ID overlap')
    def norm(text):return ' '.join(text.lower().split())
    if {norm(r['text']) for r in rows}&{norm(r['text']) for r in calibration}:
        raise ValueError('split text overlap')
    return rows,used,empty,calibration


def preflight(out,rows,calibration):
    model = load_model();model.eval()
    schemas,_ = model._build_schema_dicts_and_metadata([schema(model)])
    receipt = []
    for split,items in (('training',rows),('calibration',calibration)):
        for row in items:
            offsets = [(o['start'],o['end']) for o in row['occurrences']]
            if not offsets:
                receipt.append(dict(split=split,id=row['id'],status='coverage-only',occurrences=0));continue
            batch = model.processor.collate_fn_inference([(row['text'],schemas[0])],architecture='boundary',error_policy='raise')
            supported,unsupported,_ = align(row['text'],offsets,batch.start_mappings[0],batch.end_mappings[0])
            if unsupported or supported != offsets:
                raise ValueError('transport differs from qualified frozen input: '+row['id'])
            receipt.append(dict(split=split,id=row['id'],status='exact',occurrences=len(offsets)))
    write(out/'transport.json',receipt)
    write(out/'native-settings.json',dict(pair_temperature=model.boundary_settings.pair_temperature,schema=schemas,
        tokenizer_sha256=__import__('hashlib').sha256(model.processor.tokenizer.backend_tokenizer.to_str().encode()).hexdigest()))
    del model;gc.collect()


def scorer(model,row):
    offsets = [(o['start'],o['end']) for o in row['occurrences']]
    z,supported,unsupported,_ = score(model,row['text'],offsets)
    if unsupported or supported != offsets:
        raise ValueError('unexpected training transport drift')
    return z,torch.tensor([o['targets'] for o in row['occurrences']],dtype=z.dtype,device=z.device)


def train_one(out,number,used,batches):
    model = load_model();seed(number)
    model = model.apply_lora(r=CONFIG['lora_r'],alpha=CONFIG['lora_alpha'],dropout=0.,targets=CONFIG['targets'])
    by_id = {r['id']:r for r in used}
    # Fixed training-only save panel; never calibration/evaluation inputs.
    panel = used[-8:]
    write(out/'checkpoint-panel.json',[r['id'] for r in panel])
    def predict(candidate):
        return [scorer(candidate,row)[0].detach().tolist() for row in panel]
    def save(model,path):model.save_pretrained(str(path/'adapter'))
    def reload(path):return PeftModel.from_pretrained(load_model(),str(path/'adapter'),is_trainable=False)
    def save_at(step):
        result = checkpoint(model,out/f'update-{step}',predict,save,reload)
        write(out/f'update-{step}'/'receipt.json',result)
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=CONFIG['learning_rate'],weight_decay=CONFIG['weight_decay'])
    with (out/'steps.jsonl').open('x') as stream:
        def log(record):
            stream.write(json.dumps(record,allow_nan=False)+'\n');stream.flush()
        result = train_steps(model,by_id,batches,optimizer,scorer,save_at,log)
    write(out/'result.json',result)
    del model,optimizer;gc.collect()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=['preflight','smoke','full'],default='preflight')
    parser.add_argument('--name',required=True,help='new run directory name inside this harness')
    args = parser.parse_args()
    if not re.fullmatch('[a-z0-9][a-z0-9-]{0,63}',args.name):
        parser.error('invalid run name')
    out = HERE/'test-output'/args.name
    out.mkdir(exist_ok=False)
    torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
    write(out/'config.json',dict(mode=args.mode,configuration=CONFIG,full_training=args.mode=='full'))
    frozen = {}
    def work():
        write(out/'protected-before.json',protected())
        rows,used,empty,calibration = inputs()
        paths = list(HERE.glob('*.py'))+list(HERE.glob('*.md'))
        paths += [PLAN/'test-output'/name for name in ('training-labels.json','calibration.json','training-row-policy.json')]
        paths += [NARROW/'supervised_trial'/name for name in ('train.py','data.py')]
        paths += [NARROW/'verifier_compatibility/verifier.py',PLAN/'PROTOCOL.md',PLAN/'LABEL-CONTRACT.md']
        import gliner2
        paths += list(Path(gliner2.__file__).parent.rglob('*.py'))
        paths += [p for p in (NARROW.parent/'models/gliner2.5-base-v1').rglob('*') if p.is_file()]
        frozen.update({str(p):digest(p) for p in paths})
        write(out/'input-freeze.json',frozen)
        write(out/'environment.json',{p:importlib.metadata.version(p) for p in ('gliner2','torch','peft','transformers','numpy')})
        write(out/'coverage-only.json',empty)
        schedules = {str(n):schedule([r['id'] for r in used],n) for n in CONFIG['seeds']}
        write(out/'schedules.json',schedules)
        results = []
        preflight(out,rows,calibration)
        verify_manifest(frozen)
        if args.mode != 'preflight':
            for number in CONFIG['seeds']:
                folder = out/str(number);folder.mkdir()
                batches = schedules[str(number)][:1] if args.mode=='smoke' else schedules[str(number)]
                results.append(dict(seed=number,**train_one(folder,number,used,batches)))
                verify_manifest(frozen)
        return dict(mode=args.mode,results=results,full_training_completed=args.mode=='full')
    def audit_inputs():
        if frozen:
            verify_manifest(frozen)
        write(out/'inputs-after.json',dict(verified=len(frozen),established=bool(frozen)))
    def audit_protected():
        write(out/'protected-after.json',protected())
    result = guarded_run(work,[('input-integrity',audit_inputs),('protected-integrity',audit_protected)],
        lambda result:write(out/'completion.json',result),
        lambda errors:write(out/'failure.json',dict(errors=errors)))
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
