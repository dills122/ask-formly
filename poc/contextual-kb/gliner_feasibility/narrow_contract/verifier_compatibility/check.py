"""Offline compatibility only: frozen baselines plus two disposable one-step verifiers."""
import gc
import hashlib
import importlib.metadata
import json
import sys
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
NARROW = HERE.parent
ROOT = HERE.parents[4]
OUT = HERE / 'test-output'
sys.path.insert(0, str(NARROW / 'supervised_trial'))
from train import load_model, weights, seed, write, PeftModel, torch
sys.path.insert(0, str(HERE))
from verifier import score, schema, decide, objective, align, ROLES


def read(path):
    return json.loads(path.read_text())


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def protect(name):
    prior = NARROW / 'native_attribute_distillation_trial/test-output'
    manifests = [ROOT / r['manifest'] for r in read(prior / 'protected-after.json')]
    manifests.append(prior / 'final-freeze.json')
    reports = []
    for manifest in manifests:
        data = read(manifest); changed = []
        for key, expected in data.items():
            p = Path(key)
            if not p.is_absolute():
                p = ROOT / p if p.parts[0] == 'poc' else manifest.parent.parent / p
            if not p.exists() or digest(p) != expected:
                changed.append(str(p))
        reports.append(dict(manifest=str(manifest.relative_to(ROOT)), checked=len(data), changed=changed))
    write(OUT / name, reports)
    assert not any(r['changed'] for r in reports)
    print('protected', sum(r['checked'] for r in reports), flush=True)


def panel():
    source = NARROW / 'native_attribute_distillation/test-output/panel.json'
    selected = read(source)
    rows = read(NARROW / 'native_attribute_contrast/test-output/train.json')[:194]
    bad = read(NARROW / 'native_attribute_training/test-output/training-negatives.json')
    assert len(selected['rows']) == 8
    assert selected['rows'] == [dict(row=rows[i], negative=bad[i]) for i in selected['indices']]
    result = []
    for item in selected['rows']:
        row = item['row']; entries = {}
        for m in row['mentions']:
            y = [1.] + [float(r == m['kind']) for r in ROLES]
            entries[(m['start'], m['end'])] = y
        for m in item['negative']['negatives']:
            key = (m['start'], m['end']); assert key not in entries
            entries[key] = [0.] * 7
        result.append(dict(id=row['question_id'], text=row['question'], offsets=list(entries), targets=list(entries.values())))
    write(OUT / 'panel.json', result)
    return result


def native(model, text, offsets, override=None):
    base = model.get_base_model() if hasattr(model, 'get_base_model') else model
    schemas, metadata = base._build_schema_dicts_and_metadata([schema(model)])
    batch = model.processor.collate_fn_inference([(text, schemas[0])], architecture='boundary', error_policy='raise')
    supported, unsupported, tokens = align(text, offsets, batch.start_mappings[0], batch.end_mappings[0])
    core = base._encode_core(batch)
    decoded = {'candidate': []}; coords = {}
    for (a, b), pair in zip(supported, tokens):
        item = dict(start=a, end=b, text=text[a:b], confidence=1.)
        decoded['candidate'].append(item); coords[id(item)] = pair
    original = base.boundary_head.score_explicit_spans
    def intercept(*args, **kwargs):
        z = original(*args, **kwargs)
        if override is not None:
            # Native attribute force-scoring query order follows schema group/label order.
            assert z.shape[1] == 7
            z = torch.tensor(override, dtype=z.dtype, device=z.device).reshape(1, 7, 1).expand_as(z) * base.boundary_settings.pair_temperature
        return z
    with patch.object(base.boundary_head, 'score_explicit_spans', side_effect=intercept):
        base._attach_entity_attributes(0, core, core['ext_specs'][0], metadata[0], decoded, coords)
    return decoded['candidate']


