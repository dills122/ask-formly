"""Functional integration verification with both immutable native models."""
import gc,json,os,sys,time
from contextlib import contextmanager
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parents[1]
sys.path.insert(0,str(POC))
from agent_contract.advisory_lookup_v1.lookup import AdvisoryLookup
from agent_contract.advisory_lookup_v1.runtime import digest
from agent_contract.advisory_lookup_v1.transport import ProcessExtractor
from agent_contract.retrieval_integration_v1.bridge import readonly
from kbcompiler.question_pilot import PilotIndex

def read(path):return json.loads(Path(path).read_text())
def save(path,value):
    with Path(path).open('x') as f:json.dump(value,f,indent=2,allow_nan=False)
def verify(path):
    for filename,h in read(path).items():
        if digest(filename)!=h:raise ValueError('Frozen input changed: '+filename)

def compare(a,b):
    return (a['plan']['question_plan']==b['plan']['question_plan'] and
            a['plan']['search_requests']==b['plan']['search_requests'] and
            a['retrieval']['queries']==b['retrieval']['queries'] and
            a['retrieval']['ids']==b['retrieval']['ids'] and a['facts']==b['facts'])

@contextmanager
def model_session(index,seed,out):
    loaded=[]
    def factory():
        extractor=ProcessExtractor(seed);loaded.append(extractor)
        save(out/f'{seed}-parameters-before.json',extractor.before)
        return extractor
    try:yield AdvisoryLookup(index,factory),loaded
    finally:
        for extractor in loaded:extractor.close()

def main():
    for name in ('design','generation','run-ready'):verify(HERE/f'test-output/{name}-freeze.json')
    out=HERE/'test-output/live-native';out.mkdir(exist_ok=False)
    save(out/'first-save.json',dict(run_freeze=digest(HERE/'test-output/run-ready-freeze.json'),started_epoch=time.time()))
    records=read(HERE/'data/records.json')
    if len(records)!=48 or len({r['id'] for r in records})!=48:raise ValueError('Input coverage')
    os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(HERE/'test-output/embed-cache'),HF_HUB_OFFLINE='1')
    dbpath=POC/'build/knowledge.sqlite';before=digest(dbpath);baseline={};summaries={}
    with readonly(dbpath) as db:
        started=time.perf_counter();index=PilotIndex(db)
        save(out/'setup.json',dict(seconds=time.perf_counter()-started,db_hash=before,facts=len(index.ids)))
        service=AdvisoryLookup(index)
        with (out/'foundation.jsonl').open('x') as f:
            for row in records:
                result=service.lookup(row['request'],row['output']);baseline[row['id']]=result
                f.write(json.dumps(dict(id=row['id'],origin=row['origin'],result=result),allow_nan=False)+'\n');f.flush()
        for seed in (1701,1702):
            with model_session(index,seed,out) as (service,loaded):
                parity=[];hints=0;calls=0;diagnostics=[];extraction_seconds=0.0;query_seconds=0.0
                with (out/f'{seed}.jsonl').open('x') as f:
                    for row in records:
                        result=service.lookup(row['request'],row['output'])
                        parity.append(dict(id=row['id'],unchanged=compare(baseline[row['id']],result)))
                        hints+=len(result['plan']['role_hints']);calls+=len(result['extractions']);extraction_seconds+=result['extraction_seconds'];query_seconds+=result['retrieval']['seconds']
                        if result['advisory']['diagnostics']:diagnostics.append(dict(id=row['id'],messages=result['advisory']['diagnostics']))
                        if any(h['usable_as_filter'] is not False for h in result['plan']['role_hints']):raise AssertionError('Nonadvisory hint')
                        f.write(json.dumps(dict(id=row['id'],origin=row['origin'],result=result),allow_nan=False)+'\n');f.flush()
                checks=loaded[0].verify_unchanged() if loaded else {'parameters_unchanged':False,'error':'No native model loaded'}
                if loaded:save(out/f'{seed}-parameters-after.json',loaded[0].after)
                summaries[str(seed)]=dict(records=len(records),parity=parity,all_parity=all(r['unchanged'] for r in parity),extraction_calls=calls,hints=hints,diagnostics=diagnostics,extraction_seconds=extraction_seconds,retrieval_seconds=query_seconds,model=checks)
                save(out/f'{seed}-summary.json',summaries[str(seed)])
            del service
            loaded.clear();gc.collect()
        if digest(dbpath)!=before:raise AssertionError('DB changed')
    for name in ('design','generation','run-ready'):verify(HERE/f'test-output/{name}-freeze.json')
    passed=all(s['all_parity'] and s['hints']>0 and s['extraction_calls']==70 and s['model']['parameters_unchanged'] for s in summaries.values())
    save(out/'completion.json',dict(complete=True,passed=passed,db_unchanged=True,records=48,seeds=[1701,1702]))
    save(HERE/'test-output/live-native-freeze.json',{str(p):digest(p) for p in out.iterdir() if p.is_file()})
    print(json.dumps(summaries,indent=2))
    if not passed:raise SystemExit('Functional integration failed; inspect retained evidence')

if __name__=='__main__':main()
