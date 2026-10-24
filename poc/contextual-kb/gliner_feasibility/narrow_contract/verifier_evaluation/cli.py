"""Explicit stages: prepare -> train launch -> calibrate -> evaluate. Smoke is isolated."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from runtime import HERE,NARROW,ROOT,read,write,digest,verify_manifest,protect,Models,calibration_rows,history_rows,guarded_run,qualify_sealed
from decisions import assess,select_thresholds,qualification
from pipeline import collect,timing,validate_fresh
from stages import evaluation_ready,review_receipt

OUT=HERE/'test-output'


def name(value):
    if not re.fullmatch('[a-z0-9][a-z0-9-]{0,63}',value):raise ValueError('invalid run name')
    return value


def freeze_files(folder):
    return {str(p):digest(p) for p in sorted(folder.rglob('*')) if p.is_file() and p.name!='freeze.json'}


def code_binding():
    files=list(HERE.glob('*.py'))+list((NARROW/'verifier_harness').glob('*.py'))
    files += [NARROW/'verifier_training_plan'/p for p in ('PROTOCOL.md','LABEL-CONTRACT.md','test-output/training-labels.json','test-output/calibration.json')]
    files += [NARROW/'verifier_compatibility/verifier.py',NARROW/'pilot/labels.json']
    return {str(p):digest(p) for p in files}


def preparation(which):
    folder=OUT/name(which);verify_manifest(read(folder/'freeze.json'))
    spec=read(folder/'preparation.json');verify_manifest(spec['bindings']);verify_manifest({spec['fresh_path']:spec['fresh_sha256'],spec['review_path']:spec['review_sha256']});review_receipt(read(Path(spec['review_path'])),spec['fresh_sha256'])
    return spec


def training_reference(which):
    launch=OUT/name(which);verify_manifest(read(launch/'freeze.json'));record=read(launch/'launch.json')
    spec=preparation(record['preparation'])
    if record['preparation_sha256']!=digest(OUT/record['preparation']/'preparation.json'):raise ValueError('preparation binding drift')
    train=NARROW/'verifier_harness/test-output'/record['training_run'];done=read(train/'completion.json')
    if done.get('mode')!='full' or not done.get('full_training_completed'):raise ValueError('requires completed full training')
    verify_manifest(read(train/'input-freeze.json'))
    if {r['seed'] for r in done['results']}!={1701,1702} or any(r['updates']!=124 or r['exposures']!=992 or r['changed_frozen_state'] for r in done['results']):raise ValueError('training budget/state differs')
    verify_manifest(read(launch/'trained-files.json'))
    return train,spec,record


def calibrate(out,train,spec,mode,launch_name=None):
    rows=calibration_rows();by_seed={};cold={}
    for seed in (1701,1702):
        step=1 if mode=='smoke' else 124
        model=Models(seed,train/str(seed)/f'update-{step}/adapter',train/str(seed)/f'update-{step}/receipt.json')
        cold[str(seed)]=model.cold_seconds
        try:by_seed[str(seed)]=collect(rows,model.extract,model.score)
        finally:model.close()
    write(out/'calibration-outputs.json',by_seed)
    decision=select_thresholds(by_seed,split='calibration')
    bindings=code_binding()
    bindings.update(freeze_files(train))
    if launch_name:bindings[str(OUT/launch_name/'launch.json')]=digest(OUT/launch_name/'launch.json')
    write(out/'decision.json',dict(mode='smoke' if mode=='smoke' else 'calibration',bindings=bindings,launch=launch_name,cold_load_seconds=cold,**decision))
    return dict(selected=decision['selected'],diagnostic_only=decision['diagnostic_only'],mode=mode)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['prepare','train','calibrate','evaluate','smoke'])
    parser.add_argument('--name',required=True);parser.add_argument('--from-run');parser.add_argument('--fresh',type=Path)
    args=parser.parse_args();out=OUT/name(args.name);out.mkdir(exist_ok=False)
    initial=code_binding();write(out/'source-freeze.json',initial)
    def work():
        write(out/'protected-before.json',protect())
        if args.stage=='prepare':
            if args.fresh is None:raise ValueError('independent sealed fresh file required')
            fresh=args.fresh.resolve()
            if not fresh.is_relative_to(HERE/'sealed') or not fresh.is_file():raise ValueError('fresh must be independently prepared under verifier_evaluation/sealed')
            review_path=fresh.with_suffix('.review.json');fresh_hash=digest(fresh)
            review_receipt(read(review_path),fresh_hash)
            # Isolated qualification process may validate sealed annotations; training
            # and threshold-selection stages never receive these rows.
            sealed=read(fresh);validate_fresh(sealed)
            development=read(NARROW/'verifier_training_plan/test-output/training-labels.json')+read(NARROW/'verifier_training_plan/test-output/calibration.json')
            norm=lambda text:' '.join(text.lower().split())
            if {norm(r['text']) for r in sealed}&{norm(r['text']) for r in development}:raise ValueError('fresh split leakage')
            transport=qualify_sealed(sealed)
            write(out/'preparation.json',dict(bindings=initial,fresh_path=str(fresh),fresh_sha256=fresh_hash,review_path=str(review_path),review_sha256=digest(review_path),transport=transport))
            return dict(prepared=True,sealed_validation_only=True,no_model_predictions=True)
        if args.stage=='train':
            if not args.from_run:raise ValueError('preparation required')
            preparation(args.from_run)
            target='verifier-'+name(args.name)
            write(out/'launch.json',dict(preparation=args.from_run,preparation_sha256=digest(OUT/args.from_run/'preparation.json'),training_run=target))
            subprocess.run([sys.executable,'-B',str(NARROW/'verifier_harness/run.py'),'--mode','full','--name',target],check=True)
            write(out/'trained-files.json',freeze_files(NARROW/'verifier_harness/test-output'/target))
            return dict(training_run=target)
        if args.stage=='smoke':
            train=NARROW/'verifier_harness/test-output/smoke-001'
            if read(train/'completion.json')['mode']!='smoke':raise ValueError('smoke checkpoint mismatch')
            return calibrate(out,train,None,'smoke')
        if args.stage=='calibrate':
            if not args.from_run:raise ValueError('training launch required')
            train,spec,record=training_reference(args.from_run)
            return calibrate(out,train,spec,'calibration',args.from_run)
        if not args.from_run:raise ValueError('frozen calibration run required')
        cal=OUT/name(args.from_run);verify_manifest(read(cal/'freeze.json'));decision=read(cal/'decision.json')
        verify_manifest(decision['bindings'])
        def load_evaluation():
            train,spec,_=training_reference(decision['launch'])
            fresh=read(Path(spec['fresh_path']));validate_fresh(fresh)
            training_text={r['text'] for r in read(NARROW/'verifier_training_plan/test-output/training-labels.json')+read(NARROW/'verifier_training_plan/test-output/calibration.json')}
            if {' '.join(r['text'].lower().split()) for r in fresh}&{' '.join(t.lower().split()) for t in training_text}:raise ValueError('fresh split leakage')
            return train,fresh
        # No historical or fresh contents loaded until this gate succeeds.
        train,fresh=evaluation_ready(decision,decision['bindings'],load_evaluation)
        models={};all_groups={};cold={};timed_rows=None
        try:
            for seed in (1701,1702):
                key=str(seed);m=Models(seed,train/key/'update-124/adapter',train/key/'update-124/receipt.json');models[key]=m;cold[key]=m.cold_seconds
                groups=history_rows(seed);groups['fresh']=fresh
                if timed_rows is None:timed_rows=[dict(id=g+'/'+r['id'],text=r['text']) for g,rows in groups.items() for r in rows]
                summaries={}
                for group,rows in groups.items():
                    records=collect(rows,m.extract,m.score)
                    write(out/f'{seed}-{group}-outputs.json',records)
                    summaries[group]=assess(records,decision['selected'])
                all_groups[key]=summaries
            measured=timing(timed_rows,{s:m.extract for s,m in models.items()},{s:m.score for s,m in models.items()},decision['selected'])
        finally:
            for m in models.values():m.close()
        gate=qualification(all_groups,measured['budget_p95'])
        if decision['diagnostic_only']:gate['passed']=False;gate['issues'].append('calibration_diagnostic_only')
        write(out/'scores.json',all_groups);write(out/'timing.json',dict(cold_load_seconds=cold,**measured));write(out/'decision.json',gate)
        return gate
    def audit_sources():verify_manifest(initial)
    def audit_protected():write(out/'protected-after.json',protect())
    result=guarded_run(work,[('source-integrity',audit_sources),('protected-integrity',audit_protected)],lambda result:write(out/'completion.json',dict(stage=args.stage,result=result)),lambda errors:write(out/'failure.json',dict(errors=errors)))
    write(out/'freeze.json',freeze_files(out))
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
