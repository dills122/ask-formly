#!/usr/bin/env python3
"""Run against a disposable copy of our fixture after a real pnpm install."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tests/project-index'))
from pnpm_nx_contract import call,verify
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workspace',required=True);args=p.parse_args()
root=Path(args.workspace).resolve()
if json.loads((root/'package.json').read_text()).get('name')!='ask-formly-pnpm-nx-fixture':p.error('Expected a disposable copy of tests/fixtures/pnpm-nx-formly')
compiler=root/'node_modules/typescript/lib/typescript.js'
if not compiler.exists():p.error('Install fixture dependencies with pnpm first')
(root/'.agents/ask-formly').mkdir(parents=True,exist_ok=True)
export='.agents/ask-formly/nx-project-graph.json'
env={**os.environ,'NX_DAEMON':'false','NX_ISOLATE_PLUGINS':'false','NX_INTERACTIVE':'false','NX_CACHE_PROJECT_GRAPH':'false'}
r=subprocess.run(['pnpm','exec','nx','graph','--file='+export],cwd=root,env=env,capture_output=True,text=True,timeout=120)
if r.returncode:raise RuntimeError(r.stdout+r.stderr)
def scan():
    call(root,'scan','--typescript',str(compiler),'--nx-graph',export,'--project','admin')
    return json.loads((root/'.agents/ask-formly/graph.json').read_text())
result=verify(root,scan())
result['versions']={name:json.loads((root/'node_modules'/name/'package.json').read_text())['version'] for name in ['nx','typescript','@angular/core','@angular/material','@ngx-formly/core','@ngx-formly/material']}
result['versions']['pnpm']=subprocess.check_output(['pnpm','--version'],cwd=root,text=True).strip()
base=root/'tsconfig.base.json';original=base.read_bytes();config=json.loads(original);config['compilerOptions'].pop('paths')
try:
    base.write_text(json.dumps(config,indent=2)+'\n')
    result['pnpm_package_exports']=verify(root,scan())
finally:
    base.write_bytes(original)
    scan()
print(json.dumps(result,indent=2))
