"""Pilot-only source annotation validation and lossless native training export.

No model calls, filesystem access, query construction or semantic repair.
Native format: https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/8-train_data.md
"""
from copy import deepcopy

FIELDS = ('targets','request_cues','conditions','negative_constraints','identifiers',
          'literals','versions','ui_adapters','references','resolved_antecedents',
          'unresolved_references')
ENTITY_TYPES = ('api','custom_identifier','literal','version','ui_adapter')


def validate_annotation(row):
    def require(condition, message):
        if not condition: raise ValueError(message)
    require(set(row)=={'id','question','status','aspects','entities','relations','rationale'}, 'annotation fields')
    q=row['question']
    require(isinstance(q,str) and bool(q.strip()), 'question')
    require(row['status'] in ('clear','needs_clarification'), 'status')
    def span(s):
        require(isinstance(s,dict) and set(s)=={'text','start','end'}, 'span fields')
        a,b=s['start'],s['end']
        require(type(a) is int and type(b) is int and 0<=a<b<=len(q), 'span bounds')
        require(s['text']==q[a:b], 'span text')
    def spans(xs):
        require(isinstance(xs,list), 'span list')
        for s in xs: span(s)
    require(isinstance(row['aspects'],list) and bool(row['aspects']), 'aspects')
    ids=set(); unresolved=False
    for a in row['aspects']:
        require(set(a)=={'id','target_anchor',*FIELDS}, 'aspect fields')
        require(isinstance(a['id'],str) and a['id'] not in ids, 'aspect id')
        ids.add(a['id']); span(a['target_anchor'])
        for k in FIELDS: spans(a[k])
        require(bool(a['targets']) and a['target_anchor']==min(a['targets'],key=lambda s:s['start']), 'first target anchor')
        unresolved |= bool(a['unresolved_references'])
    require(unresolved==(row['status']=='needs_clarification'), 'grounded ambiguity')
    require(isinstance(row['entities'],dict) and set(row['entities'])==set(ENTITY_TYPES), 'entity types')
    for xs in row['entities'].values(): spans(xs)
    require(isinstance(row['relations'],list), 'relations')
    for r in row['relations']:
        require(set(r)=={'kind','head','tail'} and r['kind'] in ('has_value','refers_to'), 'relation fields')
        span(r['head']); span(r['tail'])
    return row


def export_example(row):
    validate_annotation(row)
    output={
        'entities':row['entities'],
        'classifications':[{'task':'interpretation','labels':['clear','needs_clarification'],
                            'true_label':row['status'],'multi_label':False}],
        'json_structures':[{'request':{k:v for k,v in a.items() if k!='id'}} for a in row['aspects']],
        'record_metadata':{'request':{'mode':'natural','anchor':'target_anchor'}},
        'relations':[{r['kind']:{'head':r['head'],'tail':r['tail']}} for r in row['relations']],
    }
    return deepcopy({'input':row['question'],'output':output})
