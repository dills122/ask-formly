"""Supplemental saved-adapter reserialization parity; no optimization.

This cannot reconstruct uncaptured losses from the original pre-first-save model.
"""
import json
import random
from rng_diagnostic import fingerprint
import os
import sys
from revision import HERE,load_pilot,check_access
os.environ.update(HF_HOME=str(HERE/'.cache/hf'),HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',
                  TOKENIZERS_PARALLELISM='false',TMPDIR=str(HERE/'.cache/tmp'))
import torch
from peft import PeftModel
from compatibility import load_model,prepare
from training_smoke import predictions,tensor_hash


def measure_losses(model,rows):
    model.train();values=[]
    with torch.no_grad():
        for index,row in enumerate(rows):
            torch.manual_seed(1701+index)
            random.seed(1701+index)
            batch=prepare(model,row)
            batch_fingerprint=fingerprint(batch)
            out=model(batch,gold_injection_prob=1.)
            required={'classification_loss','record_object_loss','record_field_loss','relation_loss'}
            if not required.issubset(out.losses):raise AssertionError('Missing auxiliary losses')
            terms={'total_loss':float(out.total_loss)}
            terms.update({k:float(v) for k,v in out.losses.items() if torch.is_tensor(v) and v.numel()==1})
            if not all(torch.isfinite(torch.tensor(v)) for v in terms.values()):raise AssertionError('Nonfinite loss')
            values.append({'id':row['id'],'losses':terms,'batch':batch_fingerprint})
    return values


def verify_reload():
    dest=HERE/'reload-supplement-v3';dest.mkdir(exist_ok=False)
    report={'status':'started','optimizer_steps':0,
            'scope':'saved-adapter reserialization; original pre-first-save losses were not captured'}
    try:
        rows=load_pilot();sys.addaudithook(check_access)
        model=PeftModel.from_pretrained(load_model(),str(HERE/'smoke-run/adapter'),is_trainable=False)
        before_hashes={n:tensor_hash(p) for n,p in model.named_parameters()}
        losses=measure_losses(model,rows)
        outputs=predictions(model,rows)
        model.save_pretrained(str(dest/'adapter'))
        fresh=PeftModel.from_pretrained(load_model(),str(dest/'adapter'),is_trainable=False)
        after_hashes={n:tensor_hash(p) for n,p in fresh.named_parameters()}
        after_losses=measure_losses(fresh,rows)
        after_outputs=predictions(fresh,rows)
        report.update(cases=len(rows),losses_equal=losses==after_losses,
                      parameters_equal=before_hashes==after_hashes,outputs_equal=outputs==after_outputs,
                      batches_equal=[v['batch'] for v in losses]==[v['batch'] for v in after_losses])
        for name,data in [('before-losses',losses),('after-losses',after_losses),
                          ('before-parameters',before_hashes),('after-parameters',after_hashes),
                          ('before-outputs',outputs),('after-outputs',after_outputs)]:
            (dest/(name+'.json')).write_text(json.dumps(data,indent=2,ensure_ascii=False,default=str)+'\n')
        if not all(report[k] for k in ['losses_equal','parameters_equal','outputs_equal']):
            raise AssertionError('Reserialization mismatch')
        report['status']='completed';return report
    except BaseException as exc:
        report['status']='failed';report['error']={'type':type(exc).__name__,'message':str(exc)}
        raise
    finally:(dest/'report.json').write_text(json.dumps(report,indent=2)+'\n')
