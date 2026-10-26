"""Controlled optional-grace reproduction using the real Codex MCP client."""
import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from mcp_v1.planner import planner_command


def probe(name, required, delay, fail=False, wait_catalog=False, discovery=False, identity=False, bound=False):
    job=HERE/'test-output'/name
    job.mkdir(exist_ok=False)
    instructions=HERE/('STARTUP-CALLER-BOUND.md' if bound else 'STARTUP-CALLER-IDENTITY.md' if identity else 'STARTUP-CALLER-DISCOVERY.md' if discovery else 'STARTUP-CALLER.md')
    command=planner_command('codex',instructions,HERE/'startup.schema.json',job)
    options=['-c','mcp_servers.formly.command='+json.dumps(sys.executable),
             '-c','mcp_servers.formly.args='+json.dumps(['-B',str(HERE/'startup_fixture.py'),'--delay',str(delay),'--log',str(job/'server.jsonl')]+(['--fail'] if fail else [])),
             '-c','mcp_servers.formly.startup_timeout_sec=60','-c','mcp_servers.formly.tool_timeout_sec=60']
    if required:options+=['-c','mcp_servers.formly.required=true']
    if wait_catalog:options+=['-c','mcp_optional_startup_grace_ms=0']
    command[-1:-1]=options
    (job/'command.json').write_text(json.dumps(command,indent=2))
    start=time.perf_counter()
    with (job/'events.jsonl').open('xb') as out,(job/'stderr.txt').open('xb') as err:
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=out,stderr=err,start_new_session=True)
        try:process.communicate(b'Run the availability probe.',timeout=180)
        except BaseException:
            os.killpg(process.pid,signal.SIGTERM)
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait()
            raise
    events=[json.loads(x) for x in (job/'events.jsonl').read_text().splitlines()]
    calls=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='mcp_tool_call']
    messages=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
    report=dict(required=required,wait_catalog=wait_catalog,discovery=discovery,identity=identity,bound=bound,delay=delay,injected_failure=fail,exit_code=process.returncode,seconds=time.perf_counter()-start,calls=calls,messages=messages)
    (job/'receipt.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('--required',action='store_true');p.add_argument('--delay',type=float,default=3);p.add_argument('--fail',action='store_true');p.add_argument('--wait-catalog',action='store_true');p.add_argument('--discovery',action='store_true');p.add_argument('--identity',action='store_true');p.add_argument('--bound',action='store_true');a=p.parse_args()
    probe(a.name,a.required,a.delay,a.fail,a.wait_catalog,a.discovery,a.identity,a.bound)
