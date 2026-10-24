"""Read-only reproduction of retained development aggregates and integrity checks."""
import hashlib
import json
from pathlib import Path
import statistics

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
API_GOLD = {'D01':['resetOnHide','FormControl'],
            'D04':['expressions','expressionProperties'],
            'D05':['props.placeholder'], 'D06':['defaultValue'],
            'D08':['options.formState'], 'D11':['FormlyFieldConfig<MyProps>']}


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def verify():
    samples = rows(HERE/'evidence/phase1-raw.jsonl') + rows(HERE/'evidence/phase2-raw.jsonl')
    retained = json.loads((HERE/'evidence/summary.json').read_text())
    assert retained['API_slot_gold'] == API_GOLD
    assert retained['total_calls'] == len(samples) == 123
    original = {r['case_id']:r['native'] for r in rows(BASE/'evidence/raw.jsonl') if r['repeat']==0}
    assert retained['baseline_reproduced'] == all(
        r['native']==original[r['case_id']] for r in samples if r['variant']=='E0')
    computed = {}
    for variant in [f'E{i}' for i in range(10)]:
        selected = [r for r in samples if r['variant']==variant]
        assert len(selected)==12 and {r['case_id'] for r in selected}==set(original)
        label = 'formly_api' if variant=='E9' else 'API name' if variant=='E4' else 'identifier'
        predictions = {r['case_id']:[x['text'] for x in r['native'].get('entities',{}).get(label,[])]
                       for r in selected}
        computed[variant] = {
            'calls':len(selected), 'errors':sum('error' in r for r in selected),
            'span_occurrences':sum(r.get('validated_span_occurrences',0) for r in selected),
            'median_seconds':statistics.median(r['seconds'] for r in selected),
            'requires_context_count':sum(len(r['native'].get('relation_extraction',{}).get('requires_context',[])) for r in selected),
            'refers_to_count':sum(len(r['native'].get('relation_extraction',{}).get('refers_to',[])) for r in selected),
            'API_slot_metric_applicable':variant not in ['E5','E6','E8'],
            'exact_API_slot_hits':[{'case_id':c,'text':t} for c,terms in API_GOLD.items()
                                   for t in terms if t in predictions.get(c,[])],
            'exact_API_slot_denominator':8,
            'API_slot_nonmatches':[{'case_id':c,'text':t} for c,terms in predictions.items()
                                   for t in terms if t not in API_GOLD.get(c,[])],
            'predicted_ambiguous':[r['case_id'] for r in selected
                                   if r['native'].get('interpretation',{}).get('label')=='ambiguous'],
            'ambiguity_metric_applicable':any('interpretation' in r['native'] for r in selected),
        }
    assert computed == retained['variants'], 'Aggregate mismatch'
    checks = {}
    for name,root,manifest in [
        ('protected',BASE.parent,BASE/'evidence/protected-before.json'),
        ('previous',BASE,HERE/'evidence/previous-artifacts-before.json'),
        ('phase1',BASE,HERE/'evidence/phase1-freeze.json'),
        ('phase2',BASE,HERE/'evidence/phase2-freeze.json')]:
        entries=json.loads(manifest.read_text())
        changed=[n for n,h in entries.items() if hashlib.sha256((root/n).read_bytes()).hexdigest()!=h]
        assert not changed, (name,changed)
        checks[name]={'checked':len(entries),'changed':changed}
    assert checks == json.loads((HERE/'evidence/integrity-after.json').read_text())
    return {'samples':len(samples),'aggregate_match':True,'integrity':checks}


if __name__ == '__main__':
    print(json.dumps(verify(),indent=2))
