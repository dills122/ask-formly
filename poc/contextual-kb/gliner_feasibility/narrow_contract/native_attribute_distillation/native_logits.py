"""Differentiable public native span primitive, no new head or copied engine."""
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;PRIOR=HERE.parent/'native_attribute_training'
sys.path.insert(0,str(PRIOR))
from native import schema,ROLES,torch
sys.path.insert(0,str(HERE))

def inverse_mapping(mapping,shift=0):
 return {v:k+shift for k,v in (mapping.items() if isinstance(mapping,dict) else enumerate(mapping))}

def validate_offsets(text,offsets):
 if len(offsets)!=len(set(offsets)) or any(type(a)!=int or type(b)!=int or not 0<=a<b<=len(text) for a,b in offsets):raise ValueError('duplicate or invalid offset')
 return offsets

def logits(model,text,offsets):
 validate_offsets(text,offsets)
 base=model.get_base_model() if hasattr(model,'get_base_model') else model
 # Schema serialization remains existing private transport; scoring itself is public.
 schemas,_=base._build_schema_dicts_and_metadata([schema(model)])
 batch=model.processor.collate_fn_inference([(text,schemas[0])],architecture='boundary',error_policy='raise')
 starts=inverse_mapping(batch.start_mappings[0]);ends=inverse_mapping(batch.end_mappings[0],1)
 aligned=[(a,b) for a,b in offsets if a in starts and b in ends and 0<=a<b<=len(text)]
 unsupported=[(a,b) for a,b in offsets if (a,b) not in aligned]
 if not aligned:raise ValueError('no representable supplied spans')
 encoded=base.encode(batch)
 by_name={q.role_name:q.query_id for q in encoded.query_layouts[0].queries if q.task_type=='entities'}
 query_ids=[by_name['target_role: '+r] for r in ROLES]
 indices=torch.tensor([(starts[a],ends[b]) for a,b in aligned],dtype=torch.long,device=encoded.text_states.device).view(1,1,len(aligned),2).expand(1,encoded.query_states.shape[1],len(aligned),2)
 scores=base.score_explicit_spans(encoded,indices)[0,query_ids,:].transpose(0,1)/base.boundary_settings.pair_temperature
 return scores,aligned,unsupported,query_ids