def verify(model, rows):
    records = []; max_diff = 0.
    with torch.no_grad():
        for row in rows:
            z, supported, unsupported, _ = score(model, row['text'], row['offsets'])
            assert supported == row['offsets'] and not unsupported
            attached = native(model, row['text'], row['offsets'])
            probabilities = z.sigmoid()
            for i, (item, span) in enumerate(zip(attached, supported)):
                assert (item['start'], item['end']) == span and item['text'] == row['text'][span[0]:span[1]]
                for group, labels, start in (('boundary', ['complete'], 0), ('supported_role', ROLES, 1)):
                    actual = {v['label']: v['confidence'] for v in item[group]}
                    expected = {r: float(probabilities[i, start+j]) for j, r in enumerate(labels) if probabilities[i,start+j] >= .5}
                    assert actual.keys() == expected.keys()
                    for r in actual:
                        diff = abs(actual[r]-expected[r]); max_diff = max(max_diff, diff); assert diff < 1e-5
            records.append(dict(id=row['id'], offsets=supported, logits=z.tolist(), native=attached, decisions=[decide(v) for v in z]))
        # Same text at two occurrences and non-token offset: no searching/snapping.
        text = "In Formly, compare 'echo' with 'echo'."
        a = text.index("'echo'"); b = text.rindex("'echo'")
        offsets = [(b,b+6),(a,a+6),(a+2,a+6)]
        z, supported, unsupported, _ = score(model,text,offsets)
        assert supported == offsets[:2] and unsupported == offsets[2:]
        assert [(v['start'],v['end']) for v in native(model,text,supported)] == supported
        modes = {'none':[8,-8,-8,-8,-8,-8,-8], 'one':[8,8,-8,-8,-8,-8,-8], 'many':[8,8,8,-8,-8,-8,-8], 'boundary_veto':[-8,8,-8,-8,-8,-8,-8]}
        synthetic = {}
        for name, logits in modes.items():
            item = native(model,text,[offsets[0]],logits)[0]
            decision = decide(torch.tensor(logits,dtype=torch.float32))
            assert [r['label'] for r in item['supported_role']] == decision['supported_roles']
            assert bool(item['boundary']) == decision['boundary_pass']
            synthetic[name] = dict(native=item, decision=decision)
    return dict(records=records, max_native_probability_difference=max_diff, repeated_offsets=supported,
                unsupported_offsets=unsupported, synthetic_native_decisions=synthetic)


def predictions(model, rows):
    with torch.no_grad():
        return [score(model,r['text'],r['offsets'])[0].tolist() for r in rows]


def main():
    torch.set_num_threads(4); torch.use_deterministic_algorithms(True)
    protect('protected-before.json')
    rows = panel()
    files = list(HERE.glob('*.py')) + [HERE/'PROTOCOL.md', OUT/'panel.json']
    write(OUT/'input-freeze.json', {str(p):digest(p) for p in files})
    write(OUT/'environment.json', {n:importlib.metadata.version(n) for n in ('torch','gliner2','peft')})
    for number in (1701,1702):
        folder = OUT / str(number); folder.mkdir()
        path = NARROW/f'role_boundary_adaptation/test-output/after-{number}/epoch-6/adapter'
        baseline = PeftModel.from_pretrained(load_model(),str(path),is_trainable=False); baseline.eval()
        before = weights(baseline)
        report = verify(baseline,rows)
        assert weights(baseline) == before and all(p.grad is None and not p.requires_grad for p in baseline.parameters())
        write(folder/'baseline-schema-check.json',report)
        del baseline; gc.collect()
        model = load_model(); seed(number)
        model = model.apply_lora(r=8,alpha=16.,dropout=0.,targets=['encoder','extractive_head']); model.eval()
        initial = weights(model); params = [p for p in model.parameters() if p.requires_grad]
        names = [n for n,p in model.named_parameters() if p.requires_grad]
        assert names and all('lora_' in n for n in names)
        optimizer = torch.optim.SGD(params,lr=1e-4); optimizer.zero_grad(set_to_none=True)
        losses = []
        for row in rows:
            z, supported, unsupported, _ = score(model,row['text'],row['offsets'])
            assert supported == row['offsets'] and not unsupported
            loss = objective(z,torch.tensor(row['targets'])) / len(rows)
            loss.backward(); losses.append(float(loss.detach()))
        norm = sum(float(p.grad.square().sum()) for p in params if p.grad is not None)**.5
        assert norm > 0 and all(p.grad is None or torch.isfinite(p.grad).all() for p in params)
        optimizer.step()
        final = weights(model); changed = [n for n in initial if initial[n] != final[n]]
        assert changed and all(n in names for n in changed)
        before_save = predictions(model,rows)
        model.save_pretrained(str(folder/'disposable-adapter'))
        reloaded = PeftModel.from_pretrained(load_model(),str(folder/'disposable-adapter'),is_trainable=False); reloaded.eval()
        assert weights(reloaded) == final and predictions(reloaded,rows) == before_save
        write(folder/'verifier-schema-check.json',verify(reloaded,rows))
        write(folder/'step-receipt.json',dict(seed=number,steps=1,loss=sum(losses),gradient_norm=norm,
            changed_lora_tensors=len(changed),changed_frozen_tensors=0,first_save_parameters_identical=True,
            first_save_predictions_identical=True,baseline_parameters_unchanged=True,trainable_names=names))
        print('seed',number,'compatibility passed',flush=True)
        del model,reloaded,optimizer,params; gc.collect()
    assert all(digest(Path(p)) == h for p,h in read(OUT/'input-freeze.json').items())
    protect('protected-after.json')

if __name__ == '__main__': main()
