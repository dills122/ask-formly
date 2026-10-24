"""Local frozen model loader. No training, downloads or checkpoint writes."""
import hashlib,json,os,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
POC=HERE.parents[1]
NARROW=POC/'gliner_feasibility/narrow_contract'

class IntegrityError(ValueError):
    """A positively observed frozen-model identity mismatch, never availability."""

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def parameter_hashes(model):
    return {name:hashlib.sha256(p.detach().cpu().contiguous().numpy().tobytes()).hexdigest() for name,p in model.named_parameters()}

class FrozenExtractor:
    def __init__(self,seed=1701):
        if seed not in (1701,1702):raise ValueError('Only retained seeds1701/1702 supported')
        os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HOME=str(HERE/'test-output/runtime-cache/huggingface'),TOKENIZERS_PARALLELISM='false')
        started=time.perf_counter()
        import torch
        from gliner2 import AutoExtractor
        from gliner2.processor import SamplingConfig
        from peft import PeftModel
        torch.set_num_threads(4);torch.use_deterministic_algorithms(True);torch.manual_seed(1701)
        base=AutoExtractor.from_pretrained(str(POC/'gliner_feasibility/models/gliner2.5-base-v1'),local_files_only=True,map_location='cpu').float()
        base.processor.sampling_config=SamplingConfig(remove_json_structure_prob=0,shuffle_json_fields=False,remove_json_field_prob=0,remove_entities_prob=0,shuffle_entities=False,remove_entity_prob=0,synthetic_entity_label_prob=0,remove_relations_prob=0,swap_head_tail_prob=0,remove_classification_prob=0,shuffle_classification_labels=False,remove_classification_label_prob=0,synthetic_label_prob=0,include_true_label_prob=1)
        checkpoint=NARROW/f'role_boundary_adaptation/test-output/after-{seed}'
        self.model=PeftModel.from_pretrained(base,str(checkpoint/'epoch-6/adapter'),is_trainable=False)
        self.model.eval()
        for parameter in self.model.parameters():parameter.requires_grad_(False)
        self.schema=self.model.create_schema().entities(json.loads((NARROW/'pilot/labels.json').read_text()))
        self.torch=torch;self.seed=seed
        self.before=parameter_hashes(self.model)
        expected=json.loads((checkpoint/'training-receipt.json').read_text())['final_hashes']
        if self.before!=expected:raise IntegrityError('Frozen checkpoint parameter mismatch')
        self.load_seconds=time.perf_counter()-started

    def __call__(self,text):
        with self.torch.inference_mode():
            return self.model.extract(text,self.schema,threshold=.5,overlap_policy='flat',include_spans=True,include_confidence=True)

    def verify_unchanged(self):
        after=parameter_hashes(self.model)
        if after!=self.before:raise IntegrityError('Frozen model parameters changed')
        return dict(seed=self.seed,parameter_count=len(after),parameters_unchanged=True,load_seconds=self.load_seconds,
                    threshold=.5,overlap_policy='flat',device='cpu',dtype='float32',threads=4)
