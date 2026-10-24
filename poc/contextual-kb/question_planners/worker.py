"""Worker entrypoint: load once, accept questions only, never execute searches."""
import json
import os
from pathlib import Path
import sys


def install_guard(arm):
    root = Path(__file__).resolve().parent.parent
    blocked = [root / name for name in ('authored', 'corpus', 'kbcompiler', 'build', 'planner_cases')]

    def audit(event, args):
        if event == 'sqlite3.connect':
            raise PermissionError('Question planners cannot access SQLite')
        if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
            path = Path(os.fsdecode(args[0])).resolve()
            if any(path == base or base in path.parents for base in blocked):
                raise PermissionError('Question planners cannot access locked data or cases')
        if event == 'socket.connect':
            address = args[1]
            if arm != 'B' or not isinstance(address, tuple) or address[:2] != ('127.0.0.1', 11434):
                raise PermissionError('Only the fixed local model endpoint is permitted')
        if event in {'subprocess.Popen', 'os.system'}:
            raise PermissionError('Question planners cannot launch commands')
    sys.addaudithook(audit)


def main():
    arm = sys.argv[1]
    try:
        if arm == 'A':
            from .syntax import SyntaxPlanner
            planner = SyntaxPlanner()
        elif arm == 'B':
            from .llama import LlamaPlanner
            planner = LlamaPlanner()
        else:
            raise ValueError('Unknown arm')
        install_guard(arm)
        print(json.dumps({'ready': True}), flush=True)
    except Exception as exc:
        print(json.dumps({'startup_error': str(exc)}), flush=True)
        return
    for line in sys.stdin:
        question = json.loads(line)['question']
        plan, trace = planner.plan(question)
        print(json.dumps({'plan': plan.model_dump(), 'trace': trace}), flush=True)


if __name__ == '__main__': main()
