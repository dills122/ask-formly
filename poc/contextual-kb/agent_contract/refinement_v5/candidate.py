"""v5 ledger instructions with the frozen v3 structural/advisory transport."""
from pathlib import Path
import sys

# This package is wholly inside the same contextual-kb POC.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agent_contract.refinement_v3.candidate import (
    build_plan, nonempty, optional_hints, parse_output, validate,
)


def build_messages(request):
    """Select v5 instructions; preserve the user's request verbatim."""
    if not nonempty(request):
        raise ValueError('Request must be a nonempty string')
    return [
        {'role': 'system', 'content': Path(__file__).with_name('CONTRACT.md').read_text()},
        {'role': 'user', 'content': request},
    ]
