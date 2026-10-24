"""First-save receipts from the original model, with exact fresh-load checks."""
from contextlib import contextmanager
import hashlib
import json
import random
import numpy as np
import torch

REQUIRED_LOSSES = {'total_loss', 'classification_loss', 'record_object_loss',
                   'record_field_loss', 'relation_loss'}


def write_json(path, value):
    # Fail rather than quietly stringify unsupported objects or nonfinite numbers.
    data = json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n'
    with path.open('x') as stream:
        stream.write(data)
        stream.flush()
        import os
        os.fsync(stream.fileno())


def tensor_hash(tensor):
    tensor = tensor.detach().cpu().contiguous()
    return hashlib.sha256(tensor.numpy().tobytes()).hexdigest()


def parameter_hashes(model):
    return {name: {'sha256': tensor_hash(p), 'shape': list(p.shape), 'dtype': str(p.dtype)}
            for name, p in model.named_parameters()}


def seed_all(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)


@contextmanager
def preserve_state(model):
    python_state, numpy_state, torch_state = random.getstate(), np.random.get_state(), torch.get_rng_state()
    modes = [(module, module.training) for module in model.modules()]
    gradients = {name: None if p.grad is None else p.grad.detach().clone()
                 for name, p in model.named_parameters()}
    try:
        yield
    finally:
        random.setstate(python_state); np.random.set_state(numpy_state); torch.set_rng_state(torch_state)
        for module, mode in modes: module.training = mode
        for name, p in model.named_parameters(): p.grad = gradients[name]


def validate_capture(capture, rows):
    if [c['id'] for c in capture['cases']] != [r['id'] for r in rows]:
        raise ValueError('Verification panel changed')
    for case in capture['cases']:
        if not REQUIRED_LOSSES.issubset(case['losses']):
            raise ValueError('Required auxiliary loss absent')
        if 'batch' not in case or 'output' not in case:
            raise ValueError('Missing batches or predictions')
    # Strict serialization catches NaN and unsupported metadata before any save.
    json.dumps(capture, allow_nan=False)


def execution_state(model):
    """JSON-safe entry RNG values and diagnostic mode/gradient hashes."""
    numpy_state = np.random.get_state()
    return {
        'rng': {'python': random.getstate(),
                'numpy': [numpy_state[0], numpy_state[1].tolist(), *numpy_state[2:]],
                'torch': torch.get_rng_state().tolist()},
        'modes': {name: module.training for name, module in model.named_modules()},
        'gradients': {name: None if p.grad is None else
                      {'shape': list(p.grad.shape), 'sha256': tensor_hash(p.grad)}
                      for name, p in model.named_parameters()},
    }


def verify_first_save(model, backend, rows, destination, context):
    """backend.capture observes model; no save/reload may precede before.json."""
    destination.mkdir(exist_ok=False)
    receipt = {'status': 'started', 'context': context, 'cases': len(rows)}
    original = parameter_hashes(model)
    with preserve_state(model):
        try:
            write_json(destination/'state-before.json', execution_state(model))
            if not rows or len({r['id'] for r in rows}) != len(rows):
                raise ValueError('Verification panel must be nonempty and unique')
            capture = backend.capture(model, rows)
            validate_capture(capture, rows)
            if parameter_hashes(model) != original: raise ValueError('Capture mutated original parameters')
            before = {'context': context, 'parameters': original, 'capture': capture}
            write_json(destination/'before.json', before)
            backend.save(model, destination/'adapter')
            fresh = backend.restore(destination/'adapter')
            after_capture = backend.capture(fresh, rows)
            validate_capture(after_capture, rows)
            after = {'context': context, 'parameters': parameter_hashes(fresh), 'capture': after_capture}
            write_json(destination/'after.json', after)
            differences = []
            if original != after['parameters']: differences.append('parameters')
            for left, right in zip(capture['cases'], after_capture['cases']):
                for field in ('batch', 'losses', 'output'):
                    if left[field] != right[field]: differences.append(f"{left['id']}:{field}")
            receipt['differences'] = differences
            if differences: raise ValueError('First-save parity mismatch: '+', '.join(differences))
            if parameter_hashes(model) != original: raise ValueError('Save mutated original parameters')
            receipt['before_sha256'] = hashlib.sha256((destination/'before.json').read_bytes()).hexdigest()
            receipt['after_sha256'] = hashlib.sha256((destination/'after.json').read_bytes()).hexdigest()
            receipt['artifact_hashes'] = {str(p.relative_to(destination)): hashlib.sha256(p.read_bytes()).hexdigest()
                                         for p in sorted((destination/'adapter').rglob('*')) if p.is_file()}
            if not receipt['artifact_hashes']: raise ValueError('Empty checkpoint')
            receipt['status'] = 'verified'
            return receipt
        except BaseException as exc:
            receipt.update(status='failed', error={'type': type(exc).__name__, 'message': str(exc)})
            raise
        finally:
            write_json(destination/'receipt.json', receipt)
