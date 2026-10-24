"""Execute full-text and optional-probe requests on the immutable DB."""
import json,os,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parents[1]
sys.path.insert(0,str(POC))
from bridge import readonly,retrieve,relevance
from extract import read,write,sha,verify
from agent_contract.qualification_v3.candidate import build_plan
from kbcompiler.question_pilot import PilotIndex

def main():
 verify()
 if not read(HERE/'test-output/extraction/completion.json')['complete']:raise ValueError('extraction incomplete')
 out=HERE/'test-output/retrieval';out.mkdir(exist_ok=False)
 os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(HERE/'test-output/embed-cache'),HF_HUB_OFFLINE='1')
 records=read(HERE/'data/records.json');cases={r['id']:r for r in read(HERE/'data/cases.json')};gold=read(HERE/'data/gold.json')
 plans={arm:{r['id']:r['plan'] for r in map(json.loads,(HERE/f'test-output/extraction/{arm}.jsonl').read_text().splitlines())} for arm in ('foundation','1701','1702')}
 plans['oracle']={}
 for r in records:
  hints=[dict(question_index=g['question_index'],**m) for g in gold if g['record_id']==r['id'] for m in g['gold']]
  plans['oracle'][r['id']]=build_plan(r['request'],r['output'],hints)
 dbpath=POC/'build/knowledge.sqlite';before=sha(dbpath)
 with readonly(dbpath) as db:
  started=time.perf_counter();index=PilotIndex(db);setup=time.perf_counter()-started
  write(out/'setup.json',dict(seconds=setup,facts=len(index.ids),db_hash=before))
  with (out/'results.jsonl').open('x') as f:
   for number,r in enumerate(records):
    arms=['foundation','1701','1702','oracle'];arms=arms[number%4:]+arms[:number%4]
    for arm in arms:
     result=retrieve(index,plans[arm][r['id']],arm!='foundation')
     result.update(id=r['id'],batch=r['batch'],arm=arm,metrics={str(k):relevance(result['ids'],cases[r['id']],k) for k in (4,8)})
     f.write(json.dumps(result,allow_nan=False)+'\n');f.flush()
  if sha(dbpath)!=before:raise ValueError('DB changed')
 verify();write(out/'completion.json',dict(complete=True,records=36,arms=['foundation','1701','1702','oracle'],db_unchanged=sha(dbpath)==before))
 write(HERE/'test-output/retrieval-freeze.json',{str(p):sha(p) for p in out.iterdir() if p.is_file()})
if __name__=='__main__':main()
