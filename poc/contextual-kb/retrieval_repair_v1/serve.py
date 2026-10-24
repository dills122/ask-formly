"""Separate candidate launcher; original mcp_v1 remains untouched."""
import argparse,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parent
sys.path.insert(0,str(POC));sys.path.insert(0,str(POC/'mcp_v1'))
from mcp_v1.server import create_server
from mcp_v1.service import LookupService
from mcp_v1.planner import CodexPlanner
from retrieval_repair_v1.integration import Backend
from retrieval_repair_v1.selector import Selector

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed',type=int,choices=(1701,1702),default=1701)
    parser.add_argument('--audit-dir',type=Path)
    parser.add_argument('--runtime-dir',type=Path,default=HERE/'runtime')
    args=parser.parse_args()
    service=LookupService(CodexPlanner(args.runtime_dir/'planner'),lambda:Backend(args.seed,Selector(args.runtime_dir/'selector')))
    create_server(service,args.audit_dir).run(transport='stdio')
if __name__=='__main__':main()
