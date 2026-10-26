"""Test-only dependency injection; all serving implementations remain unchanged."""
import argparse
import contextlib
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from harness import database,POC

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('arm',choices=('baseline','candidate'));p.add_argument('--settings',required=True)
    a=p.parse_args();path,sha=database(a.arm)
    sys.path.insert(0,str(POC))
    with contextlib.redirect_stdout(sys.stderr):
        from parity_v1.serve_discovery import create_discovery_server,RepairService,Service,Store
        store=Store(path,sha)
        try:server=create_discovery_server(RepairService(Service(store,a.settings)))
        except BaseException:store.close();raise
    server.run(transport='stdio')
