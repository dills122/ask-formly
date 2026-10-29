"""Test adapter: launch the chosen source tree with an explicitly pinned read-only DB."""
import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--poc', type=Path, required=True)
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--settings', type=Path, required=True)
    args = parser.parse_args()
    poc = args.poc.resolve()
    sys.path[:0] = [str(poc), str(poc / 'model_free_v1')]
    from parity_v1.serve_discovery import create_discovery_server
    from model_free_repair_v1.feedback import RepairService
    from model_free_v1.candidate import Service, Store
    if args.settings.resolve() == args.database.resolve():
        parser.error('Settings and knowledge DB must differ')
    store = Store(args.database, args.sha256)
    create_discovery_server(RepairService(Service(store, args.settings))).run(transport='stdio')


if __name__ == '__main__':
    main()
