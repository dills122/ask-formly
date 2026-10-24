"""Persistent isolated worker with a supervisor-enforced request deadline."""
import json
import os
import selectors
import select
import subprocess
import sys
from pathlib import Path
from time import monotonic
from .contract import Plan, failed, validate_question


class PlannerProcess:
    def __init__(self, arm=None, *, command=None, deadline=10.0):
        self.deadline = deadline
        self.pending = b''
        root = Path(__file__).resolve().parent.parent
        if command is None:
            if arm not in {'A', 'B'}:
                raise ValueError('Select arm A or B')
            command = [sys.executable, '-u', '-m', 'question_planners.worker', arm]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TOKENIZERS_PARALLELISM='false')
        # Model/runtime assets belong in the isolated environment, never data/DB.
        env['NLTK_DATA'] = str(root / 'planner_env' / '.cache' / 'nltk')
        self.process = subprocess.Popen(command, cwd=root, env=env, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.process.stdout, selectors.EVENT_READ)
        os.set_blocking(self.process.stdin.fileno(), False)
        start = monotonic()
        try:
            ready = self._read(start + 60)
            if ready != {'ready': True}:
                raise RuntimeError(f'Worker initialization failed: {ready}')
        except BaseException:
            self.close()
            raise
        self.startup_seconds = monotonic() - start

    def _read(self, end):
        while b'\n' not in self.pending:
            remaining = end - monotonic()
            if remaining <= 0 or not self.selector.select(remaining):
                raise TimeoutError('Worker exceeded deadline')
            chunk = os.read(self.process.stdout.fileno(), 65536)
            if not chunk:
                raise RuntimeError('Worker exited without a complete response')
            self.pending += chunk
            if len(self.pending) > 1_000_000:
                raise ValueError('Worker response exceeds 1 MB')
        line, self.pending = self.pending.split(b'\n', 1)
        return json.loads(line)

    def query(self, question):
        start = monotonic()
        trace = {}
        try:
            validate_question(question)
        except ValueError as exc:
            return {'plan': failed(question, 'invalid_input', str(exc)).model_dump(),
                    'trace': trace, 'seconds': monotonic() - start}
        try:
            if self.process.poll() is not None:
                raise RuntimeError('Worker is stopped; no automatic restart/retry')
            message = (json.dumps({'question': question}) + '\n').encode()
            offset = 0
            while offset < len(message):
                remaining = start + self.deadline - monotonic()
                if remaining <= 0 or not select.select([], [self.process.stdin], [], remaining)[1]:
                    raise TimeoutError('Sending input exceeded request deadline')
                try:
                    offset += os.write(self.process.stdin.fileno(), message[offset:])
                except BlockingIOError:
                    continue
            payload = self._read(start + self.deadline)
            if not isinstance(payload, dict) or set(payload) != {'plan', 'trace'}:
                raise ValueError('Invalid worker envelope')
            plan = Plan.model_validate(payload['plan'])
            if plan.question != question:
                raise ValueError('Worker changed original question')
            trace = payload['trace']
            if monotonic() - start > self.deadline:
                raise TimeoutError('Validation exceeded request deadline')
        except TimeoutError as exc:
            self.close()
            plan = failed(question, 'timeout', str(exc))
        except (ValueError, TypeError, KeyError) as exc:
            self.close()
            plan = failed(question, 'invalid_output', str(exc))
        except (OSError, RuntimeError) as exc:
            self.close()
            plan = failed(question, 'backend_error', str(exc))
        return {'plan': plan.model_dump(), 'trace': trace, 'seconds': monotonic() - start}

    def close(self):
        if self.process.poll() is None:
            self.process.kill()
        self.process.wait(timeout=2)
        self.selector.close()
        for stream in (self.process.stdin, self.process.stdout):
            if stream and not stream.closed:
                stream.close()

    def __enter__(self): return self
    def __exit__(self, *args): self.close()
