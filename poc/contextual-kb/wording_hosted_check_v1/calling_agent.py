"""Separate real calling-agent smoke; never overwrites prior qualification."""
import json,os,signal,subprocess,time,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parent
sys.path.insert(0,str(POC));sys.path.insert(0,str(POC/'mcp_v1'))
from mcp_v1.qualify import command as original_command

def main():
    root=HERE/'test-output/native';root.mkdir()
    cases=[c for c in json.loads((POC/'mcp_v1/cases.json').read_text()) if c['id'] in {'M03','M05','M07'}]
    fresh=json.loads((POC/'retrieval_repair_v1/test-output/fresh/F01.json').read_text())
    cases.insert(0,{'id':'F01','request':fresh['request']})
    prompt=json.dumps([{'id':c['id'],'request':c['request']} for c in cases])
    for seed in (1701,1702):
        job=root/str(seed);job.mkdir();cmd=original_command(job,seed)
        for i,value in enumerate(cmd):
            if value.startswith('mcp_servers.formly.args='):
                cmd[i]='mcp_servers.formly.args='+json.dumps(['-B',str(POC/'wording_candidate_v1/serve.py'),'--seed',str(seed),'--audit-dir',str(job/'audit'),'--runtime-dir',str(job/'runtime')])
        (job/'prompt.json').write_text(prompt);(job/'command.json').write_text(json.dumps(cmd,indent=2))
        start=time.perf_counter()
        with (job/'events.jsonl').open('xb') as out,(job/'stderr.txt').open('xb') as err:
            process=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=out,stderr=err,start_new_session=True)
            try:process.communicate(prompt.encode(),timeout=600)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid,signal.SIGTERM)
                try:process.wait(timeout=10)
                except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait()
        (job/'receipt.json').write_text(json.dumps(dict(seed=seed,exit_code=process.returncode,seconds=time.perf_counter()-start,scope='authorized full candidate diagnostic; exposed cases, not held-out qualification'),indent=2))
        print(seed,process.returncode,flush=True)
if __name__=='__main__':main()
