"""Use the already-qualified local Codex transport with a separate selector contract."""
import json,os,signal,subprocess,time,uuid,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parent
sys.path.insert(0,str(POC))
from mcp_v1.planner import planner_command,decode_plan,MODEL,EFFORT

class Selector:
    def __init__(self,directory=None,timeout=180):
        self.directory=Path(directory or HERE/'runtime/selector');self.directory.mkdir(parents=True,exist_ok=True)
        self.timeout=timeout
    def __call__(self,payload):
        job=self.directory/uuid.uuid4().hex;job.mkdir()
        prompt=json.dumps(payload);(job/'input.json').write_text(prompt)
        command=planner_command('codex',HERE/'SELECTOR.md',HERE/'selector.schema.json',job)
        start=time.perf_counter();error=None;process=None
        try:
            with (job/'events.jsonl').open('xb') as output,(job/'stderr.txt').open('xb') as errors:
                process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=output,stderr=errors,start_new_session=True)
                try:process.communicate(prompt.encode(),timeout=self.timeout)
                except BaseException:
                    if process.poll() is None:
                        os.killpg(process.pid,signal.SIGTERM)
                        try:process.wait(timeout=5)
                        except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait()
                    raise
            if process.returncode:raise RuntimeError('Selector process failed; attempt '+job.name)
            if (job/'events.jsonl').stat().st_size>4*1024*1024:raise ValueError('Selector output exceeds limit')
            events=[json.loads(s) for s in (job/'events.jsonl').read_text().splitlines() if s]
            messages=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
            if any(e.get('type')=='item.completed' and e.get('item',{}).get('type') not in {'agent_message','reasoning'} for e in events):raise ValueError('Selector attempted a tool')
            if not events or events[-1].get('type')!='turn.completed' or len(messages)!=1:raise ValueError('Missing single selector response')
            value=decode_plan(messages[0]);(job/'decision.json').write_text(json.dumps(value,indent=2))
            return value
        except BaseException as exc:error=type(exc).__name__+': '+str(exc);raise
        finally:
            (job/'receipt.json').write_text(json.dumps(dict(model=MODEL,effort=EFFORT,seconds=time.perf_counter()-start,error=error,exit_code=None if process is None else process.returncode),indent=2))
