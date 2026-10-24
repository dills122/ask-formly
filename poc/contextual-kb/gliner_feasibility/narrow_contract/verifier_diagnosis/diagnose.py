"""Read-only development-cache diagnosis plus synthetic native decoder reproduction."""
import collections
import json
import sys
from pathlib import Path
from types import SimpleNamespace,MethodType
HERE=Path(__file__).resolve().parent
NARROW=HERE.parent
sys.path.insert(0,str(NARROW/'verifier_evaluation'))
from runtime import read,write,protect,verify_manifest
from decisions import groups,ROLES
from gliner2.models.boundary.engine import BoundaryExtractor
from gliner2.inference.runtime import ExtractorRuntimeMixin

# Exercise actual native entity decoding, without an encoder or model weights.
fake=SimpleNamespace(boundary_settings=SimpleNamespace(abstention_threshold=.5))
fake._attach_entity_attributes=MethodType(BoundaryExtractor._attach_entity_attributes,fake)
fake._format_spans=MethodType(ExtractorRuntimeMixin._format_spans,fake)
names=['api_reference','value']
specs=[dict(task_type='entities',field_name=n) for n in names]
decoded=BoundaryExtractor._decode_entities(fake,0,{},specs,[[(.9,0,1)],[(.8,0,1)]],dict(entity_order=names),None,'flat',0,[0],[1],'x',1,True,True)
eligible,blocked,_=groups('x',{'entities':decoded})
assert eligible==[(0,1)] and not blocked
result={'synthetic_decoder':dict(role_names=list(decoded),eligible_groups=eligible,no_encoder=True), 'seeds':{}}
rows_by_seed=read(NARROW/'verifier_evaluation/test-output/full-calibration-v1/calibration-outputs.json')
for seed,rows in rows_by_seed.items():
 counts=collections.Counter();failures=[];baseline_errors=[]
 for row in rows:
  raw={(m['start'],m['end'],k) for k,ms in row['raw']['entities'].items() for m in ms};gold={tuple(x) for x in row['gold']}
  e,b,spans=groups(row['text'],row['raw']);counts['eligible']+=len(e);counts['blocked']+=len(b)
  counts['raw_mentions']+=len(raw);counts['raw_correct']+=len(raw&gold)
  for a,z,k in gold:
   if (a,z,k) in raw:counts['gold_exact']+=1
   elif any(a==i and z==j for i,j,r in raw):counts['gold_same_span_wrong_role']+=1
   elif any(a<j and i<z for i,j,r in raw):counts['gold_partial_only']+=1
   else:counts['gold_no_proposal']+=1
  for a,z,k in raw-gold:baseline_errors.append(dict(id=row['id'],text=row['text'][a:z],role=k))
  for probe in row['probes']:
   expected=probe['expected_role'];p=probe['probabilities']
   if expected is None:continue
   top=max(range(6),key=lambda i:p[i+1]);passing=[r for r,v in zip(ROLES,p[1:]) if v>=.5]
   good=p[0]>=.5 and passing==[expected]
   counts['top_role_correct']+=ROLES[top]==expected
   if not good:
    failures.append(dict(id=row['id'],text=row['text'][probe['start']:probe['end']],expected=expected,probabilities=p,top_role=ROLES[top],passing=passing))
 result['seeds'][seed]=dict(counts=dict(counts),failures=failures,baseline_errors=baseline_errors)
training=read(NARROW/'verifier_training_plan/test-output/training-labels.json')
result['training_surface_counts']={word:dict(collections.Counter(o['source_kind'] for r in training for o in r['occurrences'] if o['targets'][0] and o['text']==word)) for word in ('type','expressions','defaultValue','Material',"'invoice-entry'",'[]')}
write(HERE/'test-output/diagnosis.json',result)
checks={name:verify_manifest(read(NARROW/'verifier_evaluation/test-output'/name)) for name in ('full-run-final-freeze.json','sealed-preparation-freeze.json')}
audit=protect();write(HERE/'test-output/preservation.json',dict(manifests=checks,protected=audit,model_predictions_run=False,sealed_contents_inspected=False))
print(json.dumps(dict(synthetic_decoder=result['synthetic_decoder'],seeds={s:r['counts'] for s,r in result['seeds'].items()},protected=sum(x['checked'] for x in audit))))
