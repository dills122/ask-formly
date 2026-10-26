"""Opt-in service: new spelling adapter, unchanged checked DB/backend/server."""
import argparse
import contextlib
import json
import os
import sys
import time
from pathlib import Path
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'custom-types-v1'
sys.path.insert(0,str(PRIOR))


def make_service(seed, runtime, planner=None, backend_factory=None):
    from experiment import ExperimentBackend, CodexPlanner, LookupService
    from capitalization import CapitalizingPlanner
    return LookupService(CapitalizingPlanner(planner if planner is not None else CodexPlanner(runtime/'planner')),
                         backend_factory if backend_factory is not None else lambda:ExperimentBackend('candidate',seed,runtime))


def serve(runtime,seed,replay=None):
    runtime=Path(runtime).resolve()
    if not runtime.is_relative_to(HERE/'test-output'):
        raise ValueError('Runtime must remain in the isolated candidate')
    runtime.mkdir(parents=True,exist_ok=False)
    def milestone(event):
        with (runtime/'startup.jsonl').open('a') as log:
            log.write(json.dumps(dict(event=event,time=time.time()))+'\n')
    milestone('process_started')
    # Dedicated native/Python stderr survives even if the client omits logs.
    with (runtime/'stderr.txt').open('w') as errors:
        os.dup2(errors.fileno(),2)
        try:
            from experiment import preserved, checked_database, ReplayPlanner, create_server
            from mcp_foundation.launcher import preflight
            milestone('imports_completed')
            report=preflight()
            if not report['ok']:raise ValueError(report['errors'])
            preserved();checked_database('candidate');milestone('preflight_passed')
            with contextlib.redirect_stdout(sys.stderr):
                planner=ReplayPlanner(json.loads(Path(replay).read_text())) if replay else None
                service=make_service(seed,runtime,planner)
                server=create_server(service,runtime/'audit')
            milestone('server_ready')
            server.run(transport='stdio')
        except BaseException:
            milestone('server_failed')
            raise
        finally:milestone('process_stopped')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--runtime',required=True);parser.add_argument('--seed',type=int,choices=(1701,1702),default=1701);parser.add_argument('--replay');args=parser.parse_args()
    serve(args.runtime,args.seed,args.replay)
