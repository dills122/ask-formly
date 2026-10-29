"""Explicit read-only baseline server for candidate comparisons; no installed changes."""
import argparse
from pathlib import Path
import sys

POC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(POC))
sys.path.insert(0, str(POC / 'model_free_v1'))
from parity_v1.serve_discovery import create_discovery_server, RepairService, Service, Store

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--settings', type=Path, required=True)
    args = parser.parse_args()
    create_discovery_server(RepairService(Service(Store(args.database, args.sha256), args.settings))).run(transport='stdio')
