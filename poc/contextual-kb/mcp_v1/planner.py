"""One-shot, tool-disabled Codex generation using the frozen foundation contract."""
import json
import os
import signal
import subprocess
import time
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
POC = HERE.parent
CONTRACT = POC / 'agent_contract/qualification_v3/CONTRACT.md'
MODEL = 'gpt-6-astra'
EFFORT = 'medium'

class PlannerError(ValueError):
    pass

def decode_plan(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise PlannerError('Duplicate planner JSON key')
            result[key] = value
        return result
    def invalid(_):
        raise PlannerError('Non-finite planner JSON')
    try:
        value = json.loads(text, object_pairs_hook=pairs, parse_constant=invalid)
    except (ValueError, TypeError) as exc:
        raise PlannerError('Planner did not return strict JSON') from exc
    if not isinstance(value, dict):
        raise PlannerError('Planner must return an object')
    return value

def planner_command(executable, contract, schema, directory):
    return [executable, 'exec', '--ignore-user-config', '--ephemeral',
            '--skip-git-repo-check', '--sandbox', 'read-only', '-C', str(directory),
            '-m', MODEL, '-c', f'model_reasoning_effort="{EFFORT}"',
            '-c', 'features.shell_tool=false', '-c', 'features.multi_agent=false',
            '-c', 'features.apps=false', '-c', 'web_search="disabled"',
            '-c', 'project_doc_max_bytes=0',
            '-c', 'model_instructions_file='+json.dumps(str(contract)),
            '--output-schema', str(schema), '--json', '-']

class CodexPlanner:
    def __init__(self, directory, executable='codex', timeout=180):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.executable = executable
        self.timeout = timeout

    def __call__(self, request):
        job = self.directory / uuid.uuid4().hex
        job.mkdir()
        (job/'request.json').write_text(json.dumps(request))
        command = planner_command(self.executable, CONTRACT, HERE/'plan.schema.json', job)
        started = time.perf_counter()
        with (job/'events.jsonl').open('xb') as output, (job/'stderr.txt').open('xb') as errors:
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=output,
                                       stderr=errors, start_new_session=True)
            try:
                process.communicate(request.encode(), timeout=self.timeout)
            except BaseException:
                os.killpg(process.pid, signal.SIGTERM)
                try: process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                raise
        elapsed = time.perf_counter()-started
        receipt = {'model':MODEL, 'reasoning_effort':EFFORT, 'seconds':elapsed,
                   'exit_code':process.returncode, 'attempt_id':job.name,
                   'contract_path':str(CONTRACT), 'sampling_seed':None}
        (job/'receipt.json').write_text(json.dumps(receipt, indent=2))
        if process.returncode:
            raise PlannerError('Planner process failed; attempt '+job.name)
        if (job/'events.jsonl').stat().st_size > 4*1024*1024:
            raise PlannerError('Planner output exceeds limit')
        events = [json.loads(line) for line in (job/'events.jsonl').read_text().splitlines() if line]
        messages = [e['item']['text'] for e in events if e.get('type')=='item.completed'
                    and e.get('item',{}).get('type')=='agent_message']
        allowed = {'agent_message','reasoning'}
        if any(e.get('type')=='item.completed' and e.get('item',{}).get('type') not in allowed for e in events):
            raise PlannerError('Planner attempted tools instead of pure planning')
        if not events or events[-1].get('type')!='turn.completed' or len(messages)!=1:
            raise PlannerError('Planner did not deliver one completed response')
        return decode_plan(messages[0]), receipt
