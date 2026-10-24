"""Check label transport only. No inference, backward, optimizer or evaluation."""
import json,os,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
OUT=HERE/'native-transport-v1'
OUT.mkdir(exist_ok=False)
(OUT/'.cache/tmp').mkdir(parents=True)
os.environ.update(HF_HOME=str(OUT/'.cache/hf'),HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',
                  TOKENIZERS_PARALLELISM='false',TMPDIR=str(OUT/'.cache/tmp'))
FULL=HERE.parent/'full_training';REV=HERE.parent/'identity_revision';PILOT=HERE.parent/'pilot';BASE=HERE.parents[1]
sys.path.insert(0,str(FULL))
from inputs import access_policy
allowed=list(FULL.glob('*.py'))+list(REV.glob('*.py'))+list(PILOT.glob('*.py'))+[HERE/'native_transport.py',HERE/'adjudicated-v1/train.json',HERE/'adjudicated-v1/dev.json']
sys.addaudithook(access_policy(HERE.parents[4],allowed,OUT,[BASE/'env',BASE/'models']))
from native import load_model,prepare,verify_transport
model=load_model()
report={'scope':'strict native preprocessing only','optimizer_steps':0,'inference_calls':0,'cases':[],'failures':[]}
for split in ('train','dev'):
    rows=json.loads((HERE/'adjudicated-v1'/f'{split}.json').read_text())
    for row in rows:
        try:report['cases'].append(dict(verify_transport(row,prepare(model,row)),split=split))
        except Exception as exc:report['failures'].append({'id':row['id'],'type':type(exc).__name__,'message':str(exc)})
report['status']='passed' if not report['failures'] else 'failed'
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'passed':len(report['cases']),'failures':report['failures']},indent=2))
raise SystemExit(bool(report['failures']))
