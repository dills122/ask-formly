"""Supplemental all-logit parity; reads existing artifacts, no optimizer."""
import json
from unittest.mock import patch
from check import HERE, OUT, NARROW, load_model, PeftModel, torch, score, native, read, write, digest


def main():
    torch.set_num_threads(4); torch.use_deterministic_algorithms(True)
    rows = read(OUT/'panel.json')
    # JSON stores pairs as lists; scorer deliberately accepts unique tuple offsets.
    for row in rows:
        row['offsets'] = [tuple(x) for x in row['offsets']]
    write(OUT/'supplemental-freeze.json',{str(HERE/'check_all_logits.py'):digest(HERE/'check_all_logits.py')})
    reports = []
    for number in (1701,1702):
        for kind, path in (
            ('baseline', NARROW/f'role_boundary_adaptation/test-output/after-{number}/epoch-6/adapter'),
            ('disposable', OUT/str(number)/'disposable-adapter'),
        ):
            model = PeftModel.from_pretrained(load_model(),str(path),is_trainable=False);model.eval()
            base = model.get_base_model(); original = base.boundary_head.score_explicit_spans
            records = []
            for row in rows:
                captured = []
                def capture(*args, **kwargs):
                    z = original(*args, **kwargs); captured.append(z.detach().clone()); return z
                with torch.no_grad():
                    expected, aligned, unsupported, _ = score(model,row['text'],row['offsets'])
                    with patch.object(base.boundary_head,'score_explicit_spans',side_effect=capture):
                        attached = native(model,row['text'],row['offsets'])
                assert len(captured) == 1 and len(attached) == len(aligned) == len(row['offsets']) and not unsupported
                actual = captured[0][0].T / base.boundary_settings.pair_temperature
                assert actual.shape == expected.shape
                assert torch.allclose(actual,expected,atol=1e-5,rtol=1e-5)
                records.append(dict(id=row['id'], logits=actual.tolist(), max_difference=float((actual-expected).abs().max())))
            reports.append(dict(seed=number,kind=kind,records=records))
            del model,base
            import gc
            gc.collect()
    write(OUT/'all-logit-parity.json',reports)
    print('all-logit parity passed: four adapters x eight questions',flush=True)

if __name__=='__main__':main()
