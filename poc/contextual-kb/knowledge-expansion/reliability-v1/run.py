"""Fixed no-retry real-caller regression for the isolated reliability candidate."""
import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'custom-types-v1'
sys.path.insert(0,str(PRIOR))
from experiment import MODEL,EFFORT,parse_agent_output,preserved
from delivery import verify_calls
from mcp_v1.planner import planner_command
from transport import connection_options


def caller_command(job,seed):
    command=planner_command('codex',HERE/'CALLER.md',PRIOR/'answer.schema.json',job)
    command[-1:-1]=['-c','mcp_servers.formly.command='+json.dumps(sys.executable),
                   '-c','mcp_servers.formly.args='+json.dumps(['-B',str(HERE/'server.py'),'--seed',str(seed),'--runtime',str(job/'mcp')])]+connection_options()
    return command


def run_agent(cases,seed,job):
    job=Path(job).resolve()
    if not job.is_relative_to(HERE/'test-output'):raise ValueError('Output outside candidate')
    job.mkdir(parents=True,exist_ok=False)
    prompt=json.dumps([dict(id=c['id'],request=c['request']) for c in cases])
    (job/'prompt.json').write_text(prompt)
    command=caller_command(job,seed)
    (job/'command.json').write_text(json.dumps(command,indent=2))
    error=None;start=time.perf_counter()
    with (job/'events.jsonl').open('xb') as out,(job/'stderr.txt').open('xb') as err:
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=out,stderr=err,start_new_session=True)
        try:process.communicate(prompt.encode(),timeout=1800)
        except BaseException as exc:
            error=type(exc).__name__+': '+str(exc);os.killpg(process.pid,signal.SIGTERM)
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait()
    receipt=dict(arm='candidate',seed=seed,model=MODEL,effort=EFFORT,seconds=time.perf_counter()-start,exit_code=process.returncode,error=error)
    try:
        if error or process.returncode:raise RuntimeError('Calling agent/startup failed; no retry')
        events=[json.loads(line) for line in (job/'events.jsonl').read_text().splitlines()]
        value=parse_agent_output(events,[c['id'] for c in cases]);(job/'answers.json').write_text(json.dumps(value,indent=2))
        receipt['mcp_calls']=verify_calls(events,[c['request'] for c in cases])
    except Exception as exc:receipt['error']=type(exc).__name__+': '+str(exc)
    (job/'receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt),flush=True)
    return receipt


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cases',required=True);p.add_argument('--name',required=True);p.add_argument('--repeats',type=int,default=3);p.add_argument('--batch-size',type=int,default=5);a=p.parse_args()
    if Path(a.name).name!=a.name:raise ValueError('Invalid output name')
    cases=json.loads(Path(a.cases).read_text())['cases'];root=HERE/'test-output'/a.name;root.mkdir(exist_ok=False)
    for repeat in range(1,a.repeats+1):
        seed=1702 if repeat==2 else 1701
        for batch,start in enumerate(range(0,len(cases),a.batch_size),1):
            receipt=run_agent(cases[start:start+a.batch_size],seed,root/f'r{repeat}-b{batch}-candidate')
            if receipt['exit_code']!=0:raise RuntimeError('Startup/provider process failed; retain missing expected cases')
    preserved()
