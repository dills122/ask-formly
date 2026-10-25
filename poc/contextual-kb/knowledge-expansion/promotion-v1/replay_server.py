"""Test-only injection of saved planning output into the promoted composition."""
import sys,json,argparse
from pathlib import Path
POC=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(POC));sys.path.insert(0,str(POC/'mcp_v1'))
from mcp_foundation.service import make_service
from mcp_foundation.launcher import preflight
from mcp_v1.server import create_server
p=argparse.ArgumentParser();p.add_argument('--seed',type=int);p.add_argument('--runtime');p.add_argument('--replay');a=p.parse_args()
report=preflight()
if not report['ok']:raise ValueError(report['errors'])
records=json.loads(Path(a.replay).read_text())
def planner(request):
 row=records[request];return row['core'],row['generation']
r=Path(a.runtime);r.mkdir(parents=True,exist_ok=False)
create_server(make_service(a.seed,r,planner=planner),r/'audit').run(transport='stdio')
