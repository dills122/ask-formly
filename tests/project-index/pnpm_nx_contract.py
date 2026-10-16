"""Full-flow contract shared by offline regressions and real pnpm qualification."""
import json
from pathlib import Path
import subprocess
import sys
REPO=Path(__file__).resolve().parents[2]
SCRIPT=REPO/'skill/ask-formly/scripts/project_index.py'
CONTEXT='apps/admin/tsconfig.app.json'

def call(root,command,*args,expected=0):
    r=subprocess.run([sys.executable,str(SCRIPT),command,'--root',str(root),*args],capture_output=True,text=True,timeout=330)
    assert r.returncode==expected,r.stdout+r.stderr
    return json.loads(r.stdout)

def verify(root,g):
    nodes={n['id']:n for n in g['nodes']}
    assert g['mode']=='typescript-static' and g['workspace']['mode']=='exported-graph'
    assert {p['name'] for p in g['workspace']['projects']}=={'admin','portal','forms','form-helpers','fields','validation'}
    assert {n['context'] for n in nodes.values()}=={CONTEXT}
    assert all(not n['file'].startswith('apps/portal/') for n in nodes.values())
    for prefix,owner in {'apps/admin/':'admin','libs/forms/':'forms','libs/form-helpers/':'form-helpers','libs/fields/':'fields','libs/validation/':'validation'}.items():
        matching=[n for n in nodes.values() if n['file'].startswith(prefix)]
        assert matching and all(n['projects']==[owner] for n in matching),prefix
    def node(name,kind):
        found=[n for n in nodes.values() if n['name']==name and n['kind']==kind]
        assert len(found)==1,(name,kind,found)
        return found[0]
    def edge(a,relation,b):
        found=[e for e in g['edges'] if e['from']==a['id'] and e['to']==b['id'] and e['relation']==relation]
        assert len(found)==1,(a['name'],relation,b['name'])
        return found[0]
    chain=[node(name,kind) for name,kind in [('suppliers','route'),('SupplierComponent','class'),('formly-form','form-host'),('fields','declaration'),('buildSupplierFields','function'),('billing','field-config'),('addressFields','declaration'),('accountCode','field-config')]]
    relations=['route-component','renders','binds-fields','assigned-from','contains-field','references','contains-field']
    for a,relation,b in zip(chain,relations,chain[1:]):edge(a,relation,b)
    entry=node('FormlyModule.forRoot','entry-point')
    assert entry['file']=='apps/admin/src/main.ts'
    implementations=[]
    for name,relation,implname,kind in [('account-code','type-candidate','AccountCodeType','class'),('section-panel','wrapper-candidate','SectionPanelWrapper','class'),('accountCode','validator-candidate','accountCodeValidator','function')]:
        reg=node(name,'registration');impl=node(implname,kind)
        assert edge(chain[-1],relation,reg)['evidence']=='registration-scope-unresolved'
        edge(reg,'implementation',impl);edge(entry,'registers',reg)
        assert reg['scope']==entry['id'];implementations.append(impl)
    for source,target in [('admin','forms'),('admin','fields'),('forms','form-helpers'),('fields','validation')]:
        assert any(d['target']==target for d in g['workspace']['dependencies'][source]),(source,target)
    assert {i['reason'] for i in g['unresolved']}=={'nx-export-freshness-unverified'},g['unresolved']
    trace=call(root,'trace','--query','suppliers','--context',CONTEXT,'--depth','10','--limit','100')
    assert all(n['id'] in {t['id'] for t in trace['nodes']} for n in chain+implementations)
    assert not trace['truncated']
    assert call(root,'check')['status']=='fresh'
    return {'chain':[f"{a['name']} --{relation}--> {b['name']}" for a,relation,b in zip(chain,relations,chain[1:])],
        'implementations':[{k:n[k] for k in ['name','file','projects','context']} for n in implementations],
        'trace_nodes':len(trace['nodes']),'trace_edges':len(trace['edges']),'trace_truncated':trace['truncated'],'unresolved':g['unresolved'],'status':'pass'}
