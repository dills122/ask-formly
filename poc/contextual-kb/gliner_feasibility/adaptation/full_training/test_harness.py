"""Behavior tests use small real torch models; never load evaluation or GLiNER."""
import copy
import json
from pathlib import Path
import random
import tempfile
import unittest
import numpy as np
import torch
from checkpoint import verify_first_save, parameter_hashes
from harness import train_epoch, groups, select_checkpoint, run_training

HERE = Path(__file__).resolve().parent
REQUIRED = ['classification_loss', 'record_object_loss', 'record_field_loss', 'relation_loss']

class Tiny(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder_lora = torch.nn.Parameter(torch.tensor(1.0))
        self.head = torch.nn.Parameter(torch.tensor(2.0), requires_grad=False)

class Backend:
    def __init__(self, defect=None):
        self.defect = defect
        self.saved = False
        self.pre_save_observed = False

    def capture(self, model, rows):
        random.random(); np.random.rand(); torch.rand(1)
        loss = float(model.encoder_lora.detach())
        if self.saved and self.defect == 'loss': loss += 1
        terms = {name: loss for name in REQUIRED}
        if self.defect == 'serialization': terms['unsupported'] = object()
        if self.defect == 'missing': terms.pop('relation_loss')
        if self.defect == 'nonfinite': terms['relation_loss'] = float('nan')
        return {'cases': [{'id': r['id'], 'batch': [1, 3] if self.saved and self.defect == 'batch' else [1, 2], 'losses': dict(terms, total_loss=loss),
                           'output': ({'request': [{'target': 'changed'}]} if self.saved and self.defect == 'output'
                                      else {'request': [{'target': 'wrapper'}, {'target': 'wrapper'}]})}
                          for r in rows]}

    def save(self, model, path):
        self.pre_save_observed = (path.parent/'before.json').exists()
        self.assert_before = json.loads((path.parent/'before.json').read_text())
        path.mkdir()
        self.model = copy.deepcopy(model)
        if self.defect == 'parameter':
            with torch.no_grad(): self.model.encoder_lora.add_(1)
        (path/'weights.json').write_text('{}')
        self.saved = True

    def restore(self, path):
        return self.model

class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=HERE/'test-output')
        self.root = Path(self.temp.name)
        self.rows = [{'id': 'P01'}, {'id': 'P02'}]
        self.context = {'seed': 1701, 'epoch': 1, 'step': 1,
                        'base_sha': 'base', 'schema_sha': 'schema', 'config_sha': 'config'}
    def tearDown(self): self.temp.cleanup()

    def test_original_receipt_before_first_save_and_state_preserved(self):
        model = Tiny(); model.eval(); model.encoder_lora.grad = torch.tensor(3.)
        hashes = parameter_hashes(model)
        random.seed(11); np.random.seed(11); torch.manual_seed(11)
        expected = (random.random(), np.random.rand(), torch.rand(1).item())
        random.seed(11); np.random.seed(11); torch.manual_seed(11)
        backend = Backend()
        report = verify_first_save(model, backend, self.rows, self.root/'checkpoint', self.context)
        self.assertTrue(backend.pre_save_observed)
        state=json.loads((self.root/'checkpoint/state-before.json').read_text())
        self.assertEqual(set(state['rng']),{'python','numpy','torch'})
        self.assertEqual(state['gradients']['encoder_lora']['shape'],[])
        self.assertFalse(state['modes'][''])
        self.assertEqual(report['status'], 'verified')
        self.assertEqual(report['context'], self.context)
        self.assertEqual(hashes, parameter_hashes(model))
        self.assertFalse(model.training)
        self.assertEqual(model.encoder_lora.grad.item(), 3.)
        self.assertEqual(expected, (random.random(), np.random.rand(), torch.rand(1).item()))
        before = json.loads((self.root/'checkpoint/before.json').read_text())
        self.assertEqual(before['parameters'], hashes)
        self.assertEqual(len(before['capture']['cases'][0]['output']['request']), 2)

    def test_corruptions_cannot_receive_verified_receipt(self):
        for defect in ['loss', 'parameter', 'batch', 'missing', 'nonfinite', 'output', 'serialization']:
            with self.subTest(defect=defect):
                path = self.root/defect
                with self.assertRaises((ValueError, AssertionError, TypeError)):
                    verify_first_save(Tiny(), Backend(defect), self.rows, path, self.context)
                self.assertEqual(json.loads((path/'receipt.json').read_text())['status'], 'failed')

    def test_existing_directory_is_never_overwritten(self):
        path = self.root/'existing'; path.mkdir(); (path/'keep').write_text('old')
        with self.assertRaises(FileExistsError):
            verify_first_save(Tiny(), Backend(), self.rows, path, self.context)
        self.assertEqual((path/'keep').read_text(), 'old')

