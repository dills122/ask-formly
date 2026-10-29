"""Explicit runtime choice: model-free by default, model-backed only by opt-in."""
import argparse
import contextlib
import hashlib
from importlib import metadata
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
POC=HERE.parent
sys.path.insert(0,str(POC))
from mcp_runtime.identity import build_identity


def verify_files(root,pins):
    root=Path(root).resolve();errors=[]
    for name,expected in pins.items():
        path=(root/name).resolve()
        if Path(name).is_absolute() or not path.is_relative_to(root):
            errors.append('outside POC: '+name)
        elif not path.is_file():
            errors.append('missing: '+name)
        elif hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            errors.append('hash mismatch: '+name)
    return errors


def model_free_preflight(root=POC,manifest=None):
    """Read-only pins/package checks. No worker process, models or provider calls."""
    if manifest is None:
        manifest=json.loads((HERE/'model-free.json').read_text())
    errors=verify_files(root,manifest['files']);versions={}
    for name,expected in manifest['server_packages'].items():
        try:
            actual=metadata.version(name);versions[name]=actual
            if actual!=expected:errors.append(f'{name} version {actual}; expected {expected}')
        except metadata.PackageNotFoundError:
            errors.append('missing package: '+name)
    return dict(ok=not errors,mode='model-free',build_identity=build_identity(manifest),files_checked=len(manifest['files']),
                server_packages=versions,server_inference='none',
                caller_responsibility='Plan, assess relevance, select evidence and answer.',
                errors=errors)


def start_model_free(args):
    # Only import the selected implementation; its modules remain frozen.
    sys.path.insert(0,str(POC))
    with contextlib.redirect_stdout(sys.stderr):
        from parity_v1.serve_discovery import create_discovery_server,RepairService,Service,Store
        manifest=json.loads((HERE/'model-free.json').read_text())
        store=Store(POC/'build/knowledge.sqlite',manifest['files']['build/knowledge.sqlite'])
        try:
            service=RepairService(Service(store,args.runtime_dir/'project-settings.sqlite'))
            server=create_discovery_server(service,args.audit_dir)
        except BaseException:
            store.close();raise
    server.run(transport='stdio')


def run_model_backed(args):
    sys.path.insert(0,str(POC))
    from mcp_foundation import launcher as legacy
    forwarded=[args.command,'--seed',str(args.seed or 1701),'--runtime-dir',str(args.runtime_dir)]
    if args.audit_dir is not None:forwarded+=['--audit-dir',str(args.audit_dir)]
    # Preserve the existing implementation, preflight, failures and fallbacks.
    return legacy.main(forwarded)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('serve','doctor'))
    parser.add_argument('--mode',choices=('model-free','model-backed'),default='model-free',
                        help='No automatic switching or cross-mode fallback.')
    parser.add_argument('--seed',type=int,choices=(1701,1702),
                        help='Model-backed frozen adapter seed only; default1701.')
    parser.add_argument('--runtime-dir',type=Path)
    parser.add_argument('--audit-dir',type=Path,help='Optional lookup packet audit directory.')
    args=parser.parse_args(argv)
    if args.mode=='model-free' and args.seed is not None:
        parser.error('--seed applies only to --mode model-backed')
    if args.runtime_dir is None:args.runtime_dir=HERE/'test-output'/args.mode
    if args.mode=='model-backed':
        print('Model-backed mode: local GLiNER/embeddings and hosted Codex planner/selector; doctor does not invoke inference.',file=sys.stderr)
        return run_model_backed(args)
    try:
        report=model_free_preflight()
    except (OSError,ValueError,KeyError) as exc:
        print('Model-free startup check failed: '+str(exc),file=sys.stderr);return 2
    if args.command=='doctor':
        print(json.dumps(report,indent=2));return 0 if report['ok'] else 2
    if not report['ok']:
        print('Model-free startup check failed:\n'+'\n'.join(report['errors']),file=sys.stderr);return 2
    start_model_free(args)
    return 0


if __name__=='__main__':raise SystemExit(main())
