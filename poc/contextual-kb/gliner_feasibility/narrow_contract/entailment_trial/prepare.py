"""Author-controlled development cases; no model calls."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
rows=[]
def add(pair,text,mentions):
    gold=[]
    for spec in mentions:
        fragment,role,*occ=spec; n=occ[0] if occ else 0
        start=-1
        for _ in range(n+1):start=text.index(fragment,start+1)
        gold.append([start,start+len(fragment),role])
    rows.append(dict(id=f'NLI-{len(rows)+1:02}',pair=pair,text=text,gold=sorted(gold),probes=[dict(start=a,end=b,expected_role=r,family='gold') for a,b,r in sorted(gold)]))
for name in ('willow-meter','coral-frame'):
    q=repr(name)
    add(name,f'In Formly, how do I register a custom wrapper named {q}?',[(q,'registration_name')])
    add(name,f'In Formly, how do I supply {q} as the literal caption text?',[(q,'value')])
for name in ('delivery.zone','résumé.code'):
    q=repr(name)
    add(name,f'In Formly, how do I use {q} as the model path?',[(q,'model_key')])
    add(name,f'In Formly, how do I display the literal caption {q} without treating it as a model path?',[(q,'value')])
for name in ('Material','Bootstrap'):
    add(name,f'In Formly, what changes when I use the {name} UI adapter?',[(name,'ui_adapter')])
    q=repr(name)
    add(name,f'In Formly core, how do I register a custom wrapper named {q}, without a UI adapter?',[(q,'registration_name')])
for api,expr in [('field.props.disabled','field => field.props.disabled'),('field.options.formState.reviewMode','field => field.options.formState.reviewMode')]:
    add(api,f'In Formly, how can an expression read the API path `{api}`?',[(api,'api_reference')])
    add(api,f'In Formly, how do I supply the complete expression `{expr}` as a configuration value?',[(expr,'value')])
add('prose','In Formly, what does the configuration property `type` select?',[('type','api_reference')])
add('prose','In Formly, how do I implement a reusable custom type?',[])
add('version','What changed for hidden fields in Formly v6?',[('v6','version')])
add('version',"In Formly, how do I display the literal caption 'v6'?",[("'v6'",'value')])
add('negative',"In Formly, how do I use the already registered wrapper 'spruce-shell' without registering it again?",[("'spruce-shell'",'registration_name')])
add('negative',"In Formly, how do I display the literal 'spruce-shell' without selecting a wrapper with that name?",[("'spruce-shell'",'value')])
add('repeated',"In Formly, how do I use the registered type 'lake-code' with the literal caption 'lake-code'?",[("'lake-code'",'registration_name',0),("'lake-code'",'value',1)])
add('repeated',"In Formly, how do I use the model path 'lake-code' with the literal caption 'lake-code'?",[("'lake-code'",'model_key',0),("'lake-code'",'value',1)])
with (P/'data/fresh-development.json').open('x') as f:json.dump(rows,f,indent=2,ensure_ascii=False)
