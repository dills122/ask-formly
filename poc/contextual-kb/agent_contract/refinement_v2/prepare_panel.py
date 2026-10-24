import hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent

def save(name,value):
    with (P/name).open('x') as f:json.dump(value,f,indent=2,ensure_ascii=False)

def main():
    frozen=json.loads((P/'candidate-freeze.json').read_text())
    for name,h in frozen.items():
        if hashlib.sha256((P/name).read_bytes()).hexdigest()!=h:raise ValueError('Candidate changed before cases')
    cases=json.loads((P/'new-cases.json').read_text());rubric=json.loads((P/'new-rubric.json').read_text())
    if len(cases)!=24 or len(rubric)!=24 or {c['id'] for c in cases}!={f'H{i:02}' for i in range(1,25)}:raise ValueError('Bad hard panel')
    old_cases={c['id']:c for c in json.loads((P.parent/'stress_v1/cases.json').read_text())}
    old_rubric={c['id']:c for c in json.loads((P.parent/'stress_v1/rubric.json').read_text())}
    conformance={}
    for index,(source,count) in enumerate([('W01',3),('W03',3),('E01',2),('E04',2),('S05',1),('M03',1)],1):
        id=f'R{index:02}'
        cases.append(dict(old_cases[source],id=id,group='regression'))
        rubric.append(dict(old_rubric[source],id=id))
        conformance[id]={'source_case':source,'expected_questions':count}
        if source=='S05':conformance[id]['ui_adapter']='none'
    if {r['id'] for r in rubric}!={c['id'] for c in cases}:raise ValueError('Rubric mismatch')
    save('cases.json',cases);save('rubric.json',rubric);save('candidate-conformance.json',conformance)
    (P/'inputs').mkdir()
    save('inputs/forward.json',[{'id':c['id'],'request':c['request']} for c in cases])
    save('inputs/reverse.json',[{'id':c['id'],'request':c['request']} for c in reversed(cases)])
    for label,source in [('alpha','BASELINE.md'),('beta','CONTRACT.md')]:
        (P/'inputs'/label).mkdir()
        (P/'inputs'/label/'instruction.md').write_bytes((P/source).read_bytes())
    files=['BASELINE.md','CONTRACT.md','cases.json','rubric.json','candidate-conformance.json','inputs/forward.json','inputs/reverse.json','inputs/alpha/instruction.md','inputs/beta/instruction.md']
    save('panel-freeze.json',{name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in files})
if __name__=='__main__':main()
