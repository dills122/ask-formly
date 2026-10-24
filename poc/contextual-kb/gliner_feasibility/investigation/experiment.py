"""Explicit development ablations; no question planning or semantic repair."""
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
from time import perf_counter

HERE = Path(__file__).resolve().parent
PROBE = HERE.parent


def validate_native(question, value):
    """Include record fields as well as entity/relation spans in fidelity checks."""
    if isinstance(value, list):
        return sum(validate_native(question, x) for x in value)
    if not isinstance(value, dict):
        return 0
    if 'text' in value:
        start, end = value.get('start'), value.get('end')
        if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(question):
            raise ValueError('Invalid span offsets')
        if question[start:end] != value['text']:
            raise ValueError('Native span text changed')
        return 1
    return sum(validate_native(question, x) for x in value.values())


def observe_native(question, extract):
    result = {}
    start = perf_counter()
    try:
        result['native'] = extract()
        result['validated_span_occurrences'] = validate_native(question, result['native'])
    except Exception as exc:
        result['error'] = {'type': type(exc).__name__, 'message': str(exc)}
    result['seconds'] = perf_counter()-start
    return result


def schema_for(model, spec):
    # Installed GLiNER2 2.1.0 public Schema API; see official tutorial/README.
    schema = model.create_schema()
    if 'entities' in spec:
        schema.entities(spec['entities'])
    if 'relations' in spec:
        schema.relations(spec['relations'])
    if 'interpretation' in spec:
        schema.classification('interpretation', spec['interpretation'])
    if 'structure' in spec:
        record = spec['structure']
        builder = schema.structure(record['name'])
        for name, description in record['fields'].items():
            builder.field(name, dtype='list', description=description)
    return schema


def run(phase):
    if phase not in {'phase1', 'phase2'}:
        raise ValueError('Only explicit development phases are permitted')
    sys.path.insert(0, str(PROBE))
    from probe import load_development, check_access
    from run import verify_protected
    verify_protected()
    cases = load_development()
    variants = json.loads((HERE / f'{phase}-variants.json').read_text())
    controls = json.loads((HERE / 'controls.json').read_text()) if phase == 'phase1' else []
    # Capture inputs and code before opening output or loading model.
    files = [HERE/'experiment.py', HERE/f'{phase}-variants.json', HERE/'controls.json',
             HERE/'PLAN.md', PROBE/'schema.json', PROBE/'env/uv.lock']
    files += [PROBE/n for n in json.loads((PROBE/'evidence/probe-freeze.json').read_text())
              if n.startswith('models/')]
    manifest = {str(p.relative_to(PROBE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    with (HERE/f'evidence/{phase}-freeze.json').open('x') as out:
        json.dump(manifest,out,indent=2)
    with (HERE/f'evidence/{phase}-raw.jsonl').open('x') as out:
        os.environ.update({'HF_HOME':str(PROBE/'.cache/hf'),'HF_HUB_OFFLINE':'1',
                           'TRANSFORMERS_OFFLINE':'1','TOKENIZERS_PARALLELISM':'false'})
        started = perf_counter()
        import torch
        from gliner2 import AutoExtractor
        torch.set_num_threads(4)
        torch.manual_seed(1701)
        model = AutoExtractor.from_pretrained(str(PROBE/'models/gliner2.5-base-v1'),
                                              local_files_only=True,map_location='cpu')
        model.eval()
        load_seconds = perf_counter()-started
        sys.addaudithook(check_access)
        def alarm(signum, frame):
            raise TimeoutError('Diagnostic 60s Python alarm, not hard native-code deadline')
        signal.signal(signal.SIGALRM,alarm)
        jobs = [(v,c) for v in variants for c in cases]
        jobs += [({'id':c['id'],'schema':c['schema'],'threshold':.5},c) for c in controls]
        for variant,case in jobs:
            schema = schema_for(model,variant['schema'])
            signal.alarm(60)
            try:
                with torch.inference_mode():
                    row = observe_native(case['question'],lambda:model.extract(
                        case['question'],schema,threshold=variant['threshold'],
                        include_confidence=True,include_spans=True))
            finally:
                signal.alarm(0)
            row.update({'variant':variant['id'],'case_id':case['id'],'question':case['question']})
            out.write(json.dumps(row,ensure_ascii=False)+'\n');out.flush()
            print(variant['id'],case['id'],round(row['seconds'],3),row.get('error','ok'),flush=True)
            if row.get('error',{}).get('type') == 'TimeoutError':
                raise TimeoutError('Stopped bounded development phase')
        (HERE/f'evidence/{phase}-runtime.json').write_text(json.dumps(
            {'load_seconds':load_seconds,'samples':len(jobs),'device':'cpu','threads':4,
             'model_revision':'54785d51df8d86a0d8f2eb212fec15871aad2c4d',
             'timing':'Unpaired development ablations, no warmup; not a benchmark'},indent=2)+'\n')


if __name__ == '__main__':
    run(sys.argv[1])
