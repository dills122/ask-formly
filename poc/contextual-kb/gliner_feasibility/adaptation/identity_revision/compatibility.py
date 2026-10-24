"""Installed-library transport and oracle representation checks; no learned claims."""
from dataclasses import replace
from types import SimpleNamespace
import torch
from gliner2 import AutoExtractor
from gliner2.processor import SamplingConfig
from gliner2.training.data import InputExample
from gliner2.models.boundary.records import RecordHead,decode_group,PackedRecordDecodeOutput,packed_record_group_to_ragged
from revision import BASE,FIELDS,export_example


def load_model():
    torch.set_num_threads(4);torch.manual_seed(1701)
    model=AutoExtractor.from_pretrained(str(BASE/'models/gliner2.5-base-v1'),
                                        local_files_only=True,map_location='cpu')
    model.float()
    model.processor.sampling_config=SamplingConfig(
        remove_json_structure_prob=0,shuffle_json_fields=False,remove_json_field_prob=0,
        remove_entities_prob=0,shuffle_entities=False,remove_entity_prob=0,
        synthetic_entity_label_prob=0,remove_relations_prob=0,swap_head_tail_prob=0,
        remove_classification_prob=0,shuffle_classification_labels=False,
        remove_classification_label_prob=0,synthetic_label_prob=0,include_true_label_prob=1)
    if model.config.boundary_head['record_instance_queries']!=32:
        raise ValueError('Unexpected native instance capacity')
    return model


def prepare(model,row):
    native=export_example(row)
    sample=InputExample.from_dict(native)
    if not sample.is_valid():raise ValueError(sample.validate())
    restored=sample.to_dict()
    for key in ('entities','json_structures','relations','record_metadata'):
        if restored['output'][key]!=native['output'][key]:raise ValueError(f'Native roundtrip changed {key}')
    return model.processor.collate_fn_train(
        [(native['input'],native['output'])],architecture='boundary',error_policy='raise',
        on_capacity_exceeded='raise',dedupe_contained_entity_spans=False)


def verify_transport(row,batch):
    def chars(pair):
        start,end=map(int,pair)
        return (batch.start_mappings[0][start],batch.end_mappings[0][end-1])
    def offsets(spans):return sorted((s['start'],s['end']) for s in spans)
    records=batch.targets.records[0]; specs=batch.record_specs[0]
    actual=[]
    for r in records:
        spec=specs[r.task_index]
        if spec.mode!='anchorless' or spec.anchor_query_id is not None:raise ValueError('Wrong record identity')
        fields={}
        for fs in spec.fields:
            target=r.field_for_query(fs.query_id)
            if any(len(v)!=1 for v in target.values):raise ValueError('Nonunique explicit occurrence')
            fields[fs.name]=sorted(chars(v[0]) for v in target.values)
        actual.append(fields)
    expected=[dict({k:offsets(a[k]) for k in FIELDS},target_anchor=offsets([a['target_anchor']])) for a in row['aspects']]
    if actual!=expected:raise ValueError(f"Record transport mismatch {row['id']}")
    layout=batch.query_layouts[0]
    entity_count=0
    for query in layout.queries:
        if query.task_type!='entities':continue
        label=query.role_name
        if label not in row['entities']:raise ValueError(f'Unknown entity label {query}')
        pairs=batch.targets.mention_pairs[0,query.query_id][batch.targets.mention_mask[0,query.query_id]]
        if sorted(chars(p) for p in pairs)!=offsets(row['entities'][label]):
            raise ValueError(f"Entity target mismatch {row['id']} {label}")
        entity_count+=len(pairs)
    pair_tensor,pair_mask,_,_,valid,_=batch.targets.edge_targets
    relation_names=list(dict.fromkeys(q.task_name for q in layout.queries if q.task_type=='relations'))
    if set(relation_names)!={'has_value','refers_to'} or int(valid.sum())!=2:
        raise ValueError('Negative relation task missing')
    edges=0
    for idx,name in enumerate(relation_names):
        pairs=pair_tensor[0,idx][pair_mask[0,idx]]
        observed=sorted((chars(p[:2]),chars(p[2:])) for p in pairs)
        gold=sorted(((r['head']['start'],r['head']['end']),
                     (r['tail']['start'],r['tail']['end'])) for r in row['relations'] if r['kind']==name)
        if observed!=gold:raise ValueError(f"Relation target mismatch {row['id']} {name}: {observed} != {gold}")
        edges+=len(pairs)
    return {'id':row['id'],'records':len(records),'entity_mentions':entity_count,
            'relation_tasks':len(relation_names),'positive_edges':edges}


