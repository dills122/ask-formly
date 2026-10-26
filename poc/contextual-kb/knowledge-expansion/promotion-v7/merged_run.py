"""Explicitly authorized lookup-only smoke invocation for the merged settings server.

No global configuration or frozen runner is changed. The user must authorize this
run; the CLI flag records that decision rather than deriving consent from time.
"""
import argparse
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def authorized_lookup_command(command):
    if not command or command[-1]!='-':
        raise ValueError('Expected stdin prompt sentinel')
    return command[:-1]+[
        '-c','mcp_servers.formly.enabled_tools=["lookup_formly"]',
        '-c','mcp_servers.formly.tools.lookup_formly.approval_mode="approve"','-']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name',required=True)
    parser.add_argument('--approved-lookups',action='store_true',required=True)
    args=parser.parse_args()
    if Path(args.name).name!=args.name or args.name in ('.','..'):
        raise ValueError('Invalid output name')
    import run
    original=run.caller_command
    run.caller_command=lambda job,seed:authorized_lookup_command(original(job,seed))
    cases=json.loads((HERE/'cases.json').read_text())['cases']
    root=HERE/'test-output'/args.name
    root.mkdir(exist_ok=False)
    for batch,start in enumerate(range(0,len(cases),5),1):
        receipt=run.run_agent(cases[start:start+5],1701,root/f'r1-b{batch}-candidate')
        if receipt['exit_code']!=0 or receipt.get('error'):
            raise RuntimeError('Caller failed; no automatic retry')


if __name__=='__main__':main()
