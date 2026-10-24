"""Native transport validation only; no optimizer or evaluation inference."""
import run
from peft import PeftModel
run.torch.set_num_threads(4)
run.torch.use_deterministic_algorithms(True)
train=run.read(run.OUT/'train.json');labels=run.read(run.NARROW/'pilot/labels.json')
results={}
for n in (1701,1702):
 model=PeftModel.from_pretrained(run.load_model(),str(run.VOCAB/f'test-output/after-{n}/epoch-6/adapter'),is_trainable=False)
 assert run.weights(model)==run.read(run.VOCAB/f'test-output/after-{n}/training-receipt.json')['final_hashes']
 for row in train:run.export(row,{});run.prepare(model,row,labels)
 results[str(n)]=dict(native_targets_checked=len(train),initial_weights_exact=True)
 del model;run.gc.collect()
run.write(run.OUT/'native-preflight.json',results)
print(results)
