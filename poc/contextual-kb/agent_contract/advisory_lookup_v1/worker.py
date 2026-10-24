"""Private JSON-lines worker; runs only in the existing local GLiNER environment."""
import argparse,contextlib,json,sys
from runtime import FrozenExtractor,parameter_hashes

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--seed',type=int,choices=(1701,1702),required=True);args=parser.parse_args()
    try:
        with contextlib.redirect_stdout(sys.stderr):extractor=FrozenExtractor(args.seed)
    except Exception as exc:
        print(json.dumps(dict(ready=False,error_type=type(exc).__name__,error=str(exc))),flush=True)
        return
    print(json.dumps(dict(ready=True,parameters=extractor.before,load_seconds=extractor.load_seconds)),flush=True)
    for line in sys.stdin:
        request=json.loads(line)
        try:
            with contextlib.redirect_stdout(sys.stderr):
                if request['op']=='extract':result=extractor(request['text'])
                elif request['op']=='verify':result=dict(parameters=parameter_hashes(extractor.model),checks=extractor.verify_unchanged())
                else:raise ValueError('Unknown worker operation')
            response=dict(id=request['id'],result=result)
        except Exception as exc:response=dict(id=request['id'],error_type=type(exc).__name__,error=type(exc).__name__+': '+str(exc))
        print(json.dumps(response,allow_nan=False),flush=True)

if __name__=='__main__':main()
