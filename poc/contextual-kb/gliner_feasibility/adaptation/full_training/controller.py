"""Parent wall-clock enforcement; worker cannot spawn a subprocess."""
import json
import os
from pathlib import Path
import signal
import subprocess
import time


def bounded_process(command, destination, seconds):
    start=time.monotonic()
    result={'status':'started','seconds_limit':seconds,'command':command}
    with (destination/'worker.log').open('x') as log:
        process=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        try:
            result['returncode']=process.wait(timeout=seconds)
            result['status']='completed' if result['returncode']==0 else 'failed'
        except subprocess.TimeoutExpired:
            os.killpg(process.pid,signal.SIGKILL);process.wait()
            result.update(status='timeout',returncode=process.returncode)
        except BaseException:
            os.killpg(process.pid,signal.SIGKILL);process.wait()
            result.update(status='interrupted',returncode=process.returncode)
            raise
        finally:
            result['seconds']=time.monotonic()-start
            with (destination/'controller.json').open('x') as receipt:
                json.dump(result,receipt,indent=2)
    return result


if __name__=='__main__':
    import argparse,sys
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['preflight','train'])
    parser.add_argument('--seed',type=int,choices=[1701,2903],default=1701)
    parser.add_argument('--run-id',required=True)
    args=parser.parse_args()
    if not args.run_id or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-_' for c in args.run_id):
        parser.error('run-id must be a simple lowercase identifier')
    here=Path(__file__).resolve().parent
    destination=here/'test-output'/args.run_id;destination.mkdir(exist_ok=False)
    command=[sys.executable,str(here/'worker.py'),args.mode,'--seed',str(args.seed),'--output',str(destination)]
    result=bounded_process(command,destination,1800 if args.mode=='preflight' else 14400)
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['status']=='completed' else 1)