def oracle_records(batch,natural_control=False):
    """Use gold candidates/scores to test capacity, never score model accuracy."""
    spec=next(iter(batch.record_specs[0].values()))
    records=batch.targets.records[0]
    if natural_control:
        anchor=next(f.query_id for f in spec.fields if f.name=='target_anchor')
        spec=replace(spec,mode='natural',anchor_query_id=anchor,
                     fields=tuple(replace(f,is_anchor=f.query_id==anchor) for f in spec.fields))
    pool=sorted({tuple(v[0]) for r in records for f in r.fields for v in f.values})
    q=max(f.query_id for f in spec.fields)+1;c=len(pool)
    membership=torch.ones((1,q,c),dtype=torch.bool)
    if natural_control:
        anchors={tuple(v[0]) for r in records for v in r.field_for_query(spec.anchor_query_id).values}
        membership[0,spec.anchor_query_id]=torch.tensor([p in anchors for p in pool])
    candidates=SimpleNamespace(indices=torch.tensor(pool)[None,None].expand(1,q,c,2),
        valid_mask=membership,query_mask=torch.ones((1,q),dtype=torch.bool),
        pair_logits=torch.full((1,q,c),10.),candidate_states=torch.zeros((1,q,c,4)))
    head=RecordHead(hidden_size=4,record_dim=4,instance_queries=32)
    dense=head.forward_group_dense(spec,torch.zeros((q,4)),candidates,0)
    group=head.forward_group(spec,torch.zeros((q,4)),candidates,0)
    expected=[]
    for r in records:
        expected.append({f.query_id:sorted(tuple(v[0]) for v in f.values)
                         for f in r.fields if f.values})
    group.object_logits=torch.full_like(group.object_logits,-10.)
    group.object_logits[:len(records)]=10.
    for fi,fs in enumerate(group.field_specs):
        scores=torch.full_like(group.assign_logits[fi],-10.)
        spans=[tuple(map(int,p)) for p in group.field_spans[fi]]
        for ri in range(min(group.num_instances,len(records))):
            wanted=expected[ri].get(fs.query_id,[])
            if not wanted:scores[ri,0]=10.
            for s in wanted:scores[ri,spans.index(s)+1]=10.
        group.assign_logits[fi]=scores
    decoded=[{k:sorted(v) for k,v in r.fields.items()} for r in decode_group(group)]
    dense_decoded=[]
    if not natural_control:
        # Carry oracle assignments through the actual dense packed transport and
        # native conversion/decoder, not only through the ragged control path.
        n=len(records)
        scores=torch.full_like(dense.assign_logits[:n],-10.)
        for ri in range(n):
            for fi,fs in enumerate(dense.field_specs):
                wanted=expected[ri].get(fs.query_id,[])
                if not wanted:scores[ri,fi,0]=10.
                for span in wanted:scores[ri,fi,pool.index(span)+1]=10.
        packed=PackedRecordDecodeOutput(
            sample_indices=torch.zeros(n,dtype=torch.long),group_indices=torch.zeros(n,dtype=torch.long),
            instance_indices=torch.arange(n),object_logits=torch.full((n,),10.),
            assign_logits=scores,field_membership=dense.field_membership[None,None],
            pool_spans=dense.pool_spans[None])
        transported=packed_record_group_to_ragged(packed,spec,0,0)
        dense_decoded=[{k:sorted(v) for k,v in r.fields.items()} for r in decode_group(transported)]
    canonical=lambda rows: sorted(rows,key=lambda r:repr(sorted(r.items())))
    return {'expected':canonical(expected),'decoded':canonical(decoded),
            'dense_decoded':canonical(dense_decoded),
            'dense_instance_count':int(dense.instance_mask.sum()),
            'ragged_instance_count':group.num_instances}
