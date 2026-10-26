"""Fixed 30-case, three-repeat qualification using the unchanged isolated MCP caller."""
import argparse
import json
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
BATCH = HERE.parent/'extensions-v1'


def execute(cases, root, run_agent):
    if len(cases)!=30 or len({c['id'] for c in cases})!=30:
        raise ValueError('Expected thirty distinct frozen cases')
    root.mkdir(exist_ok=False)
    for repeat, seed in enumerate((1701,1702,1701),1):
        for batch,start in enumerate(range(0,len(cases),5),1):
            receipt=run_agent(cases[start:start+5],'candidate',seed,root/f'r{repeat}-b{batch}-candidate')
            if receipt['exit_code']!=0:
                raise RuntimeError('Calling process failed; stop without retry and retain fixed denominators')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--name',required=True);args=parser.parse_args()
    if Path(args.name).name!=args.name or args.name in ('.','..'):raise ValueError('Invalid output name')
    sys.path.insert(0,str(BATCH))
    from experiment import run_agent,preserved
    preserved()
    cases=json.loads((HERE/'cases.json').read_text())['cases']
    execute(cases,BATCH/'test-output'/args.name,run_agent)
    preserved()

if __name__=='__main__':main()
