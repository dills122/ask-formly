"""Pinned POC-only model and dataset adapters. Historical content loads only on request."""
import gc
import json
import sys
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent;NARROW=HERE.parent;ROOT=HERE.parents[4]
sys.path.insert(0,str(NARROW/'supervised_trial'))
from train import load_model, PeftModel, torch
sys.path.insert(0,str(NARROW/'verifier_compatibility'))
from verifier import score, schema as verifier_schema, align
sys.path.insert(0,str(NARROW/'verifier_harness'))
from harness import digest, verify_manifest, state_hashes, guarded_run
sys.path.insert(0,str(HERE))
from decisions import ROLES, tokens, probabilities


def read(path):return json.loads(path.read_text())


def write(path,data):
    with path.open('x') as f:json.dump(data,f,indent=2,allow_nan=False)


def protect():
    previous=NARROW/'verifier_harness/test-output'
    manifests=[ROOT/r['manifest'] for r in read(previous/'preflight-002/protected-after.json')]+[previous/'final-freeze.json']
    result=[]
    for manifest in manifests:
        mapping={}
        for name,h in read(manifest).items():
            p=Path(name)
            if not p.is_absolute():p=ROOT/p if p.parts[0]=='poc' else manifest.parent.parent/p
            mapping[str(p)]=h
        result.append(dict(manifest=str(manifest.relative_to(ROOT)),checked=verify_manifest(mapping),changed=[]))
    return result


def calibration_rows():
    rows=read(NARROW/'verifier_training_plan/test-output/calibration.json');result=[]
    for row in rows:
        gold=[];probes=[]
        for o in row['occurrences']:
            role=o.get('source_kind') if o['targets'][0] else None
            if role:gold.append([o['start'],o['end'],role])
            probes.append(dict(start=o['start'],end=o['end'],expected_role=role,family=o.get('negative_family','gold')))
        result.append(dict(id=row['id'],text=row['text'],gold=gold,probes=probes))
    if len(result)!=30:raise ValueError('calibration count drift')
    return result


class Models:
    def __init__(self,number,adapter,checkpoint_receipt):
        torch.set_num_threads(4);torch.use_deterministic_algorithms(True)
        started=time.perf_counter()
        baseline=NARROW/f'role_boundary_adaptation/test-output/after-{number}/epoch-6/adapter'
        self.extractor=PeftModel.from_pretrained(load_model(),str(baseline),is_trainable=False);self.extractor.eval()
        self.verifier=PeftModel.from_pretrained(load_model(),str(adapter),is_trainable=False);self.verifier.eval()
        if state_hashes(self.verifier)!=read(checkpoint_receipt)['state_hashes']:raise ValueError('verifier checkpoint state mismatch')
        self.schema=self.extractor.create_schema().entities(read(NARROW/'pilot/labels.json'))
        self.cold_seconds=time.perf_counter()-started
    def extract(self,text):
        with torch.inference_mode():
            return self.extractor.extract(text,self.schema,threshold=.5,overlap_policy='flat',include_spans=True,include_confidence=True)
    def score(self,text,offsets):
        if not offsets:return {}
        with torch.inference_mode():z,aligned,unsupported,_=score(self.verifier,text,offsets)
        if not torch.isfinite(z).all():raise ValueError('nonfinite verifier logits')
        result={s:None for s in unsupported}
        for s,p in zip(aligned,z.sigmoid().tolist()):
            if not probabilities(p):raise ValueError('nonfinite verifier probabilities')
            result[s]=p
        if set(result)!=set(offsets):raise ValueError('supplied score coverage differs')
        return result
    def close(self):
        del self.extractor,self.verifier;gc.collect()


def history_rows(number):
    """Only invoked after a qualified/frozen calibration decision; old exposed diagnostics."""
    trial=NARROW/'native_attribute_distillation_trial'
    paths={
        'historic_fresh':trial/'fresh.json', 'retention':NARROW/'native_attribute_retention/fresh.json',
        'contrast':NARROW/'native_attribute_contrast/fresh.json','attribute':NARROW/'native_attribute_training/fresh.json',
        'span':NARROW/'span_role_feasibility/fresh.json','cross':NARROW/'cross_role_resolution/fresh.json',
        'boundary':NARROW/'role_boundary_adaptation/fresh.json','vocab':NARROW/'vocabulary_adaptation/fresh.json',
        'target':NARROW/'fresh_flat/questions.json','challenge':NARROW/'challenge_adaptation/challenge.json',
        'olddev':NARROW/'supervised_trial/dev.json'}
    probe_roots={'historic_fresh':trial,'attribute':NARROW/'native_attribute_training','contrast':NARROW/'native_attribute_contrast','retention':NARROW/'native_attribute_retention'}
    result={};count=0
    for group,path in paths.items():
        source=read(path);oldname='fresh' if group=='historic_fresh' else group
        baseline=read(trial/f'test-output/{number}/{oldname}-baseline.json')
        prior=read(trial/f'test-output/{number}/{oldname}-before.json')
        if len(source)!=len(baseline) or len(source)!=len(prior):raise ValueError('historical coverage mismatch')
        candidates=read(probe_roots[group]/'probe_candidates.json')['candidates'] if group in probe_roots else []
        rows=[]
        for r,b,p in zip(source,baseline,prior):
            if r['question_id']!=b['id'] or r['question_id']!=p['id']:raise ValueError('historical identity mismatch')
            gold=[[m['start'],m['end'],m['kind']] for m in r['mentions']]
            prior_tokens=tokens(r['question'],p['resolved']['output']);raw_tokens=tokens(r['question'],b['output'])
            repairs=[]
            for a,e,k in gold:
                original={v for v in raw_tokens if v[:2]==(a,e)};after={v for v in prior_tokens if v[:2]==(a,e)}
                if len(original)>1 and after=={(a,e,k)}:repairs.append([a,e,k])
            probes=[dict(start=x['start'],end=x['end'],expected_role=None if x['expected_role']=='no_entity' else x['expected_role'],family=x.get('invalid_family') or 'gold') for x in candidates if x['question_id']==r['question_id']]
            count+=len(probes)
            rows.append(dict(id=r['question_id'],text=r['question'],gold=gold,probes=probes,expected_raw=b['output'],prior_correct_repairs=repairs))
        result[group]=rows
    if sum(map(len,result.values()))!=416 or count!=622:raise ValueError('historical totals mismatch')
    return result


def qualify_sealed(rows):
    """Native token transport only; no encoder forward or optimizer, no text in receipt."""
    model=load_model();schemas,_=model._build_schema_dicts_and_metadata([verifier_schema(model)])
    total=0;unsupported_count=0
    try:
        for row in rows:
            offsets=[(p['start'],p['end']) for p in row['probes']]
            if not offsets:continue
            batch=model.processor.collate_fn_inference([(row['text'],schemas[0])],architecture='boundary',error_policy='raise')
            _,unsupported,_=align(row['text'],offsets,batch.start_mappings[0],batch.end_mappings[0])
            expected={(p['start'],p['end']) for p in row['probes'] if p['family']=='unsupported'}
            if set(unsupported)!=expected:raise ValueError('fresh transport/family mismatch: '+row['id'])
            total+=len(offsets);unsupported_count+=len(unsupported)
    finally:
        del model;gc.collect()
    if unsupported_count!=4:raise ValueError('fresh unsupported total mismatch')
    return dict(questions=len(rows),probe_count=total,unsupported=unsupported_count,no_encoder_forward=True)
