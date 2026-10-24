"""Package the tested v2 instruction and request; does not invoke a model."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from contract import nonempty

def build_messages(request):
    if not nonempty(request):raise ValueError('Request must be a nonempty string')
    return [{'role':'system','content':Path(__file__).with_name('CONTRACT.md').read_text(encoding='utf-8')},
            {'role':'user','content':request}]

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request',required=True)
    args=parser.parse_args()
    try:print(json.dumps(build_messages(args.request),indent=2,ensure_ascii=False))
    except ValueError as exc:parser.error(str(exc))
