"""Final three declared development configurations; previous runner remains frozen."""
import hashlib
import json
import os
import signal
import sys
from time import perf_counter
from experiment import HERE, PROBE, observe_native, schema_for


def targeted_schema(model, spec):
    if 'intent' in spec:
        return (model.create_schema().entities(spec['entities'])
                .classification('intent',spec['intent'],multi_label=True,cls_threshold=.3))
    if 'structure' not in spec:
        return schema_for(model,spec)
    record=spec['structure']
    schema=model.create_schema()
    builder=schema.structure(record['name'],mode=record['mode'],anchor=record['anchor'])
    for name,description in record['fields'].items():
        anchor = name == record['anchor']
        builder.field(name,dtype='str' if anchor else 'list',description=description,
                      cardinality='required_one' if anchor else 'zero_or_more')
    return schema


def run():
    sys.path.insert(0,str(PROBE))
    from probe import load_development,check_access
    from run import verify_protected
    verify_protected()
    cases=load_development()
    variants=json.loads((HERE/'phase2-variants.json').read_text())
    files=[HERE/n for n in ['phase2.py','experiment.py','phase2-variants.json','PHASE1-ANALYSIS.md']]
    files += [PROBE/n for n in json.loads((PROBE/'evidence/probe-freeze.json').read_text()) if n.startswith('models/')]
    with (HERE/'evidence/phase2-freeze.json').open('x') as f:
        json.dump({str(p.relative_to(PROBE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},f,indent=2)
    with (HERE/'evidence/phase2-raw.jsonl').open('x') as out:
        os.environ.update({'HF_HOME':str(PROBE/'.cache/hf'),'HF_HUB_OFFLINE':'1',
                           'TRANSFORMERS_OFFLINE':'1','TOKENIZERS_PARALLELISM':'false'})
        start=perf_counter()
        import torch
        from gliner2 import AutoExtractor
        torch.set_num_threads(4);torch.manual_seed(1701)
        model=AutoExtractor.from_pretrained(str(PROBE/'models/gliner2.5-base-v1'),local_files_only=True,map_location='cpu')
        model.eval()
        load_seconds=perf_counter()-start
        sys.addaudithook(check_access)
        def alarm(signum,frame):
            raise TimeoutError('60s diagnostic Python alarm, not hard native deadline')
        signal.signal(signal.SIGALRM,alarm)
        for variant in variants:
            schema=targeted_schema(model,variant['schema'])
            for case in cases:
                signal.alarm(60)
                try:
                    with torch.inference_mode():
                        row=observe_native(case['question'],lambda:model.extract(
                            case['question'],schema,threshold=variant['threshold'],
                            overlap_policy=variant.get('overlap_policy'),
                            include_confidence=True,include_spans=True))
                finally:
                    signal.alarm(0)
                row.update({'variant':variant['id'],'case_id':case['id'],'question':case['question']})
                out.write(json.dumps(row,ensure_ascii=False)+'\n');out.flush()
                print(variant['id'],case['id'],round(row['seconds'],3),row.get('error','ok'),flush=True)
                if row.get('error',{}).get('type')=='TimeoutError':
                    raise TimeoutError('Stopping diagnostic phase')
        (HERE/'evidence/phase2-runtime.json').write_text(json.dumps({'load_seconds':load_seconds,
            'samples':36,'device':'cpu','threads':4,'timing':'Development only, no warmup'},indent=2)+'\n')


if __name__=='__main__':
    run()
