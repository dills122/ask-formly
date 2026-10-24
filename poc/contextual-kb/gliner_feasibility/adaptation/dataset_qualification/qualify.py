"""Annotation agreement and split checks; never scores a model or opens evaluation."""
from functools import lru_cache
import unicodedata

FIELDS=('targets','request_cues','conditions','negative_constraints','identifiers','literals',
        'versions','ui_adapters','references','resolved_antecedents','unresolved_references')

def offset(s):return (s['start'],s['end'])

def aspect_features(a):
    return {('target_anchor',*offset(a['target_anchor']))}|{(k,*offset(s)) for k in FIELDS for s in a[k]}

def global_features(r):
    return {('entity',kind,*offset(s)) for kind,spans in r['entities'].items() for s in spans}|{
        ('relation',x['kind'],*offset(x['head']),*offset(x['tail'])) for x in r['relations']}

def match_aspects(left,right):
    # Exact maximum-overlap one-to-one alignment; dummy/unmatched records earn no
    # overlap. Dataset has few asks; explicit bound avoids exponential accidents.
    if max(len(left),len(right))>12:raise ValueError('Agreement matcher supports at most12 asks; review larger cases separately')
    @lru_cache(None)
    def solve(i,used):
        if i==len(left):return (0,())
        best=solve(i+1,used);best=(best[0],((-1,i),)+best[1])
        for j in range(len(right)):
            if used&(1<<j):continue
            score,tail=solve(i+1,used|(1<<j));score+=len(left[i]&right[j])
            if score>best[0]:best=(score,((j,i),)+tail)
        return best
    return solve(0,0)

def compare_annotations(left,right):
    a={r['id']:r for r in left};b={r['id']:r for r in right}
    if len(a)!=len(left) or len(b)!=len(right) or set(a)!=set(b) or not a:
        raise ValueError('Agreement requires identical unique nonempty ID panels')
    cases=[];matches=na=nb=counts=status=0
    for key in a:
        x,y=a[key],b[key]
        if x['question']!=y['question']:raise ValueError('Question changed')
        la=[aspect_features(v) for v in x['aspects']];lb=[aspect_features(v) for v in y['aspects']]
        ga,gb=global_features(x),global_features(y)
        overlap,alignment=match_aspects(la,lb);overlap+=len(ga&gb)
        ca=sum(map(len,la))+len(ga);cb=sum(map(len,lb))+len(gb)
        matches+=overlap;na+=ca;nb+=cb
        equal_count=len(la)==len(lb);equal_status=x['status']==y['status'];counts+=equal_count;status+=equal_status
        cases.append({'id':key,'matched':overlap,'left_features':ca,'right_features':cb,
                      'f1':2*overlap/(ca+cb) if ca+cb else 1.,'aspect_counts':[len(la),len(lb)],
                      'status_agrees':equal_status,'alignment':alignment})
    result={'cases':len(a),'matched':matches,'left_features':na,'right_features':nb,
            'span_attachment_f1':2*matches/(na+nb) if na+nb else 1.,
            'aspect_count_agreement':counts/len(a),'ambiguity_agreement':status/len(a),'per_case':cases}
    result['passes_gate']=result['span_attachment_f1']>=.90 and result['aspect_count_agreement']>=.90 and result['ambiguity_agreement']>=.90
    return result

def normalized(q):return ' '.join(unicodedata.normalize('NFKC',q).casefold().split())

def validate_partitions(train,dev):
    if len({r['id'] for r in train+dev})!=len(train)+len(dev):raise ValueError('Duplicate IDs')
    if {r['family'] for r in train}&{r['family'] for r in dev}:raise ValueError('Cross-split family')
    if {normalized(r['question']) for r in train}&{normalized(r['question']) for r in dev}:
        raise ValueError('Cross-split repeated question')
    for name,rows in [('train',train),('dev',dev)]:
        if len({normalized(r['question']) for r in rows})!=len(rows):raise ValueError(f'Duplicate {name} question')
    return True

def boundary_findings(row):
    q=row['question'];findings=[]
    def inspect(s,role):
        a,b=s['start'],s['end']
        if not (0<=a<b<=len(q)) or q[a:b]!=s['text']:
            findings.append({'role':role,'text':s['text'],'reason':'invalid source offset'});return
        if (a>0 and q[a-1].isalnum() and q[a].isalnum()) or (b<len(q) and q[b-1].isalnum() and q[b].isalnum()):
            findings.append({'role':role,'text':s['text'],'start':a,'end':b,'reason':'partial alphanumeric token'})
    for a in row['aspects']:
        inspect(a['target_anchor'],'target_anchor')
        for key in FIELDS:
            for s in a[key]:inspect(s,key)
    for kind,spans in row['entities'].items():
        for s in spans:inspect(s,kind)
    for r in row['relations']:
        inspect(r['head'],r['kind']+':head');inspect(r['tail'],r['kind']+':tail')
    return findings
