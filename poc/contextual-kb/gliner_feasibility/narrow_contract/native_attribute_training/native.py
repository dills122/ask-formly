"""Thin pinned GLiNER native attribute transport and supplied-span audit."""
import sys,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;NARROW=HERE.parent
sys.path.insert(0,str(NARROW/'supervised_trial'))
from train import load_model,weights,write,seed
from gliner2 import AttributeGroup
from gliner2.training.data import InputExample
from peft import PeftModel
import torch
from transport import ROLES,export
LABELS=json.loads((NARROW/'pilot/labels.json').read_text())
def schema(model):return model.create_schema().entities(LABELS).entity_attributes({'target_role':AttributeGroup(list(ROLES),multi_label=False,qualify_labels=True)})
def prepare(model,row,bad):
 sample=export(row,bad);sample['output']['entity_descriptions']={**LABELS,**{'target_role: '+r:'' for r in ROLES}}
 obj=InputExample.from_dict(sample)
 if not obj.is_valid() or obj.to_dict()!=sample:raise ValueError('InputExample roundtrip')
 batch=model.processor.collate_fn_train([(sample['input'],sample['output'])],architecture='boundary',error_policy='raise',on_capacity_exceeded='raise',dedupe_contained_entity_spans=False)
 seen=set()
 for q in batch.query_layouts[0].queries:
  if q.task_type!='entities':raise ValueError('not span target')
  seen.add(q.role_name);pairs=batch.targets.mention_pairs[0,q.query_id][batch.targets.mention_mask[0,q.query_id]]
  actual=sorted((batch.start_mappings[0][int(a)],batch.end_mappings[0][int(b)-1]) for a,b in pairs)
  expected=sorted((m['start'],m['end']) for m in sample['output']['entities'][q.role_name])
  if actual!=expected:raise ValueError('target offsets '+str(row.get('question_id'))+' '+q.role_name+' '+str((actual,expected)))
 if seen!=set(sample['output']['entities']):raise ValueError('missing query incl absent labels')
 return batch

def supplied(model,text,offsets):
 """Calls native attribute force-scorer. Does not extract, repair or guess offsets."""
 base=model.get_base_model() if hasattr(model,'get_base_model') else model
 sch=schema(model);schemas,metadata=base._build_schema_dicts_and_metadata([sch])
 batch=model.processor.collate_fn_inference([(text,schemas[0])],architecture='boundary',error_policy='raise')
 core=base._encode_core(batch)
 starts={v:k for k,v in batch.start_mappings[0].items()} if isinstance(batch.start_mappings[0],dict) else {v:k for k,v in enumerate(batch.start_mappings[0])}
 ends={v:k+1 for k,v in batch.end_mappings[0].items()} if isinstance(batch.end_mappings[0],dict) else {v:k+1 for k,v in enumerate(batch.end_mappings[0])}
 decoded={'api_reference':[]};coords={};result=[]
 for a,b in offsets:
  if a not in starts or b not in ends or not 0<=a<b<=len(text):
   result.append(dict(start=a,end=b,status='unaligned'));continue
  item=dict(start=a,end=b,text=text[a:b],confidence=1.);decoded['api_reference'].append(item);coords[id(item)]=(starts[a],ends[b])
 base._attach_entity_attributes(0,core,core['ext_specs'][0],metadata[0],decoded,coords)
 for item in decoded['api_reference']:
  result.append(dict(start=item['start'],end=item['end'],status='scored',**item['target_role']))
 return sorted(result,key=lambda x:(x['start'],x['end']))
