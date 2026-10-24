import copy
import random
import tempfile
import unittest
from pathlib import Path
import numpy as np
import torch
from harness import validate_rows, schedule, batch_backward, checkpoint, state_hashes, verify_manifest, train_steps, guarded_run


def row(name='one', count=1):
    return dict(id=name,text='ab cd',occurrences=[dict(start=0,end=2,text='ab',targets=[1,1,0,0,0,0,0],source_kind='api_reference')]*count)

class Tiny(torch.nn.Module):
    def __init__(self):
        super().__init__();self.lora_weight=torch.nn.Parameter(torch.zeros(7));self.register_buffer('counter',torch.tensor(0));self.frozen=torch.nn.Parameter(torch.ones(1),requires_grad=False)

class Tests(unittest.TestCase):
    def test_empty_rows_separate(self):
        a=row();b=dict(id='empty',text='nothing',occurrences=[])
        used,empty=validate_rows([a,b]);self.assertEqual(used,[a]);self.assertEqual(empty,[b])
    def test_bad_slice_duplicate_or_target_rejected(self):
        for edit in ('slice','duplicate','target','id'):
            a=row();rows=[a]
            if edit=='slice':a['occurrences'][0]['text']='wrong'
            if edit=='duplicate':a['occurrences']*=2
            if edit=='target':a['occurrences'][0]['targets']=[0,1,0,0,0,0,0]
            if edit=='id':rows*=2
            with self.assertRaises(ValueError):validate_rows(rows)
    def test_schedule_complete_cycles_and_reproducible(self):
        ids=[str(i) for i in range(216)];a=schedule(ids,1701)
        flat=sum(a,[]);self.assertEqual(len(a),124);self.assertTrue(all(len(b)==8 for b in a));self.assertEqual(len(flat),992)
        for start in range(0,864,216):self.assertEqual(set(flat[start:start+216]),set(ids))
        self.assertEqual(a,schedule(ids,1701));self.assertNotEqual(a,schedule(ids,1702))
    def test_schedule_rejects_empty_duplicate(self):
        for ids in ([],['x','x']):
            with self.assertRaises(ValueError):schedule(ids,1701)
    def test_question_mean_not_occurrence_mean(self):
        model=Tiny();a=row('a');b=row('b');b['occurrences']*=3
        # Test the loss reducer, not row validation: unequal numbers of supplied spans.
        def scorer(m,r):
            n=len(r['occurrences']);offset=0. if r['id']=='a' else 2.
            return m.lora_weight.expand(n,7)+offset,torch.tensor([o['targets'] for o in r['occurrences']],dtype=torch.float32)
        expected=sum(torch.nn.functional.binary_cross_entropy_with_logits(scorer(model,r)[0],scorer(model,r)[1]) for r in (a,b))/2
        expected.backward();want=model.lora_weight.grad.clone();model.zero_grad()
        value=batch_backward(model,[a,b],scorer)
        self.assertAlmostEqual(value,float(expected.detach()),6);self.assertTrue(torch.allclose(want,model.lora_weight.grad))
    def test_nonfinite_loss_rejected(self):
        with self.assertRaises(ValueError):batch_backward(Tiny(),[row()],lambda m,r:(torch.full((1,7),float('nan')),torch.zeros(1,7)))
    def test_checkpoint_restores_rng_mode_and_full_state(self):
        m=Tiny();m.train();before=state_hashes(m)
        random.seed(3);np.random.seed(3);torch.manual_seed(3)
        expected=(random.random(),np.random.rand(),torch.rand(1).item())
        random.seed(3);np.random.seed(3);torch.manual_seed(3)
        def save(model,path):torch.save(model.state_dict(),path/'state.pt')
        def load(path):
            random.random();np.random.rand();torch.rand(1);fresh=Tiny();fresh.load_state_dict(torch.load(path/'state.pt',weights_only=True));return fresh
        with tempfile.TemporaryDirectory() as d:
            result=checkpoint(m,Path(d)/'save',lambda model:model.lora_weight.detach().tolist(),save,load)
        actual=(random.random(),np.random.rand(),torch.rand(1).item())
        self.assertEqual(expected,actual);self.assertTrue(m.training);self.assertEqual(before,state_hashes(m));self.assertTrue(result['state_identical'])
    def test_checkpoint_catches_buffer_mutation(self):
        def load(path):m=Tiny();m.counter+=1;return m
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):checkpoint(Tiny(),Path(d)/'save',lambda m:[0],lambda m,p:None,load)
    def test_loop_fixed_budget_and_checkpoints(self):
        m=Tiny();rows={'one':row()};events=[];logs=[]
        opt=torch.optim.AdamW([m.lora_weight],lr=1e-4,weight_decay=.01)
        def scorer(model,r):return model.lora_weight.reshape(1,7),torch.tensor([[1.,1.,0.,0.,0.,0.,0.]])
        result=train_steps(m,rows,[['one']*8]*124,opt,scorer,lambda step:events.append(step),logs.append)
        self.assertEqual(events,[1,124]);self.assertEqual(len(logs),124)
        self.assertEqual(result['exposures'],992);self.assertEqual(result['changed_frozen_state'],[])
    def test_loop_rejects_frozen_parameter_in_optimizer(self):
        m=Tiny();opt=torch.optim.AdamW(m.parameters(),lr=1e-4)
        with self.assertRaises(ValueError):train_steps(m,{'one':row()},[['one']],opt,None,None,None)
    def test_final_failure_never_completes_and_all_audits_run(self):
        events=[];failures=[]
        def fail():raise ValueError('drift')
        with self.assertRaises(RuntimeError):guarded_run(lambda: 'done',[('inputs',fail),('protected',lambda:events.append('audit'))],events.append,failures.append)
        self.assertEqual(events,['audit']);self.assertEqual(failures[0][0]['phase'],'inputs')
    def test_setup_failure_is_recorded_and_audited(self):
        events=[];failures=[]
        def fail():raise ValueError('bad input')
        with self.assertRaises(RuntimeError):guarded_run(fail,[('protected',lambda:events.append('audit'))],events.append,failures.append)
        self.assertEqual(events,['audit']);self.assertEqual(failures[0][0]['phase'],'work')
    def test_manifest_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_text('changed')
            with self.assertRaises(ValueError):verify_manifest({str(p):'wrong'})

if __name__=='__main__':unittest.main()