class TrainingTests(unittest.TestCase):
    def test_120_examples_form_eight_updates_including_partial_eight(self):
        batches = list(groups(list(range(120)), 2, 8))
        self.assertEqual([sum(map(len, g)) for g in batches], [16]*7+[8])

    def test_partial_accumulation_matches_actual_example_mean(self):
        rows = [{'x': x} for x in (1., 2., 4., 8., 16.)]
        def loss(model, row): return (model.encoder_lora-row['x'])**2
        a, b = Tiny(), Tiny()
        oa = torch.optim.SGD([a.encoder_lora], lr=.1)
        ob = torch.optim.SGD([b.encoder_lora], lr=.1)
        train_epoch(a, rows, oa, lambda m,rs: torch.stack([loss(m,r) for r in rs]).mean(), batch_size=2, accumulation=8, clip=1e9)
        torch.stack([loss(b,r) for r in rows]).mean().backward(); ob.step()
        self.assertTrue(torch.allclose(a.encoder_lora,b.encoder_lora))
        self.assertIsNone(a.encoder_lora.grad)

    def test_nonfinite_loss_stops_before_update(self):
        model = Tiny(); before = parameter_hashes(model)
        opt = torch.optim.SGD([model.encoder_lora], lr=.1)
        with self.assertRaises(ValueError):
            train_epoch(model, [{}], opt, lambda m,r: m.encoder_lora*float('nan'))
        self.assertEqual(before, parameter_hashes(model))

    def test_complete_eight_epoch_run_and_first_save_gate(self):
        with tempfile.TemporaryDirectory(dir=HERE/'test-output') as td:
            model = Tiny(); calls=[]
            def verify(m, epoch, step): calls.append((epoch,step)); return {'status':'verified'}
            result=run_training(model, [{'id':str(i),'x':2.} for i in range(120)],
                torch.optim.SGD([model.encoder_lora],lr=.01),
                lambda m,rs:torch.stack([(m.encoder_lora-r['x'])**2 for r in rs]).mean(), verify,
                lambda m,e: [{'epoch':e}], Path(td), seed=1701)
            self.assertEqual(result['steps'],64)
            self.assertEqual(calls,[(e,e*8) for e in range(1,9)])
            self.assertEqual(result['status'],'completed')

    def test_failed_checkpoint_stops_before_dev_or_next_epoch(self):
        with tempfile.TemporaryDirectory(dir=HERE/'test-output') as td:
            model=Tiny(); calls=[]
            with self.assertRaises(ValueError):
                run_training(model,[{'id':str(i),'x':2.} for i in range(120)],
                    torch.optim.SGD([model.encoder_lora],lr=.01),
                    lambda m,rs:torch.stack([(m.encoder_lora-r['x'])**2 for r in rs]).mean(),
                    lambda *args:{'status':'failed'}, lambda *args:calls.append(1), Path(td),seed=1701)
            self.assertEqual(calls,[])
            report=json.loads((Path(td)/'run.json').read_text())
            self.assertEqual(report['status'],'failed');self.assertEqual(report['steps'],8)

    def test_selection_uses_grades_then_errors_then_earliest(self):
        entries=[{'epoch':e,'complete':20,'critical':1 if e==1 else 0,
                  'cases':30,'verified':True} for e in range(1,9)]
        self.assertEqual(select_checkpoint(entries)['epoch'],2)
        entries[5]['complete']=21
        self.assertEqual(select_checkpoint(entries)['epoch'],6)
        with self.assertRaises(ValueError):select_checkpoint(entries[:-1])
        entries[0]['verified']=False
        with self.assertRaises(ValueError):select_checkpoint(entries)

if __name__=='__main__': unittest.main()
