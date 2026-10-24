"""Stable local entry point for the accepted, unchanged Formly POC components."""
import argparse
import contextlib
import hashlib
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
POC = HERE.parent
MANIFEST = HERE/'foundation.json'


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def verify_files(root, pins):
    root = root.resolve()
    errors = []
    for name, expected in pins.items():
        path = (root/name).resolve()
        if Path(name).is_absolute() or not path.is_relative_to(root):
            errors.append(f'outside POC: {name}')
        elif not path.is_file():
            errors.append(f'missing: {name}')
        elif sha256(path) != expected:
            errors.append(f'hash mismatch: {name}')
    return errors


def preflight():
    """Read-only local prerequisites; no login, provider request or model loading."""
    manifest = json.loads(MANIFEST.read_text())
    errors = verify_files(POC, manifest['files'])
    versions = {}
    for name, expected in manifest['server_packages'].items():
        try:
            actual = importlib.metadata.version(name)
            versions[name] = actual
            if actual != expected:
                errors.append(f'{name} version {actual}; expected {expected}; use mcp_v1/.venv/bin/python')
        except importlib.metadata.PackageNotFoundError:
            errors.append(f'missing package {name}; use mcp_v1/.venv/bin/python')
    worker = POC/'gliner_feasibility/env/.venv/bin/python'
    worker_versions = {}
    if not worker.is_file() or not os.access(worker, os.X_OK):
        errors.append('missing GLiNER environment: gliner_feasibility/env/.venv/bin/python')
    else:
        names = list(manifest['worker_packages'])
        script = 'import importlib.metadata as m,json;print(json.dumps({n:m.version(n) for n in '+repr(names)+'}))'
        try:
            result = subprocess.run([str(worker),'-B','-c',script],capture_output=True,text=True,timeout=15,check=True)
            worker_versions = json.loads(result.stdout)
            if worker_versions != manifest['worker_packages']:
                errors.append('GLiNER environment versions differ from foundation.json; restore the qualified environment')
        except (OSError,subprocess.SubprocessError,ValueError):
            errors.append('cannot inspect GLiNER environment; restore the qualified environment')
    codex = shutil.which('codex')
    if codex is None:
        errors.append('codex CLI not found on PATH; expose the authenticated Codex CLI to the MCP client')
    return dict(ok=not errors,foundation=manifest['id'],files_checked=len(manifest['files']),
                server_packages=versions,worker_packages=worker_versions,codex=codex,
                provider_access='not checked: login, network, model access and quota require a real lookup',errors=errors)


def start(args):
    # Preserve the native MCP stdout stream; dependency diagnostics belong on stderr.
    with contextlib.redirect_stdout(sys.stderr):
        sys.path.insert(0,str(POC))
        from wording_candidate_v1.serve import make_service
        from mcp_v1.server import create_server
        service = make_service(seed=args.seed,runtime_dir=args.runtime_dir)
        server = create_server(service,args.audit_dir)
    server.run(transport='stdio')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=('serve','doctor'))
    parser.add_argument('--seed',type=int,choices=(1701,1702),default=1701)
    parser.add_argument('--runtime-dir',type=Path,default=HERE/'runtime')
    parser.add_argument('--audit-dir',type=Path)
    args = parser.parse_args(argv)
    try:
        report = preflight()
    except (OSError,ValueError,KeyError) as exc:
        print(f'Formly startup check failed: {exc}. See mcp_foundation/README.md.',file=sys.stderr)
        return 2
    if args.mode == 'doctor':
        print(json.dumps(report,indent=2))
        return 0 if report['ok'] else 2
    if not report['ok']:
        print('Formly startup check failed:\n'+'\n'.join(report['errors'])+'\nSee mcp_foundation/README.md.',file=sys.stderr)
        return 2
    start(args)
    return 0

if __name__=='__main__':
    raise SystemExit(main())
