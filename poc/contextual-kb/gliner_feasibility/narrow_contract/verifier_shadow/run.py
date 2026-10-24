"""Frozen-model diagnostic runner. No optimizer or output repair path."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
NARROW=HERE.parent


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def authorize(new,adjudicated,review):
    for path in (new,adjudicated,review):
        if not path.resolve().is_relative_to(HERE/'data'):raise ValueError('inputs must be local reviewed development data')
    receipt=json.loads(review.read_text())
    if receipt.get('verdict')!='ready' or receipt.get('independent') is not True:raise ValueError('independent ready review required')
    binding=receipt['bindings']
    if not {str(new.resolve()),str(adjudicated.resolve())}<=set(binding):raise ValueError('review does not bind input files')
    for path,h in binding.items():
        if digest(path)!=h:raise ValueError('review input drift')
    return binding


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--new',type=Path,required=True);parser.add_argument('--adjudicated',type=Path,required=True);parser.add_argument('--review',type=Path,required=True);parser.add_argument('--name',required=True)
    args=parser.parse_args()
    if not re.fullmatch('[a-z0-9][a-z0-9-]{0,63}',args.name):raise ValueError('invalid name')
    bindings=authorize(args.new,args.adjudicated,args.review)
    bindings[str(args.review.resolve())]=digest(args.review)
    bindings.update({str(p):digest(p) for p in HERE.glob('*.py')})
    sys.path.insert(0,str(NARROW/'verifier_evaluation'))
    from runtime import Models,read,write,protect,verify_manifest,guarded_run,calibration_rows
    from shadow import collect,summarize,validate
    out=HERE/'test-output'/args.name;out.mkdir(exist_ok=False)
    write(out/'input-freeze.json',bindings)
    prior_manifests=[NARROW/'verifier_evaluation/test-output'/s for s in ('full-run-final-freeze.json','sealed-preparation-freeze.json')]+[NARROW/'verifier_diagnosis/test-output/final-freeze.json']
    def audits():
        verify_manifest(bindings)
        return dict(protected=protect(),prior={str(p):verify_manifest(read(p)) for p in prior_manifests})
    def work():
        write(out/'before.json',audits())
        panels={'new_development':read(args.new),'legacy_original':calibration_rows(),'legacy_adjudicated':read(args.adjudicated)}
        for rows in panels.values():
            validate(rows)
            if len(rows)!=30:raise ValueError('30 questions per panel required')
        old=panels['legacy_original'];adj=panels['legacy_adjudicated']
        if [(r['id'],r['text']) for r in old]!=[(r['id'],r['text']) for r in adj]:raise ValueError('overlay changed question identity/text/order')
        norm=lambda s:' '.join(s.lower().split())
        oldtexts={norm(r['text']) for r in old}
        training=read(NARROW/'verifier_training_plan/test-output/training-labels.json')
        oldtexts|={norm(r['text']) for r in training}
        newtexts=[norm(r['text']) for r in panels['new_development']]
        if len(set(newtexts))!=30 or set(newtexts)&oldtexts:raise ValueError('new development duplication')
        cache=read(NARROW/'verifier_evaluation/test-output/full-calibration-v1/calibration-outputs.json')
        result={};cost={}
        for seed in (1701,1702):
            key=str(seed);trained=NARROW/f'verifier_harness/test-output/verifier-full-verifier-v1/{seed}/update-124'
            model=Models(seed,trained/'adapter',trained/'receipt.json')
            try:
                cost[key]=dict(cold_seconds=model.cold_seconds);result[key]={}
                expected={r['id']:r['raw'] for r in cache[key]}
                for name,source in panels.items():
                    rows=[dict(r,expected_raw=expected[r['id']]) if name.startswith('legacy') else r for r in source]
                    records=collect(rows,model.extract,model.score)
                    write(out/f'{seed}-{name}-outputs.json',records)
                    result[key][name]=summarize(records)
                    cost[key][name]=dict(extraction_seconds=sum(r['seconds']['extraction'] for r in records),all_span_verifier_seconds=sum(r['seconds']['all_span_verifier'] for r in records),oracle_verifier_seconds=sum(r['seconds']['oracle_verifier'] for r in records),note='single-pass diagnostics, not latency qualification')
            finally:model.close()
        write(out/'scores.json',result);write(out/'cost.json',cost)
        return dict(diagnostic_only=True,seeds=[1701,1702],panels=list(panels),training=False,outputs_modified=False,sealed_evaluation=False)
    def after():write(out/'after.json',audits())
    result=guarded_run(work,[('preservation',after)],lambda r:write(out/'completion.json',r),lambda e:write(out/'failure.json',dict(errors=e)))
    write(out/'freeze.json',{str(p):digest(p) for p in out.iterdir() if p.is_file()})
    print(json.dumps(result))

if __name__=='__main__':main()
