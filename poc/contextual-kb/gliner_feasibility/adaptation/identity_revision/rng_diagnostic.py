import random,json,torch
from revision import HERE,load_pilot
from compatibility import load_model,prepare
from training_smoke import tensor_hash

def fingerprint(value):
    if torch.is_tensor(value):return {'shape':list(value.shape),'hash':tensor_hash(value)}
    if isinstance(value,dict):return {str(k):fingerprint(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [fingerprint(v) for v in value]
    if hasattr(value,'__dict__'):return fingerprint(vars(value))
    return value

if __name__=='__main__':
    model=load_model();row=load_pilot()[0];result={}
    for mode in ['torch_only','torch_and_python']:
        batches=[]
        for _ in range(2):
            torch.manual_seed(1701)
            if mode=='torch_and_python':random.seed(1701)
            batches.append(fingerprint(prepare(model,row)))
        result[mode]={'equal':batches[0]==batches[1],'batches':batches}
    (HERE/'evidence/rng-diagnostic.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
    print({k:v['equal'] for k,v in result.items()})
