"""qualification3 fixed interpretation policy with unchanged same-POC structural transport."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent_contract.refinement_v3.candidate import (
    build_plan, nonempty, optional_hints, parse_output, validate,
)

def build_messages(request):
    """Select qualification3 instructions and preserve request data verbatim."""
    if not nonempty(request):
        raise ValueError('Request must be a nonempty string')
    return [
        {'role':'system','content':Path(__file__).with_name('CONTRACT.md').read_text()},
        {'role':'user','content':request},
    ]
