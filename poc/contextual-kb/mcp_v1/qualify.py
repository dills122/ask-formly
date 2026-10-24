"""Run each fresh calling-agent batch once, with a real stdio MCP configured."""
import json,os,signal,subprocess,time
from pathlib import Path
from planner import MODEL,EFFORT
HERE=Path(__file__).resolve().parent

def command(job,seed):
    args=['codex','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check',
          '--sandbox','read-only','-C',str(job),'-m',MODEL,
          '-c',f'model_reasoning_effort="{EFFORT}"',
          '-c','features.shell_tool=false','-c','features.multi_agent=false',
          '-c','features.apps=false','-c','project_doc_max_bytes=0','-c','web_search="disabled"',
          '-c','model_instructions_file='+json.dumps(str(HERE/'CALLER.md')),
          '-c','mcp_servers.formly.command='+json.dumps(str(HERE/'.venv/bin/python')),
          '-c','mcp_servers.formly.args='+json.dumps(['-B',str(HERE/'server.py'),'--seed',str(seed),
              '--audit-dir',str(job/'audit'),'--planner-runs',str(job/'planner')]),
          '-c','mcp_servers.formly.tool_timeout_sec=600',
          '-c','mcp_servers.formly.startup_timeout_sec=60',
          '--output-schema',str(HERE/'answer.schema.json'),'--json','-']
    return args

def main():
    root=HERE/'test-output/qualification';root.mkdir()
    cases=json.loads((HERE/'cases.json').read_text())
    prompt=json.dumps([{'id':c['id'],'request':c['request']} for c in cases])
    for repeat,seed in enumerate([1701,1702,1701],1):
        job=root/f'round-{repeat}';job.mkdir()
        (job/'prompt.json').write_text(prompt)
        cmd=command(job,seed)
        (job/'command.json').write_text(json.dumps(cmd,indent=2))
        started=time.perf_counter()
        with (job/'events.jsonl').open('xb') as out,(job/'stderr.txt').open('xb') as err:
            process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=out,stderr=err,start_new_session=True)
            try:process.communicate(prompt.encode(),timeout=1200)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid,signal.SIGTERM)
                try:process.wait(timeout=10)
                except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait()
        (job/'receipt.json').write_text(json.dumps({'round':repeat,'seed':seed,'exit_code':process.returncode,
              'seconds':time.perf_counter()-started,'model':MODEL,'reasoning_effort':EFFORT},indent=2))
        print('round',repeat,'exit',process.returncode,flush=True)
if __name__=='__main__':main()
