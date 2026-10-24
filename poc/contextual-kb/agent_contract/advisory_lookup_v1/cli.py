"""Run advisory lookup for a caller-generated qualification_v3 foundation plan."""
import argparse,contextlib,json,os,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parents[1]
sys.path.insert(0,str(POC))
from agent_contract.qualification_v3.candidate import build_plan
from agent_contract.retrieval_integration_v1.bridge import readonly
from agent_contract.advisory_lookup_v1.lookup import AdvisoryLookup
from agent_contract.advisory_lookup_v1.runtime import digest,IntegrityError
from agent_contract.advisory_lookup_v1.transport import ProcessExtractor
from kbcompiler.question_pilot import PilotIndex

def read_input(path):
    def pairs(items):
        obj={}
        for k,v in items:
            if k in obj:raise ValueError('Duplicate JSON key: '+k)
            obj[k]=v
        return obj
    def reject(value):raise ValueError('Invalid JSON constant: '+value)
    value=json.loads(Path(path).read_text(),object_pairs_hook=pairs,parse_constant=reject)
    if not isinstance(value,dict) or set(value)!={'request','question_plan'}:raise ValueError('Input needs exactly request and question_plan')
    build_plan(value['request'],value['question_plan'])
    return value['request'],value['question_plan']

def write_output(path,value):
    with Path(path).open('x') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

def run(request,core,seed=1701,without_gliner=False):
    build_plan(request,core)
    os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(HERE/'test-output/embed-cache'),HF_HUB_OFFLINE='1')
    dbpath=POC/'build/knowledge.sqlite';before=digest(dbpath);loaded=[]
    def factory():
        extractor=ProcessExtractor(seed);loaded.append(extractor);return extractor
    try:
        with readonly(dbpath) as db:
            started=time.perf_counter();index=PilotIndex(db);setup=time.perf_counter()-started
            service=AdvisoryLookup(index,None if without_gliner else factory)
            result=service.lookup(request,core)
            checks=[]
            for extractor in loaded:
                try:checks.append(extractor.verify_unchanged())
                except IntegrityError:raise
                except Exception as exc:
                    message='extractor_verification: '+type(exc).__name__+': '+str(exc)
                    checks.append(dict(seed=seed,parameters_unchanged=None,error=message))
                    result['advisory']['diagnostics'].append(message)
                    result['advisory']['status']='degraded'
            result['runtime']=dict(extractor_seed=None if without_gliner else seed,index_setup_seconds=setup,model_checks=checks)
    finally:
        for extractor in loaded:extractor.close()
        if digest(dbpath)!=before:raise RuntimeError('Knowledge DB changed')
    result['runtime']['db_unchanged']=True
    return result

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True,type=Path,help='JSON containing request and question_plan')
    parser.add_argument('--output',type=Path,help='New output file; default stdout')
    parser.add_argument('--seed',type=int,choices=(1701,1702),default=1701,help='Frozen adapter;1701 default is administrative, not a measured winner')
    parser.add_argument('--without-gliner',action='store_true',help='Foundation-only diagnostic control')
    args=parser.parse_args(argv)
    try:
        request,core=read_input(args.input)
        if args.output and args.output.exists():raise FileExistsError('Output already exists')
        with contextlib.redirect_stdout(sys.stderr):result=run(request,core,args.seed,args.without_gliner)
        if args.output:write_output(args.output,result)
        else:print(json.dumps(result,indent=2,allow_nan=False))
    except (ValueError,OSError) as exc:parser.error(str(exc))

if __name__=='__main__':main()
