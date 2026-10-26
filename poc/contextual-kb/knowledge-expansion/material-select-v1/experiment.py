"""Separate test MCP composition; accepted components are imported unchanged."""
import argparse, contextlib, copy, json, os, signal, subprocess, sys, time
from contextlib import ExitStack
from pathlib import Path
from candidate import HERE, POC, preserved, assert_digest, digest
from delivery import verify_calls
sys.path.insert(0,str(POC/'mcp_v1'))
from mcp_v1.backend import Backend as BaseBackend
from retrieval_repair_v1.integration import Backend as SelectedBackend
from retrieval_repair_v1.selector import Selector
from mcp_v1.planner import MODEL, EFFORT
from condition_candidate_v2.planner import CodexPlanner
from mcp_v1.service import LookupService
from mcp_v1.server import create_server
from wording_candidate_v1.candidate import NormalizingPlanner
from agent_contract.advisory_lookup_v1.lookup import AdvisoryLookup
from agent_contract.retrieval_integration_v1.bridge import readonly
from kbcompiler.question_pilot import PilotIndex


from candidate import checked_database
from mcp_foundation.capitalization import CapitalizingPlanner
from mcp_foundation.transport import connection_options
from mcp_v1.planner import planner_command


class ExperimentBackend(SelectedBackend):
    """Only initialization varies: explicit checked DB rather than installed path.

    All lookup, extraction, selection, citation, integrity and closure methods are
    inherited verbatim from the accepted backend classes.
    """
    def __init__(self, arm, seed, runtime):
        self.dbpath,self.dbhash=checked_database(arm)
        self.seed=seed; self.stack=ExitStack(); self.extractors=[]; self.closed=False
        self.selector=Selector(runtime/'selector')
        os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(POC/'agent_contract/advisory_lookup_v1/test-output/embed-cache'),HF_HUB_OFFLINE='1')
        try:
            self.db=self.stack.enter_context(readonly(self.dbpath))
            start=time.perf_counter(); self.index=PilotIndex(self.db)
            self.setup_seconds=time.perf_counter()-start
            self.lookup_service=AdvisoryLookup(self.index,self._extractor)
        except BaseException:
            self.stack.close(); raise


class ReplayPlanner:
    def __init__(self, records): self.records=copy.deepcopy(records)
    def __call__(self, request):
        if request not in self.records: raise ValueError('No exact saved request for replay')
        row=self.records[request]
        return copy.deepcopy(row['core']),dict(row['generation'],replay=True)


def serve(args):
    from mcp_foundation.launcher import preflight
    report=preflight()
    if not report['ok']: raise ValueError(report['errors'])
    preserved(); checked_database(args.arm)
    runtime=Path(args.runtime).resolve()
    if not runtime.is_relative_to(HERE/'test-output'): raise ValueError('Runtime must remain inside experiment test-output')
    runtime.mkdir(parents=True,exist_ok=True)
    with contextlib.redirect_stdout(sys.stderr):
        planner=CodexPlanner(runtime/'planner') if not args.replay else ReplayPlanner(json.loads(Path(args.replay).read_text()))
        service=LookupService(CapitalizingPlanner(planner),lambda:ExperimentBackend(args.arm,args.seed,runtime))
        server=create_server(service,runtime/'audit')
    server.run(transport='stdio')


def parse_agent_output(events, expected):
    if not events or events[-1].get('type')!='turn.completed': raise ValueError('Agent turn incomplete')
    messages=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
    if len(messages)!=1: raise ValueError('Expected one final agent response')
    value=json.loads(messages[0]); rows=value['answers']
    if len(rows)!=len(expected) or {r['id'] for r in rows}!=set(expected): raise ValueError('Missing/duplicate/unexpected answer IDs')
    return value


def caller_command(job,arm,seed):
    if arm not in ('baseline','candidate'): raise ValueError('Unknown arm')
    command=planner_command('codex',POC/'mcp_foundation/CALLER.md',HERE/'answer.schema.json',job)
    command[-1:-1]=['-c','mcp_servers.formly.command='+json.dumps(sys.executable),
                   '-c','mcp_servers.formly.args='+json.dumps(['-B',str(HERE/'experiment.py'),'serve','--arm',arm,'--seed',str(seed),'--runtime',str(job/'mcp')])]+connection_options()+['-c','mcp_servers.formly.enabled_tools=["lookup_formly"]',
                   '-c','mcp_servers.formly.tools.lookup_formly.approval_mode="approve"']
    return command


def run_agent(cases, arm, seed, job):
    job=Path(job).absolute()
    if job!=job.resolve() or not job.is_relative_to(HERE/'test-output'):
        raise ValueError('Output must stay in experiment test-output without aliases')
    job.mkdir(parents=True,exist_ok=False)
    prompt=json.dumps([{'id':c['id'],'request':c['request']} for c in cases])
    (job/'prompt.json').write_text(prompt)
    command=caller_command(job,arm,seed)
    (job/'command.json').write_text(json.dumps(command,indent=2));start=time.perf_counter();error=None
    with (job/'events.jsonl').open('xb') as out,(job/'stderr.txt').open('xb') as err:
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=out,stderr=err,start_new_session=True)
        try: process.communicate(prompt.encode(),timeout=1800)
        except BaseException as exc:
            error=type(exc).__name__+': '+str(exc);os.killpg(process.pid,signal.SIGTERM)
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait()
    receipt=dict(arm=arm,seed=seed,model=MODEL,effort=EFFORT,seconds=time.perf_counter()-start,exit_code=process.returncode,error=error)
    try:
        if error or process.returncode:raise RuntimeError('Calling agent failed')
        events=[json.loads(line) for line in (job/'events.jsonl').read_text().splitlines() if line]
        value=parse_agent_output(events,[c['id'] for c in cases]);(job/'answers.json').write_text(json.dumps(value,indent=2))
        receipt['mcp_calls']=verify_calls(events,[c['request'] for c in cases])
    except Exception as exc: receipt['error']=type(exc).__name__+': '+str(exc)
    (job/'receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt),flush=True)
    return receipt


def main():
    parser=argparse.ArgumentParser();sub=parser.add_subparsers(dest='mode',required=True)
    s=sub.add_parser('serve');s.add_argument('--arm',choices=['baseline','candidate'],required=True);s.add_argument('--seed',type=int,choices=[1701,1702],default=1701);s.add_argument('--runtime',required=True);s.add_argument('--replay')
    r=sub.add_parser('agents');r.add_argument('--cases',required=True);r.add_argument('--name',required=True);r.add_argument('--repeats',type=int,default=1);r.add_argument('--batch-size',type=int,default=4)
    args=parser.parse_args()
    if args.mode=='serve':return serve(args)
    cases=json.loads(Path(args.cases).read_text())['cases']
    if Path(args.name).name!=args.name:raise ValueError('Invalid experiment name')
    root=HERE/'test-output'/args.name;root.mkdir(exist_ok=False)
    for repeat in range(1,args.repeats+1):
        seed=1702 if repeat==2 else 1701
        for batch,start in enumerate(range(0,len(cases),args.batch_size),1):
            arms=['baseline','candidate'] if (repeat+batch)%2==0 else ['candidate','baseline']
            for arm in arms:
                receipt=run_agent(cases[start:start+args.batch_size],arm,seed,root/f'r{repeat}-b{batch}-{arm}')
                if receipt['exit_code']!=0: raise RuntimeError('Provider/agent process failed; stop batch')
    preserved()

if __name__=='__main__':main()
