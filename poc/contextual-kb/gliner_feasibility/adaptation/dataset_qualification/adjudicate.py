"""Explicit human-readable adjudication decisions; never revises raw labels."""
import copy,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from pilot.contract import validate_annotation
from qualify import boundary_findings,validate_partitions

def read(name):
    value=json.loads((HERE/name).read_text());return value if isinstance(value,list) else [value]

def indexed(name):return {r['id']:r for r in read(name)}

def main():
    questions=json.loads((HERE/'questions-v3.json').read_text())
    train=indexed('train-author.json');dev=indexed('dev-author.json');independent=indexed('independent-raw.json')
    train.update(indexed('remaining-training-corrected.json'))
    dev.update(indexed('dev-replacements-author.json'));dev.update(indexed('dev-d022-v3-author.json'))
    independent.update(indexed('dev-replacements-independent.json'));independent.update(indexed('dev-d022-v3-independent.json'))
    decisions=[]
    for item in read('remaining-training-audit.json'):
        if item['decision']=='correct':decisions.append({'id':item['id'],'decision':'accept independent audit correction','reason':item['rationale']})
    choose_independent={
        'T001':'Treat which field as the complete interrogative target phrase, consistent with the component/type questions.',
        'T077':'For this field is topical target framing, not a setup condition under guide v2.',
        'D005':'Formatting and recomputation are separate operation cues on the same computed summary target, as required by same-anchor guide.',
        'D006':'The requested proposition is whether submission is allowed; do not sever its predicate from the target.',
        'D014':'The restrictive transform clause identifies which parsers are requested; it is part of the target rather than a setup condition.',
        'D026':'The requested object is Which component; the event identifies the handling operation, not the object sought.',
    }
    for key,reason in choose_independent.items():
        (train if key.startswith('T') else dev)[key]=copy.deepcopy(independent[key]);decisions.append({'id':key,'decision':'independent','reason':reason})
    decisions.extend([
        {'id':'T037','decision':'author','reason':'Retain explicit model-path/custom name occurrences and nested literal strings as well as the full array literal; source-provided names are not inferred APIs.'},
        {'id':'T045','decision':'author','reason':'Property names are sufficient placement targets; their exact values remain attached as literals. Retain supplied CSS names as user-defined identifiers, consistently with the paired training example.'},
        {'id':'T069','decision':'author','reason':'Both Which one and this are unresolved; neither is selected by the source question.'},
        {'id':'D004','decision':'author','reason':'Each error refers to the previously introduced server errors; later is temporal scope on clearing, not part of the action cue.'},
        {'id':'D015','decision':'combined','reason':'Use which type as interrogative target; preserve nested object literal and its fieldArray pairing, plus both explicitly supplied registration names as identifiers.'},
    ])
    dev['D015']=copy.deepcopy(independent['D015'])
    original=indexed('dev-author.json')['D015']
    for name in ('identifiers',):dev['D015']['aspects'][0][name]=copy.deepcopy(original['aspects'][0][name])
    dev['D015']['entities']['custom_identifier']=copy.deepcopy(original['entities']['custom_identifier'])
    for key,rows in [('train',train),('dev',dev)]:
        expected={r['id']:r['question'] for r in questions[key]}
        assert set(rows)==set(expected)
        for rid,row in rows.items():
            assert row['question']==expected[rid]
            validate_annotation(row)
            if len(row['aspects'])>32:raise ValueError('Capacity')
    # Pilot objects are included byte-for-byte semantically, without modifying source.
    pilot=json.loads((HERE.parent/'pilot/adjudicated-v2.json').read_text())
    all_train=pilot+[train[r['id']] for r in questions['train']]
    all_dev=[dev[r['id']] for r in questions['dev']]
    findings=[{'id':r['id'],'findings':boundary_findings(r)} for r in all_train+all_dev if boundary_findings(r)]
    # Family metadata stays outside strict canonical annotation rows.
    strata=list(dict.fromkeys(r['stratum'] for r in questions['train']))
    meta=[{'id':r['id'],'question':r['question'],'stratum':strata[i//4],'family':'pilot-'+r['id']} for i,r in enumerate(pilot)]+questions['train']+questions['dev']
    by_id={r['id']:r for r in meta};parent={r['id']:r['id'] for r in meta}
    def root(k):
        while parent[k]!=k:k=parent[k]
        return k
    def union(ids):
        ids=list(ids)
        for k in ids[1:]:parent[root(k)]=root(ids[0])
    # Mixed-subject reference tags are not scenario families: split those first.
    for key in ['T071','T072','T075','T076','T079','T080']:
        by_id[key]['family']='scenario-'+key
    groups={}
    for item in meta:groups.setdefault(item['family'],[]).append(item['id'])
    for ids in groups.values():union(ids)
    audit=json.loads((HERE/'family-audit.json').read_text())
    for merge in audit['same_split_family_merges']:
        if merge['split']=='train':union(merge['ids'])
    union(['P19','T077','T078'])
    for ids in [['D011','D019'],['D023','D024'],['D004','D007']]:union(ids)
    roots={key:f'family-{i+1:03}' for i,key in enumerate(sorted({root(k) for k in parent}))}
    for row in meta:row['family']=roots[root(row['id'])]
    train_meta=[by_id[r['id']] for r in all_train];dev_meta=[by_id[r['id']] for r in all_dev]
    validate_partitions(train_meta,dev_meta)
    output=HERE/'adjudicated-v1';output.mkdir(exist_ok=False)
    for name,payload in [('train',all_train),('dev',all_dev),('metadata',{'train':train_meta,'dev':dev_meta}),('decisions',decisions),('boundary-findings',findings)]:
        (output/(name+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    print({'train':len(all_train),'dev':len(all_dev),'decisions':len(decisions),'boundary_findings':len(findings),
           'train_families':len({r['family'] for r in train_meta}),'dev_families':len({r['family'] for r in dev_meta})})

if __name__=='__main__':main()
